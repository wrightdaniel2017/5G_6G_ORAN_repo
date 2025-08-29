@echo off
echo.
echo ========================================
echo   TELECOMMUNICATIONS LABORATORY
echo   Quick Fix Installation
echo ========================================
echo.

echo [1/2] Activating virtual environment...
call .5G_6G_ORAN_venv\Scripts\activate

echo [2/2] Installing missing dependency (SciPy)...
pip install scipy --quiet

echo.
echo ✅ Fixed! SciPy installed successfully.
echo.
echo Now restart the server by running:
echo   python flask_telecom_server.py
echo.
echo Or simply double-click: start_telecom_lab.bat
echo.
pause
