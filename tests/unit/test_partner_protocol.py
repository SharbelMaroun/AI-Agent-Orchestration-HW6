"""Tests for the partner decision-protocol mapping (pure)."""

import pytest

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.partner_protocol import (
    from_partner_action,
    legal_partner_actions,
    to_partner_observation,
)
from marl_cop_thief.shared.constants import ActionKind, Role
from marl_cop_thief.shared.models import GameState, Position


def _engine_state(cop=(2, 2), thief=(2, 3), to_move=Role.COP):
    engine = GameEngine(5, 5, 25, 5)
    state = GameState(5, 5, Position(*cop), Position(*thief), to_move=to_move)
    return engine, state


def test_observation_maps_coords_to_row_col():
    engine, state = _engine_state(cop=(1, 2), thief=(2, 3))
    obs = to_partner_observation(engine, state, Role.COP, visibility_radius=9, request_id="rid")
    assert obs["request_id"] == "rid" and obs["role"] == "cop"
    assert obs["self_position"] == [2, 1]  # [row=y, col=x]
    assert obs["visible_opponent"] == [3, 2]
    assert obs["grid_size"] == [5, 5] and obs["max_moves"] == 25


def test_observation_hides_opponent_out_of_range():
    engine, state = _engine_state(cop=(0, 0), thief=(4, 4))
    obs = to_partner_observation(engine, state, Role.COP, visibility_radius=1, request_id="r")
    assert obs["visible_opponent"] is None


def test_legal_actions_orthogonal_no_barrier_by_default():
    engine, state = _engine_state(cop=(2, 2), to_move=Role.COP)
    acts = legal_partner_actions(engine, state)  # allow_barrier defaults False
    dirs = {a["direction"] for a in acts if a["type"] == "move"}
    assert dirs == {"up", "down", "left", "right"}  # no diagonals
    assert not any(a["type"] == "place_barrier" for a in acts)  # off (partner 500s on it)


def test_legal_actions_includes_barrier_when_allowed():
    engine, state = _engine_state(cop=(2, 2), to_move=Role.COP)
    acts = legal_partner_actions(engine, state, allow_barrier=True)
    barrier = [a for a in acts if a["type"] == "place_barrier"]
    assert barrier and barrier[0]["target"] == [2, 2]


def test_legal_actions_thief_has_no_barrier():
    engine, state = _engine_state(to_move=Role.THIEF)
    assert all(a["type"] == "move" for a in legal_partner_actions(engine, state))


def test_from_partner_action_directions():
    assert from_partner_action({"type": "move", "direction": "right"}) == \
        from_partner_action({"type": "move", "direction": "right"})
    act = from_partner_action({"type": "move", "direction": "down"})
    assert act.kind is ActionKind.MOVE and (act.dx, act.dy) == (0, 1)
    assert from_partner_action({"type": "place_barrier", "target": [1, 1]}).kind is ActionKind.PLACE_BARRIER


def test_from_partner_action_rejects_unknown_direction():
    with pytest.raises(ValueError, match="unknown partner direction"):
        from_partner_action({"type": "move", "direction": "north"})
