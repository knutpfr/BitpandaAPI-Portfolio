#!/bin/bash

# Git Repository Initialisierung für Unix/Linux/macOS

echo "🎯 Git Repository Initialisierung"
echo "=================================="

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git ist nicht installiert"
    echo "📥 Bitte installieren Sie Git: https://git-scm.com/downloads"
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo "📁 Git Repository initialisieren..."
    git init
    echo "✅ Git Repository initialisiert!"
else
    echo "✅ Git Repository bereits vorhanden"
fi

# Make shell scripts executable
echo "🔧 Shell-Skripte ausführbar machen..."
chmod +x install.sh start.sh git-init.sh

# Create .gitignore if not exists (should already exist)
if [ ! -f ".gitignore" ]; then
    echo "📝 .gitignore erstellen..."
    cat > .gitignore << EOF
# Environment files
.env
node_modules/
__pycache__/
EOF
fi

# Add all files to git
echo "📦 Dateien zu Git hinzufügen..."
git add .

# Check git status
echo "📊 Git Status:"
git status --short

# Create initial commit
echo "📝 Ersten Commit erstellen..."
git commit -m "Initial commit: Bitpanda Portfolio Viewer webapp"

echo ""
echo "✅ Git Repository ist bereit!"
echo ""
echo "🚀 Nächste Schritte:"
echo "   1. Erstellen Sie ein Repository auf GitHub/GitLab"
echo "   2. Fügen Sie das Remote-Repository hinzu:"
echo "      git remote add origin https://github.com/username/bitpanda-portfolio-viewer.git"
echo "   3. Pushen Sie den Code:"
echo "      git push -u origin main"
echo ""
