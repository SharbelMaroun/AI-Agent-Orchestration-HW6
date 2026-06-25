"""Real OpenAI completion backend.

Omitted from coverage: it makes network calls and needs OPENAI_API_KEY. The
client reads the key from the environment (loaded from .env by the CLI).
"""

from __future__ import annotations

from collections.abc import Callable


def openai_backend(model: str = "gpt-4o-mini") -> Callable[[str], str]:
    """Return a completion callable backed by the OpenAI Chat Completions API."""
    from openai import OpenAI

    client = OpenAI()

    def call(prompt: str) -> str:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content or ""

    return call
