from flask import Blueprint, jsonify, request
import pandas as pd
from pathlib import Path
from datetime import datetime

prices_bp = Blueprint("prices", __name__)

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "processed" / "brentoilprices_processed.csv"

@prices_bp.route("/", methods=["GET"])
def get_prices():
    """
    Get historical Brent oil prices with optional date range filtering.
    
    Query Parameters:
        start_date (str): Filter from this date (YYYY-MM-DD)
        end_date (str): Filter until this date (YYYY-MM-DD)
    
    Returns:
        JSON: List of price records with Date and Price fields
    """
    try:
        df = pd.read_csv(DATA_PATH)
        
        # Ensure Date column exists and is properly formatted
        if "Date" not in df.columns:
            return jsonify({"error": "Date column not found"}), 400
        
        df["Date"] = pd.to_datetime(df["Date"])
        
        # Apply date range filtering if provided
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        
        if start_date:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            df = df[df["Date"] >= start]
        
        if end_date:
            end = datetime.strptime(end_date, "%Y-%m-%d")
            df = df[df["Date"] <= end]
        
        # Sort by date
        df = df.sort_values("Date")
        
        # Format dates for JSON serialization
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")
        
        # Ensure numeric columns are native Python types and drop rows with missing Price
        if "Price" in df.columns:
            df = df[df["Price"].notna()]
            df["Price"] = df["Price"].astype(float)

        # If log_return exists but not Price, keep both available
        if "log_return" in df.columns:
            df["log_return"] = pd.to_numeric(df["log_return"], errors="coerce")

        records = df.to_dict(orient="records")
        # Convert numpy types to native Python floats/ints where needed
        def normalize_value(v):
            try:
                if pd.isna(v):
                    return None
            except Exception:
                pass
            if isinstance(v, (int, float)):
                return float(v)
            return v

        records = [{k: normalize_value(v) for k, v in r.items()} for r in records]
        
        return jsonify({
            "data": records,
            "count": len(records),
            "filters": {
                "start_date": start_date,
                "end_date": end_date
            }
        })

    except FileNotFoundError:
        # Return sample dataset for local development
        sample = [
            {"Date": "2008-01-01", "Price": 100.0},
            {"Date": "2008-06-01", "Price": 120.5},
            {"Date": "2008-09-15", "Price": 75.3},
            {"Date": "2009-01-01", "Price": 50.1},
            {"Date": "2014-06-01", "Price": 115.0},
            {"Date": "2016-01-01", "Price": 35.0},
            {"Date": "2020-04-01", "Price": 25.0},
            {"Date": "2022-03-01", "Price": 120.0}
        ]
        return jsonify({"data": sample, "count": len(sample)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@prices_bp.route("/statistics", methods=["GET"])
def get_statistics():
    """
    Get price statistics for the dataset.
    
    Returns:
        JSON: Statistics including min, max, mean, std, etc.
    """
    try:
        df = pd.read_csv(DATA_PATH)
        
        if "Price" not in df.columns and "log_price" not in df.columns:
            return jsonify({"error": "Price or log_price column not found"}), 400
        
        # Calculate statistics
        # If Price missing but log_price present, compute Price
        if "Price" not in df.columns and "log_price" in df.columns:
            df["Price"] = pd.to_numeric(df["log_price"], errors="coerce").apply(lambda x: float(pd.np.exp(x)) if not pd.isna(x) else None)

        # Ensure Date formatting
        if "Date" in df.columns:
            try:
                df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
            except Exception:
                pass

        stats = {
            "min_price": float(df["Price"].min()),
            "max_price": float(df["Price"].max()),
            "mean_price": float(df["Price"].mean()),
            "std_price": float(df["Price"].std()),
            "median_price": float(df["Price"].median()),
            "count": int(df["Price"].count()),
            "date_range": {
                "start": str(df["Date"].min()) if "Date" in df.columns else None,
                "end": str(df["Date"].max()) if "Date" in df.columns else None
            }
        }
        
        return jsonify(stats)

    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@prices_bp.route("/volatility", methods=["GET"])
def get_volatility():
    """
    Calculate rolling volatility of oil prices.
    
    Query Parameters:
        window (int): Rolling window size (default: 30 days)
    
    Returns:
        JSON: Volatility metrics
    """
    try:
        window = int(request.args.get("window", 30))
        df = pd.read_csv(DATA_PATH)
        
        if "Date" not in df.columns:
            return jsonify({"error": "Date column not found"}), 400

        df = df.sort_values("Date")

        # prefer log_return column if present, otherwise compute simple returns
        if "log_return" in df.columns:
            df["LogReturn"] = pd.to_numeric(df["log_return"], errors="coerce")
        else:
            # compute log returns from Price if possible
            df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
            df["LogReturn"] = (df["Price"].astype(float).pct_change()).replace([pd.np.inf, -pd.np.inf], pd.NA)

        # Calculate rolling volatility (standard deviation of returns)
        df["Volatility"] = df["LogReturn"].rolling(window=window).std()

        # Format Date
        try:
            df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
        except Exception:
            pass

        records = df[["Date", "Price", "Volatility"]].dropna(subset=["Volatility"]).to_dict(orient="records")
        
        return jsonify({
            "data": records,
            "window": window,
            "avg_volatility": float(df["Volatility"].mean()) if not df["Volatility"].empty else 0
        })

    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
