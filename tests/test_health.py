from fastapi.testclient import TestClient

from graphops_ai.api import app

client = TestClient(app)


def test_health_endpoint_reports_api_status() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": "0.1.0"}
