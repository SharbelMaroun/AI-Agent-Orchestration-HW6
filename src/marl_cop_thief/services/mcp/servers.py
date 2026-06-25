"""FastMCP server factories — thin transport glue exposing the tool service.

Two independent servers (cop, thief). The LLM is NOT here; servers expose tools
only. Each tool is bound to its owning role. Run with ``server.run()``.
"""

from __future__ import annotations

from typing import Any

from fastmcp import FastMCP

from ...shared.constants import ActionKind, Role
from ...shared.models import Action
from .tools import ToolService

TOOL_NAMES = (
    "get_observation",
    "send_message",
    "receive_message",
    "submit_action",
    "verify_location",
    "get_game_status",
)


def _build(name: str, tools: ToolService, role: Role) -> FastMCP:
    mcp: FastMCP = FastMCP(name)

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


def build_cop_server(tools: ToolService) -> FastMCP:
    return _build("cop", tools, Role.COP)


def build_thief_server(tools: ToolService) -> FastMCP:
    return _build("thief", tools, Role.THIEF)
