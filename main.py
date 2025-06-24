# Legacy-Interface für Bitpanda Portfolio (CLI-Modus)
# Für die neue Webanwendung verwenden Sie: python app.py oder docker-compose up

import os
import sys
from database import SecureUserDatabase
from bitpanda_api import BitpandaAPI

def main():
    print("🔗 Bitpanda Portfolio - Legacy CLI")
    print("=" * 50)
    print("HINWEIS: Dieses CLI-Interface ist veraltet.")
    print("Verwenden Sie die neue sichere Webanwendung:")
    print("  1. docker-compose up")
    print("  2. Browser öffnen: http://localhost")
    print("=" * 50)
    
    choice = input("\nMöchten Sie trotzdem das CLI verwenden? (j/n): ").lower()
    if choice != 'j':
        print("Starten Sie die Webanwendung mit: docker-compose up")
        return
    
    # Einfaches CLI für Debug-Zwecke
    db = SecureUserDatabase()
    api = BitpandaAPI()
    
    while True:
        print("\n📋 Verfügbare Aktionen:")
        print("1. Benutzer erstellen")
        print("2. Benutzer auflisten")
        print("3. Portfolio anzeigen (erfordert Anmeldung)")
        print("4. Beenden")
        
        choice = input("\nWählen Sie eine Aktion (1-4): ").strip()
        
        if choice == '1':
            create_user_cli(db)
        elif choice == '2':
            list_users_cli(db)
        elif choice == '3':
            show_portfolio_cli(db, api)
        elif choice == '4':
            print("👋 Auf Wiedersehen!")
            break
        else:
            print("❌ Ungültige Auswahl!")

def create_user_cli(db):
    print("\n👤 Neuen Benutzer erstellen")
    try:
        username = input("Benutzername: ").strip()
        password = input("Passwort: ").strip()
        api_key = input("Bitpanda API-Schlüssel: ").strip()
        
        db.create_user(username, password, api_key)
        print(f"✅ Benutzer '{username}' erfolgreich erstellt!")
        
    except Exception as e:
        print(f"❌ Fehler: {e}")

def list_users_cli(db):
    print("\n👥 Registrierte Benutzer:")
    try:
        users = db.list_users()
        if not users:
            print("Keine Benutzer gefunden.")
        else:
            for user in users:
                print(f"  - {user['username']} (erstellt: {user['created_at']})")
    except Exception as e:
        print(f"❌ Fehler: {e}")

def show_portfolio_cli(db, api):
    print("\n🔐 Anmeldung erforderlich")
    try:
        username = input("Benutzername: ").strip()
        password = input("Passwort: ").strip()
        
        # Vereinfachte Authentifizierung für CLI
        auth_result = db.authenticate_user(username, password, "127.0.0.1", "CLI")
        
        print(f"\n📊 Portfolio für {username}:")
        portfolio = api.get_portfolio(auth_result['api_key'])
        
        print(f"💰 Gesamtwert: {portfolio['total_value_eur']:.2f} EUR")
        
        if portfolio['crypto_wallets']:
            print("\n₿ Krypto-Wallets:")
            for wallet in portfolio['crypto_wallets']:
                print(f"  {wallet['symbol']}: {wallet['balance']:.8f} ({wallet['value_eur']:.2f} EUR)")
        
        if portfolio['fiat_wallets']:
            print("\n💵 Fiat-Wallets:")
            for wallet in portfolio['fiat_wallets']:
                print(f"  {wallet['symbol']}: {wallet['balance']:.2f}")
        
        # Session wieder abmelden
        db.logout_user(auth_result['session_id'])
        
    except Exception as e:
        print(f"❌ Fehler: {e}")

if __name__ == "__main__":
    main()