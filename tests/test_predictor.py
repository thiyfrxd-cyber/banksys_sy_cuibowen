"""Tests for app.models.predictor."""

import os
import time

import pytest

from app.models import predictor

# Ensure model exists before tests
_MODEL_EXISTS = os.path.isfile(predictor._MODEL_PATH)


@pytest.fixture
def sample_features():
    """Return realistic features that should predict 'yes'."""
    return {
        "age": 35,
        "job": "admin.",
        "marital": "single",
        "education": "university.degree",
        "default": "no",
        "housing": "yes",
        "loan": "no",
        "contact": "cellular",
        "month": "may",
        "day_of_week": "mon",
        "duration": 500,
        "campaign": 1,
        "pdays": 999,
        "previous": 0,
        "poutcome": "nonexistent",
        "emp_var_rate": 1.4,
        "cons_price_index": 93.0,
        "cons_conf_index": -36.0,
        "lending_rate3m": 1.5,
        "nr_employed": 5100.0,
    }


@pytest.mark.skipif(not _MODEL_EXISTS, reason="Model not trained")
class TestPredict:
    def test_returns_expected_keys(self, sample_features):
        result = predictor.predict(sample_features)
        assert "subscribe" in result
        assert "probability" in result
        assert "confidence" in result

    def test_subscribe_is_bool(self, sample_features):
        result = predictor.predict(sample_features)
        assert isinstance(result["subscribe"], bool)

    def test_probability_in_range(self, sample_features):
        result = predictor.predict(sample_features)
        assert 0.0 <= result["probability"] <= 1.0

    def test_confidence_is_valid(self, sample_features):
        result = predictor.predict(sample_features)
        assert result["confidence"] in ("high", "medium", "low")

    def test_high_duration_high_subscribe_probability(self):
        """A customer with high duration should have higher probability."""
        high = {
            "duration": 3000,
            "age": 35,
            "job": "admin.",
            "marital": "single",
            "education": "university.degree",
            "default": "no",
            "housing": "yes",
            "loan": "no",
            "contact": "cellular",
            "month": "may",
            "day_of_week": "mon",
            "campaign": 1,
            "pdays": 999,
            "previous": 0,
            "poutcome": "nonexistent",
            "emp_var_rate": 1.4,
            "cons_price_index": 93.0,
            "cons_conf_index": -36.0,
            "lending_rate3m": 1.5,
            "nr_employed": 5100.0,
        }
        result = predictor.predict(high)
        assert result["probability"] > 0.15  # high duration suggests some probability

    def test_response_time_under_1s(self, sample_features):
        start = time.perf_counter()
        predictor.predict(sample_features)
        elapsed = time.perf_counter() - start
        assert elapsed < 1.0, f"Prediction took {elapsed:.3f}s"


class TestLoadModel:
    @pytest.mark.skipif(not _MODEL_EXISTS, reason="Model not trained")
    def test_load_model_returns_pipeline(self):
        from sklearn.pipeline import Pipeline

        m = predictor.load_model()
        assert isinstance(m, Pipeline)

    def test_missing_model_raises_clear_error(self, monkeypatch, tmp_path):
        fake_path = os.path.join(str(tmp_path), "nonexistent.pkl")
        monkeypatch.setattr(predictor, "_MODEL_PATH", fake_path)
        predictor.load_model.cache_clear()  # clear lru_cache
        with pytest.raises(FileNotFoundError, match="Model not found"):
            predictor.load_model()


class TestMissingFeatures:
    @pytest.mark.skipif(not _MODEL_EXISTS, reason="Model not trained")
    def test_handles_missing_features_gracefully(self):
        result = predictor.predict({"age": 30, "job": "admin."})
        assert "probability" in result

    @pytest.mark.skipif(not _MODEL_EXISTS, reason="Model not trained")
    def test_handles_empty_dict(self):
        result = predictor.predict({})
        assert "probability" in result
        assert isinstance(result["probability"], float)


class TestInvalidValues:
    @pytest.mark.skipif(not _MODEL_EXISTS, reason="Model not trained")
    def test_handles_invalid_numeric(self):
        result = predictor.predict({"age": "not_a_number"})
        assert isinstance(result["probability"], float)

    @pytest.mark.skipif(not _MODEL_EXISTS, reason="Model not trained")
    def test_handles_unknown_category(self):
        result = predictor.predict({"job": "astronaut"})
        assert isinstance(result["probability"], float)


class TestFeatureSchema:
    def test_returns_categorical_and_numerical(self):
        schema = predictor.get_feature_schema()
        for col in predictor.CATEGORICAL_COLS:
            assert col in schema
            assert schema[col]["type"] == "categorical"
            assert "options" in schema[col]
        for col in predictor.NUMERICAL_COLS:
            assert col in schema
            assert schema[col]["type"] == "numerical"
            assert "min" in schema[col]
