"""JSON loader for the Africa Data Intelligence ingestion pipeline."""

import json
from pathlib import Path
from typing import Optional

import pandas as pd


class JSONLoader:
    """Loads JSON files into pandas DataFrames with basic validation."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)

    def load(self) -> pd.DataFrame:
        """Load the JSON file and return it as a DataFrame.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is empty or invalid.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.file_path}")

        try:
            with self.file_path.open("r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in {self.file_path}: {exc}") from exc

        if not data:
            raise ValueError(f"JSON file is empty: {self.file_path}")

        if isinstance(data, dict):
            df = pd.DataFrame([data])
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        else:
            raise ValueError(
                f"JSON must be a dict or list of dicts, got {type(data).__name__}"
            )

        return df

    def load_with_schema(
        self,
        required_columns: Optional[list[str]] = None,
    ) -> pd.DataFrame:
        """Load a JSON file and verify it contains the required columns.

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
