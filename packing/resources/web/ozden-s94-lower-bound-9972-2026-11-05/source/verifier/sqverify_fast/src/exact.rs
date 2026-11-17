//! Exact rationals: parsing certificate tokens and enclosing them in binary64.

use std::cmp::Ordering;

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, ToPrimitive, Zero};

use crate::interval::Iv;

/// The largest numerator or denominator size, in bits, accepted from input.
pub const MAX_RATIONAL_BITS: u64 = 4096;

/// Parse an exact rational from a decimal literal (`-1.25e-3`), an integer, or
/// a fraction `p/q`. A decimal JSON number means its literal value, never the
/// binary64 value nearest to it.
///
/// # Errors
///
/// Returns a message when the token is malformed, has a zero denominator, or
/// exceeds [`MAX_RATIONAL_BITS`].
pub fn parse_rational(token: &str) -> Result<BigRational, String> {
    let token = token.trim();
    if token.is_empty() || token.len() > 4096 {
        return Err(format!("not an exact rational token: {token:?}"));
    }
    let value = if let Some((numerator, denominator)) = token.split_once('/') {
        let p = parse_integer(numerator)?;
        let q = parse_integer(denominator)?;
        if q.is_zero() {
            return Err(format!("zero denominator in {token:?}"));
        }
        BigRational::new(p, q)
    } else {
        parse_decimal(token)?
    };
    if value.numer().bits() > MAX_RATIONAL_BITS || value.denom().bits() > MAX_RATIONAL_BITS {
        return Err(format!("rational {token:?} exceeds the bit limit"));
    }
    Ok(value)
}

fn parse_integer(text: &str) -> Result<BigInt, String> {
    let digits = text.strip_prefix('-').unwrap_or(text);
    if digits.is_empty() || !digits.bytes().all(|b| b.is_ascii_digit()) {
        return Err(format!("not an integer: {text:?}"));
    }
    text.parse::<BigInt>()
        .map_err(|error| format!("not an integer: {text:?} ({error})"))
}

fn parse_decimal(text: &str) -> Result<BigRational, String> {
    let (negative, body) = match text.strip_prefix('-') {
        Some(rest) => (true, rest),
        None => (false, text),
    };
    let (mantissa, exponent) = match body.find(['e', 'E']) {
        Some(index) => {
            let exponent_text = &body[index + 1..];
            let exponent_text = exponent_text.strip_prefix('+').unwrap_or(exponent_text);
            let exponent: i64 = exponent_text
                .parse()
                .map_err(|_| format!("bad exponent in {text:?}"))?;
            if exponent.unsigned_abs() > MAX_RATIONAL_BITS {
                return Err(format!("exponent too large in {text:?}"));
            }
            (&body[..index], exponent)
        }
        None => (body, 0),
    };
    let (integer_part, fraction_part) = mantissa.split_once('.').unwrap_or((mantissa, ""));
    if integer_part.is_empty() && fraction_part.is_empty() {
        return Err(format!("not a number: {text:?}"));
    }
    if !integer_part.bytes().all(|b| b.is_ascii_digit())
        || !fraction_part.bytes().all(|b| b.is_ascii_digit())
    {
        return Err(format!("not a decimal: {text:?}"));
    }
    let digits = format!("{integer_part}{fraction_part}");
    let mut numerator: BigInt = digits
        .parse()
        .map_err(|_| format!("not a decimal: {text:?}"))?;
    if negative {
        numerator = -numerator;
    }
    let scale =
        exponent - i64::try_from(fraction_part.len()).map_err(|_| "too long".to_string())?;
    let ten = BigInt::from(10u8);
    let power = num_traits::pow(ten, usize::try_from(scale.unsigned_abs()).unwrap_or(0));
    Ok(if scale >= 0 {
        BigRational::from_integer(numerator * power)
    } else {
        BigRational::new(numerator, power)
    })
}

/// The exact rational value of a finite binary64 number.
///
/// # Panics
///
/// Panics if `x` is not finite; callers pass only finite values.
#[must_use]
pub fn of_f64(x: f64) -> BigRational {
    BigRational::from_float(x).unwrap_or_else(|| panic!("non-finite value {x}"))
}

/// The tightest binary64 interval containing an exact rational.
///
/// The starting approximation need not be correctly rounded: the loop moves it
/// until the exact comparisons hold, so the result is the largest
/// representable value at most `q` and the smallest at least `q`.
///
/// # Errors
///
/// Returns a message if `q` lies outside the finite binary64 range.
pub fn enclose(q: &BigRational) -> Result<Iv, String> {
    let mut x = q.to_f64().unwrap_or(f64::NAN);
    if !x.is_finite() {
        return Err(format!("rational {q} is outside the binary64 range"));
    }
    for _ in 0..64 {
        match compare(q, x) {
            Ordering::Equal => return Ok(Iv::point(x)),
            Ordering::Greater => {
                let next = x.next_up();
                match compare(q, next) {
                    Ordering::Less => return Ok(Iv::new(x, next)),
                    Ordering::Equal => return Ok(Iv::point(next)),
                    Ordering::Greater => x = next,
                }
            }
            Ordering::Less => {
                let previous = x.next_down();
                match compare(q, previous) {
                    Ordering::Greater => return Ok(Iv::new(previous, x)),
                    Ordering::Equal => return Ok(Iv::point(previous)),
                    Ordering::Less => x = previous,
                }
            }
        }
        if !x.is_finite() {
            break;
        }
    }
    Err(format!("cannot enclose {q}"))
}

/// Exact comparison of a rational with a finite binary64 value, without
/// building the value as a normalized rational: `x = +-m 2^e` is compared by
/// cross-multiplying with the (positive) denominator and shifting.
///
/// # Panics
///
/// Panics if `x` is not finite.
#[must_use]
pub fn compare(q: &BigRational, x: f64) -> Ordering {
    assert!(x.is_finite(), "non-finite value {x}");
    if x == 0.0 {
        return q.numer().sign().cmp(&num_bigint::Sign::NoSign);
    }
    let bits = x.to_bits();
    let negative = bits >> 63 == 1;
    let exponent_bits = i64::from(u16::try_from((bits >> 52) & 0x7ff).unwrap_or(0));
    let fraction = bits & ((1u64 << 52) - 1);
    let (mantissa, exponent) = if exponent_bits == 0 {
        (fraction, -1074)
    } else {
        (fraction | (1u64 << 52), exponent_bits - 1075)
    };
    let mut scaled = BigInt::from(mantissa) * q.denom();
    if negative {
        scaled = -scaled;
    }
    let shift = usize::try_from(exponent.unsigned_abs()).unwrap_or(usize::MAX);
    if exponent >= 0 {
        q.numer().cmp(&(scaled << shift))
    } else {
        (q.numer() << shift).cmp(&scaled)
    }
}

/// Enclose a rational and return its nearest-or-adjacent midpoint value.
///
/// # Errors
///
/// As [`enclose`].
pub fn approx(q: &BigRational) -> Result<f64, String> {
    // Either endpoint is within one unit in the last place of q, which is all
    // the classification slack of lemma F2 asks of an approximate value.
    Ok(enclose(q)?.lo)
}

/// `true` when `q` is strictly positive.
#[must_use]
pub fn is_positive(q: &BigRational) -> bool {
    q.is_positive()
}

/// The exact rational one.
#[must_use]
pub fn one() -> BigRational {
    BigRational::one()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn r(p: i64, q: i64) -> BigRational {
        BigRational::new(BigInt::from(p), BigInt::from(q))
    }

    #[test]
    fn decimals_are_their_literal_values() {
        assert_eq!(parse_rational("0.1").unwrap(), r(1, 10));
        assert_eq!(parse_rational("-2.50").unwrap(), r(-5, 2));
        assert_eq!(parse_rational("1e-3").unwrap(), r(1, 1000));
        assert_eq!(parse_rational("12.5E+1").unwrap(), r(125, 1));
        assert_eq!(parse_rational("7/21").unwrap(), r(1, 3));
        assert!(parse_rational("1/0").is_err());
        assert!(parse_rational("0x1p3").is_err());
        assert!(parse_rational("").is_err());
        assert!(parse_rational("1.2.3").is_err());
    }

    #[test]
    fn enclosures_are_tight_and_contain_the_value() {
        for (p, q) in [
            (1, 10),
            (1, 3),
            (2, 1),
            (-7, 9),
            (9977, 20000),
            (1_000_001, 1),
        ] {
            let value = r(p, q);
            let iv = enclose(&value).unwrap();
            assert!(of_f64(iv.lo) <= value && value <= of_f64(iv.hi));
            assert!(iv.lo == iv.hi || iv.lo.next_up() == iv.hi);
        }
        assert_eq!(enclose(&r(1, 2)).unwrap(), Iv::point(0.5));
    }
}
