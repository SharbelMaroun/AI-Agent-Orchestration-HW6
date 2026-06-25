"""Send email via an injected Gmail service object (no google import)."""

from __future__ import annotations

import base64
from email.message import EmailMessage
from typing import Any

from .gatekeeper import ApiGatekeeper
from .google_api import execute_request


def send_email(
    gmail_service: Any,
    to: str,
    subject: str,
    body: str,
    gatekeeper: ApiGatekeeper | None = None,
) -> str:
    """Send a real email and return the resulting Gmail message id.

    The Gmail ``service`` is injected; tests pass a fake exposing the same
    ``users().messages().send(...).execute()`` chain. The network ``.execute()`` is
    routed through ``gatekeeper`` when supplied (CLAUDE.md §2 — all external calls).
    """
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    request = gmail_service.users().messages().send(userId="me", body={"raw": raw})
    result = execute_request(request, gatekeeper)
    return result["id"]
