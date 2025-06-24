# Sichere Flask-Webanwendung für Bitpanda Portfolio
import os
import secrets
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from database import SecureUserDatabase
from bitpanda_api import BitpandaAPI

# Logging-Konfiguration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class User(UserMixin):
    def __init__(self, user_id, username, api_key):
        self.id = user_id
        self.username = username
        self.api_key = api_key

# Flask-App-Konfiguration
app = Flask(__name__, static_folder='frontend/dist', static_url_path='/static')
app.secret_key = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Sicherheitsheader
@app.after_request
def add_security_headers(response):
    # Content Security Policy
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "connect-src 'self'"
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

# Proxy-Fix für Docker
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

# CORS-Konfiguration
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

# Rate Limiting - Temporär deaktiviert für Debugging
# limiter = Limiter(
#     app=app,
#     key_func=get_remote_address,
#     default_limits=["200 per day", "50 per hour"],
#     storage_uri="memory://"
# )

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Bitte melden Sie sich an, um auf diese Seite zuzugreifen.'

# Datenbank-Initialisierung
db = SecureUserDatabase()
bitpanda_api = BitpandaAPI()

@login_manager.user_loader
def load_user(user_id):
    # Versuche zuerst über user_id zu laden (Standard Flask-Login)
    try:
        user_data = db.get_user_by_id(user_id)
        if user_data:
            logger.info(f"User geladen über ID: {user_id}")
            return User(user_data['user_id'], user_data['username'], user_data['api_key'])
    except Exception as e:
        logger.error(f"Fehler beim Laden des Users über ID {user_id}: {e}")
    
    # Fallback: Versuche über Session-ID (falls vorhanden)
    session_id = session.get('session_id')
    if session_id:
        try:
            user_data = db.get_user_by_session(session_id)
            if user_data:
                logger.info(f"User geladen über Session: {session_id}")
                return User(user_data['user_id'], user_data['username'], user_data['api_key'])
        except Exception as e:
            logger.error(f"Fehler beim Laden des Users über Session {session_id}: {e}")
    
    logger.warning(f"User konnte nicht geladen werden - ID: {user_id}, Session: {session.get('session_id')}")
    return None

# Session-Bereinigung
def cleanup_sessions():
    db.cleanup_old_sessions()

# Hilfsfunktionen für Input-Validierung
def validate_username(username):
    if not username or len(username) < 3 or len(username) > 50:
        return False
    return username.isalnum() or '_' in username

def validate_password(password):
    if not password or len(password) < 8:
        return False
    # Prüfe auf Komplexität
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit

def validate_api_key(api_key):
    return api_key and len(api_key) >= 10 and api_key.replace('-', '').isalnum()

# Routen
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            username = data.get('username', '').strip()
            password = data.get('password', '')
            
            logger.info(f"Login-Versuch für Benutzer: {username}, JSON: {request.is_json}")
            
            # Input-Validierung
            if not validate_username(username):
                logger.warning(f"Ungültiger Benutzername: {username}")
                return jsonify({'error': 'Ungültiger Benutzername'}), 400
            
            # IP-Adresse und User-Agent für Sicherheit
            ip_address = request.environ.get('REMOTE_ADDR', 'unbekannt')
            user_agent = request.headers.get('User-Agent', 'Unknown')
            
            logger.info(f"Versuche Authentifizierung für: {username}")
            
            # Authentifizierung
            auth_result = db.authenticate_user(username, password, ip_address, user_agent)
            
            logger.info(f"Authentifizierung erfolgreich für: {username}, User-ID: {auth_result['user_id']}")
            
            # User-Objekt erstellen und einloggen
            user = User(auth_result['user_id'], auth_result['username'], auth_result['api_key'])
            login_result = login_user(user, remember=False, duration=timedelta(hours=24))
            
            logger.info(f"Flask-Login Result: {login_result}, Current User: {current_user.is_authenticated if current_user else 'None'}")
            
            # Session-ID in Flask-Session speichern
            session['session_id'] = auth_result['session_id']
            
            logger.info(f"Erfolgreiche Anmeldung: {username} von {ip_address}")
            
            if request.is_json:
                return jsonify({'success': True, 'redirect': url_for('dashboard')})
            else:
                flash('Erfolgreich angemeldet!', 'success')
                return redirect(url_for('dashboard'))
                
        except ValueError as e:
            logger.warning(f"Login-Fehler: {e}")
            if request.is_json:
                return jsonify({'error': str(e)}), 401
            else:
                flash(str(e), 'error')
        except Exception as e:
            logger.error(f"Unerwarteter Login-Fehler: {e}")
            if request.is_json:
                return jsonify({'error': 'Interner Serverfehler'}), 500
            else:
                flash('Interner Serverfehler', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json() if request.is_json else request.form
            username = data.get('username', '').strip()
            password = data.get('password', '')
            api_key = data.get('api_key', '').strip()
            
            # Input-Validierung
            if not validate_username(username):
                return jsonify({'error': 'Benutzername muss 3-50 Zeichen lang sein und nur Buchstaben, Zahlen und _ enthalten'}), 400
            
            if not validate_password(password):
                return jsonify({'error': 'Passwort muss mindestens 8 Zeichen lang sein und Groß-, Kleinbuchstaben und Zahlen enthalten'}), 400
              # API-Key Validierung - Leerer Key für Demo-Modus erlaubt
            if api_key and not validate_api_key(api_key):
                return jsonify({'error': 'Ungültiger API-Schlüssel'}), 400
            
            # Demo-Modus wenn kein API-Key angegeben
            is_demo = not api_key
            if is_demo:
                api_key = 'DEMO_MODE'  # Platzhalter für Demo-Modus
              # Benutzer erstellen
            db.create_user(username, password, api_key)
            
            logger.info(f"Neuer Benutzer registriert: {username}, Demo-Modus: {is_demo}")
            
            if request.is_json:
                return jsonify({'success': True, 'message': f'Benutzer erfolgreich erstellt! {"Demo-Modus aktiviert." if is_demo else ""}'})
            else:
                flash(f'Benutzer erfolgreich erstellt! Sie können sich jetzt anmelden. {"Demo-Modus aktiviert." if is_demo else ""}', 'success')
                return redirect(url_for('login'))
                
        except ValueError as e:
            logger.warning(f"Registrierungsfehler: {e}")
            if request.is_json:
                return jsonify({'error': str(e)}), 400
            else:
                flash(str(e), 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # React Frontend servieren
    try:
        with open('frontend/dist/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except FileNotFoundError:
        # Fallback auf Development-Version
        return redirect('/static/index.html')

# Statische Assets für React App
@app.route('/assets/<path:filename>')
def react_assets(filename):
    return app.send_static_file(f'assets/{filename}')

# API Route für Benutzer-Info (für React Frontend)
@app.route('/api/user')
@login_required
def get_user_info():
    is_demo = current_user.api_key == 'DEMO_MODE'
    return jsonify({
        'username': current_user.username,
        'is_demo': is_demo,
        'user_id': current_user.id
    })

@app.route('/api/portfolio')
@login_required
def get_portfolio():
    try:        # Demo-Modus Daten mit Random-Werten
        if current_user.api_key == 'DEMO_MODE':
            import random
            
            # Zufällige Crypto-Preise generieren (basierend auf realistischen Bereichen)
            btc_price = random.uniform(25000, 35000)
            eth_price = random.uniform(1400, 1800)
            ada_price = random.uniform(0.80, 1.20)
            sol_price = random.uniform(45, 75)
            
            # Zufällige Mengen
            btc_amount = random.uniform(0.1, 0.5)
            eth_amount = random.uniform(1.5, 3.0)
            ada_amount = random.uniform(800, 1500)
            sol_amount = random.uniform(10, 25)
            
            # Werte berechnen
            btc_value = btc_price * btc_amount
            eth_value = eth_price * eth_amount
            ada_value = ada_price * ada_amount
            sol_value = sol_price * sol_amount
            
            # Zufällige 24h Änderungen (-10% bis +15%)
            btc_change_pct = random.uniform(-10, 15)
            eth_change_pct = random.uniform(-10, 15)
            ada_change_pct = random.uniform(-10, 15)
            sol_change_pct = random.uniform(-10, 15)
            
            # Absolute Änderungen berechnen
            btc_change = btc_value * (btc_change_pct / 100)
            eth_change = eth_value * (eth_change_pct / 100)
            ada_change = ada_value * (ada_change_pct / 100)
            sol_change = sol_value * (sol_change_pct / 100)
            
            # Fiat-Wallets mit zufälligen Werten
            eur_balance = random.uniform(500, 3000)
            usd_balance = random.uniform(1000, 4000)
            
            # Gesamtwerte berechnen
            crypto_total = btc_value + eth_value + ada_value + sol_value
            fiat_total_eur = eur_balance + (usd_balance * 0.85)  # USD zu EUR
            total_value = crypto_total + fiat_total_eur
            total_change = btc_change + eth_change + ada_change + sol_change
            total_change_pct = (total_change / total_value) * 100 if total_value > 0 else 0
            
            demo_portfolio = {
                'total_value': round(total_value, 2),
                'total_change_24h': round(total_change, 2),
                'total_change_24h_percentage': round(total_change_pct, 2),
                'crypto_total_value': round(crypto_total, 2),
                'fiat_total_value': round(fiat_total_eur, 2),
                'assets': [
                    {
                        'name': 'Bitcoin',
                        'symbol': 'BTC',
                        'amount': round(btc_amount, 4),
                        'current_price': round(btc_price, 2),
                        'value': round(btc_value, 2),
                        'change_24h': round(btc_change, 2),
                        'change_24h_percentage': round(btc_change_pct, 2),
                        'logo_url': '/static/crypto-logos/btc.png'
                    },
                    {
                        'name': 'Ethereum',
                        'symbol': 'ETH', 
                        'amount': round(eth_amount, 4),
                        'current_price': round(eth_price, 2),
                        'value': round(eth_value, 2),
                        'change_24h': round(eth_change, 2),
                        'change_24h_percentage': round(eth_change_pct, 2),
                        'logo_url': '/static/crypto-logos/eth.png'
                    },
                    {
                        'name': 'Cardano',
                        'symbol': 'ADA',
                        'amount': round(ada_amount, 2),
                        'current_price': round(ada_price, 4),
                        'value': round(ada_value, 2),
                        'change_24h': round(ada_change, 2),
                        'change_24h_percentage': round(ada_change_pct, 2),
                        'logo_url': '/static/crypto-logos/ada.png'
                    },
                    {
                        'name': 'Solana',
                        'symbol': 'SOL',
                        'amount': round(sol_amount, 4),
                        'current_price': round(sol_price, 2),
                        'value': round(sol_value, 2),
                        'change_24h': round(sol_change, 2),
                        'change_24h_percentage': round(sol_change_pct, 2),
                        'logo_url': '/static/crypto-logos/sol.png'
                    }
                ],
                'fiat_wallets': [
                    {
                        'symbol': 'EUR',
                        'balance': round(eur_balance, 2),
                        'name': 'Euro'
                    },
                    {
                        'symbol': 'USD', 
                        'balance': round(usd_balance, 2),
                        'name': 'US-Dollar'
                    }
                ],
                'last_update': datetime.now().isoformat(),
                'is_demo': True
            }
            return jsonify(demo_portfolio)
        
        # Echte API-Daten
        portfolio_data = bitpanda_api.get_portfolio(current_user.api_key)
        portfolio_data['is_demo'] = False
        return jsonify(portfolio_data)
    except Exception as e:
        logger.error(f"Portfolio-Abruf-Fehler für {current_user.username}: {e}")
        return jsonify({'error': 'Fehler beim Abrufen des Portfolios'}), 500

@app.route('/api/users')
@login_required
def list_users():
    try:
        users = db.list_users()
        return jsonify(users)
    except Exception as e:
        logger.error(f"Benutzer-Liste-Fehler: {e}")
        return jsonify({'error': 'Fehler beim Abrufen der Benutzerliste'}), 500

@app.route('/api/users/<username>', methods=['DELETE'])
@login_required
def delete_user(username):
    try:
        # Verhindere Selbstlöschung
        if username == current_user.username:
            return jsonify({'error': 'Sie können sich nicht selbst löschen'}), 400
        
        success = db.delete_user(username)
        if success:
            logger.info(f"Benutzer gelöscht: {username} (durch {current_user.username})")
            return jsonify({'success': True, 'message': f'Benutzer {username} wurde gelöscht'})
        else:
            return jsonify({'error': 'Benutzer nicht gefunden'}), 404
            
    except Exception as e:
        logger.error(f"Benutzer-Lösch-Fehler: {e}")
        return jsonify({'error': 'Fehler beim Löschen des Benutzers'}), 500

@app.route('/logout')
@login_required
def logout():
    session_id = session.get('session_id')
    if session_id:
        db.logout_user(session_id)
    
    logout_user()
    session.clear()
    flash('Sie wurden erfolgreich abgemeldet.', 'info')
    return redirect(url_for('login'))

@app.route('/switch_user')
@login_required
def switch_user():
    # Aktuellen Benutzer abmelden
    session_id = session.get('session_id')
    if session_id:
        db.logout_user(session_id)
    
    logout_user()
    session.clear()
    return redirect(url_for('login'))

@app.route('/health')
def health_check():
    """Health Check für Container-Monitoring"""
    try:
        # Einfache Datenbankverbindung testen
        with db.get_db_connection() as conn:
            conn.execute('SELECT 1').fetchone()
        return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503

@app.route('/api/health')
def api_health_check():
    """API Health Check für Load Balancer"""
    return health_check()

# Security Headers Middleware
@app.before_request
def security_headers():
    # Protokolliere verdächtige Anfragen
    user_agent = request.headers.get('User-Agent', '')
    if any(suspicious in user_agent.lower() for suspicious in ['sqlmap', 'nikto', 'nmap', 'burp']):
        logger.warning(f"Verdächtige Anfrage von {request.environ.get('REMOTE_ADDR', 'unbekannt')}: {user_agent}")
        return jsonify({'error': 'Forbidden'}), 403
    
    # Blockiere bekannte schädliche Pfade
    suspicious_paths = ['/wp-admin', '/admin.php', '/phpmyadmin', '/.env', '/config.php']
    if request.path in suspicious_paths:
        logger.warning(f"Blockierter Pfad-Zugriff von {request.environ.get('REMOTE_ADDR', 'unbekannt')}: {request.path}")
        return jsonify({'error': 'Not Found'}), 404

# Session-Bereinigung bei Start und regelmäßig
from threading import Timer

def periodic_cleanup():
    """Regelmäßige Bereinigung alter Sessions und Login-Versuche"""
    try:
        cleanup_sessions()
        
        # Alte Login-Versuche löschen (älter als 24 Stunden)
        with db.get_db_connection() as conn:
            cutoff_time = (datetime.now() - timedelta(hours=24)).isoformat()
            conn.execute('DELETE FROM login_attempts WHERE timestamp < ?', (cutoff_time,))
            conn.commit()
        
        logger.info("Regelmäßige Bereinigung abgeschlossen")
    except Exception as e:
        logger.error(f"Fehler bei regelmäßiger Bereinigung: {e}")
    
    # Nächste Bereinigung in 1 Stunde planen
    Timer(3600.0, periodic_cleanup).start()

# Fehlerbehandlung
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error_code=404, error_message='Seite nicht gefunden'), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Interner Server-Fehler: {error}")
    return render_template('error.html', error_code=500, error_message='Interner Server-Fehler'), 500

@app.errorhandler(429)
def ratelimit_handler(error):
    return render_template('error.html', error_code=429, error_message='Zu viele Anfragen. Bitte warten Sie.'), 429

if __name__ == '__main__':
    # Session-Bereinigung bei Start
    cleanup_sessions()
    
    # Starte regelmäßige Bereinigung
    periodic_cleanup()
    
    # Produktionsserver - WICHTIG: host='0.0.0.0' für Docker
    logger.info("Starte Bitpanda Portfolio auf 0.0.0.0:5000...")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
