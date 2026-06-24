"""Minimal deterministic heuristic deciders (default local policy).

Used so the orchestrator can run a full local match before the MCP/NL layer
exists. The cop minimizes Chebyshev distance to the thief; the thief maximizes
distance from the cop. Both choose only from the engine's legal actions.
"""

from __future__ import annotations

from ...shared.constants import ActionKind
from ...shared.models import Action, GameState, Position
from ..game_engine import GameEngine


def _chebyshev(a: Position, b: Position) -> int:
    return max(abs(a.x - b.x), abs(a.y - b.y))


def _legal_moves(engine: GameEngine, state: GameState) -> list[Action]:
    return [a for a in engine.legal_actions(state) if a.kind is ActionKind.MOVE]


def cop_action(engine: GameEngine, state: GameState) -> Action:
    """Pursue: step toward the thief, else stay."""
    moves = _legal_moves(engine, state)
    if not moves:
        return Action.stay()
    target = state.thief
    return min(moves, key=lambda a: _chebyshev(state.cop.step(a.dx, a.dy), target))


def thief_action(engine: GameEngine, state: GameState) -> Action:
    """Evade: step away from the cop, else stay."""
    moves = _legal_moves(engine, state)
    if not moves:
        return Action.stay()
    threat = state.cop
    return max(moves, key=lambda a: _chebyshev(state.thief.step(a.dx, a.dy), threat))
