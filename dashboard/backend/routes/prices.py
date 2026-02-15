from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
from flask import Blueprint, current_app, jsonify, request

from src.constants import DEFAULT_VOLATILITY_WINDOW
from src.data.macro_loader import load_macro_data

prices_bp = Blueprint("prices", __name__)

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_PATH = BASE_DIR / "data" / "processed" / "brentoilprices_processed.csv"


def _get_cache() -> Any:
    return current_app.config.get("CACHE")


def _load_prices() -> pd.DataFrame:
    cache = _get_cache()
    cache_key = "prices_df"
    if cache is not None:
        cached = cache.get(cache_key)
        if cached is not None:
            return cached.copy()

    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    if "log_return" in df.columns:
        df["log_return"] = pd.to_numeric(df["log_return"], errors="coerce")
    if cache is not None:
        cache.set(cache_key, df.copy())
    return df


def _parse_date(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d")


@prices_bp.route("/", methods=["GET"])
def get_prices() -> Any:
    try:
        df = _load_prices()
        start_date = _parse_date(request.args.get("start_date"))
        end_date = _parse_date(request.args.get("end_date"))

        if start_date is not None:
            df = df[df["Date"] >= start_date]
        if end_date is not None:
            df = df[df["Date"] <= end_date]

        df = df.sort_values("Date")
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

        records = df.to_dict(orient="records")
        normalized: list[Dict[str, Any]] = []
        for record in records:
            item: Dict[str, Any] = {}
            for key, value in record.items():
                if pd.isna(value):
                    item[key] = None
                elif isinstance(value, (np.integer, np.floating)):
                    item[key] = float(value)
                else:
                    item[key] = value
            normalized.append(item)

        return jsonify(
            {
                "data": normalized,
                "count": len(normalized),
                "filters": {
                    "start_date": request.args.get("start_date"),
                    "end_date": request.args.get("end_date"),
                },
            }
        )
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500


@prices_bp.route("/statistics", methods=["GET"])
def get_statistics() -> Any:
    try:
        df = _load_prices()
        stats: Dict[str, Any] = {
            "min_price": float(df["Price"].min()),
            "max_price": float(df["Price"].max()),
            "mean_price": float(df["Price"].mean()),
            "std_price": float(df["Price"].std()),
            "median_price": float(df["Price"].median()),
            "count": int(df["Price"].count()),
            "date_range": {
                "start": df["Date"].min().strftime("%Y-%m-%d"),
                "end": df["Date"].max().strftime("%Y-%m-%d"),
            },
        }
        return jsonify(stats)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500


@prices_bp.route("/volatility", methods=["GET"])
def get_volatility() -> Any:
    try:
        window = int(request.args.get("window", DEFAULT_VOLATILITY_WINDOW))
        df = _load_prices().sort_values("Date")
        if "log_return" not in df.columns:
            df["log_return"] = np.log(df["Price"]).diff()
        df["Volatility"] = df["log_return"].rolling(window=window).std()
        df["Date"] = df["Date"].dt.strftime("%Y-%m-%d")

        records = (
            df[["Date", "Price", "Volatility"]]
            .dropna(subset=["Volatility"])
            .to_dict(orient="records")
        )
        return jsonify(
            {
                "data": records,
                "window": window,
                "avg_volatility": float(pd.DataFrame(records)["Volatility"].mean())
                if records
                else 0.0,
            }
        )
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500


@prices_bp.route("/macro-overlay", methods=["GET"])
def get_macro_overlay() -> Any:
    """Return oil prices merged with GDP, inflation, and FX series."""
    try:
        df = _load_prices()
        merged = load_macro_data(df)
        merged["Date"] = merged["Date"].dt.strftime("%Y-%m-%d")
        out_cols = ["Date", "Price", "GDP", "Inflation", "ExchangeRate"]
        return jsonify({"data": merged[out_cols].to_dict(orient="records"), "count": len(merged)})
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500
