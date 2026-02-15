# Dashboard

This folder contains a lightweight dashboard prototype for exploring the Brent oil change-point analysis. It includes a Flask backend that serves data endpoints and a small React frontend that consumes those endpoints to render charts and an event timeline.

## Enhanced Dashboard Features

- Regime visualization for multiple Bayesian change points
- Macro overlay toggles (`GDP`, `Inflation`, `ExchangeRate`) on price chart
- Posterior distribution panel for change-point uncertainty
- Business impact panel:
  - mean % change before/after regime
  - volatility shift
  - regime durations
- SHAP tab:
  - global feature-importance summary
  - local "Why this prediction?" explanation

**Contents**

- `backend/` — Flask app, API routes and small developer scripts
- `frontend/` — React app (create-react-app-style) with chart and UI components

**Quick start (local development)**

1. Create and activate a Python virtual environment (from repo root):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Start the backend API:

```powershell
cd dashboard/backend
pip install -r requirements.txt
python app.py
```

The backend listens on port `5000` by default and exposes the API under `/api`.

3. Start the frontend (separate terminal):

```bash
cd dashboard/frontend
npm install
npm start
```

The React dev server will open a browser at `http://localhost:3000` (or an available port when prompted).

**Primary API endpoints**

- `GET /api/health` — simple health check, returns `{status: 'OK'}`.
- `GET /api/prices` — returns price time series JSON from `data/processed/brentoilprices_processed.csv` (fields: `Date`, `Price`, `log_price`, `log_return` when available).
- `GET /api/events` — returns a list of events (sourced from `data/processed/events.csv`) as `{date, title, description}` objects.
- `GET /api/change-points` — returns detected change-point summary (or a small canned example when model output is not present).
- `GET /api/change-points/details` — per-regime metrics and comparisons.
- `GET /api/change-points/posterior` — posterior sample summary for rendering.
- `GET /api/change-points/business-impact` — compact transition impact metrics.
- `GET /api/change-points/shap` — SHAP global/local images (base64 + path).
- `GET /api/prices/macro-overlay` — merged price + macro series.

**Developer notes**

- The backend resolves data file paths relative to the repository root, so run `app.py` from the `dashboard/backend` folder or from the project root to ensure consistent path resolution.
- Routes include safe fallbacks during local development (small canned JSON) if processed artifacts are missing; remove or tighten those fallbacks before deploying to production.

**Sanity checks & scripts**

- `dashboard/backend/scripts/test_endpoints.py` — quick script using Flask test client to call the endpoints and print responses. Useful for CI or local checks.

**Troubleshooting**

- If the frontend shows an empty page, open DevTools and check the network requests to `/api/*` and the console for runtime errors.
- If endpoints return canned data, ensure `data/processed/brentoilprices_processed.csv` and `data/processed/events.csv` exist and are readable.

**Next steps & suggestions**

- Remove canned fallbacks and add integration tests for API contract once production data is available.
- Add linting and small unit tests for frontend components.

If you want, I can run the backend sanity script and start the frontend dev server for you now and report any errors I see.

Structure

- `dashboard/backend/`: backend server (e.g., Flask/FastAPI) with `app.py` and route modules in `routes/`:
  - `change_points.py`, `events.py`, `prices.py` — these expose the API endpoints the frontend expects.
- `dashboard/frontend/`: React-style frontend with `src/` containing `App.jsx`, `index.js`, UI components (`ChangePointChart.jsx`, `EventTimeline.jsx`, `Filters.jsx`, `pieChart.jsx`), pages (`Dashboard.jsx`), and `services/api.js`.

Running locally

- Backend: install `dashboard/backend/requirements.txt` (if present) and run `python app.py` from `dashboard/backend`.
- Frontend: from `dashboard/frontend` run `npm install` and `npm start` if a `package.json` exists.

Notes

- Keep API route names and JSON shapes consistent between backend `routes/` and frontend `services/api.js`. 
