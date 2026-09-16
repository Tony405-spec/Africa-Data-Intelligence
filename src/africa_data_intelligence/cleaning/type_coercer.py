"""Type coercion utilities for the Africa Data Intelligence cleaning layer."""

import pandas as pd


class TypeCoercer:
    """Coerces DataFrame columns to specified dtypes with graceful failures."""

    def __init__(self, mapping: dict[str, str]) -> None:
        self.mapping = mapping

    def coerce(self, df: pd.DataFrame, errors: str = "raise") -> pd.DataFrame:
        """Return a copy of df with columns coerced to the target dtypes.

        Args:
            df: Input DataFrame.
            errors: 'raise' to fail loudly, 'coerce' to set invalid to NaN.

        Raises:
            ValueError: If a target column is missing or dtype is unsupported.
        """
        result = df.copy()

        for column, dtype in self.mapping.items():
            if column not in result.columns:
                raise ValueError(f"Column not found: {column}")

            try:
                if dtype in ("int", "int64"):
                    result[column] = pd.to_numeric(
                        result[column], errors=errors
                    ).astype("Int64")
                elif dtype in ("float", "float64"):
                    result[column] = pd.to_numeric(result[column], errors=errors)
                elif dtype in ("str", "string"):
                    result[column] = result[column].astype("string")
                elif dtype in ("bool", "boolean"):
                    result[column] = result[column].astype("boolean")
                elif dtype in ("datetime", "datetime64"):
                    result[column] = pd.to_datetime(result[column], errors=errors)
                else:
                    raise ValueError(f"Unsupported dtype: {dtype}")
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Failed to coerce column '{column}' to {dtype}: {exc}"
                ) from exc

        return result
