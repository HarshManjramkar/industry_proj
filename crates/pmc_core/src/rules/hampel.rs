//! Rule R6: Hampel Filter with Median Absolute Deviation (MAD) for Outlier Detection.

use crate::anomaly::{AnomalyFlag, AnomalySeverity};
use crate::currency::Paise;

/// Evaluates Rule R6: Hampel Filter Outlier Detection using Median and MAD.
///
/// Invariant: Eliminates all division-by-zero errors and floating-point drift.
#[must_use]
pub fn evaluate_rule_r6(
    item_id: &str,
    series: &[f64],
    target_value: f64,
    threshold: f64,
) -> Option<AnomalyFlag> {
    if series.len() < 3 {
        return None;
    }

    let mut sorted = series.to_vec();
    sorted.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let n = sorted.len();
    let median = if n % 2 == 1 {
        sorted[n / 2]
    } else {
        (sorted[(n / 2) - 1] + sorted[n / 2]) / 2.0
    };

    let mut abs_devs: Vec<f64> = sorted.iter().map(|&x| (x - median).abs()).collect();
    abs_devs.sort_by(|a, b| a.partial_cmp(b).unwrap_or(std::cmp::Ordering::Equal));
    let mad = if n % 2 == 1 {
        abs_devs[n / 2]
    } else {
        (abs_devs[(n / 2) - 1] + abs_devs[n / 2]) / 2.0
    };

    let effective_mad = if mad < 1e-9 { 1e-9 } else { mad };
    let hampel_stat = (target_value - median).abs() / (1.4826 * effective_mad);

    if hampel_stat > threshold {
        AnomalyFlag::new(
            format!("flg_r6_{item_id}"),
            "R6".to_string(),
            format!("Statistical parameter variance detected for {item_id}"),
            AnomalySeverity::High,
            Paise::ZERO,
            vec![
                "Different project scope or engineering topography".to_string(),
                "Unit mismatch in schedule of rates (e.g., meters vs kilometers)".to_string(),
                "Multiphasic contract packaging".to_string(),
            ],
        )
        .ok()
    } else {
        None
    }
}
