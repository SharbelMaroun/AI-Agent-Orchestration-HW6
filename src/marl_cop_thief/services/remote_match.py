"""Cross-network match driver: play one role against a shared remote MCP host.

Each team runs this for **its own** role against the agreed authoritative host
(`build_host_server`). It polls ``get_game_status``; on its role's turn it reads
``get_observation`` and submits a move via the remote tools — so the two teams'
drivers take turns on one shared game. Decisions stay client-side (ADR-001) and use
**only the partial observation** (self, opponent-if-visible, on-board + barrier cells):

* **cop** closes in — edge/barrier-aware, tie-breaking by alignment (to corner the
  thief) then by its own mobility (keep pursuit options);
* **thief** flees the cop while keeping the most escape room (mobility);
* **when blind** (rival unseen) both head for the visible interior — the cop to
  search, the thief for room — instead of wasting a turn standing still.

The ``client`` is injected (prod: `McpClient`; tests: a fake), keeping this pure
and offline-testable. Move strategy is heuristic by design (assignment §4).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from ..shared.constants import Role

RemoteDecider = Callable[[dict[str, Any]], tuple[str, int, int]]
Cell = tuple[int, int]
_STEPS = [(dx, dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0)]


def _cheb(a: Cell, b: Cell) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def _manhattan(a: Cell, b: Cell) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _mobility(cell: Cell, on_board: set[Cell], blocked: set[Cell]) -> int:
    """Open, on-board neighbours of ``cell`` (escape room for thief / options for cop)."""
    return sum(
        1
        for dx, dy in _STEPS
        if (cell[0] + dx, cell[1] + dy) in on_board and (cell[0] + dx, cell[1] + dy) not in blocked
    )


def _centroid(cells: set[Cell]) -> tuple[float, float]:
    """Centre of mass of visible on-board cells — biases toward the open interior."""
    n = len(cells)
    return (sum(c[0] for c in cells) / n, sum(c[1] for c in cells) / n)


def _pursuit_key(
    cell: Cell, target: Cell, on_board: set[Cell], blocked: set[Cell], is_cop: bool
) -> tuple[int, ...]:
    """Rank a candidate cell (max wins): cop closes in & aligns; thief flees & stays mobile."""
    mob = _mobility(cell, on_board, blocked)
    if is_cop:
        return (-_cheb(cell, target), -_manhattan(cell, target), mob)
    return (_cheb(cell, target), mob)


def remote_decider(role: str) -> RemoteDecider:
    """Build a strong observation-only decider for ``role`` (cop pursues, thief evades)."""
    is_cop = role == Role.COP.value

    def decide(obs: dict[str, Any]) -> tuple[str, int, int]:
        here: Cell = (obs["self"][0], obs["self"][1])
        on_board = {(c[0], c[1]) for c in obs["visible_cells"]}
        blocked = {(b[0], b[1]) for b in obs["visible_barriers"]}
        legal = [
            s
            for s in _STEPS
            if (here[0] + s[0], here[1] + s[1]) in on_board
            and (here[0] + s[0], here[1] + s[1]) not in blocked
        ]
        if not legal:
            return ("stay", 0, 0)
        opp = obs.get("opponent")
        if opp is None:  # rival unseen -> head for the open interior (search / escape room)
            gx, gy = _centroid(on_board)
            step = min(legal, key=lambda s: (here[0] + s[0] - gx) ** 2 + (here[1] + s[1] - gy) ** 2)
            return ("move", step[0], step[1])
        target: Cell = (opp[0], opp[1])
        step = max(
            legal,
            key=lambda s: _pursuit_key(
                (here[0] + s[0], here[1] + s[1]), target, on_board, blocked, is_cop
            ),
        )
        return ("move", step[0], step[1])

    return decide


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
