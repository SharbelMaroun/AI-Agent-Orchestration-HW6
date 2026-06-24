"""Tests for the config loader and version validation."""

import json

import pytest

from marl_cop_thief.shared import config
from marl_cop_thief.shared.config import ConfigError


def test_load_real_config(real_config):
    assert real_config["version"] == "1.00"
    assert real_config["grid_size"] == [5, 5]
    assert real_config["max_moves"] == 25
    assert real_config["num_games"] == 6
    assert real_config["max_barriers"] == 5
    assert real_config["scoring"]["cop_win"] == 20


def test_load_rate_limits():
    rl = config.load_json("rate_limits.json")
    assert rl["rate_limits"]["version"] == "1.00"
    assert rl["rate_limits"]["services"]["default"]["requests_per_minute"] == 30


def test_config_dir_default_exists():
    assert config.config_dir().is_dir()


def test_config_dir_env_override(monkeypatch, tmp_path):
    monkeypatch.setenv("MARL_CONFIG_DIR", str(tmp_path))
    assert config.config_dir() == tmp_path


def test_missing_file_raises(tmp_path):
    with pytest.raises(ConfigError, match="not found"):
        config.load_json("nope.json", tmp_path)


def test_invalid_json_raises(tmp_path):
    (tmp_path / "bad.json").write_text("{ not json", encoding="utf-8")
    with pytest.raises(ConfigError, match="Invalid JSON"):
        config.load_json("bad.json", tmp_path)


def test_missing_version_raises(tmp_path):
    (tmp_path / "c.json").write_text(json.dumps({"grid_size": [2, 2]}), encoding="utf-8")
    with pytest.raises(ConfigError, match="Missing 'version'"):
        config.load_config("c.json", tmp_path)


def test_version_mismatch_raises(tmp_path):
    (tmp_path / "c.json").write_text(json.dumps({"version": "9.99"}), encoding="utf-8")
    with pytest.raises(ConfigError, match="!= expected"):
        config.load_config("c.json", tmp_path)


def test_load_config_validates_and_returns(tmp_path):
    (tmp_path / "c.json").write_text(json.dumps({"version": "1.00", "x": 1}), encoding="utf-8")
    cfg = config.load_config("c.json", tmp_path)
    assert cfg["x"] == 1
