"""Stateless decision logic for the inter-group ``/decide`` protocol (reciprocal interop).

Lets a partner who **hosts** the game pull *our* agent's move: given a role-filtered
observation in the partner's protocol v1.0 (``[row, col]`` coords, 4-dir
``legal_actions``), we return exactly one of the supplied ``legal_actions``. The cop
minimises Manhattan distance to the visible opponent; the thief maximises it
(tie-break: stay central for escape room); when the opponent is unseen, both head for
the grid centre. Pure and testable — the HTTP wrapper is ``scripts/run_decide_server.py``.
"""

from __future__ import annotations

from typing import Any

# partner direction -> (d_row, d_col)
_DELTA = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}


def _apply(pos: list[int], move: dict[str, Any]) -> tuple[int, int]:
    d_row, d_col = _DELTA[move["direction"]]
    return (pos[0] + d_row, pos[1] + d_col)


def _dist(a: Any, b: Any) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def decide_action(observation: dict[str, Any]) -> dict[str, Any]:
    """Pick one of ``observation['legal_actions']`` — our move for ``observation['role']``."""
    legal = observation.get("legal_actions", [])
    moves = [a for a in legal if a.get("type") == "move" and a.get("direction") in _DELTA]
    if not moves:
        return legal[0] if legal else {"type": "move", "direction": "up"}
    self_pos = observation["self_position"]
    grid = observation.get("grid_size", [5, 5])
    center = ((grid[0] - 1) / 2, (grid[1] - 1) / 2)
    opp = observation.get("visible_opponent")
    if opp is None:  # blind: head for the open interior (search / escape room)
        return min(moves, key=lambda m: _dist(_apply(self_pos, m), center))
    if observation.get("role") == "cop":  # close in; tie-break toward the centre
        return min(moves, key=lambda m: (_dist(_apply(self_pos, m), opp),
                                         _dist(_apply(self_pos, m), center)))
    return max(moves, key=lambda m: (_dist(_apply(self_pos, m), opp),  # flee; keep escape room
                                     -_dist(_apply(self_pos, m), center)))
