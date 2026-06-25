"""Shared grid-distance helpers for strategy policies (DRY).

Chebyshev (chessboard) distance is the natural metric for 8-directional movement:
one diagonal step changes it by exactly one, so it equals the minimum number of
moves between two cells on an open board. The arithmetic itself lives in
:mod:`...shared.grid_math` so the Position- and tuple-based callers share one core.
"""

from __future__ import annotations

from ...shared import grid_math
from ...shared.models import Position


def chebyshev(a: Position, b: Position) -> int:
    """Minimum 8-directional moves between two cells (ignoring barriers)."""
    return grid_math.chebyshev(a.x, a.y, b.x, b.y)
