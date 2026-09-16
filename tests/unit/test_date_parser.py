"""Unit tests for DateParser."""

import pandas as pd
import pytest

from africa_data_intelligence.cleaning.date_parser import DateParser


def test_parse_iso_dates():
    df = pd.DataFrame({"date": ["2024-01-01", "2024-06-15"]})
    result = DateParser().parse_column(df, "date")
    assert pd.api.types.is_datetime64_any_dtype(result["date"])


def test_parse_with_explicit_format():
    df = pd.DataFrame({"date": ["01/01/2024", "15/06/2024"]})
    result = DateParser(formats=["%d/%m/%Y"]).parse_column(df, "date")
    assert result["date"].iloc[0].year == 2024


def test_missing_column_raises():
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(ValueError, match="Column not found"):
        DateParser().parse_column(df, "date")


def test_invalid_date_raises():
    df = pd.DataFrame({"date": ["not a date"]})
    with pytest.raises(Exception):
        DateParser().parse_column(df, "date")


def test_extract_components():
    df = pd.DataFrame({"date": ["2024-03-15"]})
    result = DateParser().extract_components(df, "date")
    assert result["date_year"].iloc[0] == 2024
    assert result["date_month"].iloc[0] == 3
    assert result["date_day"].iloc[0] == 15
    assert "date_weekday" in result.columns


def test_extract_components_missing_column():
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(ValueError, match="Column not found"):
        DateParser().extract_components(df, "date")
