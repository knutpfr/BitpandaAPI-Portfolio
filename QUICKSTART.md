# 🚀 Bitpanda Portfolio - Schnellstart-Anleitung

## 📋 Was wurde implementiert?

Ich habe Ihr Bitpanda Portfolio-Projekt zu einer **sicheren, mehrbenutzerfähigen Webanwendung** umgebaut:

### ✅ Kernfunktionen
- **Multi-User-System**: Mehrere Benutzer mit eigenen API-Schlüsseln
- **Sichere Authentifizierung**: Login/Logout mit Passwort-Hashing
- **Benutzerverwaltung**: Erstellen, Löschen, zwischen Benutzern wechseln
- **Portfolio-Dashboard**: Übersichtliche Darstellung aller Wallets

### 🔐 Sicherheitsfeatures
- **Verschlüsselung**: API-Schlüssel werden verschlüsselt gespeichert
- **Rate Limiting**: Schutz vor Brute-Force-Angriffen
- **Session-Management**: Sichere 24h-Sessions
- **Docker-Security**: Non-root Container, minimale Berechtigungen
- **Nginx-Proxy**: Zusätzliche Sicherheitsebene
- **Automatische Backups**: Tägliche Datenbank-Sicherungen

## 🎯 Sofort loslegen

### 1. Installation
```bash
# Repository-Verzeichnis öffnen
cd BitpandaAPI-Portfolio

# Windows: Schnell-Installation
install.bat

# Oder manuell mit Docker prüfen:
docker --version
docker-compose --version
```

### 2. Sicherer Start
```powershell
# PowerShell als Administrator
.\start-secure.ps1
```

**Oder manuell:**
```bash
# .env-Datei erstellen
cp .env.template .env

# SECRET_KEY ändern (wichtig!)
# Editor öffnen und zufälligen String einsetzen

# Container starten
docker-compose up -d
```

### 3. Erste Anmeldung
1. Browser öffnen: **http://localhost**
2. **"Registrieren"** klicken
3. Zugangsdaten eingeben:
   - **Benutzername**: z.B. "admin" (3-50 Zeichen)
   - **Passwort**: Min. 8 Zeichen mit Groß-/Kleinbuchstaben + Zahlen
   - **API-Schlüssel**: Ihr Bitpanda API-Key

## 🎮 Benutzer-Management

### Im Dashboard:
- **"Benutzer wechseln"**: Zu anderem Account wechseln
- **"Benutzer verwalten"**: Liste aller User, Löschen möglich
- **"Abmelden"**: Sicherheit durch Logout

### Neue Benutzer hinzufügen:
1. **"Benutzer verwalten"** → **"Neuer Benutzer"**
2. Oder direkt: **http://localhost/register**

### Zwischen Benutzern wechseln:
1. **Aktionen...** → **"Benutzer wechseln"**
2. Neuen Login durchführen

## 📊 Portfolio-Features

### Dashboard zeigt:
- **💰 Gesamtwert** in EUR
- **₿ Krypto-Wallets** mit aktuellen Preisen
- **💵 Fiat-Wallets** (EUR, USD, etc.)
- **🔄 Auto-Refresh** alle 5 Minuten

### API-Endpoints:
- `GET /api/portfolio` - Portfolio-Daten
- `GET /api/users` - Benutzerliste
- `DELETE /api/users/{username}` - Benutzer löschen

## 🛠️ Nützliche Befehle

```bash
# Logs anzeigen
docker-compose logs -f

# Container-Status
docker-compose ps

# Container stoppen
docker-compose down

# Neustart nach Änderungen
docker-compose restart

# Komplett neu bauen
docker-compose down && docker-compose build --no-cache && docker-compose up -d
```

## 🔧 Konfiguration

### .env-Datei anpassen:
```bash
# Sicherheitsschlüssel (WICHTIG ändern!)
SECRET_KEY=hier-32-zeichen-zufälliger-string

# Rate Limiting anpassen
LOGIN_RATE_LIMIT=5
API_RATE_LIMIT=30

# Session-Timeout (Stunden)
SESSION_TIMEOUT=24
```

## 🌐 Externen Zugriff einrichten

### Router-Konfiguration:
1. **Port-Forwarding**: Port 80 → Ihre lokale IP
2. **DynDNS**: Für dynamische IP-Adressen
3. **SSL**: Let's Encrypt Zertifikat empfohlen

### Nginx SSL aktivieren:
```bash
# SSL-Zertifikate in nginx/ssl/ ablegen
# nginx.conf HTTPS-Sektion einkommentieren
docker-compose restart nginx-proxy
```

## 🆘 Problemlösung

### Container startet nicht:
```bash
# Logs prüfen
docker-compose logs

# Ports prüfen
netstat -an | findstr :5000

# Container neu bauen
docker-compose build --no-cache
```

### Login funktioniert nicht:
1. **Rate Limiting**: 5min warten nach vielen Versuchen
2. **Passwort**: Groß-/Kleinbuchstaben + Zahlen erforderlich
3. **Container-Logs**: `docker-compose logs bitpanda-portfolio`

### Portfolio lädt nicht:
1. **API-Schlüssel prüfen**: In Benutzer-Einstellungen
2. **Bitpanda-API-Status**: https://status.bitpanda.com
3. **Netzwerk**: Internet-Verbindung zum Container

## 📁 Datei-Struktur

```
BitpandaAPI-Portfolio/
├── app.py              # Haupt-Flask-Anwendung
├── database.py         # Sichere Datenbank-Klasse
├── bitpanda_api.py     # API-Client
├── main.py             # Legacy CLI (optional)
├── docker-compose.yml  # Container-Orchestrierung
├── dockerfile          # Sicherer Container-Build
├── requirements.txt    # Python-Dependencies
├── .env.template       # Konfigurationsvorlage
├── SECURITY.md         # Detaillierte Sicherheitsdoku
├── templates/          # HTML-Templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── base.html
├── nginx/              # Reverse Proxy
│   └── nginx.conf
└── backup/             # Automatische DB-Backups
```

## 🎯 Nächste Schritte

1. **Testen**: Mehrere Benutzer anlegen und zwischen ihnen wechseln
2. **Backup prüfen**: `dir backup` - Automatische Backups vorhanden?
3. **SSL einrichten**: Für externen Zugriff (siehe SECURITY.md)
4. **Monitoring**: Logs regelmäßig auf Anomalien prüfen

---

## 🔥 Sofort-Demo

**Terminal öffnen:**
```bash
cd BitpandaAPI-Portfolio
.\start-secure.ps1
```

**Browser öffnen:**
- http://localhost → Registrieren → Portfolio ansehen! 🚀

**Problem?** → `docker-compose logs` für Details
