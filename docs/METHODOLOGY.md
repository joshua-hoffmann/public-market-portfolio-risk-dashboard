# Methodology

This project provides a reproducible, methodology-first dashboard for descriptively comparing selected public-market ETFs and assets using historical adjusted price data.

## Analytical question

How do selected public-market assets differ historically in volatility, drawdown behavior, return distribution, and correlation structure?

## Why this matters

Market participants, analysts, and data teams often need transparent ways to compare historical risk behavior across assets. A simple price chart is not enough to understand downside periods, volatility regimes, distribution shape, or whether assets moved similarly during the selected historical period.

This project focuses on making those historical risk comparisons reproducible and interpretable without converting them into investment advice or forecasts.

## Data source

The project downloads adjusted historical price data using yfinance, which accesses Yahoo Finance data. This is a practical public-market data source for reproducible analysis, but it is not treated here as institutionally validated or investment-grade data.

Raw downloaded market data is not redistributed in this repository.

## Asset universe

The selected ETFs and public-market assets are a methodological sample used to demonstrate historical risk comparison across different market exposures.

The asset list is not a recommendation list, not a preferred investment universe, and not an allocation proposal.

## Metrics

The project computes daily returns from adjusted close prices and derives descriptive historical metrics, including:

- cumulative return over the selected historical window;
- annualized historical volatility;
- maximum historical drawdown;
- best and worst daily return;
- mean and median daily return;
- rolling historical volatility;
- historical correlation matrix.

## Interpretation

The metrics are descriptive and historical. They help compare what happened within the selected sample period. They do not predict future returns, future risk, future correlations, or future diversification behavior.

Charts and tables are not rankings, recommendations, forecasts, or investment signals.

## Reproducibility

The pipeline is designed to be rerun locally. Generated output tables, figures, raw data, and processed data are intentionally not committed as project-owned public data.
