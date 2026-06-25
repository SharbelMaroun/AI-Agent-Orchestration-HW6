"""Mint a bearer token for the deployed MCP servers — to share with a partner.

    uv run python scripts/mint_token.py            # default subject "partner"
    uv run python scripts/mint_token.py --subject cop

Reads MCP_AUTH_SECRET from .env (the same value set on Render) and prints a
signed token. Your partner sends it as `Authorization: Bearer <token>` to your
cop/thief MCP URLs. One token authorizes BOTH servers (auth is by signature, not
role). To revoke everyone's access, rotate MCP_AUTH_SECRET on Render + locally.
"""

from __future__ import annotations

import argparse
import os

from dotenv import load_dotenv

from marl_cop_thief.shared.mcp_auth import TokenAuth


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Mint an MCP bearer token.")
    parser.add_argument("--subject", default="partner", help="label embedded in the token")
    args = parser.parse_args()

    secret = os.environ.get("MCP_AUTH_SECRET")
    if not secret:
        raise SystemExit("Set MCP_AUTH_SECRET in .env (same value as on Render).")
    token = TokenAuth(secret).mint(args.subject)
    print(token)
    print(f"\nShare with your partner (works for both URLs):\n  Authorization: Bearer {token}")


if __name__ == "__main__":
    main()
