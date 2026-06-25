"""Write a Calendar event via an injected Calendar service object (no google import)."""

from __future__ import annotations

from typing import Any

from ...shared.models import Meeting


def add_calendar_event(calendar_service: Any, meeting: Meeting) -> dict:
    """Insert ``meeting`` on the primary calendar; return ``{'id', 'htmlLink'}``.

    The Calendar ``service`` is injected; tests pass a fake exposing the same
    ``events().insert(...).execute()`` chain.
    """
    body = {
        "summary": meeting.title,
        "description": meeting.location or "",
        "start": {"dateTime": meeting.start},
        "end": {"dateTime": meeting.end},
    }
    result = (
        calendar_service.events()
        .insert(calendarId="primary", body=body)
        .execute()
    )
    return {"id": result.get("id"), "htmlLink": result.get("htmlLink")}
