from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

pytest.importorskip("statsmodels")
from src.models.var_model import run_var_pipeline


def test_var_pipeline_returns_summary(tmp_path) -> None:
    n = 120
    df = pd.DataFrame(
        {
            "log_return": np.random.normal(0, 0.02, n),
            "GDP": np.linspace(100, 105, n),
            "Inflation": 2 + np.sin(np.linspace(0, 2, n)),
            "ExchangeRate": 1.1 + 0.01 * np.cos(np.linspace(0, 5, n)),
        }
    )
    output = tmp_path / "var_results.json"
    summary = run_var_pipeline(df, output_path=str(output))
    assert output.exists()
    assert summary["selected_lag"] >= 1
    assert "aic" in summary
