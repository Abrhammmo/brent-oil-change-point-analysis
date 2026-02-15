from __future__ import annotations

import numpy as np
import pytest

from src.analysis.impact_quantification import quantify_mean_shift

pymc = pytest.importorskip("pymc")
pytest.importorskip("arviz")
from src.models.bayesian_change_point import build_change_point_model


def test_build_change_point_model_supports_multiple_breaks() -> None:
    returns = np.random.normal(0, 0.01, 120)
    model = build_change_point_model(returns, n_change_points=2)
    var_names = set(model.named_vars.keys())
    assert "tau" in var_names
    assert "mu_regimes" in var_names
    assert "sigma_regimes" in var_names


class _Posterior:
    def __init__(self) -> None:
        self._data = {"mu_regimes": type("V", (), {"values": np.array([[[0.1, 0.4]]])})()}

    def __contains__(self, item: str) -> bool:
        return item in self._data

    def __getitem__(self, item: str):
        return self._data[item]


class _Trace:
    posterior = _Posterior()


def test_quantify_mean_shift_with_multi_regime_trace() -> None:
    out = quantify_mean_shift(_Trace())
    assert out["mean_before"] == 0.1
    assert out["mean_after"] == 0.4
