from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.constants import SHAP_GLOBAL_PNG, SHAP_LOCAL_PNG

try:
    import shap  # type: ignore
except ImportError:  # pragma: no cover
    shap = None  # type: ignore

try:
    from sklearn.ensemble import RandomForestRegressor
except ImportError:  # pragma: no cover
    RandomForestRegressor = None  # type: ignore


def _ensure_output(path: str) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    return out


def run_shap_analysis(
    df: pd.DataFrame,
    global_path: str = SHAP_GLOBAL_PNG,
    local_path: str = SHAP_LOCAL_PNG,
    selected_date: Optional[str] = None,
) -> Dict[str, str]:
    """
    Compute SHAP explanations over macro features.
    Falls back to model feature importances when SHAP is unavailable.
    """
    data = df[["Date", "GDP", "Inflation", "ExchangeRate", "log_return"]].dropna().copy()
    x = data[["GDP", "Inflation", "ExchangeRate"]]
    y = data["log_return"]

    if RandomForestRegressor is not None:
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(x, y)
    else:
        model = None

    global_out = _ensure_output(global_path)
    local_out = _ensure_output(local_path)

    if shap is not None and model is not None:
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(x)

        # Global plot
        mean_abs = np.mean(np.abs(shap_values), axis=0)
        plt.figure(figsize=(8, 4))
        plt.bar(x.columns, mean_abs)
        plt.title("Global SHAP Feature Importance")
        plt.tight_layout()
        plt.savefig(global_out, dpi=140)
        plt.close()

        # Local plot
        if selected_date is not None:
            target_date = pd.to_datetime(selected_date, errors="coerce")
            row_idx = data.index[data["Date"] == target_date]
            idx = int(row_idx[0]) if len(row_idx) > 0 else int(len(data) - 1)
        else:
            idx = int(len(data) - 1)
        local_vals = shap_values[idx]
        plt.figure(figsize=(8, 4))
        colors = ["#2E8B57" if val >= 0 else "#B22222" for val in local_vals]
        plt.bar(x.columns, local_vals, color=colors)
        plt.title("Local SHAP Explanation")
        plt.tight_layout()
        plt.savefig(local_out, dpi=140)
        plt.close()
    else:
        # Degraded mode: still provide explainability artifacts for dashboard/CI.
        if model is not None and hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
        else:
            # Pure-numpy fallback importance: absolute correlation to target.
            corr = np.nan_to_num(np.corrcoef(np.column_stack([x.values.T, y.values]))[-1, :-1])
            importances = np.abs(corr)
        plt.figure(figsize=(8, 4))
        plt.bar(x.columns, importances)
        plt.title("Global Feature Importance (Fallback)")
        plt.tight_layout()
        plt.savefig(global_out, dpi=140)
        plt.close()

        sample = x.iloc[-1]
        centered = sample - x.mean()
        signed = centered.values * importances
        plt.figure(figsize=(8, 4))
        colors = ["#2E8B57" if val >= 0 else "#B22222" for val in signed]
        plt.bar(x.columns, signed, color=colors)
        plt.title("Local Explanation (Fallback)")
        plt.tight_layout()
        plt.savefig(local_out, dpi=140)
        plt.close()

    return {"global_plot": str(global_out), "local_plot": str(local_out)}
