"""Write a Calendar event via an injected Calendar service object (no google import)."""

from __future__ import annotations

from typing import Any

from ...shared.models import Meeting


def add_calendar_event(calendar_service: Any, meeting: Meeting, timezone: str | None = None) -> dict:
    """Insert ``meeting`` on the primary calendar; return ``{'id', 'htmlLink'}``.

    The Calendar ``service`` is injected; tests pass a fake exposing the same
    ``events().insert(...).execute()`` chain. ``timezone`` (e.g. ``Asia/Jerusalem``)
    is attached to start/end when given — the API rejects offset-less datetimes without it.
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
    result = (
        calendar_service.events()
        .insert(calendarId="primary", body=body)
        .execute()
    )
    return {"id": result.get("id"), "htmlLink": result.get("htmlLink")}
