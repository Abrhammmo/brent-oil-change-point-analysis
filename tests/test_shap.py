from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("shap")
pytest.importorskip("sklearn")

from src.models.explainability import run_shap_analysis


def test_shap_artifact_generation(tmp_path) -> None:
    n = 120
    df = pd.DataFrame(
        {
            "Date": pd.date_range("2020-01-01", periods=n),
            "GDP": np.linspace(100, 105, n),
            "Inflation": 2 + np.sin(np.linspace(0, 2, n)),
            "ExchangeRate": 1.1 + 0.01 * np.cos(np.linspace(0, 5, n)),
            "log_return": np.random.normal(0, 0.01, n),
        }
    )
    global_out = tmp_path / "shap_global.png"
    local_out = tmp_path / "shap_local.png"
    run_shap_analysis(
        df,
        global_path=str(global_out),
        local_path=str(local_out),
        selected_date="2020-02-10",
    )
    assert global_out.exists()
    assert local_out.exists()
