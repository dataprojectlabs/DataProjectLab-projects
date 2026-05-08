@echo off
cd /d "%~dp0"
echo ============================================
echo  Generation synthese executive EduTrack
echo ============================================
echo.
python -c "from pptx import Presentation" 2>nul
if errorlevel 1 (
    echo Installation de python-pptx...
    python -m pip install --quiet python-pptx
)
python build_synthese_edutrack.py
if errorlevel 1 (
    echo [ERREUR] La generation a echoue.
    pause
    exit /b 1
)
echo.
echo Fichier produit : synthese_edutrack.pptx (10 slides)
echo.
pause
