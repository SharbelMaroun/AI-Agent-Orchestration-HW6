"""Tests for the SDK facade."""

from marl_cop_thief.sdk import Sdk

CONFIG = {
    "grid_size": [4, 4],
    "max_moves": 25,
    "num_games": 6,
    "max_barriers": 5,
    "seed": 3,
    "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5},
}


def test_run_match_with_explicit_config():
    summary = Sdk(CONFIG).run_match()
    assert len(summary["sub_games"]) == 6
    assert "totals" in summary


def test_run_match_with_default_config_loads_real_config():
    summary = Sdk().run_match()
    assert len(summary["sub_games"]) == 6  # config.json num_games == 6


NL_CONFIG = {**CONFIG, "visibility_radius": 1, "strategy": {"type": "heuristic"}}


def test_stream_simple_frames_runs_to_terminal():
    frames = list(Sdk(CONFIG).stream_simple_frames())
    assert frames[0][0].moves_used == 0 and frames[-1][0].done


def test_stream_nl_frames_runs_to_terminal():
    frames = list(Sdk(NL_CONFIG).stream_nl_frames(seed=2))
    assert frames[-1][0].done
