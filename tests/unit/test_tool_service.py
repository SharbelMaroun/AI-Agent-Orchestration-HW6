"""Tests for the MCP tool service (turn-ownership, observation, status)."""

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.mcp.message_bus import MessageBus
from marl_cop_thief.services.mcp.tools import ToolService
from marl_cop_thief.shared.constants import Event, Role
from marl_cop_thief.shared.models import Action, GameState, Position


def _tools(state: GameState) -> ToolService:
    engine = GameEngine(5, 5, 25, 5)
    return ToolService(engine, state, MessageBus(), visibility_radius=1, max_barriers=5)


def test_get_observation_shape():
    t = _tools(GameState(5, 5, Position(2, 2), Position(2, 3)))
    obs = t.get_observation(Role.COP)
    assert obs["self"] == [2, 2]
    assert obs["opponent"] == [2, 3]


def test_send_and_receive_message():
    t = _tools(GameState(5, 5, Position(0, 0), Position(4, 4)))
    assert t.send_message(Role.COP, "hello")["ok"] is True
    assert t.receive_message(Role.THIEF) == {"sender": "cop", "text": "hello"}
    assert t.receive_message(Role.THIEF) is None


def test_submit_action_rejects_out_of_turn():
    t = _tools(GameState(5, 5, Position(0, 0), Position(4, 4)))  # thief to move
    res = t.submit_action(Role.COP, Action.stay())
    assert res["event"] == Event.ILLEGAL.value
    assert res["reason"] == "not your turn"


def test_submit_action_legal_advances():
    t = _tools(GameState(5, 5, Position(0, 0), Position(2, 2)))  # thief to move
    res = t.submit_action(Role.THIEF, Action.move(1, 0))
    assert res["event"] == Event.NONE.value
    assert t.state.thief == Position(3, 2)


def test_submit_action_rejected_when_done():
    state = GameState(5, 5, Position(0, 0), Position(4, 4))
    t = _tools(state)
    state.done = True
    res = t.submit_action(Role.THIEF, Action.stay())
    assert res["event"] == Event.ILLEGAL.value
    assert res["reason"] == "game over"


def test_verify_location_is_authoritative():
    t = _tools(GameState(5, 5, Position(1, 4), Position(0, 0)))
    assert t.verify_location(Role.COP) == {"x": 1, "y": 4}


def test_game_status_fields():
    t = _tools(GameState(5, 5, Position(0, 0), Position(4, 4)))
    status = t.get_game_status()
    assert status["to_move"] == "thief"
    assert status["moves_left"] == 25
    assert status["barriers_left"] == 5
    assert status["done"] is False
    assert status["winner"] is None
