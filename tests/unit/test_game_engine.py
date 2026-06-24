"""Tests for the authoritative game engine."""

import random

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.shared.constants import ActionKind, Event, Role
from marl_cop_thief.shared.models import Action, GameState, Position


def _engine(max_moves: int = 25, max_barriers: int = 5) -> GameEngine:
    return GameEngine(5, 5, max_moves, max_barriers)


def test_new_state_deterministic_and_distinct():
    e = _engine()
    s1 = e.new_state(random.Random(42))
    s2 = e.new_state(random.Random(42))
    assert s1.cop == s2.cop and s1.thief == s2.thief
    assert s1.cop != s1.thief


def test_legal_actions_corner_thief():
    e = _engine()
    s = GameState(5, 5, Position(4, 4), Position(0, 0))  # thief at corner, thief to move
    acts = e.legal_actions(s)
    assert Action.stay() in acts
    assert sum(1 for a in acts if a.kind is ActionKind.MOVE) == 3


def test_cop_barrier_action_depends_on_budget():
    e = _engine()
    s = GameState(5, 5, Position(2, 2), Position(0, 0), to_move=Role.COP)
    assert any(a.kind is ActionKind.PLACE_BARRIER for a in e.legal_actions(s))
    s.cop_barriers_used = 5
    assert not any(a.kind is ActionKind.PLACE_BARRIER for a in e.legal_actions(s))


def test_move_updates_position_and_alternates_turn():
    e = _engine()
    s = GameState(5, 5, Position(0, 0), Position(2, 2))  # thief first
    r = e.apply(s, Action.move(1, 0))
    assert s.thief == Position(3, 2)
    assert r.event is Event.NONE
    assert s.to_move is Role.COP
    assert s.moves_used == 1


def test_illegal_off_board_leaves_state_unchanged():
    e = _engine()
    s = GameState(5, 5, Position(3, 3), Position(0, 0))
    r = e.apply(s, Action.move(-1, 0))
    assert r.event is Event.ILLEGAL
    assert s.thief == Position(0, 0)
    assert s.moves_used == 0
    assert s.to_move is Role.THIEF


def test_illegal_move_into_barrier():
    e = _engine()
    s = GameState(5, 5, Position(3, 3), Position(0, 0), barriers={Position(1, 0)})
    assert e.apply(s, Action.move(1, 0)).event is Event.ILLEGAL


def test_illegal_non_unit_move():
    e = _engine()
    s = GameState(5, 5, Position(3, 3), Position(0, 0))
    assert e.apply(s, Action.move(2, 0)).event is Event.ILLEGAL


def test_capture_cop_onto_thief():
    e = _engine()
    s = GameState(5, 5, Position(1, 1), Position(2, 2), to_move=Role.COP)
    r = e.apply(s, Action.move(1, 1))
    assert r.event is Event.CAPTURE
    assert s.winner is Role.COP and s.done


def test_capture_thief_onto_cop():
    e = _engine()
    s = GameState(5, 5, Position(1, 1), Position(2, 2))  # thief to move
    r = e.apply(s, Action.move(-1, -1))
    assert r.event is Event.CAPTURE
    assert s.winner is Role.COP


def test_timeout_thief_wins():
    e = _engine(max_moves=2)
    s = GameState(5, 5, Position(0, 0), Position(4, 4))
    e.apply(s, Action.stay())  # thief, moves=1
    r = e.apply(s, Action.stay())  # cop, moves=2 -> reached
    assert r.event is Event.MAX_MOVES_REACHED
    assert s.winner is Role.THIEF and s.done


def test_barrier_placed_then_thief_cannot_place():
    e = _engine(max_barriers=1)
    s = GameState(5, 5, Position(2, 2), Position(0, 0), to_move=Role.COP)
    r = e.apply(s, Action.place_barrier())
    assert r.event is Event.BARRIER_PLACED
    assert Position(2, 2) in s.barriers and s.cop_barriers_used == 1
    assert e.apply(s, Action.place_barrier()).event is Event.ILLEGAL  # thief's turn now


def test_barrier_over_limit_is_illegal():
    e = _engine(max_barriers=0)
    s = GameState(5, 5, Position(2, 2), Position(0, 0), to_move=Role.COP)
    assert e.apply(s, Action.place_barrier()).event is Event.ILLEGAL


def test_apply_after_done_is_illegal():
    e = _engine(max_moves=1)
    s = GameState(5, 5, Position(0, 0), Position(4, 4))
    e.apply(s, Action.stay())  # moves=1 -> thief wins
    assert e.apply(s, Action.stay()).event is Event.ILLEGAL
