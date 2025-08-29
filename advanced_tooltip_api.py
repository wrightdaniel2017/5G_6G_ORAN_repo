#!/usr/bin/env python3
"""
Advanced Tooltip Management API
Additional Flask routes for enhanced tooltip functionality
"""

from flask import Flask, request, jsonify, render_template
import json
import os
from datetime import datetime, timedelta
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedTooltipManager:
    def __init__(self, app):
        self.app = app
        self.db_path = 'tooltip_analytics.db'
        self.init_database()
        self.setup_routes()
        
    def init_database(self):
        """Initialize SQLite database for tooltip analytics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables for analytics
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tooltip_interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                acronym TEXT NOT NULL,
                action TEXT NOT NULL,
                duration INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT,
                page_url TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                results_count INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_id TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_acronyms (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                acronym TEXT UNIQUE NOT NULL,
                definition TEXT NOT NULL,
                category TEXT,
                priority TEXT DEFAULT 'medium',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")

    def setup_routes(self):
        """Setup Flask routes for advanced tooltip management"""
        
        @self.app.route('/api/tooltips/search', methods=['POST'])
        def smart_search():
            """Advanced search endpoint with fuzzy matching"""
            try:
                data = request.get_json()
                query = data.get('query', '').strip().lower()
                max_results = data.get('max_results', 10)
                
                if len(query) < 2:
                    return jsonify({
                        'success': False,
                        'error': 'Query must be at least 2 characters'
                    }), 400
                
                # Log search query
                self.log_search_query(query)
                
                # Get all acronyms
                from enhanced_app_v2 import load_acronyms
                acronym_data = load_acronyms()
                
                results = []
                acronyms = acronym_data['acronyms']
                categories = acronym_data['categories']
                
                # Create reverse category lookup
                category_lookup = {}
                for category, category_acronyms in categories.items():
                    for acronym in category_acronyms:
                        category_lookup[acronym] = category
                
                # Search algorithm
                for acronym, definition in acronyms.items():
                    score = 0
                    
                    # Exact acronym match (highest priority)
                    if query == acronym.lower():
                        score = 100
                    elif query in acronym.lower():
                        score = 80
                    elif acronym.lower().startswith(query):
                        score = 70
                    elif query in definition.lower():
                        # Calculate partial definition match score
                        words = definition.lower().split()
                        query_words = query.split()
                        matches = sum(1 for word in query_words if any(word in def_word for def_word in words))
                        score = min(60, matches * 20)
                    
                    if score > 0:
                        results.append({
                            'acronym': acronym,
                            'definition': definition,
                            'category': category_lookup.get(acronym, 'General'),
                            'score': score
                        })
                
                # Sort by score and limit results
                results = sorted(results, key=lambda x: x['score'], reverse=True)[:max_results]
                
                return jsonify({
                    'success': True,
                    'query': query,
                    'results': results,
                    'total_found': len(results)
                })
                
            except Exception as e:
                logger.error(f"Search error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Search failed'
                }), 500
        
        @self.app.route('/api/tooltips/related/<acronym>', methods=['GET'])
        def get_related_acronyms(acronym):
            """Get related acronyms based on category and semantic relationships"""
            try:
                from enhanced_app_v2 import load_acronyms
                acronym_data = load_acronyms()
                
                if acronym not in acronym_data['acronyms']:
                    return jsonify({
                        'success': False,
                        'error': 'Acronym not found'
                    }), 404
                
                # Find category
                user_category = None
                for category, category_acronyms in acronym_data['categories'].items():
                    if acronym in category_acronyms:
                        user_category = category
                        break
                
                related = []
                
                # Add category-based related items
                if user_category:
                    category_acronyms = acronym_data['categories'][user_category]
                    for related_acronym in category_acronyms[:5]:  # Limit to 5
                        if related_acronym != acronym:
                            related.append({
                                'acronym': related_acronym,
                                'definition': acronym_data['acronyms'][related_acronym],
                                'category': user_category,
                                'relation_type': 'category'
                            })
                
                # Add semantic relationships
                semantic_relations = self.get_semantic_relations()
                if acronym in semantic_relations:
                    for related_acronym in semantic_relations[acronym][:3]:  # Limit to 3
                        if related_acronym in acronym_data['acronyms']:
                            # Find category for related acronym
                            related_category = 'General'
                            for cat, cat_acronyms in acronym_data['categories'].items():
                                if related_acronym in cat_acronyms:
                                    related_category = cat
                                    break
                            
                            related.append({
                                'acronym': related_acronym,
                                'definition': acronym_data['acronyms'][related_acronym],
                                'category': related_category,
                                'relation_type': 'semantic'
                            })
                
                return jsonify({
                    'success': True,
                    'acronym': acronym,
                    'related': related[:6]  # Max 6 related items
                })
                
            except Exception as e:
                logger.error(f"Related acronyms error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to get related acronyms'
                }), 500
        
        @self.app.route('/api/tooltips/analytics', methods=['POST'])
        def log_tooltip_interaction():
            """Log tooltip interaction for analytics"""
            try:
                data = request.get_json()
                acronym = data.get('acronym')
                action = data.get('action')
                duration = data.get('duration')
                user_id = data.get('user_id', 'anonymous')
                page_url = data.get('page_url', request.referrer)
                
                if not acronym or not action:
                    return jsonify({
                        'success': False,
                        'error': 'Acronym and action are required'
                    }), 400
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT INTO tooltip_interactions 
                    (acronym, action, duration, user_id, page_url)
                    VALUES (?, ?, ?, ?, ?)
                ''', (acronym, action, duration, user_id, page_url))
                
                conn.commit()
                conn.close()
                
                return jsonify({
                    'success': True,
                    'message': 'Interaction logged'
                })
                
            except Exception as e:
                logger.error(f"Analytics logging error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to log interaction'
                }), 500
        
        @self.app.route('/api/tooltips/analytics/dashboard', methods=['GET'])
        def get_analytics_dashboard():
            """Get analytics dashboard data"""
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                # Most popular acronyms (last 30 days)
                cursor.execute('''
                    SELECT acronym, COUNT(*) as count
                    FROM tooltip_interactions
                    WHERE timestamp > datetime('now', '-30 days')
                    GROUP BY acronym
                    ORDER BY count DESC
                    LIMIT 10
                ''')
                popular_acronyms = [{'acronym': row[0], 'interactions': row[1]} for row in cursor.fetchall()]
                
                # Search statistics
                cursor.execute('''
                    SELECT COUNT(*) as total_searches,
                           COUNT(DISTINCT query) as unique_queries
                    FROM search_queries
                    WHERE timestamp > datetime('now', '-30 days')
                ''')
                search_stats = cursor.fetchone()
                
                # Daily interaction trends (last 7 days)
                cursor.execute('''
                    SELECT date(timestamp) as day, COUNT(*) as interactions
                    FROM tooltip_interactions
                    WHERE timestamp > datetime('now', '-7 days')
                    GROUP BY date(timestamp)
                    ORDER BY day
                ''')
                daily_trends = [{'date': row[0], 'interactions': row[1]} for row in cursor.fetchall()]
                
                # Top search queries
                cursor.execute('''
                    SELECT query, COUNT(*) as count
                    FROM search_queries
                    WHERE timestamp > datetime('now', '-30 days')
                    GROUP BY query
                    ORDER BY count DESC
                    LIMIT 5
                ''')
                top_searches = [{'query': row[0], 'count': row[1]} for row in cursor.fetchall()]
                
                conn.close()
                
                return jsonify({
                    'success': True,
                    'data': {
                        'popular_acronyms': popular_acronyms,
                        'search_stats': {
                            'total_searches': search_stats[0] or 0,
                            'unique_queries': search_stats[1] or 0
                        },
                        'daily_trends': daily_trends,
                        'top_searches': top_searches
                    }
                })
                
            except Exception as e:
                logger.error(f"Analytics dashboard error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to load analytics'
                }), 500
        
        @self.app.route('/api/tooltips/custom', methods=['POST'])
        def add_custom_acronym():
            """Add custom acronym to the database"""
            try:
                data = request.get_json()
                acronym = data.get('acronym', '').strip().upper()
                definition = data.get('definition', '').strip()
                category = data.get('category', 'Custom')
                priority = data.get('priority', 'medium')
                
                if not acronym or not definition:
                    return jsonify({
                        'success': False,
                        'error': 'Acronym and definition are required'
                    }), 400
                
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                try:
                    cursor.execute('''
                        INSERT INTO custom_acronyms (acronym, definition, category, priority)
                        VALUES (?, ?, ?, ?)
                    ''', (acronym, definition, category, priority))
                    
                    conn.commit()
                    
                    return jsonify({
                        'success': True,
                        'message': 'Custom acronym added successfully',
                        'acronym': {
                            'acronym': acronym,
                            'definition': definition,
                            'category': category,
                            'priority': priority
                        }
                    })
                    
                except sqlite3.IntegrityError:
                    return jsonify({
                        'success': False,
                        'error': 'Acronym already exists'
                    }), 400
                    
                finally:
                    conn.close()
                
            except Exception as e:
                logger.error(f"Add custom acronym error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to add custom acronym'
                }), 500
        
        @self.app.route('/api/tooltips/custom', methods=['GET'])
        def get_custom_acronyms():
            """Get all custom acronyms"""
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT acronym, definition, category, priority, created_at
                    FROM custom_acronyms
                    ORDER BY created_at DESC
                ''')
                
                custom_acronyms = []
                for row in cursor.fetchall():
                    custom_acronyms.append({
                        'acronym': row[0],
                        'definition': row[1],
                        'category': row[2],
                        'priority': row[3],
                        'created_at': row[4]
                    })
                
                conn.close()
                
                return jsonify({
                    'success': True,
                    'custom_acronyms': custom_acronyms
                })
                
            except Exception as e:
                logger.error(f"Get custom acronyms error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to get custom acronyms'
                }), 500
        
        @self.app.route('/api/tooltips/pronunciation/<acronym>', methods=['GET'])
        def get_pronunciation(acronym):
            """Get pronunciation guide for acronym"""
            pronunciations = {
                '5G': 'five-jee',
                '6G': 'six-jee', 
                'OFDM': 'oh-eff-dee-em',
                'MIMO': 'my-moh',
                'QoS': 'kwahs',
                'URLLC': 'ur-el-el-see',
                'eMBB': 'ee-em-bee-bee',
                'mMTC': 'em-em-tee-see',
                'gNB': 'gee-en-bee',
                'eNB': 'ee-en-bee',
                'AMF': 'ay-em-eff',
                'SMF': 'es-em-eff',
                'UPF': 'you-pee-eff',
                'AUSF': 'oh-you-es-eff',
                'UDM': 'you-dee-em',
                'PCF': 'pee-see-eff',
                'NSSF': 'en-es-es-eff',
                'NRF': 'en-ar-eff',
                'NEF': 'en-ee-eff',
                'BPSK': 'bee-pee-es-kay',
                'QPSK': 'kyoo-pee-es-kay',
                'QAM': 'kwam',
                'IoT': 'eye-oh-tee',
                'IIoT': 'eye-eye-oh-tee',
                'API': 'ay-pee-eye',
                'HTTP': 'aych-tee-tee-pee',
                'HTTPS': 'aych-tee-tee-pee-es',
                'TCP': 'tee-see-pee',
                'UDP': 'you-dee-pee',
                'WiFi': 'why-fy',
                'VoIP': 'voyp'
            }
            
            pronunciation = pronunciations.get(acronym.upper(), acronym)
            
            return jsonify({
                'success': True,
                'acronym': acronym,
                'pronunciation': pronunciation,
                'has_audio': acronym.upper() in pronunciations
            })
        
        @self.app.route('/api/tooltips/context-suggestions', methods=['POST'])
        def get_context_suggestions():
            """Get acronym suggestions based on page content"""
            try:
                data = request.get_json()
                content = data.get('content', '').lower()
                
                # Context mapping for suggestions
                context_map = {
                    'network': ['5G', '6G', 'LTE', 'Wi-Fi', 'SDN', 'NFV', 'ORAN', 'RAN'],
                    'security': ['TLS', 'SSL', 'VPN', 'PKI', 'OAuth', 'JWT', 'AES', 'RSA'],
                    'radio': ['RF', 'mmWave', 'MIMO', 'OFDM', 'BPSK', 'QPSK', 'QAM'],
                    'core': ['AMF', 'SMF', 'UPF', '5GC', 'EPC', 'HSS', 'MME'],
                    'iot': ['IoT', 'NB-IoT', 'LoRa', 'MQTT', 'CoAP', 'LPWAN', 'M2M'],
                    'protocol': ['HTTP', 'TCP', 'UDP', 'IP', 'SIP', 'RTP', 'QUIC'],
                    'modulation': ['BPSK', 'QPSK', 'QAM', '16-QAM', '64-QAM', 'OFDM'],
                    'performance': ['BER', 'SNR', 'QoS', 'KPI', 'SLA', 'RSSI', 'RSRP']
                }
                
                suggestions = set()
                words = content.split()
                
                for word in words:
                    for context, acronyms in context_map.items():
                        if context in word:
                            suggestions.update(acronyms)
                
                # Limit suggestions and add definitions
                from enhanced_app_v2 import load_acronyms
                acronym_data = load_acronyms()
                
                suggestion_list = []
                for acronym in list(suggestions)[:8]:  # Limit to 8 suggestions
                    if acronym in acronym_data['acronyms']:
                        suggestion_list.append({
                            'acronym': acronym,
                            'definition': acronym_data['acronyms'][acronym]
                        })
                
                return jsonify({
                    'success': True,
                    'suggestions': suggestion_list
                })
                
            except Exception as e:
                logger.error(f"Context suggestions error: {e}")
                return jsonify({
                    'success': False,
                    'error': 'Failed to get suggestions'
                }), 500

    def log_search_query(self, query):
        """Log search query to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO search_queries (query, results_count)
                VALUES (?, ?)
            ''', (query, 0))  # Results count will be updated separately
            
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to log search query: {e}")

    def get_semantic_relations(self):
        """Define semantic relationships between acronyms"""
        return {
            '5G': ['6G', 'NR', 'mmWave', 'Sub-6', 'eMBB', 'URLLC', 'mMTC', 'gNB'],
            '6G': ['5G', 'THz', 'AI', 'ML', 'Holographic'],
            'MIMO': ['SU-MIMO', 'MU-MIMO', 'Massive MIMO', 'Beamforming'],
            'AMF': ['SMF', 'UPF', '5GC', 'AUSF', 'UDM', 'PCF'],
            'BPSK': ['QPSK', 'QAM', '16-QAM', '64-QAM', 'Modulation'],
            'TCP': ['UDP', 'IP', 'HTTP', 'HTTPS', 'Protocol'],
            'IoT': ['IIoT', 'M2M', 'WSN', 'LoRa', 'NB-IoT', 'LTE-M'],
            'SSL': ['TLS', 'HTTPS', 'PKI', 'Certificate', 'Encryption'],
            'Wi-Fi': ['802.11', 'WLAN', 'Access Point', 'SSID'],
            'VoIP': ['SIP', 'RTP', 'H.323', 'Voice', 'Telephony']
        }

# This will be imported and used in the main Flask app
def setup_advanced_tooltips(app):
    """Setup advanced tooltip management for Flask app"""
    return AdvancedTooltipManager(app)
