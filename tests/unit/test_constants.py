"""Tests for shared constants and enums."""

from marl_cop_thief.shared.constants import DIRECTIONS_8, ActionKind, Event, Role


def test_eight_directions_excludes_noop():
    assert len(DIRECTIONS_8) == 8
    assert (0, 0) not in DIRECTIONS_8
    assert len(set(DIRECTIONS_8)) == 8


def test_directions_are_unit_steps():
    for dx, dy in DIRECTIONS_8:
        assert dx in (-1, 0, 1)
        assert dy in (-1, 0, 1)


def test_enum_values():
    assert Role.COP.value == "cop"
    assert Role.THIEF.value == "thief"
    assert ActionKind.MOVE.value == "move"
    assert ActionKind.PLACE_BARRIER.value == "place_barrier"
    assert Event.CAPTURE.value == "capture"
    assert Event.MAX_MOVES_REACHED.value == "max_moves_reached"
