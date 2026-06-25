"""Tests for the inter-group interop match driver (fake partner decider)."""

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.interop_match import (
    make_partner_decide,
    play_interop_game,
    run_interop_series,
)
from marl_cop_thief.shared.constants import Role
from marl_cop_thief.shared.models import Action, GameState, Position

CONFIG = {
    "grid_size": [5, 5], "max_moves": 25, "num_games": 6, "max_barriers": 5,
    "seed": 1, "visibility_radius": 9,
    "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5},
    "reporting": {"timezone": "Asia/Jerusalem"},
}


def _passive(_role, _state):
    return Action.stay()  # partner never moves


def test_play_interop_game_reaches_terminal_capture():
    engine = GameEngine(5, 5, 25, 5)
    state = GameState(5, 5, Position(0, 0), Position(2, 0), to_move=Role.COP)
    final = play_interop_game(engine, state, Role.COP, _passive)
    assert final.done and final.winner is Role.COP  # our cop catches the passive thief


def test_make_partner_decide_builds_obs_and_parses_action():
    engine = GameEngine(5, 5, 25, 5)
    state = GameState(5, 5, Position(0, 0), Position(2, 0), to_move=Role.THIEF)

    class FakeClient:
        def __init__(self):
            self.seen = None

        def decide(self, role, obs, rid):
            self.seen = (role, obs, rid)
            return {"type": "move", "direction": "right"}

    fc = FakeClient()
    decide = make_partner_decide(fc, engine, visibility_radius=9, new_id=lambda: "rid-x")
    action = decide(Role.THIEF, state)
    assert (action.dx, action.dy) == (1, 0)  # right -> +x
    assert fc.seen[0] == "thief" and fc.seen[2] == "rid-x"
    assert fc.seen[1]["request_id"] == "rid-x"  # observation carries the matching id


def test_run_interop_series_swaps_roles_and_scores():
    report = run_interop_series(CONFIG, {Role.COP: _passive, Role.THIEF: _passive})
    assert report["report_type"] == "interop_match" and len(report["sub_games"]) == 6
    roles = [g["my_role"] for g in report["sub_games"]]
    assert roles[:3] == ["cop"] * 3 and roles[3:] == ["thief"] * 3  # 3-cop / 3-thief swap
    assert report["totals"]["us"] >= report["totals"]["partner"]  # we beat a passive partner


def test_default_id_generator_and_meta_merge():
    engine = GameEngine(5, 5, 25, 5)
    state = GameState(5, 5, Position(0, 0), Position(1, 0), to_move=Role.THIEF)

    class _Client:
        def decide(self, role, obs, rid):
            assert isinstance(rid, str) and rid  # default uuid id was generated
            return {"type": "move", "direction": "right"}

    decide = make_partner_decide(_Client(), engine, visibility_radius=9)  # default new_id (uuid)
    assert decide(Role.THIEF, state).dx == 1

    report = run_interop_series(CONFIG, {Role.COP: _passive, Role.THIEF: _passive},
                                meta={"group_name": "Sharbel"})
    assert report["group_name"] == "Sharbel"  # meta merged into the report
