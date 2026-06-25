"""Tests for the gatekeeper-routed partner /decide client."""

from marl_cop_thief.shared.gatekeeper import ApiGatekeeper
from marl_cop_thief.shared.partner_client import PartnerClient


def test_decide_routes_through_gatekeeper_with_matching_ids():
    captured = {}

    def fake_post(base, path, body, token):
        captured.update(base=base, path=path, body=body, token=token)
        return {"decision": {"action": {"type": "move", "direction": "left"}}}

    gk = ApiGatekeeper()
    client = PartnerClient("https://x/mcp/", "tok", fake_post, gatekeeper=gk)
    obs = {"protocol_version": "1.0", "request_id": "rid-1", "role": "cop"}
    action = client.decide("cop", obs, "rid-1")

    assert action == {"type": "move", "direction": "left"}
    assert gk.calls == 1  # routed through the central gatekeeper
    assert captured["base"] == "https://x/mcp"  # trailing slash stripped
    assert captured["path"] == "/decide" and captured["token"] == "tok"
    body = captured["body"]
    assert body["request_id"] == "rid-1" == body["observation"]["request_id"]  # ids match (no 409)
    assert body["correlation_id"] == "rid-1" and body["role"] == "cop"


def test_decide_uses_default_gatekeeper_and_protocol_version():
    # no gatekeeper passed -> default unlimited; observation without protocol_version -> "1.0"
    client = PartnerClient(
        "https://y/mcp", "t",
        lambda *a: {"decision": {"action": {"type": "move", "direction": "up"}}},
    )
    assert client.decide("thief", {"request_id": "r"}, "r") == {"type": "move", "direction": "up"}
