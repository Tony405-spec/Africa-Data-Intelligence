"""Unit tests for LogisticModel."""

import pandas as pd
import pytest

from africa_data_intelligence.ml.logistic import LogisticModel


def _binary_data() -> tuple[pd.DataFrame, pd.Series]:
    X = pd.DataFrame({"x": [-2, -1, 0, 1, 2, 3, 4, 5]})
    y = pd.Series([0, 0, 0, 0, 1, 1, 1, 1])
    return X, y


def test_fit_and_predict_labels():
    X, y = _binary_data()
    model = LogisticModel()
    model.fit(X, y)
    preds = model.predict(X)
    assert set(preds).issubset({0, 1})


def test_predict_before_fit_raises():
    X, _ = _binary_data()
    with pytest.raises(RuntimeError, match="must be fitted"):
        LogisticModel().predict(X)


def test_predict_proba_before_fit_raises():
    X, _ = _binary_data()
    with pytest.raises(RuntimeError, match="must be fitted"):
        LogisticModel().predict_proba(X)


def test_evaluate_returns_metrics():
    X, y = _binary_data()
    model = LogisticModel()
    model.fit(X, y)
    metrics = model.evaluate(X, y)
    assert set(metrics.keys()) == {"accuracy", "precision", "recall", "f1"}
    assert metrics["accuracy"] >= 0.9


def test_predict_proba_shape():
    X, y = _binary_data()
    model = LogisticModel()
    model.fit(X, y)
    proba = model.predict_proba(X)
    assert proba.shape == (len(X), 2)
    assert all(abs(proba.sum(axis=1) - 1.0) < 1e-6)


def test_coefficients_mapped_to_names():
    X, y = _binary_data()
    model = LogisticModel()
    model.fit(X, y)
    coefs = model.coefficients(feature_names=["x"])
    assert "x" in coefs
