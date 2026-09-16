"""Unit tests for GroupByEngine."""

import pandas as pd
import pytest

from africa_data_intelligence.analytics.groupby import GroupByEngine


def _df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "country": ["Kenya", "Kenya", "Nigeria", "Nigeria"],
            "year": [2020, 2021, 2020, 2021],
            "population": [100, 200, 500, 700],
        }
    )


def test_aggregate_mean():
    result = GroupByEngine(_df()).aggregate(["country"], "population", "mean")
    kenya_row = result[result["country"] == "Kenya"].iloc[0]
    assert kenya_row["population_mean"] == pytest.approx(150)


def test_aggregate_sum():
    result = GroupByEngine(_df()).aggregate(["country"], "population", "sum")
    nigeria_row = result[result["country"] == "Nigeria"].iloc[0]
    assert nigeria_row["population_sum"] == 1200


def test_unsupported_agg_raises():
    with pytest.raises(ValueError, match="Unsupported aggregation"):
        GroupByEngine(_df()).aggregate(["country"], "population", "fancy")


def test_missing_column_raises():
    with pytest.raises(KeyError, match="Column not found"):
        GroupByEngine(_df()).aggregate(["continent"], "population")


def test_non_numeric_raises():
    df = _df()
    with pytest.raises(TypeError, match="not numeric"):
        GroupByEngine(df).aggregate(["country"], "country")


def test_multi_aggregate_shape():
    result = GroupByEngine(_df()).multi_aggregate(["country"], "population")
    assert set(result.columns) >= {"country", "sum", "mean", "median", "min", "max", "count"}
    assert len(result) == 2


def test_group_by_multiple_columns():
    result = GroupByEngine(_df()).aggregate(["country", "year"], "population", "sum")
    assert len(result) == 4

