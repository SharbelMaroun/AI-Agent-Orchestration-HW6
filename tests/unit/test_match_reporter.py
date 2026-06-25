"""Tests for the config-gated match report-email glue."""

import json

from marl_cop_thief.services.match_reporter import send_match_report

SUMMARY = {"sub_games": [{"index": 0, "winner": "cop"}], "totals": {"cop": 90, "thief": 40}}
CONFIG = {
    "reporting": {
        "recipient_email": "dev@example.com",
        "timezone": "Asia/Jerusalem",
        "send_real_email": True,
        "report_meta": {"group_name": "Team-X", "github_repo": "https://example.com/repo"},
    }
}


def test_disabled_by_default_does_not_send():
    calls = []
    cfg = {"reporting": {"recipient_email": "x", "timezone": "Asia/Jerusalem"}}  # no send flag
    out = send_match_report(cfg, SUMMARY, lambda to, s, b: calls.append((to, s, b)) or "id")
    assert out is None and calls == []  # default: never emails


def test_sends_json_only_body_to_recipient_when_enabled():
    sent = {}

    def sender(to, subject, body):
        sent.update(to=to, subject=subject, body=body)
        return "msg-1"

    out = send_match_report(CONFIG, SUMMARY, sender)
    assert out == "msg-1"
    assert sent["to"] == "dev@example.com"
    payload = json.loads(sent["body"])  # body must be valid JSON only
    assert payload["totals"] == {"cop": 90, "thief": 40}
    assert payload["timezone"] == "Asia/Jerusalem"
    assert payload["group_name"] == "Team-X"  # meta pulled from reporting.report_meta


def test_explicit_meta_overrides_config_meta():
    sent = {}
    send_match_report(CONFIG, SUMMARY, lambda to, s, b: sent.update(b=b) or "id",
                      meta={"group_name": "Override", "github_repo": "r"})
    assert json.loads(sent["b"])["group_name"] == "Override"
