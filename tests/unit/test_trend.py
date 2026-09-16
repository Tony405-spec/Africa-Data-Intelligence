"""Unit tests for TrendAnalyzer."""

import pandas as pd
import pytest

from africa_data_intelligence.analytics.trend import TrendAnalyzer


def test_positive_slope():
    df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [1, 2, 3, 4]})
    assert TrendAnalyzer(df).slope("x", "y") == pytest.approx(1.0)


def test_direction_increasing():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
    assert TrendAnalyzer(df).direction("x", "y") == "increasing"


def test_direction_decreasing():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [3, 2, 1]})
    assert TrendAnalyzer(df).direction("x", "y") == "decreasing"


def test_direction_flat():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [5, 5, 5]})
    assert TrendAnalyzer(df).direction("x", "y") == "flat"


def test_growth_rate():
    df = pd.DataFrame({"a": [100, 150, 200]})
    assert TrendAnalyzer(df).growth_rate("a") == pytest.approx(100.0)


def test_growth_rate_zero_start():
    df = pd.DataFrame({"a": [0, 10, 20]})
    assert TrendAnalyzer(df).growth_rate("a") == 0.0


def test_rolling_mean_short_series():
    df = pd.DataFrame({"a": [1, 2, 3]})
    result = TrendAnalyzer(df).rolling_mean("a", window=7)
    assert len(result) == 3


def test_rolling_mean_invalid_window():
    df = pd.DataFrame({"a": [1, 2, 3]})
    with pytest.raises(ValueError, match="window must be"):
        TrendAnalyzer(df).rolling_mean("a", window=0)


def test_missing_column_raises():
    df = pd.DataFrame({"a": [1, 2]})
    with pytest.raises(KeyError):
        TrendAnalyzer(df).slope("a", "b")

