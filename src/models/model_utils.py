import pymc as pm
from pathlib import Path
import arviz as az
import json

def run_mcmc(model, draws=2000, tune=1000):
    try:
        with model:
            trace = pm.sample(
                draws=draws,
                tune=tune,
                return_inferencedata=True,
                target_accept=0.9
            )
        print("✅ MCMC sampling completed.")
        return trace

    except Exception as e:
        print(f"❌ MCMC sampling failed: {e}")
        raise
def save_bayesian_model(trace, model_config, model_name):
    model_dir = Path(f"src/models/saved_models/{model_name}")
    model_dir.mkdir(parents=True, exist_ok=True)

    az.to_netcdf(trace, model_dir / "posterior.nc")

    with open(model_dir / "model_config.json", "w") as f:
        json.dump(model_config, f, indent=4)

    az.summary(trace).to_csv(model_dir / "summary.csv")

    return model_dir