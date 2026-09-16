"""Unit tests for dashboard table components."""

import pandas as pd
import pytest

from dashboard.components import tables


def _df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "country": ["Kenya", "Nigeria", "Ghana", "kenya"],
            "value": [100, 200, 50, 120],
        }
    )


def test_filter_dataframe_case_insensitive():
    result = tables.filter_dataframe(_df(), "country", "kenya")
    assert len(result) == 2


def test_filter_missing_column_raises():
    with pytest.raises(KeyError):
        tables.filter_dataframe(_df(), "continent", "Africa")


def test_sort_ascending():
    result = tables.sort_dataframe(_df(), "value")
    assert list(result["value"]) == [50, 100, 120, 200]


def test_sort_descending():
    result = tables.sort_dataframe(_df(), "value", ascending=False)
    assert list(result["value"]) == [200, 120, 100, 50]


def test_sort_missing_column_raises():
    with pytest.raises(KeyError):
        tables.sort_dataframe(_df(), "unknown")


def test_paginate_page_two():
    df = pd.DataFrame({"x": list(range(25))})
    result = tables.paginate(df, page=2, page_size=10)
    assert list(result["x"]) == list(range(10, 20))


def test_paginate_invalid_page_raises():
    with pytest.raises(ValueError):
        tables.paginate(_df(), page=0, page_size=10)


def test_paginate_invalid_page_size_raises():
    with pytest.raises(ValueError):
        tables.paginate(_df(), page=1, page_size=0)


def test_summarize_returns_shape():
    result = tables.summarize(_df())
    assert result == {"rows": 4, "columns": 2}

