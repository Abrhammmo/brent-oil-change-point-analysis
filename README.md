# Brent Oil Regime Intelligence Platform

Short description: This project detects structural breaks in Brent crude oil prices using Bayesian change-point modeling, enriches analysis with macroeconomic context (GDP, inflation, FX), and delivers insights through a Flask API + React dashboard with explainability views.

[![ci2](https://github.com/Abrhammmo/brent-oil-change-point-analysis/actions/workflows/ci2.yml/badge.svg)](https://github.com/Abrhammmo/brent-oil-change-point-analysis/actions/workflows/ci2.yml)

## Business Problem
Energy markets are highly sensitive to geopolitical shocks, monetary policy, and macroeconomic cycles.  
Teams in trading, risk, and policy often need to answer:
- When did the market regime actually change?
- How did volatility and expected returns shift before vs after that break?
- Which external events best explain observed price behavior?

Manual analysis is slow and inconsistent. This project provides a repeatable, data-driven workflow for regime detection and business interpretation.

## Solution Overview
- Build a **multi-change-point Bayesian model** for Brent log returns.
- Merge oil prices with macro variables (GDP, inflation, exchange rate).
- Estimate multivariate dynamics via VAR (with safe fallback mode if runtime deps are missing).
- Expose results via Flask REST APIs.
- Visualize regimes, event context, macro overlays, and SHAP explainability in React.

## Key Results
- Metric 1: **2 statistically identified structural regime breaks** captured in `reports/change_point_results.json`.
- Metric 2: **7 passing automated tests** (`7 passed, 2 skipped`) for data, models, and API reliability.
- Metric 3: **Operational analysis time reduced from manual review to interactive seconds** via dashboard-based event mapping and regime panels.

## Quick Start
```bash
git clone https://github.com/Abrhammmo/brent-oil-change-point-analysis.git
cd project
pip install -r requirements.txt

# Run backend API
cd dashboard/backend
python app.py

# In another terminal: run frontend dashboard
cd dashboard/frontend
npm install
npm start
```

## Project Structure
```text
brent-oil-change-point-analysis/
├─ .github/workflows/ci.yml
├─ data/
│  ├─ raw/
│  └─ processed/
├─ dashboard/
│  ├─ backend/
│  │  ├─ app.py
│  │  ├─ cache.py
│  │  └─ routes/
│  │     ├─ prices.py
│  │     ├─ change_points.py
│  │     └─ events.py
│  └─ frontend/
│     └─ src/
│        ├─ pages/Dashboard.jsx
│        └─ components/
├─ models/
│  ├─ brent_cp_model_v1/model_config.json
│  └─ brent_cp_model_v2/posterior.nc
├─ reports/
│  ├─ change_point_results.json
│  ├─ var_results.json
│  ├─ shap_global.png
│  └─ shap_local.png
├─ src/
│  ├─ config.py
│  ├─ constants.py
│  ├─ data/
│  │  ├─ load_data.py
│  │  └─ macro_loader.py
│  ├─ analysis/
│  └─ models/
│     ├─ bayesian_change_point.py
│     ├─ var_model.py
│     └─ explainability.py
├─ tests/
│  ├─ test_preprocess.py
│  ├─ test_change_point_model.py
│  ├─ test_var_model.py
│  ├─ test_event_mapping.py
│  └─ test_api_routes.py
|
├─ .gitignore
├─ Requirements.txt
└─ README.md

```

## Demo
- Dashboard: `http://localhost:3000`
- API health check: `http://localhost:5000/api/health`
- Optional: add a GIF in `dashboard_imgs/` and link it here.

## Technical Details
- Data: Historical Brent prices + curated event data under `data/processed/`, with date parsing, sorting, and log-return preprocessing.
- Model: PyMC multi-change-point model with configurable `n_change_points`, `draws`, `tune`, `chains`, `target_accept` from `models/brent_cp_model_v1/model_config.json`.
- Evaluation:
  - Structured regime output in `reports/change_point_results.json`
  - VAR runtime mode is explicit in `reports/var_results.json` as `full-statsmodels` or `fallback-no-statsmodels`
  - SHAP runtime status endpoint: `GET /api/change-points/shap/status`
  - Business-impact deltas (mean shift, volatility shift, regime duration)
  - Automated validation via pytest and CI pipeline

## Future Improvements
- Replace fallback VAR/SHAP execution paths with fully pinned production environments.
- Add model backtesting and probabilistic forecasting metrics by regime.
- Add role-based dashboard views (trading, policy, executive summary).
- Add data version lineage panel (DVC metadata surfaced in dashboard).
- Add benchmark comparisons against non-Bayesian change-point methods.

## Author
Abrham Molla , [ LinkedIn ](https://www.linkedin.com/in/abrham-molla-6867511b6/), +251 985434865
