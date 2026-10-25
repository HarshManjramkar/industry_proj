"""Pre-seeded failing test oracles for Verification Layer & Story Implementation.
Enforces Article II & Prime Directive of Constitution.
"""

import pytest
from datetime import date
from pmc_recon.models.entities import TenderRecord, BudgetLine, Flag, FlagSeverity, FlagStatus
from pmc_recon.storage.db import DatabaseEngine


def test_flag_neutral_language_policy_oracle():
    """Oracle: Flag titles must strictly forbid defamatory/fraud words."""
    with pytest.raises(ValueError, match="neutral language policy"):
        Flag(
            flag_id="flg_01",
            rule_id="R1",
            title="Suspected fraud detected in tender allocation",
            severity=FlagSeverity.HIGH,
            evidence={"diff": 100},
            benign_explanations=["Mirror lag"]
        )


def test_database_immutable_raw_payload_and_change_event_oracle(tmp_path):
    """Oracle: DB must record immutable raw payload hash and detect tender modifications."""
    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    payload = b"<html><title>PMC Water Supply Tender 2026</title></html>"
    raw_doc = db.save_raw_payload(run_id="run_001", payload_bytes=payload)
    assert raw_doc.size_bytes == len(payload)
    assert len(raw_doc.content_hash) == 64

    # Insert initial tender
    t1 = TenderRecord(
        tender_id="PMCP/WTR/2026/001",
        reference_number="PMC-WTR-26-01",
        title="Pipeline maintenance in Lohegaon",
        value_inr=15000000.0,
        status="active",
        corrigenda_count=0,
        source_name="mahatenders",
        raw_doc_id=raw_doc.doc_id
    )
    chg1 = db.upsert_tender(t1)
    assert chg1 is not None
    assert chg1.change_type.value == "new"

    # Ingest modified tender with deadline/corrigendum update
    t2 = t1.model_copy(update={"value_inr": 16500000.0, "corrigenda_count": 1})
    chg2 = db.upsert_tender(t2)
    assert chg2 is not None
    assert chg2.change_type.value == "modified"
    assert "value_inr" in chg2.changed_fields


def test_budget_line_loading_oracle(tmp_path):
    """Oracle: Budget line entity must accurately store crore values and Marathi text."""
    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    line = BudgetLine(
        budget_head_code="RI11A101",
        description_marathi="पाणी पुरवठा वितरण व्यवस्था सक्षमीकरण",
        description_english="Water supply distribution strengthening",
        department="Water Supply",
        fiscal_year="2025-26",
        amount_type="actual",
        amount_inr_crore=42.50,
        source_file="budget_2025_26.xlsx"
    )
    db.insert_budget_line(line)
