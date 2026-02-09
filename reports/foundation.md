## **foundation.md**

### Foundation of the Change Point Analysis

This study investigates structural breaks in Brent crude oil prices using a Bayesian Change Point Detection framework. Oil prices are known to be highly sensitive to geopolitical events, supply–demand imbalances, macroeconomic shocks, and policy interventions. These forces often introduce abrupt regime shifts rather than smooth transitions, making traditional stationary time-series models insufficient for capturing underlying dynamics.

To address this, a Bayesian change point model is employed to probabilistically identify shifts in the statistical properties of oil price movements. Instead of assuming a fixed structure over time, the model allows the data to determine whether and when a regime change occurs, while explicitly accounting for uncertainty in both the timing and magnitude of the change.

#### Data Preparation and Transformation

Daily Brent crude oil prices were used as the primary dataset. The Date column was converted to a datetime format to ensure proper temporal alignment and analysis. Initial exploratory data analysis revealed long-term trends, sharp price shocks, and periods of heightened volatility.

Given the non-stationary nature of price levels, the analysis was conducted on log returns, defined as:

[
\log(P_t) - \log(P_{t-1})
]

This transformation stabilizes variance and centers the series around zero, making it more suitable for probabilistic modeling and regime comparison.

#### Model Assumptions

The Bayesian change point model assumes:

* A single dominant structural break exists in the log return process.
* Log returns before and after the change point follow Normal distributions with different means but shared volatility.
* The timing of the change point is unknown and treated as a random variable.

The change point ((\tau)) is modeled with a discrete uniform prior over the full time index, reflecting minimal prior assumptions about when the regime shift occurred. Regime-specific means ((\mu_1, \mu_2)) and a global volatility parameter ((\sigma)) are inferred using Markov Chain Monte Carlo (MCMC) sampling.

This foundation enables a transparent, uncertainty-aware framework for linking observed oil price behavior to real-world economic and geopolitical events.

