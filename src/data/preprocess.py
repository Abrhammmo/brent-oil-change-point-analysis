import numpy as np
import pandas as pd

def preprocess_prices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert dates, sort values, and compute log returns.
    """
    try:
        df = df.copy()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])
        df = df.sort_values("Date")

        df["log_price"] = np.log(df["Price"])
        df["log_return"] = df["log_price"].diff()

        print("✅ Preprocessing completed (datetime + log returns).")
        return df

    except Exception as e:
        print(f"❌ Preprocessing failed: {e}")
        raise
