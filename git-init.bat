@echo off
echo Git Repository Initialisierung
echo ==============================

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo Git ist nicht installiert oder nicht im PATH verfuegbar
    echo Bitte installieren Sie Git von: https://git-scm.com/download/win
    pause
    exit /b 1
)

REM Initialize git repository if not already initialized
if not exist ".git" (
    echo 📁 Git Repository initialisieren...
    git init
    echo ✅ Git Repository initialisiert!
) else (
    echo ✅ Git Repository bereits vorhanden
)

REM Create .gitignore if not exists (should already exist)
if not exist ".gitignore" (
    echo 📝 .gitignore erstellen...
    echo # Environment files > .gitignore
    echo .env >> .gitignore
    echo node_modules/ >> .gitignore
    echo __pycache__/ >> .gitignore
)

REM Add all files to git
echo 📦 Dateien zu Git hinzufügen...
git add .

REM Check git status
echo 📊 Git Status:
git status --short

REM Create initial commit
echo 📝 Ersten Commit erstellen...
git commit -m "Initial commit: Bitpanda Portfolio Viewer webapp"

echo.
echo ✅ Git Repository ist bereit!
echo.
echo 🚀 Nächste Schritte:
echo    1. Erstellen Sie ein Repository auf GitHub/GitLab
echo    2. Fügen Sie das Remote-Repository hinzu:
echo       git remote add origin https://github.com/username/bitpanda-portfolio-viewer.git
echo    3. Pushen Sie den Code:
echo       git push -u origin main
echo.
pause
