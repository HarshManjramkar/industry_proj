"""Cross-Dataset Entity Linking Engine.
Implements Tier 1 Exact ID matching and Tier 3 Levenshtein Metric Token Sort matching.
Adheres to SOLID principles and docs/formal_proofs/mathematical_model.md.
"""

from typing import Optional
from rapidfuzz import fuzz
from pmc_recon.models.entities import TenderRecord, BudgetLine, EntityLink, EntityLinkStatus
from pmc_recon.storage.db import DatabaseEngine


class EntityMatcher:
    """Calculates cross-dataset links and stores verified relationships."""
    def __init__(self, db: DatabaseEngine, threshold: float = 0.80):
        self.db = db
        self.threshold = threshold

    def match_mirror_tender(self, official_id: str, mirror_id: str, mirror_source: str) -> Optional[EntityLink]:
        """Tier 1: Normalized Exact ID matching across portal and mirror."""
        norm_official = official_id.strip().upper()
        norm_mirror = mirror_id.strip().upper()

        if norm_official == norm_mirror:
            link = EntityLink(
                link_id=f"lnk_{norm_official}_{mirror_source[:4]}",
                left_record_id=official_id,
                right_record_id=mirror_id,
                method="exact_id",
                confidence=1.0,
                status=EntityLinkStatus.AUTOMATIC
            )
            self._save_link(link)
            return link
        return None

    def link_tender_to_budget(self, tender: TenderRecord, line: BudgetLine) -> Optional[EntityLink]:
        """Tier 3: Fuzzy token similarity matching tender title with budget descriptions.
        Calculates max similarity across Marathi and English descriptions.
        """
        sim_en = fuzz.token_set_ratio(tender.title, line.description_english) / 100.0 if line.description_english else 0.0
        sim_mr = fuzz.token_set_ratio(tender.title, line.description_marathi) / 100.0 if line.description_marathi else 0.0
        similarity_ratio = max(sim_en, sim_mr)

        if similarity_ratio >= self.threshold:
            status = EntityLinkStatus.AUTOMATIC
        elif similarity_ratio >= 0.50:
            status = EntityLinkStatus.REVIEW_REQUIRED
        else:
            return None

        link = EntityLink(
            link_id=f"lnk_tb_{tender.tender_id}_{line.budget_head_code}",
            left_record_id=tender.tender_id,
            right_record_id=line.budget_head_code,
            method="rapidfuzz_token_set",
            confidence=round(similarity_ratio, 3),
            status=status
        )
        self._save_link(link)
        return link

    def _save_link(self, link: EntityLink) -> None:
        """Persist link record into the database."""
        with self.db._get_connection() as conn:
            conn.execute("""
            INSERT OR REPLACE INTO entity_links (link_id, left_record_id, right_record_id, method, confidence, status)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (link.link_id, link.left_record_id, link.right_record_id, link.method, link.confidence, link.status.value))
