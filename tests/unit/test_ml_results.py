"""Unit tests for the ML results dashboard page."""

from dashboard.pages import ml_results


def test_render_is_callable():
    assert callable(ml_results.render)


def test_dataframe_has_expected_columns():
    df = ml_results._MODEL_RESULTS
    assert set(df.columns) == {"model", "rmse", "mae", "r2"}


def test_three_models_present():
    assert len(ml_results._MODEL_RESULTS) == 3


def test_r2_values_in_range():
    r2 = ml_results._MODEL_RESULTS["r2"]
    assert (r2 >= 0).all() and (r2 <= 1).all()


def test_best_model_is_random_forest():
    df = ml_results._MODEL_RESULTS
    best = df.loc[df["rmse"].idxmin()]
    assert best["model"] == "Random Forest"


def test_rmse_positive():
    assert (ml_results._MODEL_RESULTS["rmse"] > 0).all()

