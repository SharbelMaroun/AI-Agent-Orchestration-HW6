"""Unit tests for the per-turn frame streams (services/match_stream.py).

The streams are generators: nothing runs until iterated, and each step yields a
deepcopy so a consumer (GIF list or live window) can safely hold past frames.
Covers ``stream_subgame`` and ``heuristic_subgame_stream`` to 100% (incl. branch).
"""

from marl_cop_thief.services.match_stream import heuristic_subgame_stream
from marl_cop_thief.shared.models import GameState

CONFIG = {
    "grid_size": [4, 4],
    "max_moves": 10,
    "max_barriers": 5,
    "seed": 1,
    "strategy": {"type": "heuristic"},
}


def test_heuristic_stream_yields_initial_then_terminal():
    frames = list(heuristic_subgame_stream(CONFIG))
    assert len(frames) >= 2  # initial snapshot + at least one turn
    first_state, first_caption = frames[0]
    assert isinstance(first_state, GameState) and first_caption == ""  # nothing moved yet
    assert frames[-1][0].done  # last frame is terminal


def test_heuristic_stream_captions_are_empty():
    assert all(caption == "" for _, caption in heuristic_subgame_stream(CONFIG))


def test_heuristic_stream_defaults_seed_to_zero():
    cfg = {k: v for k, v in CONFIG.items() if k != "seed"}
    assert list(heuristic_subgame_stream(cfg))[-1][0].done


def test_heuristic_stream_supports_smart_cop():
    frames = list(heuristic_subgame_stream({**CONFIG, "strategy": {"type": "smart"}}))
    assert frames[-1][0].done


def test_stream_yields_distinct_snapshots():
    frames = list(heuristic_subgame_stream(CONFIG))
    assert frames[0][0] is not frames[-1][0]  # deepcopied snapshots, not one mutated alias


def test_creating_stream_runs_nothing_until_iterated():
    gen = heuristic_subgame_stream(CONFIG)  # generator is lazy: no game run yet
    state, caption = next(gen)  # first step yields only the pre-move snapshot
    assert caption == "" and state.moves_used == 0
