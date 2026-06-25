"""Build real Gmail/Calendar services from OAuth secrets (google libs lazy).

This is the ONLY module that touches google libraries, and it imports them
lazily inside the function so the rest of the package stays offline-testable.
Omitted from coverage (requires real google libraries and a browser consent).
"""

from __future__ import annotations

import os
from typing import Any


def build_services(secrets_dir: str, scopes: list[str]) -> tuple[Any, Any]:
    """Return ``(gmail_service, calendar_service)`` built from OAuth secrets."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    token_path = os.path.join(secrets_dir, "token.json")
    client_path = os.path.join(secrets_dir, "client_secret.json")
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes)
    if creds is None or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_path, scopes)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w", encoding="utf-8") as handle:
            handle.write(creds.to_json())
    gmail = build("gmail", "v1", credentials=creds)
    calendar = build("calendar", "v3", credentials=creds)
    return gmail, calendar
