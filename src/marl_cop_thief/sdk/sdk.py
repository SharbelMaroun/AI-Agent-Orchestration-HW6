"""SDK facade. External consumers (CLI/GUI/tests) use only this.

No business logic lives here — it delegates to the domain services.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any

from ..services.bonus import SeriesResult, final_bonus, points_from_config, series_awards
from ..services.match_reporter import Sender
from ..services.match_reporter import send_match_report as _send_match_report
from ..services.match_reporter import send_report as _send_report
from ..services.match_stream import Frame, heuristic_subgame_stream
from ..services.nl_match import nl_subgame_stream, run_nl_match
from ..services.orchestrator import Orchestrator
from ..services.series_runner import run_series as _run_series
from ..shared import config as config_module
from ..shared.gatekeeper import ApiGatekeeper


class Sdk:
    """Single entry point for running matches."""

    def __init__(self, config: dict[str, Any] | None = None) -> None:
        self.config = config if config is not None else config_module.load_config()

    def run_match(self) -> dict[str, Any]:
        """Run a full match and return the serializable summary."""
        return Orchestrator(self.config).play_match()

    def run_nl_match(
        self,
        backend: Callable[[str], str] | None = None,
        gatekeeper: ApiGatekeeper | None = None,
        creative: bool = False,
    ) -> dict[str, Any]:
        """Run a natural-language match and return the serializable summary."""
        return run_nl_match(self.config, backend, gatekeeper, creative)

    def send_match_report(
        self, summary: dict[str, Any], sender: Sender, meta: dict[str, Any] | None = None
    ) -> str | None:
        """Email the JSON match report via ``sender`` (only if reporting.send_real_email)."""
        return _send_match_report(self.config, summary, sender, meta)

    def run_series(
        self, group_a: str, group_b: str, meta: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Play a 6-game role-swap inter-group series; return the bonus report dict."""
        return _run_series(self.config, group_a, group_b, meta)

    def send_report(self, report: dict[str, Any], sender: Sender) -> str | None:
        """Email a pre-built report dict (JSON-only) via ``sender`` if send_real_email."""
        return _send_report(self.config, report, sender)

    def bonus_awards(self, series: SeriesResult) -> dict[str, float]:
        """Per-series inter-group bonus points (the report's ``bonus_claim``; §12.2).

        Award values are read from the config ``bonus`` block (spec defaults if absent).
        """
        return series_awards(series, **points_from_config(self.config))

    def bonus_final(self, group: str, series_list: list[SeriesResult]) -> float:
        """A group's final bonus = average of its per-series awards (config-driven; §12.2)."""
        return final_bonus(group, series_list, **points_from_config(self.config))

    def stream_simple_frames(self) -> Iterator[Frame]:
        """Stream the heuristic/smart sub-game turn-by-turn for the live GUI."""
        return heuristic_subgame_stream(self.config)

    def stream_nl_frames(
        self,
        backend: Callable[[str], str] | None = None,
        gatekeeper: ApiGatekeeper | None = None,
        seed: int | None = None,
        creative: bool = False,
    ) -> Iterator[Frame]:
        """Stream the natural-language sub-game turn-by-turn for the live GUI."""
        return nl_subgame_stream(self.config, backend, gatekeeper, seed, creative)
