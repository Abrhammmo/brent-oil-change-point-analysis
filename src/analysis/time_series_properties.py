from __future__ import annotations

from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd


def compute_volatility_metrics(df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    """Compute rolling volatility metrics from log returns."""
    data = df.copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.sort_values("Date")
    data["rolling_volatility"] = data["log_return"].rolling(window=window).std()
    return data


def summarize_series(df: pd.DataFrame) -> Dict[str, float]:
    """Return compact descriptive metrics."""
    price = pd.to_numeric(df["Price"], errors="coerce")
    return {
        "mean_price": float(price.mean()),
        "std_price": float(price.std()),
        "min_price": float(price.min()),
        "max_price": float(price.max()),
    }


def plot_price_and_returns(df: pd.DataFrame) -> None:
    """Plot price and log return series."""
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    axes[0].plot(df["Date"], df["Price"])
    axes[0].set_title("Brent Oil Price")
    axes[1].plot(df["Date"], df["log_return"])
    axes[1].set_title("Log Returns")
    plt.tight_layout()
    plt.show()
