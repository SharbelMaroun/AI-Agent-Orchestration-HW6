"""Smoke test: both FastMCP servers build and expose the six tools.

No network/server is started — this introspects the in-process tool registry.
"""

import asyncio

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.mcp.message_bus import MessageBus
from marl_cop_thief.services.mcp.servers import (
    TOOL_NAMES,
    build_cop_server,
    build_thief_server,
)
from marl_cop_thief.services.mcp.tools import ToolService
from marl_cop_thief.shared.models import GameState, Position


def _tools() -> ToolService:
    engine = GameEngine(5, 5, 25, 5)
    state = GameState(5, 5, Position(0, 0), Position(4, 4))
    return ToolService(engine, state, MessageBus(), visibility_radius=1, max_barriers=5)


def _tool_names(server) -> set[str]:
    return {tool.name for tool in asyncio.run(server.list_tools())}


def test_cop_server_exposes_six_tools():
    names = _tool_names(build_cop_server(_tools()))
    assert names == set(TOOL_NAMES)


def test_thief_server_exposes_six_tools():
    names = _tool_names(build_thief_server(_tools()))
    assert names == set(TOOL_NAMES)
