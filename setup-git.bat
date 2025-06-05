@echo off
echo Git Repository wird initialisiert...
echo

REM Git Repository initialisieren
git init

REM Alle Dateien hinzufuegen
git add .

REM Ersten Commit erstellen
git commit -m "Initial commit: Bitpanda Portfolio Viewer"

echo.
echo Git Repository erfolgreich initialisiert!
echo.
echo Naechste Schritte:
echo 1. Erstellen Sie ein Repository auf GitHub/GitLab
echo 2. git remote add origin [IHRE-REPOSITORY-URL]
echo 3. git push -u origin main
echo.
pause
