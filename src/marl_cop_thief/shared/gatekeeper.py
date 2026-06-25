"""Centralized API gatekeeper — the single chokepoint for all external calls.

ALL external API calls (LLM, Gmail) route through here (CLAUDE.md §2): it enforces
config-driven rate limiting, FIFO queueing of overflow (never rejecting/crashing),
retries with backoff, a concurrency bound, and per-call logging. A single re-entrant
lock guards shared state (no nested locks ⇒ no deadlock); ``clock``/``sleep`` are
injected so behaviour is deterministically testable offline. See PRD_gatekeeper.md.
"""

from __future__ import annotations

import contextlib
import threading
import time
from collections import deque
from collections.abc import Callable
from dataclasses import replace
from itertools import count
from typing import Any

from .rate_limit import QueueStatus, RateLimitConfig, SlidingWindowLimiter

# Re-check cadence (s) while a call waits behind earlier FIFO calls for a slot.
_POLL_SECONDS = 0.005


class ApiGatekeeper:
    """Executes external calls with rate limiting, FIFO queueing, and retries."""

    def __init__(
        self,
        config: RateLimitConfig | None = None,
        *,
        service: str = "default",
        max_retries: int | None = None,
        clock: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.config = config or RateLimitConfig()
        if max_retries is not None:  # convenience override for no-config construction
            self.config = replace(self.config, max_retries=max_retries)
        self.service = service
        self._clock = clock
        self._sleep = sleep
        self._lock = threading.RLock()
        self._limiter = SlidingWindowLimiter(
            self.config.requests_per_minute, self.config.requests_per_hour
        )
        self._queue: deque[int] = deque()
        self._tickets = count()
        cmax = self.config.concurrent_max
        self._semaphore = threading.BoundedSemaphore(cmax) if cmax else None
        self.calls = 0  # total provider attempts (backward-compatible counter)
        self.log: list[dict[str, Any]] = []
        self._enqueued = 0
        self._drained = 0
        self._peak = 0

    @property
    def max_retries(self) -> int:
        """Maximum retry attempts on transient failure (from config)."""
        return self.config.max_retries

    def execute(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Admit through the FIFO queue/limiter, then call ``fn`` with retries."""
        ticket = self._enqueue()
        try:
            self._await_slot(ticket)
        except BaseException:  # incl. KeyboardInterrupt: never strand a ticket at the head
            self._abandon(ticket)
            raise
        if self._semaphore is not None:
            self._semaphore.acquire()
        try:
            return self._call_with_retries(fn, *args, **kwargs)
        finally:
            if self._semaphore is not None:
                self._semaphore.release()

    def get_queue_status(self) -> QueueStatus:
        """Return a snapshot of queue depth, totals, and the backpressure flag."""
        with self._lock:
            depth = len(self._queue)
            full = bool(self.config.max_queue_depth) and depth >= self.config.max_queue_depth
            return QueueStatus(
                depth, self.config.max_queue_depth, full, self._enqueued, self._drained, self._peak
            )

    def _enqueue(self) -> int:
        """Take a FIFO ticket; alert (log) if the queue is over its max depth."""
        with self._lock:
            ticket = next(self._tickets)
            self._queue.append(ticket)
            self._enqueued += 1
            depth = len(self._queue)
            self._peak = max(self._peak, depth)
            if self.config.max_queue_depth and depth >= self.config.max_queue_depth:
                self.log.append(
                    {"service": self.service, "ok": False, "event": "backpressure", "depth": depth}
                )
            return ticket

    def _abandon(self, ticket: int) -> None:
        """Remove a ticket whose wait was interrupted, so the FIFO never stalls."""
        with self._lock, contextlib.suppress(ValueError):
            self._queue.remove(ticket)

    def _await_slot(self, ticket: int) -> None:
        """Block until this ticket is at the FIFO head and the limiter has a slot."""
        while True:
            with self._lock:
                now = self._clock()
                wait = self._limiter.wait_seconds(now)
                front = self._queue[0] == ticket
                if front and wait <= 0:
                    self._limiter.record(now)
                    self._queue.popleft()
                    self._drained += 1
                    return
            self._sleep(wait if front and wait > 0 else _POLL_SECONDS)

    def _call_with_retries(self, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Call ``fn``, retrying transient failures up to ``max_retries``."""
        attempt = 0
        start = self._clock()
        while True:
            with self._lock:
                self.calls += 1
            try:
                result = fn(*args, **kwargs)
            except Exception as exc:
                if attempt >= self.config.max_retries:
                    self._record(ok=False, attempts=attempt, start=start, error=str(exc))
                    raise
                attempt += 1
                if self.config.retry_after_seconds:
                    self._sleep(self.config.retry_after_seconds)
                with self._lock:  # each retry is a real provider hit — count it against the window
                    self._limiter.record(self._clock())
                continue
            self._record(ok=True, attempts=attempt, start=start, error=None)
            return result

    def _record(self, *, ok: bool, attempts: int, start: float, error: str | None) -> None:
        """Append a per-call monitoring record (service, outcome, retries, latency)."""
        entry: dict[str, Any] = {
            "service": self.service,
            "ok": ok,
            "attempts": attempts,
            "latency": self._clock() - start,
        }
        if error is not None:
            entry["error"] = error
        with self._lock:
            self.log.append(entry)


def gatekeeper_from_config(
    rate_limits: dict[str, Any], service: str = "default", **kwargs: Any
) -> ApiGatekeeper:
    """Build a gatekeeper from a parsed, version-checked ``rate_limits.json`` mapping."""
    cfg = RateLimitConfig.from_rate_limits(rate_limits, service)
    return ApiGatekeeper(cfg, service=service, **kwargs)
