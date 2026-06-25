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
    return parser.parse_args()


def _run_simple(sdk: Sdk, gui: bool) -> None:
    if gui:
        from .gui.match_animator import animate_match

        print(f"GUI animation saved to {animate_match(sdk.config)}")
    else:
        print(json.dumps(sdk.run_match(), indent=2))


def _run_nl(sdk: Sdk, gui: bool) -> None:
    backend = select_backend(sdk.config)
    gatekeeper = select_gatekeeper(sdk.config)
    model = sdk.config.get("llm", {}).get("model", "gpt-4o-mini")
    real = bool(os.environ.get("OPENAI_API_KEY"))
    print(f"LLM backend: {'OpenAI (' + model + ')' if real else 'offline echo (no OPENAI_API_KEY)'}")
    if gui:
        from .gui.match_animator import animate_nl_match

        print(f"GUI animation saved to {animate_nl_match(sdk.config, backend, gatekeeper)}")
    else:
        print(json.dumps(sdk.run_nl_match(backend, gatekeeper), indent=2))
    print(f"LLM calls via gatekeeper: {gatekeeper.calls}")


def main() -> None:
    args = _parse_args()
    load_dotenv()  # pick up OPENAI_API_KEY (and other vars) from .env
    sdk = Sdk()
    if args.simple:
        _run_simple(sdk, args.gui)
    else:
        _run_nl(sdk, args.gui)


if __name__ == "__main__":
    main()
