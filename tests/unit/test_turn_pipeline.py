"""Tests for the single-turn pipeline."""

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.turn_pipeline import run_turn
from marl_cop_thief.shared.constants import Event, Role
from marl_cop_thief.shared.models import Action, GameState, Position


def test_run_turn_applies_action_and_advances():
    e = GameEngine(5, 5, 25, 5)
    s = GameState(5, 5, Position(0, 0), Position(2, 2))  # thief to move
    deciders = {Role.THIEF: lambda _e, _s: Action.move(1, 0), Role.COP: lambda _e, _s: Action.stay()}
    result = run_turn(e, s, deciders)
    assert result.event is Event.NONE
    assert s.thief == Position(3, 2)
    assert s.moves_used == 1


def test_run_turn_falls_back_to_stay_on_illegal():
    e = GameEngine(5, 5, 25, 5)
    s = GameState(5, 5, Position(3, 3), Position(0, 0))  # cop far from thief
    # thief decider returns an illegal off-board move -> pipeline falls back to STAY
    deciders = {
        Role.THIEF: lambda _e, _s: Action.move(-1, 0),
        Role.COP: lambda _e, _s: Action.stay(),
    }
    result = run_turn(e, s, deciders)
    assert result.event is Event.NONE  # STAY succeeded
    assert s.moves_used == 1
    assert s.thief == Position(0, 0)
