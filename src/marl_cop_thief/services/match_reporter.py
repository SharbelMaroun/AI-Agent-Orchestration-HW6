"""Glue: turn a finished match summary into the JSON report email (config-gated).

Ties the match ``summary`` (from the orchestrator/NL match) to the JSON report
builder and an injected ``sender`` (so it is fully offline-testable). Sending is
gated by ``reporting.send_real_email`` — the default is ``false`` so dev/offline
runs never email anyone. The email body is JSON-only (PRD_email_reporting §3/§4).
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .reporting import build_internal_report, report_to_json

# (to, subject, body) -> message_id ; in production a closure over gmail_client.send_email.
Sender = Callable[[str, str, str], str]

_SUBJECT = "Cop & Thief — match report"


def send_report(
    config: dict[str, Any], report: dict[str, Any], sender: Sender, subject: str = _SUBJECT
) -> str | None:
    """Email a pre-built report dict as a JSON-only body, gated by send_real_email."""
    reporting = config.get("reporting", {})
    if not reporting.get("send_real_email", False):
        return None
    return sender(reporting["recipient_email"], subject, report_to_json(report))


def send_match_report(
    config: dict[str, Any],
    summary: dict[str, Any],
    sender: Sender,
    meta: dict[str, Any] | None = None,
) -> str | None:
    """Build the internal JSON report and email it via ``sender`` when enabled.

    Returns the Gmail message id when sent, or ``None`` when
    ``reporting.send_real_email`` is false (default). ``meta`` (group/students/
    repo/MCP URLs) defaults to ``reporting.report_meta`` from config.
    """
    reporting = config.get("reporting", {})
    if not reporting.get("send_real_email", False):
        return None
    report = build_internal_report(config, summary, meta or reporting.get("report_meta", {}))
    return send_report(config, report, sender)
