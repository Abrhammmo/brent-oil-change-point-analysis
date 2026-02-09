# src

Core library for the project: reusable data loaders, preprocessing, analysis, and modelling utilities used by the notebooks and dashboard.

Structure

- `src/data/`: data loading and preprocessing (e.g., `load_data.py`, `preprocess.py`).
- `src/analysis/`: analysis helpers used by notebooks (`event_mapping.py`, `impact_quantification.py`, `time_series_properties.py`).
- `src/models/`: modelling code and utilities (`bayesian_change_point.py`, `model_utils.py`).
- `src/visualizations/`: plotting helpers (if present) for consistent figures across notebooks and the dashboard.

Usage

- Import small, testable functions from `src` in notebooks and scripts. Example:

```
from src.data.load_data import load_prices
```

Conventions

- Keep logic here (notebooks should be thin orchestration layers).
- Make functions importable from the project root so notebooks and the dashboard can reuse them.
