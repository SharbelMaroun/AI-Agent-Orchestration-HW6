"""LLM-backed speaker: voice each move in character, with a template fallback.

Produces a ``Speaker`` whose lines are written fresh by the LLM (via the gatekeeper)
each turn, giving varied, in-character speech instead of fixed templates. Any
failure or empty reply falls back to the deterministic :func:`encode`, so offline
runs and provider hiccups never break the match.
"""

from __future__ import annotations

from ...shared.constants import Role
from ...shared.llm_client import LLMClient
from ...shared.models import Action
from ..observation import Observation
from .nl_encode import Speaker, encode
from .prompt_templates import speak_prompt


def llm_speaker(llm: LLMClient) -> Speaker:
    """Return a ``Speaker`` that asks the LLM to voice the move (falls back to a template)."""

    def speak(role: Role, obs: Observation, action: Action) -> str:
        try:
            text = llm.complete(speak_prompt(role, obs, action)).strip().strip('"')
        except Exception:
            return encode(role, obs, action)
        return text or encode(role, obs, action)

    return speak
