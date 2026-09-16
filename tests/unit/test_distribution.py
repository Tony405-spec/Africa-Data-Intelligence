"""Unit tests for DistributionAnalyzer."""

import pandas as pd
import pytest

from africa_data_intelligence.analytics.distribution import DistributionAnalyzer


def test_skew_positive_for_right_tail():
    df = pd.DataFrame({"a": [1, 1, 1, 1, 100]})
    assert DistributionAnalyzer(df).skew("a") > 0


def test_kurtosis_returns_float():
    df = pd.DataFrame({"a": [1, 2, 3, 4, 5]})
    assert isinstance(DistributionAnalyzer(df).kurtosis("a"), float)


def test_quantiles_default():
    df = pd.DataFrame({"a": list(range(1, 101))})
    qs = DistributionAnalyzer(df).quantiles("a")
    assert 0.5 in qs
    assert qs[0.5] == pytest.approx(50.5)


def test_quantiles_out_of_range_raises():
    df = pd.DataFrame({"a": [1, 2, 3]})
    with pytest.raises(ValueError, match="Quantile out of range"):
        DistributionAnalyzer(df).quantiles("a", qs=[1.5])


def test_histogram_counts_and_edges():
    df = pd.DataFrame({"a": list(range(100))})
    counts, edges = DistributionAnalyzer(df).histogram("a", bins=5)
    assert len(edges) == 6
    assert sum(counts) == 100


def test_missing_column_raises():
    df = pd.DataFrame({"a": [1, 2]})
    with pytest.raises(KeyError):
        DistributionAnalyzer(df).skew("b")


def test_non_numeric_raises():
    df = pd.DataFrame({"a": ["x", "y"]})
    with pytest.raises(TypeError):
        DistributionAnalyzer(df).skew("a")

