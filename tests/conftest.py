"""Shared pytest fixtures for the project."""

import os
import sys

import pytest

# Ensure the project root is on sys.path so that "import app" works during tests
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)


@pytest.fixture
def data_dir():
    """Return the path to the data directory."""
    return os.path.join(_project_root, "data")


@pytest.fixture
def train_csv(data_dir):
    """Return the path to the training CSV."""
    return os.path.join(data_dir, "train.csv")


@pytest.fixture
def test_csv(data_dir):
    """Return the path to the test CSV."""
    return os.path.join(data_dir, "test.csv")
