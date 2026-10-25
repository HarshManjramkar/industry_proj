//! Rule R3: Budget Arithmetic Totality Invariant.

use crate::anomaly::{AnomalyFlag, AnomalySeverity};
use crate::currency::Paise;

/// Evaluates Rule R3: Budget Arithmetic Invariant.
/// Verifies sum(components) == stated_total within discrete integer arithmetic.
#[must_use]
pub fn evaluate_rule_r3(
    table_id: &str,
    components: &[Paise],
    stated_total: Paise,
) -> Option<AnomalyFlag> {
    let computed_sum: i64 = components.iter().map(|p| p.0).sum();
    let discrepancy = (computed_sum - stated_total.0).abs();

    if discrepancy > 0 {
        AnomalyFlag::new(
            format!("flg_r3_{table_id}"),
            "R3".to_string(),
            format!("Arithmetic subtotal variance identified in {table_id}"),
            AnomalySeverity::Medium,
            Paise(discrepancy),
            vec![
                "Typographical entry slip in municipal budget book".to_string(),
                "Audit timing cut-off variation across departments".to_string(),
            ],
        )
        .ok()
    } else {
        None
    }
}
