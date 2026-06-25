"""Tests for the shared Chebyshev distance helper."""

from marl_cop_thief.services.strategy.geometry import chebyshev
from marl_cop_thief.shared.models import Position


def test_chebyshev_is_max_of_axis_deltas():
    assert chebyshev(Position(0, 0), Position(3, 3)) == 3  # diagonal
    assert chebyshev(Position(0, 0), Position(0, 4)) == 4  # vertical
    assert chebyshev(Position(1, 1), Position(4, 2)) == 3  # max(3, 1)


def test_chebyshev_is_zero_for_same_cell():
    assert chebyshev(Position(2, 2), Position(2, 2)) == 0


def test_chebyshev_is_symmetric():
    a, b = Position(1, 4), Position(3, 0)
    assert chebyshev(a, b) == chebyshev(b, a)
