@echo off
echo 🚀 Bitpanda Portfolio Viewer Installation
echo =========================================

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file nicht gefunden!
    echo 📝 Erstelle .env aus .env.example...
    
    if exist ".env.example" (
        copy ".env.example" ".env" >nul
        echo ✅ .env Datei erstellt!        echo 📋 Bitte tragen Sie Ihren Bitpanda API-Schlüssel in die .env Datei ein:
        echo    API_KEY=ihr_api_schluessel_hier
        echo.
    ) else (
        echo ❌ .env.example nicht gefunden!
        pause
        exit /b 1
    )
)

REM Install Python dependencies
echo 📦 Python-Abhängigkeiten installieren...
pip install -r requirements.txt

REM Install Node.js dependencies
echo 📦 Frontend-Abhängigkeiten installieren...
cd frontend
npm install
cd ..

echo.
echo ✅ Installation abgeschlossen!
echo.
echo 🎯 Starten Sie die Anwendung mit:
echo    start.bat
echo.
echo 🌐 Zugriff über: http://localhost:5173
pause
