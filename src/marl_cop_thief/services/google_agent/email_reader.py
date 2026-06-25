"""Read Gmail messages via an injected Gmail service object (no google import)."""

from __future__ import annotations

from typing import Any


def read_emails(
    gmail_service: Any, query: str = "", max_results: int = 10
) -> list[dict]:
    """Return ``[{'id', 'snippet'}]`` for messages matching ``query``.

    The Gmail ``service`` is injected; tests pass a fake exposing the same
    ``users().messages().list(...).execute()`` / ``get(...).execute()`` chain.
    """
    messages = gmail_service.users()
    listing = (
        messages.messages()
        .list(userId="me", q=query, maxResults=max_results)
        .execute()
    )
    emails: list[dict] = []
    for ref in listing.get("messages", []):
        full = messages.messages().get(userId="me", id=ref["id"]).execute()
        emails.append({"id": full.get("id"), "snippet": full.get("snippet", "")})
    return emails
