"""Tests for the match orchestrator."""

import random

import pytest

from marl_cop_thief.services.orchestrator import Orchestrator
from marl_cop_thief.services.strategy.smart_cop import smart_cop_action
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
    orch = Orchestrator({**CONFIG, "strategy": {"type": "smart"}})
    assert orch.deciders[Role.COP] is smart_cop_action
    totals = orch.play_match()["totals"]
    assert totals["cop"] > totals["thief"]  # the cornering cop wins the match


def test_unknown_strategy_is_rejected():
    with pytest.raises(ValueError, match="Unknown cop strategy"):
        Orchestrator({**CONFIG, "strategy": {"type": "nope"}})
