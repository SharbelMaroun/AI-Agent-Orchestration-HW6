"""SDK facade. External consumers (CLI/GUI/tests) use only this.

No business logic lives here — it delegates to the domain services.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from typing import Any

from ..services.match_stream import Frame, heuristic_subgame_stream
from ..services.nl_match import nl_subgame_stream, run_nl_match
from ..services.orchestrator import Orchestrator
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
    ) -> dict[str, Any]:
        """Run a natural-language match and return the serializable summary."""
        return run_nl_match(self.config, backend, gatekeeper)

    def stream_simple_frames(self) -> Iterator[Frame]:
        """Stream the heuristic/smart sub-game turn-by-turn for the live GUI."""
        return heuristic_subgame_stream(self.config)

    def stream_nl_frames(
        self,
        backend: Callable[[str], str] | None = None,
        gatekeeper: ApiGatekeeper | None = None,
        seed: int | None = None,
    ) -> Iterator[Frame]:
        """Stream the natural-language sub-game turn-by-turn for the live GUI."""
        return nl_subgame_stream(self.config, backend, gatekeeper, seed)
