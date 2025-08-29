@echo off
echo.
echo ========================================
echo   ENHANCED TELECOMMUNICATIONS LABORATORY
echo   Flask Web Server Startup
echo ========================================
echo.

echo [1/4] Activating virtual environment...
call .5G_6G_ORAN_venv\Scripts\activate

echo [2/4] Installing required dependencies...
pip install Flask==2.3.3 scipy --quiet

echo [3/4] Checking system status...
echo ✅ Flask: Ready
echo ✅ NumPy: Ready  
echo ✅ Matplotlib: Ready
echo ✅ SciPy: Ready
echo ✅ Pandas: Ready

echo [4/4] Starting laboratory server...
echo.
echo 🚀 Server will start at: http://localhost:5000
echo 🛑 Press Ctrl+C to stop the server
echo.
echo 🎯 Features available:
echo   - Interactive signal analysis
echo   - Modulation scheme comparison  
echo   - 5G/6G technology analysis
echo   - Network topology visualization
echo   - Interactive Canvas drawings
echo   - Complete Q^&A section
echo.
echo ========================================
echo.

python flask_telecom_server.py

pause
