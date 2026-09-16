"""Data quality report for the Africa Data Intelligence validation layer."""

from dataclasses import dataclass

import pandas as pd


@dataclass
class QualityReport:
    """Aggregated data quality metrics for a DataFrame."""

    rows: int
    columns: int
    missing_values: int
    missing_percentage: float
    duplicate_rows: int
    memory_usage_mb: float
    column_dtypes: dict[str, str]

    def to_dataframe(self) -> pd.DataFrame:
        """Return the report as a tidy DataFrame."""
        return pd.DataFrame(
            {
                "metric": [
                    "rows",
                    "columns",
                    "missing_values",
                    "missing_percentage",
                    "duplicate_rows",
                    "memory_usage_mb",
                ],
                "value": [
                    self.rows,
                    self.columns,
                    self.missing_values,
                    self.missing_percentage,
                    self.duplicate_rows,
                    self.memory_usage_mb,
                ],
            }
        )


class QualityReportBuilder:
    """Builds a QualityReport from a pandas DataFrame."""

    def build(self, df: pd.DataFrame) -> QualityReport:
        """Compute quality metrics for the DataFrame."""
        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas DataFrame")

        rows, columns = df.shape
        missing_values = int(df.isnull().sum().sum())
        missing_pct = (missing_values / (rows * columns) * 100) if rows * columns else 0.0
        duplicates = int(df.duplicated().sum())
        mem_mb = round(df.memory_usage(deep=True).sum() / (1024 * 1024), 4)
        dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

        return QualityReport(
            rows=rows,
            columns=columns,
            missing_values=missing_values,
            missing_percentage=round(missing_pct, 4),
            duplicate_rows=duplicates,
            memory_usage_mb=mem_mb,
            column_dtypes=dtypes,
        )

