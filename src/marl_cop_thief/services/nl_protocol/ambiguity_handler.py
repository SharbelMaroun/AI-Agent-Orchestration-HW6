"""Defensive parsing of free text into structured hints. Never raises."""

from __future__ import annotations

import re

from ...shared.models import Position

_COORD = re.compile(r"(-?\d+)\s*,\s*(-?\d+)")


def parse_position(text: str | None) -> Position | None:
    """Extract an ``x,y`` coordinate from arbitrary text, or ``None`` if absent."""
    if not text:
        return None
    match = _COORD.search(text)
    if match is None:
        return None
    return Position(int(match.group(1)), int(match.group(2)))
