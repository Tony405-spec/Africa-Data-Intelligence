"""Unit tests for DescriptiveStats."""

import pandas as pd
import pytest

from africa_data_intelligence.analytics.descriptive import DescriptiveStats


def test_numeric_columns_detects_numbers():
    df = pd.DataFrame({"a": [1, 2], "b": ["x", "y"], "c": [1.5, 2.5]})
    stats = DescriptiveStats(df)
    assert stats.numeric_columns() == ["a", "c"]


def test_summary_returns_describe_columns():
    df = pd.DataFrame({"a": [1, 2, 3, 4]})
    summary = DescriptiveStats(df).summary()
    for expected in ("count", "mean", "std", "min", "max"):
        assert expected in summary.columns


def test_mean_value():
    df = pd.DataFrame({"a": [1, 2, 3]})
    assert DescriptiveStats(df).mean("a") == 2.0


def test_median_value():
    df = pd.DataFrame({"a": [1, 2, 3, 100]})
    assert DescriptiveStats(df).median("a") == 2.5


def test_std_value():
    df = pd.DataFrame({"a": [1, 1, 1]})
    assert DescriptiveStats(df).std("a") == 0.0


def test_missing_column_raises():
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(KeyError, match="Column not found"):
        DescriptiveStats(df).mean("b")


def test_non_numeric_raises():
    df = pd.DataFrame({"a": ["x", "y"]})
    with pytest.raises(TypeError, match="not numeric"):
        DescriptiveStats(df).mean("a")


def test_empty_numeric_returns_empty():
    df = pd.DataFrame({"a": ["x", "y"]})
    assert DescriptiveStats(df).summary().empty
