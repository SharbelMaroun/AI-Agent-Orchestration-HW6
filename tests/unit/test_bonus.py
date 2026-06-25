"""Tests for inter-group bonus scoring (§12.2: 10/5/5 + averaging + void)."""

import pytest

from marl_cop_thief.services.bonus import SeriesResult, final_bonus, series_awards


def test_winner_gets_10_loser_5():
    awards = series_awards(SeriesResult({"A": 60, "B": 80}))
    assert awards == {"A": 5.0, "B": 10.0}  # B higher -> wins


def test_winner_can_be_first_group():
    assert series_awards(SeriesResult({"A": 90, "B": 40})) == {"A": 10.0, "B": 5.0}


def test_complete_tie_is_5_each():
    assert series_awards(SeriesResult({"A": 60, "B": 60})) == {"A": 5.0, "B": 5.0}


def test_disagreement_voids_the_series():
    awards = series_awards(SeriesResult({"A": 60, "B": 80}, mutual_agreement=False))
    assert awards == {"A": 0.0, "B": 0.0}  # no correlation -> 0 for both


def test_series_must_have_two_groups():
    with pytest.raises(ValueError, match="exactly two groups"):
        series_awards(SeriesResult({"A": 60}))


def test_final_bonus_averages_valid_series():
    series = [SeriesResult({"A": 90, "B": 40}), SeriesResult({"A": 40, "B": 90})]
    assert final_bonus("A", series) == 7.5  # (10 + 5) / 2


def test_final_bonus_no_series_is_zero():
    assert final_bonus("A", []) == 0.0


def test_award_values_are_parameterizable():
    # the spec's 8.5 worked example (win 10, "lose" 7) is reproducible via overrides
    series = [SeriesResult({"A": 90, "B": 40}), SeriesResult({"A": 40, "B": 90})]
    assert final_bonus("A", series, win=10.0, lose=7.0) == 8.5


def test_points_from_config_reads_bonus_block():
    from marl_cop_thief.services.bonus import points_from_config

    assert points_from_config({"bonus": {"win": 12, "lose": 6}}) == {"win": 12.0, "lose": 6.0}
    assert points_from_config({}) == {}  # no bonus block -> spec defaults apply
