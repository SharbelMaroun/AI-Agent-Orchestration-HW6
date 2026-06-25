"""Tests for the gatekept LLM client."""

from marl_cop_thief.shared.gatekeeper import ApiGatekeeper
from marl_cop_thief.shared.llm_client import GatekeptLLM


def test_complete_routes_through_gatekeeper():
    gk = ApiGatekeeper()
    llm = GatekeptLLM(backend=lambda prompt: f"echo:{prompt}", gatekeeper=gk)
    assert llm.complete("hi") == "echo:hi"
    assert gk.calls == 1
