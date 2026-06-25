"""Encode a chosen action + observation into a natural-language message.

The cop communicates honestly (reveals its cell); the thief is deliberately
vague (partial deception) — both still "natural language", not a wire protocol.
"""

from __future__ import annotations

from ...shared.constants import ActionKind, Role
from ...shared.models import Action
from ..observation import Observation

_DIRECTIONS = {
    (0, -1): "north", (0, 1): "south", (1, 0): "east", (-1, 0): "west",
    (1, -1): "north-east", (-1, -1): "north-west",
    (1, 1): "south-east", (-1, 1): "south-west",
}


def _direction(action: Action) -> str:
    return _DIRECTIONS.get((action.dx, action.dy), "around")


def encode(role: Role, obs: Observation, action: Action) -> str:
    """Produce the free-text message describing this turn's intention."""
    if action.kind is ActionKind.PLACE_BARRIER:
        return f"Placing a wall at {obs.self_pos.x},{obs.self_pos.y}."
    if action.kind is ActionKind.STAY:
        return "Holding my position for now."
    direction = _direction(action)
    if role is Role.THIEF:
        return f"Slipping away to the {direction} — you'll never find me."
    return f"I'm at {obs.self_pos.x},{obs.self_pos.y} pushing {direction} to close in."
