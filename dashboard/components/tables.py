"""Reusable table components for the Africa Data Intelligence dashboard."""

import pandas as pd


def filter_dataframe(
    df: pd.DataFrame,
    column: str,
    value: str,
) -> pd.DataFrame:
    """Return rows where df[column] equals value (case-insensitive).

    Raises:
        KeyError: If the column does not exist.
    """
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")
    return df[df[column].astype(str).str.lower() == value.lower()].reset_index(drop=True)


def sort_dataframe(
    df: pd.DataFrame,
    column: str,
    ascending: bool = True,
) -> pd.DataFrame:
    """Return a sorted copy of df.

    Raises:
        KeyError: If the column does not exist.
    """
    if column not in df.columns:
        raise KeyError(f"Column not found: {column}")
    return df.sort_values(by=column, ascending=ascending).reset_index(drop=True)


def paginate(
    df: pd.DataFrame,
    page: int = 1,
    page_size: int = 10,
) -> pd.DataFrame:
    """Return a slice of df for the given 1-indexed page.

    Raises:
        ValueError: If page < 1 or page_size < 1.
    """
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size < 1:
        raise ValueError("page_size must be >= 1")
    start = (page - 1) * page_size
    end = start + page_size
    return df.iloc[start:end].reset_index(drop=True)


def summarize(df: pd.DataFrame) -> dict[str, int]:
    """Return row and column counts."""
    rows, columns = df.shape
    return {"rows": int(rows), "columns": int(columns)}

