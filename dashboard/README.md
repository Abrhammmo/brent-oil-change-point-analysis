# dashboard

Frontend + backend prototype for visualizing detected change points, prices, and events.

Structure

- `dashboard/backend/`: backend server (e.g., Flask/FastAPI) with `app.py` and route modules in `routes/`:
  - `change_points.py`, `events.py`, `prices.py` — these expose the API endpoints the frontend expects.
- `dashboard/frontend/`: React-style frontend with `src/` containing `App.jsx`, `index.js`, UI components (`ChangePointChart.jsx`, `EventTimeline.jsx`, `Filters.jsx`, `pieChart.jsx`), pages (`Dashboard.jsx`), and `services/api.js`.

Running locally

- Backend: install `dashboard/backend/requirements.txt` (if present) and run `python app.py` from `dashboard/backend`.
- Frontend: from `dashboard/frontend` run `npm install` and `npm start` if a `package.json` exists.

Notes

- Keep API route names and JSON shapes consistent between backend `routes/` and frontend `services/api.js`.
