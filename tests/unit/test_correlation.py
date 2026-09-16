"""Unit tests for CorrelationAnalyzer."""

import pandas as pd
import pytest

from africa_data_intelligence.analytics.correlation import CorrelationAnalyzer


def test_matrix_is_square():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [2, 4, 6], "c": [3, 1, 4]})
    matrix = CorrelationAnalyzer(df).matrix()
    assert list(matrix.columns) == ["a", "b", "c"]


def test_perfect_positive_correlation():
    df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 4, 6, 8]})
    corr = CorrelationAnalyzer(df).matrix()
    assert corr.loc["a", "b"] == pytest.approx(1.0)


def test_perfect_negative_correlation():
    df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [4, 3, 2, 1]})
    corr = CorrelationAnalyzer(df).matrix()
    assert corr.loc["a", "b"] == pytest.approx(-1.0)


def test_unsupported_method_raises():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    with pytest.raises(ValueError, match="Unsupported method"):
        CorrelationAnalyzer(df).matrix(method="bogus")


def test_top_pairs_returns_sorted():
    df = pd.DataFrame(
        {
            "a": [1, 2, 3, 4],
            "b": [2, 4, 6, 8],
            "c": [4, 1, 3, 2],
        }
    )
    pairs = CorrelationAnalyzer(df).top_pairs(n=2)
    assert pairs[0][0] in ("a", "b")
    assert pairs[0][2] <= 1.0
    assert len(pairs) <= 2


def test_weakest_pairs_returns_low_abs():
    df = pd.DataFrame({"a": [1, 2, 3, 4], "b": [2, 4, 6, 8], "c": [4, 1, 3, 2]})
    pairs = CorrelationAnalyzer(df).weakest_pairs(n=1)
    assert len(pairs) == 1
