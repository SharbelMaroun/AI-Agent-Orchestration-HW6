"""Barrier placement rules: cop-only, capped, and impassable once placed."""

from __future__ import annotations

from ..shared.models import GameState


def can_place(state: GameState, max_barriers: int) -> bool:
    """Whether the cop still has barrier budget remaining."""
    return state.cop_barriers_used < max_barriers


def place(state: GameState) -> None:
    """Place a barrier on the cop's current cell and consume one from the budget."""
    state.barriers.add(state.cop)
    state.cop_barriers_used += 1
