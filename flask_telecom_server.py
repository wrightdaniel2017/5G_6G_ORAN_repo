#!/usr/bin/env python3
"""
Enhanced Telecommunications Laboratory - Flask Web Server
Professional Web Interface for 5G/6G Communication System Analysis

Features:
- Interactive telecommunications analysis
- Real-time signal processing
- 5G/6G system demonstrations
- Performance metrics visualization
- Professional web interface

Author: Enhanced Telecommunications Laboratory
Date: August 2025
"""

from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for web server
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import io
import base64
from datetime import datetime
import json
import os
import warnings
warnings.filterwarnings('ignore')

# Try to import scipy, if not available use approximations
try:
    from scipy.special import erfc
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    # Simple approximation for erfc when scipy is not available
    def erfc(x):
        # Abramowitz and Stegun approximation
        x = np.asarray(x)
        z = np.abs(x)
        t = 1.0 / (1.0 + 0.5 * z)
        
        # Coefficients
        a1, a2, a3, a4, a5 = -1.26551223, 1.00002368, 0.37409196, 0.09678418, -0.18628806
        a6, a7, a8, a9 = 0.27886807, -1.13520398, 1.48851587, -0.82215223
        a10 = 0.17087277
        
        erfcx = t * np.exp(-z*z + a1*t + a2*t**2 + a3*t**3 + a4*t**4 + a5*t**5 + 
                          a6*t**6 + a7*t**7 + a8*t**8 + a9*t**9 + a10*t**10)
        
        return np.where(x >= 0, erfcx, 2.0 - erfcx)

# Configure matplotlib for web use
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams.update({
    'figure.figsize': (12, 8),
    'font.size': 11,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 10
})

app = Flask(__name__)
app.config['SECRET_KEY'] = 'telecom_lab_2025'

class WebTelecomLab:
    """Web-based telecommunications laboratory for Flask integration"""
    
    def __init__(self):
        self.reset_parameters()
        
    def reset_parameters(self):
        """Reset to default parameters"""
        self.N = 100
        self.sps = 20
        self.fc = 2.4e9
        self.fs = 20e6
        self.noise_power = 0.1
        self.modulation = 'BPSK'
        self.signal_df = pd.DataFrame()
        self.performance_df = pd.DataFrame()
        
    def generate_signals(self, N=None, modulation=None, noise_level=None):
        """Generate telecommunication signals for web display"""
        if N: self.N = N
        if modulation: self.modulation = modulation
        if noise_level: self.noise_power = noise_level
        
        # Time vector
        t = np.linspace(0, self.N * 1e-6, self.N * self.sps)
        
        # Generate bits
        np.random.seed(42)  # Reproducible results
        bits = np.random.randint(0, 2, self.N)
        
        # Carrier signal
        carrier = np.cos(2 * np.pi * 1e6 * t)
        
        # Generate modulated signal based on scheme
        if self.modulation == 'BPSK':
            symbols = 2 * bits - 1
            baseband = np.repeat(symbols, self.sps)
            modulated = baseband[:len(carrier)] * carrier
            
        elif self.modulation == 'QPSK':
            # Pad bits if necessary
            bits_padded = np.pad(bits, (0, len(bits) % 2), 'constant')
            bits_pairs = bits_padded.reshape(-1, 2)
            
            i_symbols = 2 * bits_pairs[:, 0] - 1
            q_symbols = 2 * bits_pairs[:, 1] - 1
            
            i_baseband = np.repeat(i_symbols, self.sps)
            q_baseband = np.repeat(q_symbols, self.sps)
            
            min_len = min(len(i_baseband), len(carrier))
            carrier_q = -np.sin(2 * np.pi * 1e6 * t[:min_len])
            
            modulated = (i_baseband[:min_len] * carrier[:min_len] + 
                        q_baseband[:min_len] * carrier_q)
        
        elif self.modulation == '16-QAM':
            # Simplified 16-QAM
            bits_padded = np.pad(bits, (0, (4 - len(bits) % 4) % 4), 'constant')
            bits_4 = bits_padded.reshape(-1, 4)
            
            # Simple mapping to constellation points
            i_symbols = []
            q_symbols = []
            for b in bits_4:
                val = b[0]*8 + b[1]*4 + b[2]*2 + b[3]
                i_symbols.append(((val % 4) - 1.5) * 2)
                q_symbols.append(((val // 4) - 1.5) * 2)
            
            i_baseband = np.repeat(i_symbols, self.sps)
            q_baseband = np.repeat(q_symbols, self.sps)
            
            min_len = min(len(i_baseband), len(carrier))
            carrier_q = -np.sin(2 * np.pi * 1e6 * t[:min_len])
            
            modulated = (i_baseband[:min_len] * carrier[:min_len] + 
                        q_baseband[:min_len] * carrier_q)
        
        # Add noise
        noise = self.noise_power * np.random.randn(len(modulated))
        received = modulated + noise
        
        # Store in DataFrame
        min_samples = min(len(t), len(bits) * self.sps, len(modulated))
        
        self.signal_df = pd.DataFrame({
            'time': t[:min_samples],
            'bits': np.repeat(bits, self.sps)[:min_samples],
            'carrier': carrier[:min_samples],
            'modulated': modulated[:min_samples],
            'received': received[:min_samples]
        })
        
        return {
            'bits': bits.tolist(),
            'modulation': self.modulation,
            'samples': min_samples,
            'snr_db': 10 * np.log10(np.var(modulated) / (np.var(noise) + 1e-10))
        }
    
    def plot_to_base64(self, fig):
        """Convert matplotlib figure to base64 string for web display"""
        img_buffer = io.BytesIO()
        fig.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        img_buffer.seek(0)
        img_b64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close(fig)
        return img_b64
    
    def generate_signal_plot(self):
        """Generate signal analysis plot for web display"""
        if self.signal_df.empty:
            self.generate_signals()
        
        fig, axes = plt.subplots(4, 1, figsize=(14, 12))
        fig.suptitle(f'{self.modulation} Signal Analysis', fontsize=16, fontweight='bold')
        
        # Limit samples for web display
        plot_samples = 1000
        time_data = self.signal_df['time'][:plot_samples]
        
        # Digital bits
        axes[0].plot(time_data, self.signal_df['bits'][:plot_samples], 
                    'b-', linewidth=2, label='Digital Bits')
        axes[0].fill_between(time_data, 0, self.signal_df['bits'][:plot_samples], 
                           alpha=0.3, color='blue')
        axes[0].set_title('Digital Bit Stream')
        axes[0].set_ylabel('Amplitude')
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        
        # Carrier signal
        axes[1].plot(time_data, self.signal_df['carrier'][:plot_samples], 
                    'g-', linewidth=1.5, label='Carrier Wave')
        axes[1].set_title('Carrier Signal (1 MHz)')
        axes[1].set_ylabel('Amplitude')
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()
        
        # Modulated signal
        axes[2].plot(time_data, self.signal_df['modulated'][:plot_samples], 
                    'r-', linewidth=1.5, label=f'{self.modulation} Modulated')
        axes[2].set_title(f'{self.modulation} Modulated Signal')
        axes[2].set_ylabel('Amplitude')
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()
        
        # Received signal with noise
        axes[3].plot(time_data, self.signal_df['received'][:plot_samples], 
                    'purple', linewidth=1.5, label='Received Signal')
        axes[3].set_title('Received Signal (with Noise)')
        axes[3].set_ylabel('Amplitude')
        axes[3].set_xlabel('Time (seconds)')
        axes[3].grid(True, alpha=0.3)
        axes[3].legend()
        
        plt.tight_layout()
        return self.plot_to_base64(fig)
    
    def generate_constellation_plot(self, modulation=None):
        """Generate constellation diagram for web display"""
        if modulation:
            self.modulation = modulation
            
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        ax.set_aspect('equal')
        
        if self.modulation == 'BPSK':
            points = np.array([-1, 1])
            ax.scatter(points, [0, 0], s=300, c=['red', 'blue'], 
                      alpha=0.8, edgecolors='black', linewidth=2)
            ax.text(-1, -0.3, '0', ha='center', fontsize=12, fontweight='bold')
            ax.text(1, -0.3, '1', ha='center', fontsize=12, fontweight='bold')
            ax.set_xlim(-2, 2)
            ax.set_ylim(-2, 2)
            ax.set_title('BPSK Constellation\n1 bit per symbol', fontsize=16, fontweight='bold')
            
        elif self.modulation == 'QPSK':
            i_points = np.array([1, -1, -1, 1]) / np.sqrt(2)
            q_points = np.array([1, 1, -1, -1]) / np.sqrt(2)
            colors = ['red', 'blue', 'green', 'orange']
            ax.scatter(i_points, q_points, s=300, c=colors, alpha=0.8, 
                      edgecolors='black', linewidth=2)
            labels = ['00', '01', '11', '10']
            for i, q, label in zip(i_points, q_points, labels):
                ax.text(i, q-0.2, label, ha='center', fontsize=12, fontweight='bold')
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            ax.set_title('QPSK Constellation\n2 bits per symbol', fontsize=16, fontweight='bold')
            
        elif self.modulation == '16-QAM':
            i_points = []
            q_points = []
            for i in [-3, -1, 1, 3]:
                for q in [-3, -1, 1, 3]:
                    i_points.append(i)
                    q_points.append(q)
            ax.scatter(i_points, q_points, s=200, c='purple', alpha=0.8, 
                      edgecolors='black', linewidth=2)
            ax.set_xlim(-5, 5)
            ax.set_ylim(-5, 5)
            ax.set_title('16-QAM Constellation\n4 bits per symbol', fontsize=16, fontweight='bold')
        
        ax.set_xlabel('In-phase (I)')
        ax.set_ylabel('Quadrature (Q)')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.5)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.5)
        
        return self.plot_to_base64(fig)
    
    def generate_performance_plot(self):
        """Generate BER vs SNR performance plot with improved error handling"""
        try:
            snr_range = np.linspace(0, 25, 26)
            snr_linear = 10**(snr_range/10)
            
            # More robust BER calculations with error handling
            try:
                # Theoretical BER curves using erfc
                ber_bpsk = 0.5 * erfc(np.sqrt(snr_linear))
                ber_qpsk = 0.5 * erfc(np.sqrt(snr_linear))  # Same as BPSK for Gray coding
                ber_16qam = (3/8) * erfc(np.sqrt((4/5) * snr_linear))  # Approximation
            except Exception as e:
                print(f"Error calculating BER: {e}")
                # Fallback to simpler approximations
                ber_bpsk = np.exp(-snr_linear/2) / 2
                ber_qpsk = np.exp(-snr_linear/2) / 2
                ber_16qam = np.exp(-snr_linear/4)
            
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            
            # Plot with error handling
            try:
                ax.semilogy(snr_range, np.maximum(ber_bpsk, 1e-12), 'b-o', linewidth=2, 
                           markersize=6, label='BPSK')
                ax.semilogy(snr_range, np.maximum(ber_qpsk, 1e-12), 'g-s', linewidth=2, 
                           markersize=6, label='QPSK')
                ax.semilogy(snr_range, np.maximum(ber_16qam, 1e-12), 'r-^', linewidth=2, 
                           markersize=6, label='16-QAM')
            except Exception as e:
                print(f"Error plotting BER curves: {e}")
                # Simple fallback plot
                ax.plot(snr_range, ber_bpsk, 'b-', label='BPSK')
                ax.plot(snr_range, ber_qpsk, 'g-', label='QPSK')
                ax.plot(snr_range, ber_16qam, 'r-', label='16-QAM')
                ax.set_yscale('log')
            
            ax.set_title('Bit Error Rate vs Signal-to-Noise Ratio', fontsize=16, fontweight='bold')
            ax.set_xlabel('SNR (dB)')
            ax.set_ylabel('Bit Error Rate (BER)')
            ax.grid(True, alpha=0.3)
            ax.legend(fontsize=12)
            ax.set_ylim(1e-12, 1)
            
            return self.plot_to_base64(fig)
            
        except Exception as e:
            print(f"Error generating performance plot: {e}")
            # Return a simple error plot
            fig, ax = plt.subplots(1, 1, figsize=(12, 8))
            ax.text(0.5, 0.5, 'Performance analysis temporarily unavailable\nPlease try again later', 
                   ha='center', va='center', transform=ax.transAxes, fontsize=14)
            ax.set_title('Performance Analysis', fontsize=16, fontweight='bold')
            return self.plot_to_base64(fig)
    
    def generate_5g_comparison_plot(self):
        """Generate 5G technology comparison plot"""
        technologies = ['4G LTE', '5G Sub-6', '5G mmWave', '6G Future']
        peak_throughput = [1, 10, 50, 1000]  # Gbps
        latency = [10, 1, 0.1, 0.01]  # ms
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # Throughput comparison
        bars1 = ax1.bar(technologies, peak_throughput, 
                       color=['blue', 'green', 'red', 'purple'], alpha=0.7)
        ax1.set_title('Peak Throughput Comparison', fontsize=14, fontweight='bold')
        ax1.set_ylabel('Peak Throughput (Gbps)')
        ax1.set_yscale('log')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, value in zip(bars1, peak_throughput):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                    f'{value} Gbps', ha='center', va='bottom', fontweight='bold')
        
        # Latency comparison
        bars2 = ax2.bar(technologies, latency, 
                       color=['blue', 'green', 'red', 'purple'], alpha=0.7)
        ax2.set_title('Latency Comparison', fontsize=14, fontweight='bold')
        ax2.set_ylabel('Latency (ms)')
        ax2.set_yscale('log')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # Add value labels
        for bar, value in zip(bars2, latency):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                    f'{value} ms', ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        return self.plot_to_base64(fig)

# Initialize global lab instance
telecom_lab = WebTelecomLab()

@app.route('/')
def index():
    """Main page with telecommunications laboratory interface"""
    return render_template('index.html')

@app.route('/generate_signals', methods=['POST'])
def generate_signals():
    """Generate telecommunication signals based on user parameters"""
    try:
        data = request.json
        
        N = data.get('num_bits', 50)
        modulation = data.get('modulation', 'BPSK')
        noise_level = data.get('noise_level', 0.1)
        
        result = telecom_lab.generate_signals(N, modulation, noise_level)
        plot_b64 = telecom_lab.generate_signal_plot()
        
        return jsonify({
            'success': True,
            'result': result,
            'plot': plot_b64
        })
    except Exception as e:
        print(f"Error in generate_signals: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/constellation/<modulation>')
def constellation_diagram(modulation):
    """Generate constellation diagram for specified modulation"""
    try:
        plot_b64 = telecom_lab.generate_constellation_plot(modulation)
        return jsonify({
            'success': True,
            'plot': plot_b64,
            'modulation': modulation
        })
    except Exception as e:
        print(f"Error in constellation_diagram: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/performance_analysis')
def performance_analysis():
    """Generate performance analysis plots"""
    try:
        plot_b64 = telecom_lab.generate_performance_plot()
        return jsonify({
            'success': True,
            'plot': plot_b64
        })
    except Exception as e:
        print(f"Error in performance_analysis: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/5g_comparison')
def g5_comparison():
    """Generate 5G technology comparison"""
    try:
        plot_b64 = telecom_lab.generate_5g_comparison_plot()
        return jsonify({
            'success': True,
            'plot': plot_b64
        })
    except Exception as e:
        print(f"Error in 5g_comparison: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/network_topology/<topology>')
def network_topology(topology):
    """Generate network topology visualization"""
    try:
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_aspect('equal')
        
        if topology == 'star':
            # Central hub
            hub = plt.Circle((5, 4), 0.4, color='yellow', ec='black')
            ax.add_patch(hub)
            ax.text(5, 4, 'Hub', ha='center', va='center', fontweight='bold')
            
            # Connected nodes
            positions = [(3, 6), (7, 6), (2, 4), (8, 4), (3, 2), (7, 2)]
            for i, pos in enumerate(positions, 1):
                circle = plt.Circle(pos, 0.3, color='lightblue', ec='black')
                ax.add_patch(circle)
                ax.text(pos[0], pos[1], str(i), ha='center', va='center', fontweight='bold')
                ax.plot([5, pos[0]], [4, pos[1]], 'k-', linewidth=2)
            
            ax.set_title('Star Topology - Centralized Architecture', fontsize=16, fontweight='bold')
            
        elif topology == 'mesh':
            # Mesh positions
            positions = [(3, 6), (7, 6), (2, 3), (8, 3), (5, 1)]
            for i, pos in enumerate(positions, 1):
                circle = plt.Circle(pos, 0.3, color='lightgreen', ec='black')
                ax.add_patch(circle)
                ax.text(pos[0], pos[1], str(i), ha='center', va='center', fontweight='bold')
            
            # Connect all nodes
            for i in range(len(positions)):
                for j in range(i+1, len(positions)):
                    start = positions[i]
                    end = positions[j]
                    ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', linewidth=1.5, alpha=0.7)
            
            ax.set_title('Mesh Topology - Fully Connected Network', fontsize=16, fontweight='bold')
        
        elif topology == 'ring':
            # Ring positions
            angles = np.linspace(0, 2*np.pi, 6)[:-1]  # 5 nodes
            center_x, center_y = 5, 4
            radius = 2
            
            positions = []
            for i, angle in enumerate(angles):
                x = center_x + radius * np.cos(angle)
                y = center_y + radius * np.sin(angle)
                positions.append((x, y))
                circle = plt.Circle((x, y), 0.3, color='lightcoral', ec='black')
                ax.add_patch(circle)
                ax.text(x, y, str(i+1), ha='center', va='center', fontweight='bold')
            
            # Connect in ring
            for i in range(len(positions)):
                start = positions[i]
                end = positions[(i+1) % len(positions)]
                ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', linewidth=2)
            
            ax.set_title('Ring Topology - Circular Network', fontsize=16, fontweight='bold')
        
        ax.axis('off')
        plt.tight_layout()
        
        plot_b64 = telecom_lab.plot_to_base64(fig)
        return jsonify({
            'success': True,
            'plot': plot_b64,
            'topology': topology
        })
    except Exception as e:
        print(f"Error in network_topology: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/lab_status')
def lab_status():
    """Get current laboratory status and parameters"""
    return jsonify({
        'current_modulation': telecom_lab.modulation,
        'num_bits': telecom_lab.N,
        'noise_level': telecom_lab.noise_power,
        'carrier_frequency': f"{telecom_lab.fc/1e9:.1f} GHz",
        'scipy_available': SCIPY_AVAILABLE,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/test_animations')
def test_animations():
    """Test page for network topology animations"""
    return render_template('animation_test.html')

@app.route('/printable')
def printable_version():
    """Printable version of the telecommunications laboratory for PDF export"""
    return render_template('index_printable.html')

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error occurred. Please try again.'
    }), 500

if __name__ == '__main__':
    print("🚀 ENHANCED TELECOMMUNICATIONS LABORATORY SERVER")
    print("="*60)
    print("🌐 Starting Flask web server...")
    print("📡 Features: Signal Analysis, Modulation, 5G Comparison")
    print(f"🔬 SciPy Available: {'Yes' if SCIPY_AVAILABLE else 'No (using approximations)'}")
    print("🔧 Access at: http://localhost:5000")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
