"""Tests for the token accounting + cost estimation utility (README R.7)."""

import pytest

from marl_cop_thief.shared.token_cost import TokenUsage, cost_usd, estimate_tokens


def test_estimate_tokens_rounds_up():
    assert estimate_tokens("", 4) == 0
    assert estimate_tokens("abcd", 4) == 1
    assert estimate_tokens("abcde", 4) == 2  # ceil(5/4)


def test_estimate_tokens_rejects_nonpositive_ratio():
    with pytest.raises(ValueError, match="positive"):
        estimate_tokens("hello", 0)


def test_token_usage_total():
    usage = TokenUsage(calls=10, input_tokens=300, output_tokens=40)
    assert usage.total_tokens == 340


def test_cost_usd_prices_input_and_output():
    usage = TokenUsage(calls=1, input_tokens=1_000_000, output_tokens=2_000_000)
    pricing = {"input_per_1m": 0.15, "output_per_1m": 0.60}
    assert cost_usd(usage, pricing) == pytest.approx(0.15 + 1.20)


def test_cost_usd_is_zero_for_no_usage():
    usage = TokenUsage(calls=0, input_tokens=0, output_tokens=0)
    assert cost_usd(usage, {"input_per_1m": 0.15, "output_per_1m": 0.60}) == 0.0
