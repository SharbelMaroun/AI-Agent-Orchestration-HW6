"""Core domain models for the pursuit game (Phase 1).

These are plain dataclasses with no business logic; the engine operates on them.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .constants import ActionKind, Event, Role


@dataclass(frozen=True)
class Position:
    """A cell on the grid."""

    x: int
    y: int

    def step(self, dx: int, dy: int) -> Position:
        """Return the position offset by ``(dx, dy)`` (no bounds check)."""
        return Position(self.x + dx, self.y + dy)


@dataclass(frozen=True)
class Action:
    """An action an agent proposes on its turn."""

    kind: ActionKind
    dx: int = 0
    dy: int = 0

    @classmethod
    def move(cls, dx: int, dy: int) -> Action:
        return cls(ActionKind.MOVE, dx, dy)

    @classmethod
    def stay(cls) -> Action:
        return cls(ActionKind.STAY)

    @classmethod
    def place_barrier(cls) -> Action:
        return cls(ActionKind.PLACE_BARRIER)


@dataclass
class GameState:
    """Mutable authoritative state of a single sub-game."""

    width: int
    height: int
    cop: Position
    thief: Position
    barriers: set[Position] = field(default_factory=set)
    moves_used: int = 0
    cop_barriers_used: int = 0
    to_move: Role = Role.THIEF  # thief moves first
    winner: Role | None = None
    done: bool = False


@dataclass(frozen=True)
class TurnResult:
    """Outcome of applying one action."""

    actor: Role
    action: Action
    event: Event
    state: GameState


@dataclass(frozen=True)
class SubGameResult:
    """Scored result of one completed sub-game."""

    index: int
    winner: Role
    moves_used: int
    cop_score: int
    thief_score: int


@dataclass(frozen=True)
class Message:
    """A free-text natural-language message from one agent to the other."""

    sender: Role
    text: str
