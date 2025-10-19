# NarhvalTest1

Deze repository bevat een eenvoudige demo van een OpenAI "agent" bestaande uit een Python-backend en een React-frontend.

## Backend (FastAPI)

De backend bevindt zich in de map [`backend`](backend/) en stelt een `/api/chat`-endpoint beschikbaar dat de OpenAI Responses API aanroept. Start de server als volgt:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn app:app --reload
```

Zorg ervoor dat de omgevingsvariabele `OPENAI_API_KEY` is ingesteld voordat je de server start.

## Frontend (React + Vite)

De frontend staat in de map [`frontend`](frontend/). De ontwikkelserver start je met:

```bash
cd frontend
npm install
npm run dev
```

De Vite-configuratie proxyt `/api`-verzoeken automatisch naar `http://localhost:8000`, waar de FastAPI-server draait.

## Werking

1. Open [http://localhost:5173](http://localhost:5173) zodra zowel backend als frontend draaien.
2. Typ een prompt in het tekstveld en druk op **Stuur naar agent**.
3. Het antwoord van het model verschijnt in het gespreksoverzicht.

De standaard systeemboodschap is "Je bent een behulpzame assistent.", maar je kunt dit naar wens aanpassen in [`App.jsx`](frontend/src/App.jsx).
