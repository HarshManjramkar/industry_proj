"""Abstract storage protocols for PMC Reconciliation.
Enforces Interface Segregation (ISP) and Dependency Inversion (DIP).
"""

from typing import Protocol, Optional
from pmc_recon.models.entities import RawDocument, TenderRecord, BudgetLine, ChangeEvent, Flag, ReviewDecision


class RawDocumentStore(Protocol):
    """Protocol for immutable raw document persistence."""
    def save_raw_payload(self, run_id: str, payload_bytes: bytes, filename_prefix: str = "payload") -> RawDocument:
        ...


class TenderRepository(Protocol):
    """Protocol for tender entity persistence and change tracking."""
    def upsert_tender(self, tender: TenderRecord) -> Optional[ChangeEvent]:
        ...


class BudgetRepository(Protocol):
    """Protocol for budget line records persistence."""
    def insert_budget_line(self, line: BudgetLine) -> None:
        ...


class FlagRepository(Protocol):
    """Protocol for anomaly flags and review audit trails."""
    def insert_flag(self, flag: Flag) -> None:
        ...
    def record_review(self, review: ReviewDecision) -> None:
        ...
