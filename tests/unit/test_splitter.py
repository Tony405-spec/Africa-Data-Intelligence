"""Unit tests for TrainTestSplitter."""

import pandas as pd
import pytest

from africa_data_intelligence.ml.splitter import TrainTestSplitter


def test_split_returns_two_dataframes():
    df = pd.DataFrame({"a": range(100)})
    train, test = TrainTestSplitter(test_size=0.2).split(df)
    assert len(train) == 80
    assert len(test) == 20


def test_split_is_reproducible():
    df = pd.DataFrame({"a": range(50)})
    train1, test1 = TrainTestSplitter(random_state=7).split(df)
    train2, test2 = TrainTestSplitter(random_state=7).split(df)
    assert train1.equals(train2)
    assert test1.equals(test2)


def test_split_rejects_invalid_test_size():
    with pytest.raises(ValueError):
        TrainTestSplitter(test_size=1.5)
    with pytest.raises(ValueError):
        TrainTestSplitter(test_size=0.0)


def test_split_empty_raises():
    with pytest.raises(ValueError, match="empty"):
        TrainTestSplitter().split(pd.DataFrame())


def test_time_split_is_chronological():
    df = pd.DataFrame({"time": [3, 1, 2, 5, 4], "value": [30, 10, 20, 50, 40]})
    train, test = TrainTestSplitter(test_size=0.4).time_split(df, "time")
    assert list(train["time"]) == [1, 2, 3]
    assert list(test["time"]) == [4, 5]


def test_time_split_missing_column_raises():
    df = pd.DataFrame({"a": [1, 2, 3]})
    with pytest.raises(KeyError):
        TrainTestSplitter().time_split(df, "time")
