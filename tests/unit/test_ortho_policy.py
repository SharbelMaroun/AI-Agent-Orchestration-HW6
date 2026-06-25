"""Tests for the 4-directional interop policy."""

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.strategy.ortho_policy import ortho_action
from marl_cop_thief.shared.constants import ActionKind, Role
from marl_cop_thief.shared.models import GameState, Position


def _state(cop, thief, to_move):
    return GameState(5, 5, Position(*cop), Position(*thief), to_move=to_move)


def _cheb(a, b):
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def test_cop_moves_closer_to_thief():
    engine = GameEngine(5, 5, 25, 5)
    state = _state((0, 0), (4, 0), Role.COP)
    act = ortho_action(engine, state)
    assert act.kind is ActionKind.MOVE
    new_cop = (state.cop.x + act.dx, state.cop.y + act.dy)
    assert _cheb(new_cop, (4, 0)) < _cheb((0, 0), (4, 0))  # closed distance


def test_thief_moves_away_from_cop():
    engine = GameEngine(5, 5, 25, 5)
    state = _state((2, 2), (2, 1), Role.THIEF)  # cop just below thief
    act = ortho_action(engine, state)
    new_thief = (state.thief.x + act.dx, state.thief.y + act.dy)
    assert _cheb(new_thief, (2, 2)) >= _cheb((2, 1), (2, 2))  # not closer to cop


def test_surrounded_actor_stays():
    engine = GameEngine(5, 5, 25, 5)
    # thief at a corner with the two orthogonal neighbours blocked by barriers
    state = _state((0, 0), (4, 4), Role.THIEF)
    state.thief = Position(0, 0)
    state.barriers = {Position(1, 0), Position(0, 1)}
    assert ortho_action(engine, state).kind is ActionKind.STAY
