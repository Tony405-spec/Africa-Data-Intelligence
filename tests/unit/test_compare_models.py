"""Unit tests for ModelComparator."""

import pytest

from africa_data_intelligence.ml.compare import ModelComparator


def _results() -> dict[str, dict[str, float]]:
    return {
        "random_forest": {"rmse": 100.0, "mae": 80.0, "r2": 0.85},
        "xgboost": {"rmse": 90.0, "mae": 70.0, "r2": 0.88},
        "linear": {"rmse": 200.0, "mae": 180.0, "r2": 0.60},
    }


def test_to_dataframe_has_all_models():
    df = ModelComparator(_results()).to_dataframe()
    assert set(df.index) == {"random_forest", "xgboost", "linear"}


def test_rank_by_rmse_ascending():
    ranked = ModelComparator(_results()).rank_by("rmse")
    assert ranked[0][0] == "xgboost"


def test_rank_by_r2_descending():
    ranked = ModelComparator(_results()).rank_by("r2", ascending=False)
    assert ranked[0][0] == "xgboost"


def test_best_by_returns_tuple():
    best = ModelComparator(_results()).best_by("rmse")
    assert best[0] == "xgboost"
    assert best[1] == 90.0


def test_rank_missing_metric_raises():
    with pytest.raises(KeyError):
        ModelComparator(_results()).rank_by("fancy_metric")


def test_summary_has_rank_column():
    summary = ModelComparator(_results()).summary("rmse")
    assert "rank" in summary.columns
    assert summary.iloc[0]["rank"] == 1


def test_empty_results():
    comparator = ModelComparator({})
    assert comparator.to_dataframe().empty
