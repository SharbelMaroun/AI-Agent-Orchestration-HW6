"""Integration: a full autonomous local match via the SDK."""

from marl_cop_thief.sdk import Sdk

CONFIG = {
    "grid_size": [5, 5],
    "max_moves": 25,
    "num_games": 6,
    "max_barriers": 5,
    "seed": 42,
    "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5},
}


def test_full_match_is_consistent():
    summary = Sdk(CONFIG).run_match()
    subs = summary["sub_games"]
    assert len(subs) == 6
    # Every sub-game has a valid winner and bounded moves.
    for sg in subs:
        assert sg["winner"] in ("cop", "thief")
        assert 1 <= sg["moves_used"] <= CONFIG["max_moves"]
    # Totals equal the sum of per-sub-game scores.
    assert summary["totals"]["cop"] == sum(sg["cop_score"] for sg in subs)
    assert summary["totals"]["thief"] == sum(sg["thief_score"] for sg in subs)
