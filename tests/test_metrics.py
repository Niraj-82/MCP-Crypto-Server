from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def test_metrics_endpoint():
    response = client.get("/metrics")
    assert response.status_code == 200
    # content type should be the Prometheus exposition format
    assert "text/plain" in response.headers.get("content-type", "")
