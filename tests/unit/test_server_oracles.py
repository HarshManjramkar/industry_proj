"""ATDD Test Oracles for FastAPI Backend and Zero-Scroll UI.
Verifies API contracts, pipeline execution endpoints, and static UI serving.
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
    assert "btn-run-pipeline" in response.text  # Interactive one-click pipeline run
    assert "btn-reset-demo" in response.text    # Interactive one-click demo reset


def test_pipeline_reset_oracle():
    """Scenario: User resets demo state to pristine condition without touching terminal."""
    client = TestClient(app)
    response = client.post("/api/pipeline/reset")
    assert response.status_code == 200
    assert response.json()["status"] == "reset_successful"

    # Metrics must show empty state
    m_res = client.get("/api/metrics")
    assert m_res.status_code == 200
    metrics = m_res.json()
    assert metrics["tenders_count"] == 0
    assert metrics["open_flags"] == 0


def test_pipeline_run_oracle():
    """Scenario: User triggers end-to-end reconciliation pipeline directly from UI."""
    client = TestClient(app)
    # Trigger pipeline run
    run_res = client.post("/api/pipeline/run", json={"mode": "demo"})
    assert run_res.status_code == 200
    data = run_res.json()
    assert data["status"] == "completed"
    assert data["tenders_ingested"] > 0
    assert data["budget_lines_loaded"] > 0
    assert data["links_created"] > 0
    assert data["flags_raised"] > 0

    # Metrics must reflect populated records
    metrics = client.get("/api/metrics").json()
    assert metrics["tenders_count"] > 0
    assert metrics["budget_count"] > 0
    assert metrics["links_count"] > 0
    assert metrics["open_flags"] > 0


def test_dossier_export_oracle():
    """Scenario: User exports audit dossier directly from browser interface."""
    client = TestClient(app)
    # Ensure pipeline has run
    client.post("/api/pipeline/run", json={"mode": "demo"})
    flags = client.get("/api/flags").json()
    assert len(flags) > 0
    flag_id = flags[0]["flag_id"]

    export_res = client.get(f"/api/dossier/export/{flag_id}")
    assert export_res.status_code == 200
    assert "PMC PROCUREMENT RECONCILIATION AUDIT DOSSIER" in export_res.text
    assert flag_id in export_res.text
