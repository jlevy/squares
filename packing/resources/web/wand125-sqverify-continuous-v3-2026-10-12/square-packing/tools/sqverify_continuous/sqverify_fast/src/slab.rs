//! Continuous-angle mode: every orientation, not a net of directions.
//!
//! Claim checked for a measure `mu` (the certificate's D4-expanded rectangles),
//! a core side `B` and a threshold `tau`: every closed square of side `B` lying
//! in `K = [0, L]^2`, at every centre and every angle, satisfies
//! `mu(P) >= tau`. With `n tau > M` (the total mass), `n` interior-disjoint
//! squares of side `B` cannot lie in `K`, so `n` unit squares do not fit in a
//! square of side `L / B` (scale by `B`).
//!
//! Reduction (lemma C1 of `CONTINUOUS.md`). `mu` is invariant under the eight
//! symmetries of `K`. A reflection maps angle `theta` to `-theta`, and the
//! square's angle matters modulo `pi/2`, so `theta` lies in `[0, pi/4]`; a
//! quarter turn about the centre of `K` then keeps the angle modulo `pi/2` and
//! moves the centre into the closed north-east quadrant. With
//! `t = tan(theta/2)`, `c = (1 - t^2)/(1 + t^2)`, `s = 2t/(1 + t^2)`,
//! `W = c + s`, `h = B/2`, the square lies in `K` exactly when its centre is
//! within `L/2 - hW` of `L/2` in both coordinates, so the north-east legal
//! centres are `x = L/2 + u E(t)`, `y = L/2 + v E(t)`, `(u, v)` in `[0, 1]^2`,
//! `E(t) = L/2 - h W(t)`.
//!
//! Search space: `t` in `[eps, T]` (`T^2 + 2T - 1 > 0`, so `T > tan(pi/8)`) by
//! interval branch and bound over boxes in `(u, v, t)`; `t` in `[0, eps]` by the
//! exact axis sweep of a side-`A` square with `A W(eps) <= B` (lemma C6), which
//! every such side-`B` square contains concentrically.
//!
//! For one box (lemmas C2 to C5): `C`, `S`, `Wv`, `Ev` enclose `c`, `s`, `W`,
//! `E` over its `t` range; the centre ranges `X`, `Y` enclose every centre of the
//! box at every angle of it; the path centre `x_m(t) = L/2 + u0 E(t)` (box
//! midpoint `u0`) has the enclosure `Xm`. For every pose `(x, y, t)` of the box,
//! `|x - x_m(t)| <= du E(t) <= dx` and the segment between them lies in `X`, so
//! `F(x, y, t) >= F(x_m, y_m, t) - dx Gx - dy Gy` with `Gx`, `Gy` bounding the
//! partial derivatives of the capture over `X x Y x [t]`. `F(x_m, y_m, t)` is
//! bounded below for all `t` of the box at once by concave sections whose
//! values are bounded over the whole `(C, S)` box (lemma C3).

use std::sync::Mutex;
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Instant;

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Zero};
use serde_json::{Value, json};

use crate::certificate::{Certificate, Rect};
use crate::exact::{enclose, of_f64};
use crate::interval::{Iv, add_dn, add_up, dn, fmax, fmin, mul_dn, mul_up, sub_dn, sub_up, up};

/// Parameters of a continuous-angle run, exact.
#[derive(Clone, Debug)]
pub struct Params {
    /// Core side `B`.
    pub core: BigRational,
    /// Capture threshold `tau`.
    pub threshold: BigRational,
    /// Lower end `eps` of the branch-and-bound range of `t`.
    pub eps: BigRational,
    /// Upper end `T` of the range of `t`.
    pub last_t: BigRational,
    /// Side `A` of the axis-aligned square used on `[0, eps]`.
    pub axis_core: BigRational,
    /// Interior breakpoints of `[eps, T]`: each piece is one root box.
    pub cuts: Vec<BigRational>,
    /// Node budget per root box.
    pub max_nodes: u64,
    /// Run only the roots with these indices (a diagnostic; never VERIFIED).
    pub only: Option<(usize, usize)>,
}

fn q(p: i64, d: i64) -> BigRational {
    BigRational::new(BigInt::from(p), BigInt::from(d))
}

/// The exact premises; returns their record or the first failure.
///
/// # Errors
///
/// Names the premise that fails.
pub fn premises(cert: &Certificate, p: &Params) -> Result<Value, String> {
    let one = BigRational::one();
    let two = q(2, 1);
    let l = &cert.side;
    let b = &p.core;
    let a = &p.axis_core;
    let eps = &p.eps;
    let t = &p.last_t;
    let n = BigRational::from_integer(BigInt::from(cert.n));
    let fail = |m: &str| Err(format!("premise refused: {m}"));
    if !(b > &BigRational::zero() && a > &BigRational::zero() && a <= b) {
        return fail("0 < A <= B");
    }
    // E(t) > 0 for every t: L/2 > h W with W <= sqrt 2, i.e. L^2 > 2 B^2.
    if l * l <= &two * b * b {
        return fail("L^2 > 2 B^2");
    }
    if !(eps > &BigRational::zero() && eps < t && t <= &q(1, 2)) {
        return fail("0 < eps < T <= 1/2");
    }
    if t * t + &two * t - &one <= BigRational::zero() {
        return fail("T^2 + 2T - 1 > 0 (T > tan(pi/8))");
    }
    // W increases on [0, sqrt2 - 1]; eps lies there because eps < 1/3 is checked
    // as eps^2 + 2 eps - 1 < 0.
    if eps * eps + &two * eps - &one >= BigRational::zero() {
        return fail("eps < sqrt 2 - 1");
    }
    let w_eps = (&one + &two * eps - eps * eps) / (&one + eps * eps);
    if a * &w_eps > *b {
        return fail("A W(eps) <= B");
    }
    if &n * &p.threshold <= cert.mass {
        return fail("n tau > M");
    }
    let mut prev = eps.clone();
    for c in &p.cuts {
        if c <= &prev {
            return fail("cuts increase strictly inside (eps, T)");
        }
        prev = c.clone();
    }
    if &prev >= t {
        return fail("cuts increase strictly inside (eps, T)");
    }
    Ok(json!({
        "n": cert.n,
        "L": l.to_string(),
        "B": b.to_string(),
        "X": (l / b).to_string(),
        "mass": cert.mass.to_string(),
        "threshold": p.threshold.to_string(),
        "counting_margin": (&n * &p.threshold - &cert.mass).to_string(),
        "eps": eps.to_string(),
        "T": t.to_string(),
        "A": a.to_string(),
        "axis_containment_margin": (b - a * &w_eps).to_string(),
        "input_sha256": cert.input_sha256,
        "expanded_rectangles": cert.rects.len(),
    }))
}

/// Enclosures of `c`, `s`, `W` over `t` in `[ta, tb]`, `0 <= ta <= tb <= 1/2`.
#[derive(Clone, Copy, Debug)]
struct Angles {
    c: Iv,
    s: Iv,
    w: Iv,
}

#[inline]
fn div_dn(a: f64, b: f64) -> f64 {
    dn(a / b)
}

#[inline]
fn div_up(a: f64, b: f64) -> f64 {
    up(a / b)
}

/// Lemma C2: `c` decreases and `s` increases on `[0, 1]`; `W` increases up to
/// `sqrt 2 - 1` and decreases after it, with maximum `sqrt 2`.
fn angles(ta: f64, tb: f64) -> Angles {
    let sq_dn = |t: f64| mul_dn(t, t);
    let sq_up = |t: f64| mul_up(t, t);
    let c_lo = div_dn(sub_dn(1.0, sq_up(tb)), add_up(1.0, sq_up(tb)));
    let c_hi = div_up(sub_up(1.0, sq_dn(ta)), add_dn(1.0, sq_dn(ta)));
    let s_lo = div_dn(2.0 * ta, add_up(1.0, sq_up(ta)));
    let s_hi = div_up(2.0 * tb, add_dn(1.0, sq_dn(tb)));
    let w_dn = |t: f64| {
        div_dn(
            sub_dn(add_dn(1.0, 2.0 * t), sq_up(t)),
            add_up(1.0, sq_up(t)),
        )
    };
    let w_up = |t: f64| {
        div_up(
            sub_up(add_up(1.0, 2.0 * t), sq_dn(t)),
            add_dn(1.0, sq_dn(t)),
        )
    };
    let w_lo = fmin(w_dn(ta), w_dn(tb));
    // Which side of sqrt 2 - 1 each end lies on, decided with directed bounds.
    let below = |t: f64| add_up(add_up(sq_up(t), 2.0 * t), 0.0) < 1.0;
    let above = |t: f64| add_dn(sq_dn(t), 2.0 * t) > 1.0;
    let w_hi = if below(tb) {
        w_up(tb)
    } else if above(ta) {
        w_up(ta)
    } else {
        // 1.4142135623730951 > sqrt 2; `up` adds a further margin.
        up(std::f64::consts::SQRT_2)
    };
    Angles {
        c: Iv::new(fmax(c_lo, 0.0), c_hi),
        s: Iv::new(fmax(s_lo, 0.0), s_hi),
        w: Iv::new(w_lo, w_hi),
    }
}

/// Box-wide constants.
#[derive(Clone, Copy, Debug)]
struct Pose {
    an: Angles,
    /// `h = B/2`, enclosed.
    h: Iv,
    /// Half the square's axis-aligned extent, upper bound `h W`.
    ext: f64,
    /// Centre ranges over the box.
    x: Iv,
    y: Iv,
    /// Path-centre ranges.
    xm: Iv,
    ym: Iv,
    /// Bounds on `du E(t)`, `dv E(t)`.
    dx: f64,
    dy: f64,
}

/// One box: `u` in `[ul, uh]`, `v` in `[vl, vh]`, `t` in `[ta, tb]`.
#[derive(Clone, Debug)]
struct Node {
    ul: f64,
    uh: f64,
    vl: f64,
    vh: f64,
    ta: f64,
    tb: f64,
    depth: u32,
    base: f64,
    active: Vec<u32>,
}

fn pose(n: &Node, half_l: Iv, h: Iv) -> Option<Pose> {
    let an = angles(n.ta, n.tb);
    let e_lo = sub_dn(half_l.lo, mul_up(h.hi, an.w.hi));
    let e_hi = sub_up(half_l.hi, mul_dn(h.lo, an.w.lo));
    // NaN-safe: refuse unless e_lo is a number above zero
    if e_lo.partial_cmp(&0.0) != Some(std::cmp::Ordering::Greater) {
        return None;
    }
    let range = |a: f64, b: f64| {
        Iv::new(
            add_dn(half_l.lo, mul_dn(a, e_lo)),
            add_up(half_l.hi, mul_up(b, e_hi)),
        )
    };
    let u0 = f64::midpoint(n.ul, n.uh);
    let v0 = f64::midpoint(n.vl, n.vh);
    let du = fmax(sub_up(n.uh, u0), sub_up(u0, n.ul));
    let dv = fmax(sub_up(n.vh, v0), sub_up(v0, n.vl));
    Some(Pose {
        an,
        h,
        ext: mul_up(h.hi, an.w.hi),
        x: range(n.ul, n.uh),
        y: range(n.vl, n.vh),
        xm: range(u0, u0),
        ym: range(v0, v0),
        dx: mul_up(du, e_hi),
        dy: mul_up(dv, e_hi),
    })
}

#[derive(Clone, Copy, PartialEq, Eq)]
enum Class {
    Inside,
    Outside,
    Boundary,
}

/// Smallest absolute value in an interval.
#[inline]
fn absmin(a: Iv) -> f64 {
    if a.lo > 0.0 {
        a.lo
    } else if a.hi < 0.0 {
        -a.hi
    } else {
        0.0
    }
}

/// Lemma C4: a rectangle inside every square of the box, outside every one, or
/// neither. Exact interval tests only.
fn classify(p: &Pose, r: &Rect) -> Class {
    // Separation along the container's axes from the square's bounding box.
    if r.x2.hi <= sub_dn(p.x.lo, p.ext)
        || r.x1.lo >= add_up(p.x.hi, p.ext)
        || r.y2.hi <= sub_dn(p.y.lo, p.ext)
        || r.y1.lo >= add_up(p.y.hi, p.ext)
    {
        return Class::Outside;
    }
    let half = Iv::point(0.5);
    let mx = r.x1.plus(r.x2).mul_nonneg(half);
    let my = r.y1.plus(r.y2).mul_nonneg(half);
    let hx = r.x2.minus(r.x1).mul_nonneg(half).pos();
    let hy = r.y2.minus(r.y1).mul_nonneg(half).pos();
    let ddx = mx.minus(p.x);
    let ddy = my.minus(p.y);
    let (c, s) = (p.an.c, p.an.s);
    let pu = c.times(ddx).plus(s.times(ddy));
    let pv = c.times(ddy).minus(s.times(ddx));
    let eu = hx.mul_nonneg(c).plus(hy.mul_nonneg(s));
    let ev = hx.mul_nonneg(s).plus(hy.mul_nonneg(c));
    if add_up(pu.mag(), eu.hi) <= p.h.lo && add_up(pv.mag(), ev.hi) <= p.h.lo {
        return Class::Inside;
    }
    if sub_dn(absmin(pu), eu.hi) >= p.h.hi || sub_dn(absmin(pv), ev.hi) >= p.h.hi {
        return Class::Outside;
    }
    Class::Boundary
}

/// Lower bound of `(n_lo..) / k` for a numerator lower bound and `k > 0`.
#[inline]
fn quot_lo(num_lo: f64, k: Iv) -> f64 {
    if num_lo >= 0.0 {
        div_dn(num_lo, k.hi)
    } else {
        div_dn(num_lo, k.lo)
    }
}

/// Upper bound of `num / k` for a numerator upper bound and `k > 0`.
#[inline]
fn quot_hi(num_hi: f64, k: Iv) -> f64 {
    if num_hi >= 0.0 {
        div_up(num_hi, k.lo)
    } else {
        div_up(num_hi, k.hi)
    }
}

/// Upper bound of `k xi` for `k >= 0` enclosed.
#[inline]
fn kx_up(k: Iv, xi: f64) -> f64 {
    if xi >= 0.0 {
        mul_up(k.hi, xi)
    } else {
        mul_up(k.lo, xi)
    }
}

/// Lower bound of `k xi` for `k >= 0` enclosed.
#[inline]
fn kx_dn(k: Iv, xi: f64) -> f64 {
    if xi >= 0.0 {
        mul_dn(k.lo, xi)
    } else {
        mul_dn(k.hi, xi)
    }
}

/// Lemma C3: a lower bound, valid at every `(c, s)` of the box, on the length
/// of `{eta in [b, e] : (xi, eta) in Q}` for the centred square `Q` of half-side
/// `h >= hl` at angle `theta`.
#[inline]
fn section_lo(c: Iv, s: Iv, hl: f64, xi: f64, e: f64, b: f64) -> f64 {
    // top: min(e, (h - c xi)/s, (h + s xi)/c), each bounded below
    let f1 = quot_lo(sub_dn(hl, kx_up(c, xi)), s);
    let f2 = quot_lo(add_dn(hl, kx_dn(s, xi)), c);
    // bottom: max(b, (-h - c xi)/s, (s xi - h)/c), each bounded above
    let g1 = quot_hi(sub_up(-hl, kx_dn(c, xi)), s);
    let g2 = quot_hi(sub_up(kx_up(s, xi), hl), c);
    sub_dn(fmin(fmin(e, f1), f2), fmax(fmax(b, g1), g2))
}

/// Breakpoint estimates of the section function at one angle (their values
/// affect only accuracy).
fn knots_at(c: f64, s: f64, h: f64, e: f64, b: f64, out: &mut Vec<f64>) {
    out.extend_from_slice(&[
        h * (c - s),
        h * (s - c),
        (h - s * e) / c,
        (c * e - h) / s,
        (-h - s * b) / c,
        (c * b + h) / s,
        h * (c + s),
        -h * (c + s),
        (-h - s * e) / c,
        (c * e + h) / s,
        (h - s * b) / c,
        (c * b - h) / s,
    ]);
}

/// Lemma C3: a lower bound on `|R ∩ Q(x_m(t), y_m(t), t)|` for every `t` of the
/// box. The inner rectangle below lies in `R - (x, y)` for every path centre.
fn area_lo(p: &Pose, r: &Rect, knots: &mut Vec<f64>) -> f64 {
    let xi1 = sub_up(r.x1.hi, p.xm.lo);
    let xi2 = sub_dn(r.x2.lo, p.xm.hi);
    let e = sub_dn(r.y2.lo, p.ym.hi);
    let b = sub_up(r.y1.hi, p.ym.lo);
    if !(xi1 < xi2 && b < e) {
        return 0.0;
    }
    let (c, s, hl) = (p.an.c, p.an.s, p.h.lo);
    knots.clear();
    knots.push(xi1);
    knots.push(xi2);
    let start = knots.len();
    knots_at(c.lo, s.hi, hl, e, b, knots);
    knots_at(c.hi, s.lo, hl, e, b, knots);
    let mut keep = start;
    for i in start..knots.len() {
        let x = knots[i];
        if x > xi1 && x < xi2 {
            knots[keep] = x;
            keep += 1;
        }
    }
    knots.truncate(keep);
    knots.sort_unstable_by(f64::total_cmp);
    let mut total = 0.0;
    let mut px = knots[0];
    let mut pv = section_lo(c, s, hl, px, e, b);
    for &x in &knots[1..] {
        let v = section_lo(c, s, hl, x, e, b);
        let sum = add_dn(pv, v);
        let width = sub_dn(x, px);
        if (sum > 0.0 || sum.is_nan()) && width > 0.0 {
            total = add_dn(total, dn(mul_dn(sum, width) * 0.5));
        }
        px = x;
        pv = v;
    }
    total
}

/// Division by an interval `k > 0`.
#[inline]
fn over(a: Iv, k: Iv) -> Iv {
    a.times(Iv::new(div_dn(1.0, k.hi), div_up(1.0, k.lo)))
}

/// Lemma C5: enclosure over the box of the length of `{z} x [lo, hi]` inside the
/// square, for a vertical line at `z` (`centre` the centre range along the line's
/// normal, `along` the centre range along the line, `(c, s)` as given), or for a
/// horizontal line with `(c, s)` exchanged.
fn chord(z: Iv, centre: Iv, along: Iv, lo: Iv, hi: Iv, c: Iv, s: Iv, h: Iv) -> Iv {
    let w = z.minus(centre);
    let top = over(h.minus(c.times(w)), s).min(over(h.plus(s.times(w)), c));
    let bottom = over(Iv::new(-h.hi, -h.lo).minus(c.times(w)), s).max(over(s.times(w).minus(h), c));
    let upper = hi.minus(along).min(top);
    let lower = lo.minus(along).max(bottom);
    upper.minus(lower).pos()
}

/// Lemma C5: enclosures of the capture's partial derivatives over the box.
fn gradient(p: &Pose, r: &Rect) -> (Iv, Iv) {
    let (c, s, h) = (p.an.c, p.an.s, p.h);
    let reach_x = |z: Iv| z.hi >= sub_dn(p.x.lo, p.ext) && z.lo <= add_up(p.x.hi, p.ext);
    let reach_y = |z: Iv| z.hi >= sub_dn(p.y.lo, p.ext) && z.lo <= add_up(p.y.hi, p.ext);
    let zero = Iv::point(0.0);
    let left = if reach_x(r.x1) {
        chord(r.x1, p.x, p.y, r.y1, r.y2, c, s, h)
    } else {
        zero
    };
    let right = if reach_x(r.x2) {
        chord(r.x2, p.x, p.y, r.y1, r.y2, c, s, h)
    } else {
        zero
    };
    let bottom = if reach_y(r.y1) {
        chord(r.y1, p.y, p.x, r.x1, r.x2, s, c, h)
    } else {
        zero
    };
    let top = if reach_y(r.y2) {
        chord(r.y2, p.y, p.x, r.x1, r.x2, s, c, h)
    } else {
        zero
    };
    (
        left.minus(right).mul_nonneg(r.rho),
        bottom.minus(top).mul_nonneg(r.rho),
    )
}

/// The outcome of one root box.
#[derive(Clone, Debug)]
pub struct RootResult {
    /// Exact ends of the root's `t` range.
    pub t_range: (BigRational, BigRational),
    /// Whether every box was accepted.
    pub verified: bool,
    /// Boxes evaluated and accepted.
    pub nodes: u64,
    /// Accepted boxes.
    pub leaves: u64,
    /// Splits along `t`.
    pub angle_splits: u64,
    /// Deepest box.
    pub max_depth: u32,
    /// Least accepted lower bound.
    pub min_lower: f64,
    /// For a refusal: the stopping box `(u, v, t)` midpoint, its half-widths and
    /// its bound, and the exact capture at that pose.
    pub witness: Option<Value>,
    /// Wall seconds.
    pub seconds: f64,
}

struct Ctx<'a> {
    cert: &'a Certificate,
    half_l: Iv,
    h: Iv,
    thr: f64,
    max_nodes: u64,
}

/// Lower bound over the box (base excluded) and the split hint.
fn bound(ctx: &Ctx, p: &Pose, active: &[u32], knots: &mut Vec<f64>) -> (f64, f64, f64) {
    let mut f = 0.0;
    let mut gx = Iv::point(0.0);
    let mut gy = Iv::point(0.0);
    for &i in active {
        let r = &ctx.cert.rects[i as usize];
        let a = area_lo(p, r, knots);
        if a > 0.0 {
            f = add_dn(f, mul_dn(r.rho.lo, a));
        }
        let (rx, ry) = gradient(p, r);
        gx = gx.plus(rx);
        gy = gy.plus(ry);
    }
    let lx = mul_up(p.dx, gx.mag());
    let ly = mul_up(p.dy, gy.mag());
    (f, lx, ly)
}

fn exact_capture(cert: &Certificate, core: &BigRational, x: f64, y: f64, t: f64) -> BigRational {
    let t = of_f64(t);
    let one = BigRational::one();
    let d = &one + &t * &t;
    let c = (&one - &t * &t) / &d;
    let s = (q(2, 1) * &t) / &d;
    let mut shrunk = cert.clone();
    shrunk.core = core.clone();
    crate::oracle::coverage(&shrunk, &of_f64(x), &of_f64(y), &c, &s)
}

fn run_root(
    ctx: &Ctx,
    core: &BigRational,
    threshold: &BigRational,
    lo: &BigRational,
    hi: &BigRational,
) -> Result<RootResult, String> {
    let start = Instant::now();
    let ta = enclose(lo)?.lo;
    let tb = enclose(hi)?.hi;
    let all: Vec<u32> = (0..ctx.cert.rects.len() as u32).collect();
    let mut stack = vec![Node {
        ul: 0.0,
        uh: 1.0,
        vl: 0.0,
        vh: 1.0,
        ta,
        tb,
        depth: 0,
        base: 0.0,
        active: all,
    }];
    let mut res = RootResult {
        t_range: (lo.clone(), hi.clone()),
        verified: false,
        nodes: 0,
        leaves: 0,
        angle_splits: 0,
        max_depth: 0,
        min_lower: f64::INFINITY,
        witness: None,
        seconds: 0.0,
    };
    let mut knots = Vec::with_capacity(32);
    while let Some(mut n) = stack.pop() {
        res.nodes += 1;
        res.max_depth = res.max_depth.max(n.depth);
        let Some(p) = pose(&n, ctx.half_l, ctx.h) else {
            return Err("empty centre domain".into());
        };
        let mut base = n.base;
        let mut active = Vec::with_capacity(n.active.len());
        for &i in &n.active {
            let r = &ctx.cert.rects[i as usize];
            match classify(&p, r) {
                Class::Inside => base = add_dn(base, r.mass.lo),
                Class::Outside => {}
                Class::Boundary => active.push(i),
            }
        }
        let (f, lx, ly) = bound(ctx, &p, &active, &mut knots);
        let lower = sub_dn(sub_dn(add_dn(base, f), lx), ly);
        if !(lower.is_finite() && lx.is_finite() && ly.is_finite()) {
            res.witness = Some(json!({"reason": "non-finite"}));
            res.seconds = start.elapsed().as_secs_f64();
            return Ok(res);
        }
        if lower >= ctx.thr {
            res.leaves += 1;
            res.min_lower = res.min_lower.min(lower);
            continue;
        }
        let tiny = (n.uh - n.ul).min(n.vh - n.vl) < 1e-12 || n.tb - n.ta < 1e-15;
        if res.nodes >= ctx.max_nodes || tiny {
            let u0 = f64::midpoint(n.ul, n.uh);
            let v0 = f64::midpoint(n.vl, n.vh);
            let tm = f64::midpoint(n.ta, n.tb);
            // the exact capture at the box's path centre for the middle angle
            let an = angles(tm, tm);
            let e = f64::midpoint(ctx.half_l.lo, ctx.half_l.hi)
                - ctx.h.lo * f64::midpoint(an.w.lo, an.w.hi);
            let (x, y) = (ctx.half_l.lo + u0 * e, ctx.half_l.lo + v0 * e);
            let exact = exact_capture(ctx.cert, core, x, y, tm);
            res.witness = Some(json!({
                "reason": if tiny { "box below resolution" } else { "node budget" },
                "u": u0, "v": v0, "t": tm, "du": (n.uh - n.ul) / 2.0, "dv": (n.vh - n.vl) / 2.0,
                "dt": (n.tb - n.ta) / 2.0, "lower": lower, "base": base, "centre_part": f,
                "loss_x": lx, "loss_y": ly,
                "exact_pose": [x, y, tm], "exact_capture": exact.to_string(),
                "exact_below_threshold": &exact < threshold,
            }));
            res.seconds = start.elapsed().as_secs_f64();
            return Ok(res);
        }
        // Split hint (accuracy only): what halving each coordinate could gain.
        // Halving u or v roughly halves its derivative loss; the gain of
        // splitting t is estimated by the whole bound at the middle angle, whose
        // centre part and derivative losses both shrink with the angle width.
        let tm = f64::midpoint(n.ta, n.tb);
        let mid = Node {
            ta: tm,
            tb: tm,
            ..n.clone()
        };
        let gain_t = match pose(&mid, ctx.half_l, ctx.h) {
            Some(pm) => {
                let (fm, lxm, lym) = bound(ctx, &pm, &active, &mut knots);
                (fm - f) + (lx + ly) - (lxm + lym)
            }
            None => f64::INFINITY,
        };
        n.base = base;
        n.active = active;
        n.depth += 1;
        let mut other = n.clone();
        if gain_t >= 0.5 * lx.max(ly) {
            n.tb = tm;
            other.ta = tm;
            res.angle_splits += 1;
        } else if lx >= ly {
            let m = f64::midpoint(n.ul, n.uh);
            n.uh = m;
            other.ul = m;
        } else {
            let m = f64::midpoint(n.vl, n.vh);
            n.vh = m;
            other.vl = m;
        }
        stack.push(n);
        stack.push(other);
    }
    res.verified = true;
    res.seconds = start.elapsed().as_secs_f64();
    Ok(res)
}

/// The full run: premises, the axis patch, then every root box on `threads`.
///
/// # Errors
///
/// Returns a message when a premise fails or a constant cannot be enclosed.
pub fn run(
    cert: &Certificate,
    p: &Params,
    threads: usize,
    out: &mut dyn FnMut(&Value),
) -> Result<bool, String> {
    let prem = premises(cert, p)?;
    out(&json!({"kind": "premises", "premises": prem}));
    let two = q(2, 1);
    // Lemma C6: the axis patch for t in [0, eps].
    let mut axis_cert = cert.clone();
    axis_cert.core = p.axis_core.clone();
    let upper = &cert.side - &p.axis_core / &two;
    let thr = enclose(&p.threshold)?.hi;
    let started = Instant::now();
    let axis = crate::axis::verify_axis(&axis_cert, thr, &upper)?;
    out(&json!({
        "kind": "axis-patch", "A": p.axis_core.to_string(), "verified": axis.verified,
        "non_finite": axis.non_finite, "vertices": axis.x_events * axis.y_events,
        "min_certified_lower_bound": axis.min_lower, "argmin": [axis.argmin.0, axis.argmin.1],
        "seconds": started.elapsed().as_secs_f64(),
    }));
    let mut ends = vec![p.eps.clone()];
    ends.extend(p.cuts.iter().cloned());
    ends.push(p.last_t.clone());
    let roots: Vec<(BigRational, BigRational)> = ends
        .windows(2)
        .map(|w| (w[0].clone(), w[1].clone()))
        .collect();
    let ctx = Ctx {
        cert,
        half_l: enclose(&(&cert.side / &two))?,
        h: enclose(&(&p.core / &two))?,
        thr,
        max_nodes: p.max_nodes,
    };
    let next = AtomicUsize::new(0);
    let results = Mutex::new(Vec::new());
    let failure = Mutex::new(None);
    let lines = Mutex::new(Vec::new());
    std::thread::scope(|scope| {
        for _ in 0..threads.max(1).min(roots.len()) {
            scope.spawn(|| {
                loop {
                    let k = next.fetch_add(1, Ordering::Relaxed);
                    let Some((lo, hi)) = roots.get(k) else { break };
                    if p.only.is_some_and(|(a, b)| k < a || k > b) {
                        continue;
                    }
                    match run_root(&ctx, &p.core, &p.threshold, lo, hi) {
                        Ok(r) => {
                            let line = json!({
                                "kind": "root", "index": k, "t": [lo.to_string(), hi.to_string()],
                                "verdict": if r.verified { "verified" } else { "refused" },
                                "nodes": r.nodes, "leaves": r.leaves, "angle_splits": r.angle_splits,
                                "max_depth": r.max_depth,
                                "min_certified_lower_bound": if r.min_lower.is_finite() { json!(r.min_lower) } else { Value::Null },
                                "witness": r.witness, "seconds": r.seconds,
                            });
                            eprintln!("{line}");
                            if let Ok(mut l) = lines.lock() {
                                l.push((k, line));
                            }
                            if let Ok(mut all) = results.lock() {
                                all.push(r);
                            }
                        }
                        Err(m) => {
                            if let Ok(mut f) = failure.lock() {
                                *f = Some(m);
                            }
                            break;
                        }
                    }
                }
            });
        }
    });
    if let Some(m) = failure.into_inner().map_err(|_| "worker panicked")? {
        return Err(m);
    }
    let mut lines = lines.into_inner().map_err(|_| "worker panicked")?;
    lines.sort_by_key(|(k, _)| *k);
    for (_, l) in &lines {
        out(l);
    }
    let results = results.into_inner().map_err(|_| "worker panicked")?;
    let roots_ok =
        p.only.is_none() && results.len() == roots.len() && results.iter().all(|r| r.verified);
    let ok = roots_ok && axis.verified;
    out(&json!({
        "kind": "sqverify-fast-continuous-summary/v1",
        "status": if ok { "VERIFIED" } else { "REFUSED" },
        "claim": if ok { format!("s({}) > {}", cert.n, &cert.side / &p.core) } else { String::new() },
        "roots": roots.len(),
        "refused_roots": lines.iter().filter(|(_, l)| l["verdict"] != "verified").map(|(k, _)| *k).collect::<Vec<_>>(),
        "axis_verified": axis.verified,
        "nodes": results.iter().map(|r| r.nodes).sum::<u64>(),
        "leaves": results.iter().map(|r| r.leaves).sum::<u64>(),
        "angle_splits": results.iter().map(|r| r.angle_splits).sum::<u64>(),
        "min_certified_lower_bound": results.iter().map(|r| r.min_lower).fold(f64::INFINITY, f64::min),
        "wall_seconds": started.elapsed().as_secs_f64(),
        "threads": threads,
        "build": crate::build_identity(),
        "premises": prem,
    }));
    Ok(ok)
}

#[cfg(test)]
#[path = "slab_tests.rs"]
mod tests;
