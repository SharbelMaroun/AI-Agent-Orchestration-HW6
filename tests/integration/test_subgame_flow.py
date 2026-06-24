"""Integration: drive a full sub-game through the engine and score it."""

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.scoring import score_subgame
from marl_cop_thief.shared.constants import Event, Role
from marl_cop_thief.shared.models import Action, GameState, Position

SCORING = {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5}


def test_full_subgame_capture_and_score():
    e = GameEngine(5, 5, 25, 5)
    s = GameState(5, 5, Position(0, 0), Position(1, 1))  # thief first
    e.apply(s, Action.stay())  # thief stays
    r = e.apply(s, Action.move(1, 1))  # cop (0,0) -> (1,1) captures
    assert r.event is Event.CAPTURE and s.winner is Role.COP
    res = score_subgame(0, s.winner, s.moves_used, SCORING)
    assert (res.cop_score, res.thief_score) == (20, 5)


def test_full_subgame_timeout_and_score():
    e = GameEngine(5, 5, 4, 5)
    s = GameState(5, 5, Position(0, 0), Position(4, 4))
    for _ in range(4):
        e.apply(s, Action.stay())
    assert s.winner is Role.THIEF and s.done
    res = score_subgame(1, s.winner, s.moves_used, SCORING)
    assert (res.cop_score, res.thief_score) == (5, 10)
