from unittest.mock import MagicMock, patch

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


def test_multiply():
    mock_response = MagicMock()
    mock_response.result = 12
    mock_response.computed_at = "2026-01-01T00:00:00Z"

    with patch("main.grpc.insecure_channel") as mock_channel:
        mock_stub = MagicMock()
        mock_stub.Multiply.return_value = mock_response
        mock_channel.return_value.__enter__ = MagicMock(return_value=MagicMock())
        with patch("main.calc_pb2_grpc.CalculatorStub", return_value=mock_stub):
            r = client.post("/api/multiply", json={"a": 3, "b": 4})
            assert r.status_code == 200
            assert r.json()["result"] == 12


def test_config():
    r = client.get("/config")
    assert r.status_code == 200
    data = r.json()
    assert "DB_HOST" in data
    assert "DB_PORT" in data
    assert "DB_NAME" in data
    assert "DB_PASSWORD" in data
