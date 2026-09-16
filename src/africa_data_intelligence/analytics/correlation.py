"""Correlation analysis for the Africa Data Intelligence analytics engine."""

import pandas as pd


class CorrelationAnalyzer:
    """Computes pairwise correlations between numeric columns."""

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def matrix(self, method: str = "pearson") -> pd.DataFrame:
        """Return the correlation matrix using the chosen method.

        Raises:
            ValueError: If the method is not one of pearson/spearman/kendall.
        """
        if method not in ("pearson", "spearman", "kendall"):
            raise ValueError(f"Unsupported method: {method}")
        return self.df.corr(numeric_only=True, method=method)

    def top_pairs(self, n: int = 5, method: str = "pearson") -> list[tuple[str, str, float]]:
        """Return the top-n strongest positive correlations (excluding self-pairs)."""
        corr = self.matrix(method=method)
        seen: set[tuple[str, str]] = set()
        pairs: list[tuple[str, str, float]] = []
        for col_a in corr.columns:
            for col_b in corr.columns:
                if col_a == col_b:
                    continue
                key = tuple(sorted((col_a, col_b)))
                if key in seen:
                    continue
                seen.add(key)
                value = float(corr.loc[col_a, col_b])
                if pd.notna(value) and value > 0:
                    pairs.append((col_a, col_b, value))
        pairs.sort(key=lambda p: p[2], reverse=True)
        return pairs[:n]

    def weakest_pairs(self, n: int = 5, method: str = "pearson") -> list[tuple[str, str, float]]:
        """Return the n weakest absolute correlations (excluding self-pairs)."""
        corr = self.matrix(method=method)
        seen: set[tuple[str, str]] = set()
        pairs: list[tuple[str, str, float]] = []
        for col_a in corr.columns:
            for col_b in corr.columns:
                if col_a == col_b:
                    continue
                key = tuple(sorted((col_a, col_b)))
                if key in seen:
                    continue
                seen.add(key)
                value = float(corr.loc[col_a, col_b])
                if pd.notna(value):
                    pairs.append((col_a, col_b, value))
        pairs.sort(key=lambda p: abs(p[2]))
        return pairs[:n]

