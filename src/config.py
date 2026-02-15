"""Configuration loading and typed config objects."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Dict

from src.constants import (
    DEFAULT_DRAWS,
    DEFAULT_N_CHANGE_POINTS,
    DEFAULT_TUNE,
    MODEL_V1_CONFIG_PATH,
)


@dataclass(frozen=True)
class ModelConfig:
    n_change_points: int = DEFAULT_N_CHANGE_POINTS
    draws: int = DEFAULT_DRAWS
    tune: int = DEFAULT_TUNE
    chains: int = 4
    target_accept: float = 0.9


def _to_int(data: Dict[str, Any], key: str, default: int) -> int:
    value = data.get(key, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _to_float(data: Dict[str, Any], key: str, default: float) -> float:
    value = data.get(key, default)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def load_model_config(path: str = MODEL_V1_CONFIG_PATH) -> ModelConfig:
    """Load model config from JSON with safe fallbacks."""
    config_path = Path(path)
    if not config_path.exists():
        return ModelConfig()

    with config_path.open("r", encoding="utf-8") as handle:
        raw: Dict[str, Any] = json.load(handle)

    return ModelConfig(
        n_change_points=_to_int(raw, "n_change_points", DEFAULT_N_CHANGE_POINTS),
        draws=_to_int(raw, "draws", DEFAULT_DRAWS),
        tune=_to_int(raw, "tune", DEFAULT_TUNE),
        chains=_to_int(raw, "chains", 4),
        target_accept=_to_float(raw, "target_accept", 0.9),
    )
