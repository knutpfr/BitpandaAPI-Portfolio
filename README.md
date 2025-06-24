# 🪙 Bitpanda Portfolio Dashboard

Ein modernes, sicheres Portfolio-Dashboard für Ihre Bitpanda Kryptowährungen mit React Frontend und Flask Backend.

## ✨ Features

### 🎯 Neu in v2.1
- **🎨 React Frontend**: Modernes, responsives UI mit Dark/Light Theme
- **🚀 Demo-Modus**: Testen Sie die App ohne API-Schlüssel mit Beispieldaten
- **🎨 Konsistente UI**: Login und Dashboard teilen dasselbe moderne Design
- **👤 Benutzerverwaltung**: Benutzer-Info, Logout-Button und Demo-Badge
- **📊 Erweiterte Portfolio-Ansicht**: Gesamtübersicht mit 24h-Änderungen

### 💎 Kernfunktionen
- **🔒 Sichere Authentifizierung**: Benutzerkonten mit verschlüsselten API-Schlüsseln
- **📈 Live Portfolio-Daten**: Echtzeit-Synchronisation mit Bitpanda API
- **🎨 Modernes UI**: Dark/Light Theme mit Bitpanda-ähnlichem Design
- **📱 Responsive Design**: Optimiert für Desktop und Mobile
- **🐳 Docker-Support**: Einfache Bereitstellung mit Docker
- **🔐 Security Headers**: Umfassende Sicherheitsfeatures

## 🚀 Schnellstart

### Option 1: Docker (Empfohlen)
```powershell
# Kompletter Build und Start
.\build-and-run.ps1
```

### Option 2: Development Mode
```powershell
# Für Entwicklung ohne Docker
.\dev-run.ps1
```

### Option 3: Manuell
```powershell
# 1. Frontend bauen
cd frontend
npm install
npm run build
cd ..

# 2. Backend starten
pip install -r requirements.txt
python app.py
```

## 🎮 Demo-Modus

**Neu!** Sie können die App jetzt ohne echten API-Schlüssel testen:

1. Öffnen Sie http://localhost:5000
2. Klicken Sie auf "Registrieren"
3. **Lassen Sie das API-Schlüssel-Feld leer**
4. Erstellen Sie Ihr Konto - Demo-Modus wird automatisch aktiviert
5. Entdecken Sie das Dashboard mit Beispieldaten

## 🔑 Echte Daten verwenden

Für Live-Daten von Ihrem Bitpanda-Konto:

1. **API-Schlüssel erstellen**:
   - Melden Sie sich bei [Bitpanda Pro](https://pro.bitpanda.com) an
   - Gehen Sie zu Einstellungen → API
   - Erstellen Sie einen neuen API-Schlüssel mit Read-Berechtigung

2. **Registrierung**:
   - Registrieren Sie sich mit Ihrem API-Schlüssel
   - Das Dashboard zeigt Ihre echten Portfolio-Daten

## 🎨 UI-Features

### 🖼️ Screenshot-Übersicht
- **🔐 Login**: Modernes Dark-Theme Login mit konsistenten Farben
- **📊 Dashboard**: React-basiertes Portfolio-Dashboard
- **🌓 Theme-Toggle**: Wechseln zwischen Dark/Light Mode
- **👤 User-Info**: Benutzername und Demo-Badge
- **📈 Portfolio-Karten**: Asset-Übersicht mit Preis-Änderungen

### 🎯 Design-Highlights
- **Bitpanda-Style**: Grün-Gradient (#00d4aa → #00b899)
- **Konsistente Farben**: Login und Dashboard verwenden dasselbe Schema
- **Smooth Animations**: Hover-Effekte und Übergänge
- **Responsive Layout**: Optimiert für alle Bildschirmgrößen

## 📋 Technische Details

### 🏗️ Architektur
```
├── Frontend (React + Vite)
│   ├── React 18 mit Hooks
│   ├── Axios für API-Calls
│   ├── CSS Custom Properties
│   └── Responsive Design
│
├── Backend (Flask)
│   ├── Flask-Login für Sessions
│   ├── SQLite mit Verschlüsselung
│   ├── Security Headers
│   └── Rate Limiting
│
└── Deployment
    ├── Docker Multi-Stage Build
    ├── Non-Root Container
    └── Health Checks
```

### 🔒 Sicherheitsfeatures
- **🔐 API-Schlüssel Verschlüsselung**: Fernet-Verschlüsselung für API-Keys
- **🛡️ Security Headers**: CSP, HSTS, X-Frame-Options
- **⚡ Rate Limiting**: Schutz vor Brute-Force-Angriffen
- **🔑 Session Management**: Sichere Flask-Sessions
- **🚫 SQL-Injection Schutz**: Parametrisierte Queries

## 🔧 Konfiguration

### Umgebungsvariablen
```bash
SECRET_KEY=your-secret-key-here
FLASK_ENV=production  # oder development
DATABASE_PATH=./data/portfolio.db
```

### Docker Ports
- **5000**: Web-Interface
- **Volumes**: 
  - `./data:/app/data` (Datenbank)
  - `./logs:/app/logs` (Log-Dateien)

## 🆘 Fehlerbehebung

### Häufige Probleme

#### Docker-Fehler
```powershell
# Docker Desktop starten
# Warten bis Docker bereit ist
docker --version

# Container-Status prüfen
docker ps -a
docker logs bitpanda-portfolio
```

#### Frontend Build-Fehler
```powershell
# Node.js Version prüfen (≥ 16 erforderlich)
node --version

# Dependencies neu installieren
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

#### API-Verbindungsfehler
- ✅ Überprüfen Sie Ihren Bitpanda API-Schlüssel
- ✅ Stellen Sie sicher, dass der Schlüssel Read-Berechtigung hat
- ✅ Verwenden Sie den Demo-Modus zum Testen

## 🛣️ Roadmap

### 🔮 Geplante Features
- [ ] **📊 Erweiterte Charts**: Historische Preis-Diagramme
- [ ] **💹 Portfolio-Tracking**: Gewinn/Verlust-Analyse
- [ ] **🔔 Benachrichtigungen**: Preis-Alerts und Updates
- [ ] **📱 PWA**: Progressive Web App für Mobile
- [ ] **🌍 Multi-Language**: Unterstützung für weitere Sprachen
- [ ] **🎨 Themes**: Weitere Design-Optionen

## 🤝 Beitragen

Beiträge sind willkommen! Bitte:

1. **🍴 Fork** das Repository
2. **🌿 Branch** für Ihr Feature erstellen
3. **💾 Commit** Ihre Änderungen
4. **📤 Push** zum Branch
5. **📬 Pull Request** erstellen

## 📄 Lizenz

Dieses Projekt steht unter der MIT-Lizenz. Siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagungen

- **Bitpanda**: Für die excellente API
- **React Team**: Für das fantastische Framework  
- **Flask Community**: Für das robuste Backend-Framework
- **Open Source Community**: Für die vielen genutzten Bibliotheken

---

**⭐ Hat Ihnen das Projekt gefallen? Geben Sie uns einen Stern!**

**🐛 Probleme gefunden? [Erstellen Sie ein Issue](../../issues)**

**💬 Fragen? [Starten Sie eine Diskussion](../../discussions)**
