"""Render a single game state to a matplotlib axes / PNG."""

from __future__ import annotations

import matplotlib.pyplot as plt

from ..shared.models import GameState

plt.switch_backend("Agg")


def render_state(state: GameState, ax, message: str = "") -> None:
    """Draw cop (blue circle), thief (red star), barriers (black); optional NL caption."""
    ax.clear()
    ax.set_xlim(-0.5, state.width - 0.5)
    ax.set_ylim(-0.5, state.height - 0.5)
    ax.set_xticks(range(state.width))
    ax.set_yticks(range(state.height))
    ax.grid(True)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    for barrier in state.barriers:
        ax.add_patch(plt.Rectangle((barrier.x - 0.5, barrier.y - 0.5), 1, 1, color="black"))
    ax.scatter([state.cop.x], [state.cop.y], c="tab:blue", s=420, marker="o", label="Cop")
    ax.scatter([state.thief.x], [state.thief.y], c="tab:red", s=520, marker="*", label="Thief")
    title = f"move {state.moves_used}"
    if state.done and state.winner is not None:
        title += f" — {state.winner.value} wins"
    ax.set_title(title)
    if message:  # natural-language message spoken this turn (NL match)
        ax.set_xlabel(message, fontsize=8, wrap=True)
    ax.legend(loc="upper right")


def save_state_png(state: GameState, path: str) -> str:
    """Render ``state`` to a PNG file and return the path."""
    fig, ax = plt.subplots(figsize=(5, 5))
    render_state(state, ax)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path
