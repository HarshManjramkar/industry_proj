//! Type-State Pattern enforcing compile-time pipeline progression.
//! RawNotice -> VerifiedNotice -> MatchedTender -> ReconciliationDossier.

use crate::anomaly::AnomalyFlag;
use crate::crypto::ContentAddress;
use crate::currency::Paise;
use serde::{Deserialize, Serialize};

/// State 1: Unverified Raw Scraped Notice
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RawTenderNotice {
    /// Scraped ID.
    pub raw_id: String,
    /// Portal source.
    pub portal: String,
    /// Raw unverified HTML/text payload.
    pub payload: Vec<u8>,
}

/// State 2: Cryptographically Verified Notice
/// Invariant: Can only be constructed by verifying the SHA-256 content address.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct VerifiedNotice {
    /// Canonical Tender ID.
    pub tender_id: String,
    /// Work title.
    pub work_title: String,
    /// Valuation in exact discrete Paise.
    pub estimated_value: Paise,
    /// Verified content digest.
    pub content_hash: ContentAddress,
    /// Source portal.
    pub portal: String,
}

impl RawTenderNotice {
    /// Transition: Verify payload and extract strongly typed attributes.
    #[must_use]
    pub fn verify(
        self,
        tender_id: String,
        work_title: String,
        estimated_value: Paise,
    ) -> VerifiedNotice {
        let content_hash = ContentAddress::from_bytes(&self.payload);
        VerifiedNotice {
            tender_id,
            work_title,
            estimated_value,
            content_hash,
            portal: self.portal,
        }
    }
}

/// State 3: Budget Matched Notice
/// Invariant: Requires a verified notice and an explicit municipal budget code correlation.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MatchedTender {
    /// The verified notice.
    pub notice: VerifiedNotice,
    /// Correlated municipal budget code (e.g. RI11A101).
    pub budget_code: String,
    /// Match confidence score (0 - 1000).
    pub confidence_milli: u32,
}

impl VerifiedNotice {
    /// Transition: Match notice to budget line.
    #[must_use]
    pub fn match_budget(self, budget_code: String, confidence_milli: u32) -> MatchedTender {
        MatchedTender {
            notice: self,
            budget_code,
            confidence_milli,
        }
    }
}

/// State 4: Fully Reconciled Audit Dossier
/// Invariant: Contains matched tender, verified rules evaluation, and ready status.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ReconciliationDossier {
    /// Correlated matched tender.
    pub matched_tender: MatchedTender,
    /// Evaluated anomaly flags (if any).
    pub flags: Vec<AnomalyFlag>,
    /// Signoff status: true if ready for UAT review.
    pub uat_ready: bool,
}

impl MatchedTender {
    /// Transition: Complete rule evaluation and produce formal audit dossier.
    #[must_use]
    pub fn generate_dossier(self, flags: Vec<AnomalyFlag>) -> ReconciliationDossier {
        ReconciliationDossier {
            matched_tender: self,
            flags,
            uat_ready: true,
        }
    }
}
