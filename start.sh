#!/bin/bash

# Bitpanda Portfolio Viewer - Start Script für Unix/Linux/macOS

echo "🚀 Bitpanda Portfolio Viewer wird gestartet..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ .env Datei nicht gefunden!"
    echo "📝 Führen Sie zuerst das Installationsskript aus: ./install.sh"
    exit 1
fi

# Function to kill processes on script exit
cleanup() {
    echo ""
    echo "🛑 Server werden beendet..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start backend in background
echo "⚙️  Backend wird gestartet (Port 5000)..."
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend in background
echo "🎨 Frontend wird gestartet (Port 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait a moment for frontend to start
sleep 5

echo ""
echo "✅ Beide Server sind gestartet!"
echo "🌐 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:5000"
echo ""
echo "📝 Drücken Sie Ctrl+C zum Beenden"

# Wait for user to stop the script
wait
