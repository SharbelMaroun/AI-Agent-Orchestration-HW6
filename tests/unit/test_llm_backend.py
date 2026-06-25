"""Tests for LLM backend selection (offline; the real OpenAI call is omitted)."""

from marl_cop_thief.shared.llm_backend import (
    echo_backend,
    select_backend,
    select_gatekeeper,
)


def test_echo_backend_is_offline():
    assert echo_backend("hello world") == "hello world"


def test_select_backend_without_key_uses_echo(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert select_backend({}) is echo_backend


def test_select_backend_with_key_uses_openai(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-used")
    backend = select_backend({"llm": {"model": "gpt-4o-mini"}})
    assert callable(backend)
    assert backend is not echo_backend


def test_select_gatekeeper_without_key_is_unlimited(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    gk = select_gatekeeper({})
    assert gk.config.requests_per_minute == 0  # 0 == unlimited; offline runs stay fast


def test_select_gatekeeper_with_key_loads_rate_limits_file(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key-not-used")
    gk = select_gatekeeper({})  # loads the real config/rate_limits.json (no network)
    assert gk.service == "llm"
    assert gk.config.requests_per_minute == 20  # value lives in the file -> no code edit to change
