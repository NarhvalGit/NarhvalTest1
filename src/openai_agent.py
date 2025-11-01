"""Utilities for interacting with the OpenAI Responses API."""
from __future__ import annotations

import os
import time
from typing import Optional

from openai import APIError, OpenAI, OpenAIError, RateLimitError


class OpenAIAgent:
    """Wrapper around the OpenAI client for simple text generation."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        client: Optional[OpenAI] = None,
        max_retries: int = 3,
        retry_backoff: float = 1.5,
    ) -> None:
        """Initialise the agent.

        Args:
            api_key: Explicit API key to use. Falls back to ``OPENAI_API_KEY``
                environment variable when omitted.
            client: Pre-configured :class:`~openai.OpenAI` client. When
                provided, ``api_key`` is ignored and no new client is created.
            max_retries: Maximum number of attempts when hitting rate limits.
            retry_backoff: Multiplicative factor for exponential backoff between
                retries.
        """

        if client is not None:
            self._client = client
        else:
            key = api_key or os.getenv("OPENAI_API_KEY")
            if not key:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is not set and no API key was provided."
                )
            self._client = OpenAI(api_key=key)

        if max_retries < 1:
            raise ValueError("max_retries must be at least 1")
        if retry_backoff <= 0:
            raise ValueError("retry_backoff must be greater than 0")

        self._max_retries = max_retries
        self._retry_backoff = retry_backoff

    @property
    def client(self) -> OpenAI:
        """Expose the underlying OpenAI client for advanced usage."""

        return self._client

    def generate_response(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        """Generate a response for the supplied prompt.

        Args:
            prompt: The user prompt to send to the model.
            model: The model identifier to call. Defaults to ``"gpt-4o-mini"``.

        Returns:
            The assistant's text response.

        Raises:
            RuntimeError: If the OpenAI API returns an unexpected error or no
                textual output is produced.
        """

        if not prompt:
            raise ValueError("Prompt must be a non-empty string")

        attempt = 0
        delay = 1.0
        while True:
            attempt += 1
            try:
                response = self._client.responses.create(model=model, input=prompt)
                text = self._extract_text(response)
                if text is None:
                    raise RuntimeError("No textual content returned by the OpenAI API")
                return text
            except RateLimitError as exc:  # pragma: no cover - triggered via mock
                if attempt >= self._max_retries:
                    raise RuntimeError("OpenAI API rate limit exceeded") from exc
                time.sleep(delay)
                delay *= self._retry_backoff
            except APIError as exc:  # pragma: no cover - triggered via mock
                raise RuntimeError(f"OpenAI API error: {exc}") from exc
            except OpenAIError as exc:  # pragma: no cover - triggered via mock
                raise RuntimeError(f"Unexpected OpenAI client error: {exc}") from exc

    @staticmethod
    def _extract_text(response: object) -> Optional[str]:
        """Extract textual content from a Responses API payload."""

        output = getattr(response, "output", None)
        if not output:
            return None

        for item in output:
            content = getattr(item, "content", None)
            if not content:
                continue
            for block in content:
                if getattr(block, "type", None) == "text":
                    text_obj = getattr(block, "text", None)
                    if text_obj is None:
                        continue
                    if isinstance(text_obj, str):
                        return text_obj
                    return getattr(text_obj, "value", None)
        return None


__all__ = ["OpenAIAgent"]
