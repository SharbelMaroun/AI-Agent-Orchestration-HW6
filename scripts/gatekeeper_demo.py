"""Offline demonstration of the API gatekeeper (Phase 9).

Reproducible: `uv run python scripts/gatekeeper_demo.py`. Uses an injected fake
clock so it runs instantly with no real sleeping and no provider. It shows three
required behaviours: config-driven rate limiting, FIFO queue + drain on reset,
and a queue-full backpressure alert. Outputs a staircase figure to assets/ and a
log to results/ for the README report (R.9).
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from marl_cop_thief.shared.config import load_json  # noqa: E402
from marl_cop_thief.shared.gatekeeper import (  # noqa: E402
    ApiGatekeeper,
    gatekeeper_from_config,
)
from marl_cop_thief.shared.rate_limit import RateLimitConfig  # noqa: E402

DPI = 150


class _FakeClock:
    """Manually-advanced clock; the fake sleep pushes time forward (no real wait)."""

    def __init__(self) -> None:
        self.t = 0.0

    def now(self) -> float:
        return self.t

    def sleep(self, seconds: float) -> None:
        self.t += seconds


def simulate(requests_per_minute: int, n_calls: int) -> tuple[list[float], ApiGatekeeper]:
    """Fire ``n_calls`` through a rate-limited gatekeeper; return admission times."""
    clock = _FakeClock()
    gk = ApiGatekeeper(
        RateLimitConfig(requests_per_minute=requests_per_minute),
        service="llm",
        clock=clock.now,
        sleep=clock.sleep,
    )
    admit_minutes: list[float] = []
    for _ in range(n_calls):
        gk.execute(lambda: admit_minutes.append(clock.t / 60.0))
    return admit_minutes, gk


def fig_throughput(rpm: int, n: int) -> list[float]:
    """Plot cumulative admitted calls vs simulated time under an RPM cap."""
    admit, _ = simulate(rpm, n)
    fig, ax = plt.subplots(figsize=(5.5, 4))
    ax.step(admit, range(1, n + 1), where="post", marker="o", color="tab:blue")
    ax.set_title(f"Gatekeeper throughput under a {rpm}/min limit ({n} calls)")
    ax.set_xlabel("simulated time (minutes)")
    ax.set_ylabel("cumulative calls admitted")
    ax.grid(True)
    fig.tight_layout()
    fig.savefig("assets/gatekeeper_throughput.png", dpi=DPI)
    return admit


def backpressure_demo(max_queue_depth: int, waiters: int) -> str:
    """Pile ``waiters`` calls into the queue and report the backpressure status."""
    gk = ApiGatekeeper(RateLimitConfig(max_queue_depth=max_queue_depth))
    for _ in range(waiters):
        gk._enqueue()
    return str(gk.get_queue_status())


def main() -> None:
    lines = ["API Gatekeeper demonstration (offline, fake clock)", "=" * 56]

    limits = load_json("rate_limits.json")
    gk = gatekeeper_from_config(limits, "llm")
    lines.append(
        f"Loaded llm limits from rate_limits.json: rpm={gk.config.requests_per_minute}, "
        f"rph={gk.config.requests_per_hour}, max_queue_depth={gk.config.max_queue_depth}"
    )

    rpm, n = 3, 9
    admit = fig_throughput(rpm, n)
    lines.append("")
    lines.append(f"Rate limiting + FIFO drain: {n} calls under a {rpm}/min cap (no rejections):")
    for i, minute in enumerate(admit):
        lines.append(f"  call {i + 1}: admitted at t={minute:.1f} min")

    lines.append("")
    lines.append("Backpressure: 5 callers queued behind a max_queue_depth of 3:")
    lines.append(f"  {backpressure_demo(3, 5)}")

    with open("results/gatekeeper_demo.txt", "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("Wrote assets/gatekeeper_throughput.png and results/gatekeeper_demo.txt")


if __name__ == "__main__":
    main()
