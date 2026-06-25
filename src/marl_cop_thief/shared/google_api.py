"""Route Google (Gmail/Calendar) API calls through the central gatekeeper.

Google client requests expose a ``.execute()`` method; wrapping that call in
:meth:`ApiGatekeeper.execute` makes every Gmail/Calendar hit rate-limited,
FIFO-queued, retried, and logged — exactly like the LLM path
(:class:`..shared.llm_client.GatekeptLLM`). This closes the CLAUDE.md §2 rule that
*all* external API calls (LLM, Gmail, MCP) go through one gatekeeper.
"""

from __future__ import annotations

from typing import Any

from .config import load_json
from .gatekeeper import ApiGatekeeper, gatekeeper_from_config


def execute_request(request: Any, gatekeeper: ApiGatekeeper | None = None) -> Any:
    """Execute a Google API ``request`` (its ``.execute()``), via ``gatekeeper`` if given."""
    if gatekeeper is None:
        return request.execute()
    return gatekeeper.execute(request.execute)


def gmail_gatekeeper(service: str = "gmail") -> ApiGatekeeper:
    """Build the config-driven gatekeeper for Google calls from ``rate_limits.json``.

    Limits are read from configuration (never hard-coded); the default ``service`` is
    the ``gmail`` block in ``config/rate_limits.json``.
    """
    return gatekeeper_from_config(load_json("rate_limits.json"), service)
