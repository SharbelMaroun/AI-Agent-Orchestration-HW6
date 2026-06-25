"""Cross-network match driver: play one role against a shared remote MCP host.

Each team runs this for **its own** role against the agreed authoritative host
(`build_host_server`). It polls ``get_game_status``; on its role's turn it reads
``get_observation`` and submits a move via the remote tools — so the two teams'
drivers take turns on one shared game. The decision logic stays client-side
(ADR-001). The MCP ``client`` is injected (production: `McpClient`; tests: a fake),
keeping this pure and offline-testable.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from ..shared.constants import Role
from ..shared.models import Position
from .strategy.geometry import chebyshev

# A remote decider maps an observation dict -> (kind, dx, dy).
RemoteDecider = Callable[[dict[str, Any]], tuple[str, int, int]]
_STEPS = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]


def remote_decider(role: str) -> RemoteDecider:
    """Greedy decider from a remote observation: cop closes in, thief flees."""
    is_cop = role == Role.COP.value

    def decide(obs: dict[str, Any]) -> tuple[str, int, int]:
        sx, sy = obs["self"]
        opp = obs.get("opponent")
        target = Position(*opp) if opp else Position(sx, sy)  # unseen -> hold direction
        if opp is None:
            return ("stay", 0, 0)
        best = min(_STEPS, key=lambda s: _rank(Position(sx + s[0], sy + s[1]), target, is_cop))
        return ("move", best[0], best[1])

    return decide


def _rank(cell: Position, target: Position, is_cop: bool) -> int:
    """Lower is better: cop wants min distance, thief wants max (negated)."""
    d = chebyshev(cell, target)
    return d if is_cop else -d


def play_my_turns(
    client: Any,
    my_role: str,
    decide: RemoteDecider,
    *,
    poll_limit: int = 400,
    sleep: Callable[[float], None] = lambda _s: None,
    wait: float = 0.5,
) -> dict[str, Any]:
    """Poll the host; on ``my_role``'s turn observe→decide→submit. Return final status."""
    for _ in range(poll_limit):
        status = client.call_tool("get_game_status")
        if status["done"]:
            return status
        if status["to_move"] != my_role:
            sleep(wait)
            continue
        obs = client.call_tool("get_observation", role=my_role)
        kind, dx, dy = decide(obs)
        result = client.call_tool("submit_action", role=my_role, kind=kind, dx=dx, dy=dy)
        if result.get("event") == "illegal":  # never stall: a STAY always advances the turn
            client.call_tool("submit_action", role=my_role, kind="stay", dx=0, dy=0)
    return client.call_tool("get_game_status")
