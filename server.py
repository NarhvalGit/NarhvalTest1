"""
Flask Web Server voor OpenAI Chat Applicatie

Deze server biedt een REST API endpoint waarmee clients prompts kunnen versturen
die worden verwerkt door de OpenAI API en teruggestuurd naar de client.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.openai_agent import OpenAIAgent

app = Flask(__name__)
CORS(app)  # Enable CORS voor cross-origin requests vanuit de browser

# Initialiseer OpenAI Agent
# Verwacht dat OPENAI_API_KEY environment variabele is ingesteld
try:
    agent = OpenAIAgent()
    print("✓ OpenAI Agent succesvol geïnitialiseerd")
except ValueError as e:
    print(f"✗ Fout bij initialiseren OpenAI Agent: {e}")
    print("  Zorg dat OPENAI_API_KEY environment variabele is ingesteld")
    agent = None


@app.route('/')
def index():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "OpenAI Chat Server",
        "version": "1.0.0",
        "agent_initialized": agent is not None
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Chat endpoint die prompts ontvangt en OpenAI responses teruggeeft

    Request Body (JSON):
    {
        "prompt": "Jouw vraag hier",
        "model": "gpt-4o-mini"  (optioneel)
    }

    Response (JSON):
    {
        "success": true,
        "response": "AI antwoord hier",
        "model": "gpt-4o-mini"
    }

    Of bij error:
    {
        "success": false,
        "error": "Foutmelding hier"
    }
    """
    # Controleer of agent is geïnitialiseerd
    if agent is None:
        return jsonify({
            "success": False,
            "error": "OpenAI Agent niet geïnitialiseerd. Controleer OPENAI_API_KEY."
        }), 500

    # Haal data uit request
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "Geen JSON data ontvangen"
            }), 400

        prompt = data.get('prompt', '').strip()
        model = data.get('model', 'gpt-4o-mini')

        # Valideer prompt
        if not prompt:
            return jsonify({
                "success": False,
                "error": "Prompt mag niet leeg zijn"
            }), 400

        print(f"📝 Ontvangen prompt: {prompt[:100]}...")
        print(f"🤖 Model: {model}")

        # Verwerk prompt met OpenAI Agent
        try:
            response = agent.generate_response(prompt, model=model)

            print(f"✓ Response gegenereerd: {response[:100]}...")

            return jsonify({
                "success": True,
                "response": response,
                "model": model
            })

        except Exception as e:
            print(f"✗ OpenAI API fout: {str(e)}")
            return jsonify({
                "success": False,
                "error": f"OpenAI API fout: {str(e)}"
            }), 500

    except Exception as e:
        print(f"✗ Server fout: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Server fout: {str(e)}"
        }), 500


@app.route('/api/models', methods=['GET'])
def get_models():
    """Geeft beschikbare OpenAI modellen terug"""
    models = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-3.5-turbo"
    ]
    return jsonify({
        "success": True,
        "models": models,
        "default": "gpt-4o-mini"
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 OpenAI Chat Server wordt gestart...")
    print("="*60)
    print(f"📡 Server draait op: http://localhost:5000")
    print(f"💬 Chat endpoint: http://localhost:5000/api/chat")
    print(f"🔧 Status endpoint: http://localhost:5000/")
    print("="*60 + "\n")

    # Start Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
