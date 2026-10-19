//! Python-compatible numeric coercion and exact rational coordinates.
use crate::value::Value;
use crate::{Result, malformed};
use rug::{Integer, Rational, ops::Pow};
/// An arbitrary-precision rational used by every geometric predicate.
pub type Q = Rational;
/// Exact Cartesian coordinates `(x, y)`.
pub type Point = (Q, Q);
/// The closed half-plane coefficients `(a, b, c)` for `a*x + b*y <= c`.
pub type Plane = (Q, Q, Q);
/// Polygon vertices in their supplied boundary order.
pub type Poly = Vec<Point>;
/// Require an object member, reporting a malformed certificate when absent.
pub fn get<'a>(v: &'a Value, key: &str) -> Result<&'a Value> {
    v.as_object()
        .and_then(|o| o.get(key))
        .ok_or_else(|| malformed(format!("missing member {key}")))
}
/// Require a JSON array without coercing other iterable values.
pub fn array(v: &Value) -> Result<&Vec<Value>> {
    v.as_array().ok_or_else(|| malformed("expected array"))
}
/// Require an array element at a zero-based index.
pub fn at(v: &Value, i: usize) -> Result<&Value> {
    array(v)?
        .get(i)
        .ok_or_else(|| malformed("array index out of range"))
}
/// Require a JSON object while preserving its key domain.
pub fn object(v: &Value) -> Result<&crate::value::Map> {
    v.as_object().ok_or_else(|| malformed("expected object"))
}
fn trim_python(s: &str) -> &str {
    s.trim_matches(|c: char| c.is_whitespace() || ('\u{1c}'..='\u{1f}').contains(&c))
}
// Unicode decimal-digit blocks, including the additions through Unicode 16.
fn decimal(c: char) -> Option<u32> {
    const STARTS: &[u32] = &[
        0x30, 0x660, 0x6f0, 0x7c0, 0x966, 0x9e6, 0xa66, 0xae6, 0xb66, 0xbe6, 0xc66, 0xce6, 0xd66,
        0xde6, 0xe50, 0xed0, 0xf20, 0x1040, 0x1090, 0x17e0, 0x1810, 0x1946, 0x19d0, 0x1a80, 0x1a90,
        0x1b50, 0x1bb0, 0x1c40, 0x1c50, 0xa620, 0xa8d0, 0xa900, 0xa9d0, 0xa9f0, 0xaa50, 0xabf0,
        0xff10, 0x104a0, 0x10d30, 0x10d40, 0x11066, 0x110f0, 0x11136, 0x111d0, 0x112f0, 0x11450,
        0x114d0, 0x11650, 0x116c0, 0x116d0, 0x116da, 0x11730, 0x118e0, 0x11950, 0x11bf0, 0x11c50,
        0x11d50, 0x11da0, 0x11f50, 0x16130, 0x16a60, 0x16ac0, 0x16b50, 0x16d70, 0x1ccf0, 0x1d7ce,
        0x1d7d8, 0x1d7e2, 0x1d7ec, 0x1d7f6, 0x1e140, 0x1e2f0, 0x1e4f0, 0x1e5f1, 0x1e950, 0x1fbf0,
    ];
    let n = c as u32;
    STARTS
        .iter()
        .find_map(|&start| (n >= start && n < start + 10).then(|| n - start))
}
/// Parse Python decimal integer syntax, including Unicode digits and underscores.
pub fn integer(s: &str) -> Result<Integer> {
    let s = trim_python(s);
    let (negative, body) = if let Some(s) = s.strip_prefix('-') {
        (true, s)
    } else {
        (false, s.strip_prefix('+').unwrap_or(s))
    };
    let mut n =
        Integer::from_str_radix(&digits(body)?, 10).map_err(|_| malformed("invalid integer"))?;
    if negative {
        n = -n;
    }
    Ok(n)
}
fn digits(s: &str) -> Result<String> {
    let mut out = String::new();
    let chars: Vec<_> = s.chars().collect();
    for (i, c) in chars.iter().enumerate() {
        if *c == '_' {
            if i == 0
                || i + 1 == chars.len()
                || decimal(chars[i - 1]).is_none()
                || decimal(chars[i + 1]).is_none()
            {
                return Err(malformed("invalid numeric underscore"));
            }
        } else if let Some(n) = decimal(*c) {
            out.push(char::from(
                b'0' + u8::try_from(n).expect("Unicode decimal digits are between zero and nine"),
            ));
        } else {
            return Err(malformed("invalid decimal digit"));
        }
    }
    if out.is_empty() {
        return Err(malformed("missing digits"));
    }
    Ok(out)
}
/// Parse Python fraction text exactly, including decimal exponents.
#[expect(
    clippy::many_single_char_names,
    reason = "Numerator and denominator symbols mirror Python fraction parsing."
)]
pub fn fraction_str(s: &str) -> Result<Q> {
    let s = trim_python(s);
    // Most certificate coordinates are plain ASCII integers or integer ratios.
    // Rust's integer parser accepts only the same sign/digit subset here; all
    // Unicode, underscore, decimal/exponent and large-integer cases stay below.
    if let Ok(n) = s.parse::<i128>() {
        return Ok(Q::from(n));
    }
    if let Some((n, d)) = s.split_once('/')
        && trim_python(d).bytes().all(|c| c.is_ascii_digit())
        && let (Ok(n), Ok(d)) = (
            trim_python(n).parse::<i128>(),
            trim_python(d).parse::<i128>(),
        )
    {
        if d == 0 {
            return Err(malformed("zero denominator"));
        }
        return Ok(Q::from((n, d)));
    }
    if let Some((a, b)) = s.split_once('/') {
        let a = trim_python(a);
        let b = trim_python(b);
        let (neg, a) = if let Some(t) = a.strip_prefix('-') {
            (true, t)
        } else {
            (false, a.strip_prefix('+').unwrap_or(a))
        };
        let mut n = integer(&digits(a)?)?;
        if neg {
            n = -n;
        }
        let d = integer(&digits(b)?)?;
        if d == 0 {
            return Err(malformed("zero denominator"));
        }
        return Ok(Q::from((n, d)));
    }
    let (negative, s) = if let Some(t) = s.strip_prefix('-') {
        (true, t)
    } else {
        (false, s.strip_prefix('+').unwrap_or(s))
    };
    let parts: Vec<_> = s.split(['e', 'E']).collect();
    if parts.len() > 2 {
        return Err(malformed("invalid exponent"));
    }
    let exponent = if parts.len() == 2 {
        let t = parts[1];
        let (neg, t) = if let Some(t) = t.strip_prefix('-') {
            (true, t)
        } else {
            (false, t.strip_prefix('+').unwrap_or(t))
        };
        let mut n = integer(&digits(t)?)?;
        if neg {
            n = -n;
        }
        n
    } else {
        Integer::from(0)
    };
    let mantissa: Vec<_> = parts[0].split('.').collect();
    if mantissa.len() > 2 {
        return Err(malformed("invalid decimal"));
    }
    let whole = if mantissa[0].is_empty() {
        String::new()
    } else {
        digits(mantissa[0])?
    };
    let frac = if mantissa.len() == 2 && !mantissa[1].is_empty() {
        digits(mantissa[1])?
    } else {
        String::new()
    };
    if whole.is_empty() && frac.is_empty() {
        return Err(malformed("missing digits"));
    }
    let mut n = integer(&(whole + &frac))?;
    if negative {
        n = -n;
    }
    let power = exponent - Integer::from(frac.len());
    let magnitude = power
        .clone()
        .abs()
        .to_u32()
        .ok_or_else(|| malformed("decimal exponent exceeds addressable size"))?;
    let ten = Integer::from(10).pow(magnitude);
    Ok(if power >= 0 {
        Q::from(n * ten)
    } else {
        Q::from((n, ten))
    })
}
/// Recognize integer JSON numbers and Python boolean integers.
#[must_use]
pub fn is_int(v: &Value) -> bool {
    matches!(v, Value::Bool(_))
        || matches!(v,Value::Number(n) if !n.to_string().contains(['.','e','E']) && !matches!(n.to_string().as_str(), "NaN" | "Infinity" | "-Infinity"))
}
/// Coerce an integer number or boolean to an exact integer.
pub fn int_value(v: &Value) -> Result<Integer> {
    match v {
        Value::Bool(b) => Ok(Integer::from(u8::from(*b))),
        Value::Number(n) if is_int(v) => integer(&n.to_string()),
        _ => Err(malformed("expected integer")),
    }
}
/// Coerce a Python fraction input; JSON floats use their binary64 rational value.
pub fn q(v: &Value) -> Result<Q> {
    match v {
        Value::String(s) => fraction_str(s),
        Value::Bool(b) => Ok(Q::from(u8::from(*b))),
        Value::Number(n) => {
            let s = n.to_string();
            if s.contains(['.', 'e', 'E']) {
                let f = s.parse::<f64>().map_err(|_| malformed("invalid float"))?;
                Q::from_f64(f).ok_or_else(|| malformed("nonfinite Fraction"))
            } else {
                Ok(Q::from(integer(&s)?))
            }
        }
        _ => Err(malformed("expected rational number")),
    }
}
/// Require a nonnegative integer that fits a platform index.
pub fn index(v: &Value) -> Result<usize> {
    int_value(v)?
        .to_usize()
        .ok_or_else(|| malformed("index out of range"))
}
/// Read the first two coordinates using the certificate point conventions.
pub fn point(v: &Value) -> Result<Point> {
    if let Some(s) = v.as_str() {
        let mut chars = s.chars();
        let a = chars
            .next()
            .ok_or_else(|| malformed("point index out of range"))?;
        let b = chars
            .next()
            .ok_or_else(|| malformed("point index out of range"))?;
        return Ok((fraction_str(&a.to_string())?, fraction_str(&b.to_string())?));
    }
    Ok((q(at(v, 0)?)?, q(at(v, 1)?)?))
}
/// Iterate arrays, object keys, or Unicode string characters with Python semantics.
pub fn iterable(v: &Value) -> Result<Vec<std::borrow::Cow<'_, Value>>> {
    use std::borrow::Cow;
    match v {
        Value::Array(a) => Ok(a.iter().map(Cow::Borrowed).collect()),
        Value::Object(o) => Ok(o
            .keys()
            .map(|s| Cow::Owned(Value::string(s.0.clone())))
            .collect()),
        Value::String(s) => Ok(s
            .chars()
            .map(|c| Cow::Owned(Value::String(c.to_string())))
            .collect()),
        _ => Err(malformed("value is not iterable")),
    }
}
/// Read an iterable of exact points, preserving the supplied order.
pub fn poly(v: &Value) -> Result<Poly> {
    iterable(v)?.iter().map(|v| point(v)).collect()
}
/// Read declared normals and upper bounds as exact half-planes.
pub fn planes(v: &Value) -> Result<Vec<Plane>> {
    iterable(v)?
        .iter()
        .map(|it| {
            let (a, b) = point(get(it, "normal")?)?;
            Ok((a, b, q(get(it, "upper")?)?))
        })
        .collect()
}
/// Render a point using Python Fraction diagnostic syntax.
#[must_use]
pub fn repr_point(p: &Point) -> String {
    format!(
        "(Fraction({}, {}), Fraction({}, {}))",
        p.0.numer(),
        p.0.denom(),
        p.1.numer(),
        p.1.denom()
    )
}
/// Evaluate an exact linear form at a point.
#[must_use]
pub fn dot(a: &Q, b: &Q, p: &Point) -> Q {
    Q::from(a * &p.0) + Q::from(b * &p.1)
}

/// Count array entries, object keys, or Python Unicode code points.
pub fn pylen(v: &Value) -> Result<usize> {
    match v {
        Value::Array(a) => Ok(a.len()),
        Value::Object(o) => Ok(o.len()),
        Value::String(s) => Ok(s.chars().count()),
        Value::SurrogateString(s) => Ok(s.len()),
        _ => Err(malformed("value has no length")),
    }
}
/// Require a numeric JSON value for an exact comparison.
pub fn numeric(v: &Value) -> Result<Q> {
    match v {
        Value::Number(_) | Value::Bool(_) => q(v),
        _ => Err(malformed("expected numeric comparison")),
    }
}
