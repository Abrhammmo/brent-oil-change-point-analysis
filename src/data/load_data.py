import pandas as pd
from pathlib import Path

def load_brent_data(file_path: str) -> pd.DataFrame:
    """
    Load Brent oil price data with robust error handling.
    """
    try:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Data file not found at {file_path}")

        df = pd.read_csv(path)

        if "Date" not in df.columns or "Price" not in df.columns:
            raise ValueError("Dataset must contain 'Date' and 'Price' columns")

        print("✅ Data loaded successfully.")
        return df

    except Exception as e:
        print(f"❌ Error loading data: {e}")
        raise
