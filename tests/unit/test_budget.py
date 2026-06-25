"""Tests for budget management (forecast + real-time spend + overrun alert)."""

from marl_cop_thief.shared.budget import BudgetConfig, BudgetTracker


def test_config_from_mapping_and_defaults():
    cfg = BudgetConfig.from_mapping({"monthly_cap_usd": 5.0, "usd_per_call": 0.01})
    assert cfg.monthly_cap_usd == 5.0 and cfg.usd_per_call == 0.01 and cfg.alert_threshold == 0.8
    empty = BudgetConfig.from_mapping({})
    assert empty.monthly_cap_usd == 0.0 and empty.alert_threshold == 0.8


def test_config_from_config_reads_llm_budget():
    cfg = BudgetConfig.from_config({"llm": {"budget": {"monthly_cap_usd": 2.0, "usd_per_call": 0.5}}})
    assert cfg.monthly_cap_usd == 2.0 and cfg.usd_per_call == 0.5
    assert BudgetConfig.from_config({}).usd_per_call == 0.0  # missing block -> defaults


def test_spend_and_remaining_track_calls():
    t = BudgetTracker(BudgetConfig(monthly_cap_usd=1.0, alert_threshold=0.8, usd_per_call=0.1))
    t.record(3)
    assert t.spent_usd == 0.3 and t.remaining_usd == 0.7
    t.record(2)
    assert t.calls == 5 and t.spent_usd == 0.5


def test_remaining_clamped_at_zero_when_over():
    t = BudgetTracker(BudgetConfig(monthly_cap_usd=1.0, alert_threshold=0.8, usd_per_call=0.1))
    t.record(20)  # $2.0 spent on a $1.0 cap
    assert t.remaining_usd == 0.0 and t.over_budget is True


def test_alert_threshold_boundary():
    t = BudgetTracker(BudgetConfig(monthly_cap_usd=1.0, alert_threshold=0.8, usd_per_call=0.1))
    t.record(7)  # $0.70 < 0.80 threshold
    assert t.alert is False and t.over_budget is False
    t.record(1)  # $0.80 == threshold
    assert t.alert is True and t.over_budget is False


def test_disabled_when_cap_is_zero():
    t = BudgetTracker(BudgetConfig(monthly_cap_usd=0.0, alert_threshold=0.8, usd_per_call=0.1))
    t.record(100)
    assert t.alert is False and t.over_budget is False  # cap 0 = monitoring disabled


def test_forecast_and_status():
    t = BudgetTracker(BudgetConfig(monthly_cap_usd=5.0, alert_threshold=0.8, usd_per_call=0.02))
    assert t.forecast_usd(100) == 2.0  # 100 calls projected
    t.record(50)
    s = t.status()
    assert (s.calls, s.spent_usd, s.cap_usd, s.remaining_usd, s.alert, s.over_budget) == (
        50, 1.0, 5.0, 4.0, False, False,
    )
