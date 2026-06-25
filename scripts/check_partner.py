"""Probe the partner's decision servers: /health, /identity, /capabilities.

    uv run python scripts/check_partner.py

Confirms reachability + Bearer auth for PARTNER_COP_URL / PARTNER_THIEF_URL (.env).
"""

from __future__ import annotations

import os

import httpx
from dotenv import load_dotenv


def _get(base: str, token: str, path: str) -> tuple[int, str]:
    r = httpx.get(base + path, headers={"Authorization": f"Bearer {token}"}, timeout=90)
    return r.status_code, r.text[:200]


def main() -> None:
    load_dotenv()
    pairs = [("cop", "PARTNER_COP_URL", "PARTNER_COP_TOKEN"),
             ("thief", "PARTNER_THIEF_URL", "PARTNER_THIEF_TOKEN")]
    for role, url_key, tok_key in pairs:
        url = os.environ.get(url_key)
        if not url:
            print(f"{role}: {url_key} not set — skipping")
            continue
        token = os.environ.get(tok_key, "")
        print(f"\n{role}: {url}")
        for path in ("/health", "/identity", "/capabilities"):
            try:
                code, body = _get(url, token, path)
                print(f"  GET {path}: {code} {body}")
            except Exception as exc:  # noqa: BLE001 - report every failure
                print(f"  GET {path}: FAILED {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
