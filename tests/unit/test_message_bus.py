"""Tests for the natural-language message bus."""

from marl_cop_thief.services.mcp.message_bus import MessageBus
from marl_cop_thief.shared.constants import Role


def test_message_routed_to_opponent():
    bus = MessageBus()
    bus.send(Role.COP, "I see you in the north.")
    assert bus.pending(Role.THIEF) == 1
    assert bus.pending(Role.COP) == 0
    msg = bus.receive(Role.THIEF)
    assert msg.sender is Role.COP
    assert msg.text == "I see you in the north."


def test_fifo_order():
    bus = MessageBus()
    bus.send(Role.THIEF, "one")
    bus.send(Role.THIEF, "two")
    assert bus.receive(Role.COP).text == "one"
    assert bus.receive(Role.COP).text == "two"


def test_receive_empty_returns_none():
    assert MessageBus().receive(Role.COP) is None


def test_peek_last_returns_newest_without_consuming():
    bus = MessageBus()
    bus.send(Role.COP, "first")
    bus.send(Role.COP, "second")
    assert bus.peek_last(Role.THIEF).text == "second"
    assert bus.pending(Role.THIEF) == 2  # peek does not pop
    assert bus.peek_last(Role.COP) is None  # empty inbox
