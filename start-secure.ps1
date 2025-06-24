# Sicheres Startup-Script für Docker
# Dieses Script sollte vor dem ersten Start ausgeführt werden

$ErrorActionPreference = "Stop"

Write-Host "=== Bitpanda Portfolio - Sicherer Docker-Start ===" -ForegroundColor Green

# 1. Umgebungsvariablen prüfen
Write-Host "1. Pruefe Umgebungsvariablen..." -ForegroundColor Yellow

if (-not $env:SECRET_KEY) {
    Write-Host "Generiere sicheren SECRET_KEY..." -ForegroundColor Yellow
    $randomBytes = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $bytes = New-Object byte[] 32
    $randomBytes.GetBytes($bytes)
    $secretKey = [Convert]::ToBase64String($bytes)
    $env:SECRET_KEY = $secretKey
    
    # .env-Datei erstellen falls nicht vorhanden
    if (-not (Test-Path ".env")) {
        Write-Output "SECRET_KEY=$secretKey" | Out-File -FilePath ".env" -Encoding UTF8
        Write-Host "SECRET_KEY wurde in .env gespeichert" -ForegroundColor Green
    }
}

# 2. Backup-Verzeichnis vorbereiten
Write-Host "2. Bereite Backup-Verzeichnis vor..." -ForegroundColor Yellow
if (-not (Test-Path "backup")) {
    New-Item -ItemType Directory -Path "backup" | Out-Null
}

# 3. Nginx-Verzeichnis prüfen
Write-Host "3. Pruefe Nginx-Konfiguration..." -ForegroundColor Yellow
if (-not (Test-Path "nginx")) {
    Write-Warning "Nginx-Verzeichnis fehlt. Bitte stellen Sie sicher, dass nginx/nginx.conf existiert."
}

# 4. Docker-Container stoppen falls sie laufen
Write-Host "4. Stoppe existierende Container..." -ForegroundColor Yellow
docker-compose down 2>&1 | Out-Null

# 4.1. Docker komplett bereinigen
Write-Host "4.1. Bereinige Docker komplett..." -ForegroundColor Yellow
docker system prune -af 2>&1 | Out-Null
docker volume prune -f 2>&1 | Out-Null

# 4.2. Lokale Images löschen
Write-Host "4.2. Loesche lokale Images..." -ForegroundColor Yellow
try {
    $images = docker images -q
    if ($images) {
        docker rmi $images -f 2>&1 | Out-Null
    }
} catch {
    # Ignoriere Fehler falls keine Images vorhanden
}

# 5. Docker-Images neu bauen
Write-Host "5. Baue Docker-Images..." -ForegroundColor Yellow
docker-compose build --no-cache

# 6. Container starten
Write-Host "6. Starte Container..." -ForegroundColor Yellow
docker-compose up -d

# 7. Warten bis Service verfügbar ist
Write-Host "7. Warte auf Service-Verfuegbarkeit..." -ForegroundColor Yellow
$maxAttempts = 30
$attempt = 0

do {
    Start-Sleep -Seconds 2
    $attempt++
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 5 -UseBasicParsing
        if ($response.StatusCode -eq 200) {
            Write-Host "Service ist verfuegbar!" -ForegroundColor Green
            break
        }
    }
    catch {
        Write-Host "." -NoNewline
    }
    
    if ($attempt -ge $maxAttempts) {
        Write-Host "`nService konnte nicht erreicht werden" -ForegroundColor Red
        Write-Host "Pruefen Sie die Logs: docker-compose logs" -ForegroundColor Yellow
        exit 1
    }
} while ($true)

Write-Host "`n=== Start erfolgreich abgeschlossen ===" -ForegroundColor Green
Write-Host "Portfolio verfuegbar unter: http://localhost" -ForegroundColor Cyan
Write-Host "Direkte App-URL: http://localhost:5000" -ForegroundColor Cyan
Write-Host "`nNuetzliche Befehle:" -ForegroundColor Yellow
Write-Host "  Logs anzeigen: docker-compose logs -f" -ForegroundColor White
Write-Host "  Container stoppen: docker-compose down" -ForegroundColor White
Write-Host "  Backups anzeigen: dir backup" -ForegroundColor White

# 8. Sicherheitshinweise
Write-Host "`n=== Sicherheitshinweise ===" -ForegroundColor Red
Write-Host "- Aendern Sie das Standard-SECRET_KEY in der .env-Datei" -ForegroundColor Yellow
Write-Host "- Verwenden Sie starke Passwoerter fuer alle Benutzerkonten" -ForegroundColor Yellow
Write-Host "- Ueberwachen Sie regelmaessig die Logs auf verdaechtige Aktivitaeten" -ForegroundColor Yellow
Write-Host "- Erstellen Sie regelmaessige Backups der Datenbank" -ForegroundColor Yellow

# 9. Debug-Informationen bei Problemen
Write-Host "`n=== Debug-Informationen ===" -ForegroundColor Cyan
Write-Host "Container-Status pruefen: docker-compose ps" -ForegroundColor White
Write-Host "Logs anzeigen: docker-compose logs bitpanda-portfolio" -ForegroundColor White
Write-Host "Health-Check testen: curl http://localhost:5000/health" -ForegroundColor White
