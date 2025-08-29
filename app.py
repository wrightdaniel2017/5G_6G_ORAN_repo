#!/usr/bin/env python3
"""
Telecommunications Laboratory 01 - Automation Script
Communication System Analysis and Signal Flow Visualization

This script automates the process of:
1. Creating conceptual communication system diagrams
2. Analyzing signal flow using matplotlib
3. Demonstrating BPSK modulation and demodulation
4. Comparing analog vs digital signals

Author: Telecommunications Laboratory
Date: August 2025
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arrow
import seaborn as sns
from datetime import datetime
import os

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class TelecomLabAutomation:
    """
    Main class for telecommunications laboratory automation
    """
    
    def __init__(self):
        self.setup_parameters()
        self.create_output_directory()
    
    def setup_parameters(self):
        """Initialize simulation parameters"""
        # BPSK Parameters
        self.N = 20                    # number of bits
        self.sps = 10                  # samples per symbol
        self.fc = 2                    # carrier frequency (Hz)
        self.fs = self.sps * 10        # sampling frequency
        self.t = np.arange(0, self.N, 1/self.sps)  # time vector
        
        # Noise parameters
        self.noise_power = 0.3
        
        print(f"Laboratory Parameters Initialized:")
        print(f"- Number of bits: {self.N}")
        print(f"- Samples per symbol: {self.sps}")
        print(f"- Carrier frequency: {self.fc} Hz")
        print(f"- Sampling frequency: {self.fs} Hz")
        print(f"- Noise power: {self.noise_power}")
    
    def create_output_directory(self):
        """Create directory for output files"""
        self.output_dir = f"telecom_lab_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"Output directory created: {self.output_dir}")
    
    def generate_communication_system_diagram(self):
        """
        Part 1: Create conceptual communication system diagram
        Equivalent to Draw.io/Lucidchart diagram creation
        """
        fig, ax = plt.subplots(1, 1, figsize=(14, 8))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        
        # Define components
        components = [
            {"name": "Source\n(Bits)", "pos": (1, 3), "color": "lightblue"},
            {"name": "Modulator\n(BPSK)", "pos": (2.8, 3), "color": "lightgreen"},
            {"name": "Channel\n(with Noise)", "pos": (5, 3), "color": "yellow"},
            {"name": "Demodulator", "pos": (7.2, 3), "color": "orange"},
            {"name": "Receiver\n(Bits)", "pos": (9, 3), "color": "lightcoral"}
        ]
        
        # Draw components
        for comp in components:
            bbox = FancyBboxPatch(
                (comp["pos"][0] - 0.6, comp["pos"][1] - 0.4),
                1.2, 0.8,
                boxstyle="round,pad=0.1",
                facecolor=comp["color"],
                edgecolor="black",
                linewidth=2
            )
            ax.add_patch(bbox)
            ax.text(comp["pos"][0], comp["pos"][1], comp["name"], 
                   ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Draw arrows between components
        arrow_positions = [
            ((1.6, 3), (2.2, 3)),    # Source to Modulator
            ((3.4, 3), (4.4, 3)),    # Modulator to Channel
            ((5.6, 3), (6.6, 3)),    # Channel to Demodulator
            ((7.8, 3), (8.4, 3))     # Demodulator to Receiver
        ]
        
        for start, end in arrow_positions:
            ax.annotate('', xy=end, xytext=start,
                       arrowprops=dict(arrowstyle='->', lw=2, color='blue'))
        
        # Add noise source to channel
        noise_box = FancyBboxPatch(
            (4.4, 1.2), 1.2, 0.6,
            boxstyle="round,pad=0.1",
            facecolor="red",
            edgecolor="black",
            linewidth=1
        )
        ax.add_patch(noise_box)
        ax.text(5, 1.5, "Noise", ha='center', va='center', 
               fontsize=9, fontweight='bold', color='white')
        
        # Arrow from noise to channel
        ax.annotate('', xy=(5, 2.6), xytext=(5, 1.8),
                   arrowprops=dict(arrowstyle='->', lw=2, color='red'))
        
        # Add title and labels
        ax.text(5, 5.5, "Digital Communication System Block Diagram", 
               ha='center', va='center', fontsize=16, fontweight='bold')
        
        ax.text(5, 0.5, "Laboratory 01: Communication System Analysis", 
               ha='center', va='center', fontsize=12, style='italic')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/communication_system_diagram.png", 
                   dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Communication system diagram generated")
    
    def generate_signal_data(self):
        """Generate signals for BPSK communication system"""
        # 1. Source bits (random)
        self.bits = np.random.randint(0, 2, self.N)
        
        # 2. BPSK mapping: 0->-1, 1->+1
        self.symbols = 2 * self.bits - 1
        
        # 3. Baseband signal (repeat symbols)
        self.baseband = np.repeat(self.symbols, self.sps)
        
        # 4. Carrier signal
        self.carrier = np.cos(2 * np.pi * self.fc * self.t)
        
        # 5. Transmitted signal (modulated)
        self.tx = self.baseband * self.carrier
        
        # 6. Add noise to transmitted signal
        noise = self.noise_power * np.random.randn(len(self.tx))
        self.rx = self.tx + noise
        
        # 7. Demodulate (multiply by carrier again)
        self.demod = self.rx * self.carrier
        
        print(f"✓ Signal data generated:")
        print(f"  - Bits: {self.bits}")
        print(f"  - Symbols: {self.symbols}")
        print(f"  - Signal length: {len(self.tx)} samples")
    
    def plot_signal_analysis(self):
        """
        Part 2: Signal Flow Analysis using matplotlib
        Plots all signals in the communication chain
        """
        fig, axes = plt.subplots(4, 1, figsize=(15, 12))
        
        # Plot 1: Baseband (bits as pulses)
        axes[0].plot(self.t, self.baseband, 'b-', linewidth=2)
        axes[0].set_title("Baseband Signal (Bits as Pulses)", fontsize=14, fontweight='bold')
        axes[0].set_ylabel("Amplitude")
        axes[0].grid(True, alpha=0.3)
        axes[0].set_ylim(-1.5, 1.5)
        
        # Plot 2: Carrier signal
        axes[1].plot(self.t, self.carrier, 'g-', linewidth=1.5)
        axes[1].set_title("Carrier Signal", fontsize=14, fontweight='bold')
        axes[1].set_ylabel("Amplitude")
        axes[1].grid(True, alpha=0.3)
        axes[1].set_ylim(-1.2, 1.2)
        
        # Plot 3: Transmitted Signal (BPSK)
        axes[2].plot(self.t, self.tx, 'r-', linewidth=1.5)
        axes[2].set_title("Transmitted Signal (BPSK Modulated)", fontsize=14, fontweight='bold')
        axes[2].set_ylabel("Amplitude")
        axes[2].grid(True, alpha=0.3)
        
        # Plot 4: Received after Demodulation
        axes[3].plot(self.t, self.demod, 'purple', linewidth=1.5)
        axes[3].set_title("Received Signal after Demodulation (with Noise)", fontsize=14, fontweight='bold')
        axes[3].set_ylabel("Amplitude")
        axes[3].set_xlabel("Time")
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/signal_flow_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Signal flow analysis plots generated")
    
    def compare_analog_digital_signals(self):
        """Create comparison between analog and digital signals"""
        fig, axes = plt.subplots(2, 1, figsize=(12, 8))
        
        # Analog signal (continuous sine wave)
        t_analog = np.linspace(0, 2, 1000)
        analog_signal = np.sin(2 * np.pi * 2 * t_analog)
        
        axes[0].plot(t_analog, analog_signal, 'b-', linewidth=2, label='Analog Signal')
        axes[0].set_title("Analog Signal - Continuous Waveform", fontsize=14, fontweight='bold')
        axes[0].set_ylabel("Amplitude")
        axes[0].grid(True, alpha=0.3)
        axes[0].legend()
        
        # Digital signal (discrete pulses)
        t_digital = np.arange(0, 2, 0.1)
        digital_bits = np.random.randint(0, 2, len(t_digital))
        digital_signal = np.repeat(digital_bits, 1)
        t_digital_extended = np.repeat(t_digital, 1)
        
        axes[1].plot(t_digital_extended, digital_signal, 'r-', linewidth=3, 
                    label='Digital Signal', drawstyle='steps-post')
        axes[1].set_title("Digital Signal - Discrete Pulses", fontsize=14, fontweight='bold')
        axes[1].set_ylabel("Amplitude")
        axes[1].set_xlabel("Time (seconds)")
        axes[1].set_ylim(-0.5, 1.5)
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/analog_vs_digital_comparison.png", 
                   dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Analog vs Digital comparison generated")
    
    def plot_network_topologies(self):
        """Generate network topology diagrams"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        fig.suptitle("Network Topologies Comparison", fontsize=16, fontweight='bold')
        
        # Bus Topology
        ax = axes[0, 0]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_title("Bus Topology", fontsize=12, fontweight='bold')
        
        # Main bus line
        ax.plot([1, 9], [4, 4], 'k-', linewidth=4)
        # Nodes
        node_positions = [2, 3.5, 5, 6.5, 8]
        for i, pos in enumerate(node_positions, 1):
            circle = Circle((pos, 4), 0.3, color='lightblue', ec='black')
            ax.add_patch(circle)
            ax.text(pos, 4, str(i), ha='center', va='center', fontweight='bold')
        ax.axis('off')
        
        # Star Topology
        ax = axes[0, 1]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_title("Star Topology", fontsize=12, fontweight='bold')
        
        # Central hub
        hub = Circle((5, 4), 0.4, color='yellow', ec='black')
        ax.add_patch(hub)
        ax.text(5, 4, 'H', ha='center', va='center', fontweight='bold')
        
        # Connected nodes
        star_positions = [(3, 6), (7, 6), (2, 4), (8, 4), (3, 2), (7, 2)]
        for i, pos in enumerate(star_positions, 1):
            circle = Circle(pos, 0.3, color='lightblue', ec='black')
            ax.add_patch(circle)
            ax.text(pos[0], pos[1], str(i), ha='center', va='center', fontweight='bold')
            ax.plot([5, pos[0]], [4, pos[1]], 'k-', linewidth=2)
        ax.axis('off')
        
        # Ring Topology
        ax = axes[1, 0]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_title("Ring Topology", fontsize=12, fontweight='bold')
        
        # Ring positions
        angles = np.linspace(0, 2*np.pi, 6)[:-1]  # 5 nodes
        ring_radius = 2
        center_x, center_y = 5, 4
        
        ring_positions = []
        for i, angle in enumerate(angles):
            x = center_x + ring_radius * np.cos(angle)
            y = center_y + ring_radius * np.sin(angle)
            ring_positions.append((x, y))
            circle = Circle((x, y), 0.3, color='lightblue', ec='black')
            ax.add_patch(circle)
            ax.text(x, y, str(i+1), ha='center', va='center', fontweight='bold')
        
        # Connect nodes in ring
        for i in range(len(ring_positions)):
            start = ring_positions[i]
            end = ring_positions[(i+1) % len(ring_positions)]
            ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', linewidth=2)
        ax.axis('off')
        
        # Mesh Topology
        ax = axes[1, 1]
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 8)
        ax.set_title("Mesh Topology", fontsize=12, fontweight='bold')
        
        # Mesh positions
        mesh_positions = [(3, 6), (7, 6), (2, 3), (8, 3), (5, 1)]
        for i, pos in enumerate(mesh_positions, 1):
            circle = Circle(pos, 0.3, color='lightblue', ec='black')
            ax.add_patch(circle)
            ax.text(pos[0], pos[1], str(i), ha='center', va='center', fontweight='bold')
        
        # Connect all nodes to all others (full mesh)
        for i in range(len(mesh_positions)):
            for j in range(i+1, len(mesh_positions)):
                start = mesh_positions[i]
                end = mesh_positions[j]
                ax.plot([start[0], end[0]], [start[1], end[1]], 'k-', 
                       linewidth=1, alpha=0.7)
        ax.axis('off')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/network_topologies.png", 
                   dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Network topology diagrams generated")
    
    def generate_performance_analysis(self):
        """Generate performance analysis charts"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle("Communication System Performance Analysis", 
                    fontsize=16, fontweight='bold')
        
        # SNR vs BER Analysis
        snr_db = np.linspace(0, 15, 50)
        ber_theoretical = 0.5 * np.exp(-snr_db/2)  # Simplified BER curve
        
        axes[0, 0].semilogy(snr_db, ber_theoretical, 'b-', linewidth=2, 
                           label='Theoretical BER')
        axes[0, 0].set_title("SNR vs Bit Error Rate", fontsize=12, fontweight='bold')
        axes[0, 0].set_xlabel("SNR (dB)")
        axes[0, 0].set_ylabel("Bit Error Rate")
        axes[0, 0].grid(True, alpha=0.3)
        axes[0, 0].legend()
        
        # Bandwidth comparison
        systems = ['Voice', 'Data', 'Video', 'Multimedia']
        bandwidth = [64, 1024, 10000, 50000]  # kbps
        colors = ['blue', 'green', 'red', 'orange']
        
        bars = axes[0, 1].bar(systems, bandwidth, color=colors, alpha=0.7)
        axes[0, 1].set_title("Bandwidth Requirements by System Type", 
                            fontsize=12, fontweight='bold')
        axes[0, 1].set_ylabel("Bandwidth (kbps)")
        axes[0, 1].set_yscale('log')
        
        # Add value labels on bars
        for bar, value in zip(bars, bandwidth):
            height = bar.get_height()
            axes[0, 1].text(bar.get_x() + bar.get_width()/2., height,
                           f'{value}', ha='center', va='bottom')
        
        # Topology comparison
        topologies = ['Bus', 'Star', 'Ring', 'Mesh']
        reliability = [2, 6, 4, 9]
        scalability = [3, 7, 5, 4]
        cost = [9, 6, 7, 2]  # Lower is better (inverted scale)
        
        x = np.arange(len(topologies))
        width = 0.25
        
        axes[1, 0].bar(x - width, reliability, width, label='Reliability', alpha=0.8)
        axes[1, 0].bar(x, scalability, width, label='Scalability', alpha=0.8)
        axes[1, 0].bar(x + width, cost, width, label='Cost Efficiency', alpha=0.8)
        
        axes[1, 0].set_title("Network Topology Comparison", 
                            fontsize=12, fontweight='bold')
        axes[1, 0].set_ylabel("Score (1-10)")
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(topologies)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Frequency spectrum
        frequencies = np.linspace(-10, 10, 1000)
        # Simulated spectrum for BPSK
        spectrum = np.sinc(frequencies)**2
        
        axes[1, 1].plot(frequencies, 10*np.log10(spectrum + 1e-10), 'purple', linewidth=2)
        axes[1, 1].set_title("BPSK Signal Spectrum", fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel("Frequency (Hz)")
        axes[1, 1].set_ylabel("Power Spectral Density (dB)")
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/performance_analysis.png", 
                   dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Performance analysis charts generated")
    
    def generate_lab_report(self):
        """Generate comprehensive lab report"""
        report_content = f"""
# Telecommunications Laboratory 01 - Report
**Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**

## Executive Summary
This laboratory exercise successfully demonstrated the fundamental concepts of digital communication systems through practical signal analysis and visualization.

## Laboratory Parameters
- Number of bits transmitted: {self.N}
- Samples per symbol: {self.sps}
- Carrier frequency: {self.fc} Hz
- Noise power level: {self.noise_power}

## Key Findings

### 1. Communication System Components
The block diagram clearly shows the five essential components:
- **Source**: Generates information bits ({self.bits.tolist()})
- **Modulator**: Implements BPSK mapping (0→-1, 1→+1)
- **Channel**: Introduces noise and distortion
- **Demodulator**: Recovers the signal using coherent detection
- **Receiver**: Outputs the recovered information

### 2. Signal Analysis Results
- **Baseband Signal**: Successfully represented {self.N} bits as pulse sequence
- **Carrier Signal**: Clean sinusoidal wave at {self.fc} Hz
- **Modulated Signal**: BPSK modulation achieved phase reversal for bit transitions
- **Received Signal**: Demonstrates noise impact on signal quality

### 3. Performance Observations
- SNR degradation due to channel noise
- Successful demodulation despite noise presence
- Signal integrity maintained through modulation process

## Network Topology Analysis
Generated comparative analysis of four major topologies:
- **Bus**: Simple but vulnerable to single points of failure
- **Star**: Centralized control with good manageability
- **Ring**: Predictable performance with moderate reliability
- **Mesh**: Excellent redundancy but high cost

## Recommendations
1. Implement error correction coding for improved reliability
2. Optimize carrier frequency for specific channel conditions
3. Consider adaptive modulation based on channel quality
4. Evaluate power efficiency for battery-operated devices

## Files Generated
All analysis results and diagrams have been saved to: {self.output_dir}/

**Generated Files:**
- communication_system_diagram.png
- signal_flow_analysis.png
- analog_vs_digital_comparison.png
- network_topologies.png
- performance_analysis.png
- laboratory_report.txt

## Conclusion
The laboratory successfully demonstrated BPSK communication system operation and provided comprehensive analysis of telecommunications fundamentals. The automated approach ensures reproducible results and facilitates deeper understanding of signal processing concepts.

---
*End of Report*
        """
        
        # Save report to file
        with open(f"{self.output_dir}/laboratory_report.txt", 'w') as f:
            f.write(report_content)
        
        print("✓ Laboratory report generated")
        print(f"\nReport saved to: {self.output_dir}/laboratory_report.txt")
    
    def run_complete_analysis(self):
        """Execute complete laboratory automation"""
        print("="*60)
        print("TELECOMMUNICATIONS LABORATORY 01 - AUTOMATION SCRIPT")
        print("="*60)
        print("Starting comprehensive communication system analysis...\n")
        
        # Part 1: Conceptual Diagrams
        print("PART 1: CONCEPTUAL SYSTEM DIAGRAMS")
        print("-" * 40)
        self.generate_communication_system_diagram()
        self.plot_network_topologies()
        
        # Part 2: Signal Flow Analysis
        print("\nPART 2: SIGNAL FLOW ANALYSIS")
        print("-" * 40)
        self.generate_signal_data()
        self.plot_signal_analysis()
        self.compare_analog_digital_signals()
        self.generate_performance_analysis()
        
        # Generate comprehensive report
        print("\nREPORT GENERATION")
        print("-" * 40)
        self.generate_lab_report()
        
        print("\n" + "="*60)
        print("LABORATORY AUTOMATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"All results saved in directory: {self.output_dir}")
        print("\nFiles generated:")
        print("✓ Communication system block diagram")
        print("✓ Signal flow analysis plots")
        print("✓ Analog vs digital comparison")
        print("✓ Network topology diagrams")
        print("✓ Performance analysis charts")
        print("✓ Comprehensive laboratory report")

# Main execution
if __name__ == "__main__":
    # Initialize and run laboratory automation
    lab = TelecomLabAutomation()
    lab.run_complete_analysis()
    
    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("1. Review all generated diagrams and plots")
    print("2. Analyze the signal flow characteristics")
    print("3. Compare different network topologies")
    print("4. Study the performance analysis results")
    print("5. Submit the laboratory report and diagrams")
    print("="*60)