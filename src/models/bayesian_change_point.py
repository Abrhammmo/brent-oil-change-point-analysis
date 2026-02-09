import pymc as pm
import numpy as np

def build_change_point_model(log_returns: np.ndarray):
    """
    Bayesian single change point model on log returns.
    """
    try:
        T = len(log_returns)

        with pm.Model() as model:
            tau = pm.DiscreteUniform("tau", lower=0, upper=T - 1)

            mu_1 = pm.Normal("mu_1", mu=0, sigma=1)
            mu_2 = pm.Normal("mu_2", mu=0, sigma=1)

            sigma = pm.HalfNormal("sigma", sigma=1)

            mu = pm.math.switch(
                np.arange(T) <= tau,
                mu_1,
                mu_2
            )

            pm.Normal("obs", mu=mu, sigma=sigma, observed=log_returns)

        print("✅ Bayesian change point model built successfully.")
        return model

    except Exception as e:
        print(f"❌ Model construction failed: {e}")
        raise
