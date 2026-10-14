pub mod coverage;
pub mod family;
pub mod geom;
pub mod leaf;
pub mod poly;
pub mod rat;
pub mod record;
pub mod report;

#[derive(Debug, Clone)]
pub struct Error {
    pub code: i32,
    pub reason: String,
}
pub type Result<T> = std::result::Result<T, Error>;
pub fn refuse(s: impl Into<String>) -> Error {
    Error {
        code: 1,
        reason: s.into(),
    }
}
pub fn parse_error(s: impl Into<String>) -> Error {
    Error {
        code: 2,
        reason: s.into(),
    }
}
impl From<std::io::Error> for Error {
    fn from(e: std::io::Error) -> Self {
        parse_error(e.to_string())
    }
}
impl From<serde_json::Error> for Error {
    fn from(e: serde_json::Error) -> Self {
        parse_error(e.to_string())
    }
}
pub fn require(ok: bool, s: impl Into<String>) -> Result<()> {
    if ok {
        Ok(())
    } else {
        Err(refuse(s))
    }
}
pub mod budget;
pub mod stage_b;
pub mod symbolic;

pub mod profile;

pub mod small_rat;

pub mod checkpoint;
