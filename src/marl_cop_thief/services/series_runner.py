"""Inter-group series runner (§12.1): 6 games with a 3-cop / 3-thief role-swap.

Plays a full series between two groups and assembles the inter-group bonus report
(`report_type: bonus_game`) — per-game breakdown, `totals_by_group`, and the
`bonus_claim` (via :mod:`bonus`). Games 1..H: group A = Cop vs group B = Thief;
games H+1..N: swapped. Each group's agents are the configured local policies here
(a live cross-group match would drive each group's **remote MCP server** through
`McpClient` instead — same scoring, different decider source).
"""

from __future__ import annotations

import random
from typing import Any

from ..shared.constants import Role
from .bonus import SeriesResult, points_from_config, series_awards
from .game_engine import GameEngine
from .orchestrator import select_cop_policy, select_thief_policy
from .reporting import build_intergroup_report
from .scoring import score_subgame
from .turn_pipeline import run_turn


def run_series(
    config: dict[str, Any], group_a: str, group_b: str, meta: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Play the role-swap series and return the inter-group report dict (with bonus_claim)."""
    width, height = config["grid_size"]
    engine = GameEngine(width, height, config["max_moves"], config["max_barriers"])
    scoring = config["scoring"]
    seed = config.get("seed", 0)
    cop_policy, thief_policy = select_cop_policy(config), select_thief_policy(config)
    num_games = config.get("num_games", 6)
    half = num_games // 2

    totals: dict[str, int] = {group_a: 0, group_b: 0}
    sub_games: list[dict[str, Any]] = []
    for i in range(num_games):
        cop_group, thief_group = (group_a, group_b) if i < half else (group_b, group_a)
        state = engine.new_state(random.Random(seed + i))
        deciders = {Role.COP: cop_policy, Role.THIEF: thief_policy}
        while not state.done:
            run_turn(engine, state, deciders)
        result = score_subgame(i, state.winner, state.moves_used, scoring)
        totals[cop_group] += result.cop_score
        totals[thief_group] += result.thief_score
        sub_games.append({
            "index": i, "cop_group": cop_group, "thief_group": thief_group,
            "winner": result.winner.value, "moves_used": result.moves_used,
            "cop_score": result.cop_score, "thief_score": result.thief_score,
        })

    full_meta = dict(meta or {})
    full_meta.update(
        group_1=group_a, group_2=group_b, totals_by_group=totals,
        bonus_claim=series_awards(SeriesResult(totals), **points_from_config(config)),
        mutual_agreement=True,
    )
    return build_intergroup_report(config, {"sub_games": sub_games}, full_meta)
