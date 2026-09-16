"""Date parsing utilities for the Africa Data Intelligence cleaning layer."""

from typing import Optional

import pandas as pd


class DateParser:
    """Parses date-like columns into pandas datetime with optional formats."""

    def __init__(self, formats: Optional[list[str]] = None) -> None:
        self.formats = formats or []

    def parse_column(
        self,
        df: pd.DataFrame,
        column: str,
        errors: str = "raise",
    ) -> pd.DataFrame:
        """Return a copy of df with the specified column parsed to datetime.

        Raises:
            ValueError: If the column is missing or cannot be parsed.
        """
        if column not in df.columns:
            raise ValueError(f"Column not found: {column}")

        result = df.copy()

        if self.formats:
            result[column] = pd.to_datetime(
                result[column], format=self.formats[0], errors=errors
            )
        else:
            result[column] = pd.to_datetime(result[column], errors=errors)

        return result

    def extract_components(
        self,
        df: pd.DataFrame,
        column: str,
    ) -> pd.DataFrame:
        """Return df with year, month, day, and weekday extracted from the column."""
        if column not in df.columns:
            raise ValueError(f"Column not found: {column}")

        result = df.copy()
        dt = pd.to_datetime(result[column])
        result[f"{column}_year"] = dt.dt.year
        result[f"{column}_month"] = dt.dt.month
        result[f"{column}_day"] = dt.dt.day
        result[f"{column}_weekday"] = dt.dt.dayofweek
        return result
