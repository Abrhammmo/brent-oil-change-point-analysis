# brent_cp_model_v1

Artifacts and configuration produced by the project's Bayesian change-point model training run.

Contents

- `model_config.json`: configuration and hyperparameters used to fit the model.
- `posterior.nc`: NetCDF file containing posterior samples from the trained model.

Usage

- These files are model outputs; use `src/models/bayesian_change_point.py` and `src/models/model_utils.py` to load, inspect, and analyse the posterior.

Notes

- The directory is intended to store a single model version. Add a short `README.md` here whenever new model versions are produced to record training metadata.
