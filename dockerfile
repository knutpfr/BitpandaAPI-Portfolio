# Multi-stage Dockerfile für Bitpanda Portfolio Viewer

# Stage 1: Frontend Build
FROM node:18-alpine AS frontend-build

WORKDIR /app/frontend

# Package.json kopieren und Dependencies installieren
COPY frontend/package*.json ./
RUN npm ci

# Frontend Code kopieren und bauen
COPY frontend/ ./
RUN npm run build

# Stage 2: Python Backend
FROM python:3.11-slim AS backend

# Arbeitsverzeichnis setzen
WORKDIR /app

# System Dependencies installieren
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Python Dependencies installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Backend Code kopieren
COPY backend/ ./backend/
COPY main.py ./

# Frontend Build aus vorheriger Stage kopieren
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Port freigeben
EXPOSE 5000

# Umgebungsvariablen setzen
ENV FLASK_APP=backend/app.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Produktionsserver installieren
RUN pip install --no-cache-dir gunicorn

# Non-root Benutzer erstellen für Sicherheit
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN chown -R appuser:appuser /app
USER appuser

# curl für Healthcheck installieren
USER root
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
USER appuser

# Healthcheck hinzufügen
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Anwendung mit Gunicorn starten (Produktionsserver)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "backend.app:app"]