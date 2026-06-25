"""Write a Calendar event via an injected Calendar service object (no google import)."""

from __future__ import annotations

from typing import Any

from ...shared.gatekeeper import ApiGatekeeper
from ...shared.google_api import execute_request
from ...shared.models import Meeting


def add_calendar_event(
    calendar_service: Any,
    meeting: Meeting,
    timezone: str | None = None,
    gatekeeper: ApiGatekeeper | None = None,
) -> dict:
    """Insert ``meeting`` on the primary calendar; return ``{'id', 'htmlLink'}``.

    The Calendar ``service`` is injected; tests pass a fake exposing the same
    ``events().insert(...).execute()`` chain. ``timezone`` (e.g. ``Asia/Jerusalem``)
    is attached to start/end when given — the API rejects offset-less datetimes
    without it. The network ``.execute()`` routes through ``gatekeeper`` when supplied (§2).
    """
    start: dict[str, str] = {"dateTime": meeting.start}
    end: dict[str, str] = {"dateTime": meeting.end}
    if timezone:
        start["timeZone"] = timezone
        end["timeZone"] = timezone
    body = {
        "summary": meeting.title,
        "description": meeting.location or "",
        "start": start,
        "end": end,
    }
    request = calendar_service.events().insert(calendarId="primary", body=body)
    result = execute_request(request, gatekeeper)
    return {"id": result.get("id"), "htmlLink": result.get("htmlLink")}
