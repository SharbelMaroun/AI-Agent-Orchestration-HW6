"""Tests for domain models."""

from marl_cop_thief.shared.constants import ActionKind
from marl_cop_thief.shared.models import Action, Position


def test_position_step():
    assert Position(1, 1).step(1, -1) == Position(2, 0)


def test_position_is_frozen_hashable():
    assert len({Position(0, 0), Position(0, 0)}) == 1


def test_action_factories():
    assert Action.move(1, 0).kind is ActionKind.MOVE
    assert Action.stay().kind is ActionKind.STAY
    assert Action.place_barrier().kind is ActionKind.PLACE_BARRIER
    a = Action.move(-1, 1)
    assert (a.dx, a.dy) == (-1, 1)
