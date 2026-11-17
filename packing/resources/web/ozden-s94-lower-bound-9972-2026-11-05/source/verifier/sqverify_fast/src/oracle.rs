//! Exact rational coverage at one centre: the fallback that confirms a
//! counterexample candidate, and the reference for differential tests.
//!
//! The rotated square is clipped against each rectangle by the four
//! axis-aligned half-planes (Sutherland--Hodgman) in exact rationals and the
//! clipped polygon's area is the shoelace sum. A point counts when it lies in
//! the closed square, a segment by the parametric length of its closed
//! intersection (spec 1.2). Nothing here is rounded.

use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{Signed, Zero};

use crate::certificate::{Certificate, ExactRect};

/// Clip `[lo, hi]` to the parameters where `a + lambda b` lies in `[-h, h]`.
fn clip_parameter(
    a: &BigRational,
    b: &BigRational,
    h: &BigRational,
    lo: &mut BigRational,
    hi: &mut BigRational,
) {
    if b.is_zero() {
        if &a.abs() > h {
            *hi = lo.clone();
        }
        return;
    }
    let t1 = (-h - a) / b;
    let t2 = (h - a) / b;
    let (t_lo, t_hi) = if t1 <= t2 { (t1, t2) } else { (t2, t1) };
    if t_lo > *lo {
        *lo = t_lo;
    }
    if t_hi < *hi {
        *hi = t_hi;
    }
}

type Point = (BigRational, BigRational);

/// Corners of the square of side `side` centred at `(x, y)` with direction
/// `(c, s)`, counterclockwise.
#[must_use]
pub fn square(
    x: &BigRational,
    y: &BigRational,
    c: &BigRational,
    s: &BigRational,
    side: &BigRational,
) -> Vec<Point> {
    let two = BigRational::from_integer(BigInt::from(2));
    let h = side / &two;
    [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        .iter()
        .map(|&(u, v)| {
            let u = BigRational::from_integer(BigInt::from(u)) * &h;
            let v = BigRational::from_integer(BigInt::from(v)) * &h;
            (x + c * &u - s * &v, y + s * &u + c * &v)
        })
        .collect()
}

fn clip(polygon: &[Point], axis: usize, edge: &BigRational, keep_above: bool) -> Vec<Point> {
    let coordinate = |p: &Point| if axis == 0 { p.0.clone() } else { p.1.clone() };
    let inside = |p: &Point| {
        let v = coordinate(p);
        if keep_above { &v >= edge } else { &v <= edge }
    };
    let mut output = Vec::with_capacity(polygon.len() + 2);
    let Some(mut previous) = polygon.last().cloned() else {
        return output;
    };
    let mut previous_inside = inside(&previous);
    for current in polygon {
        let current_inside = inside(current);
        if current_inside != previous_inside {
            let a = coordinate(&previous);
            let b = coordinate(current);
            let t = (&a - edge) / (&a - &b);
            output.push((
                &previous.0 + &t * (&current.0 - &previous.0),
                &previous.1 + &t * (&current.1 - &previous.1),
            ));
        }
        if current_inside {
            output.push(current.clone());
        }
        previous = current.clone();
        previous_inside = current_inside;
    }
    output
}

/// Exact area of a rectangle's intersection with a convex polygon.
#[must_use]
pub fn intersection_area(rect: &ExactRect, polygon: &[Point]) -> BigRational {
    let mut clipped = polygon.to_vec();
    for (axis, edge, keep_above) in [
        (0, &rect.x1, true),
        (0, &rect.x2, false),
        (1, &rect.y1, true),
        (1, &rect.y2, false),
    ] {
        clipped = clip(&clipped, axis, edge, keep_above);
        if clipped.len() < 3 {
            return BigRational::zero();
        }
    }
    let mut twice = BigRational::zero();
    for (index, p) in clipped.iter().enumerate() {
        let q = &clipped[(index + 1) % clipped.len()];
        twice += &p.0 * &q.1 - &p.1 * &q.0;
    }
    twice.abs() / BigRational::from_integer(BigInt::from(2))
}

/// Exact mass captured by the shrunk square centred at `(x, y)` at direction
/// `(c, s)`.
#[must_use]
pub fn coverage(
    cert: &Certificate,
    x: &BigRational,
    y: &BigRational,
    c: &BigRational,
    s: &BigRational,
) -> BigRational {
    let polygon = square(x, y, c, s, &cert.core);
    let left = polygon
        .iter()
        .map(|p| &p.0)
        .min()
        .cloned()
        .unwrap_or_default();
    let right = polygon
        .iter()
        .map(|p| &p.0)
        .max()
        .cloned()
        .unwrap_or_default();
    let bottom = polygon
        .iter()
        .map(|p| &p.1)
        .min()
        .cloned()
        .unwrap_or_default();
    let top = polygon
        .iter()
        .map(|p| &p.1)
        .max()
        .cloned()
        .unwrap_or_default();
    let mut total = BigRational::zero();
    for rect in &cert.exact {
        if rect.x2 <= left || rect.x1 >= right || rect.y2 <= bottom || rect.y1 >= top {
            continue;
        }
        total += &rect.density * intersection_area(rect, &polygon);
    }
    let h = &cert.core / BigRational::from_integer(BigInt::from(2));
    // Local coordinates along the square's axes u = (c, s) and v = (-s, c).
    let local = |px: &BigRational, py: &BigRational| {
        let (dx, dy) = (px - x, py - y);
        (c * &dx + s * &dy, c * &dy - s * &dx)
    };
    for point in &cert.exact_points {
        let (u, v) = local(&point.x, &point.y);
        if u.abs() <= h && v.abs() <= h {
            total += &point.mass;
        }
    }
    for segment in &cert.exact_segments {
        let (u0, v0) = local(&segment.p0.0, &segment.p0.1);
        let (u1, v1) = local(&segment.p1.0, &segment.p1.1);
        let mut lo = BigRational::zero();
        let mut hi = BigRational::from_integer(BigInt::from(1));
        clip_parameter(&u0, &(&u1 - &u0), &h, &mut lo, &mut hi);
        clip_parameter(&v0, &(&v1 - &v0), &h, &mut lo, &mut hi);
        if hi > lo {
            total += &segment.mass * (hi - lo);
        }
    }
    total
}
