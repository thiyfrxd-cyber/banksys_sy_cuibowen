"""Offline model training script for bank marketing subscribe prediction.

Usage:
    python -m app.ml.train                # Train and save model
    python -m app.ml.train --overwrite    # Overwrite existing model
    python -m app.ml.train --check-auc 0.75  # Fail if AUC below threshold
"""

import argparse
import os
import pickle
import sys

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

# Ensure project root is on sys.path for import
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from app.models.data_loader import CATEGORICAL_COLS, NUMERICAL_COLS, TARGET_COL, load_train_data

# ── Constants ──
RANDOM_STATE = 42
MODEL_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")


def build_pipeline() -> Pipeline:
    """Build the training pipeline.

    Returns:
        sklearn Pipeline: ColumnTransformer → RandomForestClassifier.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL_COLS),
        ],
        remainder="passthrough",  # Numerical columns pass through unchanged
    )

    clf = RandomForestClassifier(
        n_estimators=200,
        max_depth=15,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    return Pipeline(steps=[("preprocessor", preprocessor), ("classifier", clf)])


def train_and_evaluate() -> dict:
    """Train the model and return evaluation metrics.

    Returns:
        Dict with keys: auc, accuracy, report, model.
    """
    df = load_train_data()
    X = df[CATEGORICAL_COLS + NUMERICAL_COLS]
    y = (df[TARGET_COL] == "yes").astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    auc = float(roc_auc_score(y_test, y_proba))
    acc = float(accuracy_score(y_test, y_pred))
    report = classification_report(y_test, y_pred, target_names=["no", "yes"])

    return {
        "auc": auc,
        "accuracy": acc,
        "report": report,
        "pipeline": pipeline,
    }


def save_model(pipeline: Pipeline) -> str:
    """Save trained pipeline to disk.

    Returns:
        Path to the saved model file.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)
    return MODEL_PATH


def main() -> None:
    """CLI entry point for training."""
    parser = argparse.ArgumentParser(description="Train bank marketing prediction model")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing model file")
    parser.add_argument(
        "--check-auc",
        type=float,
        default=None,
        help="Fail if AUC is below this threshold (e.g. 0.75)",
    )
    args = parser.parse_args()

    # Check existing model
    if os.path.exists(MODEL_PATH) and not args.overwrite:
        print(f"Model already exists at {MODEL_PATH}")
        print("Use --overwrite to replace it.")
        return

    # Train
    print("Training model...")
    result = train_and_evaluate()

    # Print metrics
    print(f"\nAUC: {result['auc']:.4f}")
    print(f"Accuracy: {result['accuracy']:.4f}")
    print(f"\nClassification Report:\n{result['report']}")

    # AUC check
    if args.check_auc is not None:
        if result["auc"] < args.check_auc:
            print(f"FAIL: AUC {result['auc']:.4f} < threshold {args.check_auc}")
            sys.exit(1)
        print(f"PASS: AUC {result['auc']:.4f} >= threshold {args.check_auc}")

    # Save
    path = save_model(result["pipeline"])
    print(f"Model saved to {path}")


if __name__ == "__main__":
    main()
