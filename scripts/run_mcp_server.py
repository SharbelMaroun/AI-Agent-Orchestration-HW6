"""Run one MCP server (cop or thief) over HTTP for cloud / tunnel deployment.

Binds ``0.0.0.0:$PORT`` (Render injects ``PORT``; ngrok just points at a local
port) and — when ``MCP_AUTH_SECRET`` is set — gates access with a bearer token
(`shared.mcp_auth.TokenAuth`). Tools only: no LLM and no API keys on the public
surface (ADR-001). Role from ``--role`` or env ``MCP_ROLE``.

Local:  uv run python scripts/run_mcp_server.py --role cop --port 8001
Render: set MCP_ROLE + MCP_AUTH_SECRET; the Dockerfile runs this with $PORT.
"""

from __future__ import annotations

import argparse
import os
import random

from dotenv import load_dotenv

from marl_cop_thief.services.game_engine import GameEngine
from marl_cop_thief.services.mcp.message_bus import MessageBus
from marl_cop_thief.services.mcp.servers import build_cop_server, build_thief_server
from marl_cop_thief.services.mcp.tools import ToolService
from marl_cop_thief.shared.config import load_config
from marl_cop_thief.shared.mcp_auth import TokenAuth


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a cop/thief MCP server over HTTP.")
    parser.add_argument("--role", choices=["cop", "thief"], default=os.environ.get("MCP_ROLE"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("PORT", "8000")))
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = _parse_args()
    if args.role not in ("cop", "thief"):
        raise SystemExit("Set --role cop|thief (or env MCP_ROLE).")

    cfg = load_config()
    width, height = cfg["grid_size"]
    engine = GameEngine(width, height, cfg["max_moves"], cfg["max_barriers"])
    state = engine.new_state(random.Random(cfg.get("seed", 0)))
    tools = ToolService(
        engine, state, MessageBus(),
        visibility_radius=cfg["visibility_radius"], max_barriers=cfg["max_barriers"],
    )

    secret = os.environ.get("MCP_AUTH_SECRET")
    auth = TokenAuth(secret) if secret else None
    if auth is not None:
        print(f"[auth] bearer-token auth ENABLED. A valid '{args.role}' token (copy for the client):")
        print("   ", auth.mint(args.role))
    else:
        print("[auth] WARNING: MCP_AUTH_SECRET not set -> server is OPEN. Set it before public deploy.")

    build = build_cop_server if args.role == "cop" else build_thief_server
    server = build(tools, auth=auth)
    print(f"[run] {args.role} MCP server -> http://0.0.0.0:{args.port} (transport=http)")
    server.run(transport="http", host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
