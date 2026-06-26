# Portfolio Risk Dashboard

This project provides a reproducible dashboard for descriptively comparing selected public-market ETFs using historical data. It focuses on volatility, drawdowns, return distributions, and correlation behavior over a defined sample period.

The goal is to demonstrate a transparent analytical workflow and interpretation framework. It is not designed to provide investment advice, forecasts, rankings, allocation guidance, or portfolio recommendations.

## Important interpretation notes

This project is a descriptive, historical analysis tool for comparing selected public-market ETFs. It is not investment advice and does not provide buy, sell, hold, allocation, optimization, or forecasting recommendations.

The MVP uses Yahoo Finance data accessed through yfinance. This source is practical for reproducible public-market analysis, but it is not institutionally validated or investment-grade data.

The selected ETF universe is a methodological sample used to demonstrate the dashboard workflow. It is not a recommendation list and should not be interpreted as a preferred investment universe.

Historical volatility, drawdowns, return distributions, and correlations describe the selected sample period only. They do not predict future returns, future risk, or future diversification benefits.

Raw downloaded market data is not redistributed as project-owned or freely licensed data.

## What this project does

- Downloads historical adjusted price data for a selected ETF sample.
- Calculates descriptive historical return and risk metrics.
- Generates a risk metric table.
- Generates historical drawdown, rolling volatility, and correlation outputs.
- Provides a reproducible local workflow for methodology-first analysis.

## What this project does not do

- It does not provide investment advice.
- It does not provide buy, sell, hold, allocation, or timing guidance.
- It does not forecast future returns, volatility, drawdowns, or correlations.
- It does not identify superior ETFs or selected exposure examples.
- It does not perform portfolio optimization.
- It does not validate an investment model.
- It does not treat Yahoo Finance or yfinance data as institutionally validated market data.

## Data source and source limitations

The MVP uses Yahoo Finance data accessed through the Python package yfinance.

This source is useful for a practical, reproducible public-market-data workflow, but it has important limitations:

- The data source is external to this project.
- Data availability and formatting may change.
- The data is not institutionally validated by this project.
- The project does not redistribute raw downloaded market data.
- Results depend on the selected source, date range, and asset universe.

Users should rerun the data preflight before relying on any generated outputs for analysis.

## Asset universe

The MVP uses the following selected ETF sample:

| Ticker | Role in sample |
|---|---|
| SPY | US large-cap equity ETF sample |
| QQQ | US growth or technology-heavy equity ETF sample |
| IWM | US small-cap equity ETF sample |
| EFA | Developed ex-US equity ETF sample |
| TLT | Long-duration US Treasury ETF sample |
| GLD | Gold exposure ETF sample |
| VNQ | US real estate ETF sample |
| AGG | US aggregate bond ETF sample |

This universe is a methodological sample for demonstrating the workflow. It is not a recommendation list, preferred investment universe, or completeness claim.

## Methodology

The workflow follows these steps:

1. Load the selected ticker sample from the project configuration.
2. Download adjusted historical prices using yfinance.
3. Run a data preflight to check availability, date coverage, observations, and missing values.
4. Calculate daily returns from adjusted prices.
5. Calculate descriptive historical metrics.
6. Generate output tables and charts.
7. Save generated outputs locally under outputs/.

All outputs should be interpreted within the selected source, date range, calculation method, and asset universe.

## Metrics included

The MVP includes these descriptive historical metrics and outputs:

- Historical annualized volatility.
- Historical drawdowns.
- Historical maximum drawdown.
- Historical daily return distribution summaries.
- Historical return correlation matrix.
- Historical rolling volatility.
- Historical cumulative return over the selected period.

These metrics describe selected historical return behavior only. They do not measure all forms of risk, investor suitability, liquidity, fees, tax effects, tracking error, or future market behavior.

## How to run the dashboard

From the project root, create a virtual environment, install the project, run tests, and execute the pipeline:

1. python -m venv .venv
2. .\.venv\Scripts\python.exe -m pip install --upgrade pip
3. .\.venv\Scripts\python.exe -m pip install -e .
4. .\.venv\Scripts\python.exe -m pytest -q
5. .\.venv\Scripts\python.exe -m portfolio_risk_dashboard.pipeline

The pipeline writes generated files to:

- outputs/tables/data_preflight.csv
- outputs/tables/risk_metric_table.csv
- outputs/tables/correlation_matrix.csv
- outputs/figures/drawdown_chart.png
- outputs/figures/rolling_volatility_chart.png
- outputs/figures/correlation_heatmap.png

Generated output files are local artifacts and may be regenerated by rerunning the pipeline.

## Validation and reproducibility

The project includes unit tests for core metric calculations.

Expected validation command:

.\.venv\Scripts\python.exe -m pytest -q

The data preflight checks whether the selected tickers have usable adjusted price history for the configured period.

Validation in this project supports workflow reproducibility and basic calculation checks. It does not validate an investment model, predictive model, or trading strategy.

## Interpreting the outputs

Outputs are historical and descriptive only.

- A drawdown chart shows historical peak-to-trough declines during the selected sample period.
- A rolling volatility chart shows realized historical volatility over a rolling window.
- A correlation heatmap shows sample-period historical return relationships.
- A risk metric table summarizes selected historical return and risk statistics.

Charts and tables are not rankings, recommendations, forecasts, or investment signals. Higher or lower metric values are descriptive observations within the selected period and data source.

Correlation values are sample-period historical relationships. They should not be interpreted as stable future relationships or assured future diversification benefits.

## Limitations

- The analysis is historical-only and descriptive-only.
- Results depend on the selected data source, date range, ticker sample, and calculation choices.
- The ETF sample is not comprehensive and is not a recommendation list.
- yfinance data is practical for an MVP workflow but is not treated as institutionally validated data.
- The project does not redistribute raw downloaded market data.
- Metrics shown do not measure all forms of risk.
- Historical correlations may change materially across different periods.
- Historical drawdowns and volatility do not predict future drawdowns or volatility.
- The project does not include portfolio optimization, allocation guidance, forecasts, or investment recommendations.

## Repository structure

portfolio-risk-dashboard-public-market-data/
  docs/
    governance/
    internal/
  src/
    portfolio_risk_dashboard/
      config.py
      data_loader.py
      metrics.py
      charts.py
      pipeline.py
  outputs/
    figures/
    tables/
  tests/
    test_metrics.py
  pyproject.toml
  README.md

## License / data redistribution notice

The project code may be licensed separately by the repository owner. Raw downloaded market data is not included as project-owned or freely licensed data.

Users are responsible for complying with the terms of the external data source they access.

## Disclaimer

This project is for educational and methodological analysis only. It is not financial advice, investment advice, a recommendation, a forecast, or a portfolio-construction tool.

Nothing in this repository should be interpreted as a suggestion to buy, sell, hold, allocate to, avoid, or prefer any asset.
