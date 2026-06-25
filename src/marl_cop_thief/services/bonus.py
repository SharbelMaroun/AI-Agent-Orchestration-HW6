"""Inter-group bonus scoring (assignment §12.2): per-series 10/5/5 + averaging.

A *series* is 6 games (3 cop / 3 thief, role-swapped) between two groups. The
group with the **higher accumulated score** wins **10** points, the loser **5**,
a complete **tie 5/5**; a series whose two reports **disagree** is void (**0** for
both). The **final bonus** is the average of a group's awards over all valid
series. Award values are parameters (defaults from the spec) so the exact rule
stays confirmable with course staff (audit C5). Pure arithmetic — fully testable.
"""

from __future__ import annotations

from dataclasses import dataclass

WIN_POINTS = 10.0
LOSE_POINTS = 5.0
TIE_POINTS = 5.0
VOID_POINTS = 0.0


@dataclass(frozen=True)
class SeriesResult:
    """One inter-group series: each group's accumulated score + mutual agreement."""

    totals_by_group: dict[str, int]  # e.g. {"Team-Alpha": 60, "Team-Beta": 80}
    mutual_agreement: bool = True


def series_awards(
    series: SeriesResult,
    *,
    win: float = WIN_POINTS,
    lose: float = LOSE_POINTS,
    tie: float = TIE_POINTS,
    void: float = VOID_POINTS,
) -> dict[str, float]:
    """Award each group its bonus points for one series (the report's ``bonus_claim``)."""
    groups = list(series.totals_by_group)
    if len(groups) != 2:
        raise ValueError("a series must have exactly two groups")
    if not series.mutual_agreement:
        return dict.fromkeys(groups, void)
    a, b = groups
    if series.totals_by_group[a] == series.totals_by_group[b]:
        return {a: tie, b: tie}
    winner = a if series.totals_by_group[a] > series.totals_by_group[b] else b
    return {g: (win if g == winner else lose) for g in groups}


def final_bonus(group: str, series_list: list[SeriesResult], **pts: float) -> float:
    """Average of ``group``'s per-series awards across all series (0.0 if none)."""
    if not series_list:
        return 0.0
    awards = [series_awards(s, **pts).get(group, 0.0) for s in series_list]
    return round(sum(awards) / len(awards), 2)
