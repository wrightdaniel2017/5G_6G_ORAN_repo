@echo off
echo 🔧 Network Topology Animation Fix Tool
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.x and try again
    pause
    exit /b 1
)

REM Run the fix script
python fix_topology_animations.py

echo.
echo Press any key to exit...
pause >nul
