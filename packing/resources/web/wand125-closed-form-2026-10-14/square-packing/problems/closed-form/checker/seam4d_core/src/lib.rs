//! Rust implementation of seam4d.bound().
//!
//! Mirrors the Python reference bound() and its geometry helpers.
//! All arithmetic uses exact rug::Rational (GMP), without floating point.
//! Each function mirrors its Python counterpart, including vertex order and degenerate cases.
//! Python exposes the direct port as Family.bound_ref; Family.bound uses the optimized implementation.
//! Integer homogeneous coordinates preserve points and signs; cross-checks compare both versions with Python.

use rug::{Integer, Rational};
use std::cmp::Ordering;

pub mod b3d;
mod fast;

pub type Q = Rational;
type Pt = (Q, Q);
type HalfPlane = ((Q, Q), Q);

// ---------------------------------------------------------------- Arithmetic helpers

#[inline]
fn add(a: &Q, b: &Q) -> Q {
    Q::from(a + b)
}
#[inline]
fn sub(a: &Q, b: &Q) -> Q {
    Q::from(a - b)
}
#[inline]
fn mul(a: &Q, b: &Q) -> Q {
    Q::from(a * b)
}
#[inline]
fn div(a: &Q, b: &Q) -> Q {
    Q::from(a / b)
}
#[inline]
fn neg(a: &Q) -> Q {
    Q::from(-a)
}
#[inline]
fn absq(a: &Q) -> Q {
    Q::from(a.abs_ref())
}
#[inline]
fn half(a: &Q) -> Q {
    Q::from(a / 2u32)
}
#[inline]
fn qi(n: i64) -> Q {
    Q::from(n)
}
#[inline]
fn qf(n: i64, d: i64) -> Q {
    Q::from((n, d))
}
#[inline]
fn dot(a: &(Q, Q), x: &Q, y: &Q) -> Q {
    let mut r = mul(&a.0, x);
    r += Q::from(&a.1 * y);
    r
}

/// Python int(): truncate toward zero.
fn trunc_i64(r: &Q) -> i64 {
    let t = Q::from(r.trunc_ref());
    sat_i64(t.numer())
}
/// Python math.floor().
fn floor_i64(r: &Q) -> i64 {
    let t = Q::from(r.floor_ref());
    sat_i64(t.numer())
}
fn sat_i64(z: &Integer) -> i64 {
    match z.to_i64() {
        Some(v) => v,
        None => {
            if z.cmp0() == Ordering::Less {
                i64::MIN / 4
            } else {
                i64::MAX / 4
            }
        }
    }
}

// ---------------------------------------------------------------- Reference geometry helpers

fn cs(u: &Q) -> (Q, Q) {
    let u2 = mul(u, u);
    let d = add(&qi(1), &u2);
    (div(&sub(&qi(1), &u2), &d), div(&Q::from(u * 2u32), &d))
}

fn angular_core_halfplanes(u0: &Q, u1: &Q) -> Vec<HalfPlane> {
    let (c0, s0) = cs(u0);
    let (c1, s1) = cs(u1);
    let mut hp = Vec::with_capacity(12);
    for k in 0..4 {
        let mut n0 = (c0.clone(), s0.clone());
        let mut n1 = (c1.clone(), s1.clone());
        for _ in 0..k {
            n0 = (neg(&n0.1), n0.0.clone());
            n1 = (neg(&n1.1), n1.0.clone());
        }
        hp.push((n0.clone(), qf(1, 2)));
        if u0 != u1 {
            hp.push((n1.clone(), qf(1, 2)));
            let p0 = (half(&n0.0), half(&n0.1));
            let m = (add(&n0.0, &n1.0), add(&n0.1, &n1.1));
            let b = dot(&m, &p0.0, &p0.1);
            hp.push((m, b));
        }
    }
    hp
}

/// Sutherland–Hodgman: retain a.x <= b.
fn clip_poly(poly: &[Pt], a: &(Q, Q), b: &Q) -> Vec<Pt> {
    let n = poly.len();
    let mut out = Vec::with_capacity(n + 2);
    for i in 0..n {
        let p = &poly[i];
        let q = &poly[(i + 1) % n];
        let fp = sub(&dot(a, &p.0, &p.1), b);
        let fq = sub(&dot(a, &q.0, &q.1), b);
        let sp = fp.cmp0();
        let sq = fq.cmp0();
        if sp != Ordering::Greater {
            out.push(p.clone());
        }
        if (sp == Ordering::Less && sq == Ordering::Greater)
            || (sq == Ordering::Less && sp == Ordering::Greater)
        {
            let t = div(&fp, &sub(&fp, &fq));
            out.push((
                add(&p.0, &mul(&t, &sub(&q.0, &p.0))),
                add(&p.1, &mul(&t, &sub(&q.1, &p.1))),
            ));
        }
    }
    out
}

fn halfplanes_to_poly(hp: &[HalfPlane], big: &Q) -> Vec<Pt> {
    let nb = neg(big);
    let mut poly = vec![
        (nb.clone(), nb.clone()),
        (big.clone(), nb.clone()),
        (big.clone(), big.clone()),
        (nb.clone(), big.clone()),
    ];
    for (a, b) in hp {
        poly = clip_poly(&poly, a, b);
        if poly.is_empty() {
            return poly;
        }
    }
    poly
}

fn area(poly: &[Pt]) -> Q {
    let n = poly.len();
    let mut s = qi(0);
    for i in 0..n {
        let p = &poly[i];
        let q = &poly[(i + 1) % n];
        s += mul(&p.0, &q.1);
        s -= mul(&q.0, &p.1);
    }
    half(&s)
}

fn cross(o: &Pt, a: &Pt, b: &Pt) -> Q {
    sub(
        &mul(&sub(&a.0, &o.0), &sub(&b.1, &o.1)),
        &mul(&sub(&a.1, &o.1), &sub(&b.0, &o.0)),
    )
}

/// Monotone chain on sorted(set(pts)), matching Python and discarding collinear points.
fn hull(mut pts: Vec<Pt>) -> Vec<Pt> {
    pts.sort_by(|a, b| a.0.cmp(&b.0).then_with(|| a.1.cmp(&b.1)));
    pts.dedup();
    if pts.len() < 3 {
        return pts;
    }
    let mut lo: Vec<Pt> = Vec::new();
    for p in pts.iter() {
        while lo.len() >= 2 && cross(&lo[lo.len() - 2], &lo[lo.len() - 1], p).cmp0() != Ordering::Greater {
            lo.pop();
        }
        lo.push(p.clone());
    }
    let mut up: Vec<Pt> = Vec::new();
    for p in pts.iter().rev() {
        while up.len() >= 2 && cross(&up[up.len() - 2], &up[up.len() - 1], p).cmp0() != Ordering::Greater {
            up.pop();
        }
        up.push(p.clone());
    }
    lo.pop();
    up.pop();
    lo.extend(up);
    lo
}

fn outer_hull(u0: &Q, u1: &Q, cx: &Q, cy: &Q, rx: &Q, ry: &Q) -> Vec<Pt> {
    let (c0, s0) = cs(u0);
    let (c1, s1) = cs(u1);
    let mut pts: Vec<Pt> = Vec::with_capacity(12);
    let h = qf(1, 2);
    for (ex, ey) in [(1i64, 1i64), (-1, 1), (-1, -1), (1, -1)] {
        let (ex, ey) = (qi(ex), qi(ey));
        let v0 = (
            half(&sub(&mul(&c0, &ex), &mul(&s0, &ey))),
            half(&add(&mul(&s0, &ex), &mul(&c0, &ey))),
        );
        let v1 = (
            half(&sub(&mul(&c1, &ex), &mul(&s1, &ey))),
            half(&add(&mul(&s1, &ex), &mul(&c1, &ey))),
        );
        let det = sub(&mul(&v0.0, &v1.1), &mul(&v0.1, &v1.0));
        pts.push(v0.clone());
        pts.push(v1.clone());
        if det.cmp0() != Ordering::Equal {
            let tx = div(&sub(&mul(&h, &v1.1), &mul(&v0.1, &h)), &det);
            let ty = div(&sub(&mul(&v0.0, &h), &mul(&h, &v1.0)), &det);
            pts.push((tx, ty));
        }
    }
    let mut all = Vec::with_capacity(pts.len() * 4);
    let nrx = neg(rx);
    let nry = neg(ry);
    for p in pts.iter() {
        let bx = add(&p.0, cx);
        let by = add(&p.1, cy);
        for sx in [&nrx, rx] {
            for sy in [&nry, ry] {
                all.push((add(&bx, sx), add(&by, sy)));
            }
        }
    }
    hull(all)
}

fn clip_to(poly: Vec<Pt>, vs: &[Pt]) -> Vec<Pt> {
    let k = vs.len();
    let mut poly = poly;
    for i in 0..k {
        let p = &vs[i];
        let q = &vs[(i + 1) % k];
        let a = (sub(&q.1, &p.1), sub(&p.0, &q.0));
        let b = dot(&a, &p.0, &p.1);
        poly = clip_poly(&poly, &a, &b);
        if poly.is_empty() {
            return poly;
        }
    }
    poly
}

pub fn wmin(u0: &Q, u1: &Q) -> Q {
    if u0.cmp0() != Ordering::Greater && u1.cmp0() != Ordering::Less {
        return qi(1);
    }
    let (c0, s0) = cs(u0);
    let (c1, s1) = cs(u1);
    let w0 = add(&absq(&c0), &absq(&s0));
    let w1 = add(&absq(&c1), &absq(&s1));
    if w1 < w0 {
        w1
    } else {
        w0
    }
}

// ---------------------------------------------------------------- Segment covers (seam4d.Group + Cover.mass_convex)

struct Seg {
    w: Q,
    // Group index grid (math.floor): gx ∈ [gx0, gx1], gy ∈ [gy0, gy1].
    gx0: i64,
    gx1: i64,
    gy0: i64,
    gy1: i64,
    // Exact segment bbox, used to prefilter convex polygons of positive area.
    bx0: Q,
    bx1: Q,
    by0: Q,
    by1: Q,
    // Integer Cyrus–Beck: k is the lcm of endpoint denominators; store A·k and (B − A)·k.
    k: Integer,
    ak: (Integer, Integer),
    dk: (Integer, Integer),
}

impl Seg {
    fn new(a: Pt, b: Pt, w: Q) -> Seg {
        let (mnx, mxx) = if a.0 <= b.0 { (&a.0, &b.0) } else { (&b.0, &a.0) };
        let (mny, mxy) = if a.1 <= b.1 { (&a.1, &b.1) } else { (&b.1, &a.1) };
        let (gx0, gx1, gy0, gy1) = (floor_i64(mnx), floor_i64(mxx), floor_i64(mny), floor_i64(mxy));
        let (bx0, bx1, by0, by1) = (mnx.clone(), mxx.clone(), mny.clone(), mxy.clone());
        let mut k = Integer::from(1);
        for v in [&a.0, &a.1, &b.0, &b.1] {
            k.lcm_mut(v.denom());
        }
        let kq = Q::from(k.clone());
        let to_int = |v: Q| -> Integer { Q::from(v * &kq).into_numer_denom().0 };
        let ak = (to_int(a.0.clone()), to_int(a.1.clone()));
        let dk = (to_int(sub(&b.0, &a.0)), to_int(sub(&b.1, &a.1)));
        Seg { w, gx0, gx1, gy0, gy1, bx0, bx1, by0, by1, k, ak, dk }
    }
}

/// Keep only w > 0, matching Group.__init__.
fn make_group(segs: Vec<(Pt, Pt, Q)>) -> Vec<Seg> {
    segs.into_iter()
        .filter(|(_, _, w)| w.cmp0() == Ordering::Greater)
        .map(|(a, b, w)| Seg::new(a, b, w))
        .collect()
}

/// Mirrors Cover.mass_convex(poly, polys=False).
/// Select each segment once, as in Python, when its index grid range intersects the polygon bbox search range:
/// x from int(lx) (int(lx) − 1 if lx < 0) through int(hx), and likewise for y.
/// Match this range exactly: for collinear polygons, the Cyrus–Beck region may be the entire line.
fn mass_convex(segs: &[Seg], poly: &[Pt]) -> Q {
    if poly.len() < 3 {
        return qi(0);
    }
    let mut lx = &poly[0].0;
    let mut hx = &poly[0].0;
    let mut ly = &poly[0].1;
    let mut hy = &poly[0].1;
    for p in poly.iter() {
        if p.0 < *lx {
            lx = &p.0;
        }
        if p.0 > *hx {
            hx = &p.0;
        }
        if p.1 < *ly {
            ly = &p.1;
        }
        if p.1 > *hy {
            hy = &p.1;
        }
    }
    let lo_cell = |v: &Q| -> i64 {
        if v.cmp0() != Ordering::Less {
            trunc_i64(v)
        } else {
            trunc_i64(v) - 1
        }
    };
    let (qx0, qx1, qy0, qy1) = (lo_cell(lx), trunc_i64(hx), lo_cell(ly), trunc_i64(hy));
    let n = poly.len();
    let mut edges: Vec<HalfPlane> = Vec::with_capacity(n);
    for i in 0..n {
        let p = &poly[i];
        let q = &poly[(i + 1) % n];
        let a = (sub(&q.1, &p.1), sub(&p.0, &q.0));
        let b = dot(&a, &p.0, &p.1);
        edges.push((a, b));
    }
    // Prefilter: for a positive-area counterclockwise convex polygon, the edge half-planes intersect in the polygon itself.
    // Thus segments with disjoint closed bboxes contribute 0. All bound() polygons have this form or are degenerate.
    // For zero-area collinear polygons, the region may be an entire line; skip the prefilter and use only Python's selection rule.
    let prefilter = area(poly).cmp0() == Ordering::Greater;
    // Convert a.x <= b to integers: L is the lcm of denominators; use (a·L, b·L).
    let iedges: Vec<((Integer, Integer), Integer)> = edges
        .iter()
        .map(|(a, b)| {
            let mut l = Integer::from(a.0.denom());
            l.lcm_mut(a.1.denom());
            l.lcm_mut(b.denom());
            let lq = Q::from(l);
            let f = |v: &Q| -> Integer { Q::from(v * &lq).into_numer_denom().0 };
            ((f(&a.0), f(&a.1)), f(b))
        })
        .collect();
    let mut m = qi(0);
    for s in segs {
        if s.gx1 < qx0 || s.gx0 > qx1 || s.gy1 < qy0 || s.gy0 > qy1 {
            continue;
        }
        if prefilter && (s.bx1 < *lx || s.bx0 > *hx || s.by1 < *ly || s.by0 > *hy) {
            continue;
        }
        // Follow Python's Cyrus–Beck steps with integer ratios (num, den), normalized to den > 0.
        // Scaling edge i by L_i and segment coordinates by k multiplies num and den by the same positive factor,
        // so num/den equals Python's ratio. Compare by cross multiplication without reduction.
        let mut t0n = Integer::from(0);
        let mut t0d = Integer::from(1);
        let mut t1n = Integer::from(1);
        let mut t1d = Integer::from(1);
        let mut empty = false;
        for (al, be) in iedges.iter() {
            let mut num = Integer::from(&s.k * be);
            num -= Integer::from(&al.0 * &s.ak.0);
            num -= Integer::from(&al.1 * &s.ak.1);
            let mut den = Integer::from(&al.0 * &s.dk.0);
            den += Integer::from(&al.1 * &s.dk.1);
            match den.cmp0() {
                Ordering::Equal => {
                    if num.cmp0() == Ordering::Less {
                        empty = true;
                        break;
                    }
                }
                Ordering::Greater => {
                    // t1 = min(t1, num/den)
                    if Integer::from(&num * &t1d) < Integer::from(&t1n * &den) {
                        t1n = num;
                        t1d = den;
                    }
                }
                Ordering::Less => {
                    num = -num;
                    den = -den;
                    // t0 = max(t0, num/den)
                    if Integer::from(&num * &t0d) > Integer::from(&t0n * &den) {
                        t0n = num;
                        t0d = den;
                    }
                }
            }
            if Integer::from(&t0n * &t1d) > Integer::from(&t1n * &t0d) {
                empty = true;
                break;
            }
        }
        if !empty && Integer::from(&t1n * &t0d) > Integer::from(&t0n * &t1d) {
            let t1 = Q::from((t1n, t1d));
            let t0 = Q::from((t0n, t0d));
            m += mul(&s.w, &sub(&t1, &t0));
        }
    }
    m
}

// ---------------------------------------------------------------- Families and lower bounds

pub struct FamilyCore {
    pub d0: Q,
    pub d1: Q,
    f: Vec<Seg>,
    t: Vec<Seg>,
    v: Vec<(Q, Q, Q)>, // (x_l, y, ρ)
    u: Vec<Pt>,
    /// Family UA (a in the edge lemma) and U for poly_lower: use the "U" field, or [UA, 20]² as in the Python reference.
    pub ua: Q,
    pub u_lower: Vec<Pt>,
    // Stage B: raw JSON F/T segments, including w = 0; cover construction keeps only w > 0, matching Python.
    f_raw: Vec<(Pt, Pt, Q)>,
    t_raw: Vec<(Pt, Pt, Q)>,
}

impl FamilyCore {
    fn mass_v(&self, poly: &[Pt], delta: &Q) -> Q {
        if poly.len() < 3 {
            return qi(0);
        }
        let xr = add(&qi(w0()), delta);
        let mut segs = Vec::new();
        for (xl, y, rho) in self.v.iter() {
            if xr > *xl {
                segs.push(((xl.clone(), y.clone()), (xr.clone(), y.clone()), mul(rho, &sub(&xr, xl))));
            }
        }
        mass_convex(&make_group(segs), poly)
    }

    #[allow(clippy::too_many_arguments)]
    pub fn bound_straight(&self, x0: Q, x1: Q, y0: Q, y1: Q, u0: Q, u1: Q, e0: Q, e1: Q) -> Option<Q> {
        let lo = half(&wmin(&u0, &u1));
        let x0 = if lo > x0 { lo.clone() } else { x0 };
        let y0 = if lo > y0 { lo } else { y0 };
        if x0 > x1 || y0 > y1 {
            return None;
        }
        let cx = half(&add(&x0, &x1));
        let cy = half(&add(&y0, &y1));
        let rx = half(&sub(&x1, &x0));
        let ry = half(&sub(&y1, &y0));
        let hp: Vec<HalfPlane> = angular_core_halfplanes(&u0, &u1)
            .into_iter()
            .map(|(a, b)| {
                let mut nb = b;
                nb -= mul(&absq(&a.0), &rx);
                nb -= mul(&absq(&a.1), &ry);
                (a, nb)
            })
            .collect();
        let mut p = halfplanes_to_poly(&hp, &qi(2));
        for v in p.iter_mut() {
            v.0 += &cx;
            v.1 += &cy;
        }
        if p.len() >= 3 && area(&p).cmp0() == Ordering::Less {
            p.reverse();
        }
        let mut m = if p.len() >= 3 { mass_convex(&self.f, &p) } else { qi(0) };
        if p.len() >= 3 {
            let p0: Vec<Pt> = p.iter().map(|v| (sub(&v.0, &e0), v.1.clone())).collect();
            let pt = if e0 != e1 {
                let p1: Vec<Pt> = p.iter().map(|v| (sub(&v.0, &e1), v.1.clone())).collect();
                clip_to(p0, &p1)
            } else {
                p0
            };
            if pt.len() >= 3 {
                m += mass_convex(&self.t, &pt);
            }
            m += self.mass_v(&p, &e0);
        }
        let o = outer_hull(&u0, &u1, &cx, &cy, &rx, &ry);
        let inner = if p.len() >= 3 { clip_to(p.clone(), &self.u) } else { Vec::new() };
        let a_in = if inner.len() >= 3 { area(&inner) } else { qi(0) };
        let oc = clip_to(o.clone(), &self.u);
        let a_oc = if oc.len() >= 3 { area(&oc) } else { qi(0) };
        let a_out = sub(&qi(1), &sub(&area(&o), &a_oc));
        m += if a_out > a_in { a_out } else { a_in };
        Some(m)
    }
}

// ---------------------------------------------------------------- JSON parsing (Fraction(str) syntax)

pub fn parse_integer(s: &str) -> Result<Integer, String> {
    let s = s.trim();
    if s.is_empty() {
        return Err("empty".into());
    }
    let (neg, body) = match s.as_bytes()[0] {
        b'-' => (true, &s[1..]),
        b'+' => (false, &s[1..]),
        _ => (false, s),
    };
    let body: String = body.chars().filter(|&c| c != '_').collect();
    if body.is_empty() || !body.bytes().all(|c| c.is_ascii_digit()) {
        return Err(format!("bad integer {:?}", s));
    }
    let z = Integer::from(Integer::parse(&body).map_err(|e| e.to_string())?);
    Ok(if neg { -z } else { z })
}

/// Python Fraction(str) syntax: "a/b", integers, and decimals with optional exponents.
pub fn parse_fraction(s: &str) -> Result<Q, String> {
    let s = s.trim();
    if let Some(i) = s.find('/') {
        let n = parse_integer(&s[..i])?;
        let d = parse_integer(&s[i + 1..])?;
        if d.cmp0() == Ordering::Equal {
            return Err("zero denominator".into());
        }
        return Ok(Q::from((n, d)));
    }
    let (neg, body) = match s.as_bytes().first() {
        Some(b'-') => (true, &s[1..]),
        Some(b'+') => (false, &s[1..]),
        _ => (false, s),
    };
    let (mant, exp) = match body.find(|c| c == 'e' || c == 'E') {
        Some(i) => (&body[..i], parse_integer(&body[i + 1..])?.to_i64().ok_or("exp")?),
        None => (body, 0i64),
    };
    let (ip, fp) = match mant.find('.') {
        Some(i) => (&mant[..i], &mant[i + 1..]),
        None => (mant, ""),
    };
    let ip: String = ip.chars().filter(|&c| c != '_').collect();
    let fp: String = fp.chars().filter(|&c| c != '_').collect();
    if (ip.is_empty() && fp.is_empty()) || !ip.bytes().chain(fp.bytes()).all(|c| c.is_ascii_digit()) {
        return Err(format!("bad number {:?}", s));
    }
    let digits = format!("{}{}", ip, fp);
    let mut r = Q::from(Integer::from(Integer::parse(&digits).map_err(|e| e.to_string())?));
    let e = exp - fp.len() as i64;
    let p10 = Integer::from(Integer::u_pow_u(10, e.unsigned_abs() as u32));
    if e >= 0 {
        r *= Q::from(p10);
    } else {
        r /= Q::from(p10);
    }
    Ok(if neg { -r } else { r })
}

fn json_q(v: &serde_json::Value) -> Result<Q, String> {
    match v {
        serde_json::Value::String(s) => parse_fraction(s),
        serde_json::Value::Number(n) => {
            if let Some(i) = n.as_i64() {
                Ok(qi(i))
            } else {
                Err(format!("float in family JSON is not supported: {}", n))
            }
        }
        _ => Err(format!("not a number: {}", v)),
    }
}

fn json_rows(d: &serde_json::Value, key: &str, width: usize) -> Result<Vec<Vec<Q>>, String> {
    let arr = d.get(key).and_then(|x| x.as_array()).ok_or(format!("missing {}", key))?;
    arr.iter()
        .map(|r| {
            let r = r.as_array().ok_or(format!("{}: row is not a list", key))?;
            if r.len() != width {
                return Err(format!("{}: row width {} != {}", key, r.len(), width));
            }
            r.iter().map(json_q).collect()
        })
        .collect()
}

/// Window w₀: corner rectangle [0, w₀+δ] × [0, w₀]; V's right endpoint and the seam lie at x = w₀ + δ.
/// For w₀ = 2, omit W0 and use key V; otherwise include W0 and use VW, so checkers requiring V reject the input.
/// All families loaded in one process must share w₀, matching the Python reference.
static W0: std::sync::OnceLock<i64> = std::sync::OnceLock::new();

/// This process's w₀; defaults to 2 before loading a family.
pub fn w0() -> i64 {
    *W0.get().unwrap_or(&2)
}

fn set_w0(w: i64) -> Result<(), String> {
    let got = *W0.get_or_init(|| w);
    if got != w {
        return Err(format!("families with different W0 in one process ({} and {})", got, w));
    }
    Ok(())
}

pub fn load_family(path: &str) -> Result<FamilyCore, String> {
    let text = std::fs::read_to_string(path).map_err(|e| e.to_string())?;
    load_family_text(&text)
}

pub fn load_family_text(text: &str) -> Result<FamilyCore, String> {
    let d: serde_json::Value = serde_json::from_str(text).map_err(|e| e.to_string())?;
    let get = |k: &str| -> Result<Q, String> { json_q(d.get(k).ok_or(format!("missing {}", k))?) };
    let seg = |r: Vec<Q>| -> (Pt, Pt, Q) {
        let mut it = r.into_iter();
        let (a0, a1, b0, b1, w) = (
            it.next().unwrap(),
            it.next().unwrap(),
            it.next().unwrap(),
            it.next().unwrap(),
            it.next().unwrap(),
        );
        ((a0, a1), (b0, b1), w)
    };
    let f_raw: Vec<(Pt, Pt, Q)> = json_rows(&d, "F", 5)?.into_iter().map(seg).collect();
    let t_raw: Vec<(Pt, Pt, Q)> = json_rows(&d, "T", 5)?.into_iter().map(seg).collect();
    let f = make_group(f_raw.clone());
    let t = make_group(t_raw.clone());
    let has_w0 = d.get("W0").is_some();
    if has_w0 != d.get("VW").is_some() || (d.get("V").is_some() && d.get("VW").is_some()) {
        return Err("W0 and VW must appear together (and VW never with V)".into());
    }
    let w = if has_w0 { get("W0")? } else { qi(2) };
    if *w.denom() != 1 || w < qi(2) || (has_w0 && w == qi(2)) {
        return Err(format!("W0 must be an integer >= 3 (2 is written without the key): {}", w));
    }
    set_w0(w.numer().to_i64().ok_or("W0 is too large")?)?;
    let v = json_rows(&d, if has_w0 { "VW" } else { "V" }, 3)?
        .into_iter()
        .map(|r| {
            let mut it = r.into_iter();
            (it.next().unwrap(), it.next().unwrap(), it.next().unwrap())
        })
        .collect();
    let ua = get("UA")?;
    let big = qi(1000);
    let mut u_lower = vec![(ua.clone(), ua.clone()), (qi(20), ua.clone()), (qi(20), qi(20)), (ua.clone(), qi(20))];
    let mut u = vec![
        (ua.clone(), ua.clone()),
        (big.clone(), ua.clone()),
        (big.clone(), big.clone()),
        (ua.clone(), big),
    ];
    // One-sided edge lemma variant: if "U" is present, its counterclockwise polygon supports the Lebesgue measure.
    if let Some(uv) = d.get("U") {
        let rows = uv.as_array().ok_or("U is not an array")?;
        let mut poly = Vec::new();
        for r in rows {
            let p = r.as_array().ok_or("U vertex is not an array")?;
            if p.len() != 2 {
                return Err("U vertex must have 2 coordinates".into());
            }
            poly.push((json_q(&p[0])?, json_q(&p[1])?));
        }
        if poly.len() < 3 {
            return Err("U must have at least 3 vertices".into());
        }
        u_lower = poly.clone();
        u = poly;
    }
    Ok(FamilyCore { d0: get("d0")?, d1: get("d1")?, f, t, v, u, ua, u_lower, f_raw, t_raw })
}

impl FamilyCore {
    /// Matches Python's cover construction: keep w > 0 and scale weights to w·scale.
    fn cover(raw: &[(Pt, Pt, Q)], scale: &Q) -> Vec<(Pt, Pt, Q)> {
        raw.iter()
            .filter(|(_, _, w)| w.cmp0() == Ordering::Greater)
            .map(|(a, b, w)| (a.clone(), b.clone(), mul(w, scale)))
            .collect()
    }
}


impl FamilyCore {
    pub fn certify3(&self, bx: &[Q;6], a: &Q, b: &Q, thr: &Q, scale: &Q, concave: Option<(char,Q)>, tangent: Option<(char,Q)>) -> Result<b3d::B3Out,b3d::BErr> {
        let fc = Self::cover(&self.f_raw, scale);
        let tc = Self::cover(&self.t_raw, scale);
        let vs = self.v.iter().map(|(xl,y,rho)| (xl.clone(),y.clone(),mul(rho,scale))).collect::<Vec<_>>();
        b3d::certify3(&fc,&tc,&vs,&qi(20),bx,a,b,thr,concave,tangent)
    }
}
pub mod replay;
