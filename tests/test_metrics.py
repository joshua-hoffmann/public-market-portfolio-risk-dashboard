import pandas as pd

from portfolio_risk_dashboard.metrics import (
    calculate_daily_returns,
    calculate_drawdowns,
    calculate_risk_metric_table,
)


def test_calculate_daily_returns():
    prices = pd.DataFrame({"AAA": [100.0, 110.0, 121.0]})
    returns = calculate_daily_returns(prices)
    assert round(float(returns["AAA"].iloc[0]), 6) == 0.10
    assert round(float(returns["AAA"].iloc[1]), 6) == 0.10


def test_calculate_drawdowns():
    prices = pd.DataFrame({"AAA": [100.0, 120.0, 90.0, 130.0]})
    drawdowns = calculate_drawdowns(prices)
    assert round(float(drawdowns["AAA"].iloc[2]), 6) == -0.25


def test_calculate_risk_metric_table_has_expected_columns():
    prices = pd.DataFrame({"AAA": [100.0, 101.0, 102.0, 103.0, 104.0]})
    table = calculate_risk_metric_table(prices)
    expected_columns = {
        "ticker",
        "observations",
        "cumulative_return_historical",
        "annualized_volatility_historical",
        "maximum_drawdown_historical",
    }
    assert expected_columns.issubset(set(table.columns))
