"""Modern dark visual theme for the GUI — central palette + glow helper.

Presentation constants live here (single source, DRY) so the renderer/overlays
stay style-free. Matplotlib cannot render colour emoji, so agents are drawn as
distinct glowing tokens (a haloed circle / star) rather than emoji glyphs.
"""

from __future__ import annotations

from typing import Any

# Palette (modern dark).
BG = "#0e1117"          # figure background
PANEL = "#161b22"       # board (axes) background
GRID = "#2a3340"        # gridlines / spines
COP = "#3da5ff"         # cop = cool blue
THIEF = "#ffb454"       # thief = warm amber
BARRIER = "#3b4250"     # wall slab
TEXT = "#e6edf3"        # primary text
MUTED = "#8b98a5"       # secondary text
COP_TRAIL = "#1f4e79"   # faded cop path
THIEF_TRAIL = "#7a5320"  # faded thief path
WIN = "#42d77d"         # capture / win highlight


def style_axes(fig: Any, ax: Any) -> None:
    """Apply the dark palette to a figure + axes."""
    fig.set_facecolor(BG)
    ax.set_facecolor(PANEL)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.tick_params(colors=MUTED, labelsize=8)


def glow(ax: Any, x: float, y: float, color: str, marker: str, size: float) -> None:
    """Draw a marker with a soft layered halo for a neon-glow look."""
    for scale, alpha in ((2.6, 0.10), (1.9, 0.18), (1.35, 0.30)):
        ax.scatter([x], [y], s=size * scale, c=color, marker=marker,
                   alpha=alpha, edgecolors="none", zorder=2)
    ax.scatter([x], [y], s=size, c=color, marker=marker,
               edgecolors="white", linewidths=0.8, zorder=3)
