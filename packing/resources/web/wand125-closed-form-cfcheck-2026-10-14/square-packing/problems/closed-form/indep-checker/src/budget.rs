//! Optional command-wide computation deadline. Exhaustion marks the run incomplete, never a leaf refusal.
use std::{
    sync::OnceLock,
    time::{Duration, Instant},
};
static DEADLINE: OnceLock<Option<Instant>> = OnceLock::new();
#[derive(Debug)]
pub struct Exhausted;
pub fn start(seconds: Option<u64>) -> crate::Result<()> {
    let deadline = seconds
        .map(|s| {
            Instant::now()
                .checked_add(Duration::from_secs(s))
                .ok_or_else(|| crate::parse_error("deadline outside clock range"))
        })
        .transpose()?;
    DEADLINE.get_or_init(|| deadline);
    let previous = std::panic::take_hook();
    std::panic::set_hook(Box::new(move |info| {
        if !info.payload().is::<Exhausted>() {
            previous(info);
        }
    }));
    Ok(())
}
pub fn expired() -> bool {
    DEADLINE
        .get()
        .and_then(|v| *v)
        .is_some_and(|d| Instant::now() >= d)
}
pub fn check() {
    if expired() {
        std::panic::panic_any(Exhausted);
    }
}

/// Preserve the distinction between interruption and a genuine calculation defect.
pub fn panic_error(payload: Box<dyn std::any::Any + Send>) -> Option<crate::Error> {
    if payload.is::<Exhausted>() {
        return None;
    }
    let message = payload
        .downcast_ref::<String>()
        .map(String::as_str)
        .or_else(|| payload.downcast_ref::<&str>().copied())
        .unwrap_or("non-string panic payload");
    Some(crate::refuse(format!(
        "internal arithmetic failure: {message}"
    )))
}
#[cfg(test)]
mod tests {
    #[test]
    fn panic_classification() {
        assert!(super::panic_error(Box::new(super::Exhausted)).is_none());
        assert_eq!(
            super::panic_error(Box::new("division by zero"))
                .unwrap()
                .reason,
            "internal arithmetic failure: division by zero"
        );
    }
}
