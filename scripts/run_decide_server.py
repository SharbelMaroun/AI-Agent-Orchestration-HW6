"""Run our REST /decide server so a partner can HOST the game and pull our agent's move.

    uv run python scripts/run_decide_server.py        # binds 0.0.0.0:$PORT

Mirrors the partner's protocol v1.0: GET /health|/identity|/capabilities, POST /decide.
Bearer-token auth via MCP_AUTH_SECRET (shared.mcp_auth.TokenAuth). Stateless: the caller
owns the game; we return one of the legal_actions (services.decide_service). This is an
interop adapter only — our MCP servers stay tools-only (ADR-001).
"""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from dotenv import load_dotenv

from marl_cop_thief.services.decide_service import decide_action
from marl_cop_thief.shared.mcp_auth import TokenAuth

_NAME = "sharnamr-decide"
_INFO = {"protocol_version": "1.0", "role": "any", "status": "ok", "server_name": _NAME,
         "operations": ["health", "identity", "capabilities", "decide"]}


class _Handler(BaseHTTPRequestHandler):
    auth: TokenAuth | None = None

    def _send(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _authed(self) -> bool:
        if self.auth is None:
            return True
        header = self.headers.get("Authorization", "")
        token = header[7:] if header.startswith("Bearer ") else ""
        return self.auth.verify(token) is not None

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path.rstrip("/").rsplit("/", 1)[-1] in ("health", "identity", "capabilities"):
            self._send(200, _INFO)
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if not self.path.rstrip("/").endswith("decide"):
            self._send(404, {"error": "not found"})
            return
        if not self._authed():
            self._send(401, {"error": "unauthorized"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            body = json.loads(self.rfile.read(length) or b"{}")
            obs, rid = body.get("observation", {}), body.get("request_id")
            if obs.get("request_id") not in (None, rid):
                self._send(409, {"error": "observation request_id mismatch"})
                return
            action = decide_action(obs)
        except Exception as exc:  # noqa: BLE001 - report any failure as 500
            self._send(500, {"error": f"internal server error: {exc}"})
            return
        decision = {"protocol_version": "1.0", "request_id": rid,
                    "role": obs.get("role"), "action": action}
        self._send(200, {"protocol_version": "1.0", "request_id": rid,
                         "correlation_id": rid, "role": obs.get("role"), "decision": decision})

    def log_message(self, *args: object) -> None:  # silence default request logging
        pass


def main() -> None:
    load_dotenv()
    secret = os.environ.get("MCP_AUTH_SECRET")
    _Handler.auth = TokenAuth(secret) if secret else None
    port = int(os.environ.get("PORT", "8000"))
    if _Handler.auth is not None:
        print(f"[auth] bearer-token ENABLED. Token to share with the partner:\n   {_Handler.auth.mint('opponent')}")
    else:
        print("[auth] WARNING: MCP_AUTH_SECRET not set -> server is OPEN. Set it before deploy.")
    print(f"[run] /decide server -> http://0.0.0.0:{port}")
    ThreadingHTTPServer(("0.0.0.0", port), _Handler).serve_forever()


if __name__ == "__main__":
    main()
