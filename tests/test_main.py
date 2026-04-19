from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_add():
    r = client.post("/api/add", json={"a": 3, "b": 4})
    assert r.status_code == 200
    assert r.json()["result"] == 7


def test_config():
    r = client.get("/config")
    assert r.status_code == 200
    data = r.json()
    assert "DB_HOST" in data
    assert "DB_PORT" in data
    assert "DB_NAME" in data
    assert "DB_PASSWORD" in data
