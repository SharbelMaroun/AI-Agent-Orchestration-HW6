"""Smoke tests for the GUI renderer/animator/live-viewer (gui/ omitted from coverage)."""

import queue
import time
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


# --- live viewer: pure threading helpers (no matplotlib, no window) ---

def test_produce_enqueues_frames_then_sentinel():
    q: queue.Queue = queue.Queue()
    sentinel = object()
    live_viewer._produce(iter([("s0", ""), ("s1", "cop: hi")]), q, sentinel)
    assert q.get_nowait() == ("s0", "")
    assert q.get_nowait() == ("s1", "cop: hi")
    assert q.get_nowait() is sentinel  # done marker last


def test_render_tick_renders_one_frame_and_keeps_running():
    q: queue.Queue = queue.Queue()
    q.put(("s", "cap"))
    rendered: list = []
    running = live_viewer._render_tick(q, object(), rendered.append, lambda: None)
    assert running is True and rendered == [("s", "cap")]


def test_render_tick_empty_queue_does_not_block_or_render():
    rendered: list = []
    running = live_viewer._render_tick(queue.Queue(), object(), rendered.append, lambda: None)
    assert running is True and rendered == []  # responsive: returns immediately


def test_render_tick_sentinel_signals_done_without_rendering():
    q: queue.Queue = queue.Queue()
    sentinel = object()
    q.put(sentinel)
    events: list = []
    running = live_viewer._render_tick(
        q, sentinel, lambda f: events.append("render"), lambda: events.append("stop")
    )
    assert running is False and events == ["stop"]


# --- live viewer: play_live wiring with a simulated (mocked) event loop ---

def test_play_live_renders_all_frames_off_thread(monkeypatch):
    fake = MagicMock()
    fig, ax = MagicMock(), MagicMock()
    fake.subplots.return_value = (fig, ax)

    callbacks: list = []
    timer = MagicMock()
    timer.add_callback.side_effect = callbacks.append
    stopped = {"v": False}
    timer.stop.side_effect = lambda: stopped.__setitem__("v", True)
    fig.canvas.new_timer.return_value = timer

    rendered: list = []
    monkeypatch.setattr(live_viewer, "plt", fake)
    monkeypatch.setattr(live_viewer, "render_state", lambda s, a, c: rendered.append((s, c)))

    def fake_show(block=True):  # pump the timer callback like a real event loop
        for _ in range(2000):
            if stopped["v"]:
                break
            for cb in list(callbacks):
                cb()
            time.sleep(0.001)

    fake.show.side_effect = fake_show

    frames = [("s0", ""), ("s1", "cop: x"), ("s2", "thief: y")]
    cfg = {"gui": {"live_backend": "Agg", "poll_interval_ms": 1, "close_on_finish": False}}
    live_viewer.play_live(iter(frames), cfg)
    assert rendered == frames  # all frames drawn via the worker -> queue -> tick path
    assert stopped["v"] is True  # timer stopped on the sentinel
    fake.switch_backend.assert_called_once_with("Agg")


def test_schedule_close_closes_figure_after_hold(monkeypatch):
    fake_plt = MagicMock()
    monkeypatch.setattr(live_viewer, "plt", fake_plt)
    fig = MagicMock()
    closer = MagicMock()
    fig.canvas.new_timer.return_value = closer
    captured: list = []
    closer.add_callback.side_effect = captured.append

    result = live_viewer._schedule_close(fig, 0.01)

    assert result is closer and closer.single_shot is True
    closer.start.assert_called_once()
    captured[0]()  # fire the one-shot callback
    fake_plt.close.assert_called_once_with(fig)


def test_play_live_auto_closes_when_finished(monkeypatch):
    fake = MagicMock()
    fig, ax = MagicMock(), MagicMock()
    fake.subplots.return_value = (fig, ax)
    callbacks: list = []
    timer = MagicMock()
    timer.add_callback.side_effect = callbacks.append
    stopped = {"v": False}
    timer.stop.side_effect = lambda: stopped.__setitem__("v", True)
    fig.canvas.new_timer.return_value = timer
    monkeypatch.setattr(live_viewer, "plt", fake)
    monkeypatch.setattr(live_viewer, "render_state", lambda *a: None)
    scheduled: list = []
    monkeypatch.setattr(live_viewer, "_schedule_close", lambda f, h: scheduled.append((f, h)))

    def fake_show(block=True):
        for _ in range(2000):
            if stopped["v"]:
                break
            for cb in list(callbacks):
                cb()
            time.sleep(0.001)

    fake.show.side_effect = fake_show
    cfg = {"gui": {"live_backend": "Agg", "poll_interval_ms": 1, "close_on_finish": True}}
    live_viewer.play_live(iter([("s", "")]), cfg)
    assert scheduled and scheduled[0][0] is fig  # close scheduled on finish


def test_play_live_falls_back_to_default_backend(monkeypatch):
    fake = MagicMock()
    fake.subplots.return_value = (MagicMock(), MagicMock())
    fake.show.side_effect = lambda block=True: None  # don't pump; just exercise setup
    monkeypatch.setattr(live_viewer, "plt", fake)
    live_viewer.play_live(iter([("s", "")]), {})  # no gui config -> defaults
    fake.switch_backend.assert_called_once_with("TkAgg")
