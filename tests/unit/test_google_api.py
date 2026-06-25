"""Tests: Google API calls route through the central gatekeeper (CLAUDE.md §2)."""

from __future__ import annotations

from marl_cop_thief.shared.gatekeeper import ApiGatekeeper
from marl_cop_thief.shared.google_api import execute_request, gmail_gatekeeper


class _Request:
    """Minimal stand-in for a google-api-client request object."""

    def __init__(self, value):
        self._value = value
        self.executed = 0

    def execute(self):
        self.executed += 1
        return self._value


def test_execute_request_calls_directly_without_gatekeeper():
    req = _Request("v")
    assert execute_request(req) == "v"
    assert req.executed == 1


def test_execute_request_routes_through_gatekeeper():
    req = _Request("v")
    gk = ApiGatekeeper()
    assert execute_request(req, gk) == "v"
    assert req.executed == 1
    assert gk.calls == 1  # the request was admitted + counted by the gatekeeper


def test_gmail_gatekeeper_is_config_driven():
    gk = gmail_gatekeeper()
    assert isinstance(gk, ApiGatekeeper)
    assert gk.service == "gmail"
    # limits come from config/rate_limits.json (gmail: 15/min) — never hard-coded
    assert gk.config.requests_per_minute == 15
