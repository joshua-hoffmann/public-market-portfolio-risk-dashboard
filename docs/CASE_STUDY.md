# Case Study: Historical Risk Profiles of Selected Public-Market ETFs

## Analytical question

How do selected public-market ETFs differ historically in drawdowns, volatility, return behavior, and correlation behavior?

This case study uses the dashboard outputs to compare a methodological sample of public-market ETFs across several historical risk dimensions. The goal is not to identify a superior ETF or make an allocation decision. The goal is to show why portfolio risk should be reviewed across multiple dimensions rather than through asset labels or return figures alone.

## Why this matters

Portfolio discussions often use broad labels such as US equities, bonds, gold, real estate, or international equities. Those labels are useful, but they can hide important differences in realized risk behavior.

This case study makes four dimensions explicit:

- historical drawdowns,
- historical volatility,
- historical return distribution behavior,
- historical correlation behavior.

The main reader takeaway is that high cumulative return, high volatility, deep drawdowns, and co-movement with other assets are different risk dimensions. Reviewing them together gives a clearer historical risk profile than looking at any one metric in isolation.

## Data and scope

- Sample period: 
2015-01-02
 to 
2026-06-26
.
- Observations per ticker in the generated risk table: 
2887
.
- Data source: Yahoo Finance data accessed through yfinance.
- Asset universe: selected public-market ETF sample used for methodology demonstration.
- Analysis type: descriptive historical analysis only.

The selected ETF universe is a methodological sample. It is not a recommendation list, preferred investment universe, or completeness claim.

## Selected ETF sample

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

## Key historical observations

Across the selected period, the generated outputs showed materially different historical risk profiles across the ETF sample.

| Observation | Ticker | Historical value |
|---|---:|---:|
| Highest annualized volatility in the sample | 
IWM
 | 
22.45
% |
| Lowest annualized volatility in the sample | 
AGG
 | 
5.2
% |
| Deepest maximum drawdown in the sample | 
TLT
 | 
-48.35
% |
| Least deep maximum drawdown in the sample | 
AGG
 | 
-18.43
% |
| Highest cumulative return in the sample | 
QQQ
 | 
650.19
% |
| Lowest cumulative return in the sample | 
TLT
 | 
-6.12
% |
| Worst single daily return in the sample | 
VNQ
 | 
-17.73
% |
| Best single daily return in the sample | 
QQQ
 | 
12
% |

These observations are descriptive only. They summarize what happened in the selected sample period and do not imply future performance, future risk, or investment suitability.

## Interpretation

The historical outputs show that the selected ETFs did not differ only by asset label. They differed by the type of historical risk they exhibited.

One selected ETF had the highest cumulative return in the generated table, while another had the highest annualized volatility. The deepest maximum drawdown appeared in a different exposure than the highest cumulative return. This illustrates why a single return-oriented view is not enough to describe historical risk.

The case study therefore separates three questions that are often mixed together:

1. Which assets experienced larger historical declines?
2. Which assets showed higher or lower realized volatility?
3. Which assets moved more or less closely together during the selected period?

Reviewing these questions together helps the reader understand the structure of historical risk rather than treating each ETF as a simple label.

## Correlation interpretation

The correlation matrix provides another layer of interpretation. Historical correlations describe how daily returns moved together during the selected period. They are useful for understanding sample-period co-movement, but they should not be interpreted as stable future relationships.

In this project, the correlation output is not used to claim diversification benefits. It is used to show that assets can have different historical relationships with one another, and that those relationships should be reviewed explicitly rather than assumed from asset labels.

## What the reader should learn

The main insight is not that one ETF is better than another. The main insight is that selected public-market ETFs can show very different historical risk profiles depending on which dimension is reviewed.

A return figure alone does not show:

- how deep historical losses became,
- how volatile the path was,
- whether volatility changed over time,
- how strongly the asset moved with other assets,
- whether apparent diversification was visible in the selected historical window.

This dashboard turns those dimensions into reproducible outputs that can be reviewed together.

## Limitations

- This is a descriptive historical case study only.
- It is not investment advice.
- It does not provide buy, sell, hold, allocation, optimization, or timing guidance.
- It does not forecast future returns, volatility, drawdowns, or correlations.
- It does not identify superior ETFs.
- It does not validate an investment model.
- Yahoo Finance data accessed through yfinance is practical for a reproducible public-market workflow, but it is not treated as institutionally validated data.
- Raw downloaded market data is not redistributed as project-owned or freely licensed data.
- Results depend on the selected source, date range, asset universe, and calculation choices.

## Reproducibility

The case study is generated from the same local pipeline used by the dashboard. To reproduce the outputs, run the project pipeline from the repository root after installing the package and dependencies.

Expected generated outputs include:

- outputs/tables/data_preflight.csv
- outputs/tables/risk_metric_table.csv
- outputs/tables/correlation_matrix.csv
- outputs/figures/drawdown_chart.png
- outputs/figures/rolling_volatility_chart.png
- outputs/figures/correlation_heatmap.png

Generated outputs are local artifacts and are not redistributed as raw market data.
