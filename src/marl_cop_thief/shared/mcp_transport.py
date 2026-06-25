"""Client transport for calling a remote MCP server (via the gatekeeper).

Every remote tool call routes through the :class:`ApiGatekeeper` (rate limit,
retry, log) and carries a bearer token. The low-level ``invoke(base_url, tool,
params, token)`` callable is **injected** — production passes an adapter over
``fastmcp.Client`` (HTTP/streamable), tests pass a fake — so this stays offline-
testable and protocol-agnostic. Covers PRD_mcp_server §2.2/§3 (HTTP transport).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .gatekeeper import ApiGatekeeper

# (base_url, tool, params, token) -> tool result. Production: a fastmcp.Client adapter.
Invoke = Callable[[str, str, dict[str, Any], str], Any]


class McpClient:
    """Gatekeeper-routed, token-authenticated client for one remote MCP server."""

    def __init__(
        self,
        base_url: str,
        token: str,
        invoke: Invoke,
        gatekeeper: ApiGatekeeper | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._token = token
        self._invoke = invoke
        self._gatekeeper = gatekeeper or ApiGatekeeper()

    def call_tool(self, tool: str, **params: Any) -> Any:
        """Invoke a remote MCP tool by name through the gatekeeper; return its result."""
        return self._gatekeeper.execute(self._invoke, self.base_url, tool, params, self._token)
