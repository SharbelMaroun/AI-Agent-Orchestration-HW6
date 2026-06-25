"""Tests for LLM backend selection (offline; the real OpenAI call is omitted)."""

from marl_cop_thief.shared.llm_backend import echo_backend, select_backend


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
