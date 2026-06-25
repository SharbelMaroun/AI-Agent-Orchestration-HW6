# Convenience wrapper so you can run the app without typing the full uv command.
# Usage:
#   .\run.ps1            # heuristic match (JSON summary)
#   .\run.ps1 --nl       # natural-language match
#   .\run.ps1 --gui      # render an animated GIF to assets/match.gif
# Forwards all arguments to the app, run through uv (project venv).
uv run cop-thief @args
