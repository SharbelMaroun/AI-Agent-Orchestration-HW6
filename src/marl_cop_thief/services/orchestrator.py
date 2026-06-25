"""Match orchestrator: runs the sequence of sub-games autonomously."""

from __future__ import annotations

import random
from typing import Any

from ..shared.constants import Role
from ..shared.models import SubGameResult
from .accumulator import summarize
from .game_engine import GameEngine
from .scoring import score_subgame
from .strategy.heuristic import cop_action, thief_action
from .strategy.smart_cop import smart_cop_action
from .turn_pipeline import Decider, run_turn

# Config-selectable cop policies (config["strategy"]["type"]); thief is always greedy.
COP_POLICIES: dict[str, Decider] = {"heuristic": cop_action, "smart": smart_cop_action}


class Orchestrator:
    """Drives ``num_games`` sub-games to completion and accumulates scores."""

    def __init__(self, config: dict[str, Any]) -> None:
        self.config = config
        width, height = config["grid_size"]
        self.engine = GameEngine(width, height, config["max_moves"], config["max_barriers"])
        self.scoring = config["scoring"]
        self.num_games = config["num_games"]
        self.seed = config.get("seed", 0)
        self.deciders: dict[Role, Decider] = {
            Role.COP: self._select_cop_policy(config),
            Role.THIEF: thief_action,
        }

    @staticmethod
    def _select_cop_policy(config: dict[str, Any]) -> Decider:
        """Pick the cop decider from config (default ``heuristic``); reject unknowns."""
        name = config.get("strategy", {}).get("type", "heuristic")
        if name not in COP_POLICIES:
            raise ValueError(f"Unknown cop strategy {name!r}; choose from {sorted(COP_POLICIES)}")
        return COP_POLICIES[name]

    def play_subgame(self, index: int, rng: random.Random) -> SubGameResult:
        """Play one sub-game to a terminal state and score it."""
        state = self.engine.new_state(rng)
        while not state.done:
            run_turn(self.engine, state, self.deciders)
        return score_subgame(index, state.winner, state.moves_used, self.scoring)

    def play_match(self) -> dict[str, Any]:
        """Play all sub-games (deterministic per seed) and return the summary."""
        results = [
            self.play_subgame(i, random.Random(self.seed + i)) for i in range(self.num_games)
        ]
        return summarize(results)
