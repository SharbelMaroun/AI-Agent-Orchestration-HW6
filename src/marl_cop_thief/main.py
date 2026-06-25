"""Thin CLI entrypoint. Delegates to the SDK and prints the match summary.

Default is the natural-language match (the assignment's core). It uses OpenAI
when OPENAI_API_KEY is set in .env, otherwise a deterministic offline backend.
The active LLM backend and the gatekeeper call count are printed so a real run
is unmistakably distinct from the offline fallback.
"""

from __future__ import annotations

import argparse
import json
import os

from dotenv import load_dotenv

from .sdk import Sdk
from .shared.llm_backend import select_backend, select_gatekeeper


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run a Cop & Thief match.")
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Run the simple heuristic match (no natural language, no LLM).",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Animate a sub-game to a GIF: the NL match (default) or the heuristic match (--simple).",
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Open a live interactive window that draws each turn in real time (config gui.live_backend).",
    )
    return parser.parse_args()


def _run_simple(sdk: Sdk, gui: bool, live: bool) -> None:
    if live:
        from .gui.live_viewer import play_live

        play_live(sdk.stream_simple_frames(), sdk.config, "Cop & Thief — heuristic")
    elif gui:
        from .gui.match_animator import animate_match

        print(f"GUI animation saved to {animate_match(sdk.config)}")
    else:
        summary = sdk.run_match()
        print(json.dumps(summary, indent=2))
        _maybe_send_report(sdk, summary)


def _maybe_send_report(sdk: Sdk, summary: dict) -> None:
    """Email the JSON match report via real Gmail (gatekeeper-routed) when enabled."""
    if not sdk.config.get("reporting", {}).get("send_real_email", False):
        return
    from .shared.gmail_client import send_email
    from .shared.google_api import gmail_gatekeeper
    from .shared.google_auth import build_services

    sd = os.environ.get("MARL_GOOGLE_SECRETS_DIR") or sdk.config.get("google", {}).get("secrets_dir", "")
    gmail, _ = build_services(sd, sdk.config["google"]["scopes"])
    gk = gmail_gatekeeper()  # route the Gmail send through the central gatekeeper (§2)
    mid = sdk.send_match_report(summary, lambda to, subj, body: send_email(gmail, to, subj, body, gk))
    print(f"Report email sent: id={mid}")


def _run_nl(sdk: Sdk, gui: bool, live: bool) -> None:
    backend = select_backend(sdk.config)
    gatekeeper = select_gatekeeper(sdk.config)
    model = sdk.config.get("llm", {}).get("model", "gpt-4o-mini")
    real = bool(os.environ.get("OPENAI_API_KEY"))
    # Creative LLM speech only helps the visual modes (the message is shown) and needs a real key.
    creative = real and bool(sdk.config.get("llm", {}).get("creative_speech", True))
    print(f"LLM backend: {'OpenAI (' + model + ')' if real else 'offline echo (no OPENAI_API_KEY)'}")
    if live:
        from .gui.live_viewer import play_live

        frames = sdk.stream_nl_frames(backend, gatekeeper, creative=creative)
        play_live(frames, sdk.config, "Cop & Thief — natural language")
    elif gui:
        from .gui.match_animator import animate_nl_match

        path = animate_nl_match(sdk.config, backend, gatekeeper, creative=creative)
        print(f"GUI animation saved to {path}")
    else:
        summary = sdk.run_nl_match(backend, gatekeeper)
        print(json.dumps(summary, indent=2))
        print(f"LLM calls via gatekeeper: {gatekeeper.calls}")
        if real:
            _report_budget(sdk.config, gatekeeper.calls)
        _maybe_send_report(sdk, summary)
        return
    print(f"LLM calls via gatekeeper: {gatekeeper.calls}")
    if real:
        _report_budget(sdk.config, gatekeeper.calls)


def _report_budget(config: dict, calls: int) -> None:
    """Print real-time spend vs the config-driven budget cap, with an overrun alert."""
    from .shared.budget import BudgetConfig, BudgetTracker

    tracker = BudgetTracker(BudgetConfig.from_config(config))
    tracker.record(calls)
    s = tracker.status()
    flag = " [OVER BUDGET]" if s.over_budget else (" [ALERT]" if s.alert else "")
    print(f"Budget: ${s.spent_usd:.4f} spent / ${s.cap_usd:.2f} cap "
          f"(${s.remaining_usd:.4f} left){flag}")


def main() -> None:
    args = _parse_args()
    load_dotenv()  # pick up OPENAI_API_KEY (and other vars) from .env
    sdk = Sdk()
    if args.simple:
        _run_simple(sdk, args.gui, args.live)
    else:
        _run_nl(sdk, args.gui, args.live)


if __name__ == "__main__":
    main()
