"""Tuple-based grid-distance helpers — the DRY core for every grid metric.

Both the strategy policies (via :mod:`..services.strategy.geometry`, which works on
:class:`..shared.models.Position` objects) and the remote-match driver (which works
on raw ``(x, y)`` tuples from the MCP observation) need the same distances, so the
arithmetic lives here once and each caller wraps it for its own types.
"""

from __future__ import annotations


def chebyshev(ax: int, ay: int, bx: int, by: int) -> int:
    """Minimum 8-directional moves between (ax, ay) and (bx, by) (chessboard distance)."""
    return max(abs(ax - bx), abs(ay - by))


def manhattan(ax: int, ay: int, bx: int, by: int) -> int:
    """4-directional (taxicab) distance between (ax, ay) and (bx, by)."""
    return abs(ax - bx) + abs(ay - by)
