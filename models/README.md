# models

This folder contains trained model artifacts and model-related metadata used by analyses and the dashboard.

Current contents

- `brent_cp_model_v1/` — first change-point model release. Contains `model_config.json`, `posterior.nc`, and a README describing the model.
- `brent_cp_model_v2/` — subsequent model release(s); contains `posterior.nc` and related assets.

Quick notes

- Model posteriors are stored in NetCDF (`posterior.nc`) and can be loaded with `arviz` or `xarray`:

```python
import arviz as az
idata = az.from_netcdf("models/brent_cp_model_v1/posterior.nc")
print(idata)
```

- `model_config.json` holds configuration and provenance (hyperparameters, training date, data version). Use it to document model assumptions.

Adding a new model release

1. Create a new directory `models/<name>` (e.g., `brent_cp_model_v3`).
2. Add `posterior.nc` and `model_config.json` with clear metadata (data source, preprocessing steps, training date, software versions).
3. Optionally include a short `README.md` in the model folder describing training notes and usage.

Reproducibility

- Store minimal metadata required to reproduce the model (dataset version, seed, package versions). Large raw model artifacts may be stored in DVC if needed.

If you want, I can add a small loader utility in `src/models/` to standardize loading and validating model artifacts.
