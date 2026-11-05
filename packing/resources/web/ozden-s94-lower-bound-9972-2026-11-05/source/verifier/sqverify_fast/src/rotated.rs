//! Interval branch and bound over centre boxes: every direction `r >= 1`, and
//! direction zero when the measure has points or segments (lemma B5).
//!
//! For a box of centres with midpoint `c0` and half-widths `(dx, dy)` the
//! accepted bound is
//!
//! `F(c) >= F(c0) - Gx dx - Gy dy`,
//!
//! where `Gx`, `Gy` bound `|dF/dx|`, `|dF/dy|` over the whole box (lemma R3 of
//! `SOUNDNESS.md`). Rectangles certified inside the common core of every square
//! in the box contribute their whole mass and no derivative; rectangles
//! certified outside every square contribute nothing (lemma R1). The others
//! contribute a certified lower bound on their overlap area at `c0` (lemma R2,
//! concave sections and trapezoids) and an enclosure of their edge-length
//! derivative (lemmas R4, R5). Points and segments add a lower bound valid
//! over the whole box and no derivative (lemmas B1 to B3).

use std::time::Instant;

use num_bigint::BigInt;
use num_rational::BigRational;

use crate::certificate::{Certificate, Point, Rect, Segment, direction, domain_upper};
use crate::exact::{approx, enclose, of_f64};
use crate::interval::{Iv, add_dn, add_up, dn, fmax, fmin, mul_dn, mul_up, sub_dn, sub_up, up};

/// Absolute slack for classification decisions made in plain binary64
/// (lemma F2: the rounding error of those expressions is below `1e-11` for
/// sides up to `MAX_SIDE`).
pub const TAU: f64 = 1e-9;

/// Search limits for one direction.
#[derive(Clone, Copy, Debug)]
pub struct Limits {
    /// Node budget; exceeding it leaves the direction unresolved.
    pub max_nodes: u64,
    /// Depth budget; exceeding it leaves the direction unresolved.
    pub max_depth: u32,
    /// Audit every `audit_every`-th box (counting from the root, which is always
    /// audited) by recomputing its centre bound from the full rectangle list
    /// with no classification; zero turns the audit off.
    pub audit_every: u64,
    /// A control hook: at this box (1-based), classify the first boundary
    /// rectangle as inside. Never set outside a control run.
    pub inject_fault_at: Option<u64>,
}

/// The verdict of one direction.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Verdict {
    /// Every box of the reduced centre domain was accepted.
    Verified,
    /// A box centre's lower bound is below the threshold by more than the
    /// arithmetic could explain; the centre is reported for exact confirmation.
    CounterexampleCandidate,
    /// A budget ran out first.
    Unresolved,
    /// An audited box's incremental centre bound disagreed with its full
    /// recomputation: the search's bookkeeping is wrong, and nothing it
    /// accepted can be trusted.
    AuditFailed,
    /// A box's bound or derivative enclosure was not finite; lemma F3 proves
    /// this cannot happen for an admitted certificate, so it is a refusal.
    NonFinite,
}

impl Verdict {
    /// The receipt spelling.
    #[must_use]
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Verified => "verified",
            Self::CounterexampleCandidate => "counterexample-candidate",
            Self::Unresolved => "unresolved",
            Self::AuditFailed => "audit-failed",
            Self::NonFinite => "non-finite",
        }
    }
}

/// The outcome of one rotated direction.
#[derive(Clone, Debug)]
pub struct DirectionResult {
    /// Net index.
    pub index: u32,
    /// Verdict.
    pub verdict: Verdict,
    /// Boxes evaluated.
    pub nodes: u64,
    /// Boxes accepted.
    pub leaves: u64,
    /// Deepest box evaluated.
    pub max_depth: u32,
    /// Least accepted lower bound (a certified lower bound on the minimum).
    pub min_lower: f64,
    /// Centre and half-widths of the accepted box with the least bound.
    pub argmin: Option<(f64, f64, f64, f64)>,
    /// For a non-verified direction, the box centre that stopped the search.
    /// `(x, y, centre lower bound, dx, dy)` of that box.
    pub witness: Option<(f64, f64, f64, f64, f64)>,
    /// Wall seconds of this direction's search.
    pub seconds: f64,
    /// Mean number of boundary rectangles per evaluated box.
    pub mean_boundary: f64,
    /// Boxes audited against a full recomputation.
    pub audits: u64,
}

/// Coefficients of the four boundary lines of a centred square, seen from a
/// family of parallel lines (vertical or horizontal), as enclosures.
#[derive(Clone, Copy, Debug)]
struct LineCoeffs {
    /// `h/s` for vertical lines (`h/c` for horizontal ones), and so on with
    /// cosine and sine exchanged.
    hs: Iv,
    hc: Iv,
    cs: Iv,
    sc: Iv,
    isc: Iv,
    two_hs: Iv,
    two_hc: Iv,
    hsum: Iv,
}

/// Per-direction constants.
#[derive(Clone, Copy, Debug)]
struct Frame {
    cf: f64,
    sf: f64,
    /// A lower bound on `h = B/2` (the low end of its enclosure).
    hf: f64,
    /// An upper bound on `h`.
    h_hi: f64,
    /// Direction zero: the square is axis-aligned, and the line coefficients,
    /// which divide by the sine, are unused (lemmas Z1, Z2).
    axis: bool,
    vertical: LineCoeffs,
    horizontal: LineCoeffs,
}

fn quotient(p: &BigRational, q: &BigRational) -> Result<Iv, String> {
    enclose(&(p / q))
}

fn frame(cert: &Certificate, index: u32) -> Result<Frame, String> {
    let (c, s) = direction(&cert.step, index);
    let two = BigRational::from_integer(BigInt::from(2));
    let h = &cert.core / &two;
    let one = BigRational::from_integer(BigInt::from(1));
    let h_iv = enclose(&h)?;
    if index == 0 {
        let zero = Iv::point(0.0);
        let unused = LineCoeffs {
            hs: zero,
            hc: zero,
            cs: zero,
            sc: zero,
            isc: zero,
            two_hs: zero,
            two_hc: zero,
            hsum: zero,
        };
        return Ok(Frame {
            cf: 1.0,
            sf: 0.0,
            hf: h_iv.lo,
            h_hi: h_iv.hi,
            axis: true,
            vertical: unused,
            horizontal: unused,
        });
    }
    let vertical = LineCoeffs {
        hs: quotient(&h, &s)?,
        hc: quotient(&h, &c)?,
        cs: quotient(&c, &s)?,
        sc: quotient(&s, &c)?,
        isc: quotient(&one, &(&s * &c))?,
        two_hs: quotient(&(&two * &h), &s)?,
        two_hc: quotient(&(&two * &h), &c)?,
        hsum: enclose(&(&h / &s + &h / &c))?,
    };
    let horizontal = LineCoeffs {
        hs: vertical.hc,
        hc: vertical.hs,
        cs: vertical.sc,
        sc: vertical.cs,
        isc: vertical.isc,
        two_hs: vertical.two_hc,
        two_hc: vertical.two_hs,
        hsum: vertical.hsum,
    };
    Ok(Frame {
        cf: approx(&c)?,
        sf: approx(&s)?,
        hf: h_iv.lo,
        h_hi: h_iv.hi,
        axis: false,
        vertical,
        horizontal,
    })
}

/// A lower bound on `|[x - h, x + h] ∩ [a, b]|` for `h >= hf` and an interval
/// `[a, b]` inside the exact one (lemma Z1).
#[inline]
fn overlap_dn(x: f64, hf: f64, a: f64, b: f64) -> f64 {
    let right = fmin(add_dn(x, hf), b);
    let left = fmax(sub_up(x, hf), a);
    fmax(sub_dn(right, left), 0.0)
}

/// Lemma Z1: at direction zero the overlap area is the product of two
/// interval overlaps, each bounded below with the inner rectangle and `hf`.
#[inline]
fn area_dn_axis(fr: &Frame, rect: &Rect, x0: f64, y0: f64) -> f64 {
    let ox = overlap_dn(x0, fr.hf, rect.x1.hi, rect.x2.lo);
    let oy = overlap_dn(y0, fr.hf, rect.y1.hi, rect.y2.lo);
    if ox > 0.0 && oy > 0.0 {
        mul_dn(ox, oy)
    } else {
        0.0
    }
}

/// The indicator that `centre + shift` lies in `[a, b]`, for every centre in
/// `[c - d, c + d]` and shift in `[shift_lo, shift_hi]`: one, zero, or either.
#[inline]
fn indicator(c: f64, d: f64, shift_lo: f64, shift_hi: f64, a: Iv, b: Iv) -> Iv {
    let lo = add_dn(sub_dn(c, d), shift_lo);
    let hi = add_up(add_up(c, d), shift_hi);
    if lo >= a.hi && hi <= b.lo {
        Iv::point(1.0)
    } else if hi < a.lo || lo > b.hi {
        Iv::point(0.0)
    } else {
        Iv::new(0.0, 1.0)
    }
}

/// One partial derivative at direction zero (lemma Z2): along the axis with
/// centre range `c +- d` and rectangle side `[a, b]`, across it `oc +- od` and
/// `[oa, ob]`.
#[inline]
fn axis_partial(fr: &Frame, along: (f64, f64, Iv, Iv), across: (f64, f64, Iv, Iv), rho: Iv) -> Iv {
    let (c, d, a, b) = along;
    let (oc, od, oa, ob) = across;
    // The cross overlap is unimodal in its centre, so its least value over a
    // range is at an end; the ends here are rounded outward.
    let ends = fmin(
        overlap_dn(sub_dn(oc, od), fr.hf, oa.hi, ob.lo),
        overlap_dn(add_up(oc, od), fr.hf, oa.hi, ob.lo),
    );
    let most = fmin(up(2.0 * fr.h_hi), sub_up(ob.hi, oa.lo));
    let width = Iv::new(fmin(ends, most), most);
    let plus = indicator(c, d, fr.hf, fr.h_hi, a, b);
    let minus = indicator(c, d, -fr.h_hi, -fr.hf, a, b);
    width.times(plus.minus(minus)).mul_nonneg(rho)
}

/// Lemma Z2: the gradient enclosure of one rectangle at direction zero.
#[inline]
fn gradient_axis(fr: &Frame, g: &BoxGeom, rect: &Rect) -> (Iv, Iv) {
    let x = (g.x0, g.dx, rect.x1, rect.x2);
    let y = (g.y0, g.dy, rect.y1, rect.y2);
    (
        axis_partial(fr, x, y, rect.rho),
        axis_partial(fr, y, x, rect.rho),
    )
}

/// The parameters at which a segment's approximate point lies within `hu` and
/// `hv` of `(x0, y0)` along the square's axes, clipped to `[0, 1]`. A
/// floating-point estimate: whatever uses it for a bound proves its ends.
#[inline]
fn lambda_range(
    fr: &Frame,
    x0: f64,
    y0: f64,
    sg: &Segment,
    hu: f64,
    hv: f64,
) -> Option<(f64, f64)> {
    if hu <= 0.0 || hv <= 0.0 {
        return None;
    }
    let (c, s) = (fr.cf, fr.sf);
    let (ax, ay) = (sg.x0 - x0, sg.y0 - y0);
    let (ex, ey) = (sg.x1 - sg.x0, sg.y1 - sg.y0);
    let (mut lo, mut hi) = (0.0f64, 1.0f64);
    for (a, b, half) in [
        (c * ax + s * ay, c * ex + s * ey, hu),
        (c * ay - s * ax, c * ey - s * ex, hv),
    ] {
        if b.abs() < f64::MIN_POSITIVE {
            if a.abs() > half {
                return None;
            }
            continue;
        }
        let t1 = (-half - a) / b;
        let t2 = (half - a) / b;
        lo = lo.max(t1.min(t2));
        hi = hi.min(t1.max(t2));
    }
    (lo < hi).then_some((lo, hi))
}

/// Lemma B3: a certified lower bound on a segment's mass inside every square
/// of the box. Two parameters are chosen in floating point, and the points at
/// both are then proved inside every square by R1 with zero extent; every
/// point between them is inside too (the square is convex), and the mass is
/// uniform in the parameter.
#[inline]
fn segment_dn(fr: &Frame, g: &BoxGeom, sg: &Segment) -> f64 {
    let (ex, ey) = (sg.x1 - sg.x0, sg.y1 - sg.y0);
    let inside = |lambda: f64| {
        matches!(
            classify_extent(fr, g, sg.x0 + lambda * ex, sg.y0 + lambda * ey, 0.0, 0.0),
            Class::Inside
        )
    };
    if inside(0.0) && inside(1.0) {
        return sg.mass.lo;
    }
    let Some((mut lo, mut hi)) = lambda_range(
        fr,
        g.x0,
        g.y0,
        sg,
        fr.hf - g.bu - 2.0 * TAU,
        fr.hf - g.bv - 2.0 * TAU,
    ) else {
        return 0.0;
    };
    let nudge = (hi - lo) * 1e-9;
    if !inside(lo) {
        lo += nudge;
        if !inside(lo) {
            return 0.0;
        }
    }
    if !inside(hi) {
        hi -= nudge;
        if !inside(hi) {
            return 0.0;
        }
    }
    if lo < hi {
        mul_dn(sg.mass.lo, sub_dn(hi, lo))
    } else {
        0.0
    }
}

/// Classify a segment by its bounding box (lemma B1): a box inside every
/// square holds the segment, one outside every square misses it.
#[inline]
fn classify_segment(fr: &Frame, g: &BoxGeom, sg: &Segment) -> Class {
    classify_extent(
        fr,
        g,
        f64::midpoint(sg.x0, sg.x1),
        f64::midpoint(sg.y0, sg.y1),
        0.5 * (sg.x1 - sg.x0).abs(),
        0.5 * (sg.y1 - sg.y0).abs(),
    )
}

/// The box of zero size at a box's centre.
fn centre_geom(g: &BoxGeom) -> BoxGeom {
    BoxGeom {
        dx: 0.0,
        dy: 0.0,
        bu: 0.0,
        bv: 0.0,
        ..*g
    }
}

/// A certified lower bound on the atom mass inside every square of the box,
/// from the full lists (lemmas B1 to B3): the probes' version.
fn atoms_dn(fr: &Frame, g: &BoxGeom, points: &[Point], segments: &[Segment]) -> f64 {
    let mut total = 0.0;
    for point in points {
        if matches!(
            classify_extent(fr, g, point.x, point.y, 0.0, 0.0),
            Class::Inside
        ) {
            total = add_dn(total, point.mass.lo);
        }
    }
    for sg in segments {
        match classify_segment(fr, g, sg) {
            Class::Inside => total = add_dn(total, sg.mass.lo),
            Class::Outside => {}
            Class::Boundary => total = add_dn(total, segment_dn(fr, g, sg)),
        }
    }
    total
}

/// The straddling atoms of one box, by index into the certificate's lists.
#[derive(Clone, Copy)]
struct Straddling<'a> {
    points: &'a [Point],
    point_ids: &'a [u32],
    segments: &'a [Segment],
    segment_ids: &'a [u32],
}

impl Straddling<'_> {
    /// A certified lower bound on their mass in the square at the box's centre.
    fn centre_dn(&self, fr: &Frame, g: &BoxGeom) -> f64 {
        let centre = centre_geom(g);
        let mut total = 0.0;
        for &id in self.point_ids {
            let point = &self.points[id as usize];
            if matches!(
                classify_extent(fr, &centre, point.x, point.y, 0.0, 0.0),
                Class::Inside
            ) {
                total = add_dn(total, point.mass.lo);
            }
        }
        for &id in self.segment_ids {
            total = add_dn(total, segment_dn(fr, &centre, &self.segments[id as usize]));
        }
        total
    }

    /// An estimate from above of their mass in the square at the box's centre:
    /// it only decides whether a stopped search reports a counterexample
    /// candidate, never whether a box is accepted.
    fn centre_estimate_up(&self, fr: &Frame, g: &BoxGeom) -> f64 {
        let centre = centre_geom(g);
        let mut total = 0.0;
        for &id in self.point_ids {
            let point = &self.points[id as usize];
            if !matches!(
                classify_extent(fr, &centre, point.x, point.y, 0.0, 0.0),
                Class::Outside
            ) {
                total += point.mass.hi;
            }
        }
        let half = fr.h_hi + TAU;
        for &id in self.segment_ids {
            let sg = &self.segments[id as usize];
            if let Some((lo, hi)) = lambda_range(fr, g.x0, g.y0, sg, half, half) {
                total += sg.mass.hi * (hi - lo + 1e-9);
            }
        }
        total * (1.0 + 1e-12)
    }
}

/// What the release audit compares (lemma A3): the mass certified inside every
/// square of the box, and how many items of each kind straddle it.
#[derive(Clone, Copy, Debug)]
struct Tally {
    inside: f64,
    rects: usize,
    points: usize,
    segments: usize,
}

impl Tally {
    /// Every item classified against the box afresh, nothing inherited.
    fn fresh(fr: &Frame, g: &BoxGeom, cert: &Certificate) -> Self {
        let mut tally = Self {
            inside: 0.0,
            rects: 0,
            points: 0,
            segments: 0,
        };
        for rect in &cert.rects {
            match classify(fr, g, rect) {
                Class::Inside => tally.inside = add_dn(tally.inside, rect.mass.lo),
                Class::Outside => {}
                Class::Boundary => tally.rects += 1,
            }
        }
        for point in &cert.points {
            match classify_extent(fr, g, point.x, point.y, 0.0, 0.0) {
                Class::Inside => tally.inside = add_dn(tally.inside, point.mass.lo),
                Class::Outside => {}
                Class::Boundary => tally.points += 1,
            }
        }
        for sg in &cert.segments {
            match classify_segment(fr, g, sg) {
                Class::Inside => tally.inside = add_dn(tally.inside, sg.mass.lo),
                Class::Outside => {}
                Class::Boundary => tally.segments += 1,
            }
        }
        tally
    }

    fn agrees(&self, other: &Self) -> bool {
        self.rects == other.rects
            && self.points == other.points
            && self.segments == other.segments
            && (self.inside - other.inside).abs() <= AUDIT_TOLERANCE * (1.0 + self.inside.abs())
    }
}

/// Lower bound on `k * x` for an interval `k >= 0` and a value `x`.
#[inline]
fn kx_dn(k: Iv, x: f64) -> f64 {
    if x >= 0.0 {
        mul_dn(k.lo, x)
    } else {
        mul_dn(k.hi, x)
    }
}

/// Upper bound on `k * x` for an interval `k >= 0` and a value `x`.
#[inline]
fn kx_up(k: Iv, x: f64) -> f64 {
    if x >= 0.0 {
        mul_up(k.hi, x)
    } else {
        mul_up(k.lo, x)
    }
}

/// Lower bound of `h(xi) = min(e, f1, f2) - max(b, g1, g2)` at offset `xi`,
/// where `e` is a lower and `b` an upper bound of the segment's offsets.
#[inline]
fn section_dn(k: &LineCoeffs, xi: f64, e: f64, b: f64) -> f64 {
    let f1 = sub_dn(k.hs.lo, kx_up(k.cs, xi));
    let f2 = add_dn(k.hc.lo, kx_dn(k.sc, xi));
    let g1 = sub_up(-k.hs.lo, kx_dn(k.cs, xi));
    let g2 = add_up(-k.hc.lo, kx_up(k.sc, xi));
    sub_dn(fmin(fmin(e, f1), f2), fmax(fmax(b, g1), g2))
}

/// A certified lower bound on `|R ∩ Q(c0)|` (lemma R2).
fn area_dn(fr: &Frame, rect: &Rect, x0: f64, y0: f64) -> f64 {
    if fr.axis {
        return area_dn_axis(fr, rect, x0, y0);
    }
    let k = &fr.vertical;
    // The inner representable rectangle [x1.hi, x2.lo] x [y1.hi, y2.lo] lies in R.
    let xi1 = sub_up(rect.x1.hi, x0);
    let xi2 = sub_dn(rect.x2.lo, x0);
    let e = sub_dn(rect.y2.lo, y0);
    let b = sub_up(rect.y1.hi, y0);
    if !(xi1 < xi2 && b < e) {
        return 0.0;
    }
    let (c, s, h) = (fr.cf, fr.sf, fr.hf);
    // Approximate breakpoints of h(xi): its exact positions only affect accuracy.
    // Breakpoints of the concave h are where two of its affine pieces cross;
    // its zeros are added too, so that no trapezoid straddles a sign change by
    // more than rounding (a straddling trapezoid is valid but loses area).
    let mut nodes = [0.0f64; 14];
    nodes[0] = xi1;
    nodes[1] = xi2;
    let candidates = [
        // top and bottom vertices, where f1 = f2 and g1 = g2
        h * (c - s),
        -h * (c - s),
        // e = f1, e = f2, b = g1, b = g2
        (h - s * e) / c,
        (c * e - h) / s,
        -(h + s * b) / c,
        (c * b + h) / s,
        // zeros: right and left vertices (f1 = g2, f2 = g1), e = g1, e = g2,
        // f1 = b, f2 = b
        h * (c + s),
        -h * (c + s),
        -(h + s * e) / c,
        (c * e + h) / s,
        (h - s * b) / c,
        (c * b - h) / s,
    ];
    let mut count = 2;
    for t in candidates {
        if t > xi1 && t < xi2 {
            nodes[count] = t;
            count += 1;
        }
    }
    let nodes = &mut nodes[..count];
    nodes.sort_unstable_by(f64::total_cmp);
    let mut total = 0.0;
    let mut previous_x = nodes[0];
    let mut previous_v = section_dn(k, previous_x, e, b);
    for &x in &nodes[1..] {
        let v = section_dn(k, x, e, b);
        let sum = add_dn(previous_v, v);
        if sum > 0.0 || sum.is_nan() {
            let width = sub_dn(x, previous_x);
            if width > 0.0 {
                total = add_dn(total, dn(mul_dn(sum, width) * 0.5));
            }
        }
        previous_x = x;
        previous_v = v;
    }
    total
}

/// Enclosure over the box of the length of a segment inside the square
/// (lemma R5). `w` encloses the line's offset from the centre, `e`/`b` the
/// segment ends' offsets, `len` its length.
#[inline]
fn segment_length(k: &LineCoeffs, w: Iv, e: Iv, b: Iv, len: Iv) -> Iv {
    let cw = w.mul_nonneg(k.cs);
    let sw = w.mul_nonneg(k.sc);
    let iw = w.mul_nonneg(k.isc);
    let t2 = e.plus(k.hs).plus(cw);
    let t3 = e.plus(k.hc).minus(sw);
    let t4 = k.hs.minus(cw).minus(b);
    let t5 = k.hc.plus(sw).minus(b);
    let t8 = k.hsum.minus(iw);
    let t9 = k.hsum.plus(iw);
    len.min(t2)
        .min(t3)
        .min(t4)
        .min(t5)
        .min(k.two_hs)
        .min(k.two_hc)
        .min(t8)
        .min(t9)
        .pos()
}

/// Offset enclosure `a - (centre +- half)` for a coordinate enclosure `a`.
#[inline]
fn offset(a: Iv, centre: f64, half: f64) -> Iv {
    Iv::new(
        sub_dn(sub_dn(a.lo, centre), half),
        add_up(sub_up(a.hi, centre), half),
    )
}

/// The geometry of one box of centres, shared by every rectangle test.
#[derive(Clone, Copy, Debug)]
struct BoxGeom {
    x0: f64,
    y0: f64,
    dx: f64,
    dy: f64,
    /// Box half-extent along the square's first axis, `c dx + s dy`.
    bu: f64,
    /// Box half-extent along the square's second axis, `s dx + c dy`.
    bv: f64,
    /// Half the square's axis-aligned extent, `h (c + s)`.
    ext: f64,
}

/// Gradient enclosure of one rectangle's overlap area over the box.
#[inline]
fn gradient(fr: &Frame, g: &BoxGeom, rect: &Rect) -> (Iv, Iv) {
    if fr.axis {
        return gradient_axis(fr, g, rect);
    }
    let ylen = rect.y2.minus(rect.y1);
    let xlen = rect.x2.minus(rect.x1);
    let ye = offset(rect.y2, g.y0, g.dy);
    let yb = offset(rect.y1, g.y0, g.dy);
    let xe = offset(rect.x2, g.x0, g.dx);
    let xb = offset(rect.x1, g.x0, g.dx);
    let v = &fr.vertical;
    let hz = &fr.horizontal;
    let left = segment_length(v, xb, ye, yb, ylen);
    let right = segment_length(v, xe, ye, yb, ylen);
    let bottom = segment_length(hz, yb, xe, xb, xlen);
    let top = segment_length(hz, ye, xe, xb, xlen);
    (
        left.minus(right).mul_nonneg(rect.rho),
        bottom.minus(top).mul_nonneg(rect.rho),
    )
}

#[derive(Clone, Copy, Debug)]
enum Class {
    Inside,
    Outside,
    Boundary,
}

/// Classify an axis-aligned rectangle with centre `(mx, my)` and half-sizes
/// `(wx, wy)` against every square centred in the box (lemma R1). The
/// comparisons carry the slack `TAU`, which exceeds their rounding error.
#[inline]
fn classify_extent(fr: &Frame, g: &BoxGeom, mx: f64, my: f64, wx: f64, wy: f64) -> Class {
    let (c, s, h) = (fr.cf, fr.sf, fr.hf);
    let ddx = mx - g.x0;
    let ddy = my - g.y0;
    let du = (c * ddx + s * ddy).abs();
    let dv = (c * ddy - s * ddx).abs();
    let eu = c * wx + s * wy;
    let ev = s * wx + c * wy;
    if du + eu + g.bu + TAU <= h && dv + ev + g.bv + TAU <= h {
        return Class::Inside;
    }
    if du >= eu + h + g.bu + TAU
        || dv >= ev + h + g.bv + TAU
        || ddx.abs() >= wx + g.dx + g.ext + TAU
        || ddy.abs() >= wy + g.dy + g.ext + TAU
    {
        return Class::Outside;
    }
    Class::Boundary
}

/// Classify a rectangle against every square centred in the box.
#[inline]
fn classify(fr: &Frame, g: &BoxGeom, rect: &Rect) -> Class {
    classify_extent(fr, g, rect.mx, rect.my, rect.wx, rect.wy)
}

#[derive(Clone, Copy, Debug)]
struct Node {
    xl: f64,
    xh: f64,
    yl: f64,
    yh: f64,
    depth: u32,
    parent_start: usize,
    parent_end: usize,
    inner: f64,
    /// Bounds on `|dF/dx|`, `|dF/dy|` proved over the parent box, which
    /// contains this one, so valid here (infinite at the root).
    gx_inherited: f64,
    gy_inherited: f64,
    /// The parent's straddling points and segments (arena ranges) and the
    /// atom mass certified inside every square of the parent (lemma B1).
    point_start: usize,
    point_end: usize,
    segment_start: usize,
    segment_end: usize,
    atom_inner: f64,
}

/// Indices `0..count` for an arena.
fn ids(count: usize, what: &str) -> Result<Vec<u32>, String> {
    Ok((0..u32::try_from(count).map_err(|_| format!("too many {what}"))?).collect())
}

/// How many boxes may reach the depth limit before the search stops: past one,
/// it continues only to look for a counterexample candidate elsewhere.
const MAX_DEEP_BOXES: u64 = 4096;

/// How many of those boxes have their centre's capture evaluated exactly.
const MAX_EXACT_CENTRES: u64 = 32;

/// Verify one net direction by branch and bound: any `index >= 1`, and
/// `index = 0` for a measure with points or segments.
///
/// # Errors
///
/// Returns a message if a constant cannot be enclosed.
pub fn verify_direction(
    cert: &Certificate,
    index: u32,
    threshold: &BigRational,
    threshold_hi: f64,
    limits: Limits,
) -> Result<DirectionResult, String> {
    let start = Instant::now();
    let fr = frame(cert, index)?;
    let (c, s) = direction(&cert.step, index);
    let two = BigRational::from_integer(BigInt::from(2));
    let extent = &cert.core * (&c + &s) / &two;
    let lower = enclose(&(&cert.side / &two))?.lo;
    let upper = enclose(&domain_upper(cert, index)?)?.hi;
    // Half the axis-aligned extent of the square, an upper bound with slack.
    let ext = approx(&extent)?;

    let rects = &cert.rects;
    let points: &[Point] = &cert.points;
    let segments: &[Segment] = &cert.segments;
    let mut arena = ids(rects.len(), "rectangles")?;
    let mut point_arena = ids(points.len(), "points")?;
    let mut segment_arena = ids(segments.len(), "segments")?;
    let mut stack = vec![Node {
        xl: lower,
        xh: upper,
        yl: lower,
        yh: upper,
        depth: 0,
        parent_start: 0,
        parent_end: rects.len(),
        inner: 0.0,
        gx_inherited: f64::INFINITY,
        gy_inherited: f64::INFINITY,
        point_start: 0,
        point_end: points.len(),
        segment_start: 0,
        segment_end: segments.len(),
        atom_inner: 0.0,
    }];
    let mut nodes = 0u64;
    let mut leaves = 0u64;
    let mut max_depth = 0u32;
    let mut min_lower = f64::INFINITY;
    let mut argmin = None;
    let mut boundary_total = 0u64;
    let mut audits = 0u64;
    let mut verdict = Verdict::Verified;
    let mut witness = None;
    // Boxes left at the depth limit: the search goes on past them, so that a
    // counterexample elsewhere is still found, and the first is reported.
    let mut deep_boxes = 0u64;
    let mut deep_witness = None;
    while let Some(node) = stack.pop() {
        arena.truncate(node.parent_end);
        point_arena.truncate(node.point_end);
        segment_arena.truncate(node.segment_end);
        nodes += 1;
        max_depth = max_depth.max(node.depth);
        let x0 = f64::midpoint(node.xl, node.xh);
        let y0 = f64::midpoint(node.yl, node.yh);
        let dx = up((node.xh - x0).max(x0 - node.xl));
        let dy = up((node.yh - y0).max(y0 - node.yl));
        let g = BoxGeom {
            x0,
            y0,
            dx,
            dy,
            bu: fr.cf * dx + fr.sf * dy,
            bv: fr.sf * dx + fr.cf * dy,
            ext,
        };
        let mut inner = node.inner;
        let own_start = arena.len();
        let mut inject = limits.inject_fault_at == Some(nodes);
        for position in node.parent_start..node.parent_end {
            let id = arena[position];
            let rect = &rects[id as usize];
            match classify(&fr, &g, rect) {
                Class::Inside => inner = add_dn(inner, rect.mass.lo),
                Class::Outside => {}
                Class::Boundary if inject => {
                    inject = false;
                    inner = add_dn(inner, rect.mass.lo);
                }
                Class::Boundary => arena.push(id),
            }
        }
        let own_end = arena.len();
        boundary_total += (own_end - own_start) as u64;
        // Points and segments (lemmas B1 to B3): mass proved inside every square
        // of the box is inherited by its sub-boxes; a straddling segment adds
        // the part of it proved inside here, and a straddling point nothing.
        let mut atom_inner = node.atom_inner;
        let own_point_start = point_arena.len();
        for position in node.point_start..node.point_end {
            let id = point_arena[position];
            let point = &points[id as usize];
            match classify_extent(&fr, &g, point.x, point.y, 0.0, 0.0) {
                Class::Inside => atom_inner = add_dn(atom_inner, point.mass.lo),
                Class::Outside => {}
                Class::Boundary if inject => {
                    inject = false;
                    atom_inner = add_dn(atom_inner, point.mass.lo);
                }
                Class::Boundary => point_arena.push(id),
            }
        }
        let own_point_end = point_arena.len();
        let own_segment_start = segment_arena.len();
        let mut straddling = 0.0;
        for position in node.segment_start..node.segment_end {
            let id = segment_arena[position];
            let sg = &segments[id as usize];
            match classify_segment(&fr, &g, sg) {
                Class::Inside => atom_inner = add_dn(atom_inner, sg.mass.lo),
                Class::Outside => {}
                Class::Boundary if inject => {
                    inject = false;
                    atom_inner = add_dn(atom_inner, sg.mass.lo);
                }
                Class::Boundary => {
                    segment_arena.push(id);
                    straddling = add_dn(straddling, segment_dn(&fr, &g, sg));
                }
            }
        }
        let own_segment_end = segment_arena.len();
        let atoms = add_dn(atom_inner, straddling);
        let atom_lists = Straddling {
            points,
            point_ids: &point_arena[own_point_start..own_point_end],
            segments,
            segment_ids: &segment_arena[own_segment_start..own_segment_end],
        };
        let mut value = inner;
        for position in own_start..own_end {
            let rect = &rects[arena[position] as usize];
            value = add_dn(value, mul_dn(rect.rho.lo, area_dn(&fr, rect, x0, y0)));
        }
        // Lemma F3: every quantity that can decide acceptance is finite for an
        // admitted certificate; one that is not stops the direction.
        if !(value.is_finite() && atoms.is_finite()) {
            verdict = Verdict::NonFinite;
            witness = Some((x0, y0, value, dx, dy));
            break;
        }
        // Lemma A3: the audit recomputes the centre bound from every rectangle,
        // using no classification and nothing inherited, and classifies every
        // item afresh; a disagreement means the incremental bookkeeping (R1's
        // inheritance) is wrong, and stops the search.
        if limits.audit_every > 0 && (nodes - 1).is_multiple_of(limits.audit_every) {
            audits += 1;
            let full = full_centre_bound(&fr, rects, x0, y0);
            let slack = representation_slack(&fr, &g, rects);
            let incremental = Tally {
                inside: add_dn(inner, atom_inner),
                rects: own_end - own_start,
                points: own_point_end - own_point_start,
                segments: own_segment_end - own_segment_start,
            };
            if (full - value).abs() > AUDIT_TOLERANCE * (1.0 + full.abs()) + slack
                || (full - value).is_nan()
                || !Tally::fresh(&fr, &g, cert).agrees(&incremental)
            {
                verdict = Verdict::AuditFailed;
                witness = Some((x0, y0, add_dn(value, atom_lists.centre_dn(&fr, &g)), dx, dy));
                break;
            }
        }
        // Lemma R3 with the parent's derivative bounds, valid on this sub-box:
        // a box that certifies with them needs no derivative work of its own.
        if node.gx_inherited.is_finite() && node.gy_inherited.is_finite() {
            let penalty = add_up(mul_up(node.gx_inherited, dx), mul_up(node.gy_inherited, dy));
            let bound = add_dn(sub_dn(value, penalty), atoms);
            if bound >= threshold_hi {
                leaves += 1;
                if bound < min_lower {
                    min_lower = bound;
                    argmin = Some((x0, y0, dx, dy));
                }
                continue;
            }
        }
        let mut gx = Iv::point(0.0);
        let mut gy = Iv::point(0.0);
        for position in own_start..own_end {
            let (rx, ry) = gradient(&fr, &g, &rects[arena[position] as usize]);
            gx = gx.plus(rx);
            gy = gy.plus(ry);
        }
        if !(gx.is_valid() && gy.is_valid()) {
            verdict = Verdict::NonFinite;
            witness = Some((x0, y0, value, dx, dy));
            break;
        }
        // Both this box's enclosure and the inherited one bound the derivative here.
        let gx_bound = gx.mag().min(node.gx_inherited);
        let gy_bound = gy.mag().min(node.gy_inherited);
        let px = mul_up(gx_bound, dx);
        let py = mul_up(gy_bound, dy);
        let bound = add_dn(sub_dn(value, add_up(px, py)), atoms);
        if bound >= threshold_hi {
            leaves += 1;
            if bound < min_lower {
                min_lower = bound;
                argmin = Some((x0, y0, dx, dy));
            }
            continue;
        }
        // The rectangles' centre bound is within about 1e-11 of their exact
        // capture (lemma R2's nodes sit at the breakpoints). With an estimate
        // from above of the atoms there, a centre this far below the threshold
        // is almost surely a counterexample; `--confirm` decides it exactly.
        if add_dn(value, atoms) < threshold_hi - 1e-9
            && value + atom_inner + atom_lists.centre_estimate_up(&fr, &g) < threshold_hi - 1e-9
        {
            verdict = Verdict::CounterexampleCandidate;
            witness = Some((
                x0,
                y0,
                add_dn(value, add_dn(atom_inner, atom_lists.centre_dn(&fr, &g))),
                dx,
                dy,
            ));
            break;
        }
        if node.depth >= limits.max_depth || nodes >= limits.max_nodes {
            let here = (
                x0,
                y0,
                add_dn(value, add_dn(atom_inner, atom_lists.centre_dn(&fr, &g))),
                dx,
                dy,
            );
            deep_witness.get_or_insert(here);
            deep_boxes += 1;
            // The first few such centres are evaluated exactly: one below the
            // threshold is a refutation, which a band of centres within the
            // floating-point estimate's error of the threshold would hide.
            if deep_boxes <= MAX_EXACT_CENTRES
                && &crate::oracle::coverage(cert, &of_f64(x0), &of_f64(y0), &c, &s) < threshold
            {
                verdict = Verdict::CounterexampleCandidate;
                witness = Some(here);
                break;
            }
            if nodes >= limits.max_nodes || deep_boxes >= MAX_DEEP_BOXES {
                verdict = Verdict::Unresolved;
                witness = deep_witness;
                break;
            }
            continue;
        }
        // Split where the derivative penalty is larger, unless straddling atoms
        // cost more than the penalty does: they stop straddling only as the box
        // shrinks along both axes, so then halve the longer side.
        let atom_led = !(atom_lists.point_ids.is_empty() && atom_lists.segment_ids.is_empty())
            && add_up(px, py) < 0.5 * (threshold_hi - bound);
        let split_x = if atom_led || px == py {
            dx >= dy
        } else {
            px > py
        };
        let child = |xl, xh, yl, yh| Node {
            xl,
            xh,
            yl,
            yh,
            depth: node.depth + 1,
            parent_start: own_start,
            parent_end: own_end,
            inner,
            gx_inherited: gx_bound,
            gy_inherited: gy_bound,
            point_start: own_point_start,
            point_end: own_point_end,
            segment_start: own_segment_start,
            segment_end: own_segment_end,
            atom_inner,
        };
        let halves = if split_x {
            (x0 > node.xl && x0 < node.xh).then(|| {
                (
                    child(x0, node.xh, node.yl, node.yh),
                    child(node.xl, x0, node.yl, node.yh),
                )
            })
        } else {
            (y0 > node.yl && y0 < node.yh).then(|| {
                (
                    child(node.xl, node.xh, y0, node.yh),
                    child(node.xl, node.xh, node.yl, y0),
                )
            })
        };
        let Some((second, first)) = halves else {
            verdict = Verdict::Unresolved;
            witness = Some((
                x0,
                y0,
                add_dn(value, add_dn(atom_inner, atom_lists.centre_dn(&fr, &g))),
                dx,
                dy,
            ));
            break;
        };
        stack.push(second);
        stack.push(first);
    }
    if verdict == Verdict::Verified && deep_witness.is_some() {
        verdict = Verdict::Unresolved;
        witness = deep_witness;
    }
    Ok(DirectionResult {
        index,
        verdict,
        nodes,
        leaves,
        max_depth,
        min_lower: if verdict == Verdict::Verified {
            min_lower
        } else {
            f64::NAN
        },
        argmin,
        witness,
        seconds: start.elapsed().as_secs_f64(),
        mean_boundary: boundary_total as f64 / nodes.max(1) as f64,
        audits,
    })
}

/// A certified lower bound on the mass captured at one centre, summed over
/// every rectangle without classification: the differential-test probe.
///
/// # Errors
///
/// Returns a message if a constant cannot be enclosed.
pub fn centre_lower_bound(cert: &Certificate, index: u32, x0: f64, y0: f64) -> Result<f64, String> {
    let fr = frame(cert, index)?;
    let g = probe_geom(cert, &fr, index, (x0, y0, 0.0, 0.0))?;
    Ok(add_dn(
        full_centre_bound(&fr, &cert.rects, x0, y0),
        atoms_dn(&fr, &g, &cert.points, &cert.segments),
    ))
}

/// The estimate from above of the mass captured at one centre that decides
/// whether a stopped search reports a counterexample candidate: the probe that
/// shows why a centre was, or was not, reported.
///
/// # Errors
///
/// Returns a message if a constant cannot be enclosed.
pub fn centre_estimate_up(cert: &Certificate, index: u32, x0: f64, y0: f64) -> Result<f64, String> {
    let fr = frame(cert, index)?;
    let g = probe_geom(cert, &fr, index, (x0, y0, 0.0, 0.0))?;
    let point_ids = ids(cert.points.len(), "points")?;
    let segment_ids = ids(cert.segments.len(), "segments")?;
    let lists = Straddling {
        points: &cert.points,
        point_ids: &point_ids,
        segments: &cert.segments,
        segment_ids: &segment_ids,
    };
    Ok(full_centre_bound(&fr, &cert.rects, x0, y0) + lists.centre_estimate_up(&fr, &g))
}

/// The geometry of a probe box `(x0, y0, dx, dy)`.
fn probe_geom(
    cert: &Certificate,
    fr: &Frame,
    index: u32,
    b: (f64, f64, f64, f64),
) -> Result<BoxGeom, String> {
    let (c, s) = direction(&cert.step, index);
    let two = BigRational::from_integer(BigInt::from(2));
    let (x0, y0, dx, dy) = b;
    Ok(BoxGeom {
        x0,
        y0,
        dx,
        dy,
        bu: fr.cf * dx + fr.sf * dy,
        bv: fr.sf * dx + fr.cf * dy,
        ext: approx(&(&cert.core * (&c + &s) / &two))?,
    })
}

/// The audit's tolerance, relative to the bound: the incremental and full sums
/// differ only by rounding (inside masses enter as exact enclosures, the full
/// sum through lemma R2), far below this.
const AUDIT_TOLERANCE: f64 = 1e-9;

/// An upper bound on how much lemma R2's inner representable rectangles can
/// lose against the exact ones at the box's centre: for each rectangle that can
/// meet the centre's square, its density times the area between its outer and
/// inner representable rectangles. The incremental sum counts an inside
/// rectangle by its exact mass, the full recomputation by R2, so this is the
/// gap the audit must allow besides rounding (finding TI-1 of the 3 October
/// testing review: slivers of extreme density).
fn representation_slack(fr: &Frame, g: &BoxGeom, rects: &[Rect]) -> f64 {
    let centre = centre_geom(g);
    let mut slack = 0.0;
    for rect in rects {
        if matches!(classify(fr, &centre, rect), Class::Outside) {
            continue;
        }
        let outer = mul_up(
            sub_up(rect.x2.hi, rect.x1.lo),
            sub_up(rect.y2.hi, rect.y1.lo),
        );
        let inner = mul_dn(
            fmax(sub_dn(rect.x2.lo, rect.x1.hi), 0.0),
            fmax(sub_dn(rect.y2.lo, rect.y1.hi), 0.0),
        );
        slack = add_up(slack, mul_up(rect.rho.hi, sub_up(outer, inner)));
    }
    slack
}

/// The centre bound from every rectangle, by lemma R2 alone.
fn full_centre_bound(fr: &Frame, rects: &[Rect], x0: f64, y0: f64) -> f64 {
    let mut value = 0.0;
    for rect in rects {
        value = add_dn(value, mul_dn(rect.rho.lo, area_dn(fr, rect, x0, y0)));
    }
    value
}

/// A certified lower bound over a whole box of centres, from the root's full
/// rectangle list: the differential-test probe for boxes.
///
/// # Errors
///
/// Returns a message if a constant cannot be enclosed.
pub fn box_lower_bound(
    cert: &Certificate,
    index: u32,
    x0: f64,
    y0: f64,
    dx: f64,
    dy: f64,
) -> Result<f64, String> {
    let fr = frame(cert, index)?;
    let g = probe_geom(cert, &fr, index, (x0, y0, dx, dy))?;
    let mut value = 0.0;
    let mut gx = Iv::point(0.0);
    let mut gy = Iv::point(0.0);
    for rect in &cert.rects {
        match classify(&fr, &g, rect) {
            Class::Inside => value = add_dn(value, rect.mass.lo),
            Class::Outside => {}
            Class::Boundary => {
                value = add_dn(value, mul_dn(rect.rho.lo, area_dn(&fr, rect, x0, y0)));
                let (rx, ry) = gradient(&fr, &g, rect);
                gx = gx.plus(rx);
                gy = gy.plus(ry);
            }
        }
    }
    Ok(add_dn(
        sub_dn(value, add_up(mul_up(gx.mag(), dx), mul_up(gy.mag(), dy))),
        atoms_dn(&fr, &g, &cert.points, &cert.segments),
    ))
}

#[cfg(test)]
#[path = "rotated_tests.rs"]
mod tests;
