"""Unit tests for the climate dashboard page."""

import pandas as pd

from dashboard.pages import climate


def test_render_is_callable():
    assert callable(climate.render)


def test_dataframe_has_expected_columns():
    df = climate._RAINFALL_DATA
    assert set(df.columns) == {"month", "rainfall_mm", "temperature_c"}


def test_dataframe_has_twelve_months():
    assert len(climate._RAINFALL_DATA) == 12


def test_rainfall_non_negative():
    assert (climate._RAINFALL_DATA["rainfall_mm"] >= 0).all()


def test_temperature_realistic_range():
    temps = climate._RAINFALL_DATA["temperature_c"]
    assert temps.min() >= 15
    assert temps.max() <= 35


def test_month_column_is_string():
    assert climate._RAINFALL_DATA["month"].dtype == object

