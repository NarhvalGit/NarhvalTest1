from __future__ import annotations

import types

import pytest

pytest.importorskip("openai")

from openai import APIError, RateLimitError

from src.openai_agent import OpenAIAgent


class DummyClient:
    def __init__(self, handler):
        self._handler = handler
        self.responses = types.SimpleNamespace(create=self._handler)


def build_response(text: str | None):
    if text is None:
        content = []
    else:
        content = [
            types.SimpleNamespace(
                type="text", text=types.SimpleNamespace(value=text)
            )
        ]
    return types.SimpleNamespace(
        output=[types.SimpleNamespace(content=content)]
    )


def test_generate_response_success(monkeypatch):
    calls = {}

    def handler(model: str, input: str):
        calls["model"] = model
        calls["input"] = input
        return build_response("Hello back")

    agent = OpenAIAgent(client=DummyClient(handler))
    result = agent.generate_response("Hello", model="test-model")

    assert result == "Hello back"
    assert calls == {"model": "test-model", "input": "Hello"}


def test_generate_response_handles_rate_limit(monkeypatch):
    attempts = {"count": 0}

    def handler(model: str, input: str):
        attempts["count"] += 1
        if attempts["count"] < 3:
            raise RateLimitError("rate limit", None, None)
        return build_response("final response")

    agent = OpenAIAgent(client=DummyClient(handler), max_retries=3, retry_backoff=0.01)
    result = agent.generate_response("prompt", model="model")

    assert result == "final response"
    assert attempts["count"] == 3


def test_generate_response_raises_runtime_error_on_api_error():
    def handler(model: str, input: str):
        raise APIError("boom", None, None)

    agent = OpenAIAgent(client=DummyClient(handler))

    with pytest.raises(RuntimeError):
        agent.generate_response("prompt")


def test_generate_response_missing_text():
    def handler(model: str, input: str):
        return build_response(None)

    agent = OpenAIAgent(client=DummyClient(handler))

    with pytest.raises(RuntimeError):
        agent.generate_response("prompt")


def test_generate_response_requires_prompt():
    agent = OpenAIAgent(client=DummyClient(lambda *args, **kwargs: None))

    with pytest.raises(ValueError):
        agent.generate_response("")


def test_missing_api_key_raises_value_error(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError):
        OpenAIAgent(api_key=None, client=None)
