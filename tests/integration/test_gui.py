"""Smoke tests for the GUI renderer/animator (gui/ is omitted from coverage)."""

from marl_cop_thief.gui.board_renderer import save_state_png
from marl_cop_thief.gui.match_animator import animate_match, animate_nl_match
from marl_cop_thief.shared.models import GameState, Position

CONFIG = {
    "grid_size": [4, 4],
    "max_moves": 10,
    "num_games": 1,
    "max_barriers": 5,
    "seed": 1,
    "visibility_radius": 1,
    "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5},
}


def test_render_state_png(tmp_path):
    out = tmp_path / "state.png"
    save_state_png(GameState(5, 5, Position(0, 0), Position(4, 4)), str(out))
    assert out.exists() and out.stat().st_size > 0


def test_animate_match_gif(tmp_path):
    out = tmp_path / "match.gif"
    animate_match(CONFIG, str(out))
    assert out.exists() and out.stat().st_size > 0


def test_animate_nl_match_gif(tmp_path):
    out = tmp_path / "match_nl.gif"  # offline echo backend -> no network
    animate_nl_match(CONFIG, path=str(out))
    assert out.exists() and out.stat().st_size > 0


def test_animate_smart_strategy_gif(tmp_path):
    out = tmp_path / "smart.gif"
    animate_match({**CONFIG, "strategy": {"type": "smart"}}, str(out))
    assert out.exists() and out.stat().st_size > 0
