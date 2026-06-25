"""Thin CLI entrypoint. Delegates to the SDK and prints the match summary."""

from __future__ import annotations

import json

from .sdk import Sdk


def main() -> None:
    summary = Sdk().run_match()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
