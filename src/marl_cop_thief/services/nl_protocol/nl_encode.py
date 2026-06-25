"""Encode a chosen action + observation into a natural-language message.

The cop communicates honestly (reveals its cell); the thief is deliberately
vague (partial deception) — both still "natural language", not a wire protocol.
"""

from __future__ import annotations

from collections.abc import Callable

from ...shared.constants import ActionKind, Role
from ...shared.models import Action
from ..observation import Observation

# A speaker turns (role, observation, action) into this turn's free-text message.
# Two implementations exist: deterministic ``encode`` (below) and ``nl_speak.llm_speaker``.
Speaker = Callable[[Role, Observation, Action], str]

_DIRECTIONS = {
    (0, -1): "north", (0, 1): "south", (1, 0): "east", (-1, 0): "west",
    (1, -1): "north-east", (-1, -1): "north-west",
    (1, 1): "south-east", (-1, 1): "south-west",
}


def direction(action: Action) -> str:
    """Compass word for an action's delta (``around`` for non-moves)."""
    return _DIRECTIONS.get((action.dx, action.dy), "around")


def encode(role: Role, obs: Observation, action: Action) -> str:
    """Produce the free-text message describing this turn's intention (deterministic)."""
    if action.kind is ActionKind.PLACE_BARRIER:
        return f"Placing a wall at {obs.self_pos.x},{obs.self_pos.y}."
    if action.kind is ActionKind.STAY:
        return "Holding my position for now."
    heading = direction(action)
    if role is Role.THIEF:
        return f"Slipping away to the {heading} — you'll never find me."
    return f"I'm at {obs.self_pos.x},{obs.self_pos.y} pushing {heading} to close in."
