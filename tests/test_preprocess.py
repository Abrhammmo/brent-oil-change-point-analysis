from __future__ import annotations

import pandas as pd

from src.data.preprocess import preprocess_prices


def test_preprocess_prices_creates_log_columns() -> None:
    raw = pd.DataFrame(
        {
            "Date": ["2020-01-02", "2020-01-01", "2020-01-03"],
            "Price": [11.0, 10.0, 12.0],
        }
    )
    out = preprocess_prices(raw)
    assert "log_price" in out.columns
    assert "log_return" in out.columns
    assert out["Date"].iloc[0].strftime("%Y-%m-%d") == "2020-01-01"
