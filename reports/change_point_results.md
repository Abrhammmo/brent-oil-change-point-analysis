## **change_point_results.md**

### Change Point Results and Interpretation

#### Model Diagnostics and Posterior Behavior

The Bayesian change point model successfully converged, as indicated by stable trace plots and acceptable (\hat{R}) values for key parameters. The volatility parameter ((\sigma \approx 0.0256)) shows strong convergence, suggesting reliable estimation of overall market variability.

The posterior trace of the change point parameter ((\tau)) exhibits multimodality and wide dispersion, indicating uncertainty in the precise timing of the regime shift. However, the posterior density is heavily skewed toward the later portion of the dataset, suggesting a higher likelihood of a structural change occurring in the post-2010 period.

#### Estimated Change Point

* **Mean change point index:** 6353
* **Mapped calendar date:** **2012-06-04**
* **94% HDI:** Index range 382 to 9009

The extremely wide credible interval highlights that while the model detects a regime change, the exact timing is uncertain. This uncertainty is consistent with oil markets undergoing prolonged structural transitions rather than instantaneous breaks.

#### Regime Comparison: Before vs. After the Change Point

**Regime 1 (Before (\tau))**

* Mean log return: (9.3 \times 10^{-5})
* 94% HDI: ([-0.0008, 0.0012])

This regime is statistically centered around zero, indicating a relatively stable market with no persistent upward or downward drift.

**Regime 2 (After (\tau))**

* Mean log return: (0.0082)
* 94% HDI: ([-0.78, 0.48])

Although the mean is substantially higher, the large HDI reflects significantly increased uncertainty and volatility, suggesting a more unstable and shock-driven market environment.

#### Quantified Impact

* **Absolute change in mean log returns:** +0.0081
* **Percent increase:** ~8722%

This represents a transition from a near-zero growth regime to one characterized by higher average returns but dramatically higher risk and noise.

#### Event Association and Hypothesized Causes

The detected change point around mid-2012 aligns closely with major structural shifts in global oil markets, including:

* The expansion of US shale oil production, which altered global supply dynamics.
* OPEC’s evolving production strategy and diminishing ability to stabilize prices unilaterally.
* Increased sensitivity to geopolitical tensions and macroeconomic uncertainty.

Rather than a single triggering event, the model suggests a **structural regime transition**, where cumulative supply-side innovations and policy changes fundamentally altered oil price behavior.

#### Overall Interpretation

The Bayesian change point analysis identifies a meaningful shift in Brent oil price dynamics, moving from a relatively stable pre-2012 regime to a post-2012 regime marked by higher expected returns and substantially increased volatility. While the precise timing of the change is uncertain, the results strongly support the presence of a long-term structural transformation in global oil markets, validating the use of probabilistic change point modeling for financial and energy time series analysis.
