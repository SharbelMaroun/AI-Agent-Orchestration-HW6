"""Sensitivity analysis + chart suite (line / heatmap / box / scatter).

Reproducible research: `uv run python scripts/sensitivity.py` → writes high-resolution
PNGs to assets/ and the numeric tables to results/sensitivity.txt. All data comes from
real (offline, deterministic) match runs — no network. OAT (one-at-a-time) sweeps vary a
single parameter (visibility_radius or grid_size) with everything else fixed.
"""

from __future__ import annotations

import random

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from marl_cop_thief.services.game_engine import GameEngine  # noqa: E402
from marl_cop_thief.services.mcp.message_bus import MessageBus  # noqa: E402
from marl_cop_thief.services.nl_protocol.nl_decider import NLDecider  # noqa: E402
from marl_cop_thief.services.strategy.smart_cop import smart_cop_action  # noqa: E402
from marl_cop_thief.services.strategy.smart_thief import smart_thief_action  # noqa: E402
from marl_cop_thief.services.turn_pipeline import run_turn  # noqa: E402
from marl_cop_thief.shared.constants import Role  # noqa: E402
from marl_cop_thief.shared.gatekeeper import ApiGatekeeper  # noqa: E402
from marl_cop_thief.shared.llm_client import GatekeptLLM  # noqa: E402

DPI = 150
LINES: list[str] = []


def _log(msg: str) -> None:
    print(msg)
    LINES.append(msg)


def nl_subgame(n: int, visibility: int, seed: int, max_moves: int = 25):
    """One natural-language sub-game (offline echo backend) under partial observation."""
    engine = GameEngine(n, n, max_moves, 5)
    state = engine.new_state(random.Random(seed))
    llm = GatekeptLLM(lambda p: p, ApiGatekeeper())
    bus = MessageBus()
    deciders = {r: NLDecider(r, bus, llm, visibility) for r in (Role.COP, Role.THIEF)}
    while not state.done:
        run_turn(engine, state, deciders)
    return state


def smart_subgame(n: int, seed: int, max_moves: int = 25):
    """One fully-observable smart-cop vs smart-thief sub-game."""
    engine = GameEngine(n, n, max_moves, 5)
    state = engine.new_state(random.Random(seed))
    deciders = {Role.COP: smart_cop_action, Role.THIEF: smart_thief_action}
    while not state.done:
        run_turn(engine, state, deciders)
    return state


def nl_cop_rate(n: int, vis: int, runs: int) -> float:
    return sum(nl_subgame(n, vis, s).winner is Role.COP for s in range(runs)) / runs


def fig_visibility(runs: int) -> None:
    """LINE: NL cop capture rate vs visibility_radius (OAT, 5x5)."""
    vis = list(range(5))
    rates = [nl_cop_rate(5, v, runs) for v in vis]
    _log(f"[visibility OAT, 5x5, {runs} seeds] "
         + ", ".join(f"r={v}:{x:.2f}" for v, x in zip(vis, rates, strict=True)))
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(vis, rates, marker="o", color="tab:cyan")
    ax.set(title=f"NL cop capture rate vs visibility radius (5x5, {runs} seeds)",
           xlabel="visibility radius", ylabel="cop win rate", ylim=(0, 1.05))
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    fig.savefig("assets/sensitivity_visibility.png", dpi=DPI)


def fig_heatmap(runs: int) -> None:
    """HEATMAP: NL cop capture rate over grid_size x visibility_radius."""
    grids, vis = [3, 4, 5, 6], [0, 1, 2, 3]
    grid = np.array([[nl_cop_rate(n, v, runs) for v in vis] for n in grids])
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(grid, cmap="viridis", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(vis)), labels=vis)
    ax.set_yticks(range(len(grids)), labels=[f"{n}x{n}" for n in grids])
    ax.set(title=f"NL cop capture rate ({runs} seeds)", xlabel="visibility radius", ylabel="grid size")
    for i in range(len(grids)):
        for j in range(len(vis)):
            ax.text(j, i, f"{grid[i, j]:.2f}", ha="center", va="center", color="white", fontsize=8)
    fig.colorbar(im, ax=ax, label="cop win rate")
    fig.tight_layout()
    fig.savefig("assets/sensitivity_heatmap.png", dpi=DPI)


def fig_boxplot(runs: int) -> None:
    """BOX: distribution of moves-per-sub-game by grid size (smart vs smart)."""
    grids = [3, 4, 5, 6, 7]
    data = [[smart_subgame(n, s).moves_used for s in range(runs)] for n in grids]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.boxplot(data, tick_labels=[f"{n}x{n}" for n in grids])
    ax.set(title=f"Moves per sub-game by grid size (smart vs smart, {runs} seeds)",
           xlabel="grid size", ylabel="moves used")
    ax.grid(True, axis="y", alpha=0.4)
    fig.tight_layout()
    fig.savefig("assets/moves_boxplot.png", dpi=DPI)


def fig_scatter(runs: int) -> None:
    """SCATTER: board area vs mean moves-to-conclusion (smart vs smart)."""
    grids = list(range(2, 8))
    areas = [n * n for n in grids]
    means = [sum(smart_subgame(n, s).moves_used for s in range(runs)) / runs for n in grids]
    _log("[area vs mean-moves] "
         + ", ".join(f"{n}x{n}:{m:.1f}" for n, m in zip(grids, means, strict=True)))
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.scatter(areas, means, s=80, color="tab:orange", edgecolors="black")
    for n, a, m in zip(grids, areas, means, strict=True):
        ax.annotate(f"{n}x{n}", (a, m), textcoords="offset points", xytext=(6, 4), fontsize=8)
    ax.set(title=f"Board area vs mean moves to conclusion ({runs} seeds)",
           xlabel="board area (cells)", ylabel="mean moves used")
    ax.grid(True, alpha=0.4)
    fig.tight_layout()
    fig.savefig("assets/scatter_area_moves.png", dpi=DPI)


def main() -> None:
    _log("Sensitivity analysis (OAT) — real offline runs")
    _log("=" * 56)
    fig_visibility(40)
    fig_heatmap(30)
    fig_boxplot(40)
    fig_scatter(40)
    with open("results/sensitivity.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(LINES) + "\n")
    print("Wrote assets/sensitivity_*.png, assets/moves_boxplot.png, assets/scatter_area_moves.png")


if __name__ == "__main__":
    main()
