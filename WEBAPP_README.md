# 🤖 OpenAI Chat Webapp

Een complete client-server webapp voor interactie met OpenAI's API.

## 📋 Overzicht

Deze webapp bestaat uit twee componenten:

1. **Client** - HTML/CSS/JavaScript webapp die in de browser draait
2. **Server** - Python Flask API server die OpenAI API aanroept

## 🏗️ Architectuur

```
┌──────────────────┐                              ┌──────────────────┐
│   WEB BROWSER    │      HTTP/HTTPS              │   FLASK SERVER   │
│                  │◄────────────────────────────►│                  │
│  HTML + CSS +    │    POST /api/chat            │  server.py       │
│  JavaScript      │                              │  + OpenAI Agent  │
└──────────────────┘                              └────────┬─────────┘
                                                           │
                                                           ▼
                                                  ┌─────────────────┐
                                                  │  OpenAI API     │
                                                  │  (Internet)     │
                                                  └─────────────────┘
```

## 🚀 Snelstart

### 1️⃣ Installeer Dependencies

```bash
# Installeer server dependencies
pip install -r requirements-server.txt

# Of installeer de volledige package (inclusief OpenAI agent)
pip install -e .
```

### 2️⃣ Configureer OpenAI API Key

```bash
# Optie A: Environment variabele (aanbevolen)
export OPENAI_API_KEY="sk-your-api-key-here"

# Optie B: .env file
cp .env.example .env
# Edit .env en vul je API key in
```

### 3️⃣ Start de Server

```bash
python server.py
```

De server draait nu op: `http://localhost:5000`

### 4️⃣ Open de Client

Open in je browser:
```
file:///home/user/NarhvalTest1/client/index.html
```

Of gebruik een lokale webserver (aanbevolen voor CORS):
```bash
# Optie 1: Python's ingebouwde server
cd client
python -m http.server 8000

# Open dan: http://localhost:8000
```

```bash
# Optie 2: Node.js http-server (als je Node hebt)
cd client
npx http-server -p 8000
```

## 📁 Bestanden Structuur

```
NarhvalTest1/
├── client/                     # Frontend Webapp
│   ├── index.html             # Hoofdpagina
│   ├── style.css              # Styling
│   └── app.js                 # Client-side logica
│
├── server.py                  # Backend Flask Server
│
├── src/                       # OpenAI Agent Module
│   ├── openai_agent.py       # OpenAI API wrapper
│   └── agent_cli.py          # CLI interface
│
├── requirements-server.txt    # Server dependencies
├── .env.example              # API key template
└── WEBAPP_README.md          # Deze documentatie
```

## 🔧 Server API Endpoints

### `GET /`
Health check endpoint
```json
{
  "status": "online",
  "service": "OpenAI Chat Server",
  "version": "1.0.0",
  "agent_initialized": true
}
```

### `POST /api/chat`
Chat endpoint voor prompts

**Request:**
```json
{
  "prompt": "Wat is de hoofdstad van Nederland?",
  "model": "gpt-4o-mini"
}
```

**Response (Success):**
```json
{
  "success": true,
  "response": "De hoofdstad van Nederland is Amsterdam.",
  "model": "gpt-4o-mini"
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "Error bericht"
}
```

### `GET /api/models`
Geeft beschikbare OpenAI modellen

```json
{
  "success": true,
  "models": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
  "default": "gpt-4o-mini"
}
```

## 💡 Gebruik

1. **Start de server** (zie Snelstart)
2. **Open de client** in je browser
3. **Selecteer een model** (standaard: GPT-4o Mini)
4. **Typ je vraag** in het tekstveld
5. **Klik "Verzenden"** of druk **Enter**
6. **Wacht op het antwoord** van de AI

### Keyboard Shortcuts
- **Enter**: Verzend prompt
- **Shift + Enter**: Nieuwe regel in prompt

## 🎨 Client Features

- ✅ Real-time chat interface
- ✅ Model selectie (GPT-4o, GPT-4o-mini, etc.)
- ✅ Loading indicatoren
- ✅ Server status indicator
- ✅ Error handling met gebruiksvriendelijke meldingen
- ✅ Responsive design (werkt op desktop én mobiel)
- ✅ Smooth animations
- ✅ Auto-scroll naar nieuwe berichten

## 🔐 Server Features

- ✅ RESTful API met JSON
- ✅ CORS support voor cross-origin requests
- ✅ OpenAI Agent integratie met retry logic
- ✅ Exponential backoff voor rate limits
- ✅ Comprehensive error handling
- ✅ Input validatie
- ✅ Logging voor debugging

## 🐛 Troubleshooting

### Server start niet
```
✗ OpenAI Agent niet geïnitialiseerd
```
**Oplossing**: Controleer of `OPENAI_API_KEY` environment variabele is ingesteld.

### Client kan geen verbinding maken
```
Verbindingsfout: Failed to fetch
```
**Oplossing**:
1. Controleer of de server draait op `http://localhost:5000`
2. Controleer CORS instellingen in `server.py`
3. Open de client via `http://` i.p.v. `file://`

### CORS errors in browser console
**Oplossing**: Gebruik een lokale webserver voor de client:
```bash
cd client
python -m http.server 8000
```

### OpenAI API errors
```json
{"success": false, "error": "OpenAI API fout: ..."}
```
**Oplossing**:
1. Controleer je API key
2. Controleer je OpenAI account credits
3. Check OpenAI API status: https://status.openai.com/

## 📊 Beschikbare Modellen

| Model | Beschrijving | Gebruik |
|-------|-------------|---------|
| `gpt-4o-mini` | Snel en goedkoop | Ideaal voor de meeste taken |
| `gpt-4o` | Krachtigste model | Complexe taken |
| `gpt-4-turbo` | Snelle GPT-4 variant | Snelheid + kwaliteit |
| `gpt-3.5-turbo` | Oudere generatie | Budget-vriendelijk |

## 🚢 Production Deployment

Voor productie gebruik, gebruik een WSGI server zoals Gunicorn:

```bash
# Installeer Gunicorn (zit al in requirements-server.txt)
pip install gunicorn

# Start met Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app
```

Voor HTTPS en verdere optimalisaties, gebruik Nginx als reverse proxy.

## 🔒 Security Notes

⚠️ **Belangrijk voor productie:**

1. **API Key**: Bewaar NOOIT je API key in code of version control
2. **CORS**: Beperk CORS origins in productie
3. **Rate Limiting**: Implementeer rate limiting op de server
4. **HTTPS**: Gebruik altijd HTTPS in productie
5. **Input Validation**: Valideer en sanitize alle user input

## 🤝 Bijdragen

Dit project is onderdeel van NarhvalTest1. Zie `README.md` voor meer informatie over het bredere project.

## 📝 License

Zie hoofdproject README.

## 🙏 Credits

- OpenAI API
- Flask Framework
- Moderne CSS3 & ES6 JavaScript

---

**Veel plezier met de webapp! 🚀**
