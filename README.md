# NarhvalTest1

A minimal command-line interface for experimenting with the OpenAI Responses API.

## Requirements

* Python 3.10+
* An OpenAI API key with access to the target model

Install the Python dependencies into your environment:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
# Install tooling needed for development
pip install -e .[dev]
```

The project depends on the official [`openai`](https://pypi.org/project/openai/) package.

## Configuration

Export your API key before running the agent:

```bash
export OPENAI_API_KEY="sk-..."
```

## Usage

You can interact with the agent either via the packaged console script or the
standalone helper in `scripts/run_agent.py`.

### Console script

After installing the package, invoke the entry point:

```bash
run-openai-agent "Write a short haiku about narwhals"
```

### Standalone script

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
