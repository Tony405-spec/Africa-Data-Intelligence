"""Unit tests for the CSVLoader class."""

import pandas as pd
import pytest

from africa_data_intelligence.ingestion.csv_loader import CSVLoader


def test_load_valid_csv(tmp_path):
    """CSVLoader should load a valid CSV file into a DataFrame."""
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("name,value\nalpha,1\nbeta,2\n")

    loader = CSVLoader(csv_path)
    df = loader.load()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["name", "value"]


def test_load_missing_file_raises(tmp_path):
    """CSVLoader should raise FileNotFoundError for a missing file."""
    loader = CSVLoader(tmp_path / "does_not_exist.csv")

    with pytest.raises(FileNotFoundError):
        loader.load()


def test_load_empty_csv_raises(tmp_path):
    """CSVLoader should raise ValueError when the file has no rows."""
    csv_path = tmp_path / "empty.csv"
    csv_path.write_text("name,value\n")

    loader = CSVLoader(csv_path)

    with pytest.raises(ValueError, match="empty"):
        loader.load()


def test_load_with_schema_passes_when_columns_present(tmp_path):
    """load_with_schema should return the DataFrame when all columns exist."""
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("name,value\nalpha,1\n")

    loader = CSVLoader(csv_path)
    df = loader.load_with_schema(required_columns=["name", "value"])

    assert list(df.columns) == ["name", "value"]


def test_load_with_schema_raises_on_missing_columns(tmp_path):
    """load_with_schema should raise ValueError when required columns are missing."""
    csv_path = tmp_path / "sample.csv"
    csv_path.write_text("name,value\nalpha,1\n")

    loader = CSVLoader(csv_path)

    with pytest.raises(ValueError, match="Missing required columns"):
        loader.load_with_schema(required_columns=["name", "value", "missing_col"])
