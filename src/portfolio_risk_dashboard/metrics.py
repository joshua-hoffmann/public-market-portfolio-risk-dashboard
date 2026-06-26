"""Descriptive historical risk metrics.

All metrics are historical and descriptive only.
They are not forecasts, recommendations, or validated risk-model outputs.
"""

from __future__ import annotations

import numpy as np
import pandas as pd


def _format_index_value(value: object) -> str:
    """Return a stable string for date-like or non-date index values."""
    if hasattr(value, "date"):
        return str(value.date())
    return str(value)


def calculate_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate simple daily returns from adjusted prices."""
    if prices.empty:
        raise ValueError("Price DataFrame is empty.")
    return prices.pct_change(fill_method=None).dropna(how="all")


def calculate_drawdowns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate historical drawdown series from adjusted prices."""
    if prices.empty:
        raise ValueError("Price DataFrame is empty.")
    wealth_index = prices / prices.iloc[0]
    running_max = wealth_index.cummax()
    return wealth_index / running_max - 1.0


def calculate_risk_metric_table(
    prices: pd.DataFrame,
    annualization_days: int = 252,
) -> pd.DataFrame:
    """Calculate descriptive historical risk metrics."""
    if prices.empty:
        raise ValueError("Price DataFrame is empty.")

    returns = calculate_daily_returns(prices)
    drawdowns = calculate_drawdowns(prices)

    rows = []
    for ticker in prices.columns:
        ticker_returns = returns[ticker].dropna()
        ticker_prices = prices[ticker].dropna()
        ticker_drawdowns = drawdowns[ticker].dropna()

        if ticker_returns.empty or ticker_prices.empty:
            continue

        cumulative_return = ticker_prices.iloc[-1] / ticker_prices.iloc[0] - 1.0
        annualized_volatility = ticker_returns.std(ddof=1) * np.sqrt(annualization_days)

        rows.append(
            {
                "ticker": ticker,
                "observations": int(ticker_prices.shape[0]),
                "first_date": _format_index_value(ticker_prices.index.min()),
                "last_date": _format_index_value(ticker_prices.index.max()),
                "cumulative_return_historical": float(cumulative_return),
                "annualized_volatility_historical": float(annualized_volatility),
                "maximum_drawdown_historical": float(ticker_drawdowns.min()),
                "best_daily_return_historical": float(ticker_returns.max()),
                "worst_daily_return_historical": float(ticker_returns.min()),
                "mean_daily_return_historical": float(ticker_returns.mean()),
                "median_daily_return_historical": float(ticker_returns.median()),
            }
        )

    return pd.DataFrame(rows)


def calculate_correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """Calculate historical return correlation matrix."""
    if returns.empty:
        raise ValueError("Return DataFrame is empty.")
    return returns.corr()


def calculate_rolling_volatility(
    returns: pd.DataFrame,
    rolling_window_days: int = 63,
    annualization_days: int = 252,
) -> pd.DataFrame:
    """Calculate rolling annualized historical volatility."""
    if returns.empty:
        raise ValueError("Return DataFrame is empty.")
    return returns.rolling(rolling_window_days).std() * np.sqrt(annualization_days)
