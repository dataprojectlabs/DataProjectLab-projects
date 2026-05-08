@echo off
cd /d "%~dp0"
echo ============================================
echo  Generation + publication des banners
echo ============================================
echo.

REM 1. Generer les banners
python -c "from PIL import Image" 2>nul
if errorlevel 1 (
    echo Installation de Pillow...
    python -m pip install --quiet pillow
)
python build_banners.py
if errorlevel 1 (
    echo [ERREUR] La generation a echoue.
    pause
    exit /b 1
)

REM 2. Aller a la racine du repo
cd ..

REM 3. Git add + commit + push
echo.
echo --- Git status ---
git status media\banners\
echo.

git add media\banners\

REM Verifier s'il y a quelque chose a commit
git diff --cached --quiet
if errorlevel 1 (
    set /p msg="Message de commit (Enter = defaut) : "
    if "%msg%"=="" set msg=feat(media): update notebook banners
    git commit -m "%msg%"
    git push origin main
    echo.
    echo [OK] Banners pousses sur GitHub.
) else (
    echo [INFO] Aucun changement a commit.
)

echo.
pause
