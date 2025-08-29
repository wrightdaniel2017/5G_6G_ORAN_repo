#!/usr/bin/env python3
"""
Enhanced Flask Telecommunications Laboratory with Advanced Tooltip System
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
from advanced_tooltip_api import setup_advanced_tooltips

app = Flask(__name__)
app.config['SECRET_KEY'] = 'telecom_lab_2025_enhanced'

# Setup advanced tooltip management
tooltip_manager = setup_advanced_tooltips(app)

# Extended acronyms database with latest additions
def load_acronyms():
    """Load the comprehensive telecommunications acronyms database"""
    acronym_data = {
        "acronyms": {
            # Core 5G/6G Technologies
            "5G": "Fifth Generation - The latest standard for broadband cellular networks",
            "6G": "Sixth Generation - Next-generation wireless technology beyond 5G", 
            "NR": "New Radio - The radio access technology for 5G networks",
            "ORAN": "Open Radio Access Network - An initiative to disaggregate RAN functions",
            "O-RAN": "Open Radio Access Network - An open and intelligent RAN architecture",
            "RAN": "Radio Access Network - Part of a mobile telecommunication system",
            "NSA": "Non-Standalone - 5G deployment mode using existing 4G core",
            "SA": "Standalone - Pure 5G deployment with 5G core network",
            "FR1": "Frequency Range 1 - Sub-6 GHz frequency bands for 5G",
            "FR2": "Frequency Range 2 - mmWave frequency bands for 5G (24-100 GHz)",
            
            # Advanced Core Network Functions
            "5GC": "5G Core - Core network architecture for 5G networks",
            "EPC": "Evolved Packet Core - Core network architecture for LTE",
            "AMF": "Access and Mobility Management Function - 5G core network function",
            "SMF": "Session Management Function - 5G core network function",
            "UPF": "User Plane Function - 5G core network function for data routing",
            "AUSF": "Authentication Server Function - 5G core network function",
            "UDM": "Unified Data Management - 5G core network function",
            "UDR": "Unified Data Repository - 5G data storage function",
            "PCF": "Policy Control Function - 5G policy management function",
            "NSSF": "Network Slice Selection Function - 5G network slicing function",
            "NRF": "Network Repository Function - 5G service discovery function",
            "NEF": "Network Exposure Function - 5G external API gateway",
            "AF": "Application Function - 5G application integration function",
            "UDSF": "Unstructured Data Storage Function - 5G analytics data storage",
            "NWDAF": "Network Data Analytics Function - 5G AI/ML analytics",
            "CHF": "Charging Function - 5G charging and billing function",
            "BSF": "Binding Support Function - 5G service binding function",
            
            # RAN Architecture Components
            "RIC": "RAN Intelligent Controller - AI/ML enabled RAN optimization platform",
            "Near-RT RIC": "Near Real-Time RAN Intelligent Controller - Edge RAN intelligence",
            "Non-RT RIC": "Non Real-Time RAN Intelligent Controller - Cloud RAN intelligence",
            "SMO": "Service Management and Orchestration - O-RAN management function",
            "CU": "Central Unit - Upper layer RAN function in 5G architecture",
            "DU": "Distributed Unit - Lower layer RAN function in 5G architecture",
            "RU": "Radio Unit - Radio frequency part of base station",
            "O-CU": "O-RAN Central Unit - Centralized baseband processing unit",
            "O-DU": "O-RAN Distributed Unit - Distributed baseband processing unit",
            "O-RU": "O-RAN Radio Unit - Open radio unit interface",
            "O-Cloud": "O-RAN Cloud - Cloud infrastructure for O-RAN functions",
            "rApp": "RAN Application - Applications running on Non-RT RIC",
            "xApp": "RAN Application - Applications running on Near-RT RIC",
            
            # Advanced Modulation and Signal Processing
            "BPSK": "Binary Phase Shift Keying - Digital modulation technique using phase changes",
            "QPSK": "Quadrature Phase Shift Keying - Digital modulation technique using four phase states",
            "QAM": "Quadrature Amplitude Modulation - Digital modulation scheme using amplitude and phase",
            "16-QAM": "16-Quadrature Amplitude Modulation - QAM using 16 distinct combinations",
            "64-QAM": "64-Quadrature Amplitude Modulation - QAM using 64 distinct combinations",
            "256-QAM": "256-Quadrature Amplitude Modulation - High-order QAM scheme",
            "1024-QAM": "1024-Quadrature Amplitude Modulation - Ultra-high-order QAM",
            "OFDM": "Orthogonal Frequency Division Multiplexing - Multi-carrier modulation technique",
            "OFDMA": "Orthogonal Frequency Division Multiple Access - Multi-user OFDM",
            "SC-FDMA": "Single Carrier Frequency Division Multiple Access - Uplink access scheme",
            "DFT-S-OFDM": "Discrete Fourier Transform Spread OFDM - 5G uplink waveform",
            "CP-OFDM": "Cyclic Prefix OFDM - Standard OFDM with cyclic prefix",
            "FBMC": "Filter Bank Multicarrier - Advanced waveform for 6G",
            "UFMC": "Universal Filtered Multicarrier - 5G candidate waveform",
            "GFDM": "Generalized Frequency Division Multiplexing - Advanced modulation",
            
            # MIMO Technologies
            "MIMO": "Multiple-Input Multiple-Output - Multi-antenna technology",
            "SU-MIMO": "Single-User MIMO - MIMO for one user at a time",
            "MU-MIMO": "Multi-User MIMO - MIMO serving multiple users simultaneously",
            "Massive MIMO": "Large-scale MIMO - MIMO with hundreds of antennas",
            "FD-MIMO": "Full-Dimension MIMO - 3D beamforming MIMO system",
            "Distributed MIMO": "Distributed MIMO - Spatially distributed antenna system",
            "CoMP": "Coordinated Multipoint - Cooperative MIMO transmission",
            "Beamforming": "Beamforming - Directional signal transmission technique",
            "Precoding": "Precoding - Signal preprocessing for MIMO systems",
            
            # Service Categories and Applications
            "eMBB": "Enhanced Mobile Broadband - High-speed data service category",
            "URLLC": "Ultra-Reliable Low Latency Communication - Mission-critical service",
            "mMTC": "Massive Machine Type Communication - IoT service category",
            "V2X": "Vehicle-to-Everything - Automotive communication service",
            "V2V": "Vehicle-to-Vehicle - Direct vehicle communication",
            "V2I": "Vehicle-to-Infrastructure - Vehicle to roadside communication",
            "V2N": "Vehicle-to-Network - Vehicle to cellular network communication",
            "V2P": "Vehicle-to-Pedestrian - Vehicle to pedestrian device communication",
            "XR": "Extended Reality - AR/VR/MR applications",
            "AR": "Augmented Reality - Computer-generated overlay on real world",
            "VR": "Virtual Reality - Immersive computer-generated environment",
            "MR": "Mixed Reality - Blend of physical and digital worlds",
            "Tactile Internet": "Tactile Internet - Ultra-low latency haptic communication",
            "Digital Twin": "Digital Twin - Real-time digital replica of physical systems",
            
            # Performance Metrics and Quality
            "BER": "Bit Error Rate - Percentage of bits with errors",
            "PER": "Packet Error Rate - Percentage of packets with errors",
            "FER": "Frame Error Rate - Percentage of frames with errors",
            "BLER": "Block Error Rate - Percentage of blocks with errors",
            "SNR": "Signal-to-Noise Ratio - Signal strength vs noise measure",
            "SINR": "Signal-to-Interference-plus-Noise Ratio - Signal quality with interference",
            "CNR": "Carrier-to-Noise Ratio - Carrier signal vs noise measure",
            "RSSI": "Received Signal Strength Indicator - Power level measurement",
            "RSRP": "Reference Signal Received Power - LTE/5G signal strength",
            "RSRQ": "Reference Signal Received Quality - LTE/5G signal quality",
            "SS-RSRP": "Synchronization Signal RSRP - 5G NR signal strength",
            "SS-RSRQ": "Synchronization Signal RSRQ - 5G NR signal quality",
            "SS-SINR": "Synchronization Signal SINR - 5G NR signal quality",
            "CQI": "Channel Quality Indicator - Feedback for link adaptation",
            "PMI": "Precoding Matrix Indicator - MIMO precoding feedback",
            "RI": "Rank Indicator - MIMO layer count feedback",
            "CSI": "Channel State Information - Complete channel feedback",
            "QoS": "Quality of Service - Network performance guarantee",
            "QoE": "Quality of Experience - User-perceived service quality",
            "SLS": "Service Level Specification - Network slice performance requirements",
            
            # Advanced Radio Technologies
            "RF": "Radio Frequency - Electromagnetic waves for communication",
            "mmWave": "Millimeter Wave - High-frequency radio waves (24-100 GHz)",
            "Sub-6": "Sub-6 GHz - Frequency bands below 6 GHz",
            "THz": "Terahertz - Ultra-high frequency waves (0.1-10 THz)",
            "Beamforming": "Beamforming - Directional antenna transmission",
            "Beam Steering": "Beam Steering - Dynamic beam direction control",
            "Beam Tracking": "Beam Tracking - Following mobile device with beam",
            "Beam Management": "Beam Management - Complete beam control system",
            "Cell-Free": "Cell-Free - Distributed antenna system without cell boundaries",
            "RIS": "Reconfigurable Intelligent Surface - Smart reflecting surfaces",
            "IRS": "Intelligent Reflecting Surface - Programmable metasurfaces",
            "UAV": "Unmanned Aerial Vehicle - Drone-based communication",
            "HAP": "High Altitude Platform - Stratospheric communication platform",
            "LEO": "Low Earth Orbit - Satellite constellation at low altitude",
            "MEO": "Medium Earth Orbit - Satellite constellation at medium altitude",
            "GEO": "Geostationary Earth Orbit - Fixed position satellite",
            
            # AI/ML and Intelligence
            "AI": "Artificial Intelligence - Machine intelligence for network optimization",
            "ML": "Machine Learning - Algorithm learning from data",
            "DL": "Deep Learning - Multi-layer neural network learning",
            "RL": "Reinforcement Learning - Trial-and-error based learning",
            "FL": "Federated Learning - Distributed machine learning",
            "AutoML": "Automated Machine Learning - Automated ML model development",
            "MLOps": "Machine Learning Operations - ML lifecycle management",
            "AIOps": "Artificial Intelligence for IT Operations - AI-driven operations",
            "Intent-Based": "Intent-Based Networking - High-level policy automation",
            "Zero-Touch": "Zero-Touch Network - Fully automated network management",
            "SON": "Self-Organizing Network - Automated network optimization",
            "ANR": "Automatic Neighbor Relations - Self-configuring neighbor lists",
            
            # Security and Privacy
            "SSL": "Secure Sockets Layer - Encryption protocol",
            "TLS": "Transport Layer Security - SSL successor encryption protocol",
            "IPSec": "Internet Protocol Security - IP layer security framework",
            "VPN": "Virtual Private Network - Secure network tunnel",
            "PKI": "Public Key Infrastructure - Digital certificate management",
            "AES": "Advanced Encryption Standard - Symmetric encryption algorithm",
            "RSA": "Rivest-Shamir-Adleman - Public key encryption algorithm",
            "ECC": "Elliptic Curve Cryptography - Public key cryptography method",
            "ECDSA": "Elliptic Curve Digital Signature Algorithm - Digital signature",
            "ECDH": "Elliptic Curve Diffie-Hellman - Key exchange algorithm",
            "5G-AKA": "5G Authentication and Key Agreement - 5G security protocol",
            "SUCI": "Subscription Concealed Identifier - Privacy-preserving identifier",
            "SUPI": "Subscription Permanent Identifier - Permanent user identifier",
            "GUTI": "Globally Unique Temporary Identifier - Temporary user identifier",
            "PEI": "Permanent Equipment Identifier - Device identifier",
            "Zero Trust": "Zero Trust - Never trust, always verify security model",
            "SASE": "Secure Access Service Edge - Cloud-delivered network security",
            "ZTNA": "Zero Trust Network Access - Secure remote access",
            
            # Emerging Technologies
            "Blockchain": "Blockchain - Distributed ledger technology",
            "DLT": "Distributed Ledger Technology - Decentralized database",
            "Smart Contract": "Smart Contract - Self-executing contract with code",
            "NFT": "Non-Fungible Token - Unique digital asset",
            "Metaverse": "Metaverse - Persistent virtual shared space",
            "Web3": "Web3 - Decentralized internet built on blockchain",
            "DeFi": "Decentralized Finance - Blockchain-based financial services",
            "DAO": "Decentralized Autonomous Organization - Blockchain governance",
            "Quantum Computing": "Quantum Computing - Computing using quantum mechanics",
            "QKD": "Quantum Key Distribution - Quantum-secure key exchange",
            "PQC": "Post-Quantum Cryptography - Quantum-resistant encryption",
            "Neuromorphic": "Neuromorphic Computing - Brain-inspired computing",
            "Photonic": "Photonic Computing - Light-based computing",
            "DNA Storage": "DNA Storage - Data storage using DNA molecules",
            
            # Standards and Organizations  
            "3GPP": "3rd Generation Partnership Project - Mobile standards organization",
            "IEEE": "Institute of Electrical and Electronics Engineers - Technical standards",
            "ITU": "International Telecommunication Union - UN telecom agency",
            "ITU-T": "ITU Telecommunication Standardization Sector - Telecom standards",
            "ITU-R": "ITU Radiocommunication Sector - Radio standards",
            "ETSI": "European Telecommunications Standards Institute - European standards",
            "IETF": "Internet Engineering Task Force - Internet standards",
            "W3C": "World Wide Web Consortium - Web standards",
            "GSMA": "GSM Association - Mobile operator alliance",
            "O-RAN Alliance": "Open RAN Alliance - Open RAN standards consortium",
            "TIP": "Telecom Infra Project - Open source telecom infrastructure",
            "Linux Foundation": "Linux Foundation - Open source software collaboration",
            "CNCF": "Cloud Native Computing Foundation - Cloud native standards",
            "ONF": "Open Networking Foundation - SDN standards organization",
            
            # IoT and Connectivity
            "IoT": "Internet of Things - Network of connected devices",
            "IIoT": "Industrial Internet of Things - IoT in industrial settings",
            "AIoT": "Artificial Intelligence of Things - AI-powered IoT devices",
            "M2M": "Machine-to-Machine - Direct device communication",
            "WSN": "Wireless Sensor Network - Network of sensor nodes",
            "RFID": "Radio Frequency Identification - Wireless identification technology",
            "NFC": "Near Field Communication - Short-range communication technology",
            "LoRa": "Long Range - Low-power wide-area network technology",
            "LoRaWAN": "LoRa Wide Area Network - Network protocol for LoRa",
            "Sigfox": "Sigfox - Low-power wide-area network technology",
            "NB-IoT": "Narrowband IoT - Cellular IoT technology",
            "LTE-M": "LTE for Machines - Cellular IoT technology",
            "Cat-M1": "Category M1 - LTE-M device category",
            "LPWAN": "Low-Power Wide-Area Network - IoT connectivity technology",
            "Thread": "Thread - IPv6-based mesh networking for IoT",
            "Matter": "Matter - Universal IoT connectivity standard",
            "Zigbee": "Zigbee - Low-power mesh networking standard",
            "Z-Wave": "Z-Wave - Low-power mesh networking for home automation"
        },
        "categories": {
            "5G/6G Technologies": ["5G", "6G", "NR", "ORAN", "O-RAN", "RAN", "NSA", "SA", "FR1", "FR2", "gNB", "ng-eNB"],
            "Core Network": ["5GC", "EPC", "AMF", "SMF", "UPF", "AUSF", "UDM", "UDR", "PCF", "NSSF", "NRF", "NEF", "AF", "UDSF", "NWDAF", "CHF", "BSF"],
            "RAN Components": ["RIC", "Near-RT RIC", "Non-RT RIC", "SMO", "CU", "DU", "RU", "O-CU", "O-DU", "O-RU", "O-Cloud", "rApp", "xApp"],
            "Modulation": ["BPSK", "QPSK", "QAM", "16-QAM", "64-QAM", "256-QAM", "1024-QAM", "OFDM", "OFDMA", "SC-FDMA", "DFT-S-OFDM", "CP-OFDM", "FBMC", "UFMC", "GFDM"],
            "MIMO Technologies": ["MIMO", "SU-MIMO", "MU-MIMO", "Massive MIMO", "FD-MIMO", "Distributed MIMO", "CoMP", "Beamforming", "Precoding"],
            "Service Categories": ["eMBB", "URLLC", "mMTC", "V2X", "V2V", "V2I", "V2N", "V2P", "XR", "AR", "VR", "MR", "Tactile Internet", "Digital Twin"],
            "Performance Metrics": ["BER", "PER", "FER", "BLER", "SNR", "SINR", "CNR", "RSSI", "RSRP", "RSRQ", "SS-RSRP", "SS-RSRQ", "SS-SINR", "CQI", "PMI", "RI", "CSI", "QoS", "QoE", "SLS"],
            "Radio Technologies": ["RF", "mmWave", "Sub-6", "THz", "Beam Steering", "Beam Tracking", "Beam Management", "Cell-Free", "RIS", "IRS", "UAV", "HAP", "LEO", "MEO", "GEO"],
            "AI/ML": ["AI", "ML", "DL", "RL", "FL", "AutoML", "MLOps", "AIOps", "Intent-Based", "Zero-Touch", "SON", "ANR"],
            "Security": ["SSL", "TLS", "IPSec", "VPN", "PKI", "AES", "RSA", "ECC", "ECDSA", "ECDH", "5G-AKA", "SUCI", "SUPI", "GUTI", "PEI", "Zero Trust", "SASE", "ZTNA"],
            "Emerging Technologies": ["Blockchain", "DLT", "Smart Contract", "NFT", "Metaverse", "Web3", "DeFi", "DAO", "Quantum Computing", "QKD", "PQC", "Neuromorphic", "Photonic", "DNA Storage"],
            "Standards Organizations": ["3GPP", "IEEE", "ITU", "ITU-T", "ITU-R", "ETSI", "IETF", "W3C", "GSMA", "O-RAN Alliance", "TIP", "Linux Foundation", "CNCF", "ONF"],
            "IoT Technologies": ["IoT", "IIoT", "AIoT", "M2M", "WSN", "RFID", "NFC", "LoRa", "LoRaWAN", "Sigfox", "NB-IoT", "LTE-M", "Cat-M1", "LPWAN", "Thread", "Matter", "Zigbee", "Z-Wave"]
        }
    }
    return acronym_data

@app.route('/')
def index():
    """Main telecommunications laboratory page with enhanced tooltips"""
    return render_template('index.html')

@app.route('/tooltip_dashboard')
def tooltip_dashboard():
    """Advanced tooltip management dashboard"""
    return render_template('tooltip_dashboard.html')

@app.route('/api/acronyms')
def get_acronyms():
    """API endpoint to get all acronyms for the tooltip system"""
    try:
        acronym_data = load_acronyms()
        return jsonify({
            'success': True,
            'data': acronym_data,
            'count': len(acronym_data['acronyms']),
            'categories': len(acronym_data['categories'])
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

# Include all the existing Flask routes from the original app
@app.route('/analytics')
def analytics_dashboard():
    """Analytics dashboard for tooltip usage insights"""
    return render_template('analytics_dashboard.html')

@app.route('/enhanced_test')
def enhanced_tooltip_test():
    """Enhanced tooltip testing and demonstration page"""
    return render_template('enhanced_tooltip_test.html')

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

# All the existing signal processing and visualization routes
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
    """Generate constellation diagram for modulation scheme"""
    try:
        plt.figure(figsize=(8, 6))
        
        if modulation == 'BPSK':
            # BPSK constellation points
            points = np.array([-1, 1])
            plt.scatter([p for p in points], [0]*len(points), s=100, c='red', marker='o')
            plt.title('BPSK Constellation Diagram')
            plt.xlim(-2, 2)
            plt.ylim(-1, 1)
            
        elif modulation == 'QPSK':
            # QPSK constellation points
            points = np.array([1+1j, -1+1j, -1-1j, 1-1j]) / np.sqrt(2)
            plt.scatter([p.real for p in points], [p.imag for p in points], s=100, c='blue', marker='o')
            plt.title('QPSK Constellation Diagram')
            plt.xlim(-1.5, 1.5)
            plt.ylim(-1.5, 1.5)
            
        elif modulation == '16-QAM':
            # 16-QAM constellation points
            points = []
            for i in [-3, -1, 1, 3]:
                for q in [-3, -1, 1, 3]:
                    points.append(complex(i, q))
            points = np.array(points) / np.sqrt(10)
            plt.scatter([p.real for p in points], [p.imag for p in points], s=100, c='green', marker='o')
            plt.title('16-QAM Constellation Diagram')
            plt.xlim(-1.5, 1.5)
            plt.ylim(-1.5, 1.5)
            
        plt.xlabel('In-Phase (I)')
        plt.ylabel('Quadrature (Q)')
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        
        # Convert to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=300, bbox_inches='tight')
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode()
        plt.close()
        
        return jsonify({
            'success': True,
            'plot': img_base64,
            'modulation': modulation
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
        snr_db = np.linspace(0, 20, 21)
        snr_linear = 10**(snr_db/10)
        
        # Theoretical BER calculations
        ber_bpsk = 0.5 * np.exp(-snr_linear)
        ber_qpsk = 0.5 * np.exp(-snr_linear)
        ber_16qam = 3/8 * np.exp(-snr_linear/2.5)
        
        plt.figure(figsize=(10, 6))
        plt.semilogy(snr_db, ber_bpsk, 'r-o', label='BPSK', linewidth=2)
        plt.semilogy(snr_db, ber_qpsk, 'b-s', label='QPSK', linewidth=2)
        plt.semilogy(snr_db, ber_16qam, 'g-^', label='16-QAM', linewidth=2)
        
        plt.xlabel('SNR (dB)')
        plt.ylabel('Bit Error Rate (BER)')
        plt.title('BER vs SNR Performance Comparison')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.xlim(0, 20)
        plt.ylim(1e-6, 1)
        
        # Convert to base64
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
def comparison_5g():
    """Generate 5G vs 4G vs 6G comparison chart"""
    try:
        technologies = ['4G LTE', '5G', '6G (Future)']
        peak_speeds = [1, 20, 1000]  # Gbps
        latency = [50, 1, 0.1]  # ms
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
        
        # Peak speeds comparison
        bars1 = ax1.bar(technologies, peak_speeds, color=['blue', 'green', 'red'])
        ax1.set_ylabel('Peak Speed (Gbps)')
        ax1.set_title('Peak Data Rates')
        ax1.set_yscale('log')
        
        # Latency comparison
        bars2 = ax2.bar(technologies, latency, color=['blue', 'green', 'red'])
        ax2.set_ylabel('Latency (ms)')
        ax2.set_title('Network Latency')
        ax2.set_yscale('log')
        
        plt.tight_layout()
        
        # Convert to base64
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
            plt.title('Star Network Topology')
            # Draw star topology
            center = (0, 0)
            plt.scatter(*center, s=500, c='red', marker='*', label='Hub/Switch')
            
            # Draw nodes around the center
            angles = np.linspace(0, 2*np.pi, 7)
            for i, angle in enumerate(angles[:-1]):
                x = 2 * np.cos(angle)
                y = 2 * np.sin(angle)
                plt.scatter(x, y, s=300, c='blue', marker='o')
                plt.plot([center[0], x], [center[1], y], 'k-', alpha=0.7)
                plt.text(x*1.2, y*1.2, f'PC{i+1}', ha='center', va='center')
                
        elif topology == 'mesh':
            plt.title('Mesh Network Topology')
            # Draw mesh topology
            positions = [(0, 2), (2, 1), (2, -1), (0, -2), (-2, -1), (-2, 1)]
            
            for i, pos in enumerate(positions):
                plt.scatter(*pos, s=300, c='green', marker='o')
                plt.text(pos[0]*1.2, pos[1]*1.2, f'Node{i+1}', ha='center', va='center')
                
                # Connect to all other nodes
                for j, other_pos in enumerate(positions):
                    if i < j:  # Avoid duplicate lines
                        plt.plot([pos[0], other_pos[0]], [pos[1], other_pos[1]], 'k-', alpha=0.5)
                        
        elif topology == 'ring':
            plt.title('Ring Network Topology')
            # Draw ring topology
            angles = np.linspace(0, 2*np.pi, 7)
            positions = []
            
            for i, angle in enumerate(angles[:-1]):
                x = 2 * np.cos(angle)
                y = 2 * np.sin(angle)
                positions.append((x, y))
                plt.scatter(x, y, s=300, c='purple', marker='o')
                plt.text(x*1.2, y*1.2, f'Node{i+1}', ha='center', va='center')
            
            # Connect nodes in ring
            for i in range(len(positions)):
                next_i = (i + 1) % len(positions)
                plt.plot([positions[i][0], positions[next_i][0]], 
                        [positions[i][1], positions[next_i][1]], 'k-', alpha=0.7)
        
        plt.axis('equal')
        plt.xlim(-4, 4)
        plt.ylim(-4, 4)
        plt.grid(True, alpha=0.3)
        
        # Convert to base64
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
    print("📡 Features: Advanced Tooltips, Signal Processing, AI Analytics")
    print("🔍 New Features: Smart Search, Context Awareness, Learning Mode")
    print("🌐 Access: http://localhost:5000")
    print("🎛️  Dashboard: http://localhost:5000/tooltip_dashboard")
    print("="*70)
    app.run(debug=True, host='0.0.0.0', port=5000)
