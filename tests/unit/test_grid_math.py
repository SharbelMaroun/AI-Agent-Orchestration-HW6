"""Tests for the shared tuple-based grid-distance helpers."""

from marl_cop_thief.shared.grid_math import chebyshev, manhattan


def test_chebyshev_is_max_axis_delta():
    assert chebyshev(0, 0, 3, 1) == 3
    assert chebyshev(2, 2, 2, 2) == 0


def test_manhattan_is_sum_of_abs_deltas():
    assert manhattan(0, 0, 3, 1) == 4
    assert manhattan(1, 5, 1, 2) == 3
