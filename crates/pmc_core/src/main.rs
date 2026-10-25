//! PMC Procurement Reconciliation Kernel CLI & Executable Entry Point

#![forbid(unsafe_code)]
#![deny(missing_docs, clippy::all, clippy::pedantic)]

use pmc_core::*;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_paise_exact_arithmetic() {
        let p1 = Paise::from_crore(80.90);
        let p2 = Paise::from_crore(185.22);
        let total = Paise::from_crore(265.72);
        let computed = Paise(p1.0 + p2.0);

        // Real worked example from PMC budget: 266.12 vs 265.72 = 0.40 Crore
        let diff = computed.abs_diff(total);
        assert_eq!(diff, Paise::from_crore(0.40));
    }

    #[test]
    fn test_sha256_content_addressing() {
        let payload = b"<html><title>PMC Mahatenders Active</title></html>";
        let addr = ContentAddress::from_bytes(payload);
        assert_eq!(addr.0.len(), 64);
    }

    #[test]
    fn test_neutral_language_invariant() {
        let res = AnomalyFlag::new(
            "flg_1".into(),
            "R1".into(),
            "Suspected fraud in procurement".into(),
            AnomalySeverity::High,
            Paise::ZERO,
            vec!["Testing".into()],
        );
        assert!(res.is_err());
    }

    #[test]
    fn test_type_state_transition_pipeline() {
        let raw = RawTenderNotice {
            raw_id: "RAW_001".into(),
            portal: "mahatenders".into(),
            payload: b"<p>Tender 42 Trunk Line</p>".to_vec(),
        };

        // Transition 1: Verification
        let verified = raw.verify(
            "PMCP/WTR/2026/042".into(),
            "Trunk line Wagholi".into(),
            Paise::from_crore(18.50),
        );
        assert_eq!(verified.content_hash.0.len(), 64);

        // Transition 2: Budget Matching
        let matched = verified.match_budget("RI11A101".into(), 950);
        assert_eq!(matched.budget_code, "RI11A101");

        // Transition 3: Dossier Generation
        let dossier = matched.generate_dossier(vec![]);
        assert!(dossier.uat_ready);
        assert!(dossier.flags.is_empty());
    }

    #[test]
    fn test_rule_r6_hampel_filter() {
        let historical_lengths = vec![16.5, 22.0, 35.0, 48.0, 52.0, 77.0];
        // Lohegaon outlier: 450 km
        let outlier_flag = evaluate_rule_r6("LOHEGAON_PIPE", &historical_lengths, 450.0, 3.0);
        assert!(outlier_flag.is_some());
        let flag = outlier_flag.unwrap();
        assert_eq!(flag.rule_code, "R6");
        assert_eq!(flag.severity, AnomalySeverity::High);

        // In-range value: 40 km
        let normal_flag = evaluate_rule_r6("PASHAN_PIPE", &historical_lengths, 40.0, 3.0);
        assert!(normal_flag.is_none());
    }
}

fn main() {
    println!("PMC Reconciliation Mathematical Kernel v0.1.0");
    println!("Mathematical Formalisms: Separation Logic, Affine Type-States, Discrete Integer Algebra");
}
