"""CSV loader for the Africa Data Intelligence ingestion pipeline."""

from pathlib import Path
from typing import Optional

import pandas as pd


class CSVLoader:
    """Loads CSV files into pandas DataFrames with basic validation."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        """Load the CSV file and return it as a DataFrame.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"CSV file not found: {self.file_path}")

        df = pd.read_csv(self.file_path)

        if df.empty:
            raise ValueError(f"CSV file is empty: {self.file_path}")

        return df

    def load_with_schema(
        self,
        required_columns: Optional[list[str]] = None,
    ) -> pd.DataFrame:
        """Load a CSV and verify it contains the required columns.

        Args:
            required_columns: List of column names that must be present.

        Raises:
            ValueError: If required columns are missing.
        """
        df = self.load()

        if required_columns:
            missing = set(required_columns) - set(df.columns)
            if missing:
                raise ValueError(f"Missing required columns: {missing}")

        return df
