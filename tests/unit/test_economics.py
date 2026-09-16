"""Unit tests for the economics dashboard page."""

import pandas as pd

from dashboard.pages import economics


def test_render_is_callable():
    assert callable(economics.render)


def test_dataframe_has_expected_columns():
    df = economics._ECONOMIC_DATA
    assert set(df.columns) == {"year", "gdp_usd_billions", "inflation_pct"}


def test_dataframe_has_five_years():
    assert len(economics._ECONOMIC_DATA) == 5


def test_year_column_is_int():
    assert pd.api.types.is_integer_dtype(economics._ECONOMIC_DATA["year"])


def test_gdp_positive():
    assert (economics._ECONOMIC_DATA["gdp_usd_billions"] > 0).all()


def test_inflation_positive():
    assert (economics._ECONOMIC_DATA["inflation_pct"] > 0).all()

