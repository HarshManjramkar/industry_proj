"""Track B: Mahatenders and mirror portals ingestion adapter.
Parses tender notices, saves immutable raw payloads, and yields standardized TenderRecord entities.
"""

from typing import List
from bs4 import BeautifulSoup
from pmc_recon.models.entities import TenderRecord, TenderStatus
from pmc_recon.ingest.normalizer import parse_inr_value, parse_iso_date
from pmc_recon.storage.interfaces import RawDocumentStore, TenderRepository


class MahatendersAdapter:
    """Single Responsibility: Parse Mahatenders HTML format and decouple persistence."""
    def __init__(self, raw_store: RawDocumentStore, repository: TenderRepository):
        self.raw_store = raw_store
        self.repository = repository

    def ingest_html(self, run_id: str, html_content: str) -> List[TenderRecord]:
        """Save raw HTML document and extract Water Supply tenders."""
        raw_doc = self.raw_store.save_raw_payload(
            run_id=run_id,
            payload_bytes=html_content.encode("utf-8"),
            filename_prefix="mahatenders_active"
        )
        return self._extract_tenders(html_content, raw_doc.doc_id)

    def _extract_tenders(self, html_content: str, raw_doc_id: str) -> List[TenderRecord]:
        """Focused parsing method keeping abstraction levels clean."""
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table", {"id": "activeTendersTable"}) or soup.find("table")
        if not table:
            return []

        tenders: List[TenderRecord] = []
        for row in table.find_all("tr")[1:]:
            cols = [td.get_text(strip=True) for td in row.find_all("td")]
            if len(cols) < 6:
                continue

            corrigenda_count = int(cols[6]) if len(cols) > 6 and cols[6].isdigit() else 0
            tender = TenderRecord(
                tender_id=cols[0],
                reference_number=cols[1],
                title=cols[2],
                department_chain=cols[3],
                closing_date=parse_iso_date(cols[4]),
                value_inr=parse_inr_value(cols[5]),
                status=TenderStatus.ACTIVE,
                corrigenda_count=corrigenda_count,
                source_name="mahatenders",
                raw_doc_id=raw_doc_id
            )
            self.repository.upsert_tender(tender)
            tenders.append(tender)

        return tenders
