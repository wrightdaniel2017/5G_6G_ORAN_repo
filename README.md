# Enhanced Telecommunications Laboratory - Flask Web Server

A comprehensive web-based telecommunications laboratory featuring advanced signal processing, modulation analysis, and 5G/6G system demonstrations.

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Virtual environment (recommended)

### Installation and Setup

1. **Activate your existing virtual environment:**
   ```bash
   # On Windows
   .5G_6G_ORAN_venv\Scripts\activate
   
   # On macOS/Linux
   source .5G_6G_ORAN_venv/bin/activate
   ```

2. **Install additional dependencies:**
   ```bash
   pip install Flask==2.3.3
   ```
   *Note: Other dependencies (numpy, matplotlib, pandas, seaborn) are already installed in your environment*

3. **Run the Flask server:**
   ```bash
   python flask_telecom_server.py
   ```

4. **Access the laboratory:**
   Open your web browser and navigate to: `http://localhost:5000`

## 📡 Features

### Interactive Web Interface
- **Real-time Signal Processing**: Generate and analyze BPSK, QPSK, and 16-QAM signals
- **Interactive Controls**: Adjust parameters like number of bits, modulation scheme, and noise level
- **Live Visualizations**: Real-time plots and constellation diagrams

### Advanced Analysis Tools
- **Modulation Comparison**: Interactive constellation diagrams for different schemes
- **Performance Metrics**: BER vs SNR analysis with theoretical curves
- **5G/6G Technology**: Comparison charts for wireless technology evolution
- **Network Topologies**: Visual representation of star, mesh, and ring architectures

### Educational Content
- **Comprehensive Q&A**: All five telecommunications questions with detailed answers
- **Interactive Learning**: Click-to-explore modulation schemes and network topologies
- **Professional Visualizations**: Publication-quality plots and diagrams

## 🎯 Laboratory Sections

1. **Signal Analysis Controls**
   - Adjust number of bits (20-200)
   - Select modulation scheme (BPSK, QPSK, 16-QAM)
   - Control noise level (0.0-1.0)

2. **Modulation Schemes Analysis**
   - Interactive constellation diagrams
   - Spectral efficiency comparison
   - Application recommendations

3. **Performance Analysis**
   - Real-time BER calculations
   - SNR measurements
   - Throughput metrics

4. **5G/6G Technology Analysis**
   - Technology evolution comparison
   - Peak throughput analysis
   - Latency comparison charts

5. **Network Topology Visualization**
   - Star, mesh, and ring topologies
   - Interactive selection
   - Performance characteristics

## 🔬 Technical Specifications

### Server Architecture
- **Backend**: Flask with Python 3.7+
- **Signal Processing**: NumPy and SciPy
- **Visualization**: Matplotlib with web-optimized output
- **Data Analysis**: Pandas for metrics calculation
- **Styling**: Seaborn for professional plots

### Web Interface
- **Frontend**: Bootstrap 5.3 with responsive design
- **Icons**: Font Awesome 6.4
- **Charts**: Base64-encoded matplotlib figures
- **Interactivity**: Vanilla JavaScript with AJAX

### Supported Analysis
- **Modulation Schemes**: BPSK, QPSK, 16-QAM with constellation diagrams
- **Channel Models**: AWGN (Additive White Gaussian Noise)
- **Performance Metrics**: BER, SNR, spectral efficiency, throughput
- **Network Analysis**: Star, mesh, ring topology visualization

## 🎓 Educational Objectives

This laboratory demonstrates:
- Digital communication system fundamentals
- Modulation scheme characteristics and trade-offs
- Performance analysis and optimization
- Modern 5G/6G wireless technologies
- Network architecture principles

## 🛠️ Customization

### Adding New Modulation Schemes
1. Update the `WebTelecomLab` class in `flask_telecom_server.py`
2. Add constellation mapping in `generate_constellation_plot()`
3. Update the HTML select options in `templates/index.html`

### Adding New Network Topologies
1. Create new topology visualization in the `/network_topology/<topology>` route
2. Add topology button in the HTML interface
3. Include performance characteristics

### Extending Performance Analysis
1. Modify `generate_performance_plot()` for additional metrics
2. Update the performance metrics display in the HTML template
3. Add new calculation functions as needed

## 📊 Output Files

The server generates:
- **Interactive Plots**: Real-time signal analysis charts
- **Constellation Diagrams**: Modulation scheme visualizations
- **Performance Curves**: BER vs SNR theoretical analysis
- **Technology Comparisons**: 5G evolution charts
- **Topology Diagrams**: Network architecture visualizations

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all packages are installed: `pip install -r requirements.txt`
   - Activate the virtual environment before running

2. **Port Already in Use**
   - Change the port in `flask_telecom_server.py`: `app.run(port=5001)`

3. **Plots Not Displaying**
   - Check matplotlib backend configuration
   - Ensure PIL (Pillow) is installed for image processing

4. **Slow Performance**
   - Reduce number of bits for analysis (< 100 for web interface)
   - Decrease plot resolution if needed

## 📈 Advanced Usage

### API Endpoints
- `GET /`: Main laboratory interface
- `POST /generate_signals`: Generate modulated signals
- `GET /constellation/<modulation>`: Get constellation diagram
- `GET /performance_analysis`: BER vs SNR analysis
- `GET /5g_comparison`: Technology evolution charts
- `GET /network_topology/<topology>`: Network visualizations
- `GET /api/lab_status`: Current system status

### Data Export
- JSON format for analysis parameters
- Base64-encoded PNG images for plots
- CSV export capability for signal data

## 🎉 Getting Started

1. Start the server: `python flask_telecom_server.py`
2. Open `http://localhost:5000` in your browser
3. Explore the signal analysis controls
4. Try different modulation schemes
5. Compare network topologies
6. Review the comprehensive Q&A section

Enjoy exploring advanced telecommunications concepts with this interactive laboratory!
