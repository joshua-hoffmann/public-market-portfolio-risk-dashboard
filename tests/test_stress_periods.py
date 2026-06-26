from __future__ import annotations

import math

import pandas as pd
import pytest

from portfolio_risk_dashboard.stress_periods import (
    StressPeriod,
    calculate_stress_period_metrics,
    common_overlapping_window,
    cumulative_return,
    max_drawdown,
    negative_return_day_share,
    realized_volatility,
    recovery_status,
    slice_period,
    validate_period_coverage,
    worst_daily_return,
)


def sample_prices() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "AAA": [100.0, 90.0, 95.0, 110.0, 105.0],
            "BBB": [100.0, 80.0, 70.0, 75.0, 85.0],
        },
        index=pd.to_datetime(
            ["2020-02-19", "2020-02-20", "2020-02-21", "2020-02-24", "2020-03-23"]
        ),
    )


def test_slice_period_uses_inclusive_boundaries() -> None:
    prices = sample_prices()
    period = StressPeriod("test", "2020-02-20", "2020-02-24")

    result = slice_period(prices, period)

    assert list(result.index.strftime("%Y-%m-%d")) == ["2020-02-20", "2020-02-21", "2020-02-24"]


def test_validate_period_coverage_includes_complete_series() -> None:
    prices = sample_prices()
    period = StressPeriod("test", "2020-02-19", "2020-03-23")

    result = validate_period_coverage(prices, period)

    assert {item.ticker: item.status for item in result} == {"AAA": "INCLUDE", "BBB": "INCLUDE"}
    assert all(item.coverage_rate == 1.0 for item in result)


def test_validate_period_coverage_excludes_missing_series() -> None:
    prices = sample_prices()
    prices.loc[pd.Timestamp("2020-02-20"), "BBB"] = None
    prices.loc[pd.Timestamp("2020-02-21"), "BBB"] = None
    period = StressPeriod("test", "2020-02-19", "2020-03-23")

    result = validate_period_coverage(prices, period)
    status_by_ticker = {item.ticker: item.status for item in result}

    assert status_by_ticker["AAA"] == "INCLUDE"
    assert status_by_ticker["BBB"] == "EXCLUDE"


def test_common_overlapping_window_uses_latest_start_and_earliest_end() -> None:
    prices = sample_prices()
    prices.loc[pd.Timestamp("2020-02-19"), "BBB"] = None
    prices.loc[pd.Timestamp("2020-03-23"), "AAA"] = None

    start, end = common_overlapping_window(prices)

    assert start == pd.Timestamp("2020-02-20")
    assert end == pd.Timestamp("2020-02-24")


def test_approved_metric_functions_return_expected_values() -> None:
    prices = sample_prices()

    returns = cumulative_return(prices)
    drawdowns = max_drawdown(prices)
    volatility = realized_volatility(prices)
    worst = worst_daily_return(prices)
    negative_share = negative_return_day_share(prices)
    recovery = recovery_status(prices)

    assert math.isclose(returns["AAA"], 0.05)
    assert math.isclose(returns["BBB"], -0.15)
    assert math.isclose(drawdowns["AAA"], -0.10)
    assert math.isclose(drawdowns["BBB"], -0.30)
    assert worst["BBB"] < worst["AAA"]
    assert 0 <= volatility["AAA"]
    assert math.isclose(negative_share["AAA"], 0.5)
    assert recovery["AAA"] == "RECOVERED_WITHIN_PERIOD"
    assert recovery["BBB"] == "NOT_RECOVERED_WITHIN_PERIOD"


def test_calculate_stress_period_metrics_combines_metrics_and_coverage() -> None:
    prices = sample_prices()
    period = (StressPeriod("test", "2020-02-19", "2020-03-23"),)

    result = calculate_stress_period_metrics(prices, period)

    assert set(result["ticker"]) == {"AAA", "BBB"}
    assert set(result["period"]) == {"test"}
    assert set(result["coverage_status"]) == {"INCLUDE"}
    assert "cumulative_return" in result.columns
    assert "max_drawdown" in result.columns
    assert "realized_volatility_daily" in result.columns
    assert "worst_daily_return" in result.columns
    assert "negative_return_day_share" in result.columns
    assert "recovery_status" in result.columns


def test_calculate_stress_period_metrics_fails_on_excluded_coverage() -> None:
    prices = sample_prices()
    prices["CCC"] = [None, None, None, None, 100.0]
    period = (StressPeriod("test", "2020-02-19", "2020-03-23"),)

    with pytest.raises(ValueError, match="Insufficient coverage"):
        calculate_stress_period_metrics(prices, period)


def test_empty_prices_are_rejected() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        cumulative_return(pd.DataFrame())

