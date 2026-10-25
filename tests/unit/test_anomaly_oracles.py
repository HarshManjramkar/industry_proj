"""ATDD Test Oracles for Epic 4: Anomaly Detection Engine (Rules R1, R2, R3, R4, R6, R7).
Verifies detection of real-world PMC discrepancies without defamatory language.
"""

import pytest
from pmc_recon.models.entities import TenderRecord, BudgetLine, FlagSeverity, FlagStatus
from pmc_recon.storage.db import DatabaseEngine


def test_story_4_1_rule_r1_mirror_mismatch_oracle(tmp_path):
    """Scenario: Rule R1 detects value discrepancy between official portal and mirror.
    Given official tender at ₹18.50 Cr and mirror listing at ₹19.20 Cr
    When Rule R1 evaluates the pair
    Then an anomaly flag is raised with measured delta and benign explanation checklist.
    """
    from pmc_recon.rules.engine import AnomalyEngine

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    engine = AnomalyEngine(db)

    official = TenderRecord(
        tender_id="PMCP/WTR/2026/042",
        reference_number="PMC-WS-2026-T42",
        title="Laying of trunk water pipeline in Lohegaon Wagholi zone",
        value_inr=185000000.0,
        source_name="mahatenders"
    )
    mirror = {
        "id": "PMCP/WTR/2026/042",
        "tender_value_inr": 192000000.0,
        "source": "publicservicesmap.in"
    }

    flag = engine.evaluate_rule_r1(official, mirror)
    assert flag is not None
    assert flag.rule_id == "R1"
    assert flag.severity == FlagSeverity.MEDIUM
    assert "₹ 70,00,000" in flag.evidence["measured_difference"] or flag.evidence["diff_amount_inr"] == 7000000.0
    assert "Mirror synchronization lag" in flag.benign_explanations


def test_story_4_2_rule_r3_budget_arithmetic_subtotal_oracle(tmp_path):
    """Scenario: Rule R3 catches components vs stated total arithmetic slip.
    Given Electrical department: Capital 80.90 + Revenue 185.22 = 266.12 vs Stated 265.72
    When Rule R3 evaluates subtotal consistency
    Then an anomaly flag is generated with exact difference of 0.40 Crore.
    """
    from pmc_recon.rules.engine import AnomalyEngine

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    engine = AnomalyEngine(db)

    flag = engine.evaluate_rule_r3(
        table_name="Electrical Department Budget 2026-27",
        component_amounts=[80.90, 185.22],
        stated_total=265.72,
        fiscal_year="2026-27"
    )
    assert flag is not None
    assert flag.rule_id == "R3"
    assert round(flag.evidence["discrepancy_crore"], 2) == 0.40
    assert "Typographical error or rounding" in flag.benign_explanations


def test_story_4_3_rule_r6_hampel_filter_outlier_oracle(tmp_path):
    """Scenario: Rule R6 applies Median Absolute Deviation (MAD) to detect pipeline length outlier.
    Given peer group lengths [16.5, 24.0, 32.5, 45.0, 77.0] km and outlier 450.0 km
    When Hampel outlier detector evaluates the series
    Then 450.0 km is flagged with modified z-score > 3.5.
    """
    from pmc_recon.rules.engine import AnomalyEngine

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    engine = AnomalyEngine(db)

    peer_lengths = [16.5, 24.0, 32.5, 45.0, 77.0]
    flag = engine.evaluate_rule_r6(
        entity_name="Lohegaon-Wagholi Water Pipeline",
        metric_name="pipeline_length_km",
        observed_value=450.0,
        peer_distribution=peer_lengths
    )
    assert flag is not None
    assert flag.rule_id == "R6"
    assert flag.evidence["modified_z_score"] > 3.5
    assert flag.severity == FlagSeverity.HIGH
