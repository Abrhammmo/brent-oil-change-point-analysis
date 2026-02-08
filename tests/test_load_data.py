import os
import pandas as pd

from src.data.load_data import load_prices, load_events


def test_load_prices_mixed_dates(tmp_path):
    # Create a small CSV with mixed date formats (one two-digit year, one long format)
    csv = tmp_path / "prices.csv"
    csv.write_text('Date,Price\n20-May-87,18.63\n"Apr 22, 2020",45.0\n')

    df = load_prices(str(csv))

    # After cleaning and differencing, there should be at least one row
    assert len(df) >= 1
    # Date column should be datetime
    assert pd.api.types.is_datetime64_any_dtype(df["Date"]) 
    # log_return should exist and be numeric
    assert "log_return" in df.columns
    assert pd.api.types.is_float_dtype(df["log_return"]) 


def test_load_events_parsing(tmp_path):
    csv = tmp_path / "events.csv"
    csv.write_text('event_id,event_name,start_date\n1,TestEvent,2020-04-22\n')

    events = load_events(str(csv))
    assert len(events) == 1
    assert "start_date" in events.columns
    assert pd.api.types.is_datetime64_any_dtype(events["start_date"]) 
