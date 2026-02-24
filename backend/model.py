"""Model loading and prediction utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import joblib
import numpy as np
import pandas as pd
import scipy.io as sio

from backend.schema import FEATURE_NAMES_MODEL, INPUT_FACTOR

BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR_CANDIDATES = [
    BASE_DIR,
]

_MODEL: Optional[object] = None
_ARR_MIN: Optional[np.ndarray] = None
_ARR_MAX: Optional[np.ndarray] = None


def _resolve_asset_path(filename: str) -> Path:
    for directory in MODEL_DIR_CANDIDATES:
        candidate = directory / filename
        if candidate.exists():
            return candidate

    searched = ", ".join(str(path / filename) for path in MODEL_DIR_CANDIDATES)
    raise FileNotFoundError(f"Missing file '{filename}'. Searched: {searched}")


def _load_assets() -> None:
    global _MODEL, _ARR_MIN, _ARR_MAX
    if _MODEL is not None and _ARR_MIN is not None and _ARR_MAX is not None:
        return

    norm_file = _resolve_asset_path("aa_norm.mat")
    model_file = _resolve_asset_path("final_model.pkl")

    mat = sio.loadmat(str(norm_file))
    _ARR_MIN = np.squeeze(mat["arr_min"]).astype(np.float64)
    _ARR_MAX = np.squeeze(mat["arr_max"]).astype(np.float64)
    _MODEL = joblib.load(str(model_file))


def _scale_input(raw_values: np.ndarray) -> np.ndarray:
    _load_assets()
    assert _ARR_MIN is not None
    assert _ARR_MAX is not None

    vector = np.asarray(raw_values, dtype=np.float64).reshape(1, INPUT_FACTOR).copy()

    # Use training minimum for missing values, matching existing service behavior.
    for idx in range(INPUT_FACTOR):
        if np.isnan(vector[0, idx]):
            vector[0, idx] = _ARR_MIN[idx]

    denom = _ARR_MAX - _ARR_MIN
    denom = np.where(denom == 0.0, 1.0, denom)
    scaled = (vector - _ARR_MIN) / denom
    return np.nan_to_num(scaled, nan=0.0, posinf=0.0, neginf=0.0)


def predict_probability(raw_values: np.ndarray) -> float:
    _load_assets()
    assert _MODEL is not None

    scaled = _scale_input(raw_values)
    frame = pd.DataFrame(scaled, columns=FEATURE_NAMES_MODEL)
    prob = _MODEL.predict_proba(frame)
    return float(prob[0, 1])
