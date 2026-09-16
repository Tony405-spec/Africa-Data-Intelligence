"""Unit tests for TypeCoercer."""

import pandas as pd
import pytest

from africa_data_intelligence.cleaning.type_coercer import TypeCoercer


def test_coerce_string_to_int():
    df = pd.DataFrame({"a": ["1", "2", "3"]})
    result = TypeCoercer({"a": "int"}).coerce(df)
    assert str(result["a"].dtype) == "Int64"
    assert result["a"].tolist() == [1, 2, 3]


def test_coerce_to_float():
    df = pd.DataFrame({"a": ["1.5", "2.5"]})
    result = TypeCoercer({"a": "float"}).coerce(df)
    assert result["a"].tolist() == [1.5, 2.5]


def test_coerce_to_string():
    df = pd.DataFrame({"a": [1, 2, 3]})
    result = TypeCoercer({"a": "str"}).coerce(df)
    assert str(result["a"].dtype) == "string"


def test_coerce_to_datetime():
    df = pd.DataFrame({"a": ["2024-01-01", "2024-06-15"]})
    result = TypeCoercer({"a": "datetime"}).coerce(df)
    assert pd.api.types.is_datetime64_any_dtype(result["a"])


def test_missing_column_raises():
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(ValueError, match="Column not found"):
        TypeCoercer({"b": "int"}).coerce(df)


def test_unsupported_dtype_raises():
    df = pd.DataFrame({"a": [1]})
    with pytest.raises(ValueError, match="Unsupported dtype"):
        TypeCoercer({"a": "complex128"}).coerce(df)


def test_coerce_with_errors_coerce():
    df = pd.DataFrame({"a": ["1", "bad", "3"]})
    result = TypeCoercer({"a": "float"}).coerce(df, errors="coerce")
    assert pd.isna(result["a"].iloc[1])
