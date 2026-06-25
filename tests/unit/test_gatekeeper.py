"""Tests for the minimal API gatekeeper."""

import pytest

from marl_cop_thief.shared.gatekeeper import ApiGatekeeper, gatekeeper_from_config


def test_success_is_single_call():
    gk = ApiGatekeeper(max_retries=3)
    assert gk.execute(lambda x: x + 1, 41) == 42
    assert gk.calls == 1
    assert gk.log[-1]["ok"] is True


def test_retries_then_succeeds():
    state = {"n": 0}

    def flaky() -> str:
        state["n"] += 1
        if state["n"] < 3:
            raise ValueError("transient")
        return "ok"

    gk = ApiGatekeeper(max_retries=3)
    assert gk.execute(flaky) == "ok"
    assert state["n"] == 3
    assert gk.calls == 3


def test_raises_after_exhausting_retries():
    def always_fail() -> None:
        raise RuntimeError("down")

    gk = ApiGatekeeper(max_retries=2)
    with pytest.raises(RuntimeError):
        gk.execute(always_fail)
    assert gk.calls == 3  # 1 + 2 retries
    assert gk.log[-1]["ok"] is False


def test_gatekeeper_from_config_uses_service_then_default():
    limits = {"rate_limits": {"services": {"default": {"max_retries": 1}, "llm": {"max_retries": 5}}}}
    assert gatekeeper_from_config(limits, "llm").max_retries == 5
    assert gatekeeper_from_config(limits, "missing").max_retries == 1
    assert gatekeeper_from_config({}, "x").max_retries == 3
