"""Animate a sub-game to an animated GIF (real-time agent + barrier movement)."""

from __future__ import annotations

import copy
import random
from typing import Any

import matplotlib.pyplot as plt
from matplotlib import animation

from ..services.game_engine import GameEngine
from ..services.strategy.heuristic import cop_action, thief_action
from ..services.turn_pipeline import run_turn
from ..shared.constants import Role
from .board_renderer import render_state

plt.switch_backend("Agg")


def _frames(config: dict[str, Any]) -> list:
    """Run a heuristic sub-game, snapshotting the state after every turn."""
    width, height = config["grid_size"]
    engine = GameEngine(width, height, config["max_moves"], config["max_barriers"])
    state = engine.new_state(random.Random(config.get("seed", 0)))
    deciders = {Role.COP: cop_action, Role.THIEF: thief_action}
    frames = [copy.deepcopy(state)]
    while not state.done:
        run_turn(engine, state, deciders)
        frames.append(copy.deepcopy(state))
    return frames


def animate_match(config: dict[str, Any], path: str = "assets/match.gif", fps: int = 2) -> str:
    """Render a sub-game as an animated GIF and return the output path."""
    frames = _frames(config)
    fig, ax = plt.subplots(figsize=(5, 5))
    anim = animation.FuncAnimation(
        fig, lambda i: render_state(frames[i], ax), frames=len(frames), interval=400
    )
    anim.save(path, writer=animation.PillowWriter(fps=fps))
    plt.close(fig)
    return path
