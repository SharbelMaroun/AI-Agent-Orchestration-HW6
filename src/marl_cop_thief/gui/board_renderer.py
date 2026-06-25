"""Render a game state to a matplotlib axes / PNG — modern dark theme.

Draws the board, faded movement trails, glowing cop/thief tokens, barrier slabs,
a capture flash on a cop win, and the HUD + speech-bubble overlays. Render-only
(no game logic); trails and ``max_moves`` are supplied by the caller so the
function stays stateless. Omitted from coverage (matplotlib drawing).
"""

from __future__ import annotations

from collections.abc import Sequence

import matplotlib.pyplot as plt

from ..shared.constants import Role
from ..shared.models import GameState, Position
from . import theme
from .overlays import draw_hud, draw_speech

plt.switch_backend("Agg")


def _trail(ax, positions: Sequence[Position], color: str) -> None:
    """Draw a fading breadcrumb path (older = fainter); skip the current cell."""
    history = positions[:-1]
    for i, p in enumerate(history):
        alpha = 0.10 + 0.45 * (i + 1) / len(history)
        ax.scatter([p.x], [p.y], s=80, c=color, alpha=alpha, edgecolors="none", zorder=1)


def render_state(
    state: GameState,
    ax,
    message: str = "",
    *,
    max_moves: int | None = None,
    cop_trail: Sequence[Position] = (),
    thief_trail: Sequence[Position] = (),
) -> None:
    """Draw the whole board frame (dark theme, glow tokens, trails, HUD, speech)."""
    ax.clear()
    theme.style_axes(ax.figure, ax)
    # Reserve margin for the title/legend (top) and the speech bubble (bottom) so
    # they are never clipped; do NOT use tight_layout (it squeezes them off-frame).
    ax.figure.subplots_adjust(left=0.09, right=0.96, top=0.85, bottom=0.22)
    ax.set_xlim(-0.5, state.width - 0.5)
    ax.set_ylim(-0.5, state.height - 0.5)
    ax.set_xticks(range(state.width))
    ax.set_yticks(range(state.height))
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.grid(True, color=theme.GRID, linewidth=0.6, alpha=0.5)
    for barrier in state.barriers:
        ax.add_patch(plt.Rectangle((barrier.x - 0.5, barrier.y - 0.5), 1, 1,
                                   color=theme.BARRIER, zorder=1))
    _trail(ax, cop_trail, theme.COP_TRAIL)
    _trail(ax, thief_trail, theme.THIEF_TRAIL)
    if state.done and state.winner is Role.COP:  # capture flash under the cop
        theme.glow(ax, state.cop.x, state.cop.y, theme.WIN, "o", 1000)
    theme.glow(ax, state.cop.x, state.cop.y, theme.COP, "o", 430)
    theme.glow(ax, state.thief.x, state.thief.y, theme.THIEF, "*", 640)
    draw_hud(ax, state, max_moves)
    draw_speech(ax, state, message)


def save_state_png(state: GameState, path: str) -> str:
    """Render ``state`` to a PNG file and return the path."""
    fig, ax = plt.subplots(figsize=(5.5, 6))
    render_state(state, ax)
    fig.savefig(path, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    return path
