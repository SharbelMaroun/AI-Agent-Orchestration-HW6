"""Gatekeeper-routed client for the partner's custom ``/decide`` protocol (v1.0).

Every call carries a bearer token and routes through the :class:`ApiGatekeeper`
(rate limit, retry, log) — CLAUDE.md §2. The low-level ``post(base_url, path,
body, token)`` transport is injected (prod: an httpx adapter; tests: a fake), so
this stays offline-testable. The partner requires ``observation.request_id`` to
equal the envelope ``request_id``, so :meth:`decide` stamps both from one id.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .gatekeeper import ApiGatekeeper

# (base_url, path, body, token) -> parsed JSON response.
Post = Callable[[str, str, dict[str, Any], str], dict[str, Any]]


class PartnerClient:
    """One partner decision server (cop or thief): token-authed, gatekeeper-routed."""

    def __init__(
        self, base_url: str, token: str, post: Post, gatekeeper: ApiGatekeeper | None = None
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self._token = token
        self._post = post
        self._gatekeeper = gatekeeper or ApiGatekeeper()

    def decide(self, role: str, observation: dict[str, Any], request_id: str) -> dict[str, Any]:
        """POST one observation to ``/decide`` and return the chosen action dict."""
        body = {
            "protocol_version": observation.get("protocol_version", "1.0"),
            "request_id": request_id,
            "correlation_id": request_id,
            "role": role,
            "observation": observation,
        }
        resp = self._gatekeeper.execute(self._post, self.base_url, "/decide", body, self._token)
        return resp["decision"]["action"]
