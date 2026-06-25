"""Configuration loader with runtime version validation (guidelines section 8.1).

All tunables live in JSON under ``config/`` — nothing is hard-coded in the code.
The config directory is resolved relative to the package root, or overridden via
the ``MARL_CONFIG_DIR`` environment variable.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .version import CONFIG_VERSION


class ConfigError(Exception):
    """Raised when a configuration file is missing, malformed, or wrong-versioned."""


def _repo_root() -> Path:
    """Repo root, anchored on this file (src/marl_cop_thief/shared/config.py)."""
    return Path(__file__).resolve().parents[3]


def config_dir() -> Path:
    """Return the active config directory (``MARL_CONFIG_DIR`` overrides the default)."""
    override = os.environ.get("MARL_CONFIG_DIR")
    return Path(override) if override else _repo_root() / "config"


def load_json(name: str, directory: Path | None = None) -> dict[str, Any]:
    """Load and parse a JSON config file, raising :class:`ConfigError` on failure."""
    path = (directory or config_dir()) / name
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Invalid JSON in {path}: {exc}") from exc


def validate_version(
    cfg: dict[str, Any], expected: str = CONFIG_VERSION, *, key: str = "version"
) -> None:
    """Validate that ``cfg[key]`` matches the expected version string."""
    actual = cfg.get(key)
    if actual is None:
        raise ConfigError(f"Missing '{key}' in config")
    if str(actual) != str(expected):
        raise ConfigError(f"Config version {actual!r} != expected {expected!r}")


def load_config(name: str = "config.json", directory: Path | None = None) -> dict[str, Any]:
    """Load a config file and validate its top-level version key."""
    cfg = load_json(name, directory)
    validate_version(cfg)
    return cfg
