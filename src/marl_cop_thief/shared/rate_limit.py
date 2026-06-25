"""Config-driven rate-limiting primitives for the API gatekeeper.

A :class:`SlidingWindowLimiter` tracks call timestamps over a minute and an hour
window and reports how long a new call must wait before a slot frees. A limit of
``0`` means *unlimited* — the default for local/offline runs where there is no
provider to protect. These primitives live apart from the gatekeeper so the
windowing maths is unit-testable in isolation and the gatekeeper file stays well
within the 150-line budget (CLAUDE.md §3).
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any

from .config import validate_version
from .version import RATE_LIMIT_VERSION

_MINUTE = 60.0
_HOUR = 3600.0


@dataclass(frozen=True)
class RateLimitConfig:
    """Per-service limits, mirroring one entry of ``config/rate_limits.json``."""

    requests_per_minute: int = 0
    requests_per_hour: int = 0
    concurrent_max: int = 0
    retry_after_seconds: float = 0.0
    max_retries: int = 3
    max_queue_depth: int = 0

    @classmethod
    def from_mapping(cls, cfg: dict[str, Any]) -> RateLimitConfig:
        """Build a config from a parsed mapping, defaulting any missing key."""
        return cls(
            requests_per_minute=int(cfg.get("requests_per_minute", 0)),
            requests_per_hour=int(cfg.get("requests_per_hour", 0)),
            concurrent_max=int(cfg.get("concurrent_max", 0)),
            retry_after_seconds=float(cfg.get("retry_after_seconds", 0.0)),
            max_retries=int(cfg.get("max_retries", 3)),
            max_queue_depth=int(cfg.get("max_queue_depth", 0)),
        )

    @classmethod
    def from_rate_limits(cls, rate_limits: dict[str, Any], service: str = "default") -> RateLimitConfig:
        """Select+validate a service's limits from a parsed ``rate_limits.json`` mapping.

        A non-empty ``rate_limits`` block is version-checked (CLAUDE.md §5); an empty
        mapping falls back to defaults so callers can pass ``{}`` for "unlimited".
        """
        block = rate_limits.get("rate_limits", {})
        if block:
            validate_version(block, RATE_LIMIT_VERSION)
        services = block.get("services", {})
        return cls.from_mapping(services.get(service, services.get("default", {})))


@dataclass(frozen=True)
class QueueStatus:
    """Snapshot of the gatekeeper's FIFO queue for monitoring/backpressure."""

    depth: int
    max_depth: int
    backpressure: bool
    enqueued: int
    drained: int
    peak_depth: int


class SlidingWindowLimiter:
    """Tracks recent call times; reports whether a call may proceed now."""

    def __init__(self, requests_per_minute: int, requests_per_hour: int) -> None:
        self._rpm = requests_per_minute
        self._rph = requests_per_hour
        self._minute: deque[float] = deque()
        self._hour: deque[float] = deque()

    def _prune(self, now: float) -> None:
        """Drop timestamps that have aged out of each window."""
        while self._minute and now - self._minute[0] >= _MINUTE:
            self._minute.popleft()
        while self._hour and now - self._hour[0] >= _HOUR:
            self._hour.popleft()

    def wait_seconds(self, now: float) -> float:
        """Seconds until a slot frees; ``0.0`` means a call may proceed now."""
        self._prune(now)
        waits = []
        if self._rpm and len(self._minute) >= self._rpm:
            waits.append(_MINUTE - (now - self._minute[0]))
        if self._rph and len(self._hour) >= self._rph:
            waits.append(_HOUR - (now - self._hour[0]))
        return max(waits) if waits else 0.0

    def record(self, now: float) -> None:
        """Register an admitted call against both windows."""
        self._minute.append(now)
        self._hour.append(now)
