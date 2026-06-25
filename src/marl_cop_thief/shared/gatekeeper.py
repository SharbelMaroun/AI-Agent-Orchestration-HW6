"""Minimal centralized API gatekeeper (pulled forward from Phase 9).

ALL external API calls (LLM, Gmail) must route through here. This minimal
version provides retry-on-failure and per-call logging driven by config limits;
the full FIFO queueing / backpressure / drain arrives with the Phase 9 version.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


class ApiGatekeeper:
    """Executes external calls with bounded retries and per-call logging."""

    def __init__(self, max_retries: int = 3) -> None:
        self.max_retries = max_retries
        self.calls = 0
        self.log: list[dict[str, Any]] = []

    def execute(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Call ``fn`` through the gatekeeper, retrying transient failures."""
        attempt = 0
        while True:
            self.calls += 1
            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                self.log.append({"ok": False, "attempt": attempt, "error": str(exc)})
                if attempt >= self.max_retries:
                    raise
                attempt += 1
                continue
            self.log.append({"ok": True, "attempt": attempt})
            return result


def gatekeeper_from_config(rate_limits: dict[str, Any], service: str = "default") -> ApiGatekeeper:
    """Build a gatekeeper from a parsed ``rate_limits.json`` mapping."""
    services = rate_limits.get("rate_limits", {}).get("services", {})
    cfg = services.get(service, services.get("default", {}))
    return ApiGatekeeper(max_retries=cfg.get("max_retries", 3))
