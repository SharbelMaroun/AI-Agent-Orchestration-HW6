"""Tests for the gatekeeper-routed MCP client transport."""

from marl_cop_thief.shared.gatekeeper import ApiGatekeeper
from marl_cop_thief.shared.mcp_transport import McpClient


def _recorder():
    calls = []

    def invoke(base_url, tool, params, token):
        calls.append((base_url, tool, params, token))
        return {"tool": tool, "ok": True}

    return invoke, calls


def test_call_tool_passes_url_tool_params_and_token():
    invoke, calls = _recorder()
    client = McpClient("https://cop-mcp.example/", "tok-123", invoke)
    out = client.call_tool("get_observation", role="cop")
    assert out == {"tool": "get_observation", "ok": True}
    assert calls == [("https://cop-mcp.example", "get_observation", {"role": "cop"}, "tok-123")]


def test_base_url_trailing_slash_is_stripped():
    invoke, _ = _recorder()
    assert McpClient("https://x/", "t", invoke).base_url == "https://x"


def test_calls_route_through_the_gatekeeper():
    invoke, _ = _recorder()
    gk = ApiGatekeeper()
    McpClient("https://x", "t", invoke, gatekeeper=gk).call_tool("verify_location")
    assert gk.calls == 1  # the shared gatekeeper fronted the remote call
