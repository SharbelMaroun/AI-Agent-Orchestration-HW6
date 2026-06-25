"""Tests for the cross-network match driver (fake MCP host client)."""

from marl_cop_thief.services.remote_match import (
    build_match_report,
    play_my_turns,
    remote_decider,
)

_SCORE_CFG = {
    "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5},
    "reporting": {"timezone": "Asia/Jerusalem"},
}

FULL_5x5 = [[x, y] for x in range(5) for y in range(5)]


def _obs(self_pos, opponent, cells=None, barriers=()):
    return {
        "self": list(self_pos),
        "opponent": list(opponent) if opponent else None,
        "visible_cells": cells if cells is not None else FULL_5x5,
        "visible_barriers": [list(b) for b in barriers],
    }


class _FakeHost:
    """Scripts get_game_status responses; records calls; canned obs + submit result."""

    def __init__(self, statuses, submit_result=None, opponent=(4, 4)):
        self._statuses = statuses
        self._i = 0
        self.submit_result = submit_result or {"event": "move", "done": False}
        self.opponent = opponent
        self.calls = []

    def call_tool(self, tool, **params):
        self.calls.append((tool, params))
        if tool == "get_game_status":
            s = self._statuses[min(self._i, len(self._statuses) - 1)]
            self._i += 1
            return s
        if tool == "get_observation":
            return _obs((0, 0), self.opponent)
        if tool == "submit_action":
            return self.submit_result
        raise AssertionError(tool)


def test_acts_on_my_turn_then_returns_when_done():
    host = _FakeHost([{"to_move": "cop", "done": False}, {"to_move": "cop", "done": True}])
    out = play_my_turns(host, "cop", remote_decider("cop"))
    assert out["done"] is True
    assert any(t == "submit_action" for t, _ in host.calls)


def test_waits_when_not_my_turn():
    sleeps = []
    host = _FakeHost([{"to_move": "thief", "done": False}, {"to_move": "cop", "done": True}])
    play_my_turns(host, "cop", remote_decider("cop"), sleep=sleeps.append)
    assert sleeps  # polled and waited at least once


def test_illegal_submit_falls_back_to_stay():
    host = _FakeHost([{"to_move": "cop", "done": False}, {"to_move": "cop", "done": True}],
                     submit_result={"event": "illegal", "done": False})
    play_my_turns(host, "cop", remote_decider("cop"))
    kinds = [p.get("kind") for t, p in host.calls if t == "submit_action"]
    assert "stay" in kinds  # never stalls on an illegal move


def test_poll_limit_returns_final_status():
    host = _FakeHost([{"to_move": "thief", "done": False}])  # never my turn / never done
    out = play_my_turns(host, "cop", remote_decider("cop"), poll_limit=3)
    assert out["to_move"] == "thief"


def test_cop_closes_in_thief_flees():
    assert remote_decider("cop")(_obs((0, 0), (3, 3))) == ("move", 1, 1)  # toward
    assert remote_decider("thief")(_obs((2, 2), (3, 3))) == ("move", -1, -1)  # away, stays mobile


def test_blind_agent_heads_for_interior_not_stay():
    # rival unseen: move toward the visible centroid (2,2), not STAY
    assert remote_decider("cop")(_obs((0, 0), None)) == ("move", 1, 1)


def test_no_legal_move_stays():
    # only the current cell is on-board/visible -> no legal neighbour
    assert remote_decider("cop")(_obs((0, 0), (3, 3), cells=[[0, 0]])) == ("stay", 0, 0)


def test_avoids_visible_barrier():
    # barrier on the best diagonal -> cop picks a different legal step
    out = remote_decider("cop")(_obs((0, 0), (3, 3), barriers=[(1, 1)]))
    assert out[0] == "move" and out != ("move", 1, 1)


def test_build_match_report_cop_win():
    r = build_match_report(_SCORE_CFG, {"winner": "cop", "moves_used": 7}, "cop")
    assert r["report_type"] == "live_match" and r["winner"] == "cop" and r["my_role"] == "cop"
    assert r["cop_score"] == 20 and r["thief_score"] == 5
    assert r["timezone"] == "Asia/Jerusalem"


def test_build_match_report_thief_win():
    r = build_match_report(_SCORE_CFG, {"winner": "thief", "moves_used": 25}, "thief")
    assert r["cop_score"] == 5 and r["thief_score"] == 10


def test_build_match_report_no_winner_and_meta():
    r = build_match_report(_SCORE_CFG, {"winner": None, "moves_used": 0}, "cop",
                           meta={"github_repo": "x"})
    assert r["cop_score"] == 0 and r["thief_score"] == 0 and r["github_repo"] == "x"
