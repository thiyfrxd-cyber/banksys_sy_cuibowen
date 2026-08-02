"""Tests for app.models.data_loader."""

import os
import tempfile

import pandas as pd
import pytest

from app.models import data_loader


class TestResolvePath:
    def test_resolve_train_csv_exists(self):
        path = data_loader._resolve_path("train.csv")
        assert os.path.isfile(path)
        assert path.endswith(os.path.join("data", "train.csv"))

    def test_resolve_test_csv_exists(self):
        path = data_loader._resolve_path("test.csv")
        assert os.path.isfile(path)
        assert path.endswith(os.path.join("data", "test.csv"))


class TestReadCsv:
    def test_read_valid_csv(self, train_csv):
        df = data_loader._read_csv(train_csv)
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_read_nonexistent_file_raises(self):
        with pytest.raises(FileNotFoundError, match="not found"):
            data_loader._read_csv("/nonexistent/path.csv")

    def test_read_empty_file_raises(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write("")
            tmp = f.name
        try:
            with pytest.raises(pd.errors.EmptyDataError, match="empty"):
                data_loader._read_csv(tmp)
        finally:
            os.unlink(tmp)


class TestLoadTrainData:
    def test_returns_dataframe_with_correct_columns(self):
        df = data_loader.load_train_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        # 22 columns: id + 20 features + subscribe
        assert len(df.columns) == 22
        assert "subscribe" in df.columns

    def test_subscribe_has_yes_no_values(self):
        df = data_loader.load_train_data()
        unique = df["subscribe"].unique().tolist()
        assert "yes" in unique
        assert "no" in unique

    def test_all_expected_columns_present(self):
        df = data_loader.load_train_data()
        for col in data_loader.EXPECTED_COLS:
            assert col in df.columns


class TestLoadTestData:
    def test_returns_dataframe_with_21_columns(self):
        df = data_loader.load_test_data()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        # Test data has 21 columns (no subscribe)
        assert len(df.columns) == 21

    def test_no_subscribe_column(self):
        df = data_loader.load_test_data()
        assert "subscribe" not in df.columns

    def test_all_feature_columns_present(self):
        df = data_loader.load_test_data()
        for col in data_loader.EXPECTED_COLS:
            assert col in df.columns


class TestValidateColumns:
    def test_passes_when_all_columns_present(self):
        df = pd.DataFrame(columns=data_loader.EXPECTED_COLS)
        data_loader._validate_columns(df, "test.csv")

    def test_raises_on_missing_columns(self):
        df = pd.DataFrame(columns=["id", "age"])
        with pytest.raises(ValueError, match="Missing expected columns"):
            data_loader._validate_columns(df, "bad.csv")


class TestGetColumnInfo:
    def test_returns_expected_keys(self):
        info = data_loader.get_column_info()
        assert "categorical" in info
        assert "numerical" in info
        assert "target" in info
        assert "all_features" in info
        assert "total_features" in info

    def test_total_features_matches(self):
        info = data_loader.get_column_info()
        expected = len(info["categorical"]) + len(info["numerical"])
        assert info["total_features"] == expected

    def test_target_is_subscribe(self):
        info = data_loader.get_column_info()
        assert info["target"] == "subscribe"


class TestGetBasicStats:
    def test_returns_row_and_col_count(self):
        df = data_loader.load_train_data()
        stats = data_loader.get_basic_stats(df)
        assert stats["row_count"] == len(df)
        assert stats["col_count"] == 22

    def test_returns_subscribe_stats_for_train_data(self):
        df = data_loader.load_train_data()
        stats = data_loader.get_basic_stats(df)
        assert "subscribe_rate" in stats
        assert "subscribe_yes" in stats
        assert "subscribe_no" in stats
        assert stats["subscribe_yes"] + stats["subscribe_no"] == len(df)
        assert 0 <= stats["subscribe_rate"] <= 100

    def test_no_subscribe_stats_for_test_data(self):
        df = data_loader.load_test_data()
        stats = data_loader.get_basic_stats(df)
        assert "subscribe_rate" not in stats


class TestMissingValueHandling:
    def test_unknown_values_present(self):
        df = data_loader.load_train_data()
        # Data contains 'unknown' and 'nonexistent' as special missing markers
        # Verify they are preserved as-is (not converted to NaN)
        has_unknown = (df == "unknown").any().any()
        has_nonexistent = (df == "nonexistent").any().any()
        assert has_unknown or has_nonexistent

    def test_data_types_are_consistent(self):
        df = data_loader.load_train_data()
        for col in data_loader.CATEGORICAL_COLS:
            dtype_str = str(df[col].dtype)
            assert (
                "str" in dtype_str or "object" in dtype_str
            ), f"{col} should be string/object dtype, got {dtype_str}"
