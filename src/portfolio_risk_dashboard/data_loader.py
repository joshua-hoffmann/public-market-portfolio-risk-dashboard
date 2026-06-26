"""Data loading and preflight utilities.

Source boundary:
- Uses yfinance / Yahoo Finance via yfinance.
- Intended for descriptive historical analysis only.
- Does not treat downloaded data as institutionally validated market data.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class TickerPreflightResult:
    ticker: str
    status: str
    observations: int
    first_date: str | None
    last_date: str | None
    missing_values: int
    message: str


def download_adjusted_prices(
    tickers: list[str],
    start_date: str,
    end_date: str | None = None,
) -> pd.DataFrame:
    """Download adjusted close prices for candidate tickers.

    Returns a DataFrame indexed by date with one column per ticker.
    """
    if not tickers:
        raise ValueError("At least one ticker is required.")

    data = yf.download(
        tickers=tickers,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        progress=False,
        group_by="column",
    )

    if data.empty:
        raise ValueError("No data returned from yfinance.")

    if isinstance(data.columns, pd.MultiIndex):
        if "Adj Close" not in data.columns.get_level_values(0):
            raise ValueError("Adjusted close data not found in yfinance response.")
        prices = data["Adj Close"].copy()
    else:
        if "Adj Close" not in data.columns:
            raise ValueError("Adjusted close data not found in yfinance response.")
        prices = data[["Adj Close"]].copy()
        prices.columns = tickers

    prices = prices.sort_index()
    prices.index = pd.to_datetime(prices.index)
    return prices


def run_price_preflight(
    prices: pd.DataFrame,
    min_observations: int,
) -> list[TickerPreflightResult]:
    """Check basic data availability and missingness for each ticker."""
    results: list[TickerPreflightResult] = []

    for ticker in prices.columns:
        series = prices[ticker].dropna()
        missing_values = int(prices[ticker].isna().sum())

        if series.empty:
            results.append(
                TickerPreflightResult(
                    ticker=ticker,
                    status="FAIL",
                    observations=0,
                    first_date=None,
                    last_date=None,
                    missing_values=missing_values,
                    message="No usable adjusted close observations.",
                )
            )
            continue

        observations = int(series.shape[0])
        status = "PASS" if observations >= min_observations else "REVIEW"
        message = "Sufficient observations." if status == "PASS" else "Below minimum observation threshold; requires governance review."

        results.append(
            TickerPreflightResult(
                ticker=ticker,
                status=status,
                observations=observations,
                first_date=str(series.index.min().date()),
                last_date=str(series.index.max().date()),
                missing_values=missing_values,
                message=message,
            )
        )

    return results


def preflight_results_to_frame(results: list[TickerPreflightResult]) -> pd.DataFrame:
    """Convert preflight results to a DataFrame."""
    return pd.DataFrame([result.__dict__ for result in results])
