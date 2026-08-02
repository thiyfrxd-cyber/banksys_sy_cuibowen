"""Sanity / health tests for the project structure."""


class TestProjectStructure:
    """Verify that the project skeleton is in place and all modules are importable."""

    def test_app_package_importable(self):
        """app package should be importable."""
        import app  # noqa: F401

    def test_app_models_importable(self):
        """app.models package should be importable."""
        from app import models  # noqa: F401

    def test_app_ml_importable(self):
        """app.ml package should be importable."""
        from app import ml  # noqa: F401

    def test_app_utils_importable(self):
        """app.utils package should be importable."""
        from app import utils  # noqa: F401

    def test_app_pages_importable(self):
        """app.pages package should be importable."""
        from app import pages  # noqa: F401

    def test_data_files_exist(self, train_csv, test_csv):
        """Both data files should exist."""
        import os

        assert os.path.isfile(train_csv), f"train.csv not found at {train_csv}"
        assert os.path.isfile(test_csv), f"test.csv not found at {test_csv}"


class TestPythonVersion:
    """Verify the runtime Python version."""

    def test_python_version_is_at_least_3_11(self):
        """Project targets Python 3.11+."""
        import sys

        assert sys.version_info >= (
            3,
            11,
        ), f"Expected Python >= 3.11, got {sys.version_info.major}.{sys.version_info.minor}"


class TestDependencies:
    """Verify key dependencies are installed."""

    def test_streamlit_installed(self):
        """streamlit should be installed."""
        import streamlit  # noqa: F401

    def test_pandas_installed(self):
        """pandas should be installed."""
        import pandas  # noqa: F401

    def test_sklearn_installed(self):
        """scikit-learn should be installed."""
        import sklearn  # noqa: F401
