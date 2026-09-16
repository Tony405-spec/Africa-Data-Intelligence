"""Unit tests for the ExcelLoader class."""

import pandas as pd
import pytest

from africa_data_intelligence.ingestion.excel_loader import ExcelLoader


def _write_excel(path, sheets: dict[str, pd.DataFrame]) -> None:
    """Helper to write a multi-sheet Excel file."""
    with pd.ExcelWriter(path) as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name, index=False)


def test_load_default_sheet(tmp_path):
    """ExcelLoader should load the first sheet by default."""
    xlsx_path = tmp_path / "sample.xlsx"
    _write_excel(xlsx_path, {"Sheet1": pd.DataFrame({"a": [1, 2], "b": [3, 4]})})

    loader = ExcelLoader(xlsx_path)
    df = loader.load()

    assert len(df) == 2
    assert list(df.columns) == ["a", "b"]


def test_load_named_sheet(tmp_path):
    """ExcelLoader should load a specifically named sheet."""
    xlsx_path = tmp_path / "multi.xlsx"
    _write_excel(
        xlsx_path,
        {
            "First": pd.DataFrame({"x": [1]}),
            "Second": pd.DataFrame({"y": [10, 20]}),
        },
    )

    loader = ExcelLoader(xlsx_path, sheet_name="Second")
    df = loader.load()

    assert list(df.columns) == ["y"]
    assert len(df) == 2


def test_list_sheets(tmp_path):
    """list_sheets should return every sheet name in order."""
    xlsx_path = tmp_path / "multi.xlsx"
    _write_excel(
        xlsx_path,
        {
            "Alpha": pd.DataFrame({"a": [1]}),
            "Beta": pd.DataFrame({"b": [2]}),
        },
    )

    loader = ExcelLoader(xlsx_path)
    sheets = loader.list_sheets()

    assert sheets == ["Alpha", "Beta"]


def test_load_missing_file_raises(tmp_path):
    """ExcelLoader should raise FileNotFoundError for a missing file."""
    loader = ExcelLoader(tmp_path / "nope.xlsx")

    with pytest.raises(FileNotFoundError):
        loader.load()


def test_load_missing_sheet_raises(tmp_path):
    """ExcelLoader should raise ValueError when the sheet doesn't exist."""
    xlsx_path = tmp_path / "sample.xlsx"
    _write_excel(xlsx_path, {"OnlyOne": pd.DataFrame({"a": [1]})})

    loader = ExcelLoader(xlsx_path, sheet_name="DoesNotExist")

    with pytest.raises(ValueError, match="Could not read sheet"):
        loader.load()


def test_load_with_schema_passes(tmp_path):
    """load_with_schema should return the DataFrame when all columns exist."""
    xlsx_path = tmp_path / "sample.xlsx"
    _write_excel(xlsx_path, {"Sheet1": pd.DataFrame({"name": ["a"], "value": [1]})})

    loader = ExcelLoader(xlsx_path)
    df = loader.load_with_schema(required_columns=["name", "value"])

    assert list(df.columns) == ["name", "value"]


def test_load_with_schema_raises_on_missing(tmp_path):
    """load_with_schema should raise when required columns are absent."""
    xlsx_path = tmp_path / "sample.xlsx"
    _write_excel(xlsx_path, {"Sheet1": pd.DataFrame({"name": ["a"]})})

    loader = ExcelLoader(xlsx_path)

    with pytest.raises(ValueError, match="Missing required columns"):
        loader.load_with_schema(required_columns=["name", "value"])
