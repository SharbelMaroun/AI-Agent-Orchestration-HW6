"""Tests for the stateless /decide decision logic."""

from marl_cop_thief.services.decide_service import decide_action

_MOVES = [{"type": "move", "direction": d} for d in ("up", "down", "left", "right")]


def _obs(role, self_pos, opp, legal=None, grid=(5, 5)):
    return {
        "role": role, "self_position": list(self_pos),
        "visible_opponent": (list(opp) if opp else None),
        "grid_size": list(grid), "legal_actions": _MOVES if legal is None else legal,
    }


def test_cop_moves_toward_opponent():
    # opp two columns right (col+2) -> "right" cuts Manhattan distance most
    assert decide_action(_obs("cop", (2, 2), (2, 4))) == {"type": "move", "direction": "right"}


def test_thief_moves_away_from_opponent():
    # opp directly above (row 0) -> flee downward (row+1)
    assert decide_action(_obs("thief", (2, 2), (0, 2))) == {"type": "move", "direction": "down"}


def test_blind_returns_a_legal_move_toward_center():
    legal = [{"type": "move", "direction": "down"}, {"type": "move", "direction": "right"}]
    assert decide_action(_obs("cop", (0, 0), None, legal=legal)) in legal


def test_no_move_actions_returns_first_legal():
    barrier = {"type": "place_barrier", "target": [1, 1]}
    assert decide_action(_obs("cop", (1, 1), (2, 2), legal=[barrier])) == barrier


def test_empty_legal_returns_safe_default_move():
    assert decide_action(_obs("cop", (1, 1), (2, 2), legal=[]))["type"] == "move"
