#!/usr/bin/env python3
"""
Tooltip System Management Utility
Utilities for managing the enhanced telecommunications tooltip system
"""

import os
import json
import sqlite3
import argparse
from datetime import datetime, timedelta
import csv

class TooltipSystemManager:
    def __init__(self, db_path='tooltip_analytics.db'):
        self.db_path = db_path
        self.ensure_database()

    def ensure_database(self):
        """Ensure the database exists and is properly structured"""
        if not os.path.exists(self.db_path):
            print(f"Creating database: {self.db_path}")
            
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
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
        print("✅ Database structure verified")

    def import_acronyms(self, file_path):
        """Import acronyms from JSON or CSV file"""
        print(f"📥 Importing acronyms from: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"❌ File not found: {file_path}")
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        imported_count = 0
        skipped_count = 0
        
        try:
            if file_path.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                if 'acronyms' in data:
                    acronyms = data['acronyms']
                else:
                    acronyms = data
                    
                for acronym, definition in acronyms.items():
                    try:
                        cursor.execute('''
                            INSERT INTO custom_acronyms (acronym, definition, category)
                            VALUES (?, ?, ?)
                        ''', (acronym, definition, 'Imported'))
                        imported_count += 1
                    except sqlite3.IntegrityError:
                        skipped_count += 1
                        
            elif file_path.endswith('.csv'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    
                    for row in reader:
                        acronym = row.get('acronym', '').strip().upper()
                        definition = row.get('definition', '').strip()
                        category = row.get('category', 'Imported').strip()
                        
                        if acronym and definition:
                            try:
                                cursor.execute('''
                                    INSERT INTO custom_acronyms (acronym, definition, category)
                                    VALUES (?, ?, ?)
                                ''', (acronym, definition, category))
                                imported_count += 1
                            except sqlite3.IntegrityError:
                                skipped_count += 1
            
            conn.commit()
            print(f"✅ Import completed: {imported_count} added, {skipped_count} skipped")
            
        except Exception as e:
            print(f"❌ Import error: {e}")
        finally:
            conn.close()

    def export_acronyms(self, file_path, format='json'):
        """Export all custom acronyms to file"""
        print(f"📤 Exporting acronyms to: {file_path}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT acronym, definition, category FROM custom_acronyms ORDER BY acronym')
        rows = cursor.fetchall()
        
        try:
            if format.lower() == 'json':
                export_data = {
                    'acronyms': {row[0]: row[1] for row in rows},
                    'categories': {},
                    'exported_at': datetime.now().isoformat(),
                    'total_count': len(rows)
                }
                
                # Group by categories
                for row in rows:
                    category = row[2] or 'General'
                    if category not in export_data['categories']:
                        export_data['categories'][category] = []
                    export_data['categories'][category].append(row[0])
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                    
            elif format.lower() == 'csv':
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['acronym', 'definition', 'category'])
                    writer.writerows(rows)
            
            print(f"✅ Export completed: {len(rows)} acronyms exported")
            
        except Exception as e:
            print(f"❌ Export error: {e}")
        finally:
            conn.close()

    def generate_analytics_report(self, days=30):
        """Generate analytics report for the specified period"""
        print(f"📊 Generating analytics report for last {days} days...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Most popular acronyms
        cursor.execute('''
            SELECT acronym, COUNT(*) as interactions
            FROM tooltip_interactions
            WHERE timestamp > ?
            GROUP BY acronym
            ORDER BY interactions DESC
            LIMIT 10
        ''', (start_date.isoformat(),))
        popular_acronyms = cursor.fetchall()
        
        # Search statistics
        cursor.execute('''
            SELECT COUNT(*) as total_searches,
                   COUNT(DISTINCT query) as unique_queries
            FROM search_queries
            WHERE timestamp > ?
        ''', (start_date.isoformat(),))
        search_stats = cursor.fetchone()
        
        # Daily interaction trends
        cursor.execute('''
            SELECT DATE(timestamp) as day, COUNT(*) as interactions
            FROM tooltip_interactions
            WHERE timestamp > ?
            GROUP BY DATE(timestamp)
            ORDER BY day
        ''', (start_date.isoformat(),))
        daily_trends = cursor.fetchall()
        
        # Generate report
        report = {
            'period': f'{start_date.date()} to {end_date.date()}',
            'popular_acronyms': [{'acronym': row[0], 'interactions': row[1]} for row in popular_acronyms],
            'search_statistics': {
                'total_searches': search_stats[0] if search_stats else 0,
                'unique_queries': search_stats[1] if search_stats else 0
            },
            'daily_trends': [{'date': row[0], 'interactions': row[1]} for row in daily_trends]
        }
        
        # Save report
        report_file = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Analytics report saved: {report_file}")
        
        # Display summary
        print("\n📈 Analytics Summary:")
        print(f"   Total interactions: {sum(trend['interactions'] for trend in report['daily_trends'])}")
        print(f"   Total searches: {report['search_statistics']['total_searches']}")
        print(f"   Unique queries: {report['search_statistics']['unique_queries']}")
        
        if popular_acronyms:
            print(f"\n🔥 Top 5 Most Popular Acronyms:")
            for i, acronym in enumerate(popular_acronyms[:5], 1):
                print(f"   {i}. {acronym[0]} ({acronym[1]} interactions)")
        
        conn.close()

    def cleanup_old_data(self, days=90):
        """Remove old analytics data to keep database size manageable"""
        print(f"🧹 Cleaning up data older than {days} days...")
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Clean old interactions
        cursor.execute('DELETE FROM tooltip_interactions WHERE timestamp < ?', (cutoff_date.isoformat(),))
        interactions_deleted = cursor.rowcount
        
        # Clean old searches
        cursor.execute('DELETE FROM search_queries WHERE timestamp < ?', (cutoff_date.isoformat(),))
        searches_deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ Cleanup completed: {interactions_deleted} interactions, {searches_deleted} searches removed")

    def system_status(self):
        """Display system status and statistics"""
        print("🔍 Tooltip System Status:")
        print("=" * 50)
        
        # Check database
        if os.path.exists(self.db_path):
            print(f"✅ Database: {self.db_path}")
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Count records
            cursor.execute('SELECT COUNT(*) FROM tooltip_interactions')
            interactions = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM search_queries')
            searches = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM custom_acronyms')
            custom_acronyms = cursor.fetchone()[0]
            
            print(f"   📊 Total interactions: {interactions}")
            print(f"   🔍 Total searches: {searches}")
            print(f"   📝 Custom acronyms: {custom_acronyms}")
            
            conn.close()
        else:
            print(f"❌ Database not found: {self.db_path}")
        
        # Check files
        files_to_check = [
            'enhanced_app_v2.py',
            'advanced_tooltip_api.py',
            'static/js/telecom_tooltips.js',
            'static/js/tooltip_enhancements.js',
            'static/css/tooltips.css',
            'static/css/tooltip_enhancements.css'
        ]
        
        print("\n📁 File Status:")
        for file_path in files_to_check:
            if os.path.exists(file_path):
                size = os.path.getsize(file_path)
                print(f"   ✅ {file_path} ({size:,} bytes)")
            else:
                print(f"   ❌ {file_path} (missing)")

def main():
    parser = argparse.ArgumentParser(description='Tooltip System Management Utility')
    parser.add_argument('--db', default='tooltip_analytics.db', help='Database file path')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Import command
    import_parser = subparsers.add_parser('import', help='Import acronyms from file')
    import_parser.add_argument('file', help='JSON or CSV file to import')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export acronyms to file')
    export_parser.add_argument('file', help='Output file path')
    export_parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Export format')
    
    # Analytics command
    analytics_parser = subparsers.add_parser('analytics', help='Generate analytics report')
    analytics_parser.add_argument('--days', type=int, default=30, help='Number of days to analyze')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up old data')
    cleanup_parser.add_argument('--days', type=int, default=90, help='Keep data newer than X days')
    
    # Status command
    subparsers.add_parser('status', help='Show system status')
    
    # Init command
    subparsers.add_parser('init', help='Initialize database')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = TooltipSystemManager(args.db)
    
    if args.command == 'import':
        manager.import_acronyms(args.file)
    elif args.command == 'export':
        manager.export_acronyms(args.file, args.format)
    elif args.command == 'analytics':
        manager.generate_analytics_report(args.days)
    elif args.command == 'cleanup':
        manager.cleanup_old_data(args.days)
    elif args.command == 'status':
        manager.system_status()
    elif args.command == 'init':
        print("✅ Database initialized")

if __name__ == '__main__':
    main()
