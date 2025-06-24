# 🔐 Sicherheitsrichtlinien - Bitpanda Portfolio

## Übersicht

Diese Dokumentation beschreibt die implementierten Sicherheitsmaßnahmen für das Bitpanda Portfolio System, das für Docker-Deployment mit potentiellem externen Zugriff entwickelt wurde.

## 🛡️ Implementierte Sicherheitsfeatures

### 1. Authentifizierung & Autorisierung
- **Passwort-Hashing**: PBKDF2 mit SHA-256 und 16-Byte Salt
- **Session-Management**: Sichere Session-IDs mit 24h Timeout
- **Rate Limiting**: Schutz vor Brute-Force-Angriffen
- **Account-Sperrung**: Automatische Sperrung nach 5 fehlgeschlagenen Versuchen

### 2. Datenverschlüsselung
- **API-Schlüssel**: Fernet-Verschlüsselung für gespeicherte API-Keys
- **Datenbank**: SQLite mit WAL-Mode für Thread-Sicherheit
- **Transport**: HTTPS-ready (SSL-Konfiguration vorbereitet)

### 3. Input-Validierung
- **SQL-Injection-Schutz**: Prepared Statements
- **XSS-Schutz**: Content Security Policy Header
- **Path-Traversal-Schutz**: Eingabevalidierung für alle Parameter

### 4. Container-Sicherheit
- **Non-Root-User**: Anwendung läuft als unprivilegierter Benutzer
- **Minimal-Capabilities**: Nur notwendige Container-Rechte
- **Read-Only-Filesystem**: Wo möglich, schreibgeschützte Container
- **Security-Opt**: `no-new-privileges` aktiviert

### 5. Netzwerk-Sicherheit
- **Nginx Reverse Proxy**: Zusätzliche Sicherheitsebene
- **Rate Limiting**: Mehrstufiges Rate Limiting
- **Security Headers**: HSTS, CSP, X-Frame-Options, etc.
- **Port-Binding**: Nur auf localhost (127.0.0.1) gebunden

## 🚀 Setup-Anleitung

### Voraussetzungen
- Docker & Docker Compose
- Windows PowerShell (für Setup-Script)

### 1. Erstes Setup
```powershell
# Repository klonen/herunterladen
cd BitpandaAPI-Portfolio

# Sicheres Setup ausführen
.\start-secure.ps1
```

### 2. Umgebungsvariablen konfigurieren
```bash
# .env-Datei aus Vorlage erstellen
cp .env.template .env

# SECRET_KEY anpassen (wichtig!)
# Verwenden Sie einen zufälligen 32+ Zeichen String
```

### 3. Ersten Benutzer erstellen
1. Browser öffnen: `http://localhost`
2. "Registrieren" wählen
3. Starke Zugangsdaten eingeben:
   - Benutzername: 3-50 Zeichen, alphanumerisch + _
   - Passwort: Min. 8 Zeichen, Groß-/Kleinbuchstaben + Zahlen
   - API-Schlüssel: Ihr Bitpanda API-Key

## 🔒 Sicherheits-Checkliste

### Vor Produktionseinsatz
- [ ] `SECRET_KEY` in `.env` auf zufälligen Wert geändert
- [ ] Starke Passwörter für alle Benutzer
- [ ] Nginx SSL-Konfiguration aktiviert (für externen Zugriff)
- [ ] Firewall-Regeln konfiguriert
- [ ] Backup-Strategy implementiert
- [ ] Log-Monitoring eingerichtet

### Regelmäßige Wartung
- [ ] Logs auf verdächtige Aktivitäten prüfen
- [ ] Datenbank-Backups überprüfen
- [ ] Container-Updates einspielen
- [ ] Nicht verwendete Benutzer löschen

## 📊 Monitoring & Logs

### Log-Dateien
- **Anwendung**: `docker-compose logs bitpanda-portfolio`
- **Nginx**: `docker-compose logs nginx-proxy`
- **Sicherheit**: `logs/security.log` (im Container)

### Überwachung
```powershell
# Live-Logs anzeigen
docker-compose logs -f

# Health-Check
curl http://localhost/health

# Container-Status
docker-compose ps
```

## 🚨 Incident Response

### Bei verdächtigen Aktivitäten
1. **Logs analysieren**: `docker-compose logs | grep "WARNING\|ERROR"`
2. **Sessions beenden**: Container neustarten
3. **IPs blockieren**: Nginx-Konfiguration anpassen
4. **Passwörter ändern**: Betroffene Benutzer informieren

### Bei Kompromittierung
1. **Sofort offline**: `docker-compose down`
2. **Backup wiederherstellen**: Aus `backup/` Verzeichnis
3. **Alle Passwörter zurücksetzen**
4. **API-Schlüssel erneuern** (bei Bitpanda)

## 🌐 Externe Zugriff einrichten

### Port-Forwarding (Router)
1. Port 80/443 auf interne IP weiterleiten
2. DynDNS für dynamische IP einrichten
3. SSL-Zertifikat installieren (Let's Encrypt empfohlen)

### Nginx SSL-Konfiguration aktivieren
```bash
# SSL-Zertifikate in nginx/ssl/ ablegen
# nginx.conf HTTPS-Sektion einkommentieren
docker-compose restart nginx-proxy
```

### Zusätzliche Sicherheitsmaßnahmen für externen Zugriff
- VPN-Zugang bevorzugen
- Fail2Ban für erweiterten Schutz
- Cloudflare als zusätzliche WAF-Ebene
- Regelmäßige Penetrationstests

## 📚 Weitere Sicherheitsressourcen

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Docker Security Best Practices](https://docs.docker.com/engine/security/)
- [Flask Security Considerations](https://flask.palletsprojects.com/en/2.3.x/security/)

## 📞 Support

Bei Sicherheitsproblemen oder Fragen:
1. Logs sammeln: `docker-compose logs > security-incident.log`
2. System-Informationen: `docker-compose ps`
3. Detaillierte Beschreibung der Problematik

---

**⚠️ Wichtiger Hinweis**: Diese Anwendung wurde mit Fokus auf Sicherheit entwickelt, aber kein System ist 100% sicher. Regelmäßige Updates, Monitoring und sichere Konfiguration sind essentiell für den sicheren Betrieb.
