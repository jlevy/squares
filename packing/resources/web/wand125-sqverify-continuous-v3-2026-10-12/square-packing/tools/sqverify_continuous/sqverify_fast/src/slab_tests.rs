//! Property tests of the continuous-angle bounds against the exact oracle.

use super::*;
use crate::certificate::{Domain, ExactRect, float_rect};
use crate::oracle::{intersection_area, square};
use num_traits::Signed;

fn lcg(state: &mut u64) -> f64 {
    *state = state
        .wrapping_mul(6_364_136_223_846_793_005)
        .wrapping_add(1_442_695_040_888_963_407);
    (*state >> 11) as f64 / (1u64 << 53) as f64
}

fn cert_of(rects: Vec<ExactRect>, side: BigRational, core: BigRational) -> Certificate {
    let floats = rects
        .iter()
        .map(|r| {
            let mass = &r.density * (&r.x2 - &r.x1) * (&r.y2 - &r.y1);
            float_rect(r, &mass).unwrap()
        })
        .collect();
    Certificate {
        n: 100,
        side,
        core,
        step: q(83, 40000),
        angle_count: 201,
        mass: q(1, 1),
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
            let x = (lcg(state) * 5_000_000.0) as i64 + 500_000;
            let y = (lcg(state) * 5_000_000.0) as i64 + 500_000;
            let w = (lcg(state) * 1_200_000.0) as i64 + 1_000;
            let h = (lcg(state) * 1_200_000.0) as i64 + 1_000;
            ExactRect {
                x1: q(x, 1_000_000),
                y1: q(y, 1_000_000),
                x2: q((x + w).min(6_000_000), 1_000_000),
                y2: q((y + h).min(6_000_000), 1_000_000),
                density: q((lcg(state) * 1000.0) as i64 + 1, 1000),
            }
        })
        .collect()
}

struct Exact {
    c: BigRational,
    s: BigRational,
    e: BigRational,
}

fn exact_at(t: f64, side: &BigRational, core: &BigRational) -> Exact {
    let t = of_f64(t);
    let one = BigRational::one();
    let d = &one + &t * &t;
    let c = (&one - &t * &t) / &d;
    let s = (q(2, 1) * &t) / &d;
    let e = side / q(2, 1) - core / q(2, 1) * (&c + &s);
    Exact { c, s, e }
}

fn random_node(state: &mut u64, n_rects: usize) -> Node {
    let ta = 1e-6 + lcg(state) * 0.44;
    let tb = ta + lcg(state).powi(3) * 0.05;
    let ul = lcg(state) * 0.9;
    let uh = ul + lcg(state).powi(2) * 0.1;
    let vl = lcg(state) * 0.9;
    let vh = vl + lcg(state).powi(2) * 0.1;
    Node {
        ul,
        uh,
        vl,
        vh,
        ta,
        tb,
        depth: 0,
        base: 0.0,
        active: (0..n_rects as u32).collect(),
    }
}

fn lerp(a: f64, b: f64, w: f64) -> f64 {
    (a + (b - a) * w).clamp(a, b)
}

fn area(
    r: &ExactRect,
    x: &BigRational,
    y: &BigRational,
    ex: &Exact,
    core: &BigRational,
) -> BigRational {
    intersection_area(r, &square(x, y, &ex.c, &ex.s, core))
}

#[test]
fn angle_enclosures_contain_exact_values() {
    let mut st = 7;
    for _ in 0..2000 {
        let ta = lcg(&mut st) * 0.5;
        let tb = (ta + lcg(&mut st).powi(2) * 0.2).min(0.5);
        let an = angles(ta, tb);
        for w in [0.0, 0.3, 0.5, 0.9, 1.0] {
            let ex = exact_at(lerp(ta, tb, w), &q(0, 1), &q(0, 1));
            let wv = &ex.c + &ex.s;
            for (v, iv) in [(&ex.c, an.c), (&ex.s, an.s), (&wv, an.w)] {
                assert!(
                    of_f64(iv.lo) <= *v && *v <= of_f64(iv.hi),
                    "t in [{ta}, {tb}]"
                );
            }
        }
    }
}

/// Area, classification, gradient and the whole box bound, at sampled poses.
#[test]
fn box_bounds_hold_at_sampled_poses() {
    let side = q(6, 1);
    let core = q(199_529, 200_000);
    let mut st = 11;
    let mut checked = 0;
    for round in 0..60 {
        let rects = random_rects(&mut st, 40);
        let cert = cert_of(rects, side.clone(), core.clone());
        let half_l = enclose(&(&side / q(2, 1))).unwrap();
        let h = enclose(&(&core / q(2, 1))).unwrap();
        let n = random_node(&mut st, cert.rects.len());
        let p = pose(&n, half_l, h).unwrap();
        let mut knots = Vec::new();
        let u0 = f64::midpoint(n.ul, n.uh);
        let v0 = f64::midpoint(n.vl, n.vh);
        let mut base = 0.0;
        let mut active = Vec::new();
        let mut classes = Vec::new();
        for (i, r) in cert.rects.iter().enumerate() {
            let k = classify(&p, r);
            classes.push(k);
            match k {
                Class::Inside => base = add_dn(base, r.mass.lo),
                Class::Outside => {}
                Class::Boundary => active.push(i as u32),
            }
        }
        let ctx = Ctx {
            cert: &cert,
            half_l,
            h,
            thr: 0.0,
            max_nodes: 1,
        };
        let (f, lx, ly) = bound(&ctx, &p, &active, &mut knots);
        let lower = sub_dn(sub_dn(add_dn(base, f), lx), ly);
        for _ in 0..6 {
            let t = lerp(n.ta, n.tb, lcg(&mut st));
            let ex = exact_at(t, &side, &core);
            let l2 = &side / q(2, 1);
            let xm = &l2 + of_f64(u0) * &ex.e;
            let ym = &l2 + of_f64(v0) * &ex.e;
            let x = &l2 + of_f64(lerp(n.ul, n.uh, lcg(&mut st))) * &ex.e;
            let y = &l2 + of_f64(lerp(n.vl, n.vh, lcg(&mut st))) * &ex.e;
            assert!(of_f64(p.x.lo) <= x && x <= of_f64(p.x.hi));
            assert!(of_f64(p.xm.lo) <= xm && xm <= of_f64(p.xm.hi));
            assert!((&x - &xm).abs() <= of_f64(p.dx) && (&y - &ym).abs() <= of_f64(p.dy));
            let mut total = BigRational::zero();
            for (i, r) in cert.exact.iter().enumerate() {
                let fr = &cert.rects[i];
                let a = area(r, &x, &y, &ex, &core);
                let full = (&r.x2 - &r.x1) * (&r.y2 - &r.y1);
                match classes[i] {
                    Class::Inside => assert_eq!(a, full, "round {round} rect {i} inside"),
                    Class::Outside => assert!(a.is_zero(), "round {round} rect {i} outside"),
                    Class::Boundary => {
                        let am = area(r, &xm, &ym, &ex, &core);
                        assert!(
                            of_f64(area_lo(&p, fr, &mut knots)) <= am,
                            "area round {round}"
                        );
                        // difference quotient along x inside the box
                        let x2 = &x + q(1, 1_000_000_000);
                        if x2 <= of_f64(p.x.hi) {
                            let dq = (area(r, &x2, &y, &ex, &core) - &a)
                                * q(1_000_000_000, 1)
                                * &r.density;
                            let (gx, _) = gradient(&p, fr);
                            assert!(
                                of_f64(gx.lo) <= dq && dq <= of_f64(gx.hi),
                                "gradient round {round}"
                            );
                        }
                    }
                }
                total += a * &r.density;
            }
            assert!(of_f64(lower) <= total, "box bound round {round}");
            checked += 1;
        }
    }
    assert!(checked > 300);
}

/// Small rectangles straddling the square's edges, against small boxes, so that
/// a classification slack of one percent is visible.
#[test]
fn classification_near_the_edge() {
    let side = q(6, 1);
    let core = q(199_529, 200_000);
    let hf = 199_529.0 / 400_000.0;
    let half_l = enclose(&(&side / q(2, 1))).unwrap();
    let h = enclose(&(&core / q(2, 1))).unwrap();
    let mut st = 23;
    let (mut inside, mut outside) = (0, 0);
    for round in 0..200 {
        let mut n = random_node(&mut st, 0);
        n.uh = n.ul + 1e-6;
        n.vh = n.vl + 1e-6;
        n.tb = n.ta + 1e-7;
        let tm = f64::midpoint(n.ta, n.tb);
        let c = (1.0 - tm * tm) / (1.0 + tm * tm);
        let s = 2.0 * tm / (1.0 + tm * tm);
        let e = 3.0 - hf * (c + s);
        let (x0, y0) = (
            3.0 + f64::midpoint(n.ul, n.uh) * e,
            3.0 + f64::midpoint(n.vl, n.vh) * e,
        );
        let mut rects = Vec::new();
        for _ in 0..30 {
            let a = hf * (0.97 + 0.06 * lcg(&mut st)) * if lcg(&mut st) < 0.5 { -1.0 } else { 1.0 };
            let b = hf * 0.9 * (2.0 * lcg(&mut st) - 1.0);
            let (a, b) = if lcg(&mut st) < 0.5 { (a, b) } else { (b, a) };
            let px = x0 + c * a - s * b;
            let py = y0 + s * a + c * b;
            let x = (px * 1e7) as i64;
            let y = (py * 1e7) as i64;
            rects.push(ExactRect {
                x1: q(x, 10_000_000),
                y1: q(y, 10_000_000),
                x2: q(x + 30, 10_000_000),
                y2: q(y + 30, 10_000_000),
                density: q(1, 1),
            });
        }
        let cert = cert_of(rects, side.clone(), core.clone());
        let p = pose(&n, half_l, h).unwrap();
        for _ in 0..4 {
            let t = lerp(n.ta, n.tb, lcg(&mut st));
            let ex = exact_at(t, &side, &core);
            let l2 = &side / q(2, 1);
            let x = &l2 + of_f64(lerp(n.ul, n.uh, lcg(&mut st))) * &ex.e;
            let y = &l2 + of_f64(lerp(n.vl, n.vh, lcg(&mut st))) * &ex.e;
            for (i, r) in cert.exact.iter().enumerate() {
                let a = area(r, &x, &y, &ex, &core);
                match classify(&p, &cert.rects[i]) {
                    Class::Inside => {
                        inside += 1;
                        assert_eq!(a, (&r.x2 - &r.x1) * (&r.y2 - &r.y1), "round {round}");
                    }
                    Class::Outside => {
                        outside += 1;
                        assert!(a.is_zero(), "round {round}");
                    }
                    Class::Boundary => {}
                }
            }
        }
    }
    assert!(inside > 1000 && outside > 1000, "{inside} {outside}");
}
