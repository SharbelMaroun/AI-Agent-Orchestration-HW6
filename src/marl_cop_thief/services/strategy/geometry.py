"""Shared grid-distance helpers for strategy policies (DRY).

Chebyshev (chessboard) distance is the natural metric for 8-directional movement:
one diagonal step changes it by exactly one, so it equals the minimum number of
moves between two cells on an open board.
"""

from __future__ import annotations

from ...shared.models import Position


def chebyshev(a: Position, b: Position) -> int:
    """Minimum 8-directional moves between two cells (ignoring barriers)."""
    return max(abs(a.x - b.x), abs(a.y - b.y))
