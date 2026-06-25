"""Tests for the gatekeeper's rate limiting, FIFO queue, backpressure, and locks."""

import threading
import time

import pytest

from marl_cop_thief.shared.gatekeeper import ApiGatekeeper
from marl_cop_thief.shared.rate_limit import RateLimitConfig


class _FakeClock:
    """A manually-advanced clock; the fake sleep pushes time forward."""

    def __init__(self) -> None:
        self.t = 0.0

    def now(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.t += seconds


def test_overflow_is_queued_and_drained_not_rejected():
    clock = _FakeClock()
    cfg = RateLimitConfig(requests_per_minute=2)
    gk = ApiGatekeeper(cfg, clock=clock.now, sleep=clock.sleep)

    order: list[int] = []
    for i in range(3):
        gk.execute(lambda i=i: order.append(i))

    assert order == [0, 1, 2]  # every call completed — none rejected
    assert clock.t == 60.0  # the 3rd call waited one window, then drained
    status = gk.get_queue_status()
    assert status.drained == 3
    assert status.depth == 0


def test_backpressure_alert_when_queue_exceeds_max():
    gk = ApiGatekeeper(RateLimitConfig(max_queue_depth=2))
    for _ in range(3):  # simulate three callers waiting at once
        gk._enqueue()

    status = gk.get_queue_status()
    assert status.depth == 3
    assert status.max_depth == 2
    assert status.backpressure is True
    assert status.peak_depth == 3
    assert any(entry.get("event") == "backpressure" for entry in gk.log)


def test_thread_safe_call_accounting():
    gk = ApiGatekeeper()  # unlimited -> no waiting, exercises only the locks

    def work() -> None:
        gk.execute(lambda: None)

    threads = [threading.Thread(target=work) for _ in range(25)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert gk.calls == 25  # no lost increments under contention
    assert len(gk.log) == 25
    assert gk.get_queue_status().depth == 0


def test_backpressure_clears_when_queue_drains_below_max():
    clock = _FakeClock()
    cfg = RateLimitConfig(requests_per_minute=5, max_queue_depth=2)
    gk = ApiGatekeeper(cfg, clock=clock.now, sleep=clock.sleep)

    tickets = [gk._enqueue() for _ in range(3)]
    assert gk.get_queue_status().backpressure is True  # depth 3 > max 2

    gk._await_slot(tickets[0])  # depth 2 == max
    assert gk.get_queue_status().backpressure is True  # full at the boundary (>= semantics)

    gk._await_slot(tickets[1])  # depth 1 < max
    assert gk.get_queue_status().backpressure is False  # flag clears once the queue drains


def test_interrupted_wait_abandons_ticket_so_fifo_never_stalls():
    clock = _FakeClock()

    def boom(_seconds: float) -> None:
        raise KeyboardInterrupt  # simulate Ctrl+C while waiting for a rate-limit slot

    gk = ApiGatekeeper(RateLimitConfig(requests_per_minute=1), clock=clock.now, sleep=boom)
    gk.execute(lambda: None)  # first call consumes the only slot this minute
    with pytest.raises(KeyboardInterrupt):
        gk.execute(lambda: None)  # second call must wait -> sleep raises mid-wait

    assert gk.get_queue_status().depth == 0  # the interrupted ticket was abandoned, not stranded
    gk._abandon(9999)  # removing an absent ticket is a safe no-op


def test_retries_count_against_rate_limiter():
    cfg = RateLimitConfig(requests_per_minute=2)
    gk = ApiGatekeeper(cfg)
    state = {"n": 0}

    def flaky() -> str:
        state["n"] += 1
        if state["n"] < 3:
            raise ValueError("transient")
        return "ok"

    assert gk.execute(flaky) == "ok"  # 3 provider attempts in one execute()
    # 1 slot recorded at admission + 2 for the retries == 3; the next call is now throttled.
    assert gk._limiter.wait_seconds(gk._clock()) > 0


def test_concurrent_max_bounds_inflight_calls():
    gk = ApiGatekeeper(RateLimitConfig(concurrent_max=2))
    state = {"inflight": 0, "peak": 0}
    lock = threading.Lock()

    def fn() -> None:
        with lock:
            state["inflight"] += 1
            state["peak"] = max(state["peak"], state["inflight"])
        time.sleep(0.02)
        with lock:
            state["inflight"] -= 1

    threads = [threading.Thread(target=lambda: gk.execute(fn)) for _ in range(6)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert state["peak"] <= 2  # the semaphore capped concurrency
