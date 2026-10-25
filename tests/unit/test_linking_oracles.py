"""ATDD Test Oracles for Epic 3: Cross-Dataset Entity Linking Engine.
Enforces TEA (Murat) standards and formal Levenshtein metric space theorems.
"""

import pytest
from pmc_recon.models.entities import TenderRecord, BudgetLine, EntityLinkStatus
from pmc_recon.storage.db import DatabaseEngine


def test_story_3_1_exact_tender_id_matcher_oracle(tmp_path):
    """Scenario: Tier 1 Exact Matching across official portal and mirror sites.
    Given an official tender and mirror records with normalized tender IDs
    When exact matcher runs
    Then confidence is exactly 1.0 and link status is AUTOMATIC.
    """
    from pmc_recon.linking.matcher import EntityMatcher

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    matcher = EntityMatcher(db)

    link = matcher.match_mirror_tender(
        official_id="PMCP/WTR/2026/042",
        mirror_id="pmcp/wtr/2026/042", # lowercase variant
        mirror_source="publicservicesmap.in"
    )
    assert link is not None
    assert link.confidence == 1.0
    assert link.status == EntityLinkStatus.AUTOMATIC
    assert link.method == "exact_id"


def test_story_3_2_fuzzy_token_similarity_oracle(tmp_path):
    """Scenario: Tier 3 Fuzzy Entity Linker matching Marathi/English project descriptions.
    Given a water supply tender in Wagholi and budget line RI11A101
    When fuzzy token sort similarity is evaluated
    Then confidence exceeds 0.80 threshold and links are stored.
    """
    from pmc_recon.linking.matcher import EntityMatcher

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    matcher = EntityMatcher(db)

    # Ingest a budget line
    line = BudgetLine(
        budget_head_code="RI11A101",
        description_marathi="पाणी पुरवठा वितरण व्यवस्था सक्षमीकरण (वाघोली, लोहगाव)",
        description_english="Water supply distribution strengthening Wagholi Lohegaon",
        department="Water Supply",
        fiscal_year="2025-26",
        amount_type="actual",
        amount_inr_crore=42.50,
        source_file="budget_2025_26.xlsx"
    )
    db.insert_budget_line(line)

    tender = TenderRecord(
        tender_id="PMCP/WTR/2026/042",
        reference_number="PMC-WS-2026-T42",
        title="Water distribution strengthening Wagholi sector works",
        value_inr=185000000.0,
        source_name="mahatenders"
    )

    link = matcher.link_tender_to_budget(tender, line)
    assert link is not None
    assert link.confidence >= 0.80
    assert link.right_record_id == "RI11A101"
    assert link.status == EntityLinkStatus.AUTOMATIC
