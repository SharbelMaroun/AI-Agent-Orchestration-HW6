"""Generate experiment graphs + board-state images + a sample NL match log.

Reproducible analysis: run `uv run python scripts/make_figures.py`. Outputs PNGs
to assets/ and a CLI log to results/. Data comes from real match runs.
"""

from __future__ import annotations

import random

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from marl_cop_thief.services.game_engine import GameEngine  # noqa: E402
from marl_cop_thief.services.mcp.message_bus import MessageBus  # noqa: E402
from marl_cop_thief.services.nl_protocol.nl_decider import NLDecider  # noqa: E402
from marl_cop_thief.services.strategy.heuristic import cop_action, thief_action  # noqa: E402
from marl_cop_thief.services.turn_pipeline import run_turn  # noqa: E402
from marl_cop_thief.shared.constants import Role  # noqa: E402
from marl_cop_thief.shared.gatekeeper import ApiGatekeeper  # noqa: E402
from marl_cop_thief.shared.llm_client import GatekeptLLM  # noqa: E402

DPI = 150
_OPP = {Role.COP: Role.THIEF, Role.THIEF: Role.COP}


def heuristic_deciders(_engine):
    return {Role.COP: cop_action, Role.THIEF: thief_action}


def nl_deciders(_engine):
    bus, gk = MessageBus(), ApiGatekeeper()
    llm = GatekeptLLM(lambda prompt: prompt, gk)
    return {Role.COP: NLDecider(Role.COP, bus, llm, 1), Role.THIEF: NLDecider(Role.THIEF, bus, llm, 1)}


def play(n, factory, seed, max_moves=25):
    engine = GameEngine(n, n, max_moves, 5)
    state = engine.new_state(random.Random(seed))
    deciders = factory(engine)
    while not state.done:
        run_turn(engine, state, deciders)
    return state


def cop_rate(n, factory, runs):
    return sum(1 for s in range(runs) if play(n, factory, s).winner is Role.COP) / runs


def fig_outcomes(states):
    cop = sum(1 for s in states if s.winner is Role.COP)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(["Cop wins", "Thief wins"], [cop, len(states) - cop], color=["tab:blue", "tab:red"])
    ax.set_title(f"Match outcomes on 5x5 ({len(states)} seeds, heuristic)")
    ax.set_ylabel("count")
    fig.tight_layout()
    fig.savefig("assets/win_distribution.png", dpi=DPI)


def fig_moves(states):
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.hist([s.moves_used for s in states], bins=range(0, 27, 2), color="tab:purple", edgecolor="white")
    ax.set_title("Distribution of moves per sub-game (5x5)")
    ax.set_xlabel("moves used")
    ax.set_ylabel("frequency")
    fig.tight_layout()
    fig.savefig("assets/moves_histogram.png", dpi=DPI)


def fig_gridsize(runs):
    sizes = [2, 3, 4, 5, 6]
    rates = [cop_rate(n, heuristic_deciders, runs) for n in sizes]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(sizes, rates, marker="o", color="tab:green")
    ax.set_title(f"Cop capture rate vs grid size ({runs} seeds)")
    ax.set_xlabel("grid size (N x N)")
    ax.set_ylabel("cop win rate")
    ax.set_ylim(0, 1)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig("assets/winrate_vs_gridsize.png", dpi=DPI)


def fig_strategy(runs):
    rates = [cop_rate(5, heuristic_deciders, runs), cop_rate(5, nl_deciders, runs)]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(["Heuristic", "Natural language"], rates, color=["tab:blue", "tab:orange"])
    ax.set_title(f"Cop win rate by strategy on 5x5 ({runs} seeds)")
    ax.set_ylabel("cop win rate")
    ax.set_ylim(0, 1)
    fig.tight_layout()
    fig.savefig("assets/heuristic_vs_nl.png", dpi=DPI)


def _draw(ax, n, cop, thief, barriers, title):
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(-0.5, n - 0.5)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.grid(True)
    ax.set_aspect("equal")
    ax.invert_yaxis()
    ax.set_title(title)
    for b in barriers:
        ax.add_patch(plt.Rectangle((b.x - 0.5, b.y - 0.5), 1, 1, color="black"))
    ax.scatter([cop.x], [cop.y], c="tab:blue", s=420, marker="o", label="Cop")
    ax.scatter([thief.x], [thief.y], c="tab:red", s=520, marker="*", label="Thief")
    ax.legend(loc="upper right")


def _first_capture_seed():
    for seed in range(60):
        if play(5, heuristic_deciders, seed).winner is Role.COP:
            return seed
    return 0


def fig_board():
    seed = _first_capture_seed()
    engine = GameEngine(5, 5, 25, 5)
    state = engine.new_state(random.Random(seed))
    start = (state.cop, state.thief)
    while not state.done:
        run_turn(engine, state, heuristic_deciders(engine))
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.5))
    _draw(axes[0], 5, start[0], start[1], set(), "Start state")
    final_title = "Final: cop captures thief" if state.winner is Role.COP else f"Final: {state.winner.value} wins"
    _draw(axes[1], 5, state.cop, state.thief, state.barriers, final_title)
    fig.suptitle(f"Cop & Thief board (5x5, heuristic, seed {seed})")
    fig.tight_layout()
    fig.savefig("assets/board_state.png", dpi=DPI)


def nl_log():
    engine = GameEngine(5, 5, 25, 5)
    state = engine.new_state(random.Random(5))
    bus, gk = MessageBus(), ApiGatekeeper()
    llm = GatekeptLLM(lambda prompt: prompt, gk)
    deciders = {Role.COP: NLDecider(Role.COP, bus, llm, 1), Role.THIEF: NLDecider(Role.THIEF, bus, llm, 1)}
    lines = ["Natural-language match log (5x5, seed 5)", "=" * 60]
    while not state.done:
        actor = state.to_move
        result = run_turn(engine, state, deciders)
        box = bus._inbox[_OPP[actor]]
        msg = box[-1].text if box else ""
        lines.append(
            f"move {state.moves_used:2d} | {actor.value:5s} {result.event.value:18s} "
            f"cop=({state.cop.x},{state.cop.y}) thief=({state.thief.x},{state.thief.y}) | {actor.value}: {msg}"
        )
    lines.append("=" * 60)
    lines.append(f"RESULT: {state.winner.value} wins in {state.moves_used} moves; LLM calls via gatekeeper={gk.calls}")
    with open("results/nl_match_sample.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    states = [play(5, heuristic_deciders, s) for s in range(60)]
    fig_outcomes(states)
    fig_moves(states)
    fig_gridsize(40)
    fig_strategy(40)
    fig_board()
    nl_log()
    print("Wrote assets/*.png and results/nl_match_sample.txt")


if __name__ == "__main__":
    main()
