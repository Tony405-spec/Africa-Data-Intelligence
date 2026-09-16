"""Trend analysis for the Africa Data Intelligence engine."""

import numpy as np
import pandas as pd


class TrendAnalyzer:
    """Computes simple trend metrics (slope, direction, growth rate)."""

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def slope(self, x_column: str, y_column: str) -> float:
        """Return the least-squares slope of y vs x."""
        self._assert_numeric(x_column, y_column)
        x = self.df[x_column].to_numpy(dtype=float)
        y = self.df[y_column].to_numpy(dtype=float)
        if len(x) < 2:
            return 0.0
        return float(np.polyfit(x, y, 1)[0])

    def direction(self, x_column: str, y_column: str, tolerance: float = 1e-9) -> str:
        """Return 'increasing', 'decreasing', or 'flat'."""
        s = self.slope(x_column, y_column)
        if s > tolerance:
            return "increasing"
        if s < -tolerance:
            return "decreasing"
        return "flat"

    def growth_rate(self, column: str) -> float:
        """Return percent change from first to last value (as %)."""
        self._assert_numeric(column)
        series = self.df[column].dropna()
        if len(series) < 2 or series.iloc[0] == 0:
            return 0.0
        return float((series.iloc[-1] - series.iloc[0]) / series.iloc[0] * 100.0)

    def rolling_mean(self, column: str, window: int = 7) -> pd.Series:
        """Return a rolling-mean Series for a numeric column.

        Raises:
            ValueError: If window is less than 1.
        """
        self._assert_numeric(column)
        if window < 1:
            raise ValueError("window must be >= 1")
        return self.df[column].rolling(window=window, min_periods=1).mean()

    def _assert_numeric(self, *columns: str) -> None:
        for col in columns:
            if col not in self.df.columns:
                raise KeyError(f"Column not found: {col}")
            if not pd.api.types.is_numeric_dtype(self.df[col]):
                raise TypeError(f"Column is not numeric: {col}")

