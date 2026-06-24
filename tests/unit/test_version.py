"""Tests for version constants (must start at 1.00)."""

from marl_cop_thief import __version__
from marl_cop_thief.shared import version


def test_versions_start_at_1_00():
    assert version.__code_version__ == "1.00"
    assert version.CONFIG_VERSION == "1.00"
    assert version.RATE_LIMIT_VERSION == "1.00"


def test_package_version_matches_code_version():
    assert __version__ == version.__code_version__
