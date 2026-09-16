"""Missing value handler for the Africa Data Intelligence cleaning layer."""

from typing import Literal

import pandas as pd


Strategy = Literal["drop", "mean", "median", "mode", "forward_fill", "backward_fill"]


class MissingValueHandler:
    """Handles missing values in pandas DataFrames using common strategies."""

    def __init__(self, strategy: Strategy = "drop") -> None:
        self.strategy = strategy

    def handle(self, df: pd.DataFrame, columns: list[str] | None = None) -> pd.DataFrame:
        """Return a copy of the DataFrame with missing values handled.

        Args:
            df: The input DataFrame.
            columns: Optional subset of columns to act on. Defaults to all.

        Raises:
            ValueError: If an unknown strategy is provided.
        """
        result = df.copy()
        target_cols = columns if columns is not None else list(result.columns)

        if self.strategy == "drop":
            return result.dropna(subset=target_cols)

        if self.strategy in ("mean", "median"):
            for col in target_cols:
                if pd.api.types.is_numeric_dtype(result[col]):
                    filler = getattr(result[col], self.strategy)()
                    result[col] = result[col].fillna(filler)
            return result

        if self.strategy == "mode":
            for col in target_cols:
                mode = result[col].mode()
                if not mode.empty:
                    result[col] = result[col].fillna(mode.iloc[0])
            return result

        if self.strategy == "forward_fill":
            return result.ffill()

        if self.strategy == "backward_fill":
            return result.bfill()

        raise ValueError(f"Unknown strategy: {self.strategy}")
