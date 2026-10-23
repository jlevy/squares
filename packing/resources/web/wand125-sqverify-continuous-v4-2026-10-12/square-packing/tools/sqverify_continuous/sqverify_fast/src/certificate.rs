//! Certificate admission: exact parsing, the D4 expansion, and the exact
//! premises (mass, shrink margin, net reach) that the coverage search assumes.

use std::collections::{HashMap, HashSet};
use std::fmt;
use std::io::Read;
use std::path::Path;

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{Signed, Zero};
use serde::de::{self, Deserializer, IgnoredAny, MapAccess, SeqAccess, Visitor};
use serde_json::Value;
use sha2::{Digest, Sha256};

use crate::exact::{enclose, parse_rational};
use crate::interval::Iv;

/// The largest container side admitted. The error budget of `SOUNDNESS.md`
/// (lemma F2) is proved for coordinates of magnitude at most `4 * MAX_SIDE`.
pub const MAX_SIDE: i64 = 1000;

/// Lemma F3's admission caps, which keep every intermediate of the search
/// finite: an expanded rectangle's density is at most `2^MAX_DENSITY_LOG2`, the
/// net has at most `MAX_ANGLE_COUNT` directions and its last half-angle tangent
/// is at most one half, and a certificate lists at most `MAX_PRIMITIVES` rows.
pub const MAX_DENSITY_LOG2: usize = 96;
/// See [`MAX_DENSITY_LOG2`].
pub const MAX_ANGLE_COUNT: u32 = 1 << 16;
/// See [`MAX_DENSITY_LOG2`].
pub const MAX_PRIMITIVES: usize = 1_000_000;

/// One expanded rectangle with its exact data.
#[derive(Clone, Debug)]
pub struct ExactRect {
    /// Left edge.
    pub x1: BigRational,
    /// Bottom edge.
    pub y1: BigRational,
    /// Right edge.
    pub x2: BigRational,
    /// Top edge.
    pub y2: BigRational,
    /// Uniform density on the rectangle.
    pub density: BigRational,
}

/// One expanded rectangle as binary64 enclosures, for the interval search.
#[derive(Clone, Copy, Debug)]
pub struct Rect {
    /// Enclosure of the left edge.
    pub x1: Iv,
    /// Enclosure of the right edge.
    pub x2: Iv,
    /// Enclosure of the bottom edge.
    pub y1: Iv,
    /// Enclosure of the top edge.
    pub y2: Iv,
    /// Enclosure of the density.
    pub rho: Iv,
    /// Enclosure of the mass `density * area`.
    pub mass: Iv,
    /// Approximate centre abscissa, for classification with slack.
    pub mx: f64,
    /// Approximate centre ordinate.
    pub my: f64,
    /// Approximate half-width.
    pub wx: f64,
    /// Approximate half-height.
    pub wy: f64,
}

/// One expanded point mass, exact.
#[derive(Clone, Debug)]
pub struct ExactPoint {
    /// Abscissa.
    pub x: BigRational,
    /// Ordinate.
    pub y: BigRational,
    /// Mass.
    pub mass: BigRational,
}

/// One expanded segment of uniform linear density, exact.
#[derive(Clone, Debug)]
pub struct ExactSegment {
    /// First endpoint.
    pub p0: (BigRational, BigRational),
    /// Second endpoint.
    pub p1: (BigRational, BigRational),
    /// Mass, spread uniformly by length.
    pub mass: BigRational,
}

/// A point mass for the interval search: coordinates within one unit in the
/// last place (lemma F2's slack covers them), mass enclosed.
#[derive(Clone, Copy, Debug)]
pub struct Point {
    /// Approximate abscissa.
    pub x: f64,
    /// Approximate ordinate.
    pub y: f64,
    /// Enclosure of the mass.
    pub mass: Iv,
}

/// A segment for the interval search.
#[derive(Clone, Copy, Debug)]
pub struct Segment {
    /// Approximate first endpoint.
    pub x0: f64,
    /// Approximate first endpoint.
    pub y0: f64,
    /// Approximate second endpoint.
    pub x1: f64,
    /// Approximate second endpoint.
    pub y1: f64,
    /// Enclosure of the mass.
    pub mass: Iv,
}

/// Which centre domain the certificate's format declares (spec 1.5).
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Domain {
    /// Every centre whose shrunk square lies in the container: `[a_r, L - a_r]^2`,
    /// `a_r = B (c_r + s_r) / 2` (formats T and L).
    Tokoharu,
    /// Every centre of a unit square whose orientation the net assigns to the
    /// node: `[rho(a_r), L - rho(a_r)]^2` (format M).
    PerBin,
}

/// An admitted certificate.
#[derive(Clone, Debug)]
pub struct Certificate {
    /// The count the certificate refutes.
    pub n: u64,
    /// Container side `L`.
    pub side: BigRational,
    /// Shrunk square side `B`.
    pub core: BigRational,
    /// Net step `D`.
    pub step: BigRational,
    /// Number of net directions.
    pub angle_count: u32,
    /// Exact total mass.
    pub mass: BigRational,
    /// Number of positive-weight source rectangles.
    pub source_rectangles: usize,
    /// The expanded, merged rectangles with exact data.
    pub exact: Vec<ExactRect>,
    /// The same rectangles as enclosures.
    pub rects: Vec<Rect>,
    /// SHA-256 of the input bytes as read (before decompression).
    pub input_sha256: String,
    /// The coverage threshold the certificate declares, if any.
    pub declared_threshold: Option<BigRational>,
    /// The format: `T` (Tokoharu rectangles), `M` (mixed rectangles) or `L`
    /// (points, segments and rectangles).
    pub format: &'static str,
    /// The centre domain the format declares.
    pub domain: Domain,
    /// Expanded, merged point masses.
    pub exact_points: Vec<ExactPoint>,
    /// The same, for the search.
    pub points: Vec<Point>,
    /// Expanded, merged segments.
    pub exact_segments: Vec<ExactSegment>,
    /// The same, for the search.
    pub segments: Vec<Segment>,
}

/// One orbit representative as a format lists it.
enum Source {
    Rect([BigRational; 4], BigRational),
    Point([BigRational; 2], BigRational),
    Segment([BigRational; 4], BigRational),
}

fn rationals(value: &Value, count: usize, field: &str) -> Result<Vec<BigRational>, AdmissionError> {
    let Some(items) = value.as_array().filter(|items| items.len() == count) else {
        return refuse(format!("{field} needs {count} numbers"));
    };
    items.iter().map(|item| rational_of(item, field)).collect()
}

fn array<'a>(
    object: &'a serde_json::Map<String, Value>,
    key: &str,
) -> Result<&'a Vec<Value>, AdmissionError> {
    object
        .get(key)
        .and_then(Value::as_array)
        .ok_or_else(|| AdmissionError(format!("missing {key} array")))
}

/// The orbit representatives of each format, with the format's name, domain
/// and declared threshold.
fn sources(
    object: &serde_json::Map<String, Value>,
) -> Result<(&'static str, Domain, Vec<Source>), AdmissionError> {
    let mut out = Vec::new();
    if object.get("schema").and_then(Value::as_str) == Some("point_line_rectangle_v1") {
        let net = object
            .get("net")
            .and_then(Value::as_object)
            .ok_or(AdmissionError("format L needs its net block".into()))?;
        let step = rational_of(net.get("step").unwrap_or(&Value::Null), "net.step")?;
        if step != ratio(83, 40_000) || net.get("last").and_then(Value::as_u64) != Some(200) {
            return refuse("format L's net must be step 83/40000, last 200");
        }
        for (index, primitive) in array(object, "primitives")?.iter().enumerate() {
            let field = format!("primitive {index}");
            let kind = primitive.get("kind").and_then(Value::as_str);
            let geometry = primitive.get("geometry").unwrap_or(&Value::Null);
            let mass = rational_of(primitive.get("mass").unwrap_or(&Value::Null), &field)?;
            out.push(match kind {
                Some("point") => {
                    let g = rationals(geometry, 2, &field)?;
                    Source::Point([g[0].clone(), g[1].clone()], mass)
                }
                Some("segment") => {
                    let g = rationals(geometry, 4, &field)?;
                    Source::Segment(
                        [g[0].clone(), g[1].clone(), g[2].clone(), g[3].clone()],
                        mass,
                    )
                }
                Some("rectangle") => {
                    let g = rationals(geometry, 4, &field)?;
                    Source::Rect(
                        [g[0].clone(), g[1].clone(), g[2].clone(), g[3].clone()],
                        mass,
                    )
                }
                _ => return refuse(format!("{field} has an unknown kind")),
            });
        }
        return Ok(("L", Domain::Tokoharu, out));
    }
    let rows = array(object, "rectangles")?;
    if rows.first().is_some_and(Value::is_object) {
        if !array(object, "points")?.is_empty() {
            return refuse("format M with a nonempty points list is refused (spec 1.4)");
        }
        for (index, row) in rows.iter().enumerate() {
            let field = format!("rectangle {index}");
            let g = rationals(row.get("rectangle").unwrap_or(&Value::Null), 4, &field)?;
            let mass = rational_of(row.get("mass").unwrap_or(&Value::Null), &field)?;
            out.push(Source::Rect(
                [g[0].clone(), g[1].clone(), g[2].clone(), g[3].clone()],
                mass,
            ));
        }
        return Ok(("M", Domain::PerBin, out));
    }
    let weights = array(object, "weights")?;
    if rows.len() != weights.len() {
        return refuse("rectangles and weights differ in length");
    }
    for (index, (row, weight)) in rows.iter().zip(weights).enumerate() {
        let weight = rational_of(weight, &format!("weight {index}"))?;
        if weight.is_zero() {
            // A zero weight puts no mass anywhere, so its coordinates cannot matter.
            if row.as_array().is_none_or(|r| r.len() != 4) {
                return refuse(format!("rectangle {index} needs four coordinates"));
            }
            continue;
        }
        let g = rationals(row, 4, &format!("rectangle {index}"))?;
        out.push(Source::Rect(
            [g[0].clone(), g[1].clone(), g[2].clone(), g[3].clone()],
            weight,
        ));
    }
    Ok(("T", Domain::Tokoharu, out))
}

/// The eight images of a point under the symmetries of `[0, L]^2`.
fn point_images(side: &BigRational, x: &BigRational, y: &BigRational) -> [[BigRational; 2]; 8] {
    let rx = side - x;
    let ry = side - y;
    [
        [x.clone(), y.clone()],
        [rx.clone(), y.clone()],
        [x.clone(), ry.clone()],
        [rx.clone(), ry.clone()],
        [y.clone(), x.clone()],
        [ry.clone(), x.clone()],
        [y.clone(), rx.clone()],
        [ry, rx],
    ]
}

/// An admission refusal.
#[derive(Debug)]
pub struct AdmissionError(pub String);

impl fmt::Display for AdmissionError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(&self.0)
    }
}

impl std::error::Error for AdmissionError {}

fn refuse<T>(message: impl Into<String>) -> Result<T, AdmissionError> {
    Err(AdmissionError(message.into()))
}

/// A visitor that walks a JSON document and refuses any object with a repeated
/// key, so that no two readers can disagree about which value a key holds.
struct DuplicateKeyCheck;

impl<'de> de::Deserialize<'de> for DuplicateKeyCheck {
    fn deserialize<D: Deserializer<'de>>(deserializer: D) -> Result<Self, D::Error> {
        deserializer.deserialize_any(DuplicateKeyVisitor)
    }
}

struct DuplicateKeyVisitor;

impl<'de> Visitor<'de> for DuplicateKeyVisitor {
    type Value = DuplicateKeyCheck;

    fn expecting(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str("any JSON value")
    }

    fn visit_bool<E>(self, _: bool) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_i64<E>(self, _: i64) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_u64<E>(self, _: u64) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_f64<E>(self, _: f64) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_str<E>(self, _: &str) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_string<E>(self, _: String) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_unit<E>(self) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_none<E>(self) -> Result<Self::Value, E> {
        Ok(DuplicateKeyCheck)
    }
    fn visit_seq<A: SeqAccess<'de>>(self, mut seq: A) -> Result<Self::Value, A::Error> {
        while seq.next_element::<DuplicateKeyCheck>()?.is_some() {}
        Ok(DuplicateKeyCheck)
    }
    fn visit_map<A: MapAccess<'de>>(self, mut map: A) -> Result<Self::Value, A::Error> {
        let mut seen = HashSet::new();
        while let Some(key) = map.next_key::<String>()? {
            if !seen.insert(key.clone()) {
                return Err(de::Error::custom(format!("duplicate JSON key {key:?}")));
            }
            if key == "$serde_json::private::Number" {
                map.next_value::<IgnoredAny>()?;
            } else {
                map.next_value::<DuplicateKeyCheck>()?;
            }
        }
        Ok(DuplicateKeyCheck)
    }
}

/// Read a candidate file, plain or gzip, returning its raw bytes and decoded JSON.
///
/// # Errors
///
/// Refuses unreadable, oversized, non-JSON or duplicate-key input.
pub fn read_json(path: &Path) -> Result<(Vec<u8>, Value), AdmissionError> {
    let raw = std::fs::read(path)
        .map_err(|error| AdmissionError(format!("cannot read {}: {error}", path.display())))?;
    if raw.len() > 64 * 1024 * 1024 {
        return refuse("candidate exceeds 64 MiB");
    }
    let decoded = if raw.starts_with(&[0x1f, 0x8b]) {
        // One gzip member and nothing after it, as Python's reader requires: a
        // second member or trailing bytes would let two readers see two inputs.
        const LIMIT: u64 = 512 * 1024 * 1024;
        let mut text = Vec::new();
        let mut decoder = flate2::bufread::GzDecoder::new(raw.as_slice());
        Read::by_ref(&mut decoder)
            .take(LIMIT)
            .read_to_end(&mut text)
            .map_err(|error| AdmissionError(format!("bad gzip: {error}")))?;
        if text.len() as u64 >= LIMIT {
            return refuse("decompressed candidate exceeds 512 MiB");
        }
        if !decoder.into_inner().is_empty() {
            return refuse("gzip input has bytes after its first member");
        }
        text
    } else {
        raw.clone()
    };
    serde_json::from_slice::<DuplicateKeyCheck>(&decoded)
        .map_err(|error| AdmissionError(format!("candidate JSON refused: {error}")))?;
    let value: Value = serde_json::from_slice(&decoded)
        .map_err(|error| AdmissionError(format!("candidate JSON refused: {error}")))?;
    Ok((raw, value))
}

fn rational_of(value: &Value, field: &str) -> Result<BigRational, AdmissionError> {
    let token = match value {
        Value::Number(number) => number.to_string(),
        Value::String(text) => text.clone(),
        _ => return refuse(format!("{field} is not a number or rational string")),
    };
    parse_rational(&token).map_err(|error| AdmissionError(format!("{field}: {error}")))
}

fn ratio(p: i64, q: i64) -> BigRational {
    BigRational::new(BigInt::from(p), BigInt::from(q))
}

/// The eight images of `[x1,x2] x [y1,y2]` under the symmetries of `[0,L]^2`.
#[must_use]
pub fn d4_images(
    side: &BigRational,
    x1: &BigRational,
    y1: &BigRational,
    x2: &BigRational,
    y2: &BigRational,
) -> [[BigRational; 4]; 8] {
    let rx1 = side - x2;
    let rx2 = side - x1;
    let ry1 = side - y2;
    let ry2 = side - y1;
    [
        [x1.clone(), y1.clone(), x2.clone(), y2.clone()],
        [rx1.clone(), y1.clone(), rx2.clone(), y2.clone()],
        [x1.clone(), ry1.clone(), x2.clone(), ry2.clone()],
        [rx1.clone(), ry1.clone(), rx2.clone(), ry2.clone()],
        [y1.clone(), x1.clone(), y2.clone(), x2.clone()],
        [ry1.clone(), x1.clone(), ry2.clone(), x2.clone()],
        [y1.clone(), rx1.clone(), y2.clone(), rx2.clone()],
        [ry1, rx1, ry2, rx2],
    ]
}

/// The upper end of the reduced centre domain `[L/2, upper]` at net index
/// `index`, by the certificate's declared domain (spec 1.5).
///
/// # Errors
///
/// Refuses a domain with no interior (`upper <= L/2`).
pub fn domain_upper(cert: &Certificate, index: u32) -> Result<BigRational, String> {
    let two = ratio(2, 1);
    let one = ratio(1, 1);
    let upper = match cert.domain {
        Domain::Tokoharu => {
            let (c, s) = direction(&cert.step, index);
            &cert.side - &cert.core * (c + s) / &two
        }
        Domain::PerBin => {
            let t = &cert.step * BigRational::from_integer(BigInt::from(index));
            let half_step = &cert.step / &two;
            let a = if t > half_step {
                t - half_step
            } else {
                BigRational::zero()
            };
            let rho = (&one + &two * &a - &a * &a) / (&two * (&one + &a * &a));
            &cert.side - rho
        }
    };
    if upper <= &cert.side / &two {
        return Err(format!("the centre domain at index {index} is empty"));
    }
    Ok(upper)
}

/// The net direction's exact cosine and sine, `t = r D`, `theta = 2 atan t`.
#[must_use]
pub fn direction(step: &BigRational, index: u32) -> (BigRational, BigRational) {
    let t = step * BigRational::from_integer(BigInt::from(index));
    let one = BigRational::from_integer(BigInt::from(1));
    let denominator = &one + &t * &t;
    let cosine = (&one - &t * &t) / &denominator;
    let sine = (BigRational::from_integer(BigInt::from(2)) * &t) / &denominator;
    (cosine, sine)
}

/// Admit a candidate value for count `n` (and, if given, side `expected_side`).
///
/// # Errors
///
/// Refuses any malformed field and any failed exact premise: the mass must lie
/// strictly between zero and `n`, `0 < B < 1`, `B (1 + D) < 1`, the net must reach
/// past `pi/4`, and every positive rectangle must be a nondegenerate rectangle
/// inside the container.
pub fn admit(
    raw: &[u8],
    value: &Value,
    n: u64,
    expected_side: Option<&BigRational>,
) -> Result<Certificate, AdmissionError> {
    let Value::Object(object) = value else {
        return refuse("candidate JSON must be an object");
    };
    if let Some(declared) = object.get("n")
        && declared.as_u64() != Some(n)
    {
        return refuse(format!(
            "candidate n {declared} does not match requested n {n}"
        ));
    }
    let side = rational_of(
        object.get("L").ok_or(AdmissionError("missing L".into()))?,
        "L",
    )?;
    let core = rational_of(
        object.get("B").ok_or(AdmissionError("missing B".into()))?,
        "B",
    )?;
    if let Some(expected) = expected_side
        && &side != expected
    {
        return refuse(format!(
            "candidate side {side} is not the requested {expected}"
        ));
    }
    let mut step = ratio(83, 40_000);
    let mut angle_count: u32 = 201;
    if let Some(metadata) = object.get("certificate") {
        let Value::Object(metadata) = metadata else {
            return refuse("certificate metadata must be an object");
        };
        if let Some(d) = metadata.get("D") {
            step = rational_of(d, "certificate.D")?;
        }
        if let Some(count) = metadata.get("angle_count") {
            angle_count = count
                .as_u64()
                .and_then(|c| u32::try_from(c).ok())
                .ok_or(AdmissionError("bad angle_count".into()))?;
        }
        for (key, mine) in [("L", &side), ("B", &core)] {
            if let Some(declared) = metadata.get(key)
                && &rational_of(declared, key)? != mine
            {
                return refuse(format!(
                    "certificate metadata {key} disagrees with the candidate"
                ));
            }
        }
    }
    // A format M candidate may declare its own uniform net as `proof_net:
    // {step, last}`, meaning t_r = r * step for r = 0..=last. The net is then
    // part of the candidate (its digest covers it), not metadata, so finding
    // TI-3 still holds: metadata never changes a net. Lemmas N1-N3 and D are
    // written for a general step D, and admission below checks B (1 + D) < 1,
    // the per-bin tangent form, the endpoint and lemma F3's last <= 1/2.
    let mut declared_net = false;
    if let Some(net) = object.get("proof_net") {
        let Value::Object(net) = net else {
            return refuse("proof_net must be an object");
        };
        if net.len() != 2 || !net.contains_key("step") || !net.contains_key("last") {
            return refuse("proof_net must have exactly the fields step and last");
        }
        if object.get("certificate").is_some() {
            return refuse("proof_net and certificate metadata may not both set the net");
        }
        step = rational_of(&net["step"], "proof_net.step")?;
        let last = net["last"]
            .as_u64()
            .and_then(|l| u32::try_from(l).ok())
            .and_then(|l| l.checked_add(1))
            .ok_or(AdmissionError("bad proof_net.last".into()))?;
        angle_count = last;
        declared_net = true;
    }
    let zero = BigRational::zero();
    let one = ratio(1, 1);
    if !(side.is_positive() && side <= ratio(MAX_SIDE, 1)) {
        return refuse(format!("side {side} outside (0, {MAX_SIDE}]"));
    }
    if !(core > zero && core < one) {
        return refuse("B must lie strictly between 0 and 1");
    }
    if &side * &side < ratio(2, 1) * &core * &core {
        return refuse("L^2 < 2 B^2: the centre domain could be empty");
    }
    if !(step.is_positive() && (2..=MAX_ANGLE_COUNT).contains(&angle_count)) {
        return refuse(format!(
            "the net needs a positive step and 2 to {MAX_ANGLE_COUNT} directions"
        ));
    }
    if &core * (&one + &step) >= one {
        return refuse("B (1 + D) >= 1: the shrunk square need not fit inside the unit square");
    }
    let last = &step * BigRational::from_integer(BigInt::from(angle_count - 1));
    if &last * &last + ratio(2, 1) * &last - &one <= zero {
        return refuse("the net does not reach past pi/4");
    }
    if last > ratio(1, 2) {
        return refuse("the net's last half-angle tangent exceeds 1/2 (lemma F3)");
    }

    let (format, domain, listed) = sources(object)?;
    // Formats M and L fix the net unless a format M candidate declares
    // `proof_net`; metadata may restate the fixed net but never change it.
    if declared_net && format != "M" {
        return refuse("proof_net is accepted only for format M");
    }
    if format != "T" && !declared_net && (step != ratio(83, 40_000) || angle_count != 201) {
        return refuse(format!(
            "format {format}'s net is step 83/40000 with 201 directions; certificate \
             metadata may not change it"
        ));
    }
    // The per-bin domain assigns a half-angle tangent within D/2 of t_r, so the
    // angle may differ from theta_r by up to 2 atan(D/2), whose tangent is
    // D/(1 - D^2/4). Lemma N3 needs only B(1 + D) < 1 (by the half-angle form),
    // and admission also checks the bound a tangent-based argument would need.
    if domain == Domain::PerBin {
        let quarter = &step * &step / ratio(4, 1);
        if &core * (&one + &step / (&one - quarter)) >= one {
            return refuse("B (1 + D / (1 - D^2/4)) >= 1 for the per-bin domain");
        }
    }
    if listed.len() > MAX_PRIMITIVES {
        return refuse("too many primitives");
    }
    let inside = |q: &BigRational| &zero <= q && q <= &side;
    let mut merged: HashMap<[BigRational; 4], BigRational> = HashMap::new();
    let mut order: Vec<[BigRational; 4]> = Vec::new();
    let mut point_mass: HashMap<[BigRational; 2], BigRational> = HashMap::new();
    let mut point_order: Vec<[BigRational; 2]> = Vec::new();
    let mut segment_mass: HashMap<[BigRational; 4], BigRational> = HashMap::new();
    let mut segment_order: Vec<[BigRational; 4]> = Vec::new();
    let mut mass = BigRational::zero();
    let mut source_rectangles = 0usize;
    let eight = ratio(8, 1);
    for (index, source) in listed.iter().enumerate() {
        let weight = match source {
            Source::Rect(_, w) | Source::Point(_, w) | Source::Segment(_, w) => w,
        };
        if weight.is_negative() {
            return refuse(format!("mass of primitive {index} is negative"));
        }
        mass += weight;
        if weight.is_zero() {
            continue;
        }
        let share = weight / &eight;
        match source {
            Source::Rect([x1, y1, x2, y2], _) => {
                if !(inside(x1) && x1 < x2 && inside(x2) && inside(y1) && y1 < y2 && inside(y2)) {
                    return refuse(format!(
                        "positive rectangle {index} is degenerate or outside [0, L]^2"
                    ));
                }
                source_rectangles += 1;
                let density = &share / ((x2 - x1) * (y2 - y1));
                for image in d4_images(&side, x1, y1, x2, y2) {
                    if let Some(total) = merged.get_mut(&image) {
                        *total += &density;
                    } else {
                        order.push(image.clone());
                        merged.insert(image, density.clone());
                    }
                }
            }
            Source::Point([x, y], _) => {
                if !(inside(x) && inside(y)) {
                    return refuse(format!("point {index} is outside [0, L]^2"));
                }
                for image in point_images(&side, x, y) {
                    if let Some(total) = point_mass.get_mut(&image) {
                        *total += &share;
                    } else {
                        point_order.push(image.clone());
                        point_mass.insert(image, share.clone());
                    }
                }
            }
            Source::Segment([x0, y0, x1, y1], _) => {
                if !(inside(x0) && inside(y0) && inside(x1) && inside(y1)) {
                    return refuse(format!("segment {index} is outside [0, L]^2"));
                }
                if x0 == x1 && y0 == y1 {
                    return refuse(format!("segment {index} has length zero"));
                }
                let first = point_images(&side, x0, y0);
                let second = point_images(&side, x1, y1);
                for (a, b) in first.into_iter().zip(second) {
                    // The same segment either way round is one key.
                    let key = if (&a[0], &a[1]) <= (&b[0], &b[1]) {
                        [a[0].clone(), a[1].clone(), b[0].clone(), b[1].clone()]
                    } else {
                        [b[0].clone(), b[1].clone(), a[0].clone(), a[1].clone()]
                    };
                    if let Some(total) = segment_mass.get_mut(&key) {
                        *total += &share;
                    } else {
                        segment_order.push(key.clone());
                        segment_mass.insert(key, share.clone());
                    }
                }
            }
        }
    }
    if let Some(declared) = object.get("total_mass")
        && rational_of(declared, "total_mass")? != mass
    {
        return refuse("total_mass is not the exact sum of the masses");
    }
    if !(mass.is_positive() && mass < BigRational::from_integer(BigInt::from(n))) {
        return refuse(format!(
            "exact mass {mass} is not strictly between 0 and n = {n}"
        ));
    }
    let mut exact = Vec::with_capacity(order.len());
    let mut rects = Vec::with_capacity(order.len());
    let mut integrated = BigRational::zero();
    let max_density = BigRational::from_integer(BigInt::from(1) << MAX_DENSITY_LOG2);
    for key in order {
        let density = merged[&key].clone();
        if density > max_density {
            return refuse(format!(
                "a rectangle's density exceeds 2^{MAX_DENSITY_LOG2} (lemma F3)"
            ));
        }
        let [x1, y1, x2, y2] = key;
        let image_mass = &density * (&x2 - &x1) * (&y2 - &y1);
        let rect = ExactRect {
            x1,
            y1,
            x2,
            y2,
            density,
        };
        rects.push(float_rect(&rect, &image_mass).map_err(AdmissionError)?);
        integrated += image_mass;
        exact.push(rect);
    }
    let mut exact_points = Vec::with_capacity(point_order.len());
    let mut points = Vec::with_capacity(point_order.len());
    for key in point_order {
        let mass = point_mass[&key].clone();
        integrated += &mass;
        let [x, y] = key;
        points.push(Point {
            x: crate::exact::approx(&x).map_err(AdmissionError)?,
            y: crate::exact::approx(&y).map_err(AdmissionError)?,
            mass: enclose(&mass).map_err(AdmissionError)?,
        });
        exact_points.push(ExactPoint { x, y, mass });
    }
    let mut exact_segments = Vec::with_capacity(segment_order.len());
    let mut segments = Vec::with_capacity(segment_order.len());
    for key in segment_order {
        let mass = segment_mass[&key].clone();
        integrated += &mass;
        let [x0, y0, x1, y1] = key;
        let approx = |q: &BigRational| crate::exact::approx(q).map_err(AdmissionError);
        segments.push(Segment {
            x0: approx(&x0)?,
            y0: approx(&y0)?,
            x1: approx(&x1)?,
            y1: approx(&y1)?,
            mass: enclose(&mass).map_err(AdmissionError)?,
        });
        exact_segments.push(ExactSegment {
            p0: (x0, y0),
            p1: (x1, y1),
            mass,
        });
    }
    if integrated != mass {
        return refuse("the D4 expansion does not integrate to the declared mass");
    }
    // Formats M and L claim coverage one (spec 1.4); T declares its threshold.
    let declared_threshold = if format == "T" {
        object
            .get("coverage_lower_bound_exact")
            .map(|value| rational_of(value, "coverage_lower_bound_exact"))
            .transpose()?
    } else {
        Some(ratio(1, 1))
    };
    let input_sha256 = Sha256::digest(raw)
        .iter()
        .fold(String::new(), |mut text, byte| {
            use std::fmt::Write;
            let _ = write!(text, "{byte:02x}");
            text
        });
    Ok(Certificate {
        n,
        side,
        core,
        step,
        angle_count,
        mass,
        source_rectangles,
        exact,
        rects,
        input_sha256,
        declared_threshold,
        format,
        domain,
        exact_points,
        points,
        exact_segments,
        segments,
    })
}

/// Binary64 data for one exact rectangle. The edges, density and mass are
/// tight enclosures; the centre and half-sizes are approximations within a
/// few units in the last place, which lemma F2's slack covers.
///
/// # Errors
///
/// Returns a message if a value lies outside the binary64 range.
pub fn float_rect(rect: &ExactRect, mass: &BigRational) -> Result<Rect, String> {
    let x1 = enclose(&rect.x1)?;
    let x2 = enclose(&rect.x2)?;
    let y1 = enclose(&rect.y1)?;
    let y2 = enclose(&rect.y2)?;
    let rho = enclose(&rect.density)?;
    let mass = enclose(mass)?;
    Ok(Rect {
        x1,
        x2,
        y1,
        y2,
        rho,
        mass,
        mx: f64::midpoint(x1.lo, x2.lo),
        my: f64::midpoint(y1.lo, y2.lo),
        wx: 0.5 * (x2.lo - x1.lo),
        wy: 0.5 * (y2.lo - y1.lo),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn images_preserve_area_and_cover_the_orbit() {
        let side = ratio(10, 1);
        let images = d4_images(
            &side,
            &ratio(1, 1),
            &ratio(2, 1),
            &ratio(3, 1),
            &ratio(7, 1),
        );
        let unique: HashSet<_> = images.iter().cloned().collect();
        assert_eq!(unique.len(), 8);
        for [x1, y1, x2, y2] in &images {
            assert_eq!((x2 - x1) * (y2 - y1), ratio(10, 1));
        }
    }

    #[test]
    fn net_directions_are_rational_rotations() {
        let (c, s) = direction(&ratio(83, 40_000), 7);
        assert_eq!(&c * &c + &s * &s, ratio(1, 1));
        assert!(c.is_positive() && s.is_positive());
    }
}
