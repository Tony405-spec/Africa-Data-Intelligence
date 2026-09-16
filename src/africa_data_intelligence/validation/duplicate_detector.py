"""Duplicate detection for the Africa Data Intelligence validation layer."""

import pandas as pd


class DuplicateDetector:
    """Detects and optionally removes duplicate rows from a DataFrame."""

    def __init__(self, subset: list[str] | None = None) -> None:
        self.subset = subset

    def find(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return rows that are duplicates of earlier rows."""
        mask = df.duplicated(subset=self.subset, keep="first")
        return df[mask].copy()

    def count(self, df: pd.DataFrame) -> int:
        """Return the number of duplicate rows."""
        return int(df.duplicated(subset=self.subset, keep="first").sum())

    def remove(self, df: pd.DataFrame) -> pd.DataFrame:
        """Return the DataFrame with duplicates removed."""
        return df.drop_duplicates(subset=self.subset, keep="first").reset_index(drop=True)

    def has_duplicates(self, df: pd.DataFrame) -> bool:
        """Return True if any duplicates exist."""
        return self.count(df) > 0
