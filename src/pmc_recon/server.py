"""FastAPI Backend Server serving REST API & WebSocket state for PMC Procurement Reconciliation.
Adheres to strict SOLID principles, Pydantic contracts, and clean REST conventions.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pathlib import Path
from typing import List, Dict, Any

from pmc_recon.storage.db import DatabaseEngine
from pmc_recon.models.entities import FlagStatus, ReviewDecision

app = FastAPI(title="PMC Reconciliation API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

db = DatabaseEngine()


class ReviewRequest(BaseModel):
    """Pydantic model enforcing strict schema validation for review submissions (CWE-20 mitigation)."""
    flag_id: str = Field(..., min_length=3, max_length=128)
    outcome: FlagStatus
    comment: str = Field(default="", max_length=1000)
    reviewer: str = Field(default="Harsh Manjramkar", max_length=128)


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    """Serves the primary zero-scroll command center HTML interface."""
    static_file = STATIC_DIR / "index.html"
    return FileResponse(static_file)


@app.get("/api/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "pmc_reconciliation"}


@app.get("/api/metrics")
def get_metrics() -> Dict[str, Any]:
    """Retrieves operational metrics from the database."""
    with db._get_connection() as conn:
        tenders = conn.execute("SELECT COUNT(*) FROM tenders").fetchone()[0]
        budget = conn.execute("SELECT COUNT(*) FROM budget_lines").fetchone()[0]
        links = conn.execute("SELECT COUNT(*) FROM entity_links").fetchone()[0]
        flags = conn.execute("SELECT COUNT(*) FROM flags WHERE status = 'open'").fetchone()[0]
        resolved = conn.execute("SELECT COUNT(*) FROM flags WHERE status != 'open'").fetchone()[0]
    return {
        "tenders_count": tenders,
        "budget_count": budget,
        "links_count": links,
        "open_flags": flags,
        "resolved_flags": resolved
    }


@app.get("/api/flags")
def list_flags() -> List[Dict[str, Any]]:
    """Lists all audit anomaly flags ordered by creation date."""
    with db._get_connection() as conn:
        rows = conn.execute("SELECT * FROM flags ORDER BY created_at DESC").fetchall()
    return [dict(r) for r in rows]


@app.get("/api/tenders")
def list_tenders() -> List[Dict[str, Any]]:
    """Lists all stored tenders ordered by valuation."""
    with db._get_connection() as conn:
        rows = conn.execute("SELECT * FROM tenders ORDER BY value_inr DESC").fetchall()
    return [dict(r) for r in rows]


@app.get("/api/budget")
def list_budget() -> List[Dict[str, Any]]:
    """Lists all budget allocation lines ordered by amount."""
    with db._get_connection() as conn:
        rows = conn.execute("SELECT * FROM budget_lines ORDER BY amount_inr_crore DESC").fetchall()
    return [dict(r) for r in rows]


@app.get("/api/links")
def list_links() -> List[Dict[str, Any]]:
    """Lists all entity links ordered by match confidence."""
    with db._get_connection() as conn:
        rows = conn.execute("SELECT * FROM entity_links ORDER BY confidence DESC").fetchall()
    return [dict(r) for r in rows]


@app.post("/api/review")
def post_review(payload: ReviewRequest) -> Dict[str, Any]:
    """Records a UAT review decision with strict Pydantic contract validation."""
    decision = ReviewDecision(
        review_id=f"rev_{abs(hash(payload.flag_id + payload.outcome.value)) % 100000}",
        flag_id=payload.flag_id,
        reviewer=payload.reviewer,
        outcome=payload.outcome,
        comment=payload.comment
    )
    db.record_review(decision)
    return {"status": "success", "flag_id": payload.flag_id, "outcome": payload.outcome.value}
