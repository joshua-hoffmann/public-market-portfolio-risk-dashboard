"""Chart generation for approved descriptive outputs.

Uses a non-interactive Matplotlib backend so chart generation works in local
and headless environments without requiring Tk/Tcl GUI support.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd


def save_drawdown_chart(drawdowns: pd.DataFrame, output_path: str | Path) -> None:
    """Save historical drawdown chart."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ax = drawdowns.plot(figsize=(12, 7), title="Historical Drawdowns")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.figure.tight_layout()
    ax.figure.savefig(output_path, dpi=150)
    plt.close(ax.figure)


def save_rolling_volatility_chart(rolling_volatility: pd.DataFrame, output_path: str | Path) -> None:
    """Save historical rolling volatility chart."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    ax = rolling_volatility.plot(figsize=(12, 7), title="Historical Rolling Volatility")
    ax.set_xlabel("Date")
    ax.set_ylabel("Annualized volatility")
    ax.figure.tight_layout()
    ax.figure.savefig(output_path, dpi=150)
    plt.close(ax.figure)


def save_correlation_heatmap(correlation_matrix: pd.DataFrame, output_path: str | Path) -> None:
    """Save historical correlation heatmap without investment interpretation."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 7))
    image = ax.imshow(correlation_matrix.values, aspect="auto")
    ax.set_xticks(range(len(correlation_matrix.columns)))
    ax.set_yticks(range(len(correlation_matrix.index)))
    ax.set_xticklabels(correlation_matrix.columns, rotation=45, ha="right")
    ax.set_yticklabels(correlation_matrix.index)
    ax.set_title("Historical Return Correlation")
    fig.colorbar(image, ax=ax)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
