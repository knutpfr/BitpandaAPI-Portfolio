# Bitpanda Portfolio Viewer

Eine Web-Anwendung zur Anzeige Ihres Bitpanda-Portfolios mit einer Flask-Backend-API und einem React-Frontend.

## Features

- 📊 Portfolio-Übersicht mit Krypto- und Fiat-Wallets
- 💰 EUR-Werte für alle Assets in Echtzeit
- 🔄 Live-Preis-Updates von Bitpanda API
- 📱 Responsive Design für Desktop und Mobile
- 🚀 Einfache Installation und Einrichtung

## Voraussetzungen

- Python 3.7 oder höher
- Node.js 14 oder höher
- npm oder yarn
- Bitpanda Pro API-Schlüssel

## Installation

### 1. Repository klonen
```bash
git clone <repository-url>
cd bitpanda-portfolio-viewer
```

### 2. API-Schlüssel konfigurieren
1. Erstellen Sie eine Kopie der `.env.example` Datei:
   
   **Unix/Linux/macOS:**
   ```bash
   cp .env.example .env
   ```
   
   **Windows:**
   ```cmd
   copy .env.example .env
   ```

2. Öffnen Sie die `.env` Datei und tragen Sie Ihren Bitpanda API-Schlüssel ein:
   ```
   API_KEY=ihr_api_schluessel_hier
   ```

### 3. Backend einrichten
```bash
# Python-Abhängigkeiten installieren
pip install -r requirements.txt
```

### 4. Frontend einrichten
```bash
# In das Frontend-Verzeichnis wechseln
cd frontend

# Node.js-Abhängigkeiten installieren
npm install
```

## Anwendung starten

### Option 1: Automatischer Start
**Windows:**
```cmd
start.bat
```

**Unix/Linux/macOS:**
```bash
./start.sh
```

### Option 2: Manueller Start

**Backend starten:**
```bash
# Flask-Server starten (Port 5000)
python backend/app.py
```

**Frontend starten (neues Terminal):**
```bash
# In das Frontend-Verzeichnis wechseln
cd frontend

# Development-Server starten (Port 5173)
npm run dev
```

### Option 3: Production Build

**Frontend für Production bauen:**
```bash
cd frontend
npm run build
```

## Zugriff auf die Anwendung

Nach dem Start können Sie auf die Anwendung zugreifen:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000

## API-Endpunkte

- `GET /api/wallets` - Alle Krypto-Wallets
- `GET /api/fiatwallets` - Alle Fiat-Wallets  
- `GET /api/ticker` - Aktuelle Preise
- `GET /api/health` - Health Check

## Bitpanda API-Schlüssel erhalten

1. Besuchen Sie [Bitpanda Pro](https://pro.bitpanda.com/api)
2. Melden Sie sich in Ihrem Bitpanda-Konto an
3. Navigieren Sie zu den API-Einstellungen
4. Erstellen Sie einen neuen API-Schlüssel
5. Kopieren Sie den Schlüssel in Ihre `.env` Datei

## Projektstruktur

```
bitpanda-portfolio-viewer/
├── backend/
│   └── app.py              # Flask API Server
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # React Hauptkomponente
│   │   ├── main.jsx        # React Entry Point
│   │   └── styles.css      # CSS Styles
│   ├── index.html          # HTML Template
│   ├── package.json        # Node.js Dependencies
│   └── vite.config.js      # Vite Configuration
├── .env.example            # Beispiel-Umgebungsvariablen
├── .gitignore              # Git Ignore-Regeln
├── requirements.txt        # Python Dependencies
├── package.json            # Projekt-Metadaten
├── install.bat             # Windows Installation
├── install.sh              # Unix Installation
├── start.bat               # Windows Start
├── start.sh                # Unix Start
├── git-init.bat            # Windows Git Initialisierung
├── git-init.sh             # Unix Git Initialisierung
└── README.md               # Diese Datei
```

## Entwicklung

### Backend Development
Das Backend ist ein Flask-Server, der die Bitpanda API aufruft und die Daten für das Frontend bereitstellt.

### Frontend Development
Das Frontend ist eine React-Anwendung, die mit Vite gebaut wurde. Es zeigt die Portfolio-Daten in einer benutzerfreundlichen Oberfläche an.

### Debugging
- Backend-Logs werden in der Konsole angezeigt
- Frontend kann über Browser-Entwicklertools debuggt werden
- API-Endpunkte können direkt getestet werden: http://localhost:5000/api/health

## Problembehandlung

### "401 Unauthorized" Fehler
- Überprüfen Sie, ob Ihr API-Schlüssel korrekt in der `.env` Datei eingetragen ist
- Stellen Sie sicher, dass der API-Schlüssel gültig und aktiv ist

### "CORS" Fehler
- Das Backend ist bereits für CORS konfiguriert
- Bei weiterhin bestehenden Problemen starten Sie beide Server neu

### "Module not found" Fehler
- Backend: `pip install -r requirements.txt`
- Frontend: `cd frontend && npm install`

## Git Repository erstellen

Für die Veröffentlichung des Projekts:

**Windows:**
```cmd
git-init.bat
```

**Unix/Linux/macOS:**
```bash
./git-init.sh
```

Dies initialisiert Git, fügt alle Dateien hinzu und erstellt den ersten Commit.

## Lizenz

Dieses Projekt dient nur zu Bildungszwecken. Bitte beachten Sie die Bitpanda API-Nutzungsbedingungen.

## Beitragen

1. Fork das Repository
2. Erstellen Sie einen Feature-Branch
3. Committen Sie Ihre Änderungen
4. Push zum Branch
5. Erstellen Sie einen Pull Request

## Support

Bei Fragen oder Problemen erstellen Sie bitte ein Issue im Repository.
