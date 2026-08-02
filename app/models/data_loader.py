"""Data loading and preprocessing module for bank marketing dataset.

Provides functions to load training and test CSV files, validate data integrity,
and expose column metadata for use by analysis and prediction modules.
"""

import os

import pandas as pd

# ── Column metadata ──

CATEGORICAL_COLS = [
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "poutcome",
]

NUMERICAL_COLS = [
    "age",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
]

TARGET_COL = "subscribe"

EXPECTED_COLS = [
    "id",
    "age",
    "job",
    "marital",
    "education",
    "default",
    "housing",
    "loan",
    "contact",
    "month",
    "day_of_week",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "poutcome",
    "emp_var_rate",
    "cons_price_index",
    "cons_conf_index",
    "lending_rate3m",
    "nr_employed",
]


def _resolve_path(filename: str) -> str:
    """Resolve data file path relative to the project root."""
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base, "data", filename)


def _read_csv(filepath: str) -> pd.DataFrame:
    """Read a CSV file with standard settings.

    Raises:
        FileNotFoundError: if the file does not exist.
        pd.errors.EmptyDataError: if the file is empty.
    """
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")
    if os.path.getsize(filepath) == 0:
        raise pd.errors.EmptyDataError(f"Data file is empty: {filepath}")
    return pd.read_csv(filepath)


def _validate_columns(df: pd.DataFrame, filename: str) -> None:
    """Validate that required columns are present."""
    actual_cols = df.columns.tolist()
    missing = [c for c in EXPECTED_COLS if c not in actual_cols]
    if missing:
        raise ValueError(f"Missing expected columns in {filename}: {missing}")


def load_train_data() -> pd.DataFrame:
    """Load the training dataset (train.csv).

    Returns:
        DataFrame with 22 columns including 'subscribe' target.

    Raises:
        FileNotFoundError: if train.csv does not exist.
        pd.errors.EmptyDataError: if train.csv is empty.
        ValueError: if expected columns are missing.
    """
    path = _resolve_path("train.csv")
    df = _read_csv(path)

    # Validate that 'subscribe' column exists (training data must have it)
    if TARGET_COL not in df.columns:
        raise ValueError(f"Training data missing target column: {TARGET_COL}")

    _validate_columns(df, "train.csv")
    return df


def load_test_data() -> pd.DataFrame:
    """Load the test dataset (test.csv).

    Test data does not contain the 'subscribe' target column.

    Returns:
        DataFrame with 21 feature columns (no target).

    Raises:
        FileNotFoundError: if test.csv does not exist.
        pd.errors.EmptyDataError: if test.csv is empty.
        ValueError: if expected columns are missing.
    """
    path = _resolve_path("test.csv")
    df = _read_csv(path)

    # Test data does NOT have subscribe column
    _validate_columns(df, "test.csv")
    return df


def get_column_info() -> dict:
    """Return column metadata for UI display.

    Returns:
        Dict with keys 'categorical', 'numerical', 'target', 'all_features'.
    """
    return {
        "categorical": CATEGORICAL_COLS,
        "numerical": NUMERICAL_COLS,
        "target": TARGET_COL,
        "all_features": CATEGORICAL_COLS + NUMERICAL_COLS,
        "total_features": len(CATEGORICAL_COLS) + len(NUMERICAL_COLS),
    }


def get_basic_stats(df: pd.DataFrame) -> dict:
    """Compute basic statistics for a data overview.

    Args:
        df: DataFrame from load_train_data() or load_test_data().

    Returns:
        Dict with 'row_count', 'col_count', and optionally 'subscribe_rate'.
    """
    stats = {
        "row_count": len(df),
        "col_count": len(df.columns),
    }
    if TARGET_COL in df.columns:
        total = len(df)
        yes_count = int((df[TARGET_COL] == "yes").sum())
        stats["subscribe_yes"] = yes_count
        stats["subscribe_no"] = total - yes_count
        stats["subscribe_rate"] = round(yes_count / total * 100, 2) if total > 0 else 0.0
    return stats
