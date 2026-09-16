"""PostgreSQL reader for the Africa Data Intelligence ingestion pipeline."""

from typing import Optional

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


class PostgreSQLReader:
    """Reads data from a PostgreSQL database into pandas DataFrames."""

    def __init__(self, connection_url: str) -> None:
        self.connection_url = connection_url
        self._engine: Optional[Engine] = None

    @property
    def engine(self) -> Engine:
        """Lazily create and cache the SQLAlchemy engine."""
        if self._engine is None:
            self._engine = create_engine(self.connection_url, future=True)
        return self._engine

    def read_table(self, table_name: str, schema: str = "public") -> pd.DataFrame:
        """Read an entire table into a DataFrame.

        Raises:
            ValueError: If the table name is empty.
        """
        if not table_name:
            raise ValueError("table_name must not be empty")

        query = text(f'SELECT * FROM "{schema}"."{table_name}"')
        with self.engine.connect() as conn:
            return pd.read_sql(query, conn)

    def read_query(self, query: str, params: Optional[dict] = None) -> pd.DataFrame:
        """Run a SELECT query and return the result as a DataFrame.

        Raises:
            ValueError: If the query is empty.
        """
        if not query or not query.strip():
            raise ValueError("query must not be empty")

        with self.engine.connect() as conn:
            return pd.read_sql(text(query), conn, params=params or {})
