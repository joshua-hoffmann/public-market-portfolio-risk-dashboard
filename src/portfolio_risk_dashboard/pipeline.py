"""Narrow MVP pipeline for descriptive historical risk analysis."""

from __future__ import annotations

from pathlib import Path

from portfolio_risk_dashboard.charts import (
    save_correlation_heatmap,
    save_drawdown_chart,
    save_rolling_volatility_chart,
)
from portfolio_risk_dashboard.config import CANDIDATE_TICKERS, DEFAULT_CONFIG
from portfolio_risk_dashboard.data_loader import (
    download_adjusted_prices,
    preflight_results_to_frame,
    run_price_preflight,
)
from portfolio_risk_dashboard.metrics import (
    calculate_correlation_matrix,
    calculate_daily_returns,
    calculate_drawdowns,
    calculate_risk_metric_table,
    calculate_rolling_volatility,
)


def run_pipeline() -> None:
    """Run data preflight and descriptive historical metric generation."""
    config = DEFAULT_CONFIG
    tickers = list(CANDIDATE_TICKERS.keys())

    output_tables = Path("outputs/tables")
    output_figures = Path("outputs/figures")
    output_tables.mkdir(parents=True, exist_ok=True)
    output_figures.mkdir(parents=True, exist_ok=True)

    prices = download_adjusted_prices(
        tickers=tickers,
        start_date=config.start_date,
        end_date=config.end_date,
    )

    preflight = run_price_preflight(
        prices=prices,
        min_observations=config.min_observations,
    )
    preflight_frame = preflight_results_to_frame(preflight)
    preflight_frame.to_csv(output_tables / "data_preflight.csv", index=False)

    passed_tickers = preflight_frame.loc[preflight_frame["status"] == "PASS", "ticker"].tolist()
    if len(passed_tickers) < 2:
        raise ValueError("Fewer than two tickers passed preflight. Correlation analysis is not meaningful.")

    analysis_prices = prices[passed_tickers].dropna(how="all")
    returns = calculate_daily_returns(analysis_prices)
    drawdowns = calculate_drawdowns(analysis_prices)
    metrics = calculate_risk_metric_table(
        analysis_prices,
        annualization_days=config.annualization_days,
    )
    correlation = calculate_correlation_matrix(returns)
    rolling_volatility = calculate_rolling_volatility(
        returns,
        rolling_window_days=config.rolling_window_days,
        annualization_days=config.annualization_days,
    )

    metrics.to_csv(output_tables / "risk_metric_table.csv", index=False)
    correlation.to_csv(output_tables / "correlation_matrix.csv")

    save_drawdown_chart(drawdowns, output_figures / "drawdown_chart.png")
    save_rolling_volatility_chart(rolling_volatility, output_figures / "rolling_volatility_chart.png")
    save_correlation_heatmap(correlation, output_figures / "correlation_heatmap.png")


if __name__ == "__main__":
    run_pipeline()
