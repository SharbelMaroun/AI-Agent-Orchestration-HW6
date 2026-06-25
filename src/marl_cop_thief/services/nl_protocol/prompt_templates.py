"""Prompt templates for the natural-language agents (see docs/PROMPT_LOG.md)."""

from __future__ import annotations

from ...shared.constants import Role

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
