"""One-turn pipeline: select a decider, apply its action, return the result.

Keeps the orchestrator decoupled from *how* an action is chosen — a heuristic
now, an MCP/LLM decider later — behind the ``Decider`` callable type.
"""

from __future__ import annotations

from collections.abc import Callable

from ..shared.constants import Event, Role
from ..shared.models import Action, GameState, TurnResult
from .game_engine import GameEngine

Decider = Callable[[GameEngine, GameState], Action]


def run_turn(
    engine: GameEngine, state: GameState, deciders: dict[Role, Decider]
) -> TurnResult:
    """Apply the current actor's chosen action; fall back to STAY if illegal."""
    action = deciders[state.to_move](engine, state)
    result = engine.apply(state, action)
    if result.event is Event.ILLEGAL:
        result = engine.apply(state, Action.stay())
    return result
