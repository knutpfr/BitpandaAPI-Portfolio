import os
import requests
from dotenv import load_dotenv

# Laden der Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Abrufen des API-Schlüssels
API_KEY = os.getenv("API_KEY")

# Überprüfen, ob der API-Schlüssel geladen wurde
if API_KEY:
    print("API-Schlüssel erfolgreich geladen!")
    
    # Bitpanda API-Basis-URL
    BASE_URL = "https://api.bitpanda.com/v1"
    
    # Header für die API-Anfragen mit dem API-Schlüssel
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    def get_portfolio():
        """
        Ruft die Portfolio-Informationen des Benutzers ab
        """
        try:
            # Verschiedene Endpunkte für das Portfolio
            endpoints = {
                "asset_wallets": "/wallets",
                "fiat_wallets": "/fiatwallets",
                "ticker": "/ticker"  # Füge Ticker für Preisdaten hinzu
            }
            portfolio_data = {}
            
            # Für jeden Endpunkt eine Anfrage senden
            for key, endpoint in endpoints.items():
                print(f"Abfrage von {key} mit Endpunkt {endpoint}...")
                response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
                if response.status_code == 200:
                    portfolio_data[key] = response.json()
                    print(f"Erfolgreich abgerufen: {key}")
                else:
                    print(f"Fehler beim Abrufen von {key}: {response.status_code}")
                    print(response.text)
            
            # Informationen ausgeben
            print("\n\n==== Bitpanda Portfolio Übersicht ====")
            
            # Krypto-Wallets
            if 'asset_wallets' in portfolio_data and 'data' in portfolio_data['asset_wallets']:
                print("\nKrypto-Wallets:")
                wallets_found = False
                total_eur = 0.0
                
                # Ticker-Daten für EUR-Preise abrufen (falls verfügbar)
                ticker_data = {}
                if 'ticker' in portfolio_data:
                    print("\nAktualisiere Preisdaten...\n")
                    for crypto, prices in portfolio_data['ticker'].items():
                        if 'EUR' in prices:
                            ticker_data[crypto] = float(prices['EUR'])
                
                for wallet in portfolio_data['asset_wallets']['data']:
                    balance = float(wallet.get('attributes', {}).get('balance', 0))
                    if balance > 0:
                        symbol = wallet.get('attributes', {}).get('cryptocoin_symbol', 'Unbekannt')
                        
                        # EUR-Wert aus Ticker-Daten berechnen
                        price_eur = ticker_data.get(symbol, 0)
                        balance_eur = balance * price_eur
                        
                        # Gesamtwert in EUR aktualisieren
                        total_eur += balance_eur
                        
                        print(f"  {symbol}: {balance} ({balance_eur:.2f} EUR)")
                        wallets_found = True
                
                if wallets_found:
                    print(f"\n  Gesamtwert aller Krypto-Wallets: {total_eur:.2f} EUR")
                else:
                    print("  Keine Krypto-Wallets mit Guthaben gefunden.")
            
            # Fiat-Wallets
            if 'fiat_wallets' in portfolio_data and 'data' in portfolio_data['fiat_wallets']:
                print("\nFiat-Wallets:")
                wallets_found = False
                for wallet in portfolio_data['fiat_wallets']['data']:
                    if float(wallet.get('attributes', {}).get('balance', 0)) > 0:
                        print(f"  {wallet.get('attributes', {}).get('fiat_symbol', 'Unbekannt')}: {wallet.get('attributes', {}).get('balance', '0')} {wallet.get('attributes', {}).get('fiat_symbol', 'Unbekannt')}")
                        wallets_found = True
                if not wallets_found:
                    print("  Keine Fiat-Wallets mit Guthaben gefunden.")
            
            return portfolio_data
        except Exception as e:
            print(f"Fehler beim Abrufen des Portfolios: {e}")
            return None
    
    # Portfolio abrufen
    portfolio = get_portfolio()
    
else:
    print("Fehler: API-Schlüssel konnte nicht geladen werden. Bitte überprüfen Sie Ihre .env-Datei.")
