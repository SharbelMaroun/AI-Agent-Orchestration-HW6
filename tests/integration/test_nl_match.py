"""Integration: two NL agents coordinate over the bus, via an LLM-through-gatekeeper.

Uses a deterministic fake backend (no network): it echoes the prompt, so an
agent's interpret() recovers any coordinates the opponent revealed in its message.
"""

import random

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.mcp.message_bus import MessageBus
from marl_cop_thief.services.nl_protocol.nl_decider import NLDecider
from marl_cop_thief.services.turn_pipeline import run_turn
from marl_cop_thief.shared.constants import Role
from marl_cop_thief.shared.gatekeeper import ApiGatekeeper
from marl_cop_thief.shared.llm_client import GatekeptLLM


def test_nl_subgame_completes_and_uses_gatekeeper():
    engine = GameEngine(5, 5, 25, 5)
    state = engine.new_state(random.Random(5))
    bus = MessageBus()
    gk = ApiGatekeeper()
    llm = GatekeptLLM(backend=lambda prompt: prompt, gatekeeper=gk)  # echo backend
    deciders = {
        Role.COP: NLDecider(Role.COP, bus, llm, visibility_radius=1),
        Role.THIEF: NLDecider(Role.THIEF, bus, llm, visibility_radius=1),
    }

    while not state.done:
        run_turn(engine, state, deciders)

    assert state.done
    assert state.winner in (Role.COP, Role.THIEF)
    assert state.moves_used <= 25
    assert gk.calls > 0  # the LLM was consulted via the gatekeeper
