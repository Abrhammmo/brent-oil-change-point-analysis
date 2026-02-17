# src

Core library for the project: reusable data loaders, preprocessing, analysis, and modelling utilities used by the notebooks and dashboard.

Structure

- `src/data/` — data loading and preprocessing (`load_data.py`, `preprocess.py`).
- `src/analysis/` — analysis helpers (`event_mapping.py`, `impact_quantification.py`, `time_series_properties.py`).
- `src/models/` — modelling code (`bayesian_change_point.py`, `model_utils.py`, `var_model.py`).
- `src/visualizations/` — plotting helpers for notebooks and the dashboard.

Quick usage

1. Ensure the project root is on `PYTHONPATH` (run scripts from the repo root).
2. Import small, testable functions. Example:

```python
from src.data.load_data import load_prices
prices = load_prices("data/raw/brentoilprices.csv")
```

Testing & Contribution

- Keep reusable logic in `src/` and add unit tests under `tests/`.
- Follow existing function naming and keep functions small for easier testing.
- If you add external dependencies required by `src/`, update the top-level `requirements.txt`.

Notes

- Notebooks in `notebooks/` should remain thin: orchestrate functions from `src/` and avoid duplicating core logic.
- The dashboard backend imports handlers from `src/`; maintain stable public function names if the frontend depends on them.
