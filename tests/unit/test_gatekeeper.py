"""Tests for the API gatekeeper: retries, logging, config, and queue status."""

import pytest

from marl_cop_thief.shared.config import ConfigError
from marl_cop_thief.shared.gatekeeper import ApiGatekeeper, gatekeeper_from_config
from marl_cop_thief.shared.rate_limit import RateLimitConfig


def test_success_is_single_call():
    gk = ApiGatekeeper()
    assert gk.execute(lambda x: x + 1, 41) == 42
    assert gk.calls == 1
    assert gk.log[-1]["ok"] is True
    assert gk.log[-1]["service"] == "default"
    assert "latency" in gk.log[-1]


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
    assert gk.calls == 3  # 3 provider attempts
    entry = gk.log[-1]
    assert entry["ok"] is True and entry["attempts"] == 2 and entry["service"] == "default"


def test_raises_after_exhausting_retries():
    def always_fail() -> None:
        raise RuntimeError("down")

    gk = ApiGatekeeper(max_retries=2)
    with pytest.raises(RuntimeError):
        gk.execute(always_fail)
    assert gk.calls == 3  # 1 + 2 retries
    assert gk.log[-1]["ok"] is False
    assert gk.log[-1]["error"] == "down"


def test_backoff_sleeps_retry_after_between_attempts():
    slept: list[float] = []
    cfg = RateLimitConfig(retry_after_seconds=30.0, max_retries=2)
    gk = ApiGatekeeper(cfg, sleep=slept.append)

    def always_fail() -> None:
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        gk.execute(always_fail)
    assert slept == [30.0, 30.0]  # backoff honoured between the 2 retries


def test_max_retries_property_reflects_config():
    assert ApiGatekeeper(RateLimitConfig(max_retries=7)).max_retries == 7


def test_gatekeeper_from_config_uses_service_then_default():
    limits = {
        "rate_limits": {
            "version": "1.00",
            "services": {"default": {"max_retries": 1}, "llm": {"max_retries": 5}},
        }
    }
    assert gatekeeper_from_config(limits, "llm").max_retries == 5
    assert gatekeeper_from_config(limits, "missing").max_retries == 1
    assert gatekeeper_from_config({}, "x").max_retries == 3  # empty block -> defaults, no version check


def test_gatekeeper_from_config_binds_service_and_limits():
    limits = {
        "rate_limits": {
            "version": "1.00",
            "services": {"gmail": {"requests_per_minute": 15, "max_queue_depth": 50}},
        }
    }
    gk = gatekeeper_from_config(limits, "gmail")
    assert gk.service == "gmail"
    assert gk.config.requests_per_minute == 15
    assert gk.get_queue_status().max_depth == 50


def test_gatekeeper_from_config_rejects_wrong_version():
    bad = {"rate_limits": {"version": "9.99", "services": {"default": {}}}}
    with pytest.raises(ConfigError):
        gatekeeper_from_config(bad)


def test_queue_status_empty_by_default():
    status = ApiGatekeeper().get_queue_status()
    assert status.depth == 0
    assert status.backpressure is False
    assert status.enqueued == 0
