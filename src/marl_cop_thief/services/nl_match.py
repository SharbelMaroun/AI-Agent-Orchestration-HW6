"""Runnable natural-language match: two NL agents coordinate over the MCP bus.

Mirrors the heuristic orchestrator but wires up the NL stack — a per-sub-game
:class:`MessageBus`, an :class:`ApiGatekeeper`, a gatekept LLM, and an
:class:`NLDecider` for each role. The backend defaults to an offline echo so the
match runs deterministically with no network or external services.
"""

from __future__ import annotations

import random
from collections.abc import Callable, Iterator
from typing import Any

from ..shared.constants import Role
from ..shared.gatekeeper import ApiGatekeeper
from ..shared.llm_client import GatekeptLLM
from .accumulator import summarize
from .game_engine import GameEngine
from .match_stream import Frame, stream_subgame
from .mcp.message_bus import MessageBus
from .nl_protocol.nl_decider import NLDecider
from .scoring import score_subgame
from .turn_pipeline import run_turn


def _echo(prompt: str) -> str:
    """Offline default backend: echo the prompt back (no network)."""
    return prompt


def _make_llm(
    backend: Callable[[str], str] | None, gatekeeper: ApiGatekeeper | None
) -> GatekeptLLM:
    """Build the gatekept LLM, defaulting to the offline echo + an unlimited gatekeeper."""
    return GatekeptLLM(backend or _echo, gatekeeper or ApiGatekeeper())


def _nl_deciders(bus: MessageBus, llm: GatekeptLLM, visibility_radius: int) -> dict[Role, NLDecider]:
    """Construct an NL decider for each role, sharing one bus + LLM."""
    return {
        Role.COP: NLDecider(Role.COP, bus, llm, visibility_radius),
        Role.THIEF: NLDecider(Role.THIEF, bus, llm, visibility_radius),
    }


def run_nl_match(
    config: dict[str, Any],
    backend: Callable[[str], str] | None = None,
    gatekeeper: ApiGatekeeper | None = None,
) -> dict[str, Any]:
    """Run ``num_games`` NL sub-games to completion and return the summary.

    The LLM routes through one shared ``gatekeeper`` for the whole match, so any
    configured rate limit spans every sub-game; the default is unlimited, keeping
    offline runs fast. The CLI injects a config-driven gatekeeper for real runs.
    """
    width, height = config["grid_size"]
    engine = GameEngine(width, height, config["max_moves"], config["max_barriers"])
    visibility_radius = config["visibility_radius"]
    scoring = config["scoring"]
    num_games = config["num_games"]
    seed = config.get("seed", 0)
    llm = _make_llm(backend, gatekeeper)

    results = []
    for i in range(num_games):
        bus = MessageBus()
        deciders = _nl_deciders(bus, llm, visibility_radius)
        state = engine.new_state(random.Random(seed + i))
        while not state.done:
            run_turn(engine, state, deciders)
        results.append(score_subgame(i, state.winner, state.moves_used, scoring))
    return summarize(results)


def nl_subgame_stream(
    config: dict[str, Any],
    backend: Callable[[str], str] | None = None,
    gatekeeper: ApiGatekeeper | None = None,
    seed: int | None = None,
) -> Iterator[Frame]:
    """Stream one NL sub-game as per-turn ``(state, spoken message)`` frames.

    Reuses the shared :func:`stream_subgame` engine loop (DRY); the caption reads
    the message the acting role just spoke off the bus, so the live window shows
    the agents *talking* as they move.
    """
    width, height = config["grid_size"]
    engine = GameEngine(width, height, config["max_moves"], config["max_barriers"])
    if seed is None:
        seed = config.get("seed", 0)
    bus = MessageBus()
    deciders = _nl_deciders(bus, _make_llm(backend, gatekeeper), config["visibility_radius"])
    state = engine.new_state(random.Random(seed))

    def caption(actor: Role) -> str:
        opponent = Role.THIEF if actor is Role.COP else Role.COP
        spoken = bus.peek_last(opponent)  # the actor always speaks each turn, so never None
        return f"{actor.value}: {spoken.text}"  # type: ignore[union-attr]

    yield from stream_subgame(engine, state, deciders, caption)


def nl_subgame_frames(
    config: dict[str, Any],
    backend: Callable[[str], str] | None = None,
    gatekeeper: ApiGatekeeper | None = None,
    seed: int | None = None,
) -> list[Frame]:
    """Play one NL sub-game, returning per-turn ``(state, spoken message)`` for the GUI."""
    return list(nl_subgame_stream(config, backend, gatekeeper, seed))
