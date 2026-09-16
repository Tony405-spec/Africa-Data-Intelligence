"""Train/test splitting utilities for the Africa Data Intelligence ML engine."""

import numpy as np
import pandas as pd


class TrainTestSplitter:
    """Splits DataFrames into train/test sets deterministically."""

    def __init__(self, test_size: float = 0.2, random_state: int = 42) -> None:
        if not 0.0 < test_size < 1.0:
            raise ValueError("test_size must be in (0, 1)")
        self.test_size = test_size
        self.random_state = random_state

    def split(
        self,
        df: pd.DataFrame,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Return (train_df, test_df) via random shuffle."""
        if df.empty:
            raise ValueError("Cannot split an empty DataFrame")

        rng = np.random.default_rng(self.random_state)
        indices = rng.permutation(len(df))
        test_count = int(round(len(df) * self.test_size))
        test_idx = indices[:test_count]
        train_idx = indices[test_count:]
        return (
            df.iloc[train_idx].reset_index(drop=True),
            df.iloc[test_idx].reset_index(drop=True),
        )

    def time_split(
        self,
        df: pd.DataFrame,
        time_column: str,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Split chronologically using the given time column (earlier = train)."""
        if time_column not in df.columns:
            raise KeyError(f"Column not found: {time_column}")
        ordered = df.sort_values(time_column).reset_index(drop=True)
        cutoff = int(round(len(ordered) * (1 - self.test_size)))
        return ordered.iloc[:cutoff].reset_index(drop=True), ordered.iloc[cutoff:].reset_index(drop=True)
