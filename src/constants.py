"""Project-wide constants for modeling and API defaults."""

DEFAULT_DRAWS: int = 2000
DEFAULT_TUNE: int = 1000
DEFAULT_TARGET_ACCEPT: float = 0.9
DEFAULT_CHAINS: int = 4
DEFAULT_N_CHANGE_POINTS: int = 2
DEFAULT_VOLATILITY_WINDOW: int = 30

MODEL_V1_CONFIG_PATH: str = "models/brent_cp_model_v1/model_config.json"
MODEL_V2_POSTERIOR_PATH: str = "models/brent_cp_model_v2/posterior.nc"
CHANGE_POINT_RESULTS_PATH: str = "reports/change_point_results.json"
VAR_RESULTS_PATH: str = "reports/var_results.json"
SHAP_GLOBAL_PNG: str = "reports/shap_global.png"
SHAP_LOCAL_PNG: str = "reports/shap_local.png"
