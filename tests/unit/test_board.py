"""Tests for board geometry and passability."""

from marl_cop_thief.services.board import Board, passable
from marl_cop_thief.shared.models import Position


def test_in_bounds():
    b = Board(5, 5)
    assert b.in_bounds(Position(0, 0))
    assert b.in_bounds(Position(4, 4))
    assert not b.in_bounds(Position(5, 0))
    assert not b.in_bounds(Position(-1, 0))


def test_all_cells_count_non_square():
    assert len(list(Board(3, 2).all_cells())) == 6


def test_neighbors_corner_and_center():
    b = Board(5, 5)
    assert len(b.neighbors(Position(0, 0))) == 3
    assert len(b.neighbors(Position(2, 2))) == 8


def test_passable_blocks_barriers_and_out_of_bounds():
    b = Board(3, 3)
    barriers = {Position(1, 1)}
    assert passable(b, barriers, Position(0, 0))
    assert not passable(b, barriers, Position(1, 1))
    assert not passable(b, barriers, Position(3, 3))
