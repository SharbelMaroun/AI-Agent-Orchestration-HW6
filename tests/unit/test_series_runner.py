"""Tests for the inter-group series runner (3-cop/3-thief role-swap)."""

from marl_cop_thief.services.series_runner import run_series

CONFIG = {
    "grid_size": [5, 5],
    "max_moves": 25,
    "max_barriers": 5,
    "seed": 7,
    "num_games": 6,
    "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5},
    "reporting": {"timezone": "Asia/Jerusalem"},
}


def test_report_shape_and_role_swap():
    rep = run_series(CONFIG, "A", "B")
    assert rep["report_type"] == "bonus_game"
    assert len(rep["sub_games"]) == 6
    assert all(g["cop_group"] == "A" and g["thief_group"] == "B" for g in rep["sub_games"][:3])
    assert all(g["cop_group"] == "B" and g["thief_group"] == "A" for g in rep["sub_games"][3:])
    assert set(rep["totals_by_group"]) == {"A", "B"}
    assert set(rep["bonus_claim"]) == {"A", "B"}
    assert rep["timezone"] == "Asia/Jerusalem"


def test_totals_accumulate_per_group_with_swap():
    rep = run_series(CONFIG, "A", "B")
    a_total = sum(
        (g["cop_score"] if g["cop_group"] == "A" else g["thief_score"]) for g in rep["sub_games"]
    )
    assert rep["totals_by_group"]["A"] == a_total


def test_bonus_claim_matches_totals():
    rep = run_series(CONFIG, "A", "B")
    ta, tb = rep["totals_by_group"]["A"], rep["totals_by_group"]["B"]
    claim = rep["bonus_claim"]
    if ta > tb:
        assert claim == {"A": 10.0, "B": 5.0}
    elif tb > ta:
        assert claim == {"A": 5.0, "B": 10.0}
    else:
        assert claim == {"A": 5.0, "B": 5.0}


def test_series_is_deterministic():
    assert run_series(CONFIG, "A", "B") == run_series(CONFIG, "A", "B")
