@echo off
cd /d "%~dp0"
echo ============================================
echo  Generation rapport recommandations EduTrack
echo ============================================
echo.
python -c "from docx import Document" 2>nul
if errorlevel 1 (
    echo Installation de python-docx...
    python -m pip install --quiet python-docx
)
python build_recommandations_edutrack.py
if errorlevel 1 (
    echo [ERREUR] La generation a echoue.
    pause
    exit /b 1
)
echo.
echo Fichier produit : recommandations_edutrack.docx
echo.
pause
