"""Unit tests for the SchemaValidator class."""

import pandas as pd
import pytest

from africa_data_intelligence.validation.schema_validator import (
    SchemaSpec,
    SchemaValidator,
)


def test_validate_passes_on_correct_schema():
    """Validator should pass when all rules are satisfied."""
    df = pd.DataFrame({"name": ["a", "b"], "value": [1, 2]})
    spec = SchemaSpec(
        columns={"name": "object", "value": "int64"},
        required_columns=["name", "value"],
        non_nullable_columns=["name"],
    )
    SchemaValidator(spec).validate(df)  # should not raise


def test_missing_required_column_raises():
    """Validator should raise when a required column is absent."""
    df = pd.DataFrame({"name": ["a"]})
    spec = SchemaSpec(required_columns=["name", "value"])

    with pytest.raises(ValueError, match="Missing required columns"):
        SchemaValidator(spec).validate(df)


def test_dtype_mismatch_raises():
    """Validator should raise when a column has an unexpected dtype."""
    df = pd.DataFrame({"value": [1, 2]})
    spec = SchemaSpec(columns={"value": "float64"})

    with pytest.raises(ValueError, match="has dtype 'int64'"):
        SchemaValidator(spec).validate(df)


def test_nullable_violation_raises():
    """Validator should raise when a non-nullable column has nulls."""
    df = pd.DataFrame({"name": ["a", None]})
    spec = SchemaSpec(non_nullable_columns=["name"])

    with pytest.raises(ValueError, match="contains null values"):
        SchemaValidator(spec).validate(df)


def test_empty_spec_passes():
    """An empty spec should accept any DataFrame."""
    df = pd.DataFrame({"anything": [1, 2, 3]})
    SchemaValidator(SchemaSpec()).validate(df)  # should not raise


def test_extra_columns_are_allowed():
    """Extra columns in the DataFrame should not cause a failure."""
    df = pd.DataFrame({"name": ["a"], "value": [1], "extra": [99]})
    spec = SchemaSpec(
        columns={"name": "object", "value": "int64"},
        required_columns=["name", "value"],
    )
    SchemaValidator(spec).validate(df)  # should not raise


def test_required_column_not_in_dtype_map():
    """Required columns that aren't in the dtype map should still pass."""
    df = pd.DataFrame({"id": [1, 2], "name": ["a", "b"]})
    spec = SchemaSpec(
        columns={"name": "object"},
        required_columns=["id", "name"],
    )
    SchemaValidator(spec).validate(df)  # should not raise
