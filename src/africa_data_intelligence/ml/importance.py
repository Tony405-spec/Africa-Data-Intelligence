"""Feature importance aggregation for the Africa Data Intelligence ML engine."""

import numpy as np
import pandas as pd


class FeatureImportance:
    """Normalizes and ranks feature importance scores from multiple models."""

    def __init__(self, scores: dict[str, dict[str, float]]) -> None:
        """Store per-model importance scores.

        Args:
            scores: Mapping of model_name -> {feature_name: score}.
        """
        self.scores = scores

    def to_dataframe(self) -> pd.DataFrame:
        """Return a DataFrame with rows = features, columns = models."""
        if not self.scores:
            return pd.DataFrame()
        return pd.DataFrame(self.scores).fillna(0.0)

    def mean_importance(self) -> pd.Series:
        """Return the mean importance per feature, sorted descending."""
        df = self.to_dataframe()
        if df.empty:
            return pd.Series(dtype=float)
        return df.mean(axis=1).sort_values(ascending=False)

    def top_k(self, k: int = 5) -> list[tuple[str, float]]:
        """Return the top-k features by mean importance.

        Raises:
            ValueError: If k is less than 1.
        """
        if k < 1:
            raise ValueError("k must be >= 1")
        means = self.mean_importance()
        return [(str(name), float(value)) for name, value in means.head(k).items()]

    def normalized(self) -> pd.DataFrame:
        """Return a DataFrame where each model's scores sum to 1."""
        df = self.to_dataframe()
        if df.empty:
            return df
        totals = df.sum(axis=0).replace(0, np.nan)
        normalized = df.divide(totals, axis=1).fillna(0.0)
        return normalized
