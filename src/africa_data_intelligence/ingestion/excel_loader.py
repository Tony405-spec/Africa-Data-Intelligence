"""Excel loader for the Africa Data Intelligence ingestion pipeline."""

from pathlib import Path
from typing import Optional

import pandas as pd


class ExcelLoader:
    """Loads Excel files into pandas DataFrames with basic validation."""

    def __init__(self, file_path: str | Path, sheet_name: str | int = 0) -> None:
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name

    def load(self) -> pd.DataFrame:
        """Load the Excel file and return it as a DataFrame.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty or the sheet is missing.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {self.file_path}")

        try:
            df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
        except ValueError as exc:
            raise ValueError(
                f"Could not read sheet '{self.sheet_name}' from {self.file_path}: {exc}"
            ) from exc

        if df.empty:
            raise ValueError(f"Excel sheet is empty: {self.file_path}")

        return df

    def list_sheets(self) -> list[str]:
        """Return the names of all sheets in the workbook."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Excel file not found: {self.file_path}")

        with pd.ExcelFile(self.file_path) as xl:
            return xl.sheet_names

    def load_with_schema(
        self,
        required_columns: Optional[list[str]] = None,
    ) -> pd.DataFrame:
        """Load an Excel sheet and verify it contains the required columns.

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
