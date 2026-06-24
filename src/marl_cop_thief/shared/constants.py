"""Immutable project constants and enums.

Centralizing these here keeps magic numbers/strings out of the rest of the code
(guidelines section 7.2). String-valued enums serialize cleanly to JSON.
"""

from __future__ import annotations

from enum import Enum


class Role(str, Enum):
    """Which agent a position/score belongs to."""

    COP = "cop"
    THIEF = "thief"


class ActionKind(str, Enum):
    """The kinds of action an agent may propose on its turn."""

    MOVE = "move"
    PLACE_BARRIER = "place_barrier"
    STAY = "stay"


class Event(str, Enum):
    """Outcome of applying an action to the game state."""

    NONE = "none"
    CAPTURE = "capture"
    BARRIER_PLACED = "barrier_placed"
    ILLEGAL = "illegal"
    MAX_MOVES_REACHED = "max_moves_reached"


# 8-directional moves (orthogonal + diagonal), excluding the no-op (0, 0).
DIRECTIONS_8: tuple[tuple[int, int], ...] = tuple(
    (dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)
)
