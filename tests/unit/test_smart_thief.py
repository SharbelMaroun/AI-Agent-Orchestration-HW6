"""Tests for the smart thief evasion policy + shared evasion scoring."""

import random

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.strategy.evasion import center_distance, evade_key, mobility
from marl_cop_thief.services.strategy.geometry import chebyshev
from marl_cop_thief.services.strategy.heuristic import cop_action
from marl_cop_thief.services.strategy.smart_thief import smart_thief_action
from marl_cop_thief.services.turn_pipeline import run_turn
from marl_cop_thief.shared.constants import ActionKind, Role
from marl_cop_thief.shared.models import GameState, Position


def test_mobility_counts_open_neighbours():
    board = GameEngine(5, 5, 25, 5).board
    assert mobility(board, set(), Position(2, 2)) == 8  # centre: all 8 open
    assert mobility(board, set(), Position(0, 0)) == 3  # corner: only 3 in-bounds
    assert mobility(board, {Position(2, 3)}, Position(2, 2)) == 7  # one neighbour blocked


def test_center_distance():
    board = GameEngine(5, 5, 25, 5).board
    assert center_distance(Position(2, 2), board) == 0
    assert center_distance(Position(0, 0), board) == 2


def test_evade_key_records_distance_then_mobility_then_centrality():
    board = GameEngine(5, 5, 25, 5).board
    key = evade_key(board, set(), Position(2, 2), Position(0, 0))
    assert key == (2, 8, 0)  # (dist-from-cop, mobility, -center_distance)


def test_smart_thief_increases_distance_from_cop():
    e = GameEngine(5, 5, 25, 5)
    s = GameState(5, 5, Position(2, 2), Position(1, 1))  # thief to move
    a = smart_thief_action(e, s)
    new = s.thief.step(a.dx, a.dy)
    assert a.kind is ActionKind.MOVE and chebyshev(new, s.cop) >= chebyshev(s.thief, s.cop)


def test_smart_thief_uses_interior_not_just_one_wall():
    # greedy evasion hugs the top/left wall from this start; smart evasion ventures inside.
    e = GameEngine(5, 5, 25, 5)
    s = e.new_state(random.Random(42))
    path = [s.thief]
    for _ in range(12):
        if s.done:
            break
        run_turn(e, s, {Role.COP: cop_action, Role.THIEF: smart_thief_action})
        path.append(s.thief)
    assert any(0 < p.x < 4 and 0 < p.y < 4 for p in path)  # reaches an open interior cell


def test_smart_thief_stays_when_boxed_in():
    e = GameEngine(5, 5, 25, 5)
    barriers = {Position(1, 0), Position(0, 1), Position(1, 1)}
    s = GameState(5, 5, Position(3, 3), Position(0, 0), barriers=barriers)
    assert smart_thief_action(e, s).kind is ActionKind.STAY


def test_smart_thief_is_deterministic():
    e = GameEngine(5, 5, 25, 5)
    s = GameState(5, 5, Position(0, 0), Position(3, 3))
    assert smart_thief_action(e, s) == smart_thief_action(e, s)
