"""4-directional policy for the inter-group interop game (no diagonals).

The partner's protocol is orthogonal-only, so our side plays the same move set:
the **cop** minimises Chebyshev-then-Manhattan distance to the thief; the **thief**
maximises distance, then its own open neighbours (escape room). Pure and testable;
falls back to STAY only when fully surrounded (their protocol never needs STAY, but
our engine does when no orthogonal move is legal).
"""

from __future__ import annotations

from ...shared.constants import Role
from ...shared.models import Action, GameState, Position
from ..board import passable
from ..game_engine import GameEngine

_ORTHO = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def _legal(engine: GameEngine, state: GameState) -> list[tuple[int, int]]:
    pos = state.cop if state.to_move is Role.COP else state.thief
    return [d for d in _ORTHO if passable(engine.board, state.barriers, pos.step(*d))]


def _cheb(a: Position, b: Position) -> int:
    return max(abs(a.x - b.x), abs(a.y - b.y))


def _manhattan(a: Position, b: Position) -> int:
    return abs(a.x - b.x) + abs(a.y - b.y)


def ortho_action(engine: GameEngine, state: GameState) -> Action:
    """Pick our 4-dir move: cop closes in; thief flees while keeping escape room."""
    legal = _legal(engine, state)
    if not legal:
        return Action.stay()
    is_cop = state.to_move is Role.COP
    me = state.cop if is_cop else state.thief
    other = state.thief if is_cop else state.cop

    def mobility(d: tuple[int, int]) -> int:
        nxt = me.step(*d)
        return sum(1 for o in _ORTHO if passable(engine.board, state.barriers, nxt.step(*o)))

    if is_cop:
        dx, dy = min(legal, key=lambda d: (_cheb(me.step(*d), other), _manhattan(me.step(*d), other)))
    else:
        dx, dy = max(legal, key=lambda d: (_cheb(me.step(*d), other), mobility(d)))
    return Action.move(dx, dy)
