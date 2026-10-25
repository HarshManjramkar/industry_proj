//! PMC Procurement Reconciliation Mathematical Kernel
//!
//! Formally verified mathematical invariants:
//! 1. Complete type safety & algebraic state machines (Zero undefined behavior, #![forbid(unsafe_code)]).
//! 2. Type-State Pattern: Enforces compile-time transition order (RawNotice -> VerifiedNotice -> MatchedTender -> ReconciliationDossier).
//! 3. Fixed-point discrete currency arithmetic (Zero IEEE-754 floating-point drift: 1 INR = 100 Paise).
//! 4. Cryptographic SHA-256 pre-image binding.
//! 5. Non-defamatory flag type invariant (Impossible states are unrepresentable).
//! 6. Robust Hampel Filter with Median Absolute Deviation (MAD) for outlier detection.

#![forbid(unsafe_code)]
#![deny(missing_docs, clippy::all, clippy::pedantic)]

/// Discrete currency arithmetic eliminating floating-point drift.
pub mod currency;

/// Cryptographic SHA-256 pre-image binding.
pub mod crypto;

/// Non-defamatory anomaly classification and guarantees.
pub mod anomaly;

/// Affine type-state machine enforcing pipeline sequence.
pub mod typestate;

/// Individual verification rule engines.
pub mod rules;

// Convenient top-level re-exports
pub use anomaly::{AnomalyFlag, AnomalySeverity};
pub use crypto::ContentAddress;
pub use currency::Paise;
pub use rules::{evaluate_rule_r1, evaluate_rule_r3, evaluate_rule_r6};
pub use typestate::{MatchedTender, RawTenderNotice, ReconciliationDossier, VerifiedNotice};
