"""Track A: Budget lines ingestion and loading engine.
Loads Accounts budget lines keyed by budget_head_code (e.g. RI11A101).
"""

from typing import Any, Dict, List
from pmc_recon.models.entities import BudgetLine, BudgetLineType
from pmc_recon.storage.interfaces import BudgetRepository


class BudgetLoader:
    """Single Responsibility: Ingest and map tabular budget lines."""
    def __init__(self, repository: BudgetRepository):
        self.repository = repository

    def load_budget_rows(self, rows: List[Dict[str, Any]]) -> int:
        """Parse structured budget rows and persist via repository."""
        loaded = 0
        for r in rows:
            if "actual_amount_crore" in r and r["actual_amount_crore"] is not None:
                actual_line = BudgetLine(
                    budget_head_code=r["budget_head_code"],
                    description_marathi=r["description_marathi"],
                    description_english=r.get("description_english", ""),
                    department=r.get("department", "Water Supply"),
                    fiscal_year=r["fiscal_year"],
                    amount_type=BudgetLineType.ACTUAL,
                    amount_inr_crore=float(r["actual_amount_crore"]),
                    source_file=r.get("source_file", "unknown")
                )
                self.repository.insert_budget_line(actual_line)
                loaded += 1

            if "estimate_amount_crore" in r and r["estimate_amount_crore"] is not None:
                estimate_line = BudgetLine(
                    budget_head_code=r["budget_head_code"],
                    description_marathi=r["description_marathi"],
                    description_english=r.get("description_english", ""),
                    department=r.get("department", "Water Supply"),
                    fiscal_year=r["fiscal_year"],
                    amount_type=BudgetLineType.ESTIMATE,
                    amount_inr_crore=float(r["estimate_amount_crore"]),
                    source_file=r.get("source_file", "unknown")
                )
                self.repository.insert_budget_line(estimate_line)
        return loaded
