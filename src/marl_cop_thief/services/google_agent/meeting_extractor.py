"""LLM-assisted, never-raising extraction of a Meeting from email text."""

from __future__ import annotations

from ...shared.llm_client import LLMClient
from ...shared.models import Meeting

_PROMPT = (
    "Extract the meeting from the email below. Respond with EXACTLY one line "
    "in the format 'title|start_iso|end_iso' (ISO-8601 datetimes), or the word "
    "NONE if there is no meeting.\n\nEMAIL:\n{text}"
)


def extract_meeting(llm: LLMClient, email_text: str) -> Meeting | None:
    """Ask ``llm`` to parse ``email_text`` into a Meeting; return None on failure."""
    try:
        response = llm.complete(_PROMPT.format(text=email_text))
    except Exception:
        return None
    parts = [piece.strip() for piece in str(response).split("|")]
    if len(parts) < 3:
        return None
    title, start, end = parts[0], parts[1], parts[2]
    if not title or not start or not end:
        return None
    return Meeting(title=title, start=start, end=end)
