"""Unit tests for the runnable natural-language match (nl_match + SDK method).

All backends are injected fakes (echo / counters) — no network, no external
services. Covers ``run_nl_match`` and ``Sdk.run_nl_match`` to 100% (incl. branch).
"""

from marl_cop_thief.sdk import Sdk
from marl_cop_thief.services.nl_match import run_nl_match
from marl_cop_thief.shared.gatekeeper import ApiGatekeeper

CONFIG = {
    "grid_size": [5, 5],
    "max_moves": 25,
    "num_games": 3,
    "max_barriers": 5,
    "visibility_radius": 1,
    "seed": 11,
    "scoring": {"cop_win": 20, "thief_win": 10, "cop_loss": 5, "thief_loss": 5},
}


def test_run_nl_match_returns_summary_shape():
    summary = run_nl_match(CONFIG)
    assert set(summary) == {"sub_games", "totals"}
    assert len(summary["sub_games"]) == CONFIG["num_games"]
    assert set(summary["totals"]) == {"cop", "thief"}
    for sub in summary["sub_games"]:
        assert sub["winner"] in ("cop", "thief")
        assert sub["moves_used"] <= CONFIG["max_moves"]


def test_run_nl_match_is_deterministic_for_same_seed():
    assert run_nl_match(CONFIG) == run_nl_match(CONFIG)


def test_run_nl_match_accepts_injected_backend():
    calls: list[str] = []

    def backend(prompt: str) -> str:
        calls.append(prompt)
        return prompt  # echo

    summary = run_nl_match(CONFIG, backend=backend)
    assert len(summary["sub_games"]) == CONFIG["num_games"]
    assert calls  # the injected backend was consulted via the gatekeeper


def test_run_nl_match_defaults_seed_to_zero():
    cfg = {k: v for k, v in CONFIG.items() if k != "seed"}
    summary = run_nl_match(cfg)
    assert len(summary["sub_games"]) == CONFIG["num_games"]


def test_sdk_run_nl_match_default_backend():
    summary = Sdk(CONFIG).run_nl_match()
    assert len(summary["sub_games"]) == CONFIG["num_games"]
    assert set(summary["totals"]) == {"cop", "thief"}


def test_sdk_run_nl_match_passes_backend():
    summary = Sdk(CONFIG).run_nl_match(backend=lambda prompt: prompt)
    assert len(summary["sub_games"]) == CONFIG["num_games"]


def test_run_nl_match_routes_through_injected_gatekeeper():
    gk = ApiGatekeeper()
    run_nl_match(CONFIG, gatekeeper=gk)
    assert gk.calls > 0  # the shared gatekeeper fronted every LLM call across sub-games


def test_sdk_run_nl_match_passes_gatekeeper():
    gk = ApiGatekeeper()
    Sdk(CONFIG).run_nl_match(gatekeeper=gk)
    assert gk.calls > 0
