"""Cornering cop policy (Phase 4): a one-ply look-ahead that herds the thief.

The greedy heuristic ([`heuristic.cop_action`]) minimises *only* distance, so on an
open board the cop and an equal-speed thief mirror each other into a limit cycle and
the thief survives the move cap (README R.3). This policy instead evaluates each
candidate cop action by the position it leaves **after the thief's best evasion**,
ranking lexicographically by ``(distance, thief escape options)``. Minimising the
thief's escape options drives it into a corner — where edges act as walls and its
mobility collapses — so the cop closes the final gap and captures.

Fully observable, deterministic, and stateless: a drop-in :data:`Decider`.
"""

from __future__ import annotations

from ...shared.constants import DIRECTIONS_8, Role
from ...shared.models import Action, GameState
from ..board import passable
from ..game_engine import GameEngine
from .geometry import chebyshev
from .heuristic import thief_action


def _clone(state: GameState) -> GameState:
    """Copy a state so look-ahead simulation never mutates the real game."""
    return GameState(
        state.width,
        state.height,
        state.cop,
        state.thief,
        set(state.barriers),
        state.moves_used,
        state.cop_barriers_used,
        state.to_move,
        state.winner,
        state.done,
    )


def _escape_options(engine: GameEngine, state: GameState) -> int:
    """Count thief moves that strictly increase Chebyshev distance from the cop."""
    here = chebyshev(state.cop, state.thief)
    return sum(
        1
        for dx, dy in DIRECTIONS_8
        if passable(engine.board, state.barriers, state.thief.step(dx, dy))
        and chebyshev(state.cop, state.thief.step(dx, dy)) > here
    )


def _evaluate(engine: GameEngine, after_cop: GameState) -> tuple[int, int]:
    """Score the cop position after the thief's greedy reply (higher is better)."""
    reply = _clone(after_cop)
    engine.apply(reply, thief_action(engine, reply))
    # Negate so ``max`` prefers the smaller distance, then the fewer escape options.
    return (-chebyshev(reply.cop, reply.thief), -_escape_options(engine, reply))


def smart_cop_action(engine: GameEngine, state: GameState) -> Action:
    """Pursue with cornering: pick the action that best pins the thief."""
    best_action, best_score = Action.stay(), None
    for action in engine.legal_actions(state):
        nxt = _clone(state)
        engine.apply(nxt, action)
        if nxt.done and nxt.winner is Role.COP:
            return action  # immediate capture dominates everything
        score = _evaluate(engine, nxt)
        if best_score is None or score > best_score:
            best_action, best_score = action, score
    return best_action
