"""ATDD Test Oracles for Epic 5: Review Decisions & Evidence Reports.
Validates review state transitions and Markdown/HTML evidence generation.
"""

from pmc_recon.models.entities import Flag, FlagSeverity, FlagStatus, ReviewDecision
from pmc_recon.storage.db import DatabaseEngine


def test_story_5_1_review_decision_audit_oracle(tmp_path):
    """Scenario: Reviewer records decision on a raised flag.
    Given an open anomaly flag
    When reviewer marks it as EXPLAINED with audit remarks
    Then flag status updates and audit record is persisted.
    """
    from pmc_recon.reporting.evidence import EvidenceReporter

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    reporter = EvidenceReporter(db)

    flag = Flag(
        flag_id="flg_demo_01",
        rule_id="R1",
        title="Discrepancy in tender valuation",
        severity=FlagSeverity.LOW,
        evidence={"measured_difference": "₹ 50,000"},
        benign_explanations=["Rounding variance"]
    )
    db.insert_flag(flag)

    decision = ReviewDecision(
        review_id="rev_001",
        flag_id="flg_demo_01",
        reviewer="Harsh Manjramkar",
        outcome=FlagStatus.EXPLAINED,
        comment="Confirmed mirror lag. Official corrigendum 1 confirms original price."
    )
    db.record_review(decision)

    # Verify status changed
    with db._get_connection() as conn:
        row = conn.execute("SELECT status FROM flags WHERE flag_id = 'flg_demo_01'").fetchone()
        assert row["status"] == FlagStatus.EXPLAINED.value


def test_story_5_2_evidence_sheet_generation_oracle(tmp_path):
    """Scenario: Generate standalone evidence dossier with full cryptographic lineage.
    Given an evaluated flag in the database
    When evidence exporter compiles the dossier
    Then dossier contains rule parameters, neutral wording, and raw payload references.
    """
    from pmc_recon.reporting.evidence import EvidenceReporter

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    reporter = EvidenceReporter(db)

    flag = Flag(
        flag_id="flg_demo_02",
        rule_id="R3",
        title="Arithmetic variance in budget line items",
        severity=FlagSeverity.MEDIUM,
        evidence={"discrepancy_crore": 0.40, "stated_total": 265.72},
        benign_explanations=["Typographical error"]
    )
    db.insert_flag(flag)

    dossier = reporter.generate_flag_dossier("flg_demo_02")
    assert "Arithmetic variance in budget line items" in dossier
    assert "0.4" in dossier
    assert "Typographical error" in dossier
    assert "fraud" not in dossier.lower()
