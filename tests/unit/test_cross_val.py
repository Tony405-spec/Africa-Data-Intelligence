"""Unit tests for CrossValidator."""

import numpy as np
import pandas as pd
import pytest

from africa_data_intelligence.ml.cross_val import CrossValidator
from africa_data_intelligence.ml.linear import LinearModel


def _data() -> tuple[pd.DataFrame, pd.Series]:
    X = pd.DataFrame({"x": list(range(50))})
    y = pd.Series([v * 2 + 1 for v in range(50)])
    return X, y


def _mse(y_true, y_pred) -> float:
    return float(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2))


def test_run_returns_expected_keys():
    X, y = _data()
    results = CrossValidator(n_splits=3).run(X, y, LinearModel, _mse)
    assert set(results.keys()) == {"fold_scores", "mean", "std", "min", "max"}


def test_run_produces_correct_fold_count():
    X, y = _data()
    results = CrossValidator(n_splits=4).run(X, y, LinearModel, _mse)
    assert len(results["fold_scores"]) == 4


def test_run_rejects_invalid_n_splits():
    with pytest.raises(ValueError, match="n_splits"):
        CrossValidator(n_splits=1)


def test_run_mean_is_close_to_fold_average():
    X, y = _data()
    results = CrossValidator(n_splits=3).run(X, y, LinearModel, _mse)
    assert abs(results["mean"] - np.mean(results["fold_scores"])) < 1e-9


def test_run_linear_model_performs_well():
    X, y = _data()
    results = CrossValidator(n_splits=3).run(X, y, LinearModel, _mse)
    assert results["mean"] < 1.0
