"""Shared pytest fixtures."""

from __future__ import annotations

import pytest

from marl_cop_thief.shared import config


@pytest.fixture
def real_config() -> dict:
    """The project's actual config/config.json (validated)."""
    return config.load_config()
