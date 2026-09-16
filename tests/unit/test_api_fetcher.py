"""Unit tests for APIFetcher using monkeypatched requests.get."""

from unittest.mock import patch

import pandas as pd
import pytest
import requests

from africa_data_intelligence.ingestion.api_fetcher import APIFetcher


@patch("africa_data_intelligence.ingestion.api_fetcher.requests.get")
def test_fetch_list_payload(mock_get):
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = [{"a": 1}, {"a": 2}]

    df = APIFetcher("https://example.com").fetch("/items")

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2


@patch("africa_data_intelligence.ingestion.api_fetcher.requests.get")
def test_fetch_dict_wrapped_in_data_key(mock_get):
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = {"data": [{"x": 10}]}

    df = APIFetcher("https://example.com").fetch("items")

    assert df.iloc[0]["x"] == 10


@patch("africa_data_intelligence.ingestion.api_fetcher.requests.get")
def test_fetch_single_dict_payload(mock_get):
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = {"name": "alpha"}

    df = APIFetcher("https://example.com").fetch("/one")

    assert len(df) == 1
    assert df.iloc[0]["name"] == "alpha"


@patch("africa_data_intelligence.ingestion.api_fetcher.requests.get")
def test_fetch_raises_on_http_error(mock_get):
    mock_get.return_value.raise_for_status.side_effect = requests.HTTPError("404")

    with pytest.raises(requests.HTTPError):
        APIFetcher("https://example.com").fetch("/missing")


@patch("africa_data_intelligence.ingestion.api_fetcher.requests.get")
def test_fetch_raises_on_unsupported_payload(mock_get):
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = 42

    with pytest.raises(ValueError, match="Unsupported payload type"):
        APIFetcher("https://example.com").fetch("/weird")


@patch("africa_data_intelligence.ingestion.api_fetcher.requests.get")
def test_fetch_builds_correct_url(mock_get):
    mock_get.return_value.raise_for_status.return_value = None
    mock_get.return_value.json.return_value = []

    APIFetcher("https://example.com/").fetch("items")

    called_url = mock_get.call_args[0][0]
    assert called_url == "https://example.com/items"
