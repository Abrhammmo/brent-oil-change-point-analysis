from __future__ import annotations

from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


def build_synthetic_macro_data(dates: pd.Series) -> pd.DataFrame:
    """Create deterministic synthetic macro features aligned to provided dates."""
    idx = np.arange(len(dates), dtype=float)
    base = pd.DataFrame({"Date": pd.to_datetime(dates)})
    base["GDP"] = 100 + 0.02 * idx + 1.5 * np.sin(idx / 240.0)
    base["Inflation"] = 2.0 + 0.6 * np.sin(idx / 120.0) + 0.2 * np.cos(idx / 30.0)
    base["ExchangeRate"] = 1.2 + 0.03 * np.cos(idx / 180.0)
    return base


def load_macro_data(
    oil_df: pd.DataFrame,
    macro_path: Optional[str] = None,
) -> pd.DataFrame:
    """
    Load GDP/Inflation/ExchangeRate data and align it with oil dates.

    If no macro file exists, synthetic aligned data is generated to keep the
    workflow executable and testable.
    """
    oil = oil_df.copy()
    oil["Date"] = pd.to_datetime(oil["Date"], errors="coerce")
    oil = oil.dropna(subset=["Date"]).sort_values("Date")

    macro_df: pd.DataFrame
    if macro_path is not None and Path(macro_path).exists():
        macro_df = pd.read_csv(macro_path)
        macro_df["Date"] = pd.to_datetime(macro_df["Date"], errors="coerce")
        macro_df = macro_df.dropna(subset=["Date"]).sort_values("Date")
    else:
        macro_df = build_synthetic_macro_data(oil["Date"])

    merged = pd.merge_asof(
        oil.sort_values("Date"),
        macro_df.sort_values("Date"),
        on="Date",
        direction="nearest",
    )
    for col in ("GDP", "Inflation", "ExchangeRate"):
        merged[col] = pd.to_numeric(merged[col], errors="coerce")
    return merged.dropna(subset=["GDP", "Inflation", "ExchangeRate"])
