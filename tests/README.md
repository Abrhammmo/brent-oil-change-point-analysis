# tests

This folder contains unit tests for the project. Tests are runnable from the repository root and designed to be executed with `pytest`.

Contents

- `test_load_data.py` — tests for data loading utilities in `src/data/load_data.py`.
- Other test modules exercise preprocessing, modeling, and utility functions.

Setup

1. Create and activate a virtual environment from the project root:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

2. Install project dependencies:

```powershell
pip install -r requirements.txt
```

Running tests

- Run the entire test suite from the project root:

```powershell
pytest
```

- Run tests in the `tests/` folder only:

```powershell
pytest tests
```

- Run a single test file:

```powershell
pytest tests/test_load_data.py
```

Tips

- Use `-q` for quieter output or `-k <expr>` to filter tests by keyword.
- If tests depend on sample data in `data/raw/` or `data/processed/`, ensure those files exist or mock filesystem access in tests.
- To run tests with coverage (if `coverage` is installed):

```powershell
coverage run -m pytest && coverage report -m
```

Contributing

- Add new tests under `tests/` and keep them importable from the project root (avoid relative imports inside tests).
- When adding dependencies needed only for testing (e.g., `pytest-mock`, `coverage`), consider placing them in a separate `requirements-dev.txt`.

If you want, I can split runtime vs dev dependencies and add a `requirements-dev.txt` including test tooling.
