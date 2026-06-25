"""One-time Google setup verification (read -> extract -> calendar -> send).

Run AFTER placing ``client_secret.json`` in your secret folder and setting
``MARL_GOOGLE_SECRETS_DIR`` (+ ``OPENAI_API_KEY``) in ``.env``:

    uv run python scripts/google_smoke.py

The first run opens a browser for OAuth consent — **log in as a Test user**
(``sharbelma3@gmail.com``) — and writes ``token.json`` next to the client secret.
It sends a small test email to ``reporting.recipient_email`` (your own dev
address, NOT the lecturer). Each step is defensive: one failure won't abort the rest.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

from marl_cop_thief.services.google_agent.calendar_writer import add_calendar_event
from marl_cop_thief.services.google_agent.email_reader import read_emails
from marl_cop_thief.services.google_agent.meeting_extractor import extract_meeting
from marl_cop_thief.shared.config import load_config
from marl_cop_thief.shared.gmail_client import send_email
from marl_cop_thief.shared.google_api import gmail_gatekeeper
from marl_cop_thief.shared.google_auth import build_services
from marl_cop_thief.shared.llm_backend import select_backend, select_gatekeeper
from marl_cop_thief.shared.llm_client import GatekeptLLM

_SAMPLE = (
    "Hi team, let's meet for the project sync on 2026-07-01T14:00:00 ending "
    "2026-07-01T15:00:00 (Asia/Jerusalem). Thanks!"
)


def _step(name, fn):
    """Run one verification step, reporting success/failure without aborting the rest."""
    try:
        result = fn()
        print(f"  [OK] {name}")
        return result
    except Exception as exc:  # noqa: BLE001 - smoke test reports every failure
        print(f"  [FAILED] {name}: {exc}")
        return None


def main() -> None:
    load_dotenv()
    cfg = load_config()
    google = cfg.get("google", {})
    secrets_dir = os.environ.get("MARL_GOOGLE_SECRETS_DIR") or google.get("secrets_dir", "")
    if not secrets_dir:
        raise SystemExit("Set MARL_GOOGLE_SECRETS_DIR in .env (folder holding client_secret.json).")

    print("Building Google services (first run opens a browser for consent)...")
    services = _step("build_services (OAuth consent + token.json)",
                     lambda: build_services(secrets_dir, google["scopes"]))
    if services is None:
        raise SystemExit("Could not build Google services — check client_secret.json + test user.")
    gmail, calendar = services
    gk = gmail_gatekeeper()  # all Gmail/Calendar calls below route through the gatekeeper (§2)

    print("\n[1/4] read_emails:")
    emails = _step("read_emails", lambda: read_emails(gmail, max_results=3, gatekeeper=gk)) or []
    for e in emails:
        print(f"     - {e['id']}: {e['snippet'][:70]}")

    print("\n[2/4] extract_meeting (LLM):")
    llm = GatekeptLLM(select_backend(cfg), select_gatekeeper(cfg))
    text = emails[0]["snippet"] if emails else _SAMPLE
    meeting = _step("extract_meeting", lambda: extract_meeting(llm, text) or extract_meeting(llm, _SAMPLE))
    print(f"     -> {meeting}")

    print("\n[3/4] add_calendar_event:")
    if meeting is not None:
        tz = cfg.get("reporting", {}).get("timezone")
        event = _step("add_calendar_event",
                      lambda: add_calendar_event(calendar, meeting, timezone=tz, gatekeeper=gk))
        if event:
            print(f"     -> {event.get('htmlLink')}")

    print("\n[4/4] send_email (test, to your dev address):")
    to = cfg["reporting"]["recipient_email"]
    mid = _step("send_email", lambda: send_email(
        gmail, to, "Cop&Thief setup smoke test",
        '{"status":"ok","note":"setup verified"}', gatekeeper=gk))
    if mid:
        print(f"     -> sent message id {mid} to {to}")

    print("\nDone. Verify: token.json created, a Calendar event, and the email in your inbox.")


if __name__ == "__main__":
    main()
