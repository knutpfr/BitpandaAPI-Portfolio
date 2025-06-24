# Bitpanda Portfolio - Development Mode
# Startet die Anwendung ohne Docker für die Entwicklung

Write-Host "🛠️  Bitpanda Portfolio - Development Mode" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Überprüfe ob Python installiert ist
try {
    python --version | Out-Null
    Write-Host "✅ Python ist verfügbar" -ForegroundColor Green
} catch {
    Write-Host "❌ Python ist nicht installiert" -ForegroundColor Red
    exit 1
}

# Python Dependencies installieren
Write-Host "`n📦 Python Dependencies werden installiert..." -ForegroundColor Cyan
pip install -r requirements.txt

# Frontend bauen (falls noch nicht geschehen)
if (-not (Test-Path "frontend/dist")) {
    Write-Host "`n📦 Frontend wird gebaut..." -ForegroundColor Cyan
    Set-Location -Path "frontend"
    npm install
    npm run build
    Set-Location -Path ".."
    Write-Host "✅ Frontend erfolgreich gebaut" -ForegroundColor Green
}

# Umgebungsvariablen setzen
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
$env:SECRET_KEY = "dev-secret-key-change-in-production"

Write-Host "`n🚀 Starte Flask-Anwendung..." -ForegroundColor Cyan
Write-Host "🌐 Die Anwendung läuft auf http://localhost:5000" -ForegroundColor Yellow
Write-Host "⏹️  Drücken Sie Ctrl+C zum Beenden" -ForegroundColor Yellow
Write-Host ""

# Flask-App starten
python app.py
