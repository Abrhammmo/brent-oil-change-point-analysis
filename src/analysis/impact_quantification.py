import numpy as np

def quantify_mean_shift(trace):
    try:
        mu_1 = trace.posterior["mu_1"].values.flatten()
        mu_2 = trace.posterior["mu_2"].values.flatten()

        shift = mu_2.mean() - mu_1.mean()
        pct_change = (shift / abs(mu_1.mean())) * 100 if mu_1.mean() != 0 else None

        return {
            "mean_before": mu_1.mean(),
            "mean_after": mu_2.mean(),
            "absolute_change": shift,
            "percent_change": pct_change
        }

    except Exception as e:
        print(f"❌ Impact quantification failed: {e}")
        raise
