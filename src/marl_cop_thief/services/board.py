"""Grid geometry and passability (Phase 1)."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

from ..shared.constants import DIRECTIONS_8
from ..shared.models import Position


@dataclass(frozen=True)
class Board:
    """A ``width`` x ``height`` grid (generic, supports non-square boards)."""

    width: int
    height: int

    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height

    def all_cells(self) -> Iterator[Position]:
        for y in range(self.height):
            for x in range(self.width):
                yield Position(x, y)

    def neighbors(self, pos: Position) -> list[Position]:
        """In-bounds 8-directional neighbours (ignores barriers)."""
        result = []
        for dx, dy in DIRECTIONS_8:
            candidate = pos.step(dx, dy)
            if self.in_bounds(candidate):
                result.append(candidate)
        return result


def passable(board: Board, barriers: set[Position], pos: Position) -> bool:
    """A cell is passable if it is in bounds and not a barrier."""
    return board.in_bounds(pos) and pos not in barriers
