"""Natural-language message bus between the two agents (FIFO inbox per role)."""

from __future__ import annotations

from ...shared.constants import Role
from ...shared.models import Message

_OPPONENT = {Role.COP: Role.THIEF, Role.THIEF: Role.COP}


class MessageBus:
    """Routes free-text messages to the opponent's inbox; FIFO delivery."""

    def __init__(self) -> None:
        self._inbox: dict[Role, list[Message]] = {Role.COP: [], Role.THIEF: []}

    def send(self, sender: Role, text: str) -> None:
        self._inbox[_OPPONENT[sender]].append(Message(sender, text))

    def receive(self, role: Role) -> Message | None:
        box = self._inbox[role]
        return box.pop(0) if box else None

    def peek_last(self, role: Role) -> Message | None:
        """Return ``role``'s most recent inbox message without consuming it (for the GUI)."""
        box = self._inbox[role]
        return box[-1] if box else None

    def pending(self, role: Role) -> int:
        return len(self._inbox[role])
