#!/usr/bin/env python3
"""
Enhanced Telecommunications Laboratory 01 - Professional Automation Script
Advanced Communication System Analysis with 5G/6G Concepts

MAJOR IMPROVEMENTS BASED ON FILESYSTEM ANALYSIS:
- Leverages existing pandas, seaborn, PIL packages in virtual environment
- Advanced modulation schemes (QPSK, 16-QAM, 64-QAM)
- 5G/6G concepts integration  
- Real-time performance metrics
- Export to multiple formats
- Statistical analysis with pandas
- Eye diagrams and constellation plots
- Professional reporting and data export
- Network capacity calculations

Author: Enhanced Telecommunications Laboratory
Date: August 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arrow
import seaborn as sns
import pandas as pd
from datetime import datetime
import os
from PIL import Image, ImageDraw, ImageFont
import json
import warnings
warnings.filterwarnings('ignore')

# Enhanced plotting style using available packages
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

class EnhancedTelecomLabAutomation:
    """
    Enhanced telecommunications laboratory automation leveraging your existing packages
    """
    
    def __init__(self, advanced_mode=True):
        self.advanced_mode = advanced_mode
        self.setup_enhanced_parameters()
        self.create_enhanced_output_directory()
        self.setup_pandas_dataframes()
        
    def setup_enhanced_parameters(self):
        """Enhanced parameters utilizing your 5G/6G repository context"""
        # Enhanced BPSK Parameters with 5G context
        self.N = 100                   # More bits for better analysis
        self.sps = 20                  # Higher resolution
        self.fc = 2.4e9                # 2.4 GHz (5G frequency band)
        self.fs = self.sps * 1e6       # 20 MHz sampling (5G bandwidth)
        self.symbol_duration = 1e-6    # 1 microsecond
        
        # 5G/6G Specific Parameters (leveraging your ORAN context)
        self.subcarrier_spacing = 30e3  # 30 kHz (5G NR)
        self.num_subcarriers = 1200     # OFDM subcarriers
        self.cp_length = 0.25          # Cyclic prefix
        self.modulation_schemes = ['BPSK', 'QPSK', '16-QAM', '64-QAM']
        
        # Enhanced noise and channel modeling
        self.noise_power = 0.1
        self.channel_models = ['AWGN', 'Rayleigh', 'Rician']
        
        print("🚀 ENHANCED 5G/6G TELECOMMUNICATIONS LABORATORY")
        print("="*70)
        print(f"📡 Operating Frequency: {self.fc/1e9:.1f} GHz (5G NR Band)")
        print(f"⚡ Bandwidth: {self.fs/1e6:.1f} MHz")
        print(f"📊 Advanced Analysis: {'ENABLED' if self.advanced_mode else 'DISABLED'}")
        print(f"🌐 5G Features: OFDM, Massive MIMO, Network Slicing")
        print("="*70)
        
    def create_enhanced_output_directory(self):
        """Create professional directory structure"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.base_dir = f"Enhanced_5G_Lab_Results_{timestamp}"
        
        # Professional directory structure
        self.dirs = {
            'system_diagrams': f"{self.base_dir}/01_Advanced_System_Diagrams",
            'signal_analysis': f"{self.base_dir}/02_Multi_Modulation_Analysis", 
            'performance': f"{self.base_dir}/03_Performance_Metrics",
            'constellation': f"{self.base_dir}/04_Constellation_Analysis",
            'network_5g': f"{self.base_dir}/05_5G_Network_Analysis",
            'reports': f"{self.base_dir}/06_Professional_Reports",
            'data_export': f"{self.base_dir}/07_Data_Export"
        }
        
        for dir_path in self.dirs.values():
            os.makedirs(dir_path, exist_ok=True)
            
        print(f"📁 Professional directory structure created: {self.base_dir}")
        
    def setup_pandas_dataframes(self):
        """Initialize pandas DataFrames for advanced data analysis"""
        self.signal_df = pd.DataFrame()
        self.performance_df = pd.DataFrame()
        self.modulation_comparison_df = pd.DataFrame()
        self.network_metrics_df = pd.DataFrame()
        
    def generate_5g_system_architecture_diagram(self):
        """Advanced 5G system diagram leveraging your ORAN knowledge"""
        fig, ax = plt.subplots(1, 1, figsize=(18, 12))
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 12)
        ax.axis('off')
        
        # 5G/ORAN Components with professional styling
        components = [
            {"name": "5G Core\n(5GC)", "pos": (2, 9), "color": "#E8F5E8", "size": (1.6, 1.2)},
            {"name": "O-RAN\nSMO", "pos": (5, 9), "color": "#E3F2FD", "size": (1.6, 1.2)},
            {"name": "Near-RT\nRIC", "pos": (8, 9), "color": "#FFF3E0", "size": (1.6, 1.2)},
            {"name": "O-CU\n(Central Unit)", "pos": (11, 9), "color": "#F1F8E9", "size": (1.8, 1.2)},
            {"name": "O-DU\n(Distributed Unit)", "pos": (14, 9), "color": "#FCE4EC", "size": (1.8, 1.2)},
            
            {"name": "Massive MIMO\nAntenna Array", "pos": (2, 6), "color": "#FFEBEE", "size": (2.0, 1.2)},
            {"name": "mmWave\nBeamforming", "pos": (5.5, 6), "color": "#F3E5F5", "size": (2.0, 1.2)},
            {"name": "OFDM\nModulator", "pos": (9, 6), "color": "#E0F2F1", "size": (1.8, 1.2)},
            {"name": "Channel\nEncoder", "pos": (12, 6), "color": "#FFF8E1", "size": (1.8, 1.2)},
            {"name": "RF Frontend\n(24-40 GHz)", "pos": (14.5, 6), "color": "#FFECB3", "size": (2.0, 1.2)},
            
            {"name": "eMBB Slice\n(Enhanced Mobile\nBroadband)", "pos": (3, 3), "color": "#E8F5E8", "size": (2.4, 1.4)},
            {"name": "URLLC Slice\n(Ultra-Reliable\nLow Latency)", "pos": (8, 3), "color": "#FFEBEE", "size": (2.4, 1.4)},
            {"name": "mMTC Slice\n(Massive Machine\nType Comm)", "pos": (13, 3), "color": "#F3E5F5", "size": (2.4, 1.4)}
        ]
        
        # Draw components with professional styling
        for comp in components:
            bbox = FancyBboxPatch(
                (comp["pos"][0] - comp["size"][0]/2, comp["pos"][1] - comp["size"][1]/2),
                comp["size"][0], comp["size"][1],
                boxstyle="round,pad=0.2",
                facecolor=comp["color"],
                edgecolor="#1565C0",
                linewidth=2.5,
                alpha=0.8
            )
            ax.add_patch(bbox)
            ax.text(comp["pos"][0], comp["pos"][1], comp["name"], 
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Professional connection lines
        connections = [
            # Control plane connections
            ((2, 8.4), (5, 8.4)),     # 5GC to SMO
            ((5, 8.4), (8, 8.4)),     # SMO to Near-RT RIC
            ((8, 8.4), (11, 8.4)),    # RIC to O-CU
            ((11, 8.4), (14, 8.4)),   # O-CU to O-DU
            
            # Data plane connections
            ((2, 5.4), (9, 5.4)),     # MIMO to OFDM
            ((9, 5.4), (12, 5.4)),    # OFDM to Encoder
            ((12, 5.4), (14.5, 5.4)), # Encoder to RF
            
            # Network slicing connections
            ((3, 3.7), (8, 3.7)),     # Inter-slice coordination
            ((8, 3.7), (13, 3.7))     # Slice management
        ]
        
        for start, end in connections:
            ax.plot([start[0], end[0]], [start[1], end[1]], 
                   'b-', linewidth=3, alpha=0.7)
        
        # Add 5G specifications box
        specs_text = """5G NR Advanced Specifications:
• Peak Data Rate: 20 Gbps (DL), 10 Gbps (UL)
• Spectral Efficiency: 30 bps/Hz (DL), 15 bps/Hz (UL)
• Latency: <1ms (URLLC), <4ms (eMBB)
• Mobility: Up to 500 km/h
• Connection Density: 1M devices/km²
• Energy Efficiency: 100x improvement vs 4G
• Reliability: 99.999% (URLLC applications)"""
        
        ax.text(1, 11.5, specs_text, fontsize=10, 
               bbox=dict(boxstyle="round,pad=0.5", facecolor="#E3F2FD", alpha=0.9))
        
        # Main title with professional styling
        ax.text(8, 11, "Advanced 5G NR System Architecture with O-RAN Integration", 
               ha='center', va='center', fontsize=18, fontweight='bold', color='#1565C0')
        
        ax.text(8, 0.5, f"Enhanced Laboratory Analysis - Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
               ha='center', va='center', fontsize=12, style='italic')
        
        plt.tight_layout()
        plt.savefig(f"{self.dirs['system_diagrams']}/5g_oran_system_architecture.png", 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        print("✅ Advanced 5G O-RAN system architecture generated")
        
    def generate_advanced_modulation_signals(self):
        """Generate signals for multiple advanced modulation schemes"""
        # Enhanced time vector
        t = np.linspace(0, self.N * self.symbol_duration, self.N * self.sps)
        
        # Generate enhanced bit sequence
        np.random.seed(42)  # For reproducibility
        bits = np.random.randint(0, 2, self.N)
        
        # Initialize signal dictionary
        self.modulated_signals = {}
        
        # BPSK Implementation
        symbols_bpsk = 2 * bits - 1
        baseband_bpsk = np.repeat(symbols_bpsk, self.sps)
        carrier_freq = 1e6  # 1 MHz for visualization
        carrier = np.cos(2 * np.pi * carrier_freq * t)
        self.modulated_signals['BPSK'] = baseband_bpsk[:len(carrier)] * carrier
        
        # QPSK Implementation
        # Pair bits for I and Q channels
        bits_padded = np.pad(bits, (0, len(bits) % 2), 'constant')
        bits_reshaped = bits_padded.reshape(-1, 2)
        
        i_symbols = 2 * bits_reshaped[:, 0] - 1  # I channel
        q_symbols = 2 * bits_reshaped[:, 1] - 1  # Q channel
        
        i_baseband = np.repeat(i_symbols, self.sps)
        q_baseband = np.repeat(q_symbols, self.sps)
        
        # Ensure same length
        min_len = min(len(i_baseband), len(carrier))
        carrier_i = np.cos(2 * np.pi * carrier_freq * t[:min_len])
        carrier_q = -np.sin(2 * np.pi * carrier_freq * t[:min_len])
        
        self.modulated_signals['QPSK'] = (i_baseband[:min_len] * carrier_i + 
                                         q_baseband[:min_len] * carrier_q)
        
        # 16-QAM Implementation with Gray coding
        bits_16qam = np.pad(bits, (0, (4 - len(bits) % 4) % 4), 'constant')
        bits_16qam_reshaped = bits_16qam.reshape(-1, 4)
        
        # Gray-coded 16-QAM constellation
        gray_16qam = {
            (0,0,0,0): (-3, -3), (0,0,0,1): (-3, -1), (0,0,1,1): (-3, 1), (0,0,1,0): (-3, 3),
            (0,1,0,0): (-1, -3), (0,1,0,1): (-1, -1), (0,1,1,1): (-1, 1), (0,1,1,0): (-1, 3),
            (1,1,0,0): (1, -3),  (1,1,0,1): (1, -1),  (1,1,1,1): (1, 1),  (1,1,1,0): (1, 3),
            (1,0,0,0): (3, -3),  (1,0,0,1): (3, -1),  (1,0,1,1): (3, 1),  (1,0,1,0): (3, 3)
        }
        
        constellation_points = [gray_16qam[tuple(bits_16qam_reshaped[i])] 
                               for i in range(len(bits_16qam_reshaped))]
        
        i_symbols_16 = np.array([point[0] for point in constellation_points])
        q_symbols_16 = np.array([point[1] for point in constellation_points])
        
        i_baseband_16 = np.repeat(i_symbols_16, self.sps)
        q_baseband_16 = np.repeat(q_symbols_16, self.sps)
        
        min_len_16 = min(len(i_baseband_16), len(carrier))
        self.modulated_signals['16-QAM'] = (i_baseband_16[:min_len_16] * carrier_i[:min_len_16] + 
                                           q_baseband_16[:min_len_16] * carrier_q[:min_len_16])
        
        # Store enhanced data in pandas DataFrame
        signal_data = {
            'time': t[:min_len],
            'original_bits': np.repeat(bits[:min_len//self.sps], self.sps)[:min_len],
            'BPSK_signal': self.modulated_signals['BPSK'][:min_len],
            'QPSK_signal': self.modulated_signals['QPSK'][:min_len],
            'carrier_wave': carrier[:min_len]
        }
        
        if min_len_16 >= min_len:
            signal_data['16QAM_signal'] = self.modulated_signals['16-QAM'][:min_len]
        else:
            padded_16qam = np.pad(self.modulated_signals['16-QAM'], 
                                 (0, min_len - len(self.modulated_signals['16-QAM'])), 'constant')
            signal_data['16QAM_signal'] = padded_16qam
        
        self.signal_df = pd.DataFrame(signal_data)
        
        print("✅ Advanced modulation signals generated with pandas DataFrame")
        return bits, t[:min_len]
        
    def plot_enhanced_signal_analysis(self):
        """Enhanced signal analysis using seaborn and matplotlib"""
        if self.signal_df.empty:
            self.generate_advanced_modulation_signals()
        
        # Use seaborn style for professional plots
        with sns.axes_style("whitegrid"):
            fig, axes = plt.subplots(4, 1, figsize=(16, 14))
            fig.suptitle('Advanced Multi-Modulation Signal Analysis', 
                        fontsize=18, fontweight='bold', color='#1565C0')
        
        # Limit to first 1000 samples for clarity
        plot_samples = 1000
        time_data = self.signal_df['time'][:plot_samples]
        
        # Original digital bits
        axes[0].plot(time_data, self.signal_df['original_bits'][:plot_samples], 
                    'b-', linewidth=3, label='Digital Data Stream')
        axes[0].fill_between(time_data, 0, self.signal_df['original_bits'][:plot_samples], 
                           alpha=0.3, color='blue')
        axes[0].set_title('Original Digital Bit Stream', fontsize=14, fontweight='bold')
        axes[0].set_ylabel('Amplitude')
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        axes[0].set_ylim(-0.2, 1.2)
        
        # BPSK Modulation
        axes[1].plot(time_data, self.signal_df['BPSK_signal'][:plot_samples], 
                    'r-', linewidth=2, label='BPSK Modulated Signal')
        axes[1].set_title('BPSK Modulation - Binary Phase Shift Keying', 
                         fontsize=14, fontweight='bold')
        axes[1].set_ylabel('Amplitude')
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()
        
        # QPSK Modulation
        axes[2].plot(time_data, self.signal_df['QPSK_signal'][:plot_samples], 
                    'g-', linewidth=2, label='QPSK Modulated Signal')
        axes[2].set_title('QPSK Modulation - Quadrature Phase Shift Keying', 
                         fontsize=14, fontweight='bold')
        axes[2].set_ylabel('Amplitude')
        axes[2].grid(True, alpha=0.3)
        axes[2].legend()
        
        # 16-QAM Modulation
        axes[3].plot(time_data, self.signal_df['16QAM_signal'][:plot_samples], 
                    'purple', linewidth=2, label='16-QAM Modulated Signal')
        axes[3].set_title('16-QAM Modulation - 16-Quadrature Amplitude Modulation', 
                         fontsize=14, fontweight='bold')
        axes[3].set_ylabel('Amplitude')
        axes[3].set_xlabel('Time (seconds)')
        axes[3].grid(True, alpha=0.3)
        axes[3].legend()
        
        plt.tight_layout()
        plt.savefig(f"{self.dirs['signal_analysis']}/advanced_modulation_analysis.png", 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        print("✅ Enhanced signal analysis with professional styling")
        
    def generate_professional_constellation_diagrams(self):
        """Generate professional constellation diagrams using matplotlib and seaborn"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Professional Constellation Diagram Analysis for 5G Modulations', 
                     fontsize=16, fontweight='bold', color='#1565C0')
        
        # Enhanced BPSK Constellation
        ax = axes[0, 0]
        bpsk_points = np.array([-1, 1])
        scatter = ax.scatter(bpsk_points, [0, 0], s=300, c=['red', 'blue'], 
                           alpha=0.8, edgecolors='black', linewidth=2)
        
        # Add bit labels
        ax.text(-1, -0.3, '0', ha='center', va='top', fontsize=12, fontweight='bold')
        ax.text(1, -0.3, '1', ha='center', va='top', fontsize=12, fontweight='bold')
        
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        ax.set_title('BPSK Constellation\n1 bit/symbol', fontweight='bold')
        ax.set_xlabel('In-phase (I)')
        ax.set_ylabel('Quadrature (Q)')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.5)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.5)
        
        # Enhanced QPSK Constellation
        ax = axes[0, 1]
        qpsk_i = np.array([1, -1, -1, 1]) / np.sqrt(2)
        qpsk_q = np.array([1, 1, -1, -1]) / np.sqrt(2)
        colors = ['red', 'blue', 'green', 'orange']
        scatter = ax.scatter(qpsk_i, qpsk_q, s=300, c=colors, alpha=0.8, 
                           edgecolors='black', linewidth=2)
        
        # Add bit pair labels
        labels = ['00', '01', '11', '10']
        for i, (x, y, label) in enumerate(zip(qpsk_i, qpsk_q, labels)):
            ax.text(x, y-0.2, label, ha='center', va='top', 
                   fontsize=10, fontweight='bold')
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_title('QPSK Constellation\n2 bits/symbol', fontweight='bold')
        ax.set_xlabel('In-phase (I)')
        ax.set_ylabel('Quadrature (Q)')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.5)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.5)
        
        # Enhanced 16-QAM Constellation
        ax = axes[1, 0]
        qam16_positions = []
        qam16_labels = []
        
        # Gray-coded 16-QAM mapping
        gray_mapping = {
            (-3, -3): '0000', (-3, -1): '0001', (-3, 1): '0011', (-3, 3): '0010',
            (-1, -3): '0100', (-1, -1): '0101', (-1, 1): '0111', (-1, 3): '0110',
            (1, -3): '1100',  (1, -1): '1101',  (1, 1): '1111',  (1, 3): '1110',
            (3, -3): '1000',  (3, -1): '1001',  (3, 1): '1011',  (3, 3): '1010'
        }
        
        for (i, q), bits in gray_mapping.items():
            qam16_positions.append((i, q))
            qam16_labels.append(bits)
        
        qam16_i = [pos[0] for pos in qam16_positions]
        qam16_q = [pos[1] for pos in qam16_positions]
        
        scatter = ax.scatter(qam16_i, qam16_q, s=200, c='purple', alpha=0.8, 
                           edgecolors='black', linewidth=2)
        
        # Add bit labels (smaller font for 16-QAM)
        for i, q, label in zip(qam16_i, qam16_q, qam16_labels):
            ax.text(i, q-0.5, label, ha='center', va='top', 
                   fontsize=8, fontweight='bold')
        
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_title('16-QAM Constellation\n4 bits/symbol', fontweight='bold')
        ax.set_xlabel('In-phase (I)')
        ax.set_ylabel('Quadrature (Q)')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.5)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.5)
        
        # Enhanced 64-QAM Constellation
        ax = axes[1, 1]
        qam64_i = []
        qam64_q = []
        for i in range(-7, 8, 2):
            for q in range(-7, 8, 2):
                qam64_i.append(i)
                qam64_q.append(q)
                
        scatter = ax.scatter(qam64_i, qam64_q, s=120, c='orange', alpha=0.8, 
                           edgecolors='black', linewidth=1)
        
        ax.set_xlim(-10, 10)
        ax.set_ylim(-10, 10)
        ax.set_title('64-QAM Constellation\n6 bits/symbol', fontweight='bold')
        ax.set_xlabel('In-phase (I)')
        ax.set_ylabel('Quadrature (Q)')
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='k', linestyle='-', alpha=0.5)
        ax.axvline(x=0, color='k', linestyle='-', alpha=0.5)
        
        plt.tight_layout()
        plt.savefig(f"{self.dirs['constellation']}/professional_constellation_diagrams.png", 
                   dpi=300, bbox_inches='tight', facecolor='white')
        plt.show()
        print("✅ Professional constellation diagrams generated")
        
    def calculate_enhanced_performance_metrics(self):
        """Calculate comprehensive performance metrics with pandas"""
        # Enhanced SNR range for 5G analysis
        snr_range = np.linspace(0, 30, 31)
        
        # Theoretical BER calculations for different modulations
        # More accurate BER formulations
        snr_linear = 10**(snr_range/10)
        
        # BPSK BER
        ber_bpsk = 0.5 * np.erfc(np.sqrt(snr_linear))
        
        # QPSK BER (same as BPSK with Gray coding)
        ber_qpsk = 0.5 * np.erfc(np.sqrt(snr_linear))
        
        # 16-QAM BER (approximation)
        ber_16qam = 0.75 * np.erfc(np.sqrt(0.8 * snr_linear))
        
        # 64-QAM BER (approximation)
        ber_64qam = (7/12) * np.erfc(np.sqrt(snr_linear/42))
        
        # Spectral efficiency calculations
        se_bpsk = np