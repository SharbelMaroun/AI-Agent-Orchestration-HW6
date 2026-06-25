"""Live, real-time match window: render each turn the instant it is computed.

Unlike the GIF animator (headless ``Agg`` -> file), this switches matplotlib to an
interactive backend at runtime (config ``gui.live_backend``, default ``TkAgg``) and
draws every ``(state, caption)`` frame as it streams off the engine — so an NL match
visibly advances as each LLM call returns. Rendering only; the frames come from the
service-layer streams via the SDK (SDK-only). Omitted from coverage (interactive).
"""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

import matplotlib.pyplot as plt

from ..shared.models import GameState
from .board_renderer import render_state

# Fallback defaults if config omits a ``gui`` block (real values live in config.json).
_DEFAULT_BACKEND = "TkAgg"
_DEFAULT_DELAY = 0.6


def play_live(
    frames: Iterable[tuple[GameState, str]], config: dict[str, Any], title: str = "Cop & Thief"
) -> None:
    """Open an interactive window and draw each streamed frame in real time."""
    gui_cfg = config.get("gui", {})
    plt.switch_backend(gui_cfg.get("live_backend", _DEFAULT_BACKEND))
    delay = gui_cfg.get("turn_delay_seconds", _DEFAULT_DELAY)
    fig, ax = plt.subplots(figsize=(5, 5.5))
    fig.suptitle(title)
    plt.ion()
    for state, caption in frames:
        render_state(state, ax, caption)
        fig.tight_layout()
        plt.draw()
        plt.pause(delay)
    plt.ioff()
    plt.show(block=True)  # keep the final board on screen until the user closes it
