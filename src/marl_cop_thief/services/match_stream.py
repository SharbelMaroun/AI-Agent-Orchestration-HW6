"""Per-turn frame streams for the GUI (one ``(state, caption)`` per turn).

A *stream* yields a deepcopied snapshot before the first move and again after
every turn, so the live window can render each turn the instant the engine
computes it (genuinely real-time) while the GIF animator simply collects the
stream into a list. The single engine loop lives in :func:`stream_subgame`
(DRY); the natural-language stream in ``nl_match`` reuses it. All game logic
stays in this service layer — the GUI only renders frames (SDK-only).
"""

from __future__ import annotations

import copy
import random
from collections.abc import Callable, Iterator
from typing import Any

from ..shared.constants import Role
from ..shared.models import GameState
from .game_engine import GameEngine
from .orchestrator import select_cop_policy, select_thief_policy
from .turn_pipeline import Decider, run_turn

Frame = tuple[GameState, str]
Caption = Callable[[Role], str]


def stream_subgame(
    engine: GameEngine, state: GameState, deciders: dict[Role, Decider], caption: Caption
) -> Iterator[Frame]:
    """Yield the pre-move snapshot, then one snapshot + caption after every turn."""
    yield (copy.deepcopy(state), "")
    while not state.done:
        actor = state.to_move
        run_turn(engine, state, deciders)
        yield (copy.deepcopy(state), caption(actor))


def heuristic_subgame_stream(config: dict[str, Any]) -> Iterator[Frame]:
    """Stream a heuristic/smart sub-game (cop policy from config); no spoken messages."""
    width, height = config["grid_size"]
    engine = GameEngine(width, height, config["max_moves"], config["max_barriers"])
    state = engine.new_state(random.Random(config.get("seed", 0)))
    deciders: dict[Role, Decider] = {
        Role.COP: select_cop_policy(config),
        Role.THIEF: select_thief_policy(config),
    }
    yield from stream_subgame(engine, state, deciders, lambda _actor: "")
