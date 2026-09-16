"""Unit tests for the datasets endpoints."""

from fastapi.testclient import TestClient

from api.main import app


def test_list_datasets_returns_list():
    client = TestClient(app)
    response = client.get("/datasets")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_list_datasets_includes_kenya():
    client = TestClient(app)
    response = client.get("/datasets")
    names = [d["name"] for d in response.json()]
    assert "Kenya Population by County" in names


def test_get_dataset_detail():
    client = TestClient(app)
    response = client.get("/datasets/Kenya Population by County")
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "Kenya"
    assert "variables" in data


def test_get_missing_dataset_returns_404():
    client = TestClient(app)
    response = client.get("/datasets/Unknown Dataset")
    assert response.status_code == 404
