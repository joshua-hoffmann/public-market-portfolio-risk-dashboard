"""Configuration for the descriptive historical risk dashboard.

Candidate tickers are not investment recommendations.
They are a methodological sample for data preflight and later governance review.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProjectConfig:
    start_date: str = "2015-01-01"
    end_date: str | None = None
    rolling_window_days: int = 63
    annualization_days: int = 252
    min_observations: int = 756


CANDIDATE_TICKERS: dict[str, str] = {
    "SPY": "US large-cap equity ETF candidate",
    "QQQ": "US growth/technology-heavy equity ETF candidate",
    "IWM": "US small-cap equity ETF candidate",
    "EFA": "Developed ex-US equity ETF candidate",
    "TLT": "Long-duration US Treasury ETF candidate",
    "GLD": "Gold exposure ETF candidate",
    "VNQ": "US real estate ETF candidate",
    "AGG": "US aggregate bond ETF candidate",
}


DEFAULT_CONFIG = ProjectConfig()
