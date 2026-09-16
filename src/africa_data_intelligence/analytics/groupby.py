
"""Group-by analytics for the Africa Data Intelligence engine."""

import pandas as pd


class GroupByEngine:
    """Aggregates numeric columns over one or more grouping columns."""

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    def aggregate(
        self,
        group_by: list[str],
        value_column: str,
        agg: str = "mean",
    ) -> pd.DataFrame:
        """Return the aggregated DataFrame.

        Raises:
            KeyError: If group_by or value_column are missing.
            TypeError: If value_column is not numeric.
            ValueError: If agg is unsupported.
        """
        allowed = {"sum", "mean", "median", "min", "max", "count", "std"}
        if agg not in allowed:
            raise ValueError(f"Unsupported aggregation: {agg}")
        for col in group_by + [value_column]:
            if col not in self.df.columns:
                raise KeyError(f"Column not found: {col}")
        if not pd.api.types.is_numeric_dtype(self.df[value_column]):
            raise TypeError(f"Column is not numeric: {value_column}")

        result = (
            self.df.groupby(group_by, as_index=False)[value_column]
            .agg(agg)
            .rename(columns={value_column: f"{value_column}_{agg}"})
        )
        return result

    def multi_aggregate(
        self,
        group_by: list[str],
        value_column: str,
    ) -> pd.DataFrame:
        """Return sum/mean/median/min/max/count for a numeric column."""
        for col in group_by + [value_column]:
            if col not in self.df.columns:
                raise KeyError(f"Column not found: {col}")
        if not pd.api.types.is_numeric_dtype(self.df[value_column]):
            raise TypeError(f"Column is not numeric: {value_column}")

        grouped = self.df.groupby(group_by)[value_column]
        return pd.DataFrame(
            {
                "sum": grouped.sum(),
                "mean": grouped.mean(),
                "median": grouped.median(),
                "min": grouped.min(),
                "max": grouped.max(),
                "count": grouped.count(),
            }
        ).reset_index()

