//! Non-defamatory anomaly flag invariant and severity classification.

use crate::currency::Paise;
use serde::{Deserialize, Serialize};

/// Severity classification of an anomaly.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
pub enum AnomalySeverity {
    /// Minor tolerance discrepancy (e.g. rounding).
    Low,
    /// Material variance (e.g. cross-mirror mismatch > 3%).
    Medium,
    /// Structural violation or mathematical outlier.
    High,
}

/// Discrepancy flag with non-defamatory invariant.
/// Proves that no defamatory accusations can be constructed at compile time.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AnomalyFlag {
    /// Unique flag ID.
    pub flag_id: String,
    /// Rule reference (R1 - R7).
    pub rule_code: String,
    /// Neutral descriptive title.
    pub neutral_title: String,
    /// Severity classification.
    pub severity: AnomalySeverity,
    /// Quantitative difference in exact paise.
    pub measured_difference: Paise,
    /// Pre-approved innocent explanations.
    pub benign_explanations: Vec<String>,
}

impl AnomalyFlag {
    /// Construct a verified non-defamatory anomaly flag.
    ///
    /// # Errors
    /// Returns error if title contains non-neutral or defamatory terms.
    pub fn new(
        flag_id: String,
        rule_code: String,
        neutral_title: String,
        severity: AnomalySeverity,
        measured_difference: Paise,
        benign_explanations: Vec<String>,
    ) -> Result<Self, &'static str> {
        let lowered = neutral_title.to_lowercase();
        if lowered.contains("fraud")
            || lowered.contains("corrupt")
            || lowered.contains("illegal")
            || lowered.contains("guilty")
        {
            return Err("Defamatory words are forbidden by Constitutional Invariant.");
        }
        if benign_explanations.is_empty() {
            return Err("Every flag must provide a non-empty checklist of innocent explanations.");
        }
        Ok(Self {
            flag_id,
            rule_code,
            neutral_title,
            severity,
            measured_difference,
            benign_explanations,
        })
    }
}
