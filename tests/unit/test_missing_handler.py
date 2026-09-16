"""Unit tests for MissingValueHandler."""

import numpy as np
import pandas as pd
import pytest

from africa_data_intelligence.cleaning.missing_handler import MissingValueHandler


def test_drop_removes_rows_with_nulls():
    df = pd.DataFrame({"a": [1, np.nan, 3], "b": [4, 5, 6]})
    result = MissingValueHandler("drop").handle(df)
    assert len(result) == 2


def test_mean_fills_numeric():
    df = pd.DataFrame({"a": [1.0, np.nan, 3.0]})
    result = MissingValueHandler("mean").handle(df)
    assert result["a"].isnull().sum() == 0
    assert result["a"].iloc[1] == 2.0


def test_median_fills_numeric():
    df = pd.DataFrame({"a": [1.0, np.nan, 5.0]})
    result = MissingValueHandler("median").handle(df)
    assert result["a"].iloc[1] == 3.0


def test_mode_fills_categorical():
    df = pd.DataFrame({"a": ["x", "x", None]})
    result = MissingValueHandler("mode").handle(df)
    assert result["a"].isnull().sum() == 0
    assert result["a"].iloc[2] == "x"


def test_forward_fill():
    df = pd.DataFrame({"a": [1, None, 3]})
    result = MissingValueHandler("forward_fill").handle(df)
    assert result["a"].iloc[1] == 1


def test_backward_fill():
    df = pd.DataFrame({"a": [None, 2, 3]})
    result = MissingValueHandler("backward_fill").handle(df)
    assert result["a"].iloc[0] == 2


def test_unknown_strategy_raises():
    with pytest.raises(ValueError, match="Unknown strategy"):
        MissingValueHandler("bogus").handle(pd.DataFrame({"a": [1]}))
