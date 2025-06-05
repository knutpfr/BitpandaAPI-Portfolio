@echo off
echo Starte Bitpanda Portfolio Webapp...

echo.
echo === Backend starten ===
echo.

REM Virtuelle Umgebung aktivieren, falls vorhanden
if exist .venv\Scripts\activate (
    call .venv\Scripts\activate
)

REM Backend in einem neuen Fenster starten
start cmd /k "cd backend && python app.py"

echo.
echo === Frontend starten ===
echo.

REM In das Frontend-Verzeichnis wechseln und starten
cd frontend
start cmd /k "npm install && npm start"

echo.
echo Wenn alles korrekt gestartet wurde, öffnen Sie http://localhost:3000 in Ihrem Browser.
echo.
