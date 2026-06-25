"""Tests for the natural-language decider."""

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.mcp.message_bus import MessageBus
from marl_cop_thief.services.nl_protocol.nl_decider import NLDecider
from marl_cop_thief.shared.constants import ActionKind, Role
from marl_cop_thief.shared.models import GameState, Position


class _LLM:
    def complete(self, prompt: str) -> str:
        return "unknown"


def test_decider_returns_legal_action_and_sends_message():
    engine = GameEngine(5, 5, 25, 5)
    state = GameState(5, 5, Position(0, 0), Position(2, 2))  # thief to move
    bus = MessageBus()
    decider = NLDecider(Role.THIEF, bus, _LLM(), visibility_radius=1)
    action = decider(engine, state)
    assert action in engine.legal_actions(state)
    assert bus.pending(Role.COP) == 1  # thief messaged the cop


def test_decider_updates_belief_from_direct_observation():
    engine = GameEngine(5, 5, 25, 5)
    state = GameState(5, 5, Position(2, 2), Position(2, 3), to_move=Role.COP)  # adjacent
    decider = NLDecider(Role.COP, MessageBus(), _LLM(), visibility_radius=1)
    decider(engine, state)
    assert decider.belief == Position(2, 3)  # saw the thief directly


def test_decider_stays_when_no_moves():
    engine = GameEngine(5, 5, 25, 5)
    barriers = {Position(1, 0), Position(0, 1), Position(1, 1)}
    state = GameState(5, 5, Position(0, 0), Position(4, 4), barriers=barriers, to_move=Role.COP)
    decider = NLDecider(Role.COP, MessageBus(), _LLM(), visibility_radius=1)
    assert decider(engine, state).kind is ActionKind.STAY
