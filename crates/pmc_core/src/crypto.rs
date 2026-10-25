//! Cryptographic pre-image binding and content addressing.

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

/// Cryptographic content address representing SHA-256 digest of raw payload.
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct ContentAddress(pub String);

impl ContentAddress {
    /// Compute SHA-256 content address from raw immutable bytes.
    #[must_use]
    pub fn from_bytes(payload: &[u8]) -> Self {
        let mut hasher = Sha256::new();
        hasher.update(payload);
        Self(hex::encode(hasher.finalize()))
    }
}
