"""Tests for the heuristic deciders."""

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.strategy.heuristic import cop_action, thief_action
from marl_cop_thief.shared.constants import ActionKind, Role
from marl_cop_thief.shared.models import GameState, Position


def _chebyshev(a: Position, b: Position) -> int:
    return max(abs(a.x - b.x), abs(a.y - b.y))


def test_cop_steps_toward_thief():
    e = GameEngine(5, 5, 25, 5)
    s = GameState(5, 5, Position(0, 0), Position(4, 4), to_move=Role.COP)
    a = cop_action(e, s)
    assert a.kind is ActionKind.MOVE
    new = s.cop.step(a.dx, a.dy)
    assert _chebyshev(new, s.thief) < _chebyshev(s.cop, s.thief)


def test_thief_steps_away_from_cop():
    e = GameEngine(5, 5, 25, 5)
    s = GameState(5, 5, Position(2, 2), Position(1, 1))  # thief to move
    a = thief_action(e, s)
    assert a.kind is ActionKind.MOVE
    new = s.thief.step(a.dx, a.dy)
    assert _chebyshev(new, s.cop) >= _chebyshev(s.thief, s.cop)


def test_thief_stays_when_boxed_in():
    e = GameEngine(5, 5, 25, 5)
    barriers = {Position(1, 0), Position(0, 1), Position(1, 1)}
    s = GameState(5, 5, Position(3, 3), Position(0, 0), barriers=barriers)
    assert thief_action(e, s).kind is ActionKind.STAY


def test_cop_stays_when_boxed_in():
    e = GameEngine(5, 5, 25, 5)
    barriers = {Position(1, 0), Position(0, 1), Position(1, 1)}
    s = GameState(5, 5, Position(0, 0), Position(4, 4), barriers=barriers, to_move=Role.COP)
    assert cop_action(e, s).kind is ActionKind.STAY
