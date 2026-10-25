"""ATDD failing test oracles for Story 2.1 (Budget Ingest) and Story 2.2 (Tender Ingest).
Enforces Prime Directive: Test oracles defined BEFORE implementation.
"""

import pytest
from tests.fixtures.mock_data import MOCK_BUDGET_ROWS, MOCK_MAHATENDERS_HTML, MOCK_MIRROR_PAYLOAD
from pmc_recon.storage.db import DatabaseEngine


def test_story_2_1_budget_loader_oracle(tmp_path):
    """Scenario: Ingest Accounts budget lines and verify extraction against PRD acceptance criteria.
    Given raw budget row data containing RI11A101
    When budget ingestion is executed
    Then row RI11A101 is accurately stored with its Marathi description and actual amount.
    """
    from pmc_recon.ingest.budget_loader import BudgetLoader

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    loader = BudgetLoader(db)
    
    loaded_count = loader.load_budget_rows(MOCK_BUDGET_ROWS)
    assert loaded_count == len(MOCK_BUDGET_ROWS)

    # Verify query
    with db._get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM budget_lines WHERE budget_head_code = 'RI11A101' AND amount_type = 'actual'"
        ).fetchone()
        assert row is not None
        assert row["amount_inr_crore"] == 42.50
        assert "वाघोली" in row["description_marathi"]
        assert row["department"] == "Water Supply"


def test_story_2_2_mahatenders_adapter_oracle(tmp_path):
    """Scenario: Parse Mahatenders HTML and store standardized TenderRecord entities.
    Given raw HTML from Mahatenders containing water supply tenders
    When HTML scraper parses the payload
    Then tender PMCP/WTR/2026/042 is saved with parsed INR value and raw document hash.
    """
    from pmc_recon.ingest.tender_adapter import MahatendersAdapter

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    adapter = MahatendersAdapter(raw_store=db, repository=db)

    tenders = adapter.ingest_html(run_id="run_test_01", html_content=MOCK_MAHATENDERS_HTML)
    assert len(tenders) == 2
    
    t1 = next(t for t in tenders if t.tender_id == "PMCP/WTR/2026/042")
    assert t1.value_inr == 185000000.0  # 18.5 Cr parsed from ₹ 18,50,00,000
    assert str(t1.closing_date) == "2026-11-15"
    assert t1.source_name == "mahatenders"
    assert t1.raw_doc_id is not None


def test_story_2_3_rupee_string_normalizer_oracle():
    """Scenario: Parse varied Indian currency notation formats deterministically.
    Given inputs like '₹ 18,50,00,000', '18.50 Cr', '425 Lakh'
    When normalized to float INR
    Then all parse to exact numeric values without floating point drift.
    """
    from pmc_recon.ingest.normalizer import parse_inr_value

    assert parse_inr_value("₹ 18,50,00,000") == 185000000.0
    assert parse_inr_value("18.50 crore") == 185000000.0
    assert parse_inr_value("425 lakh") == 42500000.0
    assert parse_inr_value("Rs. 50,000") == 50000.0
