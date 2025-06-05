#!/bin/bash

# Bitpanda Portfolio Viewer - Installation Script für Unix/Linux/macOS

echo "🚀 Bitpanda Portfolio Viewer Installation"
echo "========================================="

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file nicht gefunden!"
    echo "📝 Erstelle .env aus .env.example..."
    
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ .env Datei erstellt!"
        echo "📋 Bitte tragen Sie Ihren Bitpanda API-Schlüssel in die .env Datei ein:"
        echo "   API_KEY=ihr_api_schluessel_hier"
        echo ""
    else
        echo "❌ .env.example nicht gefunden!"
        exit 1
    fi
fi

# Install Python dependencies
echo "📦 Python-Abhängigkeiten installieren..."
pip install -r requirements.txt

# Install Node.js dependencies
echo "📦 Frontend-Abhängigkeiten installieren..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Installation abgeschlossen!"
echo ""
echo "🎯 Starten Sie die Anwendung mit:"
echo "   Backend:  python backend/app.py"
echo "   Frontend: cd frontend && npm run dev"
echo ""
echo "🌐 Zugriff über: http://localhost:5173"
