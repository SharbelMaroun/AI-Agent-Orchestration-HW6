"""Tests for the sliding-window limiter and rate-limit config primitives."""

from marl_cop_thief.shared.rate_limit import (
    QueueStatus,
    RateLimitConfig,
    SlidingWindowLimiter,
)


def test_from_mapping_defaults_missing_keys():
    cfg = RateLimitConfig.from_mapping({"requests_per_minute": 20})
    assert cfg.requests_per_minute == 20
    assert cfg.requests_per_hour == 0  # unset -> unlimited
    assert cfg.max_retries == 3  # documented default
    assert cfg.max_queue_depth == 0


def test_from_mapping_reads_all_keys():
    cfg = RateLimitConfig.from_mapping(
        {
            "requests_per_minute": 15,
            "requests_per_hour": 250,
            "concurrent_max": 2,
            "retry_after_seconds": 30,
            "max_retries": 4,
            "max_queue_depth": 50,
        }
    )
    assert cfg.concurrent_max == 2
    assert cfg.retry_after_seconds == 30.0
    assert cfg.max_queue_depth == 50


def test_unlimited_never_waits():
    limiter = SlidingWindowLimiter(0, 0)
    for t in range(100):
        assert limiter.wait_seconds(float(t)) == 0.0
        limiter.record(float(t))


def test_minute_window_waits_then_frees():
    limiter = SlidingWindowLimiter(2, 0)
    limiter.record(0.0)
    limiter.record(1.0)
    # Third call within the minute must wait until the oldest ages out.
    assert limiter.wait_seconds(2.0) == 60.0 - 2.0
    # Once 60s elapse since the first call, a slot frees.
    assert limiter.wait_seconds(60.0) == 0.0


def test_hour_window_waits():
    limiter = SlidingWindowLimiter(0, 1)
    limiter.record(0.0)
    assert limiter.wait_seconds(10.0) == 3600.0 - 10.0
    assert limiter.wait_seconds(3600.0) == 0.0


def test_wait_is_max_of_both_windows():
    limiter = SlidingWindowLimiter(1, 1)
    limiter.record(0.0)
    # Minute slot frees at 60s but hour slot only at 3600s -> the larger wins.
    assert limiter.wait_seconds(30.0) == 3600.0 - 30.0


def test_queue_status_is_a_value_object():
    status = QueueStatus(3, 2, True, 5, 2, 4)
    assert status.depth == 3
    assert status.backpressure is True
    assert status.peak_depth == 4
