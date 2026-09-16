"""Unit tests for LinearModel."""

import numpy as np
import pandas as pd
import pytest

from africa_data_intelligence.ml.linear import LinearModel


def _simple_data() -> tuple[pd.DataFrame, pd.Series]:
    X = pd.DataFrame({"x": [1.0, 2.0, 3.0, 4.0, 5.0]})
    y = pd.Series([2.0, 4.0, 6.0, 8.0, 10.0])
    return X, y


def test_fit_then_predict_perfect_line():
    X, y = _simple_data()
    model = LinearModel()
    model.fit(X, y)
    preds = model.predict(X)
    np.testing.assert_allclose(preds, y, atol=1e-6)


def test_predict_before_fit_raises():
    X, _ = _simple_data()
    with pytest.raises(RuntimeError, match="must be fitted"):
        LinearModel().predict(X)


def test_evaluate_returns_metrics():
    X, y = _simple_data()
    model = LinearModel()
    model.fit(X, y)
    metrics = model.evaluate(X, y)
    assert set(metrics.keys()) == {"rmse", "mae", "r2"}
    assert metrics["rmse"] < 1e-6


def test_coefficients_mapped_to_names():
    X, y = _simple_data()
    model = LinearModel()
    model.fit(X, y)
    coefs = model.coefficients(feature_names=["x"])
    assert "x" in coefs
    assert coefs["x"] == pytest.approx(2.0, abs=1e-6)


def test_intercept_value():
    X, y = _simple_data()
    model = LinearModel()
    model.fit(X, y)
    assert model.intercept() == pytest.approx(0.0, abs=1e-6)
