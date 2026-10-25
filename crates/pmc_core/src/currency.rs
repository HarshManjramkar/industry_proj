//! Discrete monetary representation in Indian Paise (1 INR = 100 Paise).
//! Eliminates floating-point rounding inaccuracies entirely.

use serde::{Deserialize, Serialize};
use std::fmt;

/// Discrete monetary representation in Indian Paise (1 INR = 100 Paise).
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash, Serialize, Deserialize)]
pub struct Paise(pub i64);

impl Paise {
    /// Zero paise.
    pub const ZERO: Self = Self(0);

    /// Construct from Rupees integer.
    #[must_use]
    pub const fn from_inr(rupees: i64) -> Self {
        Self(rupees * 100)
    }

    /// Construct from Crore (1 Crore = 10,000,000 INR = 1,000,000,000 Paise).
    #[must_use]
    pub fn from_crore(crore: f64) -> Self {
        #[allow(clippy::cast_possible_truncation)]
        Self((crore * 1_000_000_000.0).round() as i64)
    }

    /// Construct from Lakh (1 Lakh = 100,000 INR = 10,000,000 Paise).
    #[must_use]
    pub fn from_lakh(lakh: f64) -> Self {
        #[allow(clippy::cast_possible_truncation)]
        Self((lakh * 10_000_000.0).round() as i64)
    }

    /// Returns absolute difference.
    #[must_use]
    pub const fn abs_diff(self, other: Self) -> Self {
        Self(self.0.abs_diff(other.0) as i64)
    }
}

impl fmt::Display for Paise {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        let rupees = self.0 / 100;
        let paise = (self.0 % 100).abs();
        write!(f, "INR {rupees}.{paise:02}")
    }
}
