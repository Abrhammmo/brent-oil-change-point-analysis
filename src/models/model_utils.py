from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm

from src.constants import CHANGE_POINT_RESULTS_PATH


def run_mcmc(
    model: pm.Model,
    draws: int,
    tune: int,
    chains: int = 4,
    target_accept: float = 0.9,
) -> az.InferenceData:
    """Run PyMC sampling and return an ArviZ inference object."""
    with model:
        trace = pm.sample(
            draws=draws,
            tune=tune,
            chains=chains,
            target_accept=target_accept,
            return_inferencedata=True,
            progressbar=False,
        )
    return trace


def save_inference_data(trace: az.InferenceData, posterior_path: str) -> Path:
    """Persist posterior netcdf to disk."""
    output = Path(posterior_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    az.to_netcdf(trace, output)
    return output


def write_json(payload: Dict[str, Any], path: str = CHANGE_POINT_RESULTS_PATH) -> Path:
    """Write JSON report to disk."""
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    return output


def summarize_change_points(
    dates: pd.Series,
    tau_samples: np.ndarray,
    mu_samples: np.ndarray,
    sigma_samples: np.ndarray,
) -> Dict[str, Any]:
    """Build structured JSON output for multi-change-point analysis."""
    date_values = pd.to_datetime(dates).reset_index(drop=True)
    tau_medians = np.median(tau_samples, axis=0).astype(int).tolist()
    tau_sorted = sorted(
        max(0, min(len(date_values) - 1, int(tau_val))) for tau_val in tau_medians
    )

    change_points: List[Dict[str, Any]] = []
    for cp_idx, tau_idx in enumerate(tau_sorted, start=1):
        change_points.append(
            {
                "name": f"cp_{cp_idx}",
                "tau_index": tau_idx,
                "tau_date": date_values.iloc[tau_idx].strftime("%Y-%m-%d"),
            }
        )

    mu_mean = np.mean(mu_samples, axis=0)
    sigma_mean = np.mean(sigma_samples, axis=0)

    regimes: List[Dict[str, Any]] = []
    boundaries = [0] + tau_sorted + [len(date_values) - 1]
    for regime_idx in range(len(boundaries) - 1):
        start_idx = boundaries[regime_idx]
        end_idx = boundaries[regime_idx + 1]
        regimes.append(
            {
                "name": f"regime_{regime_idx + 1}",
                "start_date": date_values.iloc[start_idx].strftime("%Y-%m-%d"),
                "end_date": date_values.iloc[end_idx].strftime("%Y-%m-%d"),
                "duration": int(max(1, end_idx - start_idx + 1)),
                "mu": float(mu_mean[regime_idx]),
                "sigma": float(sigma_mean[regime_idx]),
            }
        )

    business_impact: List[Dict[str, Any]] = []
    for idx in range(len(regimes) - 1):
        before = regimes[idx]
        after = regimes[idx + 1]
        mean_shift = after["mu"] - before["mu"]
        pct = (mean_shift / abs(before["mu"]) * 100.0) if before["mu"] != 0 else None
        volatility_shift = after["sigma"] - before["sigma"]
        business_impact.append(
            {
                "transition": f"{before['name']} -> {after['name']}",
                "mean_shift": mean_shift,
                "mean_shift_percent": pct,
                "volatility_shift": volatility_shift,
                "duration_before": before["duration"],
                "duration_after": after["duration"],
            }
        )

    return {
        "n_change_points": len(change_points),
        "change_points": change_points,
        "regimes": regimes,
        "business_impact": business_impact,
    }
