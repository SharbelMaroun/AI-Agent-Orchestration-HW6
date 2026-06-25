"""Tests for the cross-network match driver (fake MCP host client)."""

from marl_cop_thief.services.remote_match import play_my_turns, remote_decider


class _FakeHost:
    """Scripts get_game_status responses; records calls; canned obs + submit result."""

    def __init__(self, statuses, submit_result=None, opponent=(2, 2)):
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
            return {"self": [0, 0], "opponent": list(self.opponent) if self.opponent else None}
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


def test_remote_decider_directions():
    assert remote_decider("cop")({"self": [0, 0], "opponent": [3, 3]}) == ("move", 1, 1)  # toward
    assert remote_decider("thief")({"self": [2, 2], "opponent": [3, 3]}) == ("move", -1, -1)  # away
    assert remote_decider("cop")({"self": [1, 1], "opponent": None}) == ("stay", 0, 0)  # unseen
