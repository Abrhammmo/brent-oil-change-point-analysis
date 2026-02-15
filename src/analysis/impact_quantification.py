from __future__ import annotations

from typing import Any, Dict

import numpy as np


def quantify_mean_shift(trace: Any) -> Dict[str, float | None]:
    """Quantify pre/post mean shift from posterior trace."""
    if "mu_regimes" in trace.posterior:
        mu_vals = trace.posterior["mu_regimes"].values
        mu_before = float(mu_vals[..., 0].mean())
        mu_after = float(mu_vals[..., -1].mean())
    else:
        mu_before = float(trace.posterior["mu_1"].values.flatten().mean())
        mu_after = float(trace.posterior["mu_2"].values.flatten().mean())

    shift = mu_after - mu_before
    pct_change = (shift / abs(mu_before) * 100.0) if mu_before != 0 else None
    return {
        "mean_before": mu_before,
        "mean_after": mu_after,
        "absolute_change": float(shift),
        "percent_change": float(pct_change) if pct_change is not None else None,
    }


def volatility_shift(before: np.ndarray, after: np.ndarray) -> float:
    """Compute volatility delta between two regimes."""
    return float(np.nanstd(after) - np.nanstd(before))
