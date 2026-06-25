"""Run a 6-game inter-group series (3-cop/3-thief role-swap) and report it.

    uv run python scripts/run_series.py --group-a Team-Alpha --group-b Team-Beta

Plays the series via the SDK, prints the inter-group JSON report (report_type:
bonus_game, totals_by_group, bonus_claim), and — if reporting.send_real_email is
true and Google OAuth is set up — emails it to reporting.recipient_email.
(Local sim of both groups' agents; for a live cross-group match the opponent's
agents are driven over their remote MCP servers — same scoring + report.)
"""

from __future__ import annotations

import argparse
import json

from dotenv import load_dotenv

from marl_cop_thief.sdk import Sdk


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Run an inter-group bonus series.")
    parser.add_argument("--group-a", default="Team-Alpha")
    parser.add_argument("--group-b", default="Team-Beta")
    args = parser.parse_args()

    sdk = Sdk()
    report = sdk.run_series(args.group_a, args.group_b)
    print(json.dumps(report, indent=2))
    print(f"\nbonus_claim: {report['bonus_claim']}  | totals: {report['totals_by_group']}")

    if sdk.config.get("reporting", {}).get("send_real_email", False):
        import os

        from marl_cop_thief.shared.gmail_client import send_email
        from marl_cop_thief.shared.google_api import gmail_gatekeeper
        from marl_cop_thief.shared.google_auth import build_services
        sd = os.environ.get("MARL_GOOGLE_SECRETS_DIR") or sdk.config.get("google", {}).get("secrets_dir", "")
        gmail, _ = build_services(sd, sdk.config["google"]["scopes"])
        gk = gmail_gatekeeper()
        mid = sdk.send_report(report, lambda to, subj, body: send_email(gmail, to, subj, body, gk))
        print(f"Series report emailed: id={mid}")


if __name__ == "__main__":
    main()
