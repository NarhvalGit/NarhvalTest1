# NarhvalTest1 - Prompt Agent

Een Django web applicatie met PostgreSQL database voor het verwerken van AI prompts via de OpenAI API.
De applicatie bevat een command-line interface én een volledige web interface met agent management.

## Features

### Web Interface
- **Prompt Interface**: Gebruiksvriendelijke interface voor het invoeren van prompts
- **Agent Sessies**: Maak en beheer meerdere agent configuraties met verschillende models en system prompts
- **Geschiedenis**: Bekijk alle vorige prompts en responses
- **Real-time Processing**: Zie de verwerkingstijd en status van elke prompt
- **Admin Panel**: Django admin interface voor geavanceerd beheer

### CLI Interface
Ook beschikbaar als command-line tool voor snelle queries.

## Requirements

* Python 3.10+
* PostgreSQL 12+ (voor de database)
* An OpenAI API key with access to the target model

## Installatie

### 1. Python Environment Setup

Maak een virtual environment aan en installeer dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
# Voor development:
pip install -e .[dev]
```

### 2. PostgreSQL Database Setup

Installeer PostgreSQL indien nog niet geïnstalleerd:

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql
```

Start PostgreSQL en maak de database aan:

```bash
# Start PostgreSQL service
sudo service postgresql start  # Linux
# of
brew services start postgresql  # macOS

# Maak de database aan
./setup_database.sh
```

### 3. Environment Configuratie

Kopieer het `.env.example` bestand naar `.env` en vul je credentials in:

```bash
cp .env.example .env
```

Bewerk `.env` en vul in:
- `OPENAI_API_KEY`: Je OpenAI API key
- `DB_PASSWORD`: Je PostgreSQL wachtwoord (indien nodig)
- `DJANGO_SECRET_KEY`: Genereer een nieuwe secret key voor productie

### 4. Django Setup

Run migrations om de database te initialiseren:

```bash
python manage.py makemigrations
python manage.py migrate
```

Maak een admin gebruiker aan:

```bash
python manage.py createsuperuser
```

### 5. Start de Applicatie

Start de Django development server:

```bash
python manage.py runserver
```

De applicatie is nu beschikbaar op: **http://localhost:8000**

Admin panel: **http://localhost:8000/admin**

## Configuration

Configureer de applicatie via de `.env` file of environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export DB_NAME="prompt_agent_db"
export DB_USER="postgres"
export DB_PASSWORD="your_password"
```

## Usage

### Web Interface

1. Open http://localhost:8000 in je browser
2. Typ een prompt in het invoerveld
3. Kies optioneel een specifieke agent sessie
4. Klik op "Verstuur Prompt"
5. Bekijk het antwoord en de verwerkingstijd

### Agent Sessies

1. Ga naar http://localhost:8000/sessions/
2. Klik op "Nieuwe Sessie"
3. Geef de sessie een naam, kies een model (bijv. gpt-4o-mini)
4. Voeg optioneel een system prompt toe om het gedrag van de agent te configureren
5. Gebruik deze sessie bij het versturen van prompts

### CLI Interface

Je kunt ook de command-line interface gebruiken:

#### Console script

After installing the package, invoke the entry point:

```bash
run-openai-agent "Write a short haiku about narwhals"
```

#### Standalone script

If you prefer to run the repository version directly:

```bash
python scripts/run_agent.py "Explain how exponential backoff works"
```

Specify a different model using `--model`:

```bash
python scripts/run_agent.py "Summarise the latest changelog" --model gpt-4o-mini
```

## Development

Install the development extras and run the automated tests with:

```bash
pip install -e .[dev]
python -m pytest
```

The test-suite uses mocks and never contacts the OpenAI API.

## Project Structure

```
NarhvalTest1/
├── django_app/              # Django project directory
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI application
│   └── prompt_agent/        # Main Django app
│       ├── models.py        # Database models (PromptResponse, AgentSession)
│       ├── views.py         # View functions
│       ├── forms.py         # Django forms
│       ├── services.py      # Business logic and OpenAI integration
│       ├── admin.py         # Admin configuration
│       ├── urls.py          # App URL patterns
│       └── templates/       # HTML templates
├── src/                     # Core agent code
│   ├── openai_agent.py      # OpenAI agent wrapper
│   └── agent_cli.py         # CLI interface
├── scripts/                 # Utility scripts
├── tests/                   # Test suite
├── manage.py                # Django management script
├── setup_database.sh        # Database setup script
└── pyproject.toml           # Project dependencies

```

## Database Schema

### AgentSession
Beheert agent configuraties met verschillende models en system prompts.

### PromptResponse
Slaat alle prompts en responses op met metadata zoals:
- Status (pending, processing, completed, failed)
- Model gebruikt
- Verwerkingstijd
- Timestamps

## Dependencies

The project depends on:
- [`openai`](https://pypi.org/project/openai/) - OpenAI Python client
- [`django`](https://www.djangoproject.com/) - Web framework
- [`psycopg2-binary`](https://pypi.org/project/psycopg2-binary/) - PostgreSQL adapter
- [`python-dotenv`](https://pypi.org/project/python-dotenv/) - Environment variable management

## Troubleshooting

### Database Connection Issues

Als je problemen hebt met de database connectie:

```bash
# Check of PostgreSQL draait
sudo service postgresql status

# Test de connectie
psql -U postgres -h localhost -d prompt_agent_db
```

### OpenAI API Errors

Zorg ervoor dat:
- Je API key correct is ingesteld in `.env`
- Je API key niet is verlopen
- Je voldoende credits hebt in je OpenAI account

### Migration Errors

Als je problemen hebt met migrations:

```bash
# Reset migrations (pas op: verwijdert data!)
python manage.py migrate prompt_agent zero
python manage.py makemigrations
python manage.py migrate
```
