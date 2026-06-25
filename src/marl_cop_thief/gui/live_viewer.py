"""Live, real-time match window: render each turn the instant it is computed.

Unlike the GIF animator (headless ``Agg`` -> file), this switches matplotlib to an
interactive backend at runtime (config ``gui.live_backend``, default ``TkAgg``) and
draws every ``(state, caption)`` frame as it streams off the engine.

**Responsiveness.** A turn can block for seconds (the NL match makes an LLM call per
turn), so producing frames on the GUI thread would freeze the window. We run the frame
generator on a **daemon worker thread** that pushes onto a ``queue.Queue`` (plus a
sentinel when done), while the Matplotlib/Tk event loop owns the **main thread** and
drains one frame per tick via ``fig.canvas.new_timer``. Rendering only; frames come from
the SDK streams (SDK-only). Omitted from coverage (interactive).
"""

from __future__ import annotations

import queue
import threading
from collections.abc import Callable, Iterable
from typing import Any

import matplotlib.pyplot as plt

from ..shared.models import GameState
from .board_renderer import render_state

# Fallback defaults if config omits a ``gui`` block (real values live in config.json).
_DEFAULT_BACKEND = "TkAgg"
_DEFAULT_POLL_MS = 150
_DEFAULT_CLOSE_ON_FINISH = True
_DEFAULT_HOLD_SECONDS = 2.5

Frame = tuple[GameState, str]


def _schedule_close(fig: Any, hold_seconds: float) -> Any:
    """One-shot timer that closes ``fig`` after a final hold, so ``plt.show`` returns."""
    closer = fig.canvas.new_timer(interval=max(int(hold_seconds * 1000), 1))
    closer.single_shot = True
    closer.add_callback(lambda: plt.close(fig))
    closer.start()
    return closer


def _produce(frames: Iterable[Frame], q: queue.Queue, sentinel: object) -> None:
    """Worker-thread body: drain the (possibly blocking) stream into the queue."""
    for frame in frames:
        q.put(frame)
    q.put(sentinel)


def _render_tick(
    q: queue.Queue, sentinel: object, render: Callable[[Frame], None], on_done: Callable[[], None]
) -> bool:
    """Render at most one queued frame. Return ``False`` once the sentinel is seen."""
    try:
        item = q.get_nowait()
    except queue.Empty:
        return True  # nothing ready yet; keep the loop alive
    if item is sentinel:
        on_done()
        return False
    render(item)
    return True


def play_live(
    frames: Iterable[Frame], config: dict[str, Any], title: str = "Cop & Thief"
) -> None:
    """Open an interactive window; compute turns off-thread so the GUI stays responsive."""
    gui_cfg = config.get("gui", {})
    plt.switch_backend(gui_cfg.get("live_backend", _DEFAULT_BACKEND))
    poll_ms = int(gui_cfg.get("poll_interval_ms", _DEFAULT_POLL_MS))
    max_moves = config.get("max_moves")
    fig, ax = plt.subplots(figsize=(5.5, 6))
    fig.suptitle(title)

    q: queue.Queue = queue.Queue()
    sentinel = object()
    threading.Thread(target=_produce, args=(frames, q, sentinel), daemon=True).start()
    cop_trail: list = []
    thief_trail: list = []

    def render(frame: Frame) -> None:
        state, caption = frame
        cop_trail.append(state.cop)
        thief_trail.append(state.thief)
        render_state(state, ax, caption, max_moves=max_moves,
                     cop_trail=cop_trail, thief_trail=thief_trail)
        fig.tight_layout()
        fig.canvas.draw_idle()

    timer = fig.canvas.new_timer(interval=poll_ms)
    keep_alive: list[Any] = []  # retain the one-shot close timer past on_finish

    def on_finish() -> None:
        timer.stop()
        if gui_cfg.get("close_on_finish", _DEFAULT_CLOSE_ON_FINISH):
            keep_alive.append(_schedule_close(fig, gui_cfg.get("final_hold_seconds", _DEFAULT_HOLD_SECONDS)))

    timer.add_callback(lambda: _render_tick(q, sentinel, render, on_finish))
    timer.start()
    plt.show(block=True)  # main-thread event loop; keeps the window responsive
