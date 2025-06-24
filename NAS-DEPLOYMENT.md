# Bitpanda Portfolio Viewer - NAS Deployment

## 🚀 Installation auf dem NAS

### Voraussetzungen
- Docker und Docker Compose auf dem NAS installiert
- Bitpanda API-Key

### 📦 Deployment-Optionen

#### Option 1: Image-Datei verwenden (Empfohlen)

1. **Image-Datei übertragen**
   ```bash
   # Auf dem NAS das Image laden
   docker load -i bitpanda-portfolio-production.tar
   ```

2. **.env Datei erstellen**
   ```bash
   echo "API_KEY=IHR_BITPANDA_API_KEY_HIER" > .env
   ```

3. **Mit Docker Compose starten**
   ```bash
   docker-compose up -d
   ```

#### Option 2: Image direkt bauen (falls gewünscht)

1. **Repository klonen/übertragen**
   ```bash
   git clone <repository-url>
   # oder Dateien manuell übertragen
   ```

2. **Image bauen**
   ```bash
   docker build -t bitpanda-portfolio:production .
   ```

3. **Starten**
   ```bash
   docker-compose up -d
   ```

### 🔧 Konfiguration

#### Umgebungsvariablen (.env)
```env
API_KEY=your_bitpanda_api_key_here
```

#### Port-Konfiguration
- Standard: Port 5000
- Änderung in `docker-compose.yml` unter `ports: - "GEWÜNSCHTER_PORT:5000"`

### 📋 Management-Befehle

```bash
# Container starten
docker-compose up -d

# Container stoppen
docker-compose down

# Logs anzeigen
docker-compose logs -f

# Container neu starten
docker-compose restart

# Status prüfen
docker-compose ps

# Healthcheck prüfen
docker exec bitpanda-portfolio curl -f http://localhost:5000/api/health
```

### 🌐 Zugriff

Nach dem Start ist die Anwendung verfügbar unter:
- **Lokal**: `http://localhost:5000`
- **NAS-IP**: `http://IHRE_NAS_IP:5000`

### 🔒 Sicherheitsfeatures

✅ **Produktionsbereit**
- Gunicorn WSGI-Server (4 Worker)
- Non-root User (appuser)
- Healthcheck integriert
- Multi-Stage Build (kleinere Image-Größe)
- Automatischer Restart
- CORS-Schutz

### 📊 Monitoring

#### Healthcheck-Endpunkt
```bash
curl http://IHRE_NAS_IP:5000/api/health
```

#### System-Ressourcen überwachen
```bash
# Container-Ressourcen anzeigen
docker stats bitpanda-portfolio
```

### 🛠️ Troubleshooting

#### Container startet nicht
```bash
# Logs prüfen
docker-compose logs bitpanda-portfolio

# Container-Status prüfen
docker ps -a
```

#### API-Verbindung prüfen
```bash
# API-Test-Endpunkt
curl http://IHRE_NAS_IP:5000/api/test_auth
```

#### Demo-Modus (ohne API-Key)
Die Anwendung läuft automatisch im Demo-Modus mit Beispieldaten, wenn kein API-Key konfiguriert ist.

### 📂 Datei-Struktur auf dem NAS

```
/pfad/zu/bitpanda-portfolio/
├── docker-compose.yml
├── .env
├── bitpanda-portfolio-production.tar (optional)
└── logs/ (wird automatisch erstellt)
```

### 🔄 Updates

1. **Neue Image-Version**
   ```bash
   docker-compose down
   docker load -i neue-bitpanda-portfolio-production.tar
   docker-compose up -d
   ```

2. **Vollständiger Neustart**
   ```bash
   docker-compose down
   docker-compose pull  # falls von Registry
   docker-compose up -d
   ```

### 💡 Performance-Tipps

- **CPU**: Mindestens 1 Core empfohlen
- **RAM**: Mindestens 512MB verfügbar
- **Storage**: ~200MB für Image + Logs
- **Netzwerk**: Stabile Internetverbindung für API-Calls

### 🚨 Wichtige Hinweise

- **API-Key sicher aufbewahren** - Niemals in Logs oder öffentlichen Bereichen speichern
- **Firewall konfigurieren** - Nur notwendige Ports öffnen
- **Regelmäßige Backups** - .env Datei und Konfiguration sichern
- **Logs überwachen** - Regelmäßig auf Fehler prüfen

### 📞 Support

Bei Problemen:
1. Logs prüfen: `docker-compose logs`
2. Healthcheck testen: `/api/health`
3. Demo-Modus testen (ohne API-Key)
