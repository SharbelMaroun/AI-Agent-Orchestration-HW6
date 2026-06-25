"""Tests for the match orchestrator."""

import random

import pytest

from marl_cop_thief.services.orchestrator import Orchestrator, select_thief_policy
from marl_cop_thief.services.strategy.heuristic import thief_action
from marl_cop_thief.services.strategy.smart_cop import smart_cop_action
from marl_cop_thief.services.strategy.smart_thief import smart_thief_action
from marl_cop_thief.shared.constants import Role

CONFIG = {
    "grid_size": [5, 5],
    "max_moves": 25,
    "num_games": 6,
    "max_barriers": 5,
    "seed": 7,
    "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5},
}


def test_play_subgame_terminates_and_scores():
    orch = Orchestrator(CONFIG)
    res = orch.play_subgame(0, random.Random(1))
    assert res.moves_used <= CONFIG["max_moves"]
    assert res.cop_score > 0 and res.thief_score > 0


def test_play_match_runs_all_subgames():
    summary = Orchestrator(CONFIG).play_match()
    assert len(summary["sub_games"]) == 6
    assert set(summary["totals"]) == {"cop", "thief"}
    assert summary["totals"]["cop"] > 0


def test_match_is_deterministic_for_seed():
    a = Orchestrator(CONFIG).play_match()
    b = Orchestrator(CONFIG).play_match()
    assert a == b


def test_config_without_seed_defaults():
    cfg = {k: v for k, v in CONFIG.items() if k != "seed"}
    summary = Orchestrator(cfg).play_match()
    assert len(summary["sub_games"]) == 6


def test_smart_strategy_is_selected_and_dominates():
    # cornering cop vs the greedy baseline thief (the controlled R.3 comparison)
    orch = Orchestrator({**CONFIG, "strategy": {"type": "smart", "thief_type": "greedy"}})
    assert orch.deciders[Role.COP] is smart_cop_action
    assert orch.deciders[Role.THIEF] is thief_action
    totals = orch.play_match()["totals"]
    assert totals["cop"] > totals["thief"]  # the cornering cop wins the match


def test_unknown_strategy_is_rejected():
    with pytest.raises(ValueError, match="Unknown cop strategy"):
        Orchestrator({**CONFIG, "strategy": {"type": "nope"}})


def test_select_thief_policy_default_smart_and_options():
    assert select_thief_policy(CONFIG) is smart_thief_action  # default = smart
    assert select_thief_policy({"strategy": {"thief_type": "greedy"}}) is thief_action


def test_unknown_thief_strategy_is_rejected():
    with pytest.raises(ValueError, match="Unknown thief strategy"):
        select_thief_policy({"strategy": {"thief_type": "nope"}})


def test_match_runs_on_non_square_boards():
    # sanity stage 2/3 (assignment Table 2): rectangular W != H boards work generically
    for w, h in [(3, 2), (4, 3)]:
        summary = Orchestrator({**CONFIG, "grid_size": [w, h]}).play_match()
        assert len(summary["sub_games"]) == 6
        assert all(s["moves_used"] <= CONFIG["max_moves"] for s in summary["sub_games"])
