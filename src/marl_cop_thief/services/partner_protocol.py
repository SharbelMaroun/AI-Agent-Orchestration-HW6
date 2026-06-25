"""Bridge our engine to the partner's custom decision protocol (v1.0).

Their ``/decide`` is a stateless policy: we own the :class:`GameEngine`, send a
role-filtered observation with explicit ``legal_actions``, and they return exactly
one of them. Their coordinates are ``[row, col]`` = our ``(y, x)`` and movement is
4-directional (no diagonals, no STAY). These pure functions map between the two
representations so the HTTP client and the match driver stay thin.
See docs/PRD_partner_interop.md.
"""

from __future__ import annotations

from typing import Any

from ..shared.constants import Role
from ..shared.models import Action, GameState, Position
from .barriers import can_place
from .board import passable
from .game_engine import GameEngine
from .observation import observe

PROTOCOL_VERSION = "1.0"
# our (dx, dy) <-> their direction name — orthogonal only (their protocol has no diagonals).
_DXDY_TO_DIR = {(0, -1): "up", (0, 1): "down", (-1, 0): "left", (1, 0): "right"}
_DIR_TO_DXDY = {name: dxdy for dxdy, name in _DXDY_TO_DIR.items()}


def _rc(pos: Position) -> list[int]:
    """Our ``(x, y)`` -> their ``[row, col]`` (row = y, col = x)."""
    return [pos.y, pos.x]


def legal_partner_actions(
    engine: GameEngine, state: GameState, allow_barrier: bool = False
) -> list[dict[str, Any]]:
    """The current actor's legal moves in the partner's 4-dir format.

    ``place_barrier`` (cop only) is included **only** when ``allow_barrier``: a
    partner's ``/decide`` may not support it — salareen's server returns 500 on a
    ``place_barrier`` action — so interop defaults to a moves-only game.
    """
    pos = state.cop if state.to_move is Role.COP else state.thief
    actions: list[dict[str, Any]] = [
        {"type": "move", "direction": name}
        for (dx, dy), name in _DXDY_TO_DIR.items()
        if passable(engine.board, state.barriers, pos.step(dx, dy))
    ]
    if allow_barrier and state.to_move is Role.COP and can_place(state, engine.max_barriers):
        actions.append({"type": "place_barrier", "target": _rc(pos)})
    return actions


def to_partner_observation(
    engine: GameEngine, state: GameState, role: Role, visibility_radius: int,
    request_id: str, allow_barrier: bool = False
) -> dict[str, Any]:
    """Build the partner's role-filtered observation JSON for ``role`` (moves-only by default)."""
    obs = observe(state, role, visibility_radius)
    opp = obs.opponent_pos
    return {
        "protocol_version": PROTOCOL_VERSION,
        "request_id": request_id,
        "role": role.value,
        "grid_size": [state.width, state.height],
        "self_position": _rc(obs.self_pos),
        "visible_opponent": (_rc(opp) if opp else None),
        "visible_barriers": [_rc(b) for b in obs.visible_barriers],
        "legal_actions": legal_partner_actions(engine, state, allow_barrier),
        "move_round": state.moves_used,
        "max_moves": engine.max_moves,
        "barriers_placed": state.cop_barriers_used,
        "max_barriers": engine.max_barriers,
        "history_summary": [],
    }


def from_partner_action(action: dict[str, Any]) -> Action:
    """Map the partner's returned action back to our :class:`Action`."""
    if action.get("type") == "place_barrier":
        return Action.place_barrier()
    direction = action.get("direction")
    if direction not in _DIR_TO_DXDY:
        raise ValueError(f"unknown partner direction {direction!r}")
    return Action.move(*_DIR_TO_DXDY[direction])
