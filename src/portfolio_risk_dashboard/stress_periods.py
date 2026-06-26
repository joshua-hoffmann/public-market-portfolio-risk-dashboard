"""Stress-period analysis utilities.

This module supports descriptive, date-bounded historical analysis only.
It does not produce investment advice, forecasts, rankings, optimization,
or claims about future stress-period behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd

CoverageStatus = Literal["INCLUDE", "INCLUDE_WITH_LIMITATION", "EXCLUDE"]
RecoveryStatus = Literal["RECOVERED_WITHIN_PERIOD", "NOT_RECOVERED_WITHIN_PERIOD", "NO_DRAWDOWN", "INSUFFICIENT_DATA"]


@dataclass(frozen=True)
class StressPeriod:
    """Fixed historical analysis window."""

    name: str
    start: str
    end: str

    @property
    def start_timestamp(self) -> pd.Timestamp:
        return pd.Timestamp(self.start)

    @property
    def end_timestamp(self) -> pd.Timestamp:
        return pd.Timestamp(self.end)


@dataclass(frozen=True)
class PeriodCoverage:
    """Coverage status for one ticker in one stress period."""

    period: str
    ticker: str
    expected_observations: int
    valid_observations: int
    missing_observations: int
    coverage_rate: float
    has_left_boundary_history: bool
    has_right_boundary_history: bool
    status: CoverageStatus


DEFAULT_STRESS_PERIODS: tuple[StressPeriod, ...] = (
    StressPeriod("2020 shock", "2020-02-19", "2020-03-23"),
    StressPeriod("2022 rate/inflation shock", "2022-01-03", "2022-10-14"),
)


def _validate_prices(prices: pd.DataFrame) -> pd.DataFrame:
    """Return a sorted copy of a non-empty price frame with DatetimeIndex."""

    if not isinstance(prices, pd.DataFrame):
        raise TypeError("prices must be a pandas DataFrame.")
    if prices.empty:
        raise ValueError("prices must not be empty.")

    result = prices.copy()
    result.index = pd.to_datetime(result.index)
    return result.sort_index()


def slice_period(prices: pd.DataFrame, period: StressPeriod) -> pd.DataFrame:
    """Slice adjusted-close prices to an inclusive stress-period window."""

    clean_prices = _validate_prices(prices)
    return clean_prices.loc[
        (clean_prices.index >= period.start_timestamp)
        & (clean_prices.index <= period.end_timestamp)
    ].copy()


def validate_period_coverage(
    prices: pd.DataFrame,
    period: StressPeriod,
    *,
    include_threshold: float = 0.95,
    limitation_threshold: float = 0.90,
) -> list[PeriodCoverage]:
    """Validate ticker coverage for one stress period.

    Coverage uses observations present in the returned adjusted-close frame.
    It does not fill missing values or silently backfill unavailable history.
    """

    if not 0 <= limitation_threshold <= include_threshold <= 1:
        raise ValueError("coverage thresholds must satisfy 0 <= limitation <= include <= 1.")

    clean_prices = _validate_prices(prices)
    period_frame = slice_period(clean_prices, period)
    expected_observations = len(period_frame)

    results: list[PeriodCoverage] = []

    for ticker in clean_prices.columns:
        full_series = clean_prices[ticker].dropna()
        period_series = period_frame[ticker] if ticker in period_frame.columns else pd.Series(dtype=float)

        valid_observations = int(period_series.notna().sum())
        missing_observations = int(period_series.isna().sum()) if expected_observations else 0
        coverage_rate = valid_observations / expected_observations if expected_observations else 0.0

        has_left_boundary_history = bool(not full_series.loc[full_series.index <= period.start_timestamp].empty)
        has_right_boundary_history = bool(not full_series.loc[full_series.index >= period.end_timestamp].empty)

        if valid_observations < 2 or not has_left_boundary_history or not has_right_boundary_history:
            status: CoverageStatus = "EXCLUDE"
        elif coverage_rate >= include_threshold:
            status = "INCLUDE"
        elif coverage_rate >= limitation_threshold:
            status = "INCLUDE_WITH_LIMITATION"
        else:
            status = "EXCLUDE"

        results.append(
            PeriodCoverage(
                period=period.name,
                ticker=str(ticker),
                expected_observations=expected_observations,
                valid_observations=valid_observations,
                missing_observations=missing_observations,
                coverage_rate=coverage_rate,
                has_left_boundary_history=has_left_boundary_history,
                has_right_boundary_history=has_right_boundary_history,
                status=status,
            )
        )

    return results


def validate_all_periods(
    prices: pd.DataFrame,
    periods: tuple[StressPeriod, ...] = DEFAULT_STRESS_PERIODS,
) -> pd.DataFrame:
    """Return coverage validation for all configured stress periods."""

    rows = []
    for period in periods:
        for result in validate_period_coverage(prices, period):
            rows.append(result.__dict__)
    return pd.DataFrame(rows)


def common_overlapping_window(prices: pd.DataFrame) -> tuple[pd.Timestamp, pd.Timestamp]:
    """Return common first and last dates across all non-empty ticker series."""

    clean_prices = _validate_prices(prices)

    first_dates = []
    last_dates = []

    for ticker in clean_prices.columns:
        series = clean_prices[ticker].dropna()
        if series.empty:
            raise ValueError(f"Ticker {ticker} has no usable observations.")
        first_dates.append(series.index.min())
        last_dates.append(series.index.max())

    common_start = max(first_dates)
    common_end = min(last_dates)

    if common_start > common_end:
        raise ValueError("No common overlapping window exists across tickers.")

    return common_start, common_end


def cumulative_return(period_prices: pd.DataFrame) -> pd.Series:
    """Calculate start-to-end cumulative return for each ticker."""

    clean_prices = _validate_prices(period_prices).dropna(how="all")
    if len(clean_prices) < 2:
        raise ValueError("At least two price rows are required for cumulative return.")

    start_prices = clean_prices.ffill().iloc[0]
    end_prices = clean_prices.ffill().iloc[-1]
    return (end_prices / start_prices) - 1.0


def max_drawdown(period_prices: pd.DataFrame) -> pd.Series:
    """Calculate maximum drawdown within a period for each ticker."""

    clean_prices = _validate_prices(period_prices).ffill()
    if len(clean_prices) < 2:
        raise ValueError("At least two price rows are required for drawdown.")

    cumulative = clean_prices / clean_prices.iloc[0]
    running_max = cumulative.cummax()
    drawdowns = (cumulative / running_max) - 1.0
    return drawdowns.min()


def realized_volatility(period_prices: pd.DataFrame, *, annualize: bool = False, trading_days: int = 252) -> pd.Series:
    """Calculate realized volatility from daily returns.

    By default, volatility is not annualized to avoid overstating precision
    for short stress windows.
    """

    clean_prices = _validate_prices(period_prices).ffill()
    returns = clean_prices.pct_change(fill_method=None).dropna(how="all")
    if returns.empty:
        raise ValueError("At least one return row is required for volatility.")

    vol = returns.std()
    if annualize:
        vol = vol * (trading_days ** 0.5)
    return vol


def worst_daily_return(period_prices: pd.DataFrame) -> pd.Series:
    """Calculate worst daily return in the period for each ticker."""

    clean_prices = _validate_prices(period_prices).ffill()
    returns = clean_prices.pct_change(fill_method=None).dropna(how="all")
    if returns.empty:
        raise ValueError("At least one return row is required for worst daily return.")
    return returns.min()


def negative_return_day_share(period_prices: pd.DataFrame) -> pd.Series:
    """Calculate share of observed return days with negative returns."""

    clean_prices = _validate_prices(period_prices).ffill()
    returns = clean_prices.pct_change(fill_method=None).dropna(how="all")
    if returns.empty:
        raise ValueError("At least one return row is required for negative-return-day share.")
    return returns.lt(0).sum() / returns.notna().sum()


def recovery_status(period_prices: pd.DataFrame) -> pd.Series:
    """Return whether each ticker recovered its prior peak within the same period."""

    clean_prices = _validate_prices(period_prices).ffill()
    if len(clean_prices) < 2:
        return pd.Series("INSUFFICIENT_DATA", index=clean_prices.columns)

    statuses: dict[str, RecoveryStatus] = {}

    for ticker in clean_prices.columns:
        series = clean_prices[ticker].dropna()
        if len(series) < 2:
            statuses[str(ticker)] = "INSUFFICIENT_DATA"
            continue

        cumulative = series / series.iloc[0]
        running_max = cumulative.cummax()
        drawdown = (cumulative / running_max) - 1.0

        trough_date = drawdown.idxmin()
        trough_value = drawdown.loc[trough_date]

        if trough_value >= 0:
            statuses[str(ticker)] = "NO_DRAWDOWN"
            continue

        prior_peak = running_max.loc[trough_date]
        after_trough = cumulative.loc[cumulative.index >= trough_date]
        recovered = bool((after_trough >= prior_peak).any())
        statuses[str(ticker)] = "RECOVERED_WITHIN_PERIOD" if recovered else "NOT_RECOVERED_WITHIN_PERIOD"

    return pd.Series(statuses)


def calculate_stress_period_metrics(
    prices: pd.DataFrame,
    periods: tuple[StressPeriod, ...] = DEFAULT_STRESS_PERIODS,
) -> pd.DataFrame:
    """Calculate approved descriptive metrics for each ticker-period pair."""

    clean_prices = _validate_prices(prices)
    rows: list[dict[str, object]] = []

    for period in periods:
        period_prices = slice_period(clean_prices, period)
        coverage_by_ticker = {item.ticker: item for item in validate_period_coverage(clean_prices, period)}

        returns = cumulative_return(period_prices)
        drawdowns = max_drawdown(period_prices)
        volatility = realized_volatility(period_prices, annualize=False)
        worst_returns = worst_daily_return(period_prices)
        negative_share = negative_return_day_share(period_prices)
        recovery = recovery_status(period_prices)

        for ticker in clean_prices.columns:
            coverage = coverage_by_ticker[str(ticker)]
            if coverage.status == "EXCLUDE":
                raise ValueError(f"Insufficient coverage for {ticker} in {period.name}.")

            rows.append(
                {
                    "period": period.name,
                    "ticker": str(ticker),
                    "period_start": period.start,
                    "period_end": period.end,
                    "cumulative_return": float(returns[ticker]),
                    "max_drawdown": float(drawdowns[ticker]),
                    "realized_volatility_daily": float(volatility[ticker]),
                    "worst_daily_return": float(worst_returns[ticker]),
                    "negative_return_day_share": float(negative_share[ticker]),
                    "recovery_status": str(recovery[str(ticker)]),
                    "coverage_status": coverage.status,
                    "coverage_rate": coverage.coverage_rate,
                    "valid_observations": coverage.valid_observations,
                    "expected_observations": coverage.expected_observations,
                }
            )

    return pd.DataFrame(rows)


__all__ = [
    "DEFAULT_STRESS_PERIODS",
    "PeriodCoverage",
    "StressPeriod",
    "calculate_stress_period_metrics",
    "common_overlapping_window",
    "cumulative_return",
    "max_drawdown",
    "negative_return_day_share",
    "realized_volatility",
    "recovery_status",
    "slice_period",
    "validate_all_periods",
    "validate_period_coverage",
    "worst_daily_return",
]
