import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_index_returns_json(client):
    response = client.get("/")
    data = response.get_json()
    assert "message" in data
    assert "env" in data


def test_ping_returns_pong(client):
    response = client.get("/ping")
    data = response.get_json()
    assert data["pong"] is True


def test_health_returns_ok(client):
    response = client.get("/health")
    data = response.get_json()
    assert response.status_code == 200
    assert data["status"] == "ok"
