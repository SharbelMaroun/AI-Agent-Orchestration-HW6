"""Smoke tests for the GUI renderer/animator/live-viewer (gui/ omitted from coverage)."""

from unittest.mock import MagicMock

from marl_cop_thief.gui import live_viewer
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


def _fake_plt(monkeypatch):
    """Patch the live viewer's matplotlib so nothing opens a real window."""
    fake = MagicMock()
    fake.subplots.return_value = (MagicMock(), MagicMock())
    monkeypatch.setattr(live_viewer, "plt", fake)
    return fake


def test_play_live_renders_every_streamed_frame(monkeypatch):
    fake = _fake_plt(monkeypatch)
    rendered: list[tuple] = []
    monkeypatch.setattr(live_viewer, "render_state", lambda s, ax, msg: rendered.append((s, msg)))
    frames = [("s0", ""), ("s1", "cop: here"), ("s2", "thief: nope")]
    live_viewer.play_live(iter(frames), {"gui": {"live_backend": "Agg", "turn_delay_seconds": 0}})
    assert rendered == frames  # every frame drawn, in order
    fake.switch_backend.assert_called_once_with("Agg")  # config-driven backend
    assert fake.pause.call_count == len(frames)
    fake.show.assert_called_once()  # window stays open at the end


def test_play_live_falls_back_to_default_backend(monkeypatch):
    fake = _fake_plt(monkeypatch)
    monkeypatch.setattr(live_viewer, "render_state", lambda *a: None)
    live_viewer.play_live(iter([("s", "")]), {})  # no gui config -> defaults
    fake.switch_backend.assert_called_once_with("TkAgg")
