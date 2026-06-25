"""Role-parameterized MCP *host* server — one shared authoritative game.

For a live cross-group match the two teams act on **one** game state: this server
exposes the same six tools but each takes an explicit ``role`` argument (instead of
binding the role at build time like the per-agent cop/thief servers). One team
hosts it; both teams' drivers connect and each drives only its own role's turns.
No LLM, no secrets (ADR-001). Omitted from coverage (FastMCP transport glue).
"""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from ...shared.constants import ActionKind, Role
from ...shared.mcp_auth import TokenAuth
from ...shared.models import Action
from .servers import _StaticTokenVerifier
from .tools import ToolService


def build_host_server(tools: ToolService, auth: TokenAuth | None = None) -> FastMCP:
    """Build the shared-game host server (role-parameterized tools)."""
    verifier = _StaticTokenVerifier(auth) if auth is not None else None
    mcp: FastMCP = FastMCP("host", auth=verifier)

    @mcp.tool
    def get_observation(role: str) -> dict[str, Any]:
        return tools.get_observation(Role(role))

    @mcp.tool
    def send_message(role: str, text: str) -> dict[str, Any]:
        return tools.send_message(Role(role), text)

    @mcp.tool
    def receive_message(role: str) -> dict[str, Any] | None:
        return tools.receive_message(Role(role))

    @mcp.tool
    def submit_action(role: str, kind: str, dx: int = 0, dy: int = 0) -> dict[str, Any]:
        return tools.submit_action(Role(role), Action(ActionKind(kind), dx, dy))

    @mcp.tool
    def verify_location(role: str) -> dict[str, int]:
        return tools.verify_location(Role(role))

    @mcp.tool
    def get_game_status() -> dict[str, Any]:
        return tools.get_game_status()

    return mcp
