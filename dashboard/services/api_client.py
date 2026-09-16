"""HTTP client for the Africa Data Intelligence API."""

from typing import Any, Optional

import requests


class APIClient:
    """Thin wrapper around requests for talking to the ADI FastAPI service."""

    def __init__(
        self,
        base_url: str = "http://localhost:8000",
        timeout: int = 10,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def get(self, path: str, params: Optional[dict[str, Any]] = None) -> Any:
        """Perform a GET request and return the parsed JSON.

        Raises:
            requests.HTTPError: If the response status is not successful.
            ValueError: If the path is empty.
        """
        if not path or not path.strip():
            raise ValueError("path must not be empty")

        url = f"{self.base_url}/{path.lstrip('/')}"
        response = requests.get(url, params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def post(self, path: str, payload: dict[str, Any]) -> Any:
        """Perform a POST request and return the parsed JSON."""
        if not path or not path.strip():
            raise ValueError("path must not be empty")

        url = f"{self.base_url}/{path.lstrip('/')}"
        response = requests.post(url, json=payload, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def health(self) -> dict[str, Any]:
        """Return the health endpoint response."""
        return self.get("/health")

    def datasets(self) -> list[dict[str, Any]]:
        """Return the list of datasets."""
        return self.get("/datasets")

    def countries(self) -> list[dict[str, Any]]:
        """Return the list of countries."""
        return self.get("/countries")

