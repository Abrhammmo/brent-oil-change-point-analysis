from __future__ import annotations

import numpy as np
import pandas as pd


def preprocess_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Convert date column, sort, and derive log metrics."""
    data = df.copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.dropna(subset=["Date", "Price"]).sort_values("Date")
    data["Price"] = pd.to_numeric(data["Price"], errors="coerce")
    data = data.dropna(subset=["Price"])
    data["log_price"] = np.log(data["Price"])
    data["log_return"] = data["log_price"].diff()
    return data.reset_index(drop=True)
