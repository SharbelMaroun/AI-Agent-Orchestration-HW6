"""HUD scoreboard + speech-bubble overlays for the board renderer.

Render-only: reads what's available on a :class:`GameState` (move count, whose
turn, terminal winner) plus an optional ``max_moves`` for the HUD, and parses the
``"<role>: <text>"`` caption to anchor a speech bubble on the speaker.
"""

from __future__ import annotations

import textwrap
from typing import Any

from ..shared.constants import Role
from ..shared.models import GameState
from . import theme


def draw_hud(ax: Any, state: GameState, max_moves: int | None) -> None:
    """Title banner (turn / winner) + move counter + a small legend."""
    if state.done and state.winner is not None:
        banner, color = f"{state.winner.value.upper()} WINS", theme.WIN
    else:
        color = theme.COP if state.to_move is Role.COP else theme.THIEF
        banner = f"{state.to_move.value.upper()} to move"
    ax.set_title(banner, color=color, fontsize=15, fontweight="bold", pad=14)
    moves = f"MOVE {state.moves_used}" + (f" / {max_moves}" if max_moves else "")
    ax.text(0.0, 1.03, moves, transform=ax.transAxes, color=theme.MUTED, fontsize=9, ha="left")
    ax.text(1.0, 1.03, "● cop", transform=ax.transAxes, color=theme.COP, fontsize=9, ha="right")
    ax.text(0.86, 1.03, "★ thief", transform=ax.transAxes, color=theme.THIEF, fontsize=9, ha="right")


def draw_speech(ax: Any, state: GameState, message: str) -> None:
    """Anchor a rounded speech bubble (pointing at the speaker) below the board."""
    if not message:
        return
    role_name, _, text = message.partition(": ")
    is_cop = role_name == Role.COP.value
    speaker = state.cop if is_cop else state.thief
    color = theme.COP if is_cop else theme.THIEF
    ax.annotate(
        textwrap.fill(text, 46),
        xy=(speaker.x, speaker.y), xycoords="data",
        xytext=(0.5, -0.16), textcoords="axes fraction",
        ha="center", va="top", color=theme.TEXT, fontsize=9.5,
        bbox={"boxstyle": "round,pad=0.5", "fc": theme.PANEL, "ec": color, "lw": 1.5},
        arrowprops={"arrowstyle": "-|>", "color": color, "alpha": 0.8, "shrinkA": 6},
    )
