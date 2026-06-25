"""Read Gmail messages via an injected Gmail service object (no google import)."""

from __future__ import annotations

from typing import Any

from ...shared.gatekeeper import ApiGatekeeper
from ...shared.google_api import execute_request


def read_emails(
    gmail_service: Any,
    query: str = "",
    max_results: int = 10,
    gatekeeper: ApiGatekeeper | None = None,
) -> list[dict]:
    """Return ``[{'id', 'snippet'}]`` for messages matching ``query``.

    The Gmail ``service`` is injected; tests pass a fake exposing the same
    ``users().messages().list(...).execute()`` / ``get(...).execute()`` chain. Each
    network ``.execute()`` is routed through ``gatekeeper`` when supplied (§2).
    """
    messages = gmail_service.users()
    listing = execute_request(
        messages.messages().list(userId="me", q=query, maxResults=max_results), gatekeeper
    )
    emails: list[dict] = []
    for ref in listing.get("messages", []):
        full = execute_request(messages.messages().get(userId="me", id=ref["id"]), gatekeeper)
        emails.append({"id": full.get("id"), "snippet": full.get("snippet", "")})
    return emails
