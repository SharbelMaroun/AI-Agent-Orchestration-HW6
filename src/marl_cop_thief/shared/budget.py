"""Budget management: forecast, real-time spend tracking, and overrun alerts.

Estimates LLM spend from the live gatekeeper call count and a config-driven
per-call cost, flags an **alert** at a threshold fraction of the monthly cap and
an **overrun** past it, and forecasts spend for a projected number of calls.
Pure and config-driven (no I/O) so it is fully unit-testable. Closes audit
C14/C20 (cost forecasting + real-time monitoring + budget-overrun alerts).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class BudgetConfig:
    """Config-driven budget limits (from ``config.json`` → ``llm.budget``)."""

    monthly_cap_usd: float = 0.0
    alert_threshold: float = 0.8
    usd_per_call: float = 0.0

    @classmethod
    def from_mapping(cls, mapping: dict[str, Any]) -> BudgetConfig:
        """Build from a mapping, defaulting any missing keys."""
        return cls(
            float(mapping.get("monthly_cap_usd", 0.0)),
            float(mapping.get("alert_threshold", 0.8)),
            float(mapping.get("usd_per_call", 0.0)),
        )

    @classmethod
    def from_config(cls, config: dict[str, Any]) -> BudgetConfig:
        """Read the ``llm.budget`` block from a loaded config."""
        return cls.from_mapping(config.get("llm", {}).get("budget", {}))


@dataclass(frozen=True)
class BudgetStatus:
    """Snapshot of budget consumption (a value object for logging/printing)."""

    calls: int
    spent_usd: float
    cap_usd: float
    remaining_usd: float
    alert: bool
    over_budget: bool


class BudgetTracker:
    """Tracks running spend from the gatekeeper's call count; raises no exceptions."""

    def __init__(self, config: BudgetConfig) -> None:
        self.config = config
        self.calls = 0

    def record(self, calls: int = 1) -> None:
        """Add ``calls`` external calls to the running total (sync from gatekeeper.calls)."""
        self.calls += calls

    @property
    def spent_usd(self) -> float:
        return round(self.calls * self.config.usd_per_call, 6)

    @property
    def remaining_usd(self) -> float:
        return round(max(self.config.monthly_cap_usd - self.spent_usd, 0.0), 6)

    @property
    def alert(self) -> bool:
        """True once spend reaches ``alert_threshold`` of the cap (cap 0 = disabled)."""
        cap = self.config.monthly_cap_usd
        return cap > 0 and self.spent_usd >= self.config.alert_threshold * cap

    @property
    def over_budget(self) -> bool:
        cap = self.config.monthly_cap_usd
        return cap > 0 and self.spent_usd >= cap

    def forecast_usd(self, projected_calls: int) -> float:
        """Forecast spend for a projected number of calls (e.g., calls/match × matches)."""
        return round(projected_calls * self.config.usd_per_call, 6)

    def status(self) -> BudgetStatus:
        return BudgetStatus(
            self.calls, self.spent_usd, self.config.monthly_cap_usd,
            self.remaining_usd, self.alert, self.over_budget,
        )
