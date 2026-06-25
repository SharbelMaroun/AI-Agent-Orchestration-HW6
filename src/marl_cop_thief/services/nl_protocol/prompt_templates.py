"""Prompt templates for the natural-language agents (see docs/PROMPT_LOG.md)."""

from __future__ import annotations

from ...shared.constants import ActionKind, Role
from ...shared.models import Action
from ..observation import Observation
from .nl_encode import direction

_SYSTEM = (
    "You are an autonomous agent in a grid pursuit game played via natural language. "
    "You see only part of the board. Communicate intentions or observations; you may be vague."
)


def system_prompt(role: Role) -> str:
    """System prompt framing the agent's role and goal."""
    goal = "capture the thief" if role is Role.COP else "evade the cop and survive 25 moves"
    return f"{_SYSTEM} You are the {role.value}; your goal is to {goal}."


def interpret_prompt(message_text: str) -> str:
    """Prompt asking the LLM to extract the opponent's implied position."""
    return (
        "Read this message from your opponent and reply with their grid position as 'x,y' "
        f"if it is implied, otherwise reply 'unknown'. Message: {message_text!r}"
    )


def _facts(role: Role, obs: Observation, action: Action) -> str:
    """One clause of factual content for the speak prompt, role-appropriate."""
    if action.kind is ActionKind.PLACE_BARRIER:
        return f"you slam down a wall at your cell {obs.self_pos.x},{obs.self_pos.y}"
    if action.kind is ActionKind.STAY:
        return "you hold your position this turn"
    heading = direction(action)
    if role is Role.COP:
        return f"you move {heading} from your position {obs.self_pos.x},{obs.self_pos.y} to close in"
    return f"you slip {heading} to evade, hiding your exact location"


def speak_prompt(role: Role, obs: Observation, action: Action) -> str:
    """Prompt the LLM to voice this move in character (cop reveals cell; thief stays cryptic)."""
    persona = (
        "a determined, heroic police officer hunting a thief"
        if role is Role.COP
        else "a sly, taunting thief slipping through the cop's net"
    )
    disclosure = (
        "Clearly state or imply your grid position. "
        if role is Role.COP
        else "Be cryptic and boastful; do NOT reveal your exact coordinates. "
    )
    return (
        f"You are {persona} in a grid pursuit game. In ONE short, vivid sentence (max 15 words), "
        f"speak in character about this move: {_facts(role, obs, action)}. "
        f"{disclosure}Reply with only the sentence — no quotes, no preamble."
    )
