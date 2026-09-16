"""Unit tests for RegressionEvaluator and ClassificationEvaluator."""

import numpy as np
import pandas as pd
import pytest

from africa_data_intelligence.ml.evaluation import (
    ClassificationEvaluator,
    RegressionEvaluator,
)


def test_regression_perfect_predictions():
    y = pd.Series([1.0, 2.0, 3.0])
    metrics = RegressionEvaluator().evaluate(y, y.to_numpy())
    assert metrics["rmse"] == pytest.approx(0.0)
    assert metrics["r2"] == pytest.approx(1.0)


def test_regression_mape_handles_zeros():
    y_true = pd.Series([0.0, 5.0, 10.0])
    y_pred = np.array([1.0, 5.0, 9.0])
    metrics = RegressionEvaluator().evaluate(y_true, y_pred)
    assert "mape" in metrics
    assert metrics["mape"] >= 0.0


def test_regression_to_dataframe():
    y = pd.Series([1.0, 2.0, 3.0])
    df = RegressionEvaluator().to_dataframe(y, y.to_numpy())
    assert set(df.columns) == {"metric", "value"}
    assert "rmse" in df["metric"].tolist()


def test_classification_perfect_predictions():
    y = pd.Series([0, 1, 1, 0])
    metrics = ClassificationEvaluator().evaluate(y, y.to_numpy())
    assert metrics["accuracy"] == 1.0
    assert metrics["f1"] == 1.0


def test_classification_weighted_average():
    y_true = pd.Series([0, 0, 1, 1])
    y_pred = np.array([0, 1, 1, 1])
    metrics = ClassificationEvaluator().evaluate(y_true, y_pred)
    assert 0.0 <= metrics["precision"] <= 1.0
    assert 0.0 <= metrics["recall"] <= 1.0
