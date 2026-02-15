from __future__ import annotations

from typing import Iterable, List

import pandas as pd


def map_tau_to_date(df: pd.DataFrame, tau_index: int) -> pd.Timestamp:
    """Map a change-point index to a calendar date."""
    data = df.reset_index(drop=True)
    idx = max(0, min(int(tau_index), len(data) - 1))
    return pd.to_datetime(data.iloc[idx]["Date"])


def map_taus_to_dates(df: pd.DataFrame, tau_indices: Iterable[int]) -> List[str]:
    """Map multiple change-point indices to yyyy-mm-dd dates."""
    return [map_tau_to_date(df, tau).strftime("%Y-%m-%d") for tau in tau_indices]
