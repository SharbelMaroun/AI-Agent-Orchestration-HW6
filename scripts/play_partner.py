"""Play the live inter-group match against the partner's /decide servers.

    uv run python scripts/play_partner.py [--first-role cop|thief]

We own the authoritative game; our policy plays our role and the partner's /decide
plays theirs (3 games each way, §12.1). Prints the JSON report and — if
reporting.send_real_email — emails it to reporting.recipient_email. Partner URLs +
tokens come from .env (PARTNER_COP_URL/TOKEN, PARTNER_THIEF_URL/TOKEN).
"""

from __future__ import annotations

import argparse
import json
import os

import httpx
from dotenv import load_dotenv

from marl_cop_thief.sdk import Sdk
from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.interop_match import make_partner_decide
from marl_cop_thief.services.reporting import build_interop_bonus_report
from marl_cop_thief.shared.config import load_json
from marl_cop_thief.shared.constants import Role
from marl_cop_thief.shared.gatekeeper import gatekeeper_from_config
from marl_cop_thief.shared.partner_client import PartnerClient


def _post(base_url: str, path: str, body: dict, token: str) -> dict:
    r = httpx.post(base_url + path, headers={"Authorization": f"Bearer {token}",
                   "Content-Type": "application/json"}, json=body, timeout=90)
    r.raise_for_status()
    return r.json()


def _client(url_key: str, token_key: str, gk) -> PartnerClient:
    url = os.environ.get(url_key)
    if not url:
        raise SystemExit(f"Set {url_key} (+ {token_key}) in .env — the partner's server.")
    return PartnerClient(url, os.environ.get(token_key, ""), _post, gatekeeper=gk)


def _maybe_email(sdk: Sdk, report: dict) -> None:
    if not sdk.config.get("reporting", {}).get("send_real_email", False):
        print("(email off: set reporting.send_real_email=true to email this report)")
        return
    from marl_cop_thief.services.match_reporter import send_report
    from marl_cop_thief.shared.gmail_client import send_email
    from marl_cop_thief.shared.google_api import gmail_gatekeeper
    from marl_cop_thief.shared.google_auth import build_services

    sd = os.environ.get("MARL_GOOGLE_SECRETS_DIR") or sdk.config.get("google", {}).get("secrets_dir", "")
    gmail, _ = build_services(sd, sdk.config["google"]["scopes"])
    gk = gmail_gatekeeper()
    mid = send_report(sdk.config, report, lambda to, s, b: send_email(gmail, to, s, b, gk))
    rep = sdk.config["reporting"]
    to = rep.get("recipients") or [rep["recipient_email"]]
    print(f"Report emailed to {', '.join(to)}: id={mid}")


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Play the inter-group match vs the partner.")
    parser.add_argument("--first-role", choices=["cop", "thief"], default="cop")
    args = parser.parse_args()

    sdk = Sdk()
    gk = gatekeeper_from_config(load_json("rate_limits.json"), "default")
    engine = GameEngine(*sdk.config["grid_size"], sdk.config["max_moves"], sdk.config["max_barriers"])
    vis = sdk.config["visibility_radius"]
    partner_for = {
        Role.COP: make_partner_decide(_client("PARTNER_COP_URL", "PARTNER_COP_TOKEN", gk), engine, vis),
        Role.THIEF: make_partner_decide(_client("PARTNER_THIEF_URL", "PARTNER_THIEF_TOKEN", gk), engine, vis),
    }
    interop = sdk.run_interop_series(partner_for, Role(args.first_role))
    report = build_interop_bonus_report(sdk.config, interop)
    print(json.dumps(report, indent=2))
    _maybe_email(sdk, report)


if __name__ == "__main__":
    main()
