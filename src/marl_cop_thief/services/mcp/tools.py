"""Tool service: the operations the MCP servers expose (no LLM here).

Backed by one shared game session (engine + state + message bus). Enforces
turn-ownership so an agent cannot act out of turn.
"""

from __future__ import annotations

from typing import Any

from ...shared.constants import Event, Role
from ...shared.models import Action, GameState
from ..game_engine import GameEngine
from ..observation import observe
from .message_bus import MessageBus


class ToolService:
    """Stateful tool backend bound to a single sub-game session."""

    def __init__(
        self,
        engine: GameEngine,
        state: GameState,
        bus: MessageBus,
        *,
        visibility_radius: int,
        max_barriers: int,
    ) -> None:
        self.engine = engine
        self.state = state
        self.bus = bus
        self.visibility_radius = visibility_radius
        self.max_barriers = max_barriers

    def get_observation(self, role: Role) -> dict[str, Any]:
        return observe(self.state, role, self.visibility_radius).to_dict()

    def send_message(self, sender: Role, text: str) -> dict[str, Any]:
        self.bus.send(sender, text)
        return {"ok": True}

    def receive_message(self, role: Role) -> dict[str, Any] | None:
        msg = self.bus.receive(role)
        if msg is None:
            return None
        return {"sender": msg.sender.value, "text": msg.text}

    def submit_action(self, role: Role, action: Action) -> dict[str, Any]:
        if self.state.done:
            return {"event": Event.ILLEGAL.value, "reason": "game over", "done": True}
        if self.state.to_move is not role:
            return {"event": Event.ILLEGAL.value, "reason": "not your turn", "done": False}
        result = self.engine.apply(self.state, action)
        winner = self.state.winner.value if self.state.winner else None
        return {"event": result.event.value, "done": self.state.done, "winner": winner}

    def verify_location(self, role: Role) -> dict[str, int]:
        pos = self.state.cop if role is Role.COP else self.state.thief
        return {"x": pos.x, "y": pos.y}

    def get_game_status(self) -> dict[str, Any]:
        return {
            "to_move": self.state.to_move.value,
            "moves_used": self.state.moves_used,
            "moves_left": self.engine.max_moves - self.state.moves_used,
            "barriers_left": self.max_barriers - self.state.cop_barriers_used,
            "done": self.state.done,
            "winner": self.state.winner.value if self.state.winner else None,
        }
