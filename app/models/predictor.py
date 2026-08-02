"""Prediction service — load trained model and return subscribe predictions.

Provides a predict() function that accepts a feature dictionary and returns
a prediction result with probability and confidence level.
"""

import os
import pickle
from functools import lru_cache

import pandas as pd

from app.models.data_loader import CATEGORICAL_COLS, NUMERICAL_COLS

# ── Model path ──
_MODEL_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ml", "model"
)
_MODEL_PATH = os.path.join(_MODEL_DIR, "model.pkl")

# ── Confidence thresholds ──
HIGH_CONFIDENCE = 0.8
MEDIUM_CONFIDENCE = 0.5


@lru_cache(maxsize=1)
def load_model():
    """Load the trained model pipeline (cached).

    Returns:
        sklearn Pipeline: the trained model.

    Raises:
        FileNotFoundError: if model.pkl does not exist.
    """
    if not os.path.isfile(_MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {_MODEL_PATH}. " "Please run: python -m app.ml.train --overwrite"
        )
    with open(_MODEL_PATH, "rb") as f:
        return pickle.load(f)


def predict(features: dict) -> dict:
    """Predict subscribe probability for a single customer.

    Args:
        features: dict with keys matching CATEGORICAL_COLS + NUMERICAL_COLS.
            Missing keys will use default values.

    Returns:
        Dict with:
            subscribe (bool): whether customer is predicted to subscribe.
            probability (float): subscription probability (0-1).
            confidence (str): 'high', 'medium', or 'low'.
    """
    model = load_model()

    # Build default feature row (with validation)
    row = {}
    for col in CATEGORICAL_COLS:
        row[col] = str(features.get(col, "unknown"))
    for col in NUMERICAL_COLS:
        val = features.get(col, 0.0)
        try:
            row[col] = float(val)
        except (ValueError, TypeError):
            row[col] = 0.0

    df = pd.DataFrame([row])[CATEGORICAL_COLS + NUMERICAL_COLS]
    proba = float(model.predict_proba(df)[0, 1])
    subscribe = bool(proba >= 0.5)

    if proba >= HIGH_CONFIDENCE:
        confidence = "high"
    elif proba >= MEDIUM_CONFIDENCE:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "subscribe": subscribe,
        "probability": round(proba, 4),
        "confidence": confidence,
    }


def get_feature_schema() -> dict:
    """Return feature schema for building UI forms.

    Returns:
        Dict mapping feature name → {type, options (for categorical)}.
    """
    # Load training data to get unique categorical values
    from app.models.data_loader import load_train_data

    df = load_train_data()
    schema = {}
    for col in CATEGORICAL_COLS:
        unique_vals = sorted(df[col].dropna().unique().tolist())
        schema[col] = {"type": "categorical", "options": unique_vals}
    for col in NUMERICAL_COLS:
        col_min = float(df[col].min())
        col_max = float(df[col].max())
        col_mean = float(df[col].mean())
        schema[col] = {
            "type": "numerical",
            "min": col_min,
            "max": col_max,
            "default": round(col_mean, 2),
        }
    return schema
