# Sichere Datenbank-Verwaltung
import sqlite3
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash
from contextlib import contextmanager

# Logging-Konfiguration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('security.log'),
        logging.StreamHandler()
    ]
)

class SecureUserDatabase:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.encryption_key = self._get_or_create_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        self._init_database()
        
    def _get_or_create_encryption_key(self):
        """Erstellt oder lädt Verschlüsselungsschlüssel"""
        try:
            with open('.encryption_key', 'rb') as key_file:
                return key_file.read()
        except FileNotFoundError:
            key = Fernet.generate_key()
            with open('.encryption_key', 'wb') as key_file:
                key_file.write(key)
            logging.info("Neuer Verschlüsselungsschlüssel erstellt")
            return key
    
    @contextmanager
    def get_db_connection(self):
        """Sichere Datenbankverbindung mit automatischem Schließen"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=30.0)
            conn.execute("PRAGMA journal_mode=WAL")  # Write-Ahead Logging für bessere Performance
            conn.execute("PRAGMA foreign_keys=ON")   # Foreign Key Constraints aktivieren
            conn.row_factory = sqlite3.Row
            yield conn
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Datenbankfehler: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _init_database(self):
        """Initialisiert Datenbanktabellen"""
        with self.get_db_connection() as conn:
            # Benutzer-Tabelle
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    api_key_encrypted BLOB NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    failed_login_attempts INTEGER DEFAULT 0,
                    locked_until TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Session-Tabelle
            conn.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    ip_address TEXT,
                    user_agent TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
                )
            ''')
            
            # Login-Versuche-Tabelle für Rate Limiting
            conn.execute('''
                CREATE TABLE IF NOT EXISTS login_attempts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ip_address TEXT NOT NULL,
                    username TEXT,
                    success BOOLEAN NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logging.info("Datenbank initialisiert")
    
    def _encrypt_api_key(self, api_key):
        """Verschlüsselt API-Schlüssel"""
        return self.cipher_suite.encrypt(api_key.encode())
    
    def _decrypt_api_key(self, encrypted_api_key):
        """Entschlüsselt API-Schlüssel"""
        return self.cipher_suite.decrypt(encrypted_api_key).decode()
    
    def create_user(self, username, password, api_key):
        """Erstellt neuen Benutzer mit verschlüsseltem API-Schlüssel"""
        if len(username) < 3:
            raise ValueError("Benutzername muss mindestens 3 Zeichen lang sein")
        if len(password) < 8:
            raise ValueError("Passwort muss mindestens 8 Zeichen lang sein")
        if not api_key or len(api_key) < 10:
            raise ValueError("Gültiger API-Schlüssel erforderlich")
        
        password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        encrypted_api_key = self._encrypt_api_key(api_key)
        
        try:
            with self.get_db_connection() as conn:
                conn.execute('''
                    INSERT INTO users (username, password_hash, api_key_encrypted)
                    VALUES (?, ?, ?)
                ''', (username, password_hash, encrypted_api_key))
                conn.commit()
                logging.info(f"Benutzer '{username}' erfolgreich erstellt")
                return True
        except sqlite3.IntegrityError:
            logging.warning(f"Benutzer '{username}' existiert bereits")
            raise ValueError("Benutzername bereits vergeben")
    
    def authenticate_user(self, username, password, ip_address, user_agent):
        """Authentifiziert Benutzer mit Sicherheitsprüfungen"""
        # Rate Limiting prüfen
        if self._is_rate_limited(ip_address):
            logging.warning(f"Rate Limit erreicht für IP: {ip_address}")
            raise ValueError("Zu viele Anmeldeversuche. Bitte warten Sie.")
        
        # Login-Versuch protokollieren
        self._log_login_attempt(ip_address, username, False)
        
        with self.get_db_connection() as conn:
            user = conn.execute('''
                SELECT id, username, password_hash, api_key_encrypted, failed_login_attempts, locked_until
                FROM users 
                WHERE username = ? AND is_active = 1
            ''', (username,)).fetchone()
            
            if not user:
                logging.warning(f"Login-Versuch für unbekannten Benutzer: {username}")
                raise ValueError("Ungültige Anmeldedaten")
            
            # Account-Sperre prüfen
            if user['locked_until'] and datetime.fromisoformat(user['locked_until']) > datetime.now():
                logging.warning(f"Versuch, gesperrtes Konto anzumelden: {username}")
                raise ValueError("Konto ist gesperrt. Bitte kontaktieren Sie den Administrator.")
            
            # Passwort prüfen
            if not check_password_hash(user['password_hash'], password):
                # Fehlgeschlagene Versuche erhöhen
                failed_attempts = user['failed_login_attempts'] + 1
                locked_until = None
                
                if failed_attempts >= 5:
                    locked_until = (datetime.now() + timedelta(minutes=30)).isoformat()
                    logging.warning(f"Konto gesperrt nach {failed_attempts} fehlgeschlagenen Versuchen: {username}")
                
                conn.execute('''
                    UPDATE users 
                    SET failed_login_attempts = ?, locked_until = ?
                    WHERE id = ?
                ''', (failed_attempts, locked_until, user['id']))
                conn.commit()
                
                raise ValueError("Ungültige Anmeldedaten")
            
            # Erfolgreiche Anmeldung
            session_id = secrets.token_urlsafe(32)
            expires_at = (datetime.now() + timedelta(hours=24)).isoformat()
            
            # Session erstellen
            conn.execute('''
                INSERT INTO sessions (id, user_id, expires_at, ip_address, user_agent)
                VALUES (?, ?, ?, ?, ?)
            ''', (session_id, user['id'], expires_at, ip_address, user_agent))
            
            # Login-Daten aktualisieren
            conn.execute('''
                UPDATE users 
                SET last_login = CURRENT_TIMESTAMP, failed_login_attempts = 0, locked_until = NULL
                WHERE id = ?
            ''', (user['id'],))
            
            conn.commit()
            
            # Erfolgreichen Login protokollieren
            self._log_login_attempt(ip_address, username, True)
            logging.info(f"Erfolgreiche Anmeldung: {username}")
            
            return {
                'session_id': session_id,
                'user_id': user['id'],
                'username': user['username'],
                'api_key': self._decrypt_api_key(user['api_key_encrypted'])
            }
    
    def get_user_by_session(self, session_id):
        """Lädt Benutzer basierend auf Session-ID"""
        with self.get_db_connection() as conn:
            result = conn.execute('''
                SELECT u.id, u.username, u.api_key_encrypted, s.expires_at
                FROM users u
                JOIN sessions s ON u.id = s.user_id
                WHERE s.id = ? AND u.is_active = 1
            ''', (session_id,)).fetchone()
            
            if not result:
                return None
            
            # Session-Ablauf prüfen
            if datetime.fromisoformat(result['expires_at']) < datetime.now():
                self.logout_user(session_id)
                return None
            
            return {
                'user_id': result['id'],
                'username': result['username'],
                'api_key': self._decrypt_api_key(result['api_key_encrypted'])
            }
    
    def logout_user(self, session_id):
        """Meldet Benutzer ab (löscht Session)"""
        with self.get_db_connection() as conn:
            conn.execute('DELETE FROM sessions WHERE id = ?', (session_id,))
            conn.commit()
            logging.info(f"Session beendet: {session_id[:8]}...")
    
    def delete_user(self, username):
        """Löscht Benutzer (nur für Admin-Funktionen)"""
        with self.get_db_connection() as conn:
            result = conn.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
            if result.rowcount > 0:
                logging.info(f"Benutzer gelöscht: {username}")
                return True
            return False
    
    def list_users(self):
        """Listet alle aktiven Benutzer auf"""
        with self.get_db_connection() as conn:
            users = conn.execute('''
                SELECT username, created_at, last_login
                FROM users 
                WHERE is_active = 1
                ORDER BY username
            ''').fetchall()
            return [dict(user) for user in users]
    
    def _is_rate_limited(self, ip_address, max_attempts=10, time_window=15):
        """Prüft Rate Limiting für IP-Adresse"""
        with self.get_db_connection() as conn:
            cutoff_time = (datetime.now() - timedelta(minutes=time_window)).isoformat()
            attempts = conn.execute('''
                SELECT COUNT(*) as count
                FROM login_attempts
                WHERE ip_address = ? AND timestamp > ? AND success = 0
            ''', (ip_address, cutoff_time)).fetchone()
            
            return attempts['count'] >= max_attempts
    
    def _log_login_attempt(self, ip_address, username, success):
        """Protokolliert Login-Versuche"""
        with self.get_db_connection() as conn:
            conn.execute('''
                INSERT INTO login_attempts (ip_address, username, success)
                VALUES (?, ?, ?)
            ''', (ip_address, username, success))
            conn.commit()
    
    def cleanup_old_sessions(self):
        """Entfernt abgelaufene Sessions"""
        with self.get_db_connection() as conn:
            conn.execute('DELETE FROM sessions WHERE expires_at < ?', (datetime.now().isoformat(),))
            conn.commit()
    
    def get_user_by_id(self, user_id):
        """Lädt Benutzer basierend auf User-ID"""
        with self.get_db_connection() as conn:
            result = conn.execute('''
                SELECT id, username, api_key_encrypted
                FROM users 
                WHERE id = ? AND is_active = 1
            ''', (user_id,)).fetchone()
            
            if not result:
                return None
            
            return {
                'user_id': result['id'],
                'username': result['username'],
                'api_key': self._decrypt_api_key(result['api_key_encrypted'])
            }
