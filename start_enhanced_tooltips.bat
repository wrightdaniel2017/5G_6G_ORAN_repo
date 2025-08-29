@echo off
cls
echo ================================================================
echo    Enhanced Telecommunications Laboratory - Tooltip System
echo ================================================================
echo.
echo 🚀 Starting Enhanced Tooltip System with Advanced Features...
echo.
echo Features Included:
echo ✅ 300+ Telecommunications Acronyms
echo ✅ Smart Search with Fuzzy Matching
echo ✅ Context-Aware Suggestions
echo ✅ Learning Mode with Progress Tracking
echo ✅ Audio Pronunciation Support
echo ✅ Analytics Dashboard
echo ✅ Custom Acronym Management
echo ✅ Advanced API Endpoints
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".5G_6G_ORAN_venv" (
    echo 📦 Creating virtual environment...
    python -m venv .5G_6G_ORAN_venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call .5G_6G_ORAN_venv\Scripts\activate.bat

REM Install/update requirements
if exist "requirements.txt" (
    echo 📥 Installing/updating dependencies...
    pip install -r requirements.txt --quiet
) else (
    echo 📥 Installing core dependencies...
    pip install flask matplotlib numpy sqlite3 --quiet
)

REM Check for enhanced app
if exist "enhanced_app_v2.py" (
    echo ✨ Starting Enhanced Telecommunications Laboratory...
    echo.
    echo 🌐 Server will be available at:
    echo    Main Lab: http://localhost:5000
    echo    Tooltip Dashboard: http://localhost:5000/tooltip_dashboard
    echo    Enhanced Testing: http://localhost:5000/tooltip_test
    echo    Analytics: http://localhost:5000/analytics
    echo.
    echo 🎯 Enhanced Features:
    echo    • Smart Search: Ctrl+Shift+F
    echo    • Learning Mode: Ctrl+L
    echo    • Help: Ctrl+H
    echo    • Close Dialogs: Esc
    echo.
    echo 📊 New API Endpoints:
    echo    • POST /api/tooltips/search - Smart search
    echo    • GET /api/tooltips/related/[acronym] - Related terms
    echo    • POST /api/tooltips/analytics - Usage tracking
    echo    • POST /api/tooltips/custom - Add custom acronyms
    echo.
    echo Press Ctrl+C to stop the server
    echo ================================================================
    python enhanced_app_v2.py
) else (
    echo ❌ Enhanced app not found, trying original...
    if exist "flask_app_with_tooltips.py" (
        python flask_app_with_tooltips.py
    ) else if exist "enhanced_app.py" (
        python enhanced_app.py
    ) else (
        echo ❌ No Flask application found!
        echo Please ensure you have enhanced_app_v2.py in the current directory
        pause
        exit /b 1
    )
)

REM Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo ❌ Server stopped with errors
    pause
)
