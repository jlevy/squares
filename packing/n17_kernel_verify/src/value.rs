//! JSON values with Python's Unicode and nonfinite-number domain. Unlike a Rust
//! String, a Python str can contain unpaired UTF-16 surrogates.
use crate::{Result, malformed};
pub use serde_json::Number;
use std::ops::Index;
#[derive(Clone, Debug, Eq, PartialEq, Ord, PartialOrd)]
/// Python string code points used for JSON object keys and their ordering.
pub struct Key(
    /// Unicode code points, including unpaired UTF-16 surrogates.
    pub Vec<u32>,
);
impl Key {
    /// Convert to UTF-8, rejecting code points that are not Unicode scalar values.
    pub fn text(&self) -> Result<String> {
        self.0
            .iter()
            .map(|&c| char::from_u32(c).ok_or_else(|| malformed("surrogate in text field")))
            .collect()
    }
    /// Compare a key with a UTF-8 string by code point.
    #[must_use]
    pub fn is(&self, s: &str) -> bool {
        self.0.iter().copied().eq(s.chars().map(u32::from))
    }
}
impl From<String> for Key {
    fn from(s: String) -> Self {
        Self(s.chars().map(u32::from).collect())
    }
}
impl From<&str> for Key {
    fn from(s: &str) -> Self {
        Self(s.chars().map(u32::from).collect())
    }
}
#[derive(Clone, Debug, Default, PartialEq)]
/// An insertion-ordered object preserving Python string keys.
pub struct Map(Vec<(Key, Value)>);
impl Map {
    /// Create an empty insertion-ordered object.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }
    /// Count distinct object keys.
    #[must_use]
    pub fn len(&self) -> usize {
        self.0.len()
    }
    /// Test whether the object contains no keys.
    #[must_use]
    pub fn is_empty(&self) -> bool {
        self.0.is_empty()
    }
    /// Iterate keys in insertion order.
    pub fn keys(&self) -> impl Iterator<Item = &Key> {
        self.0.iter().map(|(k, _)| k)
    }
    /// Iterate key/value pairs in insertion order.
    pub fn iter(&self) -> impl Iterator<Item = (&Key, &Value)> {
        self.0.iter().map(|(k, v)| (k, v))
    }
    /// Find an object member by its UTF-8 key, returning None on absence.
    #[must_use]
    pub fn get(&self, s: &str) -> Option<&Value> {
        self.0.iter().find(|(k, _)| k.is(s)).map(|(_, v)| v)
    }
    /// Find a member using a Python code-point key.
    #[must_use]
    pub fn get_key(&self, k: &Key) -> Option<&Value> {
        self.0.iter().find(|(key, _)| key == k).map(|(_, v)| v)
    }
    /// Replace an existing value without changing key order, returning the old value.
    pub fn insert(&mut self, k: Key, v: Value) -> Option<Value> {
        if let Some((_, old)) = self.0.iter_mut().find(|(key, _)| *key == k) {
            Some(std::mem::replace(old, v))
        } else {
            self.0.push((k, v));
            None
        }
    }
}
impl<'a> IntoIterator for &'a Map {
    type Item = (&'a Key, &'a Value);
    type IntoIter =
        std::iter::Map<std::slice::Iter<'a, (Key, Value)>, fn(&(Key, Value)) -> (&Key, &Value)>;
    fn into_iter(self) -> Self::IntoIter {
        self.0.iter().map(|(k, v)| (k, v))
    }
}
impl Index<&Key> for Map {
    type Output = Value;
    fn index(&self, k: &Key) -> &Value {
        self.get_key(k).unwrap_or(&Value::Null)
    }
}
#[derive(Clone, Debug, PartialEq)]
/// A JSON value whose strings and numbers include Python decoder extensions.
pub enum Value {
    /// JSON null.
    Null,
    /// A JSON boolean.
    Bool(bool),
    /// An integer or binary64 token, including nonfinite extensions.
    Number(Number),
    /// A string consisting entirely of Unicode scalar values.
    String(String),
    /// A Python string containing unpaired surrogates.
    SurrogateString(Vec<u32>),
    /// An ordered JSON array.
    Array(Vec<Value>),
    /// An insertion-ordered JSON object.
    Object(Map),
}
impl Value {
    /// Use a UTF-8 string when possible, retaining surrogate code points otherwise.
    #[must_use]
    pub fn string(points: Vec<u32>) -> Self {
        match points
            .iter()
            .map(|&c| char::from_u32(c))
            .collect::<Option<String>>()
        {
            Some(s) => Self::String(s),
            None => Self::SurrogateString(points),
        }
    }
    /// Convert either string representation to a code-point object key.
    #[must_use]
    pub fn key(&self) -> Option<Key> {
        match self {
            Self::String(s) => Some(Key::from(s.as_str())),
            Self::SurrogateString(s) => Some(Key(s.clone())),
            _ => None,
        }
    }
    /// Test for the JSON null variant.
    #[must_use]
    pub fn is_null(&self) -> bool {
        matches!(self, Self::Null)
    }
    /// Recognize both UTF-8 and surrogate-containing Python strings.
    #[must_use]
    pub fn is_string(&self) -> bool {
        matches!(self, Self::String(_) | Self::SurrogateString(_))
    }
    /// Borrow a UTF-8 string; surrogate-containing strings return None.
    #[must_use]
    pub fn as_str(&self) -> Option<&str> {
        if let Self::String(s) = self {
            Some(s)
        } else {
            None
        }
    }
    /// Read a boolean without numeric coercion.
    #[must_use]
    pub fn as_bool(&self) -> Option<bool> {
        if let Self::Bool(b) = self {
            Some(*b)
        } else {
            None
        }
    }
    /// Parse a number as binary64, retaining nonfinite extensions.
    #[must_use]
    pub fn as_f64(&self) -> Option<f64> {
        if let Self::Number(n) = self {
            n.to_string().parse().ok()
        } else {
            None
        }
    }
    /// Borrow array entries without coercion.
    #[must_use]
    pub fn as_array(&self) -> Option<&Vec<Value>> {
        if let Self::Array(a) = self {
            Some(a)
        } else {
            None
        }
    }
    /// Borrow object members without coercion.
    #[must_use]
    pub fn as_object(&self) -> Option<&Map> {
        if let Self::Object(o) = self {
            Some(o)
        } else {
            None
        }
    }
    /// Mutably borrow object members without coercion.
    #[must_use]
    pub fn as_object_mut(&mut self) -> Option<&mut Map> {
        if let Self::Object(o) = self {
            Some(o)
        } else {
            None
        }
    }
    /// Find an object member by its UTF-8 key, returning None on absence.
    #[must_use]
    pub fn get(&self, k: &str) -> Option<&Value> {
        self.as_object().and_then(|o| o.get(k))
    }
}
impl Index<&str> for Value {
    type Output = Value;
    fn index(&self, k: &str) -> &Value {
        self.get(k).unwrap_or(&Value::Null)
    }
}
impl Index<usize> for Value {
    type Output = Value;
    fn index(&self, i: usize) -> &Value {
        self.as_array()
            .and_then(|a| a.get(i))
            .unwrap_or(&Value::Null)
    }
}
impl PartialEq<&str> for Value {
    fn eq(&self, s: &&str) -> bool {
        self.as_str() == Some(s)
    }
}
impl std::fmt::Display for Value {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.write_str(&crate::pyjson::canonical(self).map_err(|_| std::fmt::Error)?)
    }
}
impl From<serde_json::Value> for Value {
    fn from(v: serde_json::Value) -> Self {
        match v {
            serde_json::Value::Null => Self::Null,
            serde_json::Value::Bool(b) => Self::Bool(b),
            serde_json::Value::Number(n) => Self::Number(n),
            serde_json::Value::String(s) => Self::String(s),
            serde_json::Value::Array(a) => Self::Array(a.into_iter().map(Self::from).collect()),
            serde_json::Value::Object(o) => {
                let mut m = Map::new();
                for (k, v) in o {
                    m.insert(k.into(), v.into());
                }
                Self::Object(m)
            }
        }
    }
}
impl From<&Value> for Value {
    fn from(v: &Value) -> Self {
        v.clone()
    }
}
impl From<Map> for Value {
    fn from(m: Map) -> Self {
        Self::Object(m)
    }
}
impl From<String> for Value {
    fn from(s: String) -> Self {
        Self::String(s)
    }
}
impl From<&String> for Value {
    fn from(s: &String) -> Self {
        Self::String(s.clone())
    }
}
impl From<&str> for Value {
    fn from(s: &str) -> Self {
        Self::String(s.into())
    }
}
impl From<bool> for Value {
    fn from(b: bool) -> Self {
        Self::Bool(b)
    }
}
macro_rules! integers{($($t:ty),*)=>{$(impl From<$t> for Value{fn from(n:$t)->Self{Self::Number(Number::from(n))}})*}}
integers!(i32, i64, u32, u64, usize);
impl From<f64> for Value {
    fn from(n: f64) -> Self {
        Self::Number(Number::from_string_unchecked(crate::pyjson::float_repr(n)))
    }
}
impl<T: Into<Value>> From<Option<T>> for Value {
    fn from(v: Option<T>) -> Self {
        v.map_or(Self::Null, Into::into)
    }
}
impl<T: Into<Value>> From<Vec<T>> for Value {
    fn from(v: Vec<T>) -> Self {
        Self::Array(v.into_iter().map(Into::into).collect())
    }
}
#[macro_export]
/// Build certificate JSON values while preserving the custom Python value domain.
macro_rules! json{
 (null)=>{$crate::value::Value::Null};
 ({$($tt:tt)*})=>{{#[allow(unused_mut)] let mut m=$crate::value::Map::new();$crate::json!(@object m $($tt)*,);$crate::value::Value::Object(m)}};
 ([$($tt:tt)*])=>{{#[allow(clippy::vec_init_then_push, reason = "Recursive JSON macro rules append each heterogeneous token after creating the array.")] let a={#[allow(unused_mut)] let mut a=Vec::new();$crate::json!(@array a $($tt)*,);a};$crate::value::Value::Array(a)}};
 (@object $m:ident ,)=>{};
 (@object $m:ident)=>{};
 (@object $m:ident $k:literal : null, $($rest:tt)*)=>{$m.insert($k.into(),$crate::value::Value::Null);$crate::json!(@object $m $($rest)*);};
 (@object $m:ident $k:literal : {$($v:tt)*}, $($rest:tt)*)=>{$m.insert($k.into(),$crate::json!({$($v)*}));$crate::json!(@object $m $($rest)*);};
 (@object $m:ident $k:literal : [$($v:tt)*], $($rest:tt)*)=>{$m.insert($k.into(),$crate::json!([$($v)*]));$crate::json!(@object $m $($rest)*);};
 (@object $m:ident $k:literal : $v:expr, $($rest:tt)*)=>{$m.insert($k.into(),$crate::value::to_value(&($v)));$crate::json!(@object $m $($rest)*);};
 (@array $a:ident ,)=>{};
 (@array $a:ident)=>{};
 (@array $a:ident null, $($rest:tt)*)=>{$a.push($crate::value::Value::Null);$crate::json!(@array $a $($rest)*);};
 (@array $a:ident {$($v:tt)*}, $($rest:tt)*)=>{$a.push($crate::json!({$($v)*}));$crate::json!(@array $a $($rest)*);};
 (@array $a:ident [$($v:tt)*], $($rest:tt)*)=>{$a.push($crate::json!([$($v)*]));$crate::json!(@array $a $($rest)*);};
 (@array $a:ident $v:expr, $($rest:tt)*)=>{$a.push($crate::value::to_value(&($v)));$crate::json!(@array $a $($rest)*);};
 ($v:expr)=>{$crate::value::to_value(&($v))};
}

struct Parser {
    input: Vec<u32>,
    at: usize,
}
impl Parser {
    fn peek(&self) -> Option<u32> {
        self.input.get(self.at).copied()
    }
    fn ws(&mut self) {
        while self.peek().is_some_and(|c| [32, 9, 10, 13].contains(&c)) {
            self.at += 1;
        }
    }
    fn take(&mut self, c: u32) -> bool {
        if self.peek() == Some(c) {
            self.at += 1;
            true
        } else {
            false
        }
    }
    fn string(&mut self) -> Result<Vec<u32>> {
        if !self.take(34) {
            return Err(malformed("expected JSON string"));
        }
        let mut out = vec![];
        loop {
            let c = self
                .peek()
                .ok_or_else(|| malformed("unterminated string"))?;
            self.at += 1;
            if c == 34 {
                break;
            }
            if c < 32 {
                return Err(malformed("control character in JSON string"));
            }
            if c != 92 {
                out.push(c);
                continue;
            }
            let e = self
                .peek()
                .ok_or_else(|| malformed("unterminated escape"))?;
            self.at += 1;
            let c = match e {
                34 | 92 | 47 => e,
                98 => 8,
                102 => 12,
                110 => 10,
                114 => 13,
                116 => 9,
                117 => self.hex4()?,
                _ => return Err(malformed("invalid JSON escape")),
            };
            if (0xd800..=0xdbff).contains(&c)
                && self.input.get(self.at..self.at + 2) == Some(&[92, 117])
            {
                let saved = self.at;
                self.at += 2;
                let lo = self.hex4()?;
                if (0xdc00..=0xdfff).contains(&lo) {
                    out.push(0x10000 + ((c - 0xd800) << 10) + (lo - 0xdc00));
                    continue;
                }
                self.at = saved;
            }
            out.push(c);
        }
        Ok(out)
    }
    fn hex4(&mut self) -> Result<u32> {
        let mut n = 0;
        for _ in 0..4 {
            let c = self
                .peek()
                .and_then(char::from_u32)
                .and_then(|c| c.to_digit(16))
                .ok_or_else(|| malformed("invalid Unicode escape"))?;
            self.at += 1;
            n = n * 16 + c;
        }
        Ok(n)
    }
    fn value(&mut self, depth: usize) -> Result<Value> {
        if depth > 512 {
            return Err(malformed("JSON nesting limit exceeded"));
        }
        self.ws();
        match self.peek() {
            Some(34) => Ok(Value::string(self.string()?)),
            Some(91) => {
                self.at += 1;
                let mut a = vec![];
                self.ws();
                if self.take(93) {
                    return Ok(Value::Array(a));
                }
                loop {
                    a.push(self.value(depth + 1)?);
                    self.ws();
                    if self.take(93) {
                        break;
                    }
                    if !self.take(44) {
                        return Err(malformed("expected array separator"));
                    }
                }
                Ok(Value::Array(a))
            }
            Some(123) => {
                self.at += 1;
                let mut m = Map::new();
                self.ws();
                if self.take(125) {
                    return Ok(Value::Object(m));
                }
                loop {
                    self.ws();
                    let k = Key(self.string()?);
                    self.ws();
                    if !self.take(58) {
                        return Err(malformed("expected member colon"));
                    }
                    m.insert(k, self.value(depth + 1)?);
                    self.ws();
                    if self.take(125) {
                        break;
                    }
                    if !self.take(44) {
                        return Err(malformed("expected object separator"));
                    }
                }
                Ok(Value::Object(m))
            }
            _ => {
                for (literal, value) in [
                    ("null", Value::Null),
                    ("true", Value::Bool(true)),
                    ("false", Value::Bool(false)),
                    (
                        "NaN",
                        Value::Number(Number::from_string_unchecked("NaN".into())),
                    ),
                    (
                        "Infinity",
                        Value::Number(Number::from_string_unchecked("Infinity".into())),
                    ),
                    (
                        "-Infinity",
                        Value::Number(Number::from_string_unchecked("-Infinity".into())),
                    ),
                ] {
                    let chars: Vec<_> = literal.chars().map(u32::from).collect();
                    if self.input.get(self.at..self.at + chars.len()) == Some(chars.as_slice()) {
                        self.at += chars.len();
                        return Ok(value);
                    }
                }
                let start = self.at;
                self.take(45);
                if !self.take(48) {
                    let digit = self.peek().is_some_and(|c| (49..=57).contains(&c));
                    if !digit {
                        return Err(malformed("expected JSON value"));
                    }
                    while self.peek().is_some_and(|c| (48..=57).contains(&c)) {
                        self.at += 1;
                    }
                }
                if self.peek() == Some(46)
                    && self
                        .input
                        .get(self.at + 1)
                        .is_some_and(|c| (48..=57).contains(c))
                {
                    self.at += 1;
                    while self.peek().is_some_and(|c| (48..=57).contains(&c)) {
                        self.at += 1;
                    }
                }
                if matches!(self.peek(), Some(69 | 101)) {
                    let saved = self.at;
                    self.at += 1;
                    if matches!(self.peek(), Some(43 | 45)) {
                        self.at += 1;
                    }
                    let digits = self.at;
                    while self.peek().is_some_and(|c| (48..=57).contains(&c)) {
                        self.at += 1;
                    }
                    if digits == self.at {
                        self.at = saved;
                    }
                }
                let number: String = self.input[start..self.at]
                    .iter()
                    .filter_map(|&c| char::from_u32(c))
                    .collect();
                Ok(Value::Number(Number::from_string_unchecked(number)))
            }
        }
    }
}
fn decoded(bytes: &[u8]) -> Result<Vec<u32>> {
    let (b, encoding) = if let Some(b) = bytes.strip_prefix(&[0, 0, 254, 255]) {
        (b, 4)
    } else if let Some(b) = bytes.strip_prefix(&[255, 254, 0, 0]) {
        (b, -4)
    } else if let Some(b) = bytes.strip_prefix(&[254, 255]) {
        (b, 2)
    } else if let Some(b) = bytes.strip_prefix(&[255, 254]) {
        (b, -2)
    } else if let Some(b) = bytes.strip_prefix(&[239, 187, 191]) {
        (b, 1)
    } else if bytes.len() >= 4 && bytes[0] == 0 {
        (bytes, if bytes[1] == 0 { 4 } else { 2 })
    } else if bytes.len() >= 4 && bytes[1] == 0 {
        (
            bytes,
            if bytes[2] == 0 && bytes[3] == 0 {
                -4
            } else {
                -2
            },
        )
    } else if bytes.len() == 2 && bytes[0] == 0 {
        (bytes, 2)
    } else if bytes.len() == 2 && bytes[1] == 0 {
        (bytes, -2)
    } else {
        (bytes, 1)
    };
    if encoding == 1 {
        return utf8_surrogatepass(b);
    }
    let width = if encoding == 2 || encoding == -2 {
        2
    } else {
        4
    };
    if b.len() % width != 0 {
        return Err(malformed("truncated Unicode input"));
    }
    let mut units = vec![];
    for chunk in b.chunks_exact(width) {
        let n = if encoding > 0 {
            chunk.iter().fold(0, |a, &c| (a << 8) | u32::from(c))
        } else {
            chunk.iter().rev().fold(0, |a, &c| (a << 8) | u32::from(c))
        };
        if n > 0x10_ffff {
            return Err(malformed("invalid Unicode scalar"));
        }
        units.push(n);
    }
    if width == 4 {
        return Ok(units);
    }
    let mut out = vec![];
    let mut i = 0;
    while i < units.len() {
        let c = units[i];
        if (0xd800..=0xdbff).contains(&c)
            && units
                .get(i + 1)
                .is_some_and(|n| (0xdc00..=0xdfff).contains(n))
        {
            out.push(0x10000 + ((c - 0xd800) << 10) + (units[i + 1] - 0xdc00));
            i += 2;
        } else {
            out.push(c);
            i += 1;
        }
    }
    Ok(out)
}
/// Decode a complete Python-compatible JSON value, including Unicode byte encodings.
pub fn from_slice(bytes: &[u8]) -> Result<Value> {
    let mut p = Parser {
        input: decoded(bytes)?,
        at: 0,
    };
    let v = p.value(0)?;
    p.ws();
    if p.at != p.input.len() {
        return Err(malformed("trailing JSON data"));
    }
    Ok(v)
}
/// Decode a complete UTF-8 JSON value with Python number and string extensions.
pub fn from_str(s: &str) -> Result<Value> {
    from_slice(s.as_bytes())
}

/// Clone a supported Rust value into the certificate JSON domain.
#[must_use]
pub fn to_value<T: Clone>(v: &T) -> Value
where
    Value: From<T>,
{
    Value::from(v.clone())
}

/// `raw_decode`'s prefix behavior, used only at a streamed member/step boundary.
pub fn prefix_utf8(bytes: &[u8]) -> Result<(Value, usize)> {
    let text = std::str::from_utf8(bytes).map_err(|_| malformed("invalid UTF-8"))?;
    let mut p = Parser {
        input: text.chars().map(u32::from).collect(),
        at: 0,
    };
    let v = p.value(0)?;
    let used = text.chars().take(p.at).map(char::len_utf8).sum();
    Ok((v, used))
}

fn utf8_surrogatepass(bytes: &[u8]) -> Result<Vec<u32>> {
    if let Ok(s) = std::str::from_utf8(bytes) {
        return Ok(s.chars().map(u32::from).collect());
    }
    let mut out = Vec::new();
    let mut i = 0;
    while i < bytes.len() {
        let first = bytes[i];
        let (width, mut code, min) = match first {
            0..=127 => (1, u32::from(first), 0),
            194..=223 => (2, u32::from(first & 31), 0x80),
            224..=239 => (3, u32::from(first & 15), 0x800),
            240..=244 => (4, u32::from(first & 7), 0x10000),
            _ => return Err(malformed("invalid UTF-8")),
        };
        for j in 1..width {
            let b = *bytes
                .get(i + j)
                .ok_or_else(|| malformed("truncated UTF-8"))?;
            if b & 0xc0 != 0x80 {
                return Err(malformed("invalid UTF-8 continuation"));
            }
            code = (code << 6) | u32::from(b & 63);
        }
        if code < min || code > 0x10_ffff {
            return Err(malformed("invalid UTF-8 scalar"));
        }
        out.push(code);
        i += width;
    }
    Ok(out)
}
