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
import os

from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

from marl_cop_thief.services.remote_match import play_my_turns, remote_decider
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

    client = McpClient(url, token, _invoke)
    print(f"Playing role '{args.role}' against {url} ...")
    status = play_my_turns(client, args.role, remote_decider(args.role))
    print(f"Final status: {status}")


if __name__ == "__main__":
    main()
