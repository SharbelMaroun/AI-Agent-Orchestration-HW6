"""Authoritative game engine: state machine, legality, capture (Phase 1).

The engine is the single source of truth. Agents only *propose* actions; the
engine validates them and reports the resulting event.
"""

from __future__ import annotations

import random

from ..shared.constants import DIRECTIONS_8, ActionKind, Event, Role
from ..shared.models import Action, GameState, Position, TurnResult
from .barriers import can_place, place
from .board import Board, passable


class GameEngine:
    """Deterministic finite state machine for one pursuit sub-game."""

    def __init__(self, width: int, height: int, max_moves: int, max_barriers: int) -> None:
        self.board = Board(width, height)
        self.max_moves = max_moves
        self.max_barriers = max_barriers

    def new_state(self, rng: random.Random) -> GameState:
        """Create a fresh state with two distinct random start cells."""
        cells = list(self.board.all_cells())
        cop = rng.choice(cells)
        thief = rng.choice([c for c in cells if c != cop])
        return GameState(self.board.width, self.board.height, cop, thief)

    def _actor_pos(self, state: GameState) -> Position:
        return state.cop if state.to_move is Role.COP else state.thief

    def legal_actions(self, state: GameState) -> list[Action]:
        """All legal actions for the agent whose turn it is."""
        pos = self._actor_pos(state)
        actions = [Action.stay()]
        for dx, dy in DIRECTIONS_8:
            if passable(self.board, state.barriers, pos.step(dx, dy)):
                actions.append(Action.move(dx, dy))
        if state.to_move is Role.COP and can_place(state, self.max_barriers):
            actions.append(Action.place_barrier())
        return actions

    def apply(self, state: GameState, action: Action) -> TurnResult:
        """Validate and apply ``action`` for the current actor; advance the state."""
        actor = state.to_move
        if state.done:
            return TurnResult(actor, action, Event.ILLEGAL, state)
        event = self._apply_action(state, action, actor)
        if event is Event.ILLEGAL:
            return TurnResult(actor, action, Event.ILLEGAL, state)
        state.moves_used += 1
        if state.cop == state.thief:
            state.winner, state.done, event = Role.COP, True, Event.CAPTURE
        elif state.moves_used >= self.max_moves:
            state.winner, state.done, event = Role.THIEF, True, Event.MAX_MOVES_REACHED
        else:
            state.to_move = Role.COP if actor is Role.THIEF else Role.THIEF
        return TurnResult(actor, action, event, state)

    def _apply_action(self, state: GameState, action: Action, actor: Role) -> Event:
        if action.kind is ActionKind.STAY:
            return Event.NONE
        if action.kind is ActionKind.PLACE_BARRIER:
            if actor is not Role.COP or not can_place(state, self.max_barriers):
                return Event.ILLEGAL
            place(state)
            return Event.BARRIER_PLACED
        # ActionKind.MOVE
        if (action.dx, action.dy) not in DIRECTIONS_8:
            return Event.ILLEGAL
        dest = self._actor_pos(state).step(action.dx, action.dy)
        if not passable(self.board, state.barriers, dest):
            return Event.ILLEGAL
        if actor is Role.COP:
            state.cop = dest
        else:
            state.thief = dest
        return Event.NONE
