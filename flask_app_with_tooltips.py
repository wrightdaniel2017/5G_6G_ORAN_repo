#!/usr/bin/env python3
"""
Enhanced Flask Telecommunications Laboratory with Tooltip System
Professional web application for 5G/6G telecommunications education
"""

from flask import Flask, render_template, jsonify, send_from_directory, request
import json
import os
from datetime import datetime
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.config['SECRET_KEY'] = 'telecom_lab_2025'

# Load acronyms database
def load_acronyms():
    """Load the telecommunications acronyms database"""
    acronym_data = {
        "acronyms": {
            "5G": "Fifth Generation - The latest standard for broadband cellular networks",
            "6G": "Sixth Generation - Next-generation wireless technology beyond 5G", 
            "NR": "New Radio - The radio access technology for 5G networks",
            "ORAN": "Open Radio Access Network - An initiative to disaggregate RAN functions",
            "O-RAN": "Open Radio Access Network - An open and intelligent RAN architecture",
            "RAN": "Radio Access Network - Part of a mobile telecommunication system",
            "BER": "Bit Error Rate - The percentage of bits with errors relative to total bits transmitted",
            "SNR": "Signal-to-Noise Ratio - Measure of signal strength relative to background noise",
            "BPSK": "Binary Phase Shift Keying - Digital modulation technique using phase changes",
            "QPSK": "Quadrature Phase Shift Keying - Digital modulation technique using four phase states",
            "QAM": "Quadrature Amplitude Modulation - Digital modulation scheme using amplitude and phase",
            "16-QAM": "16-Quadrature Amplitude Modulation - QAM using 16 distinct amplitude and phase combinations",
            "64-QAM": "64-Quadrature Amplitude Modulation - QAM using 64 distinct amplitude and phase combinations",
            "RF": "Radio Frequency - Electromagnetic wave frequencies used for radio communication",
            "ADC": "Analog-to-Digital Converter - Converts analog signals to digital format",
            "DAC": "Digital-to-Analog Converter - Converts digital signals to analog format",
            "OFDM": "Orthogonal Frequency Division Multiplexing - Modulation technique using multiple subcarriers",
            "MIMO": "Multiple-Input Multiple-Output - Technology using multiple antennas at transmitter and receiver",
            "eMBB": "Enhanced Mobile Broadband - 5G service category for high-speed data applications",
            "URLLC": "Ultra-Reliable Low Latency Communication - 5G service category for mission-critical applications",
            "mMTC": "Massive Machine Type Communication - 5G service category for IoT applications",
            "IoT": "Internet of Things - Network of interconnected devices and sensors",
            "VoIP": "Voice over Internet Protocol - Technology for voice communication over IP networks",
            "Wi-Fi": "Wireless Fidelity - Wireless local area networking technology",
            "LTE": "Long Term Evolution - Standard for wireless broadband communication (4G)",
            "mmWave": "Millimeter Wave - High-frequency radio waves (24-100 GHz)",
            "QoS": "Quality of Service - Network performance measurement and management",
            "API": "Application Programming Interface - Set of protocols for building software applications"
        },
        "categories": {
            "Modulation": ["BPSK", "QPSK", "QAM", "16-QAM", "64-QAM", "OFDM"],
            "Network Architecture": ["5G", "6G", "LTE", "ORAN", "O-RAN", "RAN"],
            "Performance Metrics": ["BER", "SNR", "QoS"],
            "Radio Technologies": ["MIMO", "mmWave", "RF", "NR", "eMBB", "URLLC", "mMTC"],
            "IoT": ["IoT", "VoIP", "Wi-Fi"]
        }
    }
    return acronym_data

@app.route('/')
def index():
    """Main telecommunications laboratory page with tooltips"""
    return render_template('index.html')

@app.route('/analytics')
def analytics_dashboard():
    """Analytics dashboard for tooltip usage insights"""
    return render_template('analytics_dashboard.html')

@app.route('/tooltip_test')
def tooltip_test():
    """Tooltip testing and demonstration page"""
    return render_template('tooltip_test.html')

@app.route('/printable')
def printable():
    """Printable version of the lab"""
    return render_template('index_printable.html')

@app.route('/animation_test')
def animation_test():
    """Animation test page"""
    return render_template('animation_test.html')

@app.route('/api/acronyms')
def get_acronyms():
    """API endpoint to get all acronyms for the tooltip system"""
    try:
        acronym_data = load_acronyms()
        return jsonify({
            'success': True,
            'data': acronym_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/acronyms/<acronym>')
def get_acronym(acronym):
    """Get definition for a specific acronym"""
    try:
        acronym_data = load_acronyms()
        acronym = acronym.upper()
        
        if acronym in acronym_data['acronyms']:
            # Find category
            category = None
            for cat, items in acronym_data['categories'].items():
                if acronym in items:
                    category = cat
                    break
            
            return jsonify({
                'success': True,
                'acronym': acronym,
                'definition': acronym_data['acronyms'][acronym],
                'category': category
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Acronym not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/generate_signals', methods=['POST'])
def generate_signals():
    """Generate telecommunication signals for analysis"""
    try:
        data = request.json
        num_bits = data.get('num_bits', 50)
        modulation = data.get('modulation', 'BPSK')
        noise_level = data.get('noise_level', 0.1)
        
        # Generate signal data
        np.random.seed(42)  # For reproducibility
        bits = np.random.randint(0, 2, num_bits)
        
        # Simple signal generation for demonstration
        samples_per_symbol = 10
        t = np.linspace(0, num_bits, num_bits * samples_per_symbol)
        
        if modulation == 'BPSK':
            symbols = 2 * bits - 1  # Map 0->-1, 1->+1
            baseband = np.repeat(symbols, samples_per_symbol)
            carrier = np.cos(2 * np.pi * 0.1 * t)
            signal = baseband * carrier
        elif modulation == 'QPSK':
            # Simplified QPSK
            symbols = 2 * bits - 1
            baseband = np.repeat(symbols, samples_per_symbol)
            carrier = np.cos(2 * np.pi * 0.1 * t)
            signal = baseband * carrier
        elif modulation == '16-QAM':
            # Simplified 16-QAM
            symbols = 2 * bits - 1
            baseband = np.repeat(symbols, samples_per_symbol)
            carrier = np.cos(2 * np.pi * 0.1 * t)
            signal = baseband * carrier
        
        # Add noise
        noise = noise_level * np.random.randn(len(signal))
        noisy_signal = signal + noise
        
        # Calculate SNR
        signal_power = np.mean(signal**2)
        noise_power = np.mean(noise**2)
        snr_db = 10 * np.log10(signal_power / noise_power) if noise_power > 0 else float('inf')
        
        # Create plot
        plt.figure(figsize=(12, 8))
        
        plt.subplot(3, 1, 1)
        plt.plot(bits[:20], 'bo-', linewidth=2, markersize=8)
        plt.title(f'Digital Bits (First 20 of {num_bits})')
        plt.ylabel('Bit Value')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3, 1, 2)
        plt.plot(t[:200], signal[:200], 'r-', linewidth=1.5, label='Clean Signal')
        plt.title(f'{modulation} Modulated Signal')
        plt.ylabel('Amplitude')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3, 1, 3)
        plt.plot(t[:200], noisy_signal[:200], 'g-', linewidth=1.5, label='Noisy Signal')
        plt.title(f'Received Signal (SNR = {snr_db:.1f} dB)')
        plt.ylabel('Amplitude')
        plt.xlabel('Sample Index')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Convert plot to base64 string
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'plot': img_base64,
            'result': {
                'bits': bits.tolist(),
                'modulation': modulation,
                'samples': len(signal),
                'snr_db': snr_db
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/constellation/<modulation>')
def constellation_diagram(modulation):
    """Generate constellation diagram for specified modulation"""
    try:
        plt.figure(figsize=(8, 8))
        
        if modulation == 'BPSK':
            points = np.array([-1, 1])
            plt.scatter(points, [0, 0], s=200, c=['red', 'blue'], alpha=0.8)
            plt.xlim(-2, 2)
            plt.ylim(-2, 2)
            
        elif modulation == 'QPSK':
            points_i = np.array([1, -1, -1, 1]) / np.sqrt(2)
            points_q = np.array([1, 1, -1, -1]) / np.sqrt(2)
            colors = ['red', 'blue', 'green', 'orange']
            plt.scatter(points_i, points_q, s=200, c=colors, alpha=0.8)
            plt.xlim(-1.5, 1.5)
            plt.ylim(-1.5, 1.5)
            
        elif modulation == '16-QAM':
            points_i = []
            points_q = []
            for i in [-3, -1, 1, 3]:
                for q in [-3, -1, 1, 3]:
                    points_i.append(i)
                    points_q.append(q)
            plt.scatter(points_i, points_q, s=150, c='purple', alpha=0.8)
            plt.xlim(-5, 5)
            plt.ylim(-5, 5)
        
        plt.title(f'{modulation} Constellation Diagram', fontsize=16, fontweight='bold')
        plt.xlabel('In-phase (I)', fontsize=14)
        plt.ylabel('Quadrature (Q)', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.5)
        plt.axvline(x=0, color='k', linestyle='-', alpha=0.5)
        
        # Convert plot to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'modulation': modulation,
            'plot': img_base64
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/performance_analysis')
def performance_analysis():
    """Generate BER vs SNR performance analysis"""
    try:
        plt.figure(figsize=(12, 8))
        
        snr_db = np.linspace(0, 15, 31)
        snr_linear = 10**(snr_db/10)
        
        # Theoretical BER curves (simplified)
        ber_bpsk = 0.5 * np.exp(-snr_linear/2)
        ber_qpsk = 0.5 * np.exp(-snr_linear/2)
        ber_16qam = 0.75 * np.exp(-snr_linear/10)
        
        plt.semilogy(snr_db, ber_bpsk, 'b-', linewidth=3, label='BPSK', marker='o')
        plt.semilogy(snr_db, ber_qpsk, 'r-', linewidth=3, label='QPSK', marker='s')
        plt.semilogy(snr_db, ber_16qam, 'g-', linewidth=3, label='16-QAM', marker='^')
        
        plt.title('BER vs SNR Performance Comparison', fontsize=16, fontweight='bold')
        plt.xlabel('SNR (dB)', fontsize=14)
        plt.ylabel('Bit Error Rate (BER)', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend(fontsize=12)
        plt.ylim(1e-6, 1)
        
        # Convert plot to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'plot': img_base64
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/5g_comparison')
def g5_comparison():
    """Generate 5G technology comparison"""
    try:
        plt.figure(figsize=(14, 10))
        
        # Data for comparison
        technologies = ['3G', '4G/LTE', '5G Sub-6', '5G mmWave', '6G (Future)']
        peak_speeds = [2, 100, 1000, 10000, 100000]  # Mbps
        latencies = [100, 20, 5, 1, 0.1]  # ms
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Peak speeds comparison
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57']
        bars1 = ax1.bar(technologies, peak_speeds, color=colors, alpha=0.8)
        ax1.set_title('Peak Data Rates by Generation', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Peak Speed (Mbps)', fontsize=14)
        ax1.set_yscale('log')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, speed in zip(bars1, peak_speeds):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{speed:,}', ha='center', va='bottom', fontweight='bold')
        
        # Latency comparison
        bars2 = ax2.bar(technologies, latencies, color=colors, alpha=0.8)
        ax2.set_title('Latency Comparison by Generation', fontsize=16, fontweight='bold')
        ax2.set_ylabel('Latency (ms)', fontsize=14)
        ax2.set_xlabel('Technology Generation', fontsize=14)
        ax2.set_yscale('log')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for bar, latency in zip(bars2, latencies):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{latency}', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # Convert plot to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'plot': img_base64
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/network_topology/<topology>')
def network_topology(topology):
    """Generate network topology diagrams"""
    try:
        plt.figure(figsize=(10, 8))
        
        if topology == 'star':
            # Central hub
            plt.scatter(0, 0, s=1000, c='gold', marker='*', edgecolors='black', linewidth=2, label='Hub')
            plt.text(0, 0, 'HUB', ha='center', va='center', fontweight='bold')
            
            # Surrounding nodes
            angles = np.linspace(0, 2*np.pi, 7)[:-1]  # 6 nodes
            radius = 3
            for i, angle in enumerate(angles):
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                plt.scatter(x, y, s=400, c='lightblue', edgecolors='black', linewidth=2)
                plt.plot([0, x], [0, y], 'k-', linewidth=2, alpha=0.7)
                plt.text(x, y, f'PC{i+1}', ha='center', va='center', fontweight='bold', fontsize=10)
            
            plt.title('Star Network Topology', fontsize=16, fontweight='bold')
            
        elif topology == 'mesh':
            # Mesh topology - all nodes connected to all
            positions = [(0, 2), (2, 1), (2, -1), (0, -2), (-2, -1), (-2, 1)]
            
            # Draw all connections
            for i, pos1 in enumerate(positions):
                for j, pos2 in enumerate(positions[i+1:], i+1):
                    plt.plot([pos1[0], pos2[0]], [pos1[1], pos2[1]], 'k-', linewidth=1, alpha=0.5)
            
            # Draw nodes
            for i, (x, y) in enumerate(positions):
                plt.scatter(x, y, s=400, c='lightgreen', edgecolors='black', linewidth=2)
                plt.text(x, y, chr(65+i), ha='center', va='center', fontweight='bold', fontsize=12)
            
            plt.title('Mesh Network Topology', fontsize=16, fontweight='bold')
            
        elif topology == 'ring':
            # Ring topology
            angles = np.linspace(0, 2*np.pi, 7)[:-1]  # 6 nodes
            radius = 2.5
            positions = []
            
            for i, angle in enumerate(angles):
                x = radius * np.cos(angle)
                y = radius * np.sin(angle)
                positions.append((x, y))
                plt.scatter(x, y, s=400, c='lightcoral', edgecolors='black', linewidth=2)
                plt.text(x, y, chr(65+i), ha='center', va='center', fontweight='bold', fontsize=12)
            
            # Connect nodes in ring
            for i in range(len(positions)):
                x1, y1 = positions[i]
                x2, y2 = positions[(i+1) % len(positions)]
                plt.plot([x1, x2], [y1, y2], 'k-', linewidth=2)
                
                # Add direction arrow
                mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                dx, dy = x2 - x1, y2 - y1
                plt.arrow(mid_x - dx*0.1, mid_y - dy*0.1, dx*0.2, dy*0.2, 
                         head_width=0.15, head_length=0.1, fc='red', ec='red')
            
            plt.title('Ring Network Topology', fontsize=16, fontweight='bold')
        
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        
        # Convert plot to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'plot': img_base64
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Enhanced Telecommunications Laboratory Server")
    print("📡 Features: Signal Processing, 5G Analysis, Interactive Tooltips")
    print("🌐 Access: http://localhost:5000")
    print("="*60)
    app.run(debug=True, host='0.0.0.0', port=5000)
