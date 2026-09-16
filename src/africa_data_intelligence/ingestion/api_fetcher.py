"""HTTP API fetcher for the Africa Data Intelligence ingestion pipeline."""

from typing import Any, Optional

import pandas as pd
import requests


class APIFetcher:
    """Fetches JSON data from HTTP endpoints and returns pandas DataFrames."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 30,
        headers: Optional[dict[str, str]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.headers = headers or {}

    def fetch(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
    ) -> pd.DataFrame:
        """Fetch a JSON endpoint and return it as a DataFrame.

        Raises:
            requests.HTTPError: If the response is not successful.
            ValueError: If the response cannot be parsed into a DataFrame.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = requests.get(
            url, params=params, headers=self.headers, timeout=self.timeout
        )
        response.raise_for_status()
        payload = response.json()

        if isinstance(payload, dict):
            data = payload.get("data", payload)
        else:
            data = payload

        if isinstance(data, dict):
            return pd.DataFrame([data])
        if isinstance(data, list):
            return pd.DataFrame(data)
        raise ValueError(f"Unsupported payload type: {type(data).__name__}")
