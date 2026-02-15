from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd

try:
    from statsmodels.tsa.api import VAR
except ImportError:  # pragma: no cover
    VAR = None  # type: ignore

from src.constants import VAR_RESULTS_PATH


def fit_var_model(df: pd.DataFrame, maxlags: int = 3) -> Any:
    """Fit a VAR model over oil and macroeconomic variables."""
    data = df[["log_return", "GDP", "Inflation", "ExchangeRate"]].dropna().copy()
    if data.empty:
        raise ValueError("No data available for VAR fit.")
    if VAR is None:
        # Fallback: pseudo-VAR summary based on lag-1 correlations.
        lagged = data.shift(1).dropna()
        aligned = data.iloc[1:]
        corr = aligned.corrwith(lagged["log_return"]).fillna(0.0)
        return {
            "fallback": True,
            "k_ar": 1,
            "aic": float(np.nan),
            "bic": float(np.nan),
            "hqic": float(np.nan),
            "params": {"lag1_log_return": corr.to_dict()},
        }
    model = VAR(data)
    return model.fit(maxlags=maxlags, ic="aic")


def summarize_var_results(result: Any) -> Dict[str, Any]:
    """Build serializable summary from VAR results."""
    if isinstance(result, dict) and result.get("fallback"):
        return {
            "selected_lag": int(result["k_ar"]),
            "aic": None,
            "bic": None,
            "hqic": None,
            "params": {
                "log_return": {
                    key: float(value) for key, value in result["params"]["lag1_log_return"].items()
                }
            },
            "mode": "fallback-no-statsmodels",
        }
    return {
        "selected_lag": int(result.k_ar),
        "aic": float(result.aic),
        "bic": float(result.bic),
        "hqic": float(result.hqic),
        "params": {
            key: {k: float(v) for k, v in row.items()}
            for key, row in result.params.to_dict(orient="index").items()
        },
    }


def run_var_pipeline(df: pd.DataFrame, output_path: str = VAR_RESULTS_PATH) -> Dict[str, Any]:
    """Fit VAR and save JSON report in reports/."""
    result = fit_var_model(df)
    summary = summarize_var_results(result)
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)
    return summary
