"""Drive an inter-group match against the partner's ``/decide`` servers.

We own the authoritative :class:`GameEngine`; each turn we ask **our** 4-dir policy
for our role and the **partner's** ``/decide`` for theirs, then apply the action.
:func:`run_interop_series` plays the §12.1 6-game 3-cop/3-thief role swap and builds
the report. ``partner_decide`` is injected (so the loop is offline-testable); the CLI
wires a real :class:`PartnerClient` via :func:`make_partner_decide`.
"""

from __future__ import annotations

import random
import uuid
from collections.abc import Callable
from typing import Any

from ..shared.constants import Role
from ..shared.models import Action, GameState
from .game_engine import GameEngine
from .partner_protocol import from_partner_action, to_partner_observation
from .scoring import score_subgame
from .strategy.ortho_policy import ortho_action

# (role_to_move, state) -> the partner's chosen Action.
PartnerDecide = Callable[[Role, GameState], Action]


def _other(role: Role) -> Role:
    return Role.THIEF if role is Role.COP else Role.COP


def play_interop_game(
    engine: GameEngine, state: GameState, my_role: Role, partner_decide: PartnerDecide
) -> GameState:
    """Play one game to terminal: our role uses ortho_action, the other calls partner_decide."""
    while not state.done:
        if state.to_move is my_role:
            action = ortho_action(engine, state)
        else:
            action = partner_decide(state.to_move, state)
        engine.apply(state, action)
    return state


def make_partner_decide(
    client: Any,
    engine: GameEngine,
    visibility_radius: int,
    allow_barrier: bool = False,
    new_id: Callable[[], str] = lambda: uuid.uuid4().hex,
) -> PartnerDecide:
    """Wire a :class:`PartnerClient` into a ``(role, state) -> Action`` decider over ``/decide``."""

    def decide(role: Role, state: GameState) -> Action:
        rid = new_id()
        obs = to_partner_observation(engine, state, role, visibility_radius, rid, allow_barrier)
        return from_partner_action(client.decide(role.value, obs, rid))

    return decide


def run_interop_series(
    config: dict[str, Any],
    partner_for: dict[Role, PartnerDecide],
    our_first_role: Role = Role.COP,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Play the 6-game role-swap vs the partner and return the interop report dict."""
    width, height = config["grid_size"]
    engine = GameEngine(width, height, config["max_moves"], config["max_barriers"])
    num = config.get("num_games", 6)
    half = num // 2
    seed = config.get("seed", 0)
    scoring = config["scoring"]
    our_total = partner_total = 0
    games: list[dict[str, Any]] = []
    for i in range(num):
        my_role = our_first_role if i < half else _other(our_first_role)
        state = engine.new_state(random.Random(seed + i))
        play_interop_game(engine, state, my_role, partner_for[_other(my_role)])
        result = score_subgame(i, state.winner, state.moves_used, scoring)
        ours = result.cop_score if my_role is Role.COP else result.thief_score
        theirs = result.thief_score if my_role is Role.COP else result.cop_score
        our_total += ours
        partner_total += theirs
        games.append({
            "index": i, "my_role": my_role.value, "winner": result.winner.value,
            "moves_used": result.moves_used, "our_score": ours, "partner_score": theirs,
        })
    report = {
        "report_type": "interop_match", "protocol_version": "1.0",
        "timezone": config["reporting"]["timezone"], "our_first_role": our_first_role.value,
        "sub_games": games, "totals": {"us": our_total, "partner": partner_total},
    }
    if meta:
        report.update(meta)
    return report
