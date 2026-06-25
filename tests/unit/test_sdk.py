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


_REPORT_SUMMARY = {"sub_games": [{"index": 0, "winner": "cop"}], "totals": {"cop": 90, "thief": 40}}


def test_send_match_report_disabled_by_default_returns_none():
    out = Sdk(CONFIG).send_match_report(_REPORT_SUMMARY, lambda *a: "id")
    assert out is None  # no reporting.send_real_email -> never sends


def test_send_match_report_sends_when_enabled():
    cfg = {**CONFIG, "reporting": {"recipient_email": "x@y", "timezone": "Asia/Jerusalem",
                                   "send_real_email": True}}
    sent = {}
    out = Sdk(cfg).send_match_report(_REPORT_SUMMARY, lambda to, s, b: sent.update(to=to) or "mid")
    assert out == "mid" and sent["to"] == "x@y"


def test_bonus_awards_and_final_via_sdk():
    from marl_cop_thief.services.bonus import SeriesResult

    sdk = Sdk(CONFIG)
    assert sdk.bonus_awards(SeriesResult({"A": 90, "B": 40})) == {"A": 10.0, "B": 5.0}
    series = [SeriesResult({"A": 90, "B": 40}), SeriesResult({"A": 40, "B": 90})]
    assert sdk.bonus_final("A", series) == 7.5
