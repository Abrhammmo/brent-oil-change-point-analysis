from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd


def _parse_dates(series: pd.Series) -> pd.Series:
    """Parse a series of date-like strings robustly.

    Raises ValueError with examples if parsing fails for any values.
    """
    try:
        dt = pd.to_datetime(series, dayfirst=False, errors="coerce")
    except TypeError:
        dt = pd.to_datetime(series, errors="coerce")

    if dt.isna().any():
        bad = series[dt.isna()].head(10).tolist()
        raise ValueError(f"Failed to parse these date strings (examples): {bad}")
    return dt


def load_prices(path: Optional[str] = None) -> pd.DataFrame:
    """Load Brent price CSV and return cleaned DataFrame.

    Behavior:
    - If `path` provided, load from that path.
    - Otherwise prefer `data/processed/prices.csv` and fall back to `data/raw/BrentOilPrices.csv`.
    - Parse `Date` robustly, sort chronologically, coerce `Price` to numeric.
    - Compute `log_price` and `log_return` and drop rows with NA (e.g., the first diff).

    Returns a DataFrame with columns at least: `Date`, `Price`, `log_price`, `log_return`.
    """
    base = Path.cwd()
    if path:
        p = Path(path)
    else:
        p = base / "data" / "processed" / "prices.csv"

    if not p.exists():
        raw = base / "data" / "raw" / "BrentOilPrices.csv"
        if not raw.exists():
            raise FileNotFoundError(f"No price file found at {p} or {raw}")
        p = raw

    df = pd.read_csv(p)

    if "Date" not in df.columns:
        raise KeyError("Expected a 'Date' column in prices CSV")
    if "Price" not in df.columns:
        raise KeyError("Expected a 'Price' column in prices CSV")

    df["Date"] = _parse_dates(df["Date"])
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.sort_values("Date").reset_index(drop=True)

    # log transforms and returns
    df["log_price"] = np.log(df["Price"])
    df["log_return"] = df["log_price"].diff()

    # drop NaNs introduced by diff or any bad rows
    df = df.dropna().reset_index(drop=True)
    return df


def load_events(path: Optional[str] = None) -> pd.DataFrame:
    """Load event CSV and return DataFrame with parsed `start_date`.

    - If `path` provided, load from that path.
    - Otherwise prefer `data/processed/events.csv` and fall back to `data/raw/events.csv`.
    """
    base = Path.cwd()
    if path:
        p = Path(path)
    else:
        p = base / "data" / "processed" / "events.csv"

    if not p.exists():
        raw = base / "data" / "raw" / "events.csv"
        if not raw.exists():
            raise FileNotFoundError(f"No events file found at {p} or {raw}")
        p = raw

    events = pd.read_csv(p)
    if "start_date" in events.columns:
        events["start_date"] = pd.to_datetime(events["start_date"], errors="coerce")
    return events
