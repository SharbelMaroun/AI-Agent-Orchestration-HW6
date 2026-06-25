"""LLM client interface. Every completion is routed through the gatekeeper.

The orchestrator (client) holds the LLM — never the MCP server. A concrete
provider backend is injected; tests use a deterministic fake (no network).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Protocol

from .gatekeeper import ApiGatekeeper


class LLMClient(Protocol):
    """Anything that turns a prompt into a completion string."""

    def complete(self, prompt: str) -> str: ...


class GatekeptLLM:
    """Wraps a completion backend so every call passes through the gatekeeper."""

    def __init__(self, backend: Callable[[str], str], gatekeeper: ApiGatekeeper) -> None:
        self.backend = backend
        self.gatekeeper = gatekeeper

    def complete(self, prompt: str) -> str:
        return self.gatekeeper.execute(self.backend, prompt)
