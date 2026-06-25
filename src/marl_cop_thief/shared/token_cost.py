"""Token accounting and cost estimation for LLM usage (README R.7).

OpenAI bills per input/output token. Exact counts come from the API ``usage`` field
on a real run; for an **offline** estimate we approximate token counts from text
length using a fixed characters-per-token ratio (OpenAI's ~4-chars/token rule of
thumb), which needs no tokenizer download. Prices and the ratio are **config-driven**
(``config.json`` → ``llm.pricing``) — never hard-coded here (CLAUDE.md §5).
"""

from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Any


@dataclass(frozen=True)
class TokenUsage:
    """Aggregate token usage over a run (calls + input/output token totals)."""

    calls: int
    input_tokens: int
    output_tokens: int

    @property
    def total_tokens(self) -> int:
        """Combined input + output tokens."""
        return self.input_tokens + self.output_tokens


def estimate_tokens(text: str, chars_per_token: float) -> int:
    """Approximate the token count of ``text`` (offline, no tokenizer download)."""
    if chars_per_token <= 0:
        raise ValueError("chars_per_token must be positive")
    return ceil(len(text) / chars_per_token)


def cost_usd(usage: TokenUsage, pricing: dict[str, Any]) -> float:
    """Dollar cost of ``usage`` at config-driven per-million-token prices."""
    return (
        usage.input_tokens / 1_000_000 * pricing["input_per_1m"]
        + usage.output_tokens / 1_000_000 * pricing["output_per_1m"]
    )
