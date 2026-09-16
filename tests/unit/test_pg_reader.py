"""Unit tests for PostgreSQLReader using mocks (no live DB required)."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from africa_data_intelligence.ingestion.pg_reader import PostgreSQLReader


def _fake_engine(df: pd.DataFrame) -> MagicMock:
    """Build a MagicMock engine whose connect() context manager returns a conn."""
    engine = MagicMock()
    conn = MagicMock()
    engine.connect.return_value.__enter__.return_value = conn
    return engine


@patch("africa_data_intelligence.ingestion.pg_reader.pd.read_sql")
def test_read_table_returns_dataframe(mock_read_sql):
    mock_read_sql.return_value = pd.DataFrame({"a": [1, 2]})

    reader = PostgreSQLReader("postgresql://user:pass@localhost/db")
    reader._engine = _fake_engine(mock_read_sql.return_value)

    df = reader.read_table("my_table")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


def test_read_table_empty_name_raises():
    reader = PostgreSQLReader("postgresql://user:pass@localhost/db")
    with pytest.raises(ValueError, match="table_name must not be empty"):
        reader.read_table("")


def test_read_query_empty_raises():
    reader = PostgreSQLReader("postgresql://user:pass@localhost/db")
    with pytest.raises(ValueError, match="query must not be empty"):
        reader.read_query("   ")


@patch("africa_data_intelligence.ingestion.pg_reader.pd.read_sql")
def test_read_query_passes_params(mock_read_sql):
    mock_read_sql.return_value = pd.DataFrame()

    reader = PostgreSQLReader("postgresql://user:pass@localhost/db")
    reader._engine = _fake_engine(mock_read_sql.return_value)

    reader.read_query("SELECT * FROM t WHERE id = :id", params={"id": 1})

    args, kwargs = mock_read_sql.call_args
    assert kwargs["params"] == {"id": 1}


def test_engine_is_cached():
    reader = PostgreSQLReader("postgresql://user:pass@localhost/db")
    e1 = reader.engine
    e2 = reader.engine
    assert e1 is e2
