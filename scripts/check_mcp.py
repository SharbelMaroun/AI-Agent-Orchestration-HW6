"""Connectivity check for the deployed MCP servers (via our McpClient + gatekeeper).

    uv run python scripts/check_mcp.py

Reads COP_MCP_URL / THIEF_MCP_URL + MCP_AUTH_SECRET from .env, mints a bearer token,
and calls `get_game_status` on each server through `McpClient` (so the same
gatekeeper-routed, token-authenticated path the game uses is exercised end-to-end).
Render free tier cold-starts (~30-60s on the first hit).
"""

from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from fastmcp import Client
from fastmcp.client.auth import BearerAuth

from marl_cop_thief.shared.mcp_auth import TokenAuth
from marl_cop_thief.shared.mcp_transport import McpClient

_TIMEOUT = 90  # generous for Render cold starts


def _invoke(base_url: str, tool: str, params: dict, token: str):
    """Production transport adapter: call a remote MCP tool over HTTP via fastmcp.Client."""
    async def _call():
        auth = BearerAuth(token) if token else None
        async with Client(base_url.rstrip("/") + "/mcp/", auth=auth,
                          timeout=_TIMEOUT, init_timeout=_TIMEOUT) as client:
            result = await client.call_tool(tool, params or {})
            return getattr(result, "data", result)
    return asyncio.run(_call())


def main() -> None:
    load_dotenv()
    secret = os.environ.get("MCP_AUTH_SECRET")
    for role, env_key in (("cop", "COP_MCP_URL"), ("thief", "THIEF_MCP_URL")):
        url = os.environ.get(env_key)
        if not url:
            print(f"{role}: {env_key} not set in .env — skipping")
            continue
        token = TokenAuth(secret).mint(role) if secret else ""
        client = McpClient(url, token, _invoke)
        print(f"{role}: connecting to {url} (auth={'on' if token else 'off'})...")
        try:
            status = client.call_tool("get_game_status")
            print(f"  [OK] get_game_status -> {status}")
        except Exception as exc:  # noqa: BLE001 - report every failure
            print(f"  [FAILED] {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()
