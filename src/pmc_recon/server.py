"""FastAPI Backend Server serving REST API & WebSocket state for PMC Procurement Reconciliation.
Adheres to strict SOLID principles, Pydantic contracts, and clean REST conventions.
Enables full end-to-end demo execution and verification without touching the terminal.
"""

import sys
from pathlib import Path

# Bootstrap sys.path so server runs cleanly without requiring external PYTHONPATH
_SRC_DIR = Path(__file__).resolve().parent.parent
_REPO_ROOT = _SRC_DIR.parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(1, str(_REPO_ROOT))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from pathlib import Path
from typing import List, Dict, Any

from pmc_recon.storage.db import DatabaseEngine
from pmc_recon.models.entities import (
    FlagStatus, ReviewDecision, TenderRecord, TenderStatus, BudgetLine, BudgetLineType
)
from pmc_recon.ingest.budget_loader import BudgetLoader
from pmc_recon.ingest.tender_adapter import MahatendersAdapter
from pmc_recon.linking.matcher import EntityMatcher
from pmc_recon.rules.engine import AnomalyEngine
from pmc_recon.reporting.evidence import EvidenceReporter
from tests.fixtures.mock_data import MOCK_BUDGET_ROWS, MOCK_MAHATENDERS_HTML

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


class PipelineRunRequest(BaseModel):
    """Configuration options for triggering reconciliation pipeline from the browser."""
    mode: str = Field(default="demo")
    include_crawl: bool = Field(default=False)


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


@app.post("/api/pipeline/reset")
def reset_pipeline() -> Dict[str, Any]:
    """Resets demo state to clean empty baseline without requiring terminal access."""
    db.reset_database()
    return {"status": "reset_successful"}


@app.post("/api/pipeline/run")
def run_pipeline(payload: PipelineRunRequest = PipelineRunRequest()) -> Dict[str, Any]:
    """Triggers end-to-end reconciliation pipeline directly from UI controls."""
    # 1. Ingest municipal budget allocation rows
    loader = BudgetLoader(db)
    loaded_budget_count = loader.load_budget_rows(MOCK_BUDGET_ROWS)

    # 2. Ingest Mahatenders notices
    adapter = MahatendersAdapter(db, db)
    tenders = adapter.ingest_html("ui_run_001", MOCK_MAHATENDERS_HTML)

    # Add high-value benchmark tender (Wagholi-Lohegaon water supply trunk pipeline)
    benchmark_tender = TenderRecord(
        tender_id="PMCP/WTR/2026/042",
        reference_number="PMC-WS-2026-T42",
        title="Trunk distribution pipeline network Wagholi Lohegaon",
        department_chain="PMC/Water Supply/Distribution",
        value_inr=185_000_000.0,  # ₹ 18.50 Crore
        status=TenderStatus.ACTIVE,
        source_name="mahatenders"
    )
    db.upsert_tender(benchmark_tender)
    tenders.append(benchmark_tender)

    # 3. Cross-Dataset Entity Linking
    matcher = EntityMatcher(db, threshold=0.75)
    
    with db._get_connection() as conn:
        b_rows = conn.execute("SELECT * FROM budget_lines").fetchall()
    
    budget_entities = [
        BudgetLine(
            budget_head_code=r["budget_head_code"],
            fiscal_year=r["fiscal_year"],
            description_marathi=r["description_marathi"],
            description_english=r["description_english"],
            department=r["department"],
            amount_type=BudgetLineType(r["amount_type"]),
            amount_inr_crore=r["amount_inr_crore"],
            source_file=r["source_file"]
        ) for r in b_rows
    ]

    links_count = 0
    for tender in tenders:
        for b_line in budget_entities:
            link = matcher.link_tender_to_budget(tender, b_line)
            if link:
                links_count += 1

    # 4. Anomaly Detection & Mathematical Rule Evaluation
    engine = AnomalyEngine(db)
    flags_raised = 0

    # Rule R1: Mirror mismatch (Official ₹ 18.50 Cr vs Mirror ₹ 19.20 Cr, variance ₹ 0.70 Cr)
    r1_flag = engine.evaluate_rule_r1(
        official=benchmark_tender,
        mirror={"tender_value_inr": 192_000_000.0, "source": "eprocure_mirror"}
    )
    if r1_flag:
        flags_raised += 1

    # Rule R3: Budget Arithmetic Subtotal Totality (Electrical Dept ₹ 80.90 Cr + ₹ 185.22 Cr = ₹ 266.12 Cr vs stated ₹ 265.72 Cr)
    r3_flag = engine.evaluate_rule_r3(
        table_name="Electrical Department Capital Ledger Statement 4",
        component_amounts=[80.90, 185.22],
        stated_total=265.72,
        fiscal_year="2025-26"
    )
    if r3_flag:
        flags_raised += 1

    # Rule R6: Statistical Outlier Detector (Lohegaon pipeline 450 km vs distribution [16.5, 22.0, 35.0, 48.0, 52.0, 77.0])
    r6_flag = engine.evaluate_rule_r6(
        entity_name="Wagholi-Lohegaon Pipeline Package 3",
        metric_name="Length of Transmission Pipeline (km)",
        observed_value=450.0,
        peer_distribution=[16.5, 22.0, 35.0, 48.0, 52.0, 77.0],
        threshold_z=3.0
    )
    if r6_flag:
        flags_raised += 1

    return {
        "status": "completed",
        "tenders_ingested": len(tenders),
        "budget_lines_loaded": loaded_budget_count,
        "links_created": links_count,
        "flags_raised": flags_raised
    }


@app.get("/api/dossier/export/{flag_id}", response_class=PlainTextResponse)
def export_dossier(flag_id: str):
    """Exports a formal audit evidence dossier in Markdown directly to browser download."""
    reporter = EvidenceReporter(db)
    dossier_text = reporter.generate_flag_dossier(flag_id)
    return PlainTextResponse(
        content=dossier_text,
        media_type="text/markdown",
        headers={"Content-Disposition": f'attachment; filename="audit_dossier_{flag_id}.md"'}
    )
