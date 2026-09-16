"""Model comparison for the Africa Data Intelligence ML engine."""

import pandas as pd


class ModelComparator:
    """Ranks models by a chosen metric across a results dictionary."""

    def __init__(self, results: dict[str, dict[str, float]]) -> None:
        """Store per-model metric results.

        Args:
            results: Mapping of model_name -> {metric_name: value}.
        """
        self.results = results

    def to_dataframe(self) -> pd.DataFrame:
        """Return a comparison DataFrame (rows = models)."""
        if not self.results:
            return pd.DataFrame()
        return pd.DataFrame(self.results).T

    def rank_by(self, metric: str, ascending: bool = True) -> list[tuple[str, float]]:
        """Return model names sorted by metric.

        Raises:
            KeyError: If the metric is missing from any result.
        """
        df = self.to_dataframe()
        if df.empty or metric not in df.columns:
            raise KeyError(f"Metric not found: {metric}")
        ranked = df[metric].sort_values(ascending=ascending)
        return [(str(name), float(value)) for name, value in ranked.items()]

    def best_by(self, metric: str, ascending: bool = True) -> tuple[str, float]:
        """Return the best model name and its score for the metric."""
        ranked = self.rank_by(metric, ascending=ascending)
        return ranked[0]

    def summary(self, primary_metric: str = "rmse") -> pd.DataFrame:
        """Return a summary DataFrame with a rank column."""
        df = self.to_dataframe()
        if df.empty or primary_metric not in df.columns:
            return df
        df = df.copy()
        df["rank"] = df[primary_metric].rank(method="min").astype(int)
        return df.sort_values(primary_metric)
