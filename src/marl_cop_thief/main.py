"""Thin CLI entrypoint. Delegates to the SDK and prints the match summary."""

from __future__ import annotations

import argparse
import json

from .sdk import Sdk


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a cop & thief match.")
    parser.add_argument(
        "--nl",
        action="store_true",
        help="Run the natural-language (NL) match instead of the heuristic match.",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Render a sub-game to an animated GIF (assets/match.gif) instead of printing.",
    )
    args = parser.parse_args()
    sdk = Sdk()
    if args.gui:
        from .gui.match_animator import animate_match

        print(f"GUI animation saved to {animate_match(sdk.config)}")
        return
    summary = sdk.run_nl_match() if args.nl else sdk.run_match()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
