"""Tests for scoring and accumulation."""

from marl_cop_thief.services.scoring import accumulate, score_subgame
from marl_cop_thief.shared.constants import Role

SCORING = {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5}


def test_cop_win_scores():
    r = score_subgame(0, Role.COP, 10, SCORING)
    assert (r.cop_score, r.thief_score) == (20, 5)
    assert r.winner is Role.COP


def test_thief_win_scores():
    r = score_subgame(1, Role.THIEF, 25, SCORING)
    assert (r.cop_score, r.thief_score) == (5, 10)


def test_accumulate_sums_per_role():
    results = [score_subgame(i, Role.COP, 5, SCORING) for i in range(3)]
    results += [score_subgame(i, Role.THIEF, 25, SCORING) for i in range(3)]
    totals = accumulate(results)
    assert totals["cop"] == 3 * 20 + 3 * 5
    assert totals["thief"] == 3 * 5 + 3 * 10


def test_accumulate_empty():
    assert accumulate([]) == {"cop": 0, "thief": 0}
