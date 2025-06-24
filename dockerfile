# Sicheres Docker Build für Bitpanda Portfolio

FROM node:18-alpine AS frontend-builder

# Frontend bauen
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim

# Sicherheits-Updates und Dependencies
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y gcc curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Non-root Benutzer erstellen
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

# Arbeitsverzeichnis
WORKDIR /app

# Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend-Anwendung kopieren
COPY --chown=appuser:appuser . .

# Frontend-Build kopieren
COPY --from=frontend-builder --chown=appuser:appuser /frontend/dist ./frontend/dist

# Verzeichnisse für Logs und Datenbank erstellen
RUN mkdir -p /app/logs /app/data && chown -R appuser:appuser /app

# Zu non-root Benutzer wechseln
USER appuser

# Umgebungsvariablen für Sicherheit
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Port für Flask-App
EXPOSE 5000

# Health Check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=5)" || exit 1

# Startkommando
CMD ["python", "app.py"]