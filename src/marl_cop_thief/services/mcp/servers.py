"""FastMCP server factories — thin transport glue exposing the tool service.

Two independent servers (cop, thief). The LLM is NOT here; servers expose tools
only. Each tool is bound to its owning role. Run with ``server.run()``.
"""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP
from fastmcp.server.auth import AccessToken, TokenVerifier

from ...shared.constants import ActionKind, Role
from ...shared.mcp_auth import TokenAuth
from ...shared.models import Action
from .tools import ToolService


class _StaticTokenVerifier(TokenVerifier):
    """Bridge our :class:`TokenAuth` to FastMCP's bearer-token auth."""

    def __init__(self, auth: TokenAuth) -> None:
        super().__init__()
        self._auth = auth

    async def verify_token(self, token: str) -> AccessToken | None:
        subject = self._auth.verify(token)
        if subject is None:
            return None
        return AccessToken(token=token, client_id=subject, scopes=[])

TOOL_NAMES = (
    "get_observation",
    "send_message",
    "receive_message",
    "submit_action",
    "verify_location",
    "get_game_status",
)


def _build(name: str, tools: ToolService, role: Role, auth: TokenAuth | None = None) -> FastMCP:
    verifier = _StaticTokenVerifier(auth) if auth is not None else None
    mcp: FastMCP = FastMCP(name, auth=verifier)

    @mcp.tool
    def get_observation() -> dict[str, Any]:
        return tools.get_observation(role)

    @mcp.tool
    def send_message(text: str) -> dict[str, Any]:
        return tools.send_message(role, text)

    @mcp.tool
    def receive_message() -> dict[str, Any] | None:
        return tools.receive_message(role)

    @mcp.tool
    def submit_action(kind: str, dx: int = 0, dy: int = 0) -> dict[str, Any]:
        return tools.submit_action(role, Action(ActionKind(kind), dx, dy))

    @mcp.tool
    def verify_location() -> dict[str, int]:
        return tools.verify_location(role)

    @mcp.tool
    def get_game_status() -> dict[str, Any]:
        return tools.get_game_status()

    return mcp


def build_cop_server(tools: ToolService, auth: TokenAuth | None = None) -> FastMCP:
    return _build("cop", tools, Role.COP, auth)


def build_thief_server(tools: ToolService, auth: TokenAuth | None = None) -> FastMCP:
    return _build("thief", tools, Role.THIEF, auth)
