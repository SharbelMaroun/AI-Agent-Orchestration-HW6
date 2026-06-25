"""Natural-language decider: read message -> update belief -> act -> send message.

Plugs into the orchestrator's ``Decider`` interface. Agents coordinate over the
MCP message bus in free text; the LLM (via the gatekeeper) interprets opponent
messages under partial observation.
"""

from __future__ import annotations

from ...shared.constants import ActionKind, Role
from ...shared.llm_client import LLMClient
from ...shared.models import Action, GameState, Position
from ..game_engine import GameEngine
from ..mcp.message_bus import MessageBus
from ..observation import observe
from ..strategy.evasion import evade_key
from .nl_decode import interpret
from .nl_encode import Speaker, encode


def _chebyshev(a: Position, b: Position) -> int:
    return max(abs(a.x - b.x), abs(a.y - b.y))


class NLDecider:
    """Stateful decider for one agent across a sub-game (holds its belief)."""

    def __init__(
        self,
        role: Role,
        bus: MessageBus,
        llm: LLMClient,
        visibility_radius: int,
        speaker: Speaker = encode,
    ) -> None:
        self.role = role
        self.bus = bus
        self.llm = llm
        self.visibility_radius = visibility_radius
        self.speaker = speaker
        self.belief: Position | None = None

    def __call__(self, engine: GameEngine, state: GameState) -> Action:
        obs = observe(state, self.role, self.visibility_radius)
        message = self.bus.receive(self.role)
        if message is not None:
            self.belief = interpret(self.llm, message.text, self.belief, engine.board)
        if obs.opponent_pos is not None:
            self.belief = obs.opponent_pos
        action = self._choose(engine, state)
        self.bus.send(self.role, self.speaker(self.role, obs, action))
        return action

    def _choose(self, engine: GameEngine, state: GameState) -> Action:
        moves = [a for a in engine.legal_actions(state) if a.kind is ActionKind.MOVE]
        if not moves:
            return Action.stay()
        target = self.belief or Position(engine.board.width // 2, engine.board.height // 2)
        if self.role is Role.COP:
            return min(moves, key=lambda a: _chebyshev(state.cop.step(a.dx, a.dy), target))
        # Thief: flee the believed cop while keeping escape room (avoids always-left drift).
        return max(
            moves,
            key=lambda a: evade_key(engine.board, state.barriers, state.thief.step(a.dx, a.dy), target),
        )
