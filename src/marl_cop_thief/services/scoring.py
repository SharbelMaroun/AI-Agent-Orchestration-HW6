"""Scoring per sub-game and match accumulation (config-driven, no literals)."""

from __future__ import annotations

from collections.abc import Iterable

from ..shared.constants import Role
from ..shared.models import SubGameResult


def score_subgame(
    index: int, winner: Role, moves_used: int, scoring: dict[str, int]
) -> SubGameResult:
    """Score one sub-game from the config-provided scoring table."""
    if winner is Role.COP:
        return SubGameResult(index, winner, moves_used, scoring["cop_win"], scoring["thief_loss"])
    return SubGameResult(index, winner, moves_used, scoring["cop_loss"], scoring["thief_win"])


def accumulate(results: Iterable[SubGameResult]) -> dict[str, int]:
    """Sum sub-game scores into per-role match totals."""
    results = list(results)
    return {
        "cop": sum(r.cop_score for r in results),
        "thief": sum(r.thief_score for r in results),
    }
