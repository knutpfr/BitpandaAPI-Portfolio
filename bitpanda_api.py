# Bitpanda API-Client mit Sicherheitsfunktionen
import requests
import logging
from typing import Dict, Optional
import time

logger = logging.getLogger(__name__)

class BitpandaAPI:
    def __init__(self):
        self.base_url = "https://api.bitpanda.com/v1"
        self.session = requests.Session()
        self.session.timeout = 30  # Timeout für Anfragen
        
    def _make_request(self, endpoint: str, api_key: str, max_retries: int = 3) -> Optional[Dict]:
        """Sichere API-Anfrage mit Retry-Logik"""
        headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json",
            "User-Agent": "BitpandaPortfolio/1.0"
        }
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(
                    f"{self.base_url}{endpoint}", 
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    logger.error("Ungültiger API-Schlüssel")
                    raise ValueError("Ungültiger API-Schlüssel")
                elif response.status_code == 429:
                    # Rate Limiting von Bitpanda
                    wait_time = 2 ** attempt  # Exponential backoff
                    logger.warning(f"Rate Limit erreicht, warte {wait_time} Sekunden...")
                    time.sleep(wait_time)
                    continue
                else:
                    logger.error(f"API-Fehler {response.status_code}: {response.text}")
                    if attempt == max_retries - 1:
                        raise Exception(f"API-Fehler: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"Netzwerk-Fehler bei Versuch {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    raise Exception("Netzwerk-Fehler bei API-Anfrage")
                time.sleep(1)
        
        return None
    
    def get_portfolio(self, api_key: str) -> Dict:
        """Ruft Portfolio-Informationen ab"""
        try:
            endpoints = {
                "asset_wallets": "/wallets",
                "fiat_wallets": "/fiatwallets",
                "ticker": "/ticker"
            }
            
            portfolio_data = {}
            
            for key, endpoint in endpoints.items():
                logger.info(f"Lade {key}...")
                data = self._make_request(endpoint, api_key)
                if data:
                    portfolio_data[key] = data
            
            # Portfolio-Daten verarbeiten
            processed_data = self._process_portfolio_data(portfolio_data)
            return processed_data
            
        except Exception as e:
            logger.error(f"Fehler beim Abrufen des Portfolios: {e}")
            raise
    
    def _process_portfolio_data(self, raw_data: Dict) -> Dict:
        """Verarbeitet und strukturiert Portfolio-Daten"""
        result = {
            "crypto_wallets": [],
            "fiat_wallets": [],
            "total_value_eur": 0.0,
            "last_updated": time.time()
        }
        
        # Ticker-Daten für Preise
        ticker_data = {}
        if 'ticker' in raw_data:
            for crypto, prices in raw_data['ticker'].items():
                if 'EUR' in prices:
                    ticker_data[crypto] = float(prices['EUR'])
        
        # Krypto-Wallets verarbeiten
        if 'asset_wallets' in raw_data and 'data' in raw_data['asset_wallets']:
            for wallet in raw_data['asset_wallets']['data']:
                try:
                    balance = float(wallet.get('attributes', {}).get('balance', 0))
                    if balance > 0:
                        symbol = wallet.get('attributes', {}).get('cryptocoin_symbol', 'UNKNOWN')
                        price_eur = ticker_data.get(symbol, 0)
                        balance_eur = balance * price_eur
                        
                        result["crypto_wallets"].append({
                            "symbol": symbol,
                            "balance": balance,
                            "price_eur": price_eur,
                            "value_eur": balance_eur
                        })
                        
                        result["total_value_eur"] += balance_eur
                except (ValueError, KeyError) as e:
                    logger.warning(f"Fehler beim Verarbeiten der Wallet-Daten: {e}")
        
        # Fiat-Wallets verarbeiten
        if 'fiat_wallets' in raw_data and 'data' in raw_data['fiat_wallets']:
            for wallet in raw_data['fiat_wallets']['data']:
                try:
                    balance = float(wallet.get('attributes', {}).get('balance', 0))
                    if balance > 0:
                        symbol = wallet.get('attributes', {}).get('fiat_symbol', 'UNKNOWN')
                        
                        result["fiat_wallets"].append({
                            "symbol": symbol,
                            "balance": balance
                        })
                        
                        # EUR zu Gesamtwert hinzufügen
                        if symbol == 'EUR':
                            result["total_value_eur"] += balance
                except (ValueError, KeyError) as e:
                    logger.warning(f"Fehler beim Verarbeiten der Fiat-Wallet-Daten: {e}")
        
        return result
