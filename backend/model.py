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
MODEL_DIR = BASE_DIR / "web_AA" / "model"
NORM_FILE = MODEL_DIR / "aa_norm.mat"
MODEL_FILE = MODEL_DIR / "final_model.pkl"

_MODEL: Optional[object] = None
_ARR_MIN: Optional[np.ndarray] = None
_ARR_MAX: Optional[np.ndarray] = None


def _load_assets() -> None:
    global _MODEL, _ARR_MIN, _ARR_MAX
    if _MODEL is not None and _ARR_MIN is not None and _ARR_MAX is not None:
        return

    if not NORM_FILE.exists():
        raise FileNotFoundError(f"Missing normalization file: {NORM_FILE}")
    if not MODEL_FILE.exists():
        raise FileNotFoundError(f"Missing model file: {MODEL_FILE}")

    mat = sio.loadmat(str(NORM_FILE))
    _ARR_MIN = np.squeeze(mat["arr_min"]).astype(np.float64)
    _ARR_MAX = np.squeeze(mat["arr_max"]).astype(np.float64)
    _MODEL = joblib.load(str(MODEL_FILE))


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

