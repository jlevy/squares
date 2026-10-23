//! Property and differential tests of the rotated-direction bounds against the
//! exact rational oracle.

use super::*;
use crate::certificate::{Domain, ExactPoint, ExactRect, ExactSegment};
use crate::exact::of_f64;
use crate::oracle::{coverage, intersection_area, square};
use num_traits::ToPrimitive;

fn ratio(p: i64, q: i64) -> BigRational {
    BigRational::new(BigInt::from(p), BigInt::from(q))
}

fn lcg(state: &mut u64) -> f64 {
    *state = state
        .wrapping_mul(6_364_136_223_846_793_005)
        .wrapping_add(1_442_695_040_888_963_407);
    (*state >> 11) as f64 / (1u64 << 53) as f64
}

pub(crate) fn test_cert(rects: Vec<ExactRect>) -> Certificate {
    let floats = rects
        .iter()
        .map(|r| {
            let mass = &r.density * (&r.x2 - &r.x1) * (&r.y2 - &r.y1);
            crate::certificate::float_rect(r, &mass).unwrap()
        })
        .collect();
    Certificate {
        n: 100,
        side: ratio(6, 1),
        core: ratio(9977, 10000),
        step: ratio(83, 40000),
        angle_count: 201,
        mass: ratio(1, 1),
        source_rectangles: rects.len(),
        exact: rects,
        rects: floats,
        input_sha256: String::new(),
        declared_threshold: None,
        format: "T",
        domain: Domain::Tokoharu,
        exact_points: Vec::new(),
        points: Vec::new(),
        exact_segments: Vec::new(),
        segments: Vec::new(),
    }
}

fn random_rects(state: &mut u64, count: usize) -> Vec<ExactRect> {
    (0..count)
        .map(|_| {
            let x = (lcg(state) * 4_000_000.0) as i64 + 1_000_000;
            let y = (lcg(state) * 4_000_000.0) as i64 + 1_000_000;
            let w = (lcg(state) * 900_000.0) as i64 + 1_000;
            let h = (lcg(state) * 900_000.0) as i64 + 1_000;
            ExactRect {
                x1: ratio(x, 1_000_000),
                y1: ratio(y, 1_000_000),
                x2: ratio(x + w, 1_000_000),
                y2: ratio(y + h, 1_000_000),
                density: ratio(1, 1),
            }
        })
        .collect()
}

#[test]
fn area_lower_bound_is_below_and_close_to_exact() {
    let mut state = 7u64;
    let cert = test_cert(random_rects(&mut state, 300));
    for index in [0u32, 1, 2, 37, 100, 199, 200] {
        let fr = frame(&cert, index).unwrap();
        let (c, s) = direction(&cert.step, index);
        for _ in 0..12 {
            let x0 = 2.0 + 2.0 * lcg(&mut state);
            let y0 = 2.0 + 2.0 * lcg(&mut state);
            let polygon = square(&of_f64(x0), &of_f64(y0), &c, &s, &cert.core);
            for (exact, rect) in cert.exact.iter().zip(&cert.rects) {
                let truth = intersection_area(exact, &polygon);
                let bound = area_dn(&fr, rect, x0, y0);
                assert!(
                    of_f64(bound) <= truth,
                    "area bound {bound} above exact {} at r={index}",
                    truth.to_f64().unwrap()
                );
                let gap = truth.to_f64().unwrap() - bound;
                assert!(
                    gap < 1e-9,
                    "area bound {bound} loose by {gap} at r={index}, rect {rect:?}, centre ({x0}, {y0})"
                );
            }
        }
    }
}

/// Exact length of the vertical segment `{a} x [b, e]` inside the square of
/// direction `(c, s)` and half-side `h` centred at `(x, y)`.
fn exact_vertical_length(
    a: &BigRational,
    b: &BigRational,
    e: &BigRational,
    x: &BigRational,
    y: &BigRational,
    c: &BigRational,
    s: &BigRational,
    h: &BigRational,
) -> BigRational {
    let xi = a - x;
    let f1 = (h - c * &xi) / s;
    let f2 = (h + s * &xi) / c;
    let g1 = (-h - c * &xi) / s;
    let g2 = (s * &xi - h) / c;
    let top = (e - y).min(f1).min(f2);
    let bottom = (b - y).max(g1).max(g2);
    let length = top - bottom;
    if length > BigRational::from_integer(BigInt::from(0)) {
        length
    } else {
        BigRational::from_integer(BigInt::from(0))
    }
}

#[test]
fn edge_length_enclosures_contain_exact_lengths_over_the_box() {
    let mut state = 11u64;
    let cert = test_cert(random_rects(&mut state, 4));
    let two = ratio(2, 1);
    let h = &cert.core / &two;
    for index in [1u32, 2, 50, 133, 200] {
        let fr = frame(&cert, index).unwrap();
        let (c, s) = direction(&cert.step, index);
        for _ in 0..400 {
            let x0 = 3.0 + lcg(&mut state);
            let y0 = 3.0 + lcg(&mut state);
            let dx = 10f64.powf(-1.0 - 4.0 * lcg(&mut state));
            let dy = 10f64.powf(-1.0 - 4.0 * lcg(&mut state));
            // A vertical segment near the square's boundary, so all regimes occur.
            let a = x0 + (lcg(&mut state) - 0.5) * 1.4;
            let b = y0 + (lcg(&mut state) - 0.5) * 1.6;
            let e = b + lcg(&mut state) * 0.6 + 1e-6;
            let w = offset(Iv::point(a), x0, dx);
            let ev = offset(Iv::point(e), y0, dy);
            let bv = offset(Iv::point(b), y0, dy);
            let len = Iv::point(e).minus(Iv::point(b));
            let enclosure = segment_length(&fr.vertical, w, ev, bv, len);
            for (u, v) in [
                (-1.0, -1.0),
                (1.0, 1.0),
                (-1.0, 1.0),
                (0.3, -0.7),
                (0.0, 0.0),
            ] {
                let px = of_f64(x0) + of_f64(u) * of_f64(dx);
                let py = of_f64(y0) + of_f64(v) * of_f64(dy);
                let exact =
                    exact_vertical_length(&of_f64(a), &of_f64(b), &of_f64(e), &px, &py, &c, &s, &h);
                assert!(
                    of_f64(enclosure.lo) <= exact && exact <= of_f64(enclosure.hi),
                    "r={index}: {enclosure:?} misses {}",
                    exact.to_f64().unwrap()
                );
            }
        }
    }
}

fn box_geom(fr: &Frame, x0: f64, y0: f64, dx: f64, dy: f64) -> BoxGeom {
    BoxGeom {
        x0,
        y0,
        dx,
        dy,
        bu: fr.cf * dx + fr.sf * dy,
        bv: fr.sf * dx + fr.cf * dy,
        ext: 1.0,
    }
}

/// A difference quotient over an interval inside the box is an average of the
/// derivative there, so it lies in any interval enclosing the derivative on
/// the box (lemmas R4, R5 and, at direction zero, Z2).
#[test]
fn gradient_enclosures_contain_difference_quotients() {
    let mut state = 13u64;
    let cert = test_cert(random_rects(&mut state, 40));
    let half = ratio(1, 2);
    let quarter = ratio(1, 4);
    for index in [0u32, 1, 77, 200] {
        let fr = frame(&cert, index).unwrap();
        let (c, s) = direction(&cert.step, index);
        for _ in 0..40 {
            let x0 = 2.5 + 1.5 * lcg(&mut state);
            let y0 = 2.5 + 1.5 * lcg(&mut state);
            let dx = 10f64.powf(-0.5 - 3.0 * lcg(&mut state));
            let dy = 10f64.powf(-0.5 - 3.0 * lcg(&mut state));
            let g = box_geom(&fr, x0, y0, dx, dy);
            let px = of_f64(x0) + of_f64(2.0 * lcg(&mut state) - 1.0) * of_f64(dx) * &half;
            let py = of_f64(y0) + of_f64(2.0 * lcg(&mut state) - 1.0) * of_f64(dy) * &half;
            let ex = of_f64(dx) * &quarter;
            let ey = of_f64(dy) * &quarter;
            let area = |x: &BigRational, y: &BigRational, rect: &ExactRect| {
                intersection_area(rect, &square(x, y, &c, &s, &cert.core))
            };
            for (exact, rect) in cert.exact.iter().zip(&cert.rects) {
                let (gx, gy) = gradient(&fr, &g, rect);
                let qx = (area(&(&px + &ex), &py, exact) - area(&(&px - &ex), &py, exact))
                    / (&ex * ratio(2, 1));
                let qy = (area(&px, &(&py + &ey), exact) - area(&px, &(&py - &ey), exact))
                    / (&ey * ratio(2, 1));
                assert!(
                    of_f64(gx.lo) <= qx && qx <= of_f64(gx.hi),
                    "r={index}: x enclosure {gx:?} misses {}",
                    qx.to_f64().unwrap()
                );
                assert!(
                    of_f64(gy.lo) <= qy && qy <= of_f64(gy.hi),
                    "r={index}: y enclosure {gy:?} misses {}",
                    qy.to_f64().unwrap()
                );
            }
        }
    }
}

/// A certificate of random points and segments (some axis-parallel) near
/// `(3, 3)`, exact and enclosed alike.
fn atom_cert(state: &mut u64, count: usize) -> Certificate {
    let mut cert = test_cert(Vec::new());
    let mass = ratio(1, 3);
    let mass_iv = crate::exact::enclose(&mass).unwrap();
    let coordinate = |state: &mut u64| 3.0 + (lcg(state) - 0.5) * 1.4;
    for k in 0..count {
        let (x0, y0) = (coordinate(state), coordinate(state));
        cert.exact_points.push(ExactPoint {
            x: of_f64(x0),
            y: of_f64(y0),
            mass: mass.clone(),
        });
        cert.points.push(Point {
            x: x0,
            y: y0,
            mass: mass_iv,
        });
        let (mut x1, mut y1) = (coordinate(state), coordinate(state));
        match k % 3 {
            0 => y1 = y0,
            1 => x1 = x0,
            _ => {}
        }
        if x1 == x0 && y1 == y0 {
            x1 += 0.25;
        }
        cert.exact_segments.push(ExactSegment {
            p0: (of_f64(x0), of_f64(y0)),
            p1: (of_f64(x1), of_f64(y1)),
            mass: mass.clone(),
        });
        cert.segments.push(Segment {
            x0,
            y0,
            x1,
            y1,
            mass: mass_iv,
        });
    }
    cert
}

/// Lemmas B1 to B3: the box bound on points and segments is at most their
/// exact capture at every sampled centre of the box; the centre bound and the
/// candidate estimate bracket the exact capture at the centre.
#[test]
fn atom_bounds_hold_at_every_sampled_centre() {
    let mut state = 17u64;
    let cert = atom_cert(&mut state, 60);
    let mut positive = 0;
    for index in [0u32, 1, 100, 200] {
        let fr = frame(&cert, index).unwrap();
        let (c, s) = direction(&cert.step, index);
        let all_points: Vec<u32> = (0..60).collect();
        let lists = Straddling {
            points: &cert.points,
            point_ids: &all_points,
            segments: &cert.segments,
            segment_ids: &all_points,
        };
        for _ in 0..40 {
            let x0 = 3.0 + (lcg(&mut state) - 0.5) * 0.4;
            let y0 = 3.0 + (lcg(&mut state) - 0.5) * 0.4;
            let dx = 10f64.powf(-1.0 - 3.0 * lcg(&mut state));
            let dy = 10f64.powf(-1.0 - 3.0 * lcg(&mut state));
            let g = box_geom(&fr, x0, y0, dx, dy);
            let bound = atoms_dn(&fr, &g, &cert.points, &cert.segments);
            if bound > 0.0 {
                positive += 1;
            }
            for (u, v) in [
                (-1.0, -1.0),
                (1.0, -1.0),
                (-1.0, 1.0),
                (1.0, 1.0),
                (0.4, -0.9),
            ] {
                let px = of_f64(x0) + of_f64(u) * of_f64(dx);
                let py = of_f64(y0) + of_f64(v) * of_f64(dy);
                let exact = coverage(&cert, &px, &py, &c, &s);
                assert!(
                    of_f64(bound) <= exact,
                    "r={index}: box bound {bound} above exact {}",
                    exact.to_f64().unwrap()
                );
            }
            let exact = coverage(&cert, &of_f64(x0), &of_f64(y0), &c, &s);
            let lower = lists.centre_dn(&fr, &g);
            let upper = lists.centre_estimate_up(&fr, &g);
            assert!(
                of_f64(lower) <= exact,
                "r={index}: centre bound {lower} above exact"
            );
            assert!(
                exact <= of_f64(upper),
                "r={index}: estimate {upper} below exact"
            );
            assert!(
                exact.to_f64().unwrap() - lower < 1e-6,
                "r={index}: centre bound {lower} loose against {}",
                exact.to_f64().unwrap()
            );
        }
    }
    assert!(
        positive > 100,
        "only {positive} boxes captured any atom mass"
    );
}

/// The oracle counts closed intersections (spec 1.2): a point on the square's
/// edge, and a segment along it, count in full; a segment touching a corner
/// counts nothing.
#[test]
fn oracle_counts_closed_intersections() {
    let mut cert = test_cert(Vec::new());
    let h = &cert.core / ratio(2, 1);
    let (cx, cy) = (ratio(3, 1), ratio(3, 1));
    cert.exact_points.push(ExactPoint {
        x: &cx + &h,
        y: cy.clone(),
        mass: ratio(1, 5),
    });
    cert.exact_segments.push(ExactSegment {
        p0: (&cx - ratio(1, 10), &cy + &h),
        p1: (&cx + ratio(1, 10), &cy + &h),
        mass: ratio(1, 7),
    });
    cert.exact_segments.push(ExactSegment {
        p0: (&cx + &h, &cy + &h),
        p1: (&cx + &h + ratio(1, 2), &cy + &h + ratio(1, 2)),
        mass: ratio(1, 11),
    });
    cert.exact_segments.push(ExactSegment {
        p0: (cx.clone(), cy.clone()),
        p1: (&cx + &h * ratio(2, 1), cy.clone()),
        mass: ratio(1, 13),
    });
    let (c, s) = direction(&cert.step, 0);
    let exact = coverage(&cert, &cx, &cy, &c, &s);
    assert_eq!(exact, ratio(1, 5) + ratio(1, 7) + ratio(1, 26));
}
