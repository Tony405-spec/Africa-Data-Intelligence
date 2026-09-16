"""Unit tests for DuplicateDetector."""

import pandas as pd

from africa_data_intelligence.validation.duplicate_detector import DuplicateDetector


def test_count_no_duplicates():
    df = pd.DataFrame({"a": [1, 2, 3]})
    assert DuplicateDetector().count(df) == 0


def test_count_with_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2, 2, 2]})
    assert DuplicateDetector().count(df) == 3


def test_remove_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "x", "y"]})
    result = DuplicateDetector().remove(df)
    assert len(result) == 2
    assert list(result["a"]) == [1, 2]


def test_subset_only_checks_selected_columns():
    df = pd.DataFrame({"a": [1, 1, 2], "b": ["x", "y", "z"]})
    detector = DuplicateDetector(subset=["a"])
    assert detector.count(df) == 1


def test_find_returns_only_duplicates():
    df = pd.DataFrame({"a": [1, 1, 2]})
    found = DuplicateDetector().find(df)
    assert len(found) == 1
    assert found.iloc[0]["a"] == 1


def test_has_duplicates_true_and_false():
    df_dup = pd.DataFrame({"a": [1, 1]})
    df_clean = pd.DataFrame({"a": [1, 2]})
    assert DuplicateDetector().has_duplicates(df_dup) is True
    assert DuplicateDetector().has_duplicates(df_clean) is False

