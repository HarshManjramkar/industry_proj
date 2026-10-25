//! Rule R1: Cross-Source Mirror Mismatch Evaluator.

use crate::anomaly::{AnomalyFlag, AnomalySeverity};
use crate::currency::Paise;
use crate::typestate::VerifiedNotice;

/// Evaluates Rule R1: Cross-Source Mirror Mismatch between official and mirrored notices.
#[must_use]
pub fn evaluate_rule_r1(official: &VerifiedNotice, mirror_value: Paise) -> Option<AnomalyFlag> {
    let diff = official.estimated_value.abs_diff(mirror_value);
    let tolerance_paise = official.estimated_value.0 / 100;

    if diff.0 > tolerance_paise {
        let is_medium = diff.0 > (official.estimated_value.0 * 3) / 100;
        AnomalyFlag::new(
            format!("flg_r1_{}", official.tender_id.replace('/', "_")),
            "R1".to_string(),
            format!("Valuation variance detected for tender {}", official.tender_id),
            if is_medium { AnomalySeverity::Medium } else { AnomalySeverity::Low },
            diff,
            vec![
                "Mirror synchronization lag".to_string(),
                "Derived EMD fee calculation discrepancy".to_string(),
                "Rounding variance between crore and paise expressions".to_string(),
            ],
        )
        .ok()
    } else {
        None
    }
}
