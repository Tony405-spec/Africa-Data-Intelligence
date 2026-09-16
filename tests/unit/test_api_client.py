"""Unit tests for the dashboard APIClient (mocked)."""

from unittest.mock import MagicMock, patch

import pytest
import requests

from dashboard.services.api_client import APIClient


@patch("dashboard.services.api_client.requests.get")
def test_get_returns_json(mock_get):
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = {"status": "ok"}

    client = APIClient("https://example.com")
    result = client.get("/health")
    assert result == {"status": "ok"}


@patch("dashboard.services.api_client.requests.get")
def test_health_endpoint(mock_get):
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = {"status": "ok", "timestamp": "now"}

    result = APIClient("https://example.com").health()
    assert result["status"] == "ok"


@patch("dashboard.services.api_client.requests.get")
def test_datasets_endpoint_returns_list(mock_get):
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = [{"name": "A"}]

    result = APIClient("https://example.com").datasets()
    assert isinstance(result, list)


def test_empty_path_raises():
    client = APIClient("https://example.com")
    with pytest.raises(ValueError, match="must not be empty"):
        client.get("")


@patch("dashboard.services.api_client.requests.get")
def test_http_error_propagates(mock_get):
    mock_get.return_value.raise_for_status.side_effect = requests.HTTPError("404")

    with pytest.raises(requests.HTTPError):
        APIClient("https://example.com").get("/missing")


@patch("dashboard.services.api_client.requests.post")
def test_post_sends_payload(mock_post):
    mock_post.return_value.raise_for_status.return_value = None
    mock_post.return_value.json.return_value = {"predicted": 1.0}

    client = APIClient("https://example.com")
    client.post("/forecast", {"series": [1, 2, 3]})

    args, kwargs = mock_post.call_args
    assert kwargs["json"] == {"series": [1, 2, 3]}

