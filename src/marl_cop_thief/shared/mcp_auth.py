"""Token-based auth for the MCP servers: mint, verify, and revoke (assignment §6).

Issues opaque, **tamper-evident** bearer tokens (``<subject>:<nonce>.<hmac>``) that
gate access to a server's tools. Verification is constant-time (HMAC), and a
revocation set allows **immediate access withdrawal**. The signing secret comes
from the environment (never hard-coded). Pure logic — fully unit-testable, no
network. Closes C18 (token auth with revocation) + PRD_mcp_server §6 / S5.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets


class TokenAuth:
    """Mint/verify/revoke HMAC-signed bearer tokens for MCP access control."""

    def __init__(self, secret: str) -> None:
        if not secret:
            raise ValueError("MCP auth secret must be a non-empty string")
        self._secret = secret.encode()
        self._revoked: set[str] = set()

    def _sign(self, payload: str) -> str:
        return hmac.new(self._secret, payload.encode(), hashlib.sha256).hexdigest()

    def mint(self, subject: str) -> str:
        """Issue a signed bearer token for ``subject`` (e.g. a role or group id)."""
        payload = f"{subject}:{secrets.token_hex(16)}"
        return f"{payload}.{self._sign(payload)}"

    def verify(self, token: str) -> str | None:
        """Return the subject if the token is valid and not revoked, else ``None``."""
        if not token or token in self._revoked or "." not in token:
            return None
        payload, _, sig = token.rpartition(".")
        if not hmac.compare_digest(sig, self._sign(payload)):
            return None
        return payload.split(":", 1)[0]

    def revoke(self, token: str) -> None:
        """Withdraw a token's access immediately (subsequent ``verify`` returns None)."""
        self._revoked.add(token)
