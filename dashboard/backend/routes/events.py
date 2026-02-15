from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import pandas as pd
from flask import Blueprint, jsonify, request

events_bp = Blueprint("events", __name__)

BASE_DIR = Path(__file__).resolve().parents[3]
EVENTS_PATH = BASE_DIR / "data" / "processed" / "events.csv"
PRICES_PATH = BASE_DIR / "data" / "processed" / "brentoilprices_processed.csv"


def _event_date_column(df: pd.DataFrame) -> Optional[str]:
    for col in ("start_date", "date", "event_date"):
        if col in df.columns:
            return col
    return None


@events_bp.route("/", methods=["GET"])
def get_events() -> Any:
    try:
        df = pd.read_csv(EVENTS_PATH)
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        category = request.args.get("category")

        date_col = _event_date_column(df)
        if date_col is not None:
            df["_date"] = pd.to_datetime(df[date_col], errors="coerce")
            if start_date:
                df = df[df["_date"] >= datetime.strptime(start_date, "%Y-%m-%d")]
            if end_date:
                df = df[df["_date"] <= datetime.strptime(end_date, "%Y-%m-%d")]

        if category and "category" in df.columns:
            df = df[df["category"] == category]

        events: list[Dict[str, Any]] = []
        for _, row in df.iterrows():
            events.append(
                {
                    "date": str(row.get(date_col, "")) if date_col else None,
                    "title": row.get("event_name") or row.get("title") or row.get("event") or "",
                    "description": row.get("description") or "",
                    "category": row.get("category") or "",
                }
            )
        events.sort(key=lambda item: item["date"] or "", reverse=True)
        return jsonify({"events": events, "count": len(events)})
    except FileNotFoundError:
        return jsonify({"events": [], "count": 0})
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500


@events_bp.route("/correlation", methods=["GET"])
def get_event_correlation() -> Any:
    try:
        event_date = request.args.get("event_date")
        window = int(request.args.get("window", 30))
        if not event_date:
            return jsonify({"error": "event_date parameter required"}), 400

        events_df = pd.read_csv(EVENTS_PATH)
        prices_df = pd.read_csv(PRICES_PATH)
        prices_df["Date"] = pd.to_datetime(prices_df["Date"], errors="coerce")
        date_col = _event_date_column(events_df)
        if date_col is None:
            return jsonify({"error": "No date column found in events"}), 400

        event_rows = events_df[events_df[date_col].astype(str) == event_date]
        if event_rows.empty:
            return jsonify({"error": "Event not found"}), 404
        event_row = event_rows.iloc[0]
        event_title = event_row.get("event_name") or event_row.get("title") or event_row.get("event", "")

        event_dt = datetime.strptime(event_date, "%Y-%m-%d")
        before_start = event_dt - timedelta(days=window)
        after_end = event_dt + timedelta(days=window)
        before = prices_df[(prices_df["Date"] >= before_start) & (prices_df["Date"] < event_dt)]
        after = prices_df[(prices_df["Date"] > event_dt) & (prices_df["Date"] <= after_end)]
        before_avg = before["Price"].mean() if not before.empty else None
        after_avg = after["Price"].mean() if not after.empty else None
        pct = ((after_avg - before_avg) / before_avg * 100.0) if before_avg and after_avg else None

        nearby = prices_df[(prices_df["Date"] >= before_start) & (prices_df["Date"] <= after_end)].copy()
        nearby["Date"] = nearby["Date"].dt.strftime("%Y-%m-%d")
        return jsonify(
            {
                "event": {"date": event_date, "title": event_title},
                "analysis": {
                    "window_days": window,
                    "before_avg_price": round(float(before_avg), 2) if before_avg else None,
                    "after_avg_price": round(float(after_avg), 2) if after_avg else None,
                    "price_change_percent": round(float(pct), 2) if pct else None,
                },
                "chart_data": nearby[["Date", "Price"]].to_dict(orient="records"),
            }
        )
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500


@events_bp.route("/impact", methods=["GET"])
def get_event_impact() -> Any:
    try:
        events_df = pd.read_csv(EVENTS_PATH)
        prices_df = pd.read_csv(PRICES_PATH)
        prices_df["Date"] = pd.to_datetime(prices_df["Date"], errors="coerce")
        date_col = _event_date_column(events_df)
        if date_col is None:
            return jsonify({"impacts": [], "count": 0})

        impacts: list[Dict[str, Any]] = []
        for _, event in events_df.iterrows():
            if not event.get(date_col):
                continue
            event_dt = pd.to_datetime(event.get(date_col), errors="coerce")
            if pd.isna(event_dt):
                continue
            before = prices_df[(prices_df["Date"] >= event_dt - timedelta(days=30)) & (prices_df["Date"] < event_dt)]
            after = prices_df[(prices_df["Date"] > event_dt) & (prices_df["Date"] <= event_dt + timedelta(days=30))]
            before_avg = before["Price"].mean() if not before.empty else None
            after_avg = after["Price"].mean() if not after.empty else None
            pct = ((after_avg - before_avg) / before_avg * 100.0) if before_avg and after_avg else None
            impacts.append(
                {
                    "date": str(event.get(date_col)),
                    "title": event.get("event_name") or event.get("title") or event.get("event", ""),
                    "category": event.get("category") or "",
                    "price_change_percent": round(float(pct), 2) if pct else None,
                }
            )

        impacts.sort(key=lambda item: abs(item["price_change_percent"] or 0.0), reverse=True)
        return jsonify({"impacts": impacts, "count": len(impacts)})
    except FileNotFoundError:
        return jsonify({"impacts": [], "count": 0})
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500
