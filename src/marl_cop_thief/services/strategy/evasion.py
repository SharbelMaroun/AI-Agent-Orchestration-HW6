"""Shared evasion scoring for the thief (avoids degenerate one-direction drift).

Greedy "maximise distance from the cop" ties on an open board, and a fixed
tie-break (direction order) makes the thief hug one wall (always-left). This ranks
a candidate cell by ``(distance from threat, own mobility, centrality)`` so the
thief flees *and* keeps escape room — using the whole board instead of a corner.
"""

from __future__ import annotations

from ...shared.constants import DIRECTIONS_8
from ...shared.models import Position
from ..board import Board, passable
from .geometry import chebyshev


def mobility(board: Board, barriers: set[Position], pos: Position) -> int:
    """Number of passable neighbouring cells (how much open space surrounds ``pos``)."""
    return sum(1 for dx, dy in DIRECTIONS_8 if passable(board, barriers, pos.step(dx, dy)))


def center_distance(pos: Position, board: Board) -> int:
    """Chebyshev distance from the board centre (lower = more central, more escape room)."""
    return chebyshev(pos, Position(board.width // 2, board.height // 2))


def evade_key(
    board: Board, barriers: set[Position], newpos: Position, threat: Position
) -> tuple[int, int, int]:
    """Rank an evasion target: farther from the threat, then more open, then more central."""
    return (
        chebyshev(newpos, threat),
        mobility(board, barriers, newpos),
        -center_distance(newpos, board),
    )
