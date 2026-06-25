"""Tests for partial observation."""

from marl_cop_thief.services.observation import observe
from marl_cop_thief.shared.constants import Role
from marl_cop_thief.shared.models import GameState, Position


def test_opponent_visible_within_radius():
    s = GameState(5, 5, Position(2, 2), Position(3, 3))
    obs = observe(s, Role.COP, visibility_radius=1)
    assert obs.opponent_pos == Position(3, 3)
    assert obs.to_dict()["opponent"] == [3, 3]


def test_opponent_hidden_outside_radius():
    s = GameState(5, 5, Position(0, 0), Position(4, 4))
    obs = observe(s, Role.COP, visibility_radius=1)
    assert obs.opponent_pos is None
    assert obs.to_dict()["opponent"] is None


def test_visible_cells_clipped_to_board():
    s = GameState(5, 5, Position(0, 0), Position(4, 4))
    obs = observe(s, Role.COP, visibility_radius=1)
    # corner (0,0) with radius 1 -> 2x2 in-bounds window = 4 cells
    assert len(obs.visible_cells) == 4
    assert Position(0, 0) in obs.visible_cells


def test_visible_barriers_reported():
    s = GameState(5, 5, Position(2, 2), Position(0, 0), barriers={Position(2, 3), Position(0, 0)})
    obs = observe(s, Role.COP, visibility_radius=1)
    assert Position(2, 3) in obs.visible_barriers
    assert Position(0, 0) not in obs.visible_barriers  # out of view


def test_thief_role_sees_self_as_thief():
    s = GameState(5, 5, Position(1, 1), Position(2, 2))
    obs = observe(s, Role.THIEF, visibility_radius=2)
    assert obs.self_pos == Position(2, 2)
    assert obs.to_dict()["role"] == "thief"
