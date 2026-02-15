from __future__ import annotations

from typing import Any, Dict, Optional

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm
import pytensor.tensor as pt

from src.config import ModelConfig, load_model_config
from src.constants import CHANGE_POINT_RESULTS_PATH, MODEL_V2_POSTERIOR_PATH
from src.models.model_utils import (
    run_mcmc,
    save_inference_data,
    summarize_change_points,
    write_json,
)


def build_change_point_model(log_returns: np.ndarray, n_change_points: int = 1) -> pm.Model:
    """Build a Bayesian change-point model with configurable structural breaks."""
    if n_change_points < 1:
        raise ValueError("n_change_points must be >= 1")

    clean_returns = np.asarray(log_returns, dtype=float)
    clean_returns = clean_returns[~np.isnan(clean_returns)]
    t_size = len(clean_returns)
    if t_size <= (n_change_points + 1):
        raise ValueError("Insufficient data points for selected number of change points.")

    with pm.Model() as model:
        tau_raw = pm.DiscreteUniform(
            "tau_raw",
            lower=1,
            upper=t_size - 2,
            shape=n_change_points,
        )
        tau = pm.Deterministic("tau", pt.sort(tau_raw))

        mu_regimes = pm.Normal("mu_regimes", mu=0.0, sigma=1.0, shape=n_change_points + 1)
        sigma_regimes = pm.HalfNormal("sigma_regimes", sigma=1.0, shape=n_change_points + 1)

        t_index = pt.arange(t_size).dimshuffle(0, "x")
        regime_idx = pt.sum(pt.gt(t_index, tau), axis=1)
        mu_t = mu_regimes[regime_idx]
        sigma_t = sigma_regimes[regime_idx]

        pm.Normal("obs", mu=mu_t, sigma=sigma_t, observed=clean_returns)

    return model


def run_change_point_pipeline(
    df: pd.DataFrame,
    config: Optional[ModelConfig] = None,
    posterior_path: str = MODEL_V2_POSTERIOR_PATH,
    results_path: str = CHANGE_POINT_RESULTS_PATH,
) -> Dict[str, Any]:
    """Train model, persist posterior, and write structured results JSON."""
    cfg = config or load_model_config()
    model = build_change_point_model(df["log_return"].dropna().to_numpy(), cfg.n_change_points)
    trace = run_mcmc(
        model,
        draws=cfg.draws,
        tune=cfg.tune,
        chains=cfg.chains,
        target_accept=cfg.target_accept,
    )
    save_inference_data(trace, posterior_path)

    tau_samples = trace.posterior["tau"].values.reshape(-1, cfg.n_change_points)
    mu_samples = trace.posterior["mu_regimes"].values.reshape(-1, cfg.n_change_points + 1)
    sigma_samples = trace.posterior["sigma_regimes"].values.reshape(-1, cfg.n_change_points + 1)

    summary = summarize_change_points(
        dates=df["Date"].reset_index(drop=True),
        tau_samples=tau_samples,
        mu_samples=mu_samples,
        sigma_samples=sigma_samples,
    )
    write_json(summary, results_path)
    return summary


def load_posterior(path: str = MODEL_V2_POSTERIOR_PATH) -> az.InferenceData:
    """Load persisted posterior netcdf."""
    return az.from_netcdf(path)
