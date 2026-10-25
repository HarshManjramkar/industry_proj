"""Data Models and Contracts for In-Flight Table Integrity and Invariant Evaluation.
Strictly under 350 lines and compliant with neutral language policies.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator
from pmc_recon.models.entities import FlagSeverity


class TableDiscrepancyType(str, Enum):
    TOTALITY_MISMATCH = "totality_mismatch"
    CHRONOLOGY_INVERSION = "chronology_inversion"
    STATISTICAL_OUTLIER = "statistical_outlier"
    DUPLICATE_NOTICE_CONFLICT = "duplicate_notice_conflict"


class TableDiscrepancyItem(BaseModel):
    """Deterministic discrepancy item flagged during in-flight table inspection."""
    discrepancy_type: TableDiscrepancyType
    rule_id: str = Field(..., description="Rule code e.g. R3-Table, R6-Table, R-Chronology")
    title: str = Field(..., description="Non-defamatory summary of variance")
    row_identifier: str = Field(..., description="Tender ID, sector name, or row index")
    measured_values: Dict[str, Any] = Field(default_factory=dict)
    delta: Optional[float] = None
    severity: FlagSeverity = FlagSeverity.LOW
    benign_explanation: str = Field(..., description="Innocent administrative or scanning reason")

    @field_validator("title", "benign_explanation")
    @classmethod
    def validate_neutral_language(cls, v: str) -> str:
        lowered = v.lower()
        for forbidden in ["fraud", "corruption", "scam", "illegal", "criminal", "guilty"]:
            if forbidden in lowered:
                raise ValueError(f"Language must remain neutral; prohibited word found: {forbidden}")
        return v


class TableValidationReport(BaseModel):
    """Complete in-flight audit report of a scanned public table."""
    table_id: str
    total_rows_inspected: int
    columns_inspected: List[str]
    discrepancies: List[TableDiscrepancyItem] = Field(default_factory=list)
    passed_invariants: List[str] = Field(default_factory=list)
    execution_time_ms: float
    tamper_hash: str
