"""Smart thief evasion (Phase 4): flee the cop while keeping escape room.

The greedy thief ([`heuristic.thief_action`]) maximises *only* distance and, with a
fixed direction-order tie-break, drifts into one wall/corner (the "always goes left"
artefact). This instead ranks moves by :func:`evade_key` — distance from the cop,
then own mobility, then centrality — so the thief uses the whole board and is much
harder to corner. Config-selectable via ``strategy.thief_type``; a drop-in Decider.
"""

from __future__ import annotations

from ...shared.constants import ActionKind
from ...shared.models import Action, GameState
from ..game_engine import GameEngine
from .evasion import evade_key


def smart_thief_action(engine: GameEngine, state: GameState) -> Action:
    """Evade with foresight: flee the cop while maximising escape room (else stay)."""
    moves = [a for a in engine.legal_actions(state) if a.kind is ActionKind.MOVE]
    if not moves:
        return Action.stay()
    return max(
        moves,
        key=lambda a: evade_key(
            engine.board, state.barriers, state.thief.step(a.dx, a.dy), state.cop
        ),
    )
