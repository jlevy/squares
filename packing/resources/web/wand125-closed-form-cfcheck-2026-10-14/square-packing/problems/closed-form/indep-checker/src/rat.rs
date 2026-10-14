use crate::{parse_error, Result};
use num_bigint::BigInt;

use num_traits::{One, Zero};
use serde_json::Value;
use std::str::FromStr;
pub type Q = crate::small_rat::Rational;
pub fn q(n: i64, d: i64) -> Q {
    Q::ratio(n, d)
}
pub fn int(n: i64) -> Q {
    Q::from_i64(n)
}
pub fn parse(s: &str) -> Result<Q> {
    let parts: Vec<_> = s.split('/').collect();
    if parts.is_empty() || parts.len() > 2 {
        return Err(parse_error("invalid rational"));
    }
    fn integer(s: &str, signed: bool) -> Result<BigInt> {
        let digits = if signed {
            s.strip_prefix('-').unwrap_or(s)
        } else {
            s
        };
        if digits.is_empty() || !digits.bytes().all(|x| x.is_ascii_digit()) {
            return Err(parse_error("invalid rational integer"));
        }
        BigInt::from_str(s).map_err(|_| parse_error("invalid integer"))
    }
    let n = integer(parts[0], true)?;
    let d = if parts.len() == 2 {
        integer(parts[1], false)?
    } else {
        BigInt::one()
    };
    if d <= BigInt::zero() {
        return Err(parse_error("rational denominator must be positive"));
    }
    Ok(Q::new(n, d))
}
pub fn value(v: &Value) -> Result<Q> {
    parse(
        v.as_str()
            .ok_or_else(|| parse_error("rational must be a string"))?,
    )
}
pub fn array(v: &Value, n: usize) -> Result<Vec<Q>> {
    let a = v
        .as_array()
        .ok_or_else(|| parse_error("expected rational array"))?;
    if a.len() != n {
        return Err(parse_error(format!("expected {n} rational entries")));
    }
    a.iter().map(value).collect()
}
pub fn midpoint(a: &Q, b: &Q) -> Q {
    (a + b) / int(2)
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn rationals() {
        assert_eq!(parse("-12/18").unwrap(), q(-2, 3));
        assert!(parse("1/0").is_err());
        assert!(parse("1/-2").is_err());
        assert!(parse("0.5").is_err());
        assert!(parse("+1").is_err());
        assert!(parse("1/2/3").is_err());
        assert!(parse(" 1").is_err());
        assert!(parse("123456789012345678901234567890/3").is_ok());
    }
}
