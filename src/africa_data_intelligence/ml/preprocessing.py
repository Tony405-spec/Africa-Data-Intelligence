"""Preprocessing helpers for the Africa Data Intelligence ML engine."""

import pandas as pd


class MLPreprocessor:
    """Handles missing values, encoding, and scaling for ML workflows."""

    def __init__(self) -> None:
        self._fitted = False

    def fill_missing(self, df: pd.DataFrame, strategy: str = "median") -> pd.DataFrame:
        """Return df with numeric missing values filled.

        Raises:
            ValueError: If strategy is unsupported.
        """
        if strategy not in ("mean", "median", "zero"):
            raise ValueError(f"Unsupported strategy: {strategy}")
        result = df.copy()
        numeric_cols = result.select_dtypes(include="number").columns
        for col in numeric_cols:
            if strategy == "mean":
                result[col] = result[col].fillna(result[col].mean())
            elif strategy == "median":
                result[col] = result[col].fillna(result[col].median())
            else:
                result[col] = result[col].fillna(0)
        return result

    def encode_categoricals(
        self,
        df: pd.DataFrame,
        drop_first: bool = True,
    ) -> pd.DataFrame:
        """One-hot encode all object/category columns."""
        result = df.copy()
        cat_cols = result.select_dtypes(include=["object", "category"]).columns
        if len(cat_cols) == 0:
            return result
        return pd.get_dummies(result, columns=cat_cols, drop_first=drop_first)

    def standardize(self, df: pd.DataFrame) -> pd.DataFrame:
        """Z-score standardize numeric columns."""
        result = df.copy()
        numeric_cols = result.select_dtypes(include="number").columns
        for col in numeric_cols:
            mean = result[col].mean()
            std = result[col].std(ddof=0)
            if std == 0 or pd.isna(std):
                result[col] = 0.0
            else:
                result[col] = (result[col] - mean) / std
        self._fitted = True
        return result

    def is_fitted(self) -> bool:
        """Return True if standardize has been called."""
        return self._fitted
