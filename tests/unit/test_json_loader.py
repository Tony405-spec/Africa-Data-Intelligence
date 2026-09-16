"""Unit tests for the JSONLoader class."""

import json

import pandas as pd
import pytest

from africa_data_intelligence.ingestion.json_loader import JSONLoader


def test_load_dict_json(tmp_path):
    """JSONLoader should load a single dict into a one-row DataFrame."""
    json_path = tmp_path / "sample.json"
    json_path.write_text(json.dumps({"name": "alpha", "value": 1}))

    loader = JSONLoader(json_path)
    df = loader.load()

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]["name"] == "alpha"


def test_load_list_json(tmp_path):
    """JSONLoader should load a list of dicts into a multi-row DataFrame."""
    json_path = tmp_path / "list.json"
    json_path.write_text(
        json.dumps([{"name": "a", "value": 1}, {"name": "b", "value": 2}])
    )

    loader = JSONLoader(json_path)
    df = loader.load()

    assert len(df) == 2
    assert list(df["name"]) == ["a", "b"]


def test_load_missing_file_raises(tmp_path):
    """JSONLoader should raise FileNotFoundError for a missing file."""
    loader = JSONLoader(tmp_path / "nope.json")

    with pytest.raises(FileNotFoundError):
        loader.load()


def test_load_invalid_json_raises(tmp_path):
    """JSONLoader should raise ValueError for malformed JSON."""
    json_path = tmp_path / "bad.json"
    json_path.write_text("{not valid json")

    loader = JSONLoader(json_path)

    with pytest.raises(ValueError, match="Invalid JSON"):
        loader.load()


def test_load_empty_list_raises(tmp_path):
    """JSONLoader should raise ValueError for an empty list."""
    json_path = tmp_path / "empty.json"
    json_path.write_text("[]")

    loader = JSONLoader(json_path)

    with pytest.raises(ValueError, match="empty"):
        loader.load()


def test_load_with_schema_passes(tmp_path):
    """load_with_schema should return the DataFrame when all columns exist."""
    json_path = tmp_path / "sample.json"
    json_path.write_text(json.dumps([{"name": "a", "value": 1}]))

    loader = JSONLoader(json_path)
    df = loader.load_with_schema(required_columns=["name", "value"])

    assert list(df.columns) == ["name", "value"]


def test_load_with_schema_raises_on_missing(tmp_path):
    """load_with_schema should raise when required columns are absent."""
    json_path = tmp_path / "sample.json"
    json_path.write_text(json.dumps([{"name": "a"}]))

    loader = JSONLoader(json_path)

    with pytest.raises(ValueError, match="Missing required columns"):
        loader.load_with_schema(required_columns=["name", "value"])
