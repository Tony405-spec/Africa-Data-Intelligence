"""Schema validator for the Africa Data Intelligence validation layer."""

from dataclasses import dataclass, field
from typing import Optional

import pandas as pd


@dataclass
class SchemaSpec:
    """Expected schema for a DataFrame.

    Attributes:
        columns: Mapping of column name to expected pandas dtype string.
        required_columns: Columns that must be present (subset of columns).
        non_nullable_columns: Columns that must not contain null values.
    """

    columns: dict[str, str] = field(default_factory=dict)
    required_columns: Optional[list[str]] = None
    non_nullable_columns: Optional[list[str]] = None


class SchemaValidator:
    """Validates pandas DataFrames against a SchemaSpec."""

    def __init__(self, spec: SchemaSpec) -> None:
        self.spec = spec

    def validate(self, df: pd.DataFrame) -> None:
        """Validate the DataFrame against the schema.

        Raises:
            ValueError: If any part of the schema is violated.
        """
        self._check_required_columns(df)
        self._check_dtypes(df)
        self._check_nullable(df)

    def _check_required_columns(self, df: pd.DataFrame) -> None:
        if not self.spec.required_columns:
            return
        missing = set(self.spec.required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

    def _check_dtypes(self, df: pd.DataFrame) -> None:
        if not self.spec.columns:
            return
        for column, expected_dtype in self.spec.columns.items():
            if column not in df.columns:
                continue
            actual_dtype = str(df[column].dtype)
            if actual_dtype != expected_dtype:
                raise ValueError(
                    f"Column '{column}' has dtype '{actual_dtype}', "
                    f"expected '{expected_dtype}'"
                )

    def _check_nullable(self, df: pd.DataFrame) -> None:
        if not self.spec.non_nullable_columns:
            return
        for column in self.spec.non_nullable_columns:
            if column not in df.columns:
                continue
            if df[column].isnull().any():
                raise ValueError(f"Column '{column}' contains null values")
