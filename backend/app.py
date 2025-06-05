import os
import sys
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler()])
logger = logging.getLogger(__name__)

# Aktuelles Arbeitsverzeichnis ausgeben
logger.info(f"Arbeitsverzeichnis: {os.getcwd()}")

# Flask-App initialisieren
app = Flask(__name__)
CORS(app)  # CORS aktivieren, damit Frontend auf Backend zugreifen kann

# Pfad zur .env-Datei angeben (absoluten Pfad verwenden)
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
logger.info(f".env Pfad: {dotenv_path}")

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv(dotenv_path=dotenv_path)

# Abrufen des API-Schlüssels
API_KEY = os.getenv("API_KEY")

# API-Schlüssel prüfen (ohne ihn zu loggen)
if API_KEY:
    logger.info("API-Schlüssel wurde gefunden")
    api_key_masked = API_KEY[:4] + '*' * (len(API_KEY) - 8) + API_KEY[-4:] if len(API_KEY) > 8 else '****'
    logger.info(f"API-Schlüssel (maskiert): {api_key_masked}")
else:
    logger.error("API-Schlüssel wurde NICHT gefunden!")

# Bitpanda API-Basis-URL
BASE_URL = "https://api.bitpanda.com/v1"

# Header für die API-Anfragen mit dem API-Schlüssel
headers = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

def get_portfolio_data():
    """
    Ruft die Portfolio-Informationen des Benutzers ab
    """
    try:
        # Verschiedene Endpunkte für das Portfolio
        endpoints = {
            "asset_wallets": "/wallets",
            "fiat_wallets": "/fiatwallets",
            "ticker": "/ticker"
        }
        portfolio_data = {}
        
        # API-Schlüssel nochmals prüfen
        if not API_KEY:
            logger.error("API-Schlüssel ist nicht verfügbar!")
            return {"error": "API-Schlüssel nicht konfiguriert"}
            
        # Verwendete Header ausgeben (ohne den API-Schlüssel selbst zu loggen)
        logger.info(f"Header-Keys: {list(headers.keys())}")
        
        # Für jeden Endpunkt eine Anfrage senden
        for key, endpoint in endpoints.items():
            logger.info(f"Sende Anfrage an {BASE_URL}{endpoint}")
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            if response.status_code == 200:
                portfolio_data[key] = response.json()
                logger.info(f"Erfolgreich abgerufen: {key}")
            else:
                logger.error(f"Fehler beim Abrufen von {key}: Status {response.status_code}")
                logger.error(f"Antwort: {response.text[:500]}")  # Begrenzt auf 500 Zeichen, um Logs nicht zu überfüllen
                portfolio_data[key] = {"error": f"Status code: {response.status_code}", "message": response.text}
        
        return portfolio_data
    except Exception as e:
        print(f"Fehler beim Abrufen des Portfolios: {e}")
        return {"error": str(e)}

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """API-Endpunkt, der Portfolio-Daten zurückgibt"""
    if not API_KEY:
        logger.error("API_KEY nicht vorhanden!")
        return jsonify({"error": "API-Schlüssel konnte nicht geladen werden"}), 500
    
    logger.info("Portfolio-Daten werden abgerufen...")
    
    try:
        # Code aus der main.py übernehmen, die nachweislich funktioniert
        endpoints = {
            "asset_wallets": "/wallets",
            "fiat_wallets": "/fiatwallets",
            "ticker": "/ticker"
        }
        portfolio_data = {}
        
        # Für jeden Endpunkt eine Anfrage senden
        for key, endpoint in endpoints.items():
            logger.info(f"Abfrage von {key} mit Endpunkt {endpoint}...")
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            if response.status_code == 200:
                portfolio_data[key] = response.json()
                logger.info(f"Erfolgreich abgerufen: {key}")
            else:
                error_msg = f"Fehler beim Abrufen von {key}: {response.status_code}"
                logger.error(error_msg)
                return jsonify({"error": error_msg, "details": response.text[:500]}), 500
        
        # Datenstruktur für die Antwort vorbereiten
        result = {
            "crypto_wallets": [],
            "fiat_wallets": [],
            "total_value_eur": 0.0
        }
        
        # Ticker-Daten für EUR-Preise abrufen
        ticker_data = {}
        if 'ticker' in portfolio_data:
            logger.info("Ticker-Daten verarbeiten...")
            for crypto, prices in portfolio_data.get('ticker', {}).items():
                if 'EUR' in prices:
                    ticker_data[crypto] = float(prices['EUR'])
        
        # Krypto-Wallets
        total_eur = 0.0
        if 'asset_wallets' in portfolio_data and 'data' in portfolio_data['asset_wallets']:
            logger.info(f"Asset Wallets verarbeiten: {len(portfolio_data['asset_wallets']['data'])} gefunden")
            for wallet in portfolio_data['asset_wallets']['data']:
                balance = float(wallet.get('attributes', {}).get('balance', 0))
                if balance > 0:
                    symbol = wallet.get('attributes', {}).get('cryptocoin_symbol', 'Unbekannt')
                    
                    # EUR-Wert aus Ticker-Daten berechnen
                    price_eur = ticker_data.get(symbol, 0)
                    balance_eur = balance * price_eur
                    
                    # Gesamtwert in EUR aktualisieren
                    total_eur += balance_eur
                    
                    result["crypto_wallets"].append({
                        "symbol": symbol,
                        "balance": balance,
                        "balance_eur": round(balance_eur, 2),
                        "price_eur": price_eur
                    })
                    logger.info(f"Krypto Wallet hinzugefügt: {symbol} mit Balance {balance}")
        
        result["total_value_eur"] = round(total_eur, 2)
        logger.info(f"Gesamtwert aller Krypto-Wallets: {total_eur:.2f} EUR")
        
        # Fiat-Wallets
        if 'fiat_wallets' in portfolio_data and 'data' in portfolio_data['fiat_wallets']:
            logger.info(f"Fiat Wallets verarbeiten: {len(portfolio_data['fiat_wallets']['data'])} gefunden")
            for wallet in portfolio_data['fiat_wallets']['data']:
                balance = float(wallet.get('attributes', {}).get('balance', 0))
                if balance > 0:
                    symbol = wallet.get('attributes', {}).get('fiat_symbol', 'Unbekannt')
                    result["fiat_wallets"].append({
                        "symbol": symbol,
                        "balance": balance
                    })
                    logger.info(f"Fiat Wallet hinzugefügt: {symbol} mit Balance {balance}")
        
        # Letzter Check - Größe der Listen überprüfen
        logger.info(f"Endergebnis: {len(result['crypto_wallets'])} Krypto-Wallets, {len(result['fiat_wallets'])} Fiat-Wallets")
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Fehler beim Abrufen oder Verarbeiten des Portfolios: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Einfacher Health-Check Endpunkt"""
    return jsonify({"status": "ok"})

# Einfacher Endpoint zum Testen des API-Schlüssels
@app.route('/api/test_auth', methods=['GET'])
def test_auth():
    """Test-Endpunkt für API-Authentifizierung"""
    test_result = {
        "environment": {
            "api_key_exists": API_KEY is not None,
            "api_key_length": len(API_KEY) if API_KEY else 0,
            "working_dir": os.getcwd(),
            "python_version": sys.version,
        }
    }
    
    # Testen mit einem einfacheren Endpoint
    try:
        logger.info("Teste Bitpanda API mit /ticker Endpunkt")
        response = requests.get(f"{BASE_URL}/ticker", headers=headers)
        test_result["ticker_test"] = {
            "status_code": response.status_code,
            "success": response.status_code == 200,
        }
        
        if response.status_code == 200:
            test_result["ticker_test"]["content_sample"] = "Daten erfolgreich empfangen"
        else:
            test_result["ticker_test"]["error"] = response.text[:200]  # Begrenzte Fehlermeldung
            
    except Exception as e:
        logger.error(f"Fehler beim API-Test: {str(e)}")
        test_result["ticker_test"] = {"error": str(e)}
    
    return jsonify(test_result)

# Wenn diese Datei direkt ausgeführt wird
if __name__ == '__main__':
    logger.info("Server wird gestartet...")
    app.run(debug=True, host='0.0.0.0', port=5000)
