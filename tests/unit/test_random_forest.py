"""Unit tests for RandomForestModel."""

import numpy as np
import pandas as pd
import pytest

from africa_data_intelligence.ml.random_forest import RandomForestModel


def _data() -> tuple[pd.DataFrame, pd.Series]:
    X = pd.DataFrame({"x": list(range(50))})
    y = pd.Series([v * 2 + 1 for v in range(50)])
    return X, y


def test_fit_predict_shape():
    X, y = _data()
    model = RandomForestModel(n_estimators=10)
    model.fit(X, y)
    preds = model.predict(X)
    assert preds.shape == (50,)


def test_predict_before_fit_raises():
    X, _ = _data()
    with pytest.raises(RuntimeError, match="must be fitted"):
        RandomForestModel(n_estimators=5).predict(X)


def test_evaluate_returns_metrics():
    X, y = _data()
    model = RandomForestModel(n_estimators=10)
    model.fit(X, y)
    metrics = model.evaluate(X, y)
    assert set(metrics.keys()) == {"rmse", "mae", "r2"}
    assert metrics["r2"] > 0.8


def test_feature_importance_mapped_to_names():
    X, y = _data()
    model = RandomForestModel(n_estimators=10)
    model.fit(X, y)
    importance = model.feature_importance()
    assert "x" in importance
    assert 0.0 <= importance["x"] <= 1.0


def test_feature_importance_before_fit_raises():
    with pytest.raises(RuntimeError, match="must be fitted"):
        RandomForestModel(n_estimators=5).feature_importance()
