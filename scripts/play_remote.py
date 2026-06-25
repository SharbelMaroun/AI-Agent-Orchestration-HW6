"""Play one role of a live cross-network match against a shared MCP host.

    uv run python scripts/play_remote.py --role cop

Both teams run this against the **same** agreed host (`HOST_MCP_URL` + `HOST_MCP_TOKEN`
in .env) — one team `--role cop`, the other `--role thief`. The host runs the shared
game (`run_mcp_server.py --role host`). Each driver polls for its turn, observes, and
submits a move over MCP (gatekeeper-routed, token-authenticated). Prints the final status.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os

from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

from marl_cop_thief.services.match_reporter import send_report
from marl_cop_thief.services.remote_match import build_match_report, play_my_turns, remote_decider
from marl_cop_thief.shared.config import load_config
from marl_cop_thief.shared.mcp_transport import McpClient


def _invoke(base_url: str, tool: str, params: dict, token: str):
    async def _call():
        auth = BearerAuth(token) if token else None
        async with Client(base_url.rstrip("/") + "/mcp/", auth=auth, timeout=90, init_timeout=90) as c:
            result = await c.call_tool(tool, params or {})
            return getattr(result, "data", result)
    return asyncio.run(_call())


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Play one role against a shared MCP host.")
    parser.add_argument("--role", choices=["cop", "thief"], required=True)
    args = parser.parse_args()

    url = os.environ.get("HOST_MCP_URL")
    token = os.environ.get("HOST_MCP_TOKEN", "")
    if not url:
        raise SystemExit("Set HOST_MCP_URL (and HOST_MCP_TOKEN) in .env — the agreed host server.")

    cfg = load_config()
    client = McpClient(url, token, _invoke)
    print(f"Playing role '{args.role}' against {url} ...")
    status = play_my_turns(client, args.role, remote_decider(args.role))
    print(f"Final status: {status}")

    report = build_match_report(cfg, status, args.role)
    print(json.dumps(report, indent=2))
    if cfg.get("reporting", {}).get("send_real_email", False):
        from marl_cop_thief.shared.gmail_client import send_email
        from marl_cop_thief.shared.google_api import gmail_gatekeeper
        from marl_cop_thief.shared.google_auth import build_services

        sd = os.environ.get("MARL_GOOGLE_SECRETS_DIR") or cfg.get("google", {}).get("secrets_dir", "")
        gmail, _ = build_services(sd, cfg["google"]["scopes"])
        gk = gmail_gatekeeper()
        mid = send_report(cfg, report, lambda to, subj, body: send_email(gmail, to, subj, body, gk))
        print(f"Report emailed to {cfg['reporting']['recipient_email']}: id={mid}")
    else:
        print("(email off: set reporting.send_real_email=true to email this report)")


if __name__ == "__main__":
    main()
