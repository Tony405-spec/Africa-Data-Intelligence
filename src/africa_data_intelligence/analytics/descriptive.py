"""Descriptive statistics for the Africa Data Intelligence analytics engine."""

import pandas as pd


class DescriptiveStats:
    """Computes summary statistics for numeric columns in a DataFrame."""

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def numeric_columns(self) -> list[str]:
        """Return the names of numeric columns."""
        return self.df.select_dtypes(include="number").columns.tolist()

    def summary(self, columns: list[str] | None = None) -> pd.DataFrame:
        """Return a tidy summary (count, mean, std, min, 25%, 50%, 75%, max)."""
        target = columns if columns is not None else self.numeric_columns()
        if not target:
            return pd.DataFrame()
        return self.df[target].describe().T

    def mean(self, column: str) -> float:
        """Return the mean of a numeric column.

        Raises:
            KeyError: If the column does not exist.
            TypeError: If the column is not numeric.
        """
        self._assert_numeric(column)
        return float(self.df[column].mean())

    def median(self, column: str) -> float:
        """Return the median of a numeric column."""
        self._assert_numeric(column)
        return float(self.df[column].median())

    def std(self, column: str) -> float:
        """Return the standard deviation of a numeric column."""
        self._assert_numeric(column)
        return float(self.df[column].std())

    def _assert_numeric(self, column: str) -> None:
        if column not in self.df.columns:
            raise KeyError(f"Column not found: {column}")
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            raise TypeError(f"Column is not numeric: {column}")

