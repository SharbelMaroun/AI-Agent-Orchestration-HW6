"""Build the match summary (sub-game breakdown + per-role totals)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from ..shared.models import SubGameResult
from .scoring import accumulate


def summarize(results: Iterable[SubGameResult]) -> dict[str, Any]:
    """Turn scored sub-games into a serializable match summary."""
    results = list(results)
    return {
        "sub_games": [
            {
                "index": r.index,
                "winner": r.winner.value,
                "moves_used": r.moves_used,
                "cop_score": r.cop_score,
                "thief_score": r.thief_score,
            }
            for r in results
        ],
        "totals": accumulate(results),
    }
