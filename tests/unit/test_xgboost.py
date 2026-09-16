"""Unit tests for XGBoostModel."""

import pandas as pd
import pytest

from africa_data_intelligence.ml.xgboost_model import XGBoostModel


def _data() -> tuple[pd.DataFrame, pd.Series]:
    X = pd.DataFrame({"x": list(range(40))})
    y = pd.Series([v * 3 + 2 for v in range(40)])
    return X, y


def test_fit_predict_shape():
    X, y = _data()
    model = XGBoostModel(n_estimators=20)
    model.fit(X, y)
    preds = model.predict(X)
    assert preds.shape == (40,)


def test_predict_before_fit_raises():
    X, _ = _data()
    with pytest.raises(RuntimeError, match="must be fitted"):
        XGBoostModel(n_estimators=10).predict(X)


def test_evaluate_returns_metrics():
    X, y = _data()
    model = XGBoostModel(n_estimators=20)
    model.fit(X, y)
    metrics = model.evaluate(X, y)
    assert set(metrics.keys()) == {"rmse", "mae", "r2"}
    assert metrics["r2"] > 0.9


def test_feature_importance_mapped_to_names():
    X, y = _data()
    model = XGBoostModel(n_estimators=20)
    model.fit(X, y)
    importance = model.feature_importance()
    assert "x" in importance


def test_feature_importance_before_fit_raises():
    with pytest.raises(RuntimeError, match="must be fitted"):
        XGBoostModel(n_estimators=10).feature_importance()

