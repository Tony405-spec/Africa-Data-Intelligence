"""Unit tests for the countries endpoint."""

from fastapi.testclient import TestClient

from api.main import app


def test_list_countries_non_empty():
    client = TestClient(app)
    response = client.get("/countries")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5


def test_list_includes_kenya():
    client = TestClient(app)
    codes = [c["code"] for c in client.get("/countries").json()]
    assert "KE" in codes


def test_get_country_by_code():
    client = TestClient(app)
    response = client.get("/countries/ke")
    assert response.status_code == 200
    assert response.json()["name"] == "Kenya"


def test_get_unknown_country_returns_404():
    client = TestClient(app)
    response = client.get("/countries/zz")
    assert response.status_code == 404
