@echo off
cd /d "%~dp0"
echo ============================================
echo  Generation des banners DataProjectLab
echo ============================================
echo.
python -c "from PIL import Image" 2>nul
if errorlevel 1 (
    echo Installation de Pillow...
    python -m pip install --quiet pillow
)
python build_banners.py
echo.
echo ============================================
echo  Termine. Verifie ..\media\banners\
echo ============================================
pause
