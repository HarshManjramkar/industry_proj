"""ATDD Test Oracles for FastAPI Backend and Zero-Scroll UI.
Verifies API contracts and static UI serving.
"""

from fastapi.testclient import TestClient
from pmc_recon.server import app


def test_server_health_oracle():
    """Scenario: Health check endpoint returns healthy status."""
    client = TestClient(app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "pmc_reconciliation"}


def test_server_ui_serving_oracle():
    """Scenario: Root endpoint serves zero-scroll Command Center interface."""
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "PMC Procurement Reconciliation Command Center" in response.text
    assert "overflow: hidden" in response.text  # Enforces zero-scroll constraint
