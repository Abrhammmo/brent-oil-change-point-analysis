from __future__ import annotations

import pandas as pd

from src.analysis.event_mapping import map_tau_to_date, map_taus_to_dates


def test_map_tau_to_date_returns_timestamp() -> None:
    df = pd.DataFrame({"Date": pd.date_range("2020-01-01", periods=10)})
    mapped = map_tau_to_date(df, 3)
    assert mapped.strftime("%Y-%m-%d") == "2020-01-04"


def test_map_taus_to_dates_multiple() -> None:
    df = pd.DataFrame({"Date": pd.date_range("2020-01-01", periods=10)})
    mapped = map_taus_to_dates(df, [1, 5])
    assert mapped == ["2020-01-02", "2020-01-06"]
