"""ATDD Test Oracle for Webapp Live Crawler Demo Service (Story 5.4).
Enforces Prime Directive: Verification layer and test oracles exist BEFORE implementation.
"""

import pytest
from unittest.mock import MagicMock
from pmc_recon.storage.db import DatabaseEngine


def test_story_5_4_live_crawler_service_execution_oracle(tmp_path):
    """Scenario: Webapp initiates a live polite crawl without terminal access.
    Given a target portal URL
    When CrawlerDemoService triggers the polite crawl
    Then the payload is captured, hashed with SHA-256, and metadata returned for UI display.
    """
    from pmc_recon.ingest.crawler_service import CrawlerDemoService

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    service = CrawlerDemoService(db=db, request_interval_sec=0.01)

    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html><head><title>Mahatenders Demo</title></head><body>Active Tenders Table</body></html>"
    mock_response.text = "<html><head><title>Mahatenders Demo</title></head><body>Active Tenders Table</body></html>"
    mock_response.headers = {"ETag": '"etag_live_demo_123"'}
    mock_session.get.return_value = mock_response

    result = service.run_live_crawl(
        url="https://mahatenders.gov.in/nicgep/app?page=FrontEndLatestActiveTenders&service=page",
        run_id="ui_demo_test",
        session=mock_session
    )

    assert result is not None
    assert result.status_code == 200
    assert result.doc_id.startswith("doc_")
    assert len(result.content_hash) == 64
    assert result.etag == '"etag_live_demo_123"'
    assert "PMCProcurementReconciliationBot" in result.user_agent
    assert "Mahatenders Demo" in result.payload_preview


def test_story_5_4_cryptographic_preimage_integrity_oracle(tmp_path):
    """Scenario: UI verifies Theorem 1 mathematical proof on disk.
    Given a stored raw document payload
    When verify_disk_lineage is invoked for the doc_id
    Then the SHA-256 hash of the binary file on disk exactly matches the database content_hash.
    """
    from pmc_recon.ingest.crawler_service import CrawlerDemoService

    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    service = CrawlerDemoService(db=db)

    # Save a known raw payload
    test_bytes = b"Tamper-proof government record verification payload"
    raw_doc = db.save_raw_payload(run_id="test_run", payload_bytes=test_bytes, filename_prefix="gov_portal")

    verification = service.verify_disk_lineage(raw_doc.doc_id)

    assert verification["verified"] is True
    assert verification["computed_hash"] == raw_doc.content_hash
    assert verification["stored_hash"] == raw_doc.content_hash
    assert verification["size_bytes"] == len(test_bytes)
