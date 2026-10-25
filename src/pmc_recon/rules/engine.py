"""Anomaly Detection Engine implementing Rules R1 to R7.
Applies deterministic mathematical checks and robust statistical filters (Hampel/MAD).
Complies with neutral language policies and docs/formal_proofs/mathematical_model.md.
"""

import numpy as np
from typing import Any, Dict, List, Optional
from pmc_recon.models.entities import TenderRecord, Flag, FlagSeverity, FlagStatus
from pmc_recon.storage.db import DatabaseEngine


class AnomalyEngine:
    """Evaluates cross-source data against formal consistency rules."""
    def __init__(self, db: DatabaseEngine):
        self.db = db

    def evaluate_rule_r1(self, official: TenderRecord, mirror: Dict[str, Any], tolerance: float = 0.01) -> Optional[Flag]:
        """Rule R1: Mirror Mismatch detection."""
        mirror_val = float(mirror.get("tender_value_inr", 0.0))
        if official.value_inr <= 0 or mirror_val <= 0:
            return None

        relative_diff = abs(official.value_inr - mirror_val) / official.value_inr
        if relative_diff > tolerance:
            diff_abs = abs(official.value_inr - mirror_val)
            # Threshold: >= 3% relative delta or >= ₹50 Lakh absolute diff is classified as MEDIUM
            is_medium = relative_diff >= 0.03 or diff_abs >= 5_000_000.0
            flag = Flag(
                flag_id=f"flg_r1_{official.tender_id.replace('/', '_')}",
                rule_id="R1",
                title=f"Discrepancy in estimated valuation for tender {official.tender_id}",
                severity=FlagSeverity.MEDIUM if is_medium else FlagSeverity.LOW,
                evidence={
                    "official_source": official.source_name,
                    "official_value_inr": official.value_inr,
                    "mirror_source": mirror.get("source", "mirror"),
                    "mirror_value_inr": mirror_val,
                    "diff_amount_inr": diff_abs,
                    "relative_percentage": round(relative_diff * 100, 2),
                    "measured_difference": f"₹ {diff_abs:,.2f}"
                },
                benign_explanations=[
                    "Mirror synchronization lag",
                    "Mirror derived value from EMD fee ratio",
                    "Rounding difference between crore and rupee expressions"
                ]
            )
            self.db.insert_flag(flag)
            return flag
        return None

    def evaluate_rule_r3(self, table_name: str, component_amounts: List[float], stated_total: float,
                          fiscal_year: str, epsilon: float = 0.01) -> Optional[Flag]:
        """Rule R3: Budget Arithmetic Subtotal Invariant."""
        actual_sum = sum(component_amounts)
        discrepancy = abs(actual_sum - stated_total)

        if discrepancy > epsilon:
            flag = Flag(
                flag_id=f"flg_r3_{fiscal_year}_{abs(hash(table_name)) % 10000}",
                rule_id="R3",
                title=f"Arithmetic subtotal variance identified in {table_name}",
                severity=FlagSeverity.MEDIUM,
                evidence={
                    "table": table_name,
                    "fiscal_year": fiscal_year,
                    "components": component_amounts,
                    "computed_sum": round(actual_sum, 2),
                    "stated_total": stated_total,
                    "discrepancy_crore": round(discrepancy, 2)
                },
                benign_explanations=[
                    "Typographical error or rounding",
                    "OCR or extraction scanning variance",
                    "Differing accounting cutoff dates"
                ]
            )
            self.db.insert_flag(flag)
            return flag
        return None

    def evaluate_rule_r6(self, entity_name: str, metric_name: str, observed_value: float,
                          peer_distribution: List[float], threshold_z: float = 3.5) -> Optional[Flag]:
        """Rule R6: Statistical Outlier Detector via Hampel Filter (Median Absolute Deviation)."""
        data = np.array(peer_distribution)
        median = float(np.median(data))
        mad = float(np.median(np.abs(data - median)))

        # Handle zero MAD case with fallback
        if mad == 0:
            mad = 1e-6

        modified_z = (0.6745 * abs(observed_value - median)) / mad

        if modified_z > threshold_z:
            flag = Flag(
                flag_id=f"flg_r6_{abs(hash(entity_name)) % 10000}",
                rule_id="R6",
                title=f"Statistical outlier identified in {metric_name} for {entity_name}",
                severity=FlagSeverity.HIGH,
                evidence={
                    "entity": entity_name,
                    "metric": metric_name,
                    "observed_value": observed_value,
                    "peer_median": median,
                    "mad": round(mad, 4),
                    "modified_z_score": round(modified_z, 2),
                    "peer_min": float(np.min(data)),
                    "peer_max": float(np.max(data))
                },
                benign_explanations=[
                    "Typographical unit error (e.g. meters entered as kilometers)",
                    "Aggregated multi-zone project entered under a single notice",
                    "Exceptional geographic scope requiring specialized infrastructure"
                ]
            )
            self.db.insert_flag(flag)
            return flag
        return None
