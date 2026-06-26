"""Build end-of-match JSON reports (internal + inter-group bonus schemas).

The email body is JSON-only (PRD_email_reporting §3): these builders assemble
plain dicts from the accumulated match ``summary`` and group ``meta``, pulling
the timezone from config so the recipient/timezone stay config-driven.
"""

from __future__ import annotations

import json
from typing import Any

from .bonus import SeriesResult, points_from_config, series_awards


def build_internal_report(
    config: dict[str, Any], summary: dict[str, Any], meta: dict[str, Any]
) -> dict[str, Any]:
    """Assemble the single-group internal-game report (schema §3.1)."""
    return {
        "group_name": meta.get("group_name", ""),
        "students": meta.get("students", []),
        "github_repo": meta.get("github_repo", ""),
        "cop_mcp_url": meta.get("cop_mcp_url", ""),
        "thief_mcp_url": meta.get("thief_mcp_url", ""),
        "timezone": config["reporting"]["timezone"],
        "sub_games": summary["sub_games"],
        "totals": summary["totals"],
    }


def build_intergroup_report(
    config: dict[str, Any], summary: dict[str, Any], meta: dict[str, Any]
) -> dict[str, Any]:
    """Assemble the two-group inter-group bonus report (schema §3.2)."""
    return {
        "report_type": "bonus_game",
        "groups": {
            "group_1": meta.get("group_1", ""),
            "group_2": meta.get("group_2", ""),
        },
        "github_repo_group_1": meta.get("github_repo_group_1", ""),
        "github_repo_group_2": meta.get("github_repo_group_2", ""),
        "mcp_url_group_1_cop": meta.get("mcp_url_group_1_cop", ""),
        "mcp_url_group_1_thief": meta.get("mcp_url_group_1_thief", ""),
        "mcp_url_group_2_cop": meta.get("mcp_url_group_2_cop", ""),
        "mcp_url_group_2_thief": meta.get("mcp_url_group_2_thief", ""),
        "timezone": config["reporting"]["timezone"],
        "students_group_1": meta.get("students_group_1", []),
        "students_group_2": meta.get("students_group_2", []),
        "sub_games": summary["sub_games"],
        "totals_by_group": meta.get("totals_by_group", {}),
        "bonus_claim": meta.get("bonus_claim", {}),
        "mutual_agreement": meta.get("mutual_agreement", False),
    }


def build_interop_bonus_report(config: dict[str, Any], interop: dict[str, Any]) -> dict[str, Any]:
    """Assemble the §3.2 ``bonus_game`` report from a live interop result + config.

    ``interop`` is a ``run_interop_series`` result (``totals`` = ``{"us","partner"}`` +
    ``sub_games``). Group 1 = us (``reporting.report_meta``); group 2 = the opponent
    (``reporting.intergroup``); ``bonus_claim`` is computed config-driven via
    :func:`bonus.series_awards` (loser = ``bonus.lose``).
    """
    rep = config["reporting"]
    m1, ig = rep.get("report_meta", {}), rep.get("intergroup", {})
    g1, g2 = m1.get("group_name", ""), ig.get("opponent_group", "")
    totals = {g1: interop["totals"]["us"], g2: interop["totals"]["partner"]}
    meta = {
        "group_1": g1, "group_2": g2,
        "github_repo_group_1": m1.get("github_repo", ""),
        "github_repo_group_2": ig.get("opponent_github_repo", ""),
        "mcp_url_group_1_cop": m1.get("cop_mcp_url", ""),
        "mcp_url_group_1_thief": m1.get("thief_mcp_url", ""),
        "mcp_url_group_2_cop": ig.get("opponent_cop_mcp_url", ""),
        "mcp_url_group_2_thief": ig.get("opponent_thief_mcp_url", ""),
        "students_group_1": m1.get("students", []),
        "students_group_2": ig.get("opponent_students", []),
        "totals_by_group": totals,
        "bonus_claim": series_awards(SeriesResult(totals), **points_from_config(config)),
        "mutual_agreement": True,
    }
    return build_intergroup_report(config, {"sub_games": interop["sub_games"]}, meta)


def report_to_json(report: dict[str, Any]) -> str:
    """Serialize a report to a pretty-printed JSON string (email body is JSON-only).

    ``indent=2`` keeps the body human-readable while staying valid JSON for the
    lecturer's automated ingestion; ``ensure_ascii=False`` renders any unicode as-is.
    """
    return json.dumps(report, indent=2, ensure_ascii=False)
