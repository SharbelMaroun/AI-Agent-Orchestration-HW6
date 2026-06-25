"""Animate a sub-game to an animated GIF (real-time agent + barrier movement).

Two modes mirror the CLI: a **heuristic/smart** sub-game (``animate_match``, the
``--simple`` path, cop policy from ``config.strategy.type``) and the **natural-language**
sub-game (``animate_nl_match``, the default), which overlays each turn's NL message so
the GIF shows the agents *talking* as they move. Frames are ``(state, caption)`` pairs.
"""

from __future__ import annotations

import copy
import random
from collections.abc import Callable
from typing import Any

import matplotlib.pyplot as plt
from matplotlib import animation

from ..services.game_engine import GameEngine
from ..services.nl_match import nl_subgame_frames
from ..services.orchestrator import select_cop_policy
from ..services.strategy.heuristic import thief_action
from ..services.turn_pipeline import run_turn
from ..shared.constants import Role
from ..shared.gatekeeper import ApiGatekeeper
from .board_renderer import render_state

plt.switch_backend("Agg")

Frame = tuple[Any, str]


def _heuristic_frames(config: dict[str, Any]) -> list[Frame]:
    """Run a heuristic/smart sub-game (cop policy from config), snapshotting each turn."""
    width, height = config["grid_size"]
    engine = GameEngine(width, height, config["max_moves"], config["max_barriers"])
    state = engine.new_state(random.Random(config.get("seed", 0)))
    deciders = {Role.COP: select_cop_policy(config), Role.THIEF: thief_action}
    frames: list[Frame] = [(copy.deepcopy(state), "")]
    while not state.done:
        run_turn(engine, state, deciders)
        frames.append((copy.deepcopy(state), ""))
    return frames


def _animate(frames: list[Frame], path: str, fps: int) -> str:
    """Render ``(state, caption)`` frames to an animated GIF; return the output path."""
    fig, ax = plt.subplots(figsize=(5, 5.5))
    anim = animation.FuncAnimation(
        fig, lambda i: render_state(frames[i][0], ax, frames[i][1]), frames=len(frames), interval=400
    )
    fig.tight_layout()
    anim.save(path, writer=animation.PillowWriter(fps=fps))
    plt.close(fig)
    return path


def animate_match(config: dict[str, Any], path: str = "assets/match.gif", fps: int = 2) -> str:
    """Render a heuristic/smart sub-game as an animated GIF (the ``--simple`` path)."""
    return _animate(_heuristic_frames(config), path, fps)


def animate_nl_match(
    config: dict[str, Any],
    backend: Callable[[str], str] | None = None,
    gatekeeper: ApiGatekeeper | None = None,
    path: str = "assets/match_nl.gif",
    fps: int = 1,
) -> str:
    """Render a natural-language sub-game (with NL message overlay) as an animated GIF."""
    return _animate(nl_subgame_frames(config, backend, gatekeeper), path, fps)
