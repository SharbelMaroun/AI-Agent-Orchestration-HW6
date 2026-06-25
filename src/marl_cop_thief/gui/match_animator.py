"""Animate a sub-game to an animated GIF (real-time agent + barrier movement).

Two modes mirror the CLI: a **heuristic/smart** sub-game (``animate_match``, the
``--simple`` path, cop policy from ``config.strategy.type``) and the **natural-language**
sub-game (``animate_nl_match``, the default), which overlays each turn's NL message so
the GIF shows the agents *talking* as they move. The ``(state, caption)`` frames come
from the service-layer streams; this module only renders them to a file (SDK-only).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import matplotlib.pyplot as plt
from matplotlib import animation

from ..services.match_stream import Frame, heuristic_subgame_stream
from ..services.nl_match import nl_subgame_frames
from ..shared.gatekeeper import ApiGatekeeper
from .board_renderer import render_state

plt.switch_backend("Agg")


def _draw(frames: list[Frame], ax, max_moves: int | None, i: int) -> None:
    """Render frame ``i`` with the trail accumulated up to it."""
    render_state(
        frames[i][0], ax, frames[i][1], max_moves=max_moves,
        cop_trail=[f[0].cop for f in frames[: i + 1]],
        thief_trail=[f[0].thief for f in frames[: i + 1]],
    )


def _animate(frames: list[Frame], path: str, fps: int, max_moves: int | None = None) -> str:
    """Render ``(state, caption)`` frames to an animated GIF; return the output path."""
    fig, ax = plt.subplots(figsize=(5.5, 6))
    anim = animation.FuncAnimation(
        fig, lambda i: _draw(frames, ax, max_moves, i), frames=len(frames), interval=400
    )
    anim.save(path, writer=animation.PillowWriter(fps=fps))
    plt.close(fig)
    return path


def animate_match(config: dict[str, Any], path: str = "assets/match.gif", fps: int = 2) -> str:
    """Render a heuristic/smart sub-game as an animated GIF (the ``--simple`` path)."""
    return _animate(list(heuristic_subgame_stream(config)), path, fps, config["max_moves"])


def animate_nl_match(
    config: dict[str, Any],
    backend: Callable[[str], str] | None = None,
    gatekeeper: ApiGatekeeper | None = None,
    path: str = "assets/match_nl.gif",
    fps: int = 1,
    creative: bool = False,
) -> str:
    """Render a natural-language sub-game (with NL message overlay) as an animated GIF."""
    frames = nl_subgame_frames(config, backend, gatekeeper, creative=creative)
    return _animate(frames, path, fps, config["max_moves"])
