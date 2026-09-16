"""Unit tests for AnomalyDetector."""

import pandas as pd
import pytest

from africa_data_intelligence.analytics.anomaly import AnomalyDetector


def test_zscore_flags_extreme_value():
    df = pd.DataFrame({"a": [1, 1, 1, 1, 1, 100]})
    mask = AnomalyDetector(df).zscore("a", threshold=2.0)
    assert bool(mask.iloc[-1]) is True


def test_zscore_handles_zero_std():
    df = pd.DataFrame({"a": [5, 5, 5, 5]})
    mask = AnomalyDetector(df).zscore("a")
    assert mask.sum() == 0


def test_iqr_flags_outliers():
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5, 1000]})
    mask = AnomalyDetector(df).iqr("a")
    assert bool(mask.iloc[-1]) is True


def test_count_zscore():
    df = pd.DataFrame({"a": [1, 1, 1, 1, 100]})
    assert AnomalyDetector(df).count("a", method="zscore") >= 1


def test_count_iqr():
    df = pd.DataFrame({"a": [1, 2, 3, 4, 1000]})
    assert AnomalyDetector(df).count("a", method="iqr") >= 1


def test_count_unsupported_method_raises():
    df = pd.DataFrame({"a": [1, 2, 3]})
    with pytest.raises(ValueError, match="Unsupported method"):
        AnomalyDetector(df).count("a", method="magic")


def test_missing_column_raises():
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(KeyError):
        AnomalyDetector(df).zscore("b")


def test_non_numeric_raises():
    df = pd.DataFrame({"a": ["x", "y"]})
    with pytest.raises(TypeError):
        AnomalyDetector(df).iqr("a")

