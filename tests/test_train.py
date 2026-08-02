"""Tests for app.ml.train — model training pipeline."""

import os
import sys

import pytest
from sklearn.pipeline import Pipeline

# Ensure import path
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from app.ml import train


class TestBuildPipeline:
    def test_returns_pipeline(self):
        pipeline = train.build_pipeline()
        assert isinstance(pipeline, Pipeline)

    def test_pipeline_has_two_steps(self):
        pipeline = train.build_pipeline()
        assert len(pipeline.steps) == 2

    def test_step_names(self):
        pipeline = train.build_pipeline()
        names = [s[0] for s in pipeline.steps]
        assert names == ["preprocessor", "classifier"]


class TestTrainAndEvaluate:
    def test_returns_expected_keys(self):
        result = train.train_and_evaluate()
        assert "auc" in result
        assert "accuracy" in result
        assert "report" in result
        assert "pipeline" in result

    def test_auc_is_reasonable(self):
        result = train.train_and_evaluate()
        assert result["auc"] >= 0.75, f"AUC {result['auc']} too low"

    def test_accuracy_is_reasonable(self):
        result = train.train_and_evaluate()
        assert result["accuracy"] >= 0.75

    def test_pipeline_is_fitted(self):
        result = train.train_and_evaluate()
        from sklearn.utils.validation import check_is_fitted

        check_is_fitted(result["pipeline"])


class TestSaveModel:
    def test_saves_file(self, tmp_path):
        # Monkey-patch MODEL_DIR to use tmp_path
        original_dir = train.MODEL_DIR
        train.MODEL_DIR = str(tmp_path)
        train.MODEL_PATH = os.path.join(train.MODEL_DIR, "model.pkl")
        try:
            result = train.train_and_evaluate()
            path = train.save_model(result["pipeline"])
            assert os.path.isfile(path)
            assert os.path.getsize(path) > 0
        finally:
            train.MODEL_DIR = original_dir
            train.MODEL_PATH = os.path.join(original_dir, "model.pkl")

    def test_creates_directory(self, tmp_path):
        original_dir = train.MODEL_DIR
        model_subdir = os.path.join(str(tmp_path), "sub", "model")
        train.MODEL_DIR = model_subdir
        train.MODEL_PATH = os.path.join(model_subdir, "model.pkl")
        try:
            result = train.train_and_evaluate()
            train.save_model(result["pipeline"])
            assert os.path.isdir(model_subdir)
        finally:
            train.MODEL_DIR = original_dir
            train.MODEL_PATH = os.path.join(original_dir, "model.pkl")


class TestReproducibility:
    def test_same_seed_produces_same_auc(self):
        """Training twice with the same random_state should yield the same AUC."""
        result1 = train.train_and_evaluate()
        result2 = train.train_and_evaluate()
        assert result1["auc"] == pytest.approx(result2["auc"])
        assert result1["accuracy"] == pytest.approx(result2["accuracy"])


class TestConstants:
    def test_random_state_is_fixed(self):
        assert train.RANDOM_STATE == 42

    def test_model_path_in_model_dir(self):
        assert train.MODEL_PATH.startswith(train.MODEL_DIR)
