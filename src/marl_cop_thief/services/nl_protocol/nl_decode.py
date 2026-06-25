"""Interpret an opponent's message into an updated belief about their position.

The LLM (via the gatekeeper) does the interpretation; parsing is defensive so an
ambiguous or unparseable message never crashes — it keeps the prior belief.
"""

from __future__ import annotations

from ...shared.llm_client import LLMClient
from ...shared.models import Position
from ..board import Board
from .ambiguity_handler import parse_position
from .prompt_templates import interpret_prompt


def interpret(
    llm: LLMClient, message_text: str, prior: Position | None, board: Board
) -> Position | None:
    """Return an updated opponent-position belief from a free-text message."""
    try:
        response = llm.complete(interpret_prompt(message_text))
    except Exception:
        return prior
    guess = parse_position(response)
    if guess is None or not board.in_bounds(guess):
        return prior
    return guess
