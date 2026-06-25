"""Send email via an injected Gmail service object (no google import)."""

from __future__ import annotations

import base64
from email.message import EmailMessage
from typing import Any


def send_email(gmail_service: Any, to: str, subject: str, body: str) -> str:
    """Send a real email and return the resulting Gmail message id.

    The Gmail ``service`` is injected; tests pass a fake exposing the same
    ``users().messages().send(...).execute()`` chain.
    """
    msg = EmailMessage()
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = (
        gmail_service.users()
        .messages()
        .send(userId="me", body={"raw": raw})
        .execute()
    )
    return result["id"]
