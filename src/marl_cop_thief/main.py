"""Thin CLI entrypoint. Delegates to the SDK and prints the match summary.

Default is the natural-language match (the assignment's core). It uses OpenAI
when OPENAI_API_KEY is set in .env, otherwise a deterministic offline backend.
"""

from __future__ import annotations

import argparse
import json

from dotenv import load_dotenv

from .sdk import Sdk
from .shared.llm_backend import select_backend


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a Cop & Thief match.")
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Run the simple heuristic match (no natural language, no LLM).",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Render a sub-game to an animated GIF (assets/match.gif) instead of printing.",
    )
    args = parser.parse_args()
    load_dotenv()  # pick up OPENAI_API_KEY (and other vars) from .env
    sdk = Sdk()
    if args.gui:
        from .gui.match_animator import animate_match

        print(f"GUI animation saved to {animate_match(sdk.config)}")
        return
    summary = sdk.run_match() if args.simple else sdk.run_nl_match(select_backend(sdk.config))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
