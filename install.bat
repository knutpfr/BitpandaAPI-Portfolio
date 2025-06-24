@echo off
echo =======================================================
echo  Bitpanda Portfolio - Sichere Installation
echo =======================================================

REM Prüfe Docker-Installation
docker --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Docker ist nicht installiert oder nicht verfügbar
    echo Bitte installieren Sie Docker Desktop von https://docker.com
    pause
    exit /b 1
)

REM Prüfe Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Docker Compose ist nicht verfügbar
    echo Bitte stellen Sie sicher, dass Docker Compose installiert ist
    pause
    exit /b 1
)

echo Docker erfolgreich gefunden!
echo.

REM Erstelle .env-Datei falls nicht vorhanden
if not exist ".env" (
    echo Erstelle .env-Konfiguration...
    copy ".env.template" ".env"
    echo WARNUNG: Bitte bearbeiten Sie die .env-Datei und ändern Sie SECRET_KEY!
    echo.
)

REM Erstelle Backup-Verzeichnis
if not exist "backup" (
    mkdir backup
    echo Backup-Verzeichnis erstellt
)

echo Installation abgeschlossen!
echo.
echo Nächste Schritte:
echo 1. Bearbeiten Sie die .env-Datei und ändern Sie SECRET_KEY
echo 2. Führen Sie 'start-secure.ps1' in PowerShell aus
echo 3. Oder verwenden Sie 'docker-compose up -d'
echo.
pause

echo.
echo ✅ Installation abgeschlossen!
echo.
echo 🎯 Starten Sie die Anwendung mit:
echo    start.bat
echo.
echo 🌐 Zugriff über: http://localhost:5173
pause
