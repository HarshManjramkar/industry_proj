//! Reconciliation rule evaluators adhering to Constitution Article II.

/// Rule R1 mirror evaluator.
pub mod mirror;

/// Rule R3 budget arithmetic evaluator.
pub mod budget;

/// Rule R6 Hampel/MAD filter evaluator.
pub mod hampel;

pub use budget::evaluate_rule_r3;
pub use hampel::evaluate_rule_r6;
pub use mirror::evaluate_rule_r1;
