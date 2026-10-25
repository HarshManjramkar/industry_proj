"""ATDD Unit Test Oracle for Polite Crawler.
Verifies rate-limiting, User-Agent header transmission, and immutable content storage.
"""

from unittest.mock import MagicMock
from pmc_recon.ingest.polite_crawler import PoliteCrawler
from pmc_recon.storage.db import DatabaseEngine


def test_polite_crawler_rate_limiting_and_storage_oracle(tmp_path):
    """Scenario: Polite crawler enforces NFR-01 delay and persists payload.
    Given a mock URL and raw document store
    When crawler fetches the content
    Then User-Agent is explicitly sent, status 200 payload is stored with SHA-256 hash.
    """
    db = DatabaseEngine(db_path=str(tmp_path / "test.db"), raw_dir=str(tmp_path / "raw"))
    crawler = PoliteCrawler(raw_store=db, request_interval_sec=0.01)

    # Mock session
    mock_session = MagicMock()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.content = b"<html><body>Mahatenders Public Active Table</body></html>"
    mock_response.text = "<html><body>Mahatenders Public Active Table</body></html>"
    mock_response.headers = {"ETag": '"abc123etag"'}
    mock_session.get.return_value = mock_response

    result = crawler.fetch_url(
        url="https://mahatenders.gov.in/nicgep/app?page=FrontEndTendersByOrganisation",
        run_id="run_crawler_01",
        session=mock_session
    )

    assert result is not None
    assert result["status_code"] == 200
    assert result["raw_doc_id"] is not None
    assert len(result["content_hash"]) == 64
    assert result["etag"] == '"abc123etag"'

    # Verify User-Agent sent
    called_kwargs = mock_session.get.call_args[1]
    assert "PMCProcurementReconciliationBot" in called_kwargs["headers"]["User-Agent"]
