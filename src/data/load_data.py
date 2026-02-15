from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

from src.data.preprocess import preprocess_prices


@lru_cache(maxsize=8)
def _read_csv(path_str: str) -> pd.DataFrame:
    path = Path(path_str)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found at {path_str}")
    return pd.read_csv(path)


def load_brent_data(file_path: str) -> pd.DataFrame:
    """Backward-compatible Brent loader."""
    return load_prices(file_path)


def load_prices(file_path: str) -> pd.DataFrame:
    """Load and preprocess Brent price data."""
    df = _read_csv(file_path).copy()
    if "Date" not in df.columns or "Price" not in df.columns:
        raise ValueError("Dataset must contain 'Date' and 'Price' columns")
    return preprocess_prices(df)


def load_events(file_path: str) -> pd.DataFrame:
    """Load events and parse date-like columns."""
    events = _read_csv(file_path).copy()
    for column in ("start_date", "date", "event_date"):
        if column in events.columns:
            events[column] = pd.to_datetime(events[column], errors="coerce")
    return events
