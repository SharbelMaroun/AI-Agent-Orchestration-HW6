"""Select the LLM completion backend.

Uses the real OpenAI backend when ``OPENAI_API_KEY`` is set in the environment
(the CLI loads it from .env); otherwise falls back to a deterministic offline
echo backend so the app and tests still run with no network / no key.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any

from .config import load_json
from .gatekeeper import ApiGatekeeper, gatekeeper_from_config


def echo_backend(prompt: str) -> str:
    """Offline fallback: echo the prompt (no network)."""
    return prompt


def select_backend(config: dict[str, Any]) -> Callable[[str], str]:
    """OpenAI backend if a key is configured, else the offline echo backend."""
    if os.environ.get("OPENAI_API_KEY"):
        from .openai_backend import openai_backend

        model = config.get("llm", {}).get("model", "gpt-4o-mini")
        return openai_backend(model)
    return echo_backend


def select_gatekeeper(config: dict[str, Any]) -> ApiGatekeeper:
    """Config-driven gatekeeper when a real provider is in use; unlimited offline.

    Keying on the API key (not the match call) keeps offline/test runs fast and
    unthrottled, while real OpenAI runs honour ``config/rate_limits.json`` — editing
    that file changes behaviour with no code edit (PRD_gatekeeper S4). ``config`` is
    accepted for symmetry with :func:`select_backend` and future per-config limits.
    """
    if os.environ.get("OPENAI_API_KEY"):
        return gatekeeper_from_config(load_json("rate_limits.json"), "llm")
    return ApiGatekeeper()
