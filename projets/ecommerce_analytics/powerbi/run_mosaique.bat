@echo off
cd /d "%~dp0"
echo ============================================
echo  Construction de la mosaique 2x3 ShopAfrica+
echo ============================================
echo.
python -c "from PIL import Image" 2>nul
if errorlevel 1 (
    echo Installation de Pillow...
    python -m pip install --quiet pillow
)
python build_mosaique.py
echo.
echo ============================================
echo  Termine. Verifie images\00_overview_5_pages_mosaic.png
echo ============================================
pause
