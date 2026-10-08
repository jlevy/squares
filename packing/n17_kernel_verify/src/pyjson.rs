//! Python JSON formatting. Floating-point conversion is confined to JSON float
//! compatibility; all predicates on numeric JSON values use exact rationals.
use crate::exact::{integer, q};
use crate::value::Value;
use crate::{Result, malformed};
use rug::{Integer, Rational, ops::Pow};
use sha2::{Digest, Sha256};
use std::fmt::Write as _;
/// Quote a UTF-8 string using Python ASCII JSON escaping.
#[must_use]
pub fn escape(s: &str) -> String {
    escape_points(s.chars().map(u32::from))
}
/// Quote Python Unicode code points, preserving unpaired surrogates.
#[must_use]
pub fn escape_points(points: impl IntoIterator<Item = u32>) -> String {
    let mut out = String::from("\"");
    for c in points {
        match c {
            34 => out.push_str("\\\""),
            92 => out.push_str("\\\\"),
            10 => out.push_str("\\n"),
            13 => out.push_str("\\r"),
            9 => out.push_str("\\t"),
            8 => out.push_str("\\b"),
            12 => out.push_str("\\f"),
            32..=126 => out.push(
                char::from_u32(c).expect("the matched ASCII range contains only Unicode scalars"),
            ),
            0..=0xffff => {
                write!(out, "\\u{c:04x}").expect("formatting into a String is infallible");
            }
            _ => {
                let n = c - 0x10000;
                write!(
                    out,
                    "\\u{:04x}\\u{:04x}",
                    0xd800 + (n >> 10),
                    0xdc00 + (n & 1023)
                )
                .expect("formatting into a String is infallible");
            }
        }
    }
    out.push('"');
    out
}
/// Render a Python string diagnostic with its quote and printability rules.
#[must_use]
pub fn repr_key(k: &crate::value::Key) -> String {
    let quote = if k.0.contains(&39) && !k.0.contains(&34) {
        '"'
    } else {
        '\''
    };
    let mut out = String::new();
    out.push(quote);
    for &n in &k.0 {
        if let Some(c) = char::from_u32(n) {
            if c == quote || c == '\\' {
                out.push('\\');
                out.push(c);
            } else if c == '\n' {
                out.push_str("\\n");
            } else if c == '\r' {
                out.push_str("\\r");
            } else if c == '\t' {
                out.push_str("\\t");
            } else if !crate::unicode_repr::printable(n) {
                if n <= 255 {
                    write!(out, "\\x{n:02x}").expect("formatting into a String is infallible");
                } else if n <= 65535 {
                    write!(out, "\\u{n:04x}").expect("formatting into a String is infallible");
                } else {
                    write!(out, "\\U{n:08x}").expect("formatting into a String is infallible");
                }
            } else {
                out.push(c);
            }
        } else {
            write!(out, "\\u{n:04x}").expect("formatting into a String is infallible");
        }
    }
    out.push(quote);
    out
}
/// Render a UTF-8 string using Python string representation rules.
#[must_use]
pub fn repr_string(s: &str) -> String {
    repr_key(&crate::value::Key::from(s))
}
/// Render binary64 using Python shortest round-trip decimals and ties to even.
#[must_use]
pub fn float_repr(f: f64) -> String {
    if f.is_nan() {
        return "NaN".into();
    }
    if f.is_infinite() {
        return if f.is_sign_negative() {
            "-Infinity"
        } else {
            "Infinity"
        }
        .into();
    }
    if f == 0.0 {
        return if f.is_sign_negative() { "-0.0" } else { "0.0" }.into();
    }
    // Rust's shortest scientific rendering supplies the digit count and scale.
    // Choose the closest of the equally short round-tripping decimals ourselves,
    // including Python's ties-to-even rule (Rust's formatting tie rule differs).
    let raw = format!("{:e}", f.abs());
    let (mant, exp) = raw.split_once('e').unwrap_or((&raw, "0"));
    let exponent: i32 = exp.parse().unwrap_or(0);
    let ds = mant.replace('.', "");
    let mut digits = ds.clone();
    if let Ok(n) = integer(&ds) {
        let power = exponent
            - (i32::try_from(ds.len())
                .expect("binary64 shortest decimals have at most seventeen digits")
                - 1);
        let ten = Integer::from(10).pow(power.unsigned_abs());
        let target = Rational::from_f64(f.abs()).unwrap_or_default();
        let mut best: Option<(Rational, Integer)> = None;
        for delta in [-1i32, 0, 1] {
            let candidate = n.clone() + delta;
            if candidate <= 0 {
                continue;
            }
            let text = format!("{candidate}e{power}");
            if text.parse::<f64>().ok() != Some(f.abs()) {
                continue;
            }
            let val = if power >= 0 {
                Rational::from(candidate.clone() * &ten)
            } else {
                Rational::from((candidate.clone(), ten.clone()))
            };
            let distance = (val - &target).abs();
            let replace = match &best {
                None => true,
                Some((d, prior)) => {
                    distance < *d || (distance == *d && candidate.is_even() && !prior.is_even())
                }
            };
            if replace {
                best = Some((distance, candidate));
            }
        }
        if let Some((_, n)) = best {
            digits = n.to_string();
        }
    }
    // A carry can add one digit; a borrow can remove one.
    let mut exponent = exponent
        + i32::try_from(digits.len())
            .expect("a binary64 decimal candidate has at most eighteen digits")
        - i32::try_from(ds.len())
            .expect("binary64 shortest decimals have at most seventeen digits");
    while digits.len() > 1 && digits.ends_with('0') {
        digits.pop();
    }
    let mut out = if f.is_sign_negative() {
        String::from("-")
    } else {
        String::new()
    };
    if (-4..16).contains(&exponent) {
        let position = exponent + 1;
        if position <= 0 {
            out.push_str("0.");
            out.push_str(
                &"0".repeat(
                    usize::try_from(-position)
                        .expect("the decimal position is nonpositive in this branch"),
                ),
            );
            out.push_str(&digits);
        } else if usize::try_from(position)
            .expect("the decimal position is positive in this branch")
            >= digits.len()
        {
            out.push_str(&digits);
            out.push_str(&"0".repeat(
                usize::try_from(position).expect("the decimal position is positive in this branch")
                    - digits.len(),
            ));
            out.push_str(".0");
        } else {
            out.push_str(
                &digits[..usize::try_from(position)
                    .expect("the decimal position is positive in this branch")],
            );
            out.push('.');
            out.push_str(
                &digits[usize::try_from(position)
                    .expect("the decimal position is positive in this branch")..],
            );
        }
    } else {
        out.push_str(&digits[..1]);
        if digits.len() > 1 {
            out.push('.');
            out.push_str(&digits[1..]);
        }
        out.push('e');
        out.push(if exponent < 0 { '-' } else { '+' });
        exponent = exponent.abs();
        write!(out, "{exponent:02}").expect("formatting into a String is infallible");
    }
    out
}
/// Canonicalize an integer or binary64 JSON token using Python numeric rendering.
pub fn number(n: &serde_json::Number) -> Result<String> {
    let s = n.to_string();
    if matches!(s.as_str(), "NaN" | "Infinity" | "-Infinity") {
        return Ok(s);
    }
    if s.contains(['.', 'e', 'E']) {
        Ok(float_repr(
            s.parse().map_err(|_| malformed("invalid float"))?,
        ))
    } else {
        Ok(integer(&s)?.to_string())
    }
}
#[derive(Clone, Copy)]
enum Style {
    Canonical,
    Pretty,
    Compact,
}
fn write(v: &Value, out: &mut String, style: Style, depth: usize) -> Result<()> {
    let pretty = matches!(style, Style::Pretty);
    let sep = if matches!(style, Style::Canonical) {
        ":"
    } else {
        ": "
    };
    match v {
        Value::Null => out.push_str("null"),
        Value::Bool(b) => out.push_str(if *b { "true" } else { "false" }),
        Value::Number(n) => out.push_str(&number(n)?),
        Value::String(s) => out.push_str(&escape(s)),
        Value::SurrogateString(s) => out.push_str(&escape_points(s.iter().copied())),
        Value::Array(a) => {
            out.push('[');
            for (i, v) in a.iter().enumerate() {
                if i > 0 {
                    out.push(',');
                    if matches!(style, Style::Compact) {
                        out.push(' ');
                    }
                }
                if pretty {
                    out.push('\n');
                    out.push_str(&" ".repeat(depth + 1));
                }
                write(v, out, style, depth + 1)?;
            }
            if pretty && !a.is_empty() {
                out.push('\n');
                out.push_str(&" ".repeat(depth));
            }
            out.push(']');
        }
        Value::Object(o) => {
            out.push('{');
            let mut keys: Vec<_> = o.keys().collect();
            if matches!(style, Style::Canonical) {
                keys.sort();
            }
            for (i, k) in keys.iter().enumerate() {
                if i > 0 {
                    out.push(',');
                    if matches!(style, Style::Compact) {
                        out.push(' ');
                    }
                }
                if pretty {
                    out.push('\n');
                    out.push_str(&" ".repeat(depth + 1));
                }
                out.push_str(&escape_points(k.0.iter().copied()));
                out.push_str(sep);
                write(&o[*k], out, style, depth + 1)?;
            }
            if pretty && !o.is_empty() {
                out.push('\n');
                out.push_str(&" ".repeat(depth));
            }
            out.push('}');
        }
    }
    Ok(())
}
/// Render ASCII JSON with sorted keys and compact canonical separators.
pub fn canonical(v: &Value) -> Result<String> {
    let mut out = String::new();
    write(v, &mut out, Style::Canonical, 0)?;
    Ok(out)
}
/// Render receipt JSON with one-space indentation and a trailing newline.
pub fn pretty(v: &Value) -> Result<String> {
    let mut out = String::new();
    write(v, &mut out, Style::Pretty, 0)?;
    out.push('\n');
    Ok(out)
}
/// Render a one-line Python JSON summary with spaced separators.
pub fn compact(v: &Value) -> Result<String> {
    let mut out = String::new();
    write(v, &mut out, Style::Compact, 0)?;
    Ok(out)
}
/// Return the lowercase SHA-256 of the supplied bytes.
#[must_use]
pub fn digest(bytes: &[u8]) -> String {
    format!("{:x}", Sha256::digest(bytes))
}
/// Compare certificate values with Python numeric and container equality semantics.
#[must_use]
pub fn equal(a: &Value, b: &Value) -> bool {
    match (a, b) {
        (Value::Number(_) | Value::Bool(_), Value::Number(_) | Value::Bool(_)) => {
            match (q(a), q(b)) {
                (Ok(x), Ok(y)) => x == y,
                (Err(_), Err(_)) => {
                    let fa = a.as_f64();
                    let fb = b.as_f64();
                    fa.is_some() && fa == fb
                }
                _ => false,
            }
        }
        (Value::Array(a), Value::Array(b)) => {
            a.len() == b.len() && a.iter().zip(b).all(|(a, b)| container_equal(a, b))
        }
        (Value::Object(a), Value::Object(b)) => {
            a.len() == b.len()
                && a.iter()
                    .all(|(k, v)| b.get_key(k).is_some_and(|w| container_equal(v, w)))
        }
        _ => a == b,
    }
}
/// Convert common certificate scalar values using Python str conventions.
pub fn pystr(v: &Value) -> Result<String> {
    Ok(match v {
        Value::String(s) => s.clone(),
        Value::Bool(b) => if *b { "True" } else { "False" }.into(),
        Value::Null => "None".into(),
        Value::Number(n) => match number(n)?.as_str() {
            "NaN" => "nan".into(),
            "Infinity" => "inf".into(),
            "-Infinity" => "-inf".into(),
            other => other.into(),
        },
        _ => canonical(v)?,
    })
}

fn container_equal(a: &Value, b: &Value) -> bool {
    if matches!((a,b),(Value::Number(x),Value::Number(y)) if x.to_string()=="NaN" && y.to_string()=="NaN")
    {
        true
    } else {
        equal(a, b)
    }
}

/// Python round(x, digits), including binary input and decimal ties-to-even.
pub fn round_float(f: f64, digits: u32) -> Result<f64> {
    use rug::ops::DivRounding;
    let x = Rational::from_f64(f).ok_or_else(|| malformed("nonfinite time"))?
        * Integer::from(10).pow(digits);
    let mut n = x.numer().clone().div_floor(x.denom());
    let remainder = x.numer().clone() - n.clone() * x.denom();
    let twice = remainder * 2i32;
    if twice > *x.denom() || (twice == *x.denom() && !n.is_even()) {
        n += 1;
    }
    let value = format!("{n}e-{digits}")
        .parse::<f64>()
        .map_err(|_| malformed("invalid rounded time"))?;
    Ok(if value == 0.0 && f.is_sign_negative() {
        -0.0
    } else {
        value
    })
}
