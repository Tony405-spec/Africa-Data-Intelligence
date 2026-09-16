"""Anomaly detection for the Africa Data Intelligence engine."""

import numpy as np
import pandas as pd


class AnomalyDetector:
    """Detects numeric anomalies using z-score and IQR methods."""

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def zscore(self, column: str, threshold: float = 3.0) -> pd.Series:
        """Return a boolean mask of rows whose z-score exceeds threshold."""
        self._assert_numeric(column)
        series = self.df[column]
        mean = series.mean()
        std = series.std(ddof=0)
        if std == 0 or pd.isna(std):
            return pd.Series([False] * len(series), index=series.index)
        z = (series - mean) / std
        return z.abs() > threshold

    def iqr(self, column: str, factor: float = 1.5) -> pd.Series:
        """Return a boolean mask of IQR-based outliers."""
        self._assert_numeric(column)
        series = self.df[column]
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - factor * iqr
        upper = q3 + factor * iqr
        return (series < lower) | (series > upper)

    def count(self, column: str, method: str = "zscore") -> int:
        """Return the number of anomalies detected.

        Raises:
            ValueError: If the method is not zscore or iqr.
        """
        if method == "zscore":
            return int(self.zscore(column).sum())
        if method == "iqr":
            return int(self.iqr(column).sum())
        raise ValueError(f"Unsupported method: {method}")

    def _assert_numeric(self, column: str) -> None:
        if column not in self.df.columns:
            raise KeyError(f"Column not found: {column}")
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            raise TypeError(f"Column is not numeric: {column}")

