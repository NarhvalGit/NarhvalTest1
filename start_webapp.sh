#!/bin/bash
#
# Start Script voor OpenAI Chat Webapp
# Gebruik: ./start_webapp.sh
#

echo "=========================================="
echo "🚀 OpenAI Chat Webapp Starter"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "⚠️  Geen virtual environment gevonden."
    echo "📦 Aanmaken van virtual environment..."
    python3 -m venv .venv
    echo "✓ Virtual environment aangemaakt"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activeren virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment geactiveerd"
echo ""

# Install dependencies
echo "📦 Installeren dependencies..."
pip install -q -r requirements-server.txt
echo "✓ Dependencies geïnstalleerd"
echo ""

# Check for API key
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY is niet ingesteld!"
    echo ""
    echo "Stel je API key in met:"
    echo "  export OPENAI_API_KEY='sk-your-api-key-here'"
    echo ""
    echo "Of maak een .env file:"
    echo "  cp .env.example .env"
    echo "  # Edit .env en vul je API key in"
    echo ""
    read -p "Wil je doorgaan zonder API key? (j/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Jj]$ ]]; then
        exit 1
    fi
else
    echo "✓ OPENAI_API_KEY gevonden"
    echo ""
fi

# Start server
echo "=========================================="
echo "🚀 Starten Flask Server..."
echo "=========================================="
echo ""
echo "Server URL: http://localhost:5000"
echo "Client URL: http://localhost:8000"
echo ""
echo "Open de client in je browser:"
echo "  cd client && python -m http.server 8000"
echo ""
echo "Druk CTRL+C om te stoppen"
echo ""

python server.py
