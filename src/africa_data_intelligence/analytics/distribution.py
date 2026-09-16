"""Distribution analysis for the Africa Data Intelligence analytics engine."""

import pandas as pd


class DistributionAnalyzer:
    """Computes distribution shape and quantile summaries for numeric columns."""

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def skew(self, column: str) -> float:
        """Return the skewness of a numeric column."""
        self._assert_numeric(column)
        return float(self.df[column].skew())

    def kurtosis(self, column: str) -> float:
        """Return the excess kurtosis of a numeric column."""
        self._assert_numeric(column)
        return float(self.df[column].kurtosis())

    def quantiles(
        self,
        column: str,
        qs: list[float] | None = None,
    ) -> dict[float, float]:
        """Return quantile values for a numeric column.

        Raises:
            ValueError: If any quantile is outside [0, 1].
        """
        self._assert_numeric(column)
        quantiles = qs or [0.1, 0.25, 0.5, 0.75, 0.9]
        for q in quantiles:
            if not 0.0 <= q <= 1.0:
                raise ValueError(f"Quantile out of range: {q}")
        values = self.df[column].quantile(quantiles)
        return {float(q): float(v) for q, v in values.items()}

    def histogram(
        self,
        column: str,
        bins: int = 10,
    ) -> tuple[list[int], list[float]]:
        """Return (counts, bin_edges) for a histogram of a numeric column."""
        self._assert_numeric(column)
        counts, edges = pd.cut(self.df[column], bins=bins, retbins=True)
        return counts.value_counts(sort=False).tolist(), [float(e) for e in edges]

    def _assert_numeric(self, column: str) -> None:
        if column not in self.df.columns:
            raise KeyError(f"Column not found: {column}")
        if not pd.api.types.is_numeric_dtype(self.df[column]):
            raise TypeError(f"Column is not numeric: {column}")

