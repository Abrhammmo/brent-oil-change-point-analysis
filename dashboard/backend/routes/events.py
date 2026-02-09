from flask import Blueprint, jsonify, request
import pandas as pd
import json
from pathlib import Path
from datetime import datetime, timedelta

events_bp = Blueprint("events", __name__)

BASE_DIR = Path(__file__).resolve().parents[3]
EVENTS_PATH = BASE_DIR / ".." / "data" / "processed" / "events.csv"
PRICES_PATH = BASE_DIR /".." / "data" / "processed" / "brentoilprices_processed.csv"

@events_bp.route("/", methods=["GET"])
def get_events():
    """
    Get market events with optional filtering.
    
    Query Parameters:
        start_date (str): Filter events from this date (YYYY-MM-DD)
        end_date (str): Filter events until this date (YYYY-MM-DD)
        category (str): Filter by event category if available
    
    Returns:
        JSON: List of event objects
    """
    try:
        # read CSV and map to minimal event objects expected by frontend
        df = pd.read_csv(EVENTS_PATH)
        
        # Apply date filtering if provided
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        category = request.args.get("category")
        
        # Determine date column
        date_col = None
        for c in ["start_date", "date", "event_date"]:
            if c in df.columns:
                date_col = c
                break
        
        if date_col:
            df["filter_date"] = pd.to_datetime(df[date_col], errors='coerce')
            
            if start_date:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                df = df[df["filter_date"] >= start]
            
            if end_date:
                end = datetime.strptime(end_date, "%Y-%m-%d")
                df = df[df["filter_date"] <= end]
        
        # Filter by category if available
        if category and "category" in df.columns:
            df = df[df["category"] == category]
        
        events = []
        for _, row in df.iterrows():
            date_val = str(row[date_col]) if date_col is not None and pd.notna(row[date_col]) else None
            title = row.get("event_name") or row.get("title") or row.get("event") or ""
            description = row.get("description") or ""
            category_val = row.get("category", "")
            
            events.append({
                "date": date_val,
                "title": title,
                "description": description,
                "category": category_val
            })
        
        # Sort by date
        events = sorted(events, key=lambda x: x["date"] or "", reverse=True)
        
        return jsonify({
            "events": events,
            "count": len(events)
        })

    except FileNotFoundError:
        # Return sample events for local development
        sample_events = [
            {"date": "2008-09-15", "title": "Lehman Brothers Collapse", "description": "Global financial crisis intensifies", "category": "Economic"},
            {"date": "2008-07-01", "title": "Oil Price Peak", "description": "Crude oil reaches all-time high of $147/barrel", "category": "Market"},
            {"date": "2014-11-01", "title": "OPEC Production Decision", "description": "OPEC maintains production levels despite oversupply", "category": "Policy"},
            {"date": "2016-01-01", "title": "Price Recovery Begins", "description": "Market starts stabilization", "category": "Market"},
            {"date": "2020-04-01", "title": "COVID-19 Impact", "description": "Oil prices plunge amid pandemic demand collapse", "category": "Health"},
            {"date": "2022-02-01", "title": "Russia-Ukraine Conflict", "description": "Geopolitical tensions drive price surge", "category": "Geopolitical"}
        ]
        return jsonify({"events": sample_events, "count": len(sample_events)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@events_bp.route("/correlation", methods=["GET"])
def get_event_correlation():
    """
    Get price correlations around major events.
    
    Query Parameters:
        event_date (str): Date of the event to analyze (YYYY-MM-DD)
        window (int): Days before/after to analyze (default: 30)
    
    Returns:
        JSON: Price changes and statistics around the event
    """
    try:
        event_date = request.args.get("event_date")
        window = int(request.args.get("window", 30))
        
        if not event_date:
            return jsonify({"error": "event_date parameter required"}), 400
        
        # Load events
        events_df = pd.read_csv(EVENTS_PATH)
        prices_df = pd.read_csv(PRICES_PATH)
        
        prices_df["Date"] = pd.to_datetime(prices_df["Date"])
        
        # Find the event
        date_col = next((c for c in ["start_date", "date", "event_date"] if c in events_df.columns), None)
        event_row = events_df[events_df[date_col] == event_date].iloc[0] if date_col else None
        
        if event_row is None:
            return jsonify({"error": "Event not found"}), 404
        
        event_title = event_row.get("event_name") or event_row.get("title") or event_row.get("event", "")
        
        # Calculate price change around event
        event_dt = datetime.strptime(event_date, "%Y-%m-%d")
        before_start = event_dt - timedelta(days=window)
        after_end = event_dt + timedelta(days=window)
        
        before_prices = prices_df[(prices_df["Date"] >= before_start) & (prices_df["Date"] < event_dt)]
        after_prices = prices_df[(prices_df["Date"] > event_dt) & (prices_df["Date"] <= after_end)]
        
        before_avg = before_prices["Price"].mean() if not before_prices.empty else None
        after_avg = after_prices["Price"].mean() if not after_prices.empty else None
        
        price_change = None
        if before_avg and after_avg:
            price_change = ((after_avg - before_avg) / before_avg) * 100
        
        # Get nearby prices for charting
        nearby = prices_df[(prices_df["Date"] >= before_start) & (prices_df["Date"] <= after_end)]
        nearby["Date"] = nearby["Date"].dt.strftime("%Y-%m-%d")
        chart_data = nearby[["Date", "Price"]].to_dict(orient="records")
        
        return jsonify({
            "event": {
                "date": event_date,
                "title": event_title
            },
            "analysis": {
                "window_days": window,
                "before_avg_price": round(before_avg, 2) if before_avg else None,
                "after_avg_price": round(after_avg, 2) if after_avg else None,
                "price_change_percent": round(price_change, 2) if price_change else None
            },
            "chart_data": chart_data
        })

    except FileNotFoundError as e:
        return jsonify({"error": f"Data file not found: {str(e)}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@events_bp.route("/impact", methods=["GET"])
def get_event_impact():
    """
    Get impact analysis for all major events.
    
    Returns:
        JSON: List of events with their price impact analysis
    """
    try:
        events_df = pd.read_csv(EVENTS_PATH)
        prices_df = pd.read_csv(PRICES_PATH)
        
        prices_df["Date"] = pd.to_datetime(prices_df["Date"])
        
        date_col = next((c for c in ["start_date", "date", "event_date"] if c in events_df.columns), None)
        window = 30  # 30 days before/after
        
        impacts = []
        for _, event in events_df.iterrows():
            event_date = event.get(date_col) if date_col else None
            if not event_date:
                continue
                
            try:
                event_dt = pd.to_datetime(event_date)
            except:
                continue
            
            before_start = event_dt - timedelta(days=window)
            after_end = event_dt + timedelta(days=window)
            
            before_prices = prices_df[(prices_df["Date"] >= before_start) & (prices_df["Date"] < event_dt)]
            after_prices = prices_df[(prices_df["Date"] > event_dt) & (prices_df["Date"] <= after_end)]
            
            before_avg = before_prices["Price"].mean() if not before_prices.empty else None
            after_avg = after_prices["Price"].mean() if not after_prices.empty else None
            
            price_change = None
            if before_avg and after_avg:
                price_change = ((after_avg - before_avg) / before_avg) * 100
            
            impacts.append({
                "date": str(event_date),
                "title": event.get("event_name") or event.get("title") or event.get("event", ""),
                "description": event.get("description", ""),
                "category": event.get("category", ""),
                "before_avg": round(before_avg, 2) if before_avg else None,
                "after_avg": round(after_avg, 2) if after_avg else None,
                "price_change_percent": round(price_change, 2) if price_change else None
            })
        
        # Sort by absolute price change (most impactful first)
        impacts = sorted(impacts, key=lambda x: abs(x["price_change_percent"] or 0), reverse=True)
        
        return jsonify({
            "impacts": impacts,
            "count": len(impacts)
        })

    except FileNotFoundError:
        return jsonify({"error": "Data files not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
