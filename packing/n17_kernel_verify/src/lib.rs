//! Exact native replay of n17 certificate objects with Python-compatible receipts.
#![forbid(unsafe_code)]
/// Python-compatible numeric coercion and exact rational coordinates.
pub mod exact;
/// Exact convex geometry and strict ownership predicates.
pub mod geom;
/// Exact integer arithmetic with checked small-integer operations.
pub mod int;
/// Python-compatible JSON canonicalization and receipt rendering.
pub mod pyjson;
/// Python-compatible integer-seeded Mersenne Twister sampling.
pub mod pyrandom;
/// Read-once gzip node streaming and canonical object digests.
pub mod stream;
/// Exact closed-set coverage by vertical sweep events and sections.
pub mod sweep;
mod unicode_repr;
/// JSON values preserving Python Unicode and nonfinite numbers.
pub mod value;
/// Certificate admission, replay, closure checks, and receipts.
pub mod verify;

/// Verifier result separating check failures from malformed input.
pub type Result<T> = std::result::Result<T, Error>;
#[derive(Debug, Clone)]
/// A receipt-compatible validation or input failure.
pub enum Error {
    /// A failed certificate predicate.
    Check(String),
    /// A predicate diagnostic containing Python surrogate code points.
    UnicodeCheck(Vec<u32>),
    /// Input that cannot be decoded or interpreted as a certificate.
    Malformed(String),
}
impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Check(s) => f.write_str(s),
            Self::UnicodeCheck(s) => f.write_str(&pyjson::escape_points(s.iter().copied())),
            Self::Malformed(s) => write!(f, "malformed certificate: {s}"),
        }
    }
}
impl std::error::Error for Error {}
/// Construct a malformed-input failure with diagnostic context.
#[must_use]
pub fn malformed(s: impl Into<String>) -> Error {
    Error::Malformed(s.into())
}
/// Reject a failed certificate predicate with its check diagnostic.
pub fn require(b: bool, s: impl Into<String>) -> Result<()> {
    if b {
        Ok(())
    } else {
        Err(Error::Check(s.into()))
    }
}
impl From<std::io::Error> for Error {
    fn from(e: std::io::Error) -> Self {
        malformed(e.to_string())
    }
}
impl From<serde_json::Error> for Error {
    fn from(e: serde_json::Error) -> Self {
        malformed(e.to_string())
    }
}

#[cfg(test)]
mod tests;

impl Error {
    /// Preserve Python Unicode diagnostics when constructing a receipt value.
    #[must_use]
    pub fn receipt_value(&self) -> value::Value {
        match self {
            Self::UnicodeCheck(s) => value::Value::string(s.clone()),
            _ => value::Value::String(self.to_string()),
        }
    }
}
