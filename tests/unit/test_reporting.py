"""Tests for the JSON report builders (offline, fakes only)."""

from __future__ import annotations

import json

from marl_cop_thief.services.reporting import (
    build_intergroup_report,
    build_internal_report,
    build_interop_bonus_report,
    report_to_json,
)

CONFIG = {"reporting": {"timezone": "Asia/Jerusalem"}}
SUMMARY = {
    "sub_games": [{"index": 0, "winner": "cop", "moves_used": 10}],
    "totals": {"cop": 90, "thief": 40},
}


def test_internal_report_required_keys_and_passthrough():
    meta = {
        "group_name": "Team-Alpha",
        "students": ["a", "b"],
        "github_repo": "https://example/repo",
        "cop_mcp_url": "https://cop",
        "thief_mcp_url": "https://thief",
    }
    report = build_internal_report(CONFIG, SUMMARY, meta)
    for key in (
        "group_name",
        "students",
        "github_repo",
        "cop_mcp_url",
        "thief_mcp_url",
        "timezone",
        "sub_games",
        "totals",
    ):
        assert key in report
    assert report["group_name"] == "Team-Alpha"
    assert report["students"] == ["a", "b"]
    assert report["timezone"] == "Asia/Jerusalem"
    assert report["sub_games"] is SUMMARY["sub_games"]
    assert report["totals"] is SUMMARY["totals"]


def test_internal_report_safe_defaults():
    report = build_internal_report(CONFIG, SUMMARY, {})
    assert report["group_name"] == ""
    assert report["students"] == []
    assert report["github_repo"] == ""
    assert report["cop_mcp_url"] == ""
    assert report["thief_mcp_url"] == ""
    assert report["timezone"] == "Asia/Jerusalem"


def test_intergroup_report_required_keys_and_passthrough():
    meta = {
        "group_1": "Team-Alpha",
        "group_2": "Team-Beta",
        "github_repo_group_1": "https://a",
        "github_repo_group_2": "https://b",
        "mcp_url_group_1_cop": "https://a-cop",
        "mcp_url_group_1_thief": "https://a-thief",
        "mcp_url_group_2_cop": "https://b-cop",
        "mcp_url_group_2_thief": "https://b-thief",
        "students_group_1": ["a"],
        "students_group_2": ["b"],
        "totals_by_group": {"Team-Alpha": 60, "Team-Beta": 80},
        "bonus_claim": {"Team-Alpha": 7, "Team-Beta": 10},
        "mutual_agreement": True,
    }
    report = build_intergroup_report(CONFIG, SUMMARY, meta)
    for key in (
        "report_type",
        "groups",
        "github_repo_group_1",
        "github_repo_group_2",
        "mcp_url_group_1_cop",
        "mcp_url_group_1_thief",
        "mcp_url_group_2_cop",
        "mcp_url_group_2_thief",
        "timezone",
        "students_group_1",
        "students_group_2",
        "sub_games",
        "totals_by_group",
        "bonus_claim",
        "mutual_agreement",
    ):
        assert key in report
    assert report["report_type"] == "bonus_game"
    assert report["groups"] == {"group_1": "Team-Alpha", "group_2": "Team-Beta"}
    assert report["timezone"] == "Asia/Jerusalem"
    assert report["sub_games"] is SUMMARY["sub_games"]
    assert report["mutual_agreement"] is True
    assert report["totals_by_group"] == {"Team-Alpha": 60, "Team-Beta": 80}


def test_intergroup_report_safe_defaults():
    report = build_intergroup_report(CONFIG, SUMMARY, {})
    assert report["groups"] == {"group_1": "", "group_2": ""}
    assert report["github_repo_group_1"] == ""
    assert report["github_repo_group_2"] == ""
    assert report["mcp_url_group_1_cop"] == ""
    assert report["mcp_url_group_1_thief"] == ""
    assert report["mcp_url_group_2_cop"] == ""
    assert report["mcp_url_group_2_thief"] == ""
    assert report["students_group_1"] == []
    assert report["students_group_2"] == []
    assert report["totals_by_group"] == {}
    assert report["bonus_claim"] == {}
    assert report["mutual_agreement"] is False


def test_report_to_json_round_trips():
    report = build_internal_report(CONFIG, SUMMARY, {"group_name": "G"})
    body = report_to_json(report)
    assert isinstance(body, str)
    assert json.loads(body) == report


def test_interop_bonus_report_from_config_and_result():
    config = {
        "reporting": {
            "timezone": "Asia/Jerusalem",
            "report_meta": {"group_name": "G1", "students": ["a"], "github_repo": "r1",
                            "cop_mcp_url": "c1", "thief_mcp_url": "t1"},
            "intergroup": {"opponent_group": "G2", "opponent_github_repo": "r2",
                           "opponent_students": ["b"], "opponent_cop_mcp_url": "c2",
                           "opponent_thief_mcp_url": "t2"},
        },
        "bonus": {"win": 10, "lose": 7, "tie": 5, "void": 0},
    }
    interop = {"totals": {"us": 60, "partner": 40}, "sub_games": [{"index": 0}]}
    rep = build_interop_bonus_report(config, interop)
    assert rep["report_type"] == "bonus_game"
    assert rep["groups"] == {"group_1": "G1", "group_2": "G2"}
    assert rep["github_repo_group_2"] == "r2" and rep["students_group_2"] == ["b"]
    assert rep["totals_by_group"] == {"G1": 60, "G2": 40}
    assert rep["bonus_claim"] == {"G1": 10.0, "G2": 7.0}  # winner 10, loser 7 (config)
    assert rep["mutual_agreement"] is True
