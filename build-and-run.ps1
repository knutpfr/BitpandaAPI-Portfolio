# Bitpanda Portfolio - Build und Run Skript
# Dieses Skript baut das Frontend und startet die Anwendung

Write-Host "🚀 Bitpanda Portfolio Build & Run" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green

# Überprüfe ob Docker läuft
try {
    docker --version | Out-Null
    Write-Host "✅ Docker ist verfügbar" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker ist nicht verfügbar oder läuft nicht" -ForegroundColor Red
    Write-Host "Bitte starten Sie Docker Desktop und versuchen Sie es erneut." -ForegroundColor Yellow
    exit 1
}

# Überprüfe ob Node.js installiert ist
try {
    node --version | Out-Null
    Write-Host "✅ Node.js ist verfügbar" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js ist nicht installiert" -ForegroundColor Red
    Write-Host "Bitte installieren Sie Node.js und versuchen Sie es erneut." -ForegroundColor Yellow
    exit 1
}

# Frontend bauen
Write-Host "`n📦 Frontend wird gebaut..." -ForegroundColor Cyan
Set-Location -Path "frontend"

# Dependencies installieren
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
npm install

# Build erstellen
Write-Host "🔨 Building React app..." -ForegroundColor Yellow
npm run build

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Frontend Build fehlgeschlagen" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Frontend erfolgreich gebaut" -ForegroundColor Green

# Zurück zum Hauptverzeichnis
Set-Location -Path ".."

# Docker Build und Run
Write-Host "`n🐳 Docker Image wird gebaut..." -ForegroundColor Cyan
docker build -t bitpanda-portfolio:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker Build fehlgeschlagen" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker Image erfolgreich gebaut" -ForegroundColor Green

# Stoppe eventuell laufende Container
Write-Host "`n🛑 Stoppe eventuell laufende Container..." -ForegroundColor Yellow
docker stop bitpanda-portfolio 2>$null
docker rm bitpanda-portfolio 2>$null

# Container starten
Write-Host "`n🚀 Starte Container..." -ForegroundColor Cyan
docker run -d `
    --name bitpanda-portfolio `
    -p 5000:5000 `
    -e SECRET_KEY="$(Get-Random)" `
    -v "${PWD}\data:/app/data" `
    -v "${PWD}\logs:/app/logs" `
    bitpanda-portfolio:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Container Start fehlgeschlagen" -ForegroundColor Red
    exit 1
}

# Warten bis Container bereit ist
Write-Host "`n⏳ Warte auf Container..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Status prüfen
$containerStatus = docker ps --filter "name=bitpanda-portfolio" --format "table {{.Status}}"
Write-Host "📊 Container Status: $containerStatus" -ForegroundColor Cyan

# Logs anzeigen
Write-Host "`n📋 Container Logs:" -ForegroundColor Cyan
docker logs bitpanda-portfolio --tail 20

Write-Host "`n✅ Anwendung wurde erfolgreich gestartet!" -ForegroundColor Green
Write-Host "🌐 Öffnen Sie http://localhost:5000 in Ihrem Browser" -ForegroundColor Yellow
Write-Host "`n💡 Nützliche Befehle:" -ForegroundColor Cyan
Write-Host "   - docker logs bitpanda-portfolio -f  (Live-Logs anzeigen)" -ForegroundColor White
Write-Host "   - docker stop bitpanda-portfolio     (Container stoppen)" -ForegroundColor White
Write-Host "   - docker start bitpanda-portfolio    (Container starten)" -ForegroundColor White

# Browser öffnen (optional)
$openBrowser = Read-Host "`nMöchten Sie den Browser automatisch öffnen? (y/n)"
if ($openBrowser -eq "y" -or $openBrowser -eq "Y") {
    Start-Process "http://localhost:5000"
}

Write-Host "`n🎉 Viel Spaß mit Ihrem Bitpanda Portfolio Dashboard!" -ForegroundColor Green
