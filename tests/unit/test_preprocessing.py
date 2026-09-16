"""Unit tests for MLPreprocessor."""

import numpy as np
import pandas as pd
import pytest

from africa_data_intelligence.ml.preprocessing import MLPreprocessor


def test_fill_missing_median():
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
    result = MLPreprocessor().fill_missing(df, strategy="median")
    assert result["a"].isnull().sum() == 0
    assert result["a"].iloc[1] == 2.0


def test_fill_missing_mean():
    df = pd.DataFrame({"a": [1.0, np.nan, 5.0]})
    result = MLPreprocessor().fill_missing(df, strategy="mean")
    assert result["a"].iloc[1] == 3.0


def test_fill_missing_zero():
    df = pd.DataFrame({"a": [1.0, np.nan]})
    result = MLPreprocessor().fill_missing(df, strategy="zero")
    assert result["a"].iloc[1] == 0.0


def test_fill_missing_unsupported_raises():
    df = pd.DataFrame({"a": [1.0]})
    with pytest.raises(ValueError, match="Unsupported strategy"):
        MLPreprocessor().fill_missing(df, strategy="fancy")


def test_encode_categoricals():
    df = pd.DataFrame({"color": ["red", "blue", "red"], "n": [1, 2, 3]})
    result = MLPreprocessor().encode_categoricals(df)
    assert "color_red" in result.columns
    assert "color" not in result.columns


def test_encode_no_categoricals_returns_same():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    result = MLPreprocessor().encode_categoricals(df)
    assert list(result.columns) == ["a", "b"]


def test_standardize_zero_mean():
    df = pd.DataFrame({"a": [1.0, 2.0, 3.0]})
    result = MLPreprocessor().standardize(df)
    assert abs(result["a"].mean()) < 1e-9


def test_standardize_zero_std():
    df = pd.DataFrame({"a": [5.0, 5.0, 5.0]})
    result = MLPreprocessor().standardize(df)
    assert (result["a"] == 0.0).all()


def test_is_fitted_flag():
    pre = MLPreprocessor()
    assert pre.is_fitted() is False
    pre.standardize(pd.DataFrame({"a": [1, 2]}))
    assert pre.is_fitted() is True
