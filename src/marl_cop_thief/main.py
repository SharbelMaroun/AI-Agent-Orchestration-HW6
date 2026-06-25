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
    args = parser.parse_args()
    sdk = Sdk()
    summary = sdk.run_nl_match() if args.nl else sdk.run_match()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
