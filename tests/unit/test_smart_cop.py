"""Tests for the cornering (smart) cop policy."""

import random

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.strategy.heuristic import thief_action
from marl_cop_thief.services.strategy.smart_cop import smart_cop_action
from marl_cop_thief.services.turn_pipeline import run_turn
from marl_cop_thief.shared.constants import ActionKind, Role
from marl_cop_thief.shared.models import GameState, Position


def _play(n: int, seed: int, max_moves: int = 25) -> GameState:
    engine = GameEngine(n, n, max_moves, 5)
    state = engine.new_state(random.Random(seed))
    deciders = {Role.COP: smart_cop_action, Role.THIEF: thief_action}
    while not state.done:
        run_turn(engine, state, deciders)
    return state


def test_takes_the_immediate_capture_when_available():
    e = GameEngine(5, 5, 25, 5)
    s = GameState(5, 5, Position(2, 2), Position(3, 3), to_move=Role.COP)
    e.apply(s, smart_cop_action(e, s))  # should step onto the thief
    assert s.done and s.winner is Role.COP


def test_captures_on_open_board_where_greedy_would_cycle():
    state = _play(5, 3)
    assert state.winner is Role.COP
    assert state.moves_used < 25  # caught before the move cap, not a timeout


def test_corners_thief_on_every_sampled_seed():
    assert all(_play(5, seed).winner is Role.COP for seed in range(15))


def test_stays_when_boxed_in():
    e = GameEngine(5, 5, 25, 5)
    barriers = {Position(1, 0), Position(0, 1), Position(1, 1)}
    s = GameState(5, 5, Position(0, 0), Position(4, 4), barriers=barriers, to_move=Role.COP)
    assert smart_cop_action(e, s).kind is ActionKind.STAY


def test_is_deterministic_for_the_same_state():
    e = GameEngine(6, 6, 25, 5)
    s = GameState(6, 6, Position(1, 1), Position(4, 4), to_move=Role.COP)
    assert smart_cop_action(e, s) == smart_cop_action(e, s)
