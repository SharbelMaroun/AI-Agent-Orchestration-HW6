"""Tests for barrier rules."""

from marl_cop_thief.services.barriers import can_place, place
from marl_cop_thief.shared.models import GameState, Position


def _state() -> GameState:
    return GameState(5, 5, Position(2, 2), Position(0, 0))


def test_can_place_respects_budget():
    s = _state()
    assert can_place(s, 5)
    s.cop_barriers_used = 5
    assert not can_place(s, 5)


def test_place_adds_barrier_and_counts():
    s = _state()
    place(s)
    assert Position(2, 2) in s.barriers
    assert s.cop_barriers_used == 1
