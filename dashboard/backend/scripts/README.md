# Scripts

This folder contains lightweight developer scripts used to sanity-check the dashboard backend API during local development and CI.

Files

- `test_endpoints.py` — exercises the Flask app using the test client and prints the JSON responses for the primary endpoints (`/api/health`, `/api/prices`, `/api/events`, `/api/change-points`).

How to run

From the repository root (recommended) with the project virtual environment active:

```powershell
python dashboard/backend/scripts/test_endpoints.py
```

What the script checks (sanity expectations)

- Health endpoint responds with a JSON object containing `status: 'OK'`.
- Prices endpoint returns a JSON object with a `data` array of records and at minimum `Date` and a numeric `Price` or `log_price` fields.
- Events endpoint returns an array of objects containing `date`, `title`, and `description`.
- Change-points endpoint returns an object with at least `tau_date` (ISO date string) and `tau_index` (integer index into the price series), or a small canned example when model outputs are not present.

Tested breakpoints (recommended baseline)

The project focuses on major structural breaks in the Brent price series. The following historical events are used as candidate/expected breakpoints for validation and interpretation (the script does not automatically assert them by default):

- 1990-08: Iraqi invasion of Kuwait / Gulf War supply shock
- 1997-07: Asian financial crisis (regional demand shock)
- 2008-09: Global Financial Crisis (large price shock and volatility)
- 2014-07: Oil price collapse (supply + demand dynamics)
- 2020-03: COVID-19 market shock and demand collapse
- 2022-02: Russia–Ukraine conflict and related market disruptions

Validating detected change points

Currently `test_endpoints.py` confirms the presence and shape of the change-point response (i.e., the endpoint returns `tau_date` and `tau_index`). To validate the model output against expected breakpoints, extend the test script to compare `tau_date` against the list above with a tolerance window (for example ±60 days). Example snippet to add to the script:

```python
from datetime import datetime, timedelta

expected = [
    '1990-08-01', '1997-07-01', '2008-09-15', '2014-07-01', '2020-03-01', '2022-02-24'
]
tol_days = 60
# assume `response` is the JSON returned from /api/change-points
tau = datetime.fromisoformat(response['tau_date'])
matches = [d for d in expected if abs((tau - datetime.fromisoformat(d)).days) <= tol_days]
if matches:
    print('Detected change point is close to expected event(s):', matches)
else:
    print('No close match found; consider inspecting the returned time index and series.')
```

How to extend tests

- Add assertions to `test_endpoints.py` to fail CI when endpoint shapes change unexpectedly.
- Add a `tests/` integration test (pytest) that starts the Flask app and asserts both shape and domain-level expectations (e.g., `tau_date` inside data range, `tau_index` within array length, and proximity to expected events).

Troubleshooting

- If the change-point endpoint returns the canned example, confirm the model artifact (e.g., `models/brent_cp_model_v1/posterior.nc` or a JSON summary) exists and the `change_points.py` route is pointed to it.
- If date parsing fails, inspect CSV `Date` formats in `data/processed/brentoilprices_processed.csv` and ensure they parse to ISO strings in the `/api/prices` response.

If you want, I can extend `test_endpoints.py` to include the breakpoint-matching snippet above and add a small pytest-compatible integration test that asserts the change-point falls within a tolerance of expected events.
