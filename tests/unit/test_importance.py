"""Unit tests for FeatureImportance."""

import pandas as pd
import pytest

from africa_data_intelligence.ml.importance import FeatureImportance


def _scores() -> dict[str, dict[str, float]]:
    return {
        "rf": {"age": 0.4, "income": 0.35, "score": 0.25},
        "xgb": {"age": 0.3, "income": 0.5, "score": 0.2},
    }


def test_to_dataframe_shape():
    df = FeatureImportance(_scores()).to_dataframe()
    assert set(df.columns) == {"rf", "xgb"}
    assert set(df.index) == {"age", "income", "score"}


def test_mean_importance_sorted():
    means = FeatureImportance(_scores()).mean_importance()
    assert means.index[0] in ("income", "age")


def test_top_k_returns_expected_count():
    top = FeatureImportance(_scores()).top_k(k=2)
    assert len(top) == 2
    assert all(isinstance(name, str) for name, _ in top)


def test_top_k_invalid_raises():
    with pytest.raises(ValueError, match="k must be"):
        FeatureImportance(_scores()).top_k(k=0)


def test_normalized_sums_to_one():
    normalized = FeatureImportance(_scores()).normalized()
    for col in normalized.columns:
        assert abs(normalized[col].sum() - 1.0) < 1e-9


def test_empty_input_returns_empty():
    fi = FeatureImportance({})
    assert fi.to_dataframe().empty
    assert fi.mean_importance().empty
