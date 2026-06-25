"""Partial-observation snapshot for an agent (within its visibility radius)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..shared.constants import Role
from ..shared.models import GameState, Position


@dataclass(frozen=True)
class Observation:
    """What one agent can see this turn (Dec-POMDP partial observation)."""

    role: Role
    self_pos: Position
    opponent_pos: Position | None
    visible_cells: tuple[Position, ...]
    visible_barriers: tuple[Position, ...]

    def to_dict(self) -> dict[str, Any]:
        opp = [self.opponent_pos.x, self.opponent_pos.y] if self.opponent_pos else None
        return {
            "role": self.role.value,
            "self": [self.self_pos.x, self.self_pos.y],
            "opponent": opp,
            "visible_cells": [[p.x, p.y] for p in self.visible_cells],
            "visible_barriers": [[p.x, p.y] for p in self.visible_barriers],
        }


def _chebyshev(a: Position, b: Position) -> int:
    return max(abs(a.x - b.x), abs(a.y - b.y))


def observe(state: GameState, role: Role, visibility_radius: int) -> Observation:
    """Compute ``role``'s partial view of ``state``."""
    self_pos = state.cop if role is Role.COP else state.thief
    opp_pos = state.thief if role is Role.COP else state.cop
    visible_opponent = opp_pos if _chebyshev(self_pos, opp_pos) <= visibility_radius else None
    cells = tuple(
        Position(x, y)
        for x in range(self_pos.x - visibility_radius, self_pos.x + visibility_radius + 1)
        for y in range(self_pos.y - visibility_radius, self_pos.y + visibility_radius + 1)
        if 0 <= x < state.width and 0 <= y < state.height
    )
    barriers = tuple(c for c in cells if c in state.barriers)
    return Observation(role, self_pos, visible_opponent, cells, barriers)
