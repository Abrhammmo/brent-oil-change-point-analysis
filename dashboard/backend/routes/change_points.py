from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from flask import Blueprint, jsonify, request

from src.constants import CHANGE_POINT_RESULTS_PATH, SHAP_GLOBAL_PNG, SHAP_LOCAL_PNG
from src.data.macro_loader import load_macro_data
from src.models.explainability import run_shap_analysis

change_points_bp = Blueprint("change_points", __name__)

BASE_DIR = Path(__file__).resolve().parents[3]
RESULTS_PATH = BASE_DIR / CHANGE_POINT_RESULTS_PATH
PRICES_PATH = BASE_DIR / "data" / "processed" / "brentoilprices_processed.csv"
SHAP_GLOBAL_PATH = BASE_DIR / SHAP_GLOBAL_PNG
SHAP_LOCAL_PATH = BASE_DIR / SHAP_LOCAL_PNG


def _load_change_point_results() -> Dict[str, Any]:
    if RESULTS_PATH.exists():
        with RESULTS_PATH.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    return {
        "n_change_points": 1,
        "change_points": [{"name": "cp_1", "tau_date": "2012-06-04", "tau_index": 1500}],
        "regimes": [],
        "business_impact": [],
    }


@change_points_bp.route("/", methods=["GET"])
def get_change_points() -> Any:
    return jsonify(_load_change_point_results())


@change_points_bp.route("/details", methods=["GET"])
def get_change_point_details() -> Any:
    try:
        results = _load_change_point_results()
        prices = pd.read_csv(PRICES_PATH)
        prices["Date"] = pd.to_datetime(prices["Date"], errors="coerce")

        regimes: List[Dict[str, Any]] = []
        for cp in results.get("change_points", []):
            tau_date = pd.to_datetime(cp["tau_date"])
            before = prices[prices["Date"] < tau_date]
            after = prices[prices["Date"] >= tau_date]
            if before.empty or after.empty:
                continue
            regimes.append(
                {
                    "change_point": cp,
                    "before_mean": float(before["Price"].mean()),
                    "after_mean": float(after["Price"].mean()),
                    "before_volatility": float(before["Price"].std()),
                    "after_volatility": float(after["Price"].std()),
                    "mean_shift_percent": float(
                        ((after["Price"].mean() - before["Price"].mean()) / before["Price"].mean())
                        * 100.0
                    ),
                    "duration_before": int(len(before)),
                    "duration_after": int(len(after)),
                }
            )
        return jsonify({"regime_analysis": regimes, "business_impact": results.get("business_impact", [])})
    except FileNotFoundError:
        return jsonify({"error": "Required files not found"}), 404
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": str(exc)}), 500


@change_points_bp.route("/posterior", methods=["GET"])
def get_posterior_samples() -> Any:
    """Provide synthetic posterior samples shaped for dashboard rendering."""
    results = _load_change_point_results()
    cps = results.get("change_points", [])
    posterior: Dict[str, Dict[str, Any]] = {}
    for idx, cp in enumerate(cps, start=1):
        center = cp.get("tau_index", 1)
        samples = np.random.normal(center, 5.0, 300).clip(min=0).tolist()
        posterior[f"tau_{idx}"] = {
            "samples": samples,
            "posterior_mean": float(np.mean(samples)),
            "hdi_lower": float(np.percentile(samples, 3)),
            "hdi_upper": float(np.percentile(samples, 97)),
            "tau_date": cp.get("tau_date"),
        }
    return jsonify(posterior)


@change_points_bp.route("/business-impact", methods=["GET"])
def get_business_impact() -> Any:
    results = _load_change_point_results()
    return jsonify({"business_impact": results.get("business_impact", [])})


def _png_to_base64(path: Path) -> str | None:
    if not path.exists():
        return None
    return base64.b64encode(path.read_bytes()).decode("utf-8")


@change_points_bp.route("/shap", methods=["GET"])
def get_shap_assets() -> Any:
    selected_date = request.args.get("selected_date")
    try:
        prices = pd.read_csv(PRICES_PATH)
        prices["Date"] = pd.to_datetime(prices["Date"], errors="coerce")
        merged = load_macro_data(prices)
        run_shap_analysis(
            merged,
            global_path=str(SHAP_GLOBAL_PATH),
            local_path=str(SHAP_LOCAL_PATH),
            selected_date=selected_date,
        )
    except Exception:
        # Keep serving existing artifacts if dynamic generation fails.
        pass

    return jsonify(
        {
            "global_plot_b64": _png_to_base64(SHAP_GLOBAL_PATH),
            "local_plot_b64": _png_to_base64(SHAP_LOCAL_PATH),
            "global_plot_path": str(SHAP_GLOBAL_PATH),
            "local_plot_path": str(SHAP_LOCAL_PATH),
        }
    )
