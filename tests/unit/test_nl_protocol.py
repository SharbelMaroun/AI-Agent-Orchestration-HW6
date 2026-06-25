"""Tests for NL encode/decode, ambiguity handling, and prompt templates."""

from marl_cop_thief.services.board import Board
from marl_cop_thief.services.nl_protocol.ambiguity_handler import parse_position
from marl_cop_thief.services.nl_protocol.nl_decode import interpret
from marl_cop_thief.services.nl_protocol.nl_encode import encode
from marl_cop_thief.services.nl_protocol.prompt_templates import interpret_prompt, system_prompt
from marl_cop_thief.services.observation import Observation
from marl_cop_thief.shared.constants import Role
from marl_cop_thief.shared.models import Action, Position


class _LLM:
    def __init__(self, reply: str | None = None, fail: bool = False):
        self.reply = reply
        self.fail = fail

    def complete(self, prompt: str) -> str:
        if self.fail:
            raise RuntimeError("provider down")
        return self.reply if self.reply is not None else prompt


def _obs(role: Role, pos: Position) -> Observation:
    return Observation(role, pos, None, (pos,), ())


def test_parse_position():
    assert parse_position("near 2,3 maybe") == Position(2, 3)
    assert parse_position("no coords here") is None
    assert parse_position("") is None
    assert parse_position(None) is None


def test_encode_cop_reveals_thief_hides():
    cop_msg = encode(Role.COP, _obs(Role.COP, Position(1, 2)), Action.move(1, 0))
    assert "1,2" in cop_msg and "east" in cop_msg
    thief_msg = encode(Role.THIEF, _obs(Role.THIEF, Position(4, 4)), Action.move(-1, 0))
    assert "4,4" not in thief_msg  # thief is vague
    assert encode(Role.COP, _obs(Role.COP, Position(0, 0)), Action.stay()) == "Holding my position for now."
    assert "wall" in encode(Role.COP, _obs(Role.COP, Position(2, 2)), Action.place_barrier())


def test_interpret_extracts_position():
    board = Board(5, 5)
    assert interpret(_LLM("3,1"), "msg", None, board) == Position(3, 1)


def test_interpret_keeps_prior_on_failure_or_garbage():
    board = Board(5, 5)
    prior = Position(2, 2)
    assert interpret(_LLM(fail=True), "msg", prior, board) == prior  # LLM error
    assert interpret(_LLM("unknown"), "msg", prior, board) == prior  # no coords
    assert interpret(_LLM("99,99"), "msg", prior, board) == prior    # out of bounds


def test_prompt_templates():
    assert "cop" in system_prompt(Role.COP)
    assert "thief" in system_prompt(Role.THIEF)
    assert "x,y" in interpret_prompt("hello")
