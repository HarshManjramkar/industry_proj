"""Strict Pydantic Data Models and Contracts for PMC Procurement Reconciliation.
Complies with Article II of Project Constitution and Harsh Manjramkar Flow.
"""

from datetime import datetime, date, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


def current_utc_datetime() -> datetime:
    """Return timezone-aware current UTC datetime."""
    return datetime.now(timezone.utc)


class AccessMethod(str, Enum):
    MANUAL_DOWNLOAD = "manual_download"
    BULK_API = "bulk_api"
    HTML_SCRAPING = "html_scraping"


class TermsStatus(str, Enum):
    PERMITTED = "permitted"
    CONDITIONAL = "conditional"
    RESTRICTED = "restricted"
    PENDING_CHECK = "pending_check"


class Source(BaseModel):
    """Source registry entity representing a portal or publication channel."""
    source_id: str = Field(..., description="Unique alphanumeric source identifier (e.g., 'src_mahatenders')")
    name: str = Field(..., description="Human-readable name of the source")
    base_url: str = Field(..., description="Base URL of portal or data source")
    owner_dept: str = Field(..., description="Owning agency or department (e.g. PMC Accounts, NIC)")
    access_method: AccessMethod = Field(..., description="Access technique")
    terms_status: TermsStatus = Field(default=TermsStatus.PENDING_CHECK, description="Checked robots/terms status")
    crawl_frequency: str = Field(default="weekly", description="Frequency: daily, weekly, yearly")


class Dataset(BaseModel):
    """Specific dataset or collection within a source."""
    dataset_id: str = Field(..., description="Unique dataset identifier (e.g., 'ds_water_supply_tenders')")
    source_id: str = Field(..., description="Foreign key to source")
    title: str = Field(..., description="Dataset title")
    url: str = Field(..., description="Endpoint or download URL")
    format: str = Field(..., description="File format: html, xlsx, pdf, json")
    update_frequency: str = Field(default="weekly")
    schema_version: str = Field(default="1.0.0")


class RawDocument(BaseModel):
    """Immutable raw document payload saved with cryptographic hash."""
    doc_id: str = Field(..., description="Unique document ID (doc_<hash[:12]>)")
    run_id: str = Field(..., description="Associated ingest run ID")
    storage_path: str = Field(..., description="Relative filesystem storage path")
    content_hash: str = Field(..., min_length=64, max_length=64, description="SHA-256 hash of payload")
    size_bytes: int = Field(..., ge=0)
    fetched_at: datetime = Field(default_factory=current_utc_datetime)


class TenderStatus(str, Enum):
    ACTIVE = "active"
    CORRIGENDUM = "corrigendum"
    CLOSED = "closed"
    RESULTS_PENDING = "results_pending"
    AWARDED = "awarded"
    CANCELLED = "cancelled"


class TenderRecord(BaseModel):
    """Cleaned, standardized Tender entity from Mahatenders or mirror."""
    tender_id: str = Field(..., description="Standardized tender ID (e.g., PMCP/WTR/2026/042)")
    reference_number: str = Field(..., description="Official tender notice reference number")
    title: str = Field(..., min_length=3, description="Descriptive work title")
    department_chain: str = Field(default="Pune Municipal Corporation/Water Supply", description="Department hierarchy")
    published_date: Optional[date] = None
    closing_date: Optional[date] = None
    opening_date: Optional[date] = None
    value_inr: float = Field(..., ge=0.0, description="Estimated work value in INR")
    fee_inr: Optional[float] = Field(default=0.0, ge=0.0)
    emd_inr: Optional[float] = Field(default=0.0, ge=0.0)
    status: TenderStatus = Field(default=TenderStatus.ACTIVE)
    corrigenda_count: int = Field(default=0, ge=0)
    source_name: str = Field(..., description="Portal where observed: 'mahatenders' or mirror")
    raw_doc_id: Optional[str] = None


class BudgetLineType(str, Enum):
    ACTUAL = "actual"
    ESTIMATE = "estimate"
    REVISED = "revised"


class BudgetLine(BaseModel):
    """Normalized budget line from Accounts budget book/presentation."""
    budget_head_code: str = Field(..., min_length=4, description="Standard budget code, e.g. RI11A101")
    description_marathi: str = Field(..., description="Original description in Marathi")
    description_english: Optional[str] = Field(default="", description="Transliterated/translated description")
    department: str = Field(default="Water Supply", description="Associated department")
    fiscal_year: str = Field(..., pattern=r"^\d{4}-\d{2,4}$", description="Fiscal year string, e.g. '2025-26'")
    amount_type: BudgetLineType = Field(default=BudgetLineType.ACTUAL)
    amount_inr_crore: float = Field(..., ge=0.0, description="Amount in INR Crore")
    source_file: str = Field(..., description="Source file reference")


class ChangeType(str, Enum):
    NEW = "new"
    MODIFIED = "modified"
    REMOVED = "removed"


class ChangeEvent(BaseModel):
    """Detected difference between consecutive observations of a record."""
    change_id: str = Field(..., description="Unique event identifier")
    record_id: str = Field(..., description="Logical record key")
    record_type: str = Field(..., description="'tender' or 'budget_line'")
    change_type: ChangeType
    changed_fields: Dict[str, Any] = Field(default_factory=dict, description="Key -> {old_val, new_val}")
    detected_at: datetime = Field(default_factory=current_utc_datetime)


class EntityLinkStatus(str, Enum):
    AUTOMATIC = "automatic"
    REVIEW_REQUIRED = "review_required"
    CONFIRMED = "confirmed"
    REJECTED = "rejected"


class EntityLink(BaseModel):
    """Link established between cross-source records (e.g. Tender to Budget Line)."""
    link_id: str = Field(..., description="Unique link identifier")
    left_record_id: str = Field(..., description="e.g. tender_id")
    right_record_id: str = Field(..., description="e.g. budget_head_code or village")
    method: str = Field(..., description="exact_id, composite_key, or rapidfuzz_token")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Match confidence score [0.0 - 1.0]")
    status: EntityLinkStatus = Field(default=EntityLinkStatus.AUTOMATIC)


class FlagSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class FlagStatus(str, Enum):
    OPEN = "open"
    CONFIRMED_ISSUE = "confirmed_issue"
    EXPLAINED = "explained"
    FALSE_POSITIVE = "false_positive"


class Flag(BaseModel):
    """Anomaly flag raised by rules R1-R7."""
    flag_id: str = Field(..., description="Unique flag identifier (e.g. flg_r1_1024)")
    rule_id: str = Field(..., description="R1, R2, R3, R4, R5, R6, or R7")
    title: str = Field(..., description="Neutral statement of inconsistency")
    severity: FlagSeverity
    evidence: Dict[str, Any] = Field(..., description="Deterministic numbers, documents, diff traces")
    benign_explanations: List[str] = Field(..., min_length=1, description="List of innocent explanations to check")
    status: FlagStatus = Field(default=FlagStatus.OPEN)
    created_at: datetime = Field(default_factory=current_utc_datetime)

    @field_validator("title")
    @classmethod
    def validate_neutral_language(cls, v: str) -> str:
        lowered = v.lower()
        if "fraud" in lowered or "corruption" in lowered or "illegal" in lowered or "guilty" in lowered:
            raise ValueError("Flag title must adhere to neutral language policy (Article IV of Constitution).")
        return v


class ReviewDecision(BaseModel):
    """Human review decision logged by the single human in the loop."""
    review_id: str = Field(...)
    flag_id: str = Field(...)
    reviewer: str = Field(default="Client Reviewer", description="Human reviewer name")
    outcome: FlagStatus = Field(...)
    comment: str = Field(..., min_length=3, description="Review commentary explaining the decision")
    reviewed_at: datetime = Field(default_factory=current_utc_datetime)
