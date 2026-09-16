"""Unit tests for the FastAPI app skeleton and health endpoint."""

from fastapi.testclient import TestClient

from api.main import app


def test_root_returns_metadata():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Africa Data Intelligence API"
    assert "version" in data


def test_health_endpoint_ok():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data


def test_health_timestamp_is_iso_format():
    client = TestClient(app)
    response = client.get("/health")
    timestamp = response.json()["timestamp"]
    # ISO format contains a "T" separating date and time
    assert "T" in timestamp
