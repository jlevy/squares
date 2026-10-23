//! Adversarial soundness tests from the 3 October soundness review
//! (`docs/project/reviews/review-2026-10-03-sqverify-fast-soundness.md`).
//!
//! Each test builds a certificate or a box aimed at one suspected weakness and
//! compares the verifier's certified bounds with the exact rational oracle. A
//! test marked `ignore` reproduces an open defect: it fails on the reviewed
//! build and should pass, un-ignored, once the defect is fixed.

use num_bigint::BigInt;
use num_rational::BigRational;
use serde_json::{Value, json};
use sqverify_fast::certificate::{Certificate, admit, direction, domain_upper};
use sqverify_fast::exact::{of_f64, parse_rational};
use sqverify_fast::oracle::coverage;
use sqverify_fast::rotated::{Limits, box_lower_bound, centre_lower_bound};

fn ratio(p: i64, q: i64) -> BigRational {
    BigRational::new(BigInt::from(p), BigInt::from(q))
}

fn text(q: &BigRational) -> String {
    format!("{}/{}", q.numer(), q.denom())
}

fn admit_value(value: &Value, n: u64) -> Result<Certificate, String> {
    let raw = value.to_string().into_bytes();
    admit(&raw, value, n, None).map_err(|error| error.0)
}

const LIMITS: Limits = Limits {
    max_nodes: 2_000_000,
    max_depth: 60,
    audit_every: 1024,
    inject_fault_at: None,
};

// ---------------------------------------------------------------- admission

#[test]
fn decimal_masses_are_exact_and_the_mass_premise_is_strict() {
    // 0.1 + 0.2 is 0.3 exactly, which binary64 would deny; total_mass is checked
    // against the exact sum.
    let base = |weights: Value, total: &str| {
        json!({"n": 1, "L": "3", "B": "9/10", "total_mass": total,
            "rectangles": [{"rectangle": [0, 0, 1, 1], "mass": weights[0]},
                           {"rectangle": [1, 1, 2, 2], "mass": weights[1]}],
            "points": []})
    };
    assert!(admit_value(&base(json!([0.1, 0.2]), "0.3"), 1).is_ok());
    assert!(admit_value(&base(json!([0.1, 0.2]), "0.30000000000000004"), 1).is_err());
    // A mass equal to n, written as decimals that sum to it exactly, is refused;
    // one part in 10^40 below it is admitted.
    let at_n = base(
        json!(["0.9999999999999999999999999999999999999999", "1e-40"]),
        "1",
    );
    assert!(admit_value(&at_n, 1).is_err());
    let below = base(
        json!(["0.9999999999999999999999999999999999999998", "1e-40"]),
        "0.9999999999999999999999999999999999999999",
    );
    assert!(admit_value(&below, 1).is_ok());
}

#[test]
fn admission_refuses_each_broken_premise() {
    let good = json!({"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1]], "weights": [1]});
    assert!(admit_value(&good, 2).is_ok());
    let variants = [
        // B (1 + D) = 1 exactly
        json!({"L": "3", "B": "40000/40083", "rectangles": [[0, 0, 1, 1]], "weights": [1]}),
        // a negative weight balanced by a positive one
        json!({"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1], [1, 1, 2, 2]], "weights": [2, -1]}),
        // a rectangle poking out of the container by 10^-30
        json!({"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, "3.000000000000000000000000000001"]], "weights": [1]}),
        // a degenerate rectangle
        json!({"L": "3", "B": "9/10", "rectangles": [[1, 0, 1, 1]], "weights": [1]}),
        // a net that stops one step short of pi/4 (t_199 < tan(pi/8))
        json!({"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1]], "weights": [1],
               "certificate": {"angle_count": 200}}),
        // metadata that disagrees with the candidate's side
        json!({"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1]], "weights": [1],
               "certificate": {"L": "3.0000000000000000001"}}),
        // format L with a different net
        json!({"schema": "point_line_rectangle_v1", "L": "3", "B": "9/10",
               "net": {"step": "83/40001", "last": 200},
               "primitives": [{"kind": "point", "geometry": [1, 1], "mass": 1}]}),
        // format L, a segment of length zero
        json!({"schema": "point_line_rectangle_v1", "L": "3", "B": "9/10",
               "net": {"step": "83/40000", "last": 200},
               "primitives": [{"kind": "segment", "geometry": [1, 1, 1, 1], "mass": 1}]}),
    ];
    for (index, variant) in variants.iter().enumerate() {
        assert!(
            admit_value(variant, 2).is_err(),
            "variant {index} was admitted"
        );
    }
}

#[test]
fn duplicate_keys_are_refused_before_any_reader_disagrees() {
    let dir = std::env::temp_dir().join(format!("sqverify-adv-{}", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let path = dir.join("dup.json");
    std::fs::write(
        &path,
        r#"{"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1]], "weights": [1], "weights": [0.5]}"#,
    )
    .unwrap();
    assert!(sqverify_fast::certificate::read_json(&path).is_err());
    std::fs::remove_dir_all(&dir).unwrap();
}

// ------------------------------------------------- boxes at the F2 extremes

/// A format L certificate at side 1000 (the largest admitted, where lemma F2's
/// slack is tightest) whose rectangles, points and segments sit exactly on the
/// boundary of the square at `(x0, y0)` and direction `index`: the square's
/// axis-aligned bounding box, a sliver along each square edge, every vertex as
/// a point, and every square edge as a segment.
fn boundary_cert(index: u32, x0: f64, y0: f64) -> Certificate {
    let side = ratio(1000, 1);
    let core = ratio(9977, 10000);
    let (c, s) = direction(&ratio(83, 40000), index);
    let corners = sqverify_fast::oracle::square(&of_f64(x0), &of_f64(y0), &c, &s, &core);
    let xs: Vec<&BigRational> = corners.iter().map(|p| &p.0).collect();
    let ys: Vec<&BigRational> = corners.iter().map(|p| &p.1).collect();
    let (left, right) = (
        (*xs.iter().min().expect("four corners")).clone(),
        (*xs.iter().max().expect("four corners")).clone(),
    );
    let (bottom, top) = (
        (*ys.iter().min().expect("four corners")).clone(),
        (*ys.iter().max().expect("four corners")).clone(),
    );
    let eps = ratio(1, 1_000_000_000_000);
    let mut primitives = vec![
        json!({"kind": "rectangle", "geometry": [text(&left), text(&bottom), text(&right), text(&top)], "mass": "1"}),
        // slivers of width 10^-12 hugging each side of the bounding box from inside
        json!({"kind": "rectangle", "geometry": [text(&left), text(&bottom), text(&(&left + &eps)), text(&top)], "mass": "1"}),
        json!({"kind": "rectangle", "geometry": [text(&(&right - &eps)), text(&bottom), text(&right), text(&top)], "mass": "1"}),
        json!({"kind": "rectangle", "geometry": [text(&left), text(&(&top - &eps)), text(&right), text(&top)], "mass": "1"}),
    ];
    for (k, p) in corners.iter().enumerate() {
        let q = &corners[(k + 1) % 4];
        primitives
            .push(json!({"kind": "point", "geometry": [text(&p.0), text(&p.1)], "mass": "1"}));
        primitives.push(json!({"kind": "segment", "geometry": [text(&p.0), text(&p.1), text(&q.0), text(&q.1)], "mass": "1"}));
        // a segment from the vertex straight outward, touching the square at one point
        let out = (&p.0 + (&p.0 - of_f64(x0)), &p.1 + (&p.1 - of_f64(y0)));
        primitives.push(json!({"kind": "segment", "geometry": [text(&p.0), text(&p.1), text(&out.0), text(&out.1)], "mass": "1"}));
    }
    let value = json!({"schema": "point_line_rectangle_v1", "L": text(&side), "B": text(&core),
        "net": {"step": "83/40000", "last": 200}, "primitives": primitives});
    admit_value(&value, 1_000_000).expect("boundary certificate is admissible")
}

#[test]
fn box_bounds_never_exceed_exact_capture_on_boundary_configurations() {
    let mut checked = 0;
    for index in [0u32, 1, 57, 133, 200] {
        let cert = boundary_cert(index, 700.123_456_789, 811.987_654_321);
        let (c, s) = direction(&cert.step, index);
        for &(x0, y0) in &[
            (700.123_456_789, 811.987_654_321),
            (700.123_456_789 + 3e-10, 811.987_654_321),
        ] {
            let centre = centre_lower_bound(&cert, index, x0, y0).unwrap();
            let exact = coverage(&cert, &of_f64(x0), &of_f64(y0), &c, &s);
            assert!(
                of_f64(centre) <= exact,
                "r={index} centre {centre} > {exact}"
            );
            for &d in &[0.0, 1e-12, 1e-9, 1e-6, 1e-3, 0.25] {
                for &(dx, dy) in &[(d, d), (d, 0.0), (0.0, d), (d, 2.0 * d)] {
                    let bound = box_lower_bound(&cert, index, x0, y0, dx, dy).unwrap();
                    for (sx, sy) in [
                        (-1.0, -1.0),
                        (1.0, -1.0),
                        (-1.0, 1.0),
                        (1.0, 1.0),
                        (0.0, 0.0),
                        (0.37, -0.81),
                    ] {
                        let (px, py) = (x0 + sx * dx, y0 + sy * dy);
                        // Only poses inside the box the bound speaks for.
                        if (px - x0).abs() > dx || (py - y0).abs() > dy {
                            continue;
                        }
                        let truth = coverage(&cert, &of_f64(px), &of_f64(py), &c, &s);
                        assert!(
                            of_f64(bound) <= truth,
                            "r={index} box ({x0},{y0})+-({dx},{dy}) bound {bound} above exact at ({px},{py})"
                        );
                        checked += 1;
                    }
                }
            }
        }
    }
    assert!(checked > 500);
}

// ------------------------------------------------------- the domain premise

#[test]
fn per_bin_domain_needs_the_fold_at_pi_over_four() {
    // Lemma D's per-bin domain is the least half-width over [a_r, tan(pi/8)];
    // at r = 200 the bin [t - D/2, t + D/2] reaches past tan(pi/8), where the
    // half-width rho falls again. A unit square at half-angle t_200 + D/2 has a
    // half-width below rho(a_200): the domain is valid only because orientations
    // above pi/4 are folded by the diagonal (spec N5), not merely those above
    // theta_max (SOUNDNESS.md step N2).
    let rho = |a: &BigRational| {
        let one = ratio(1, 1);
        let two = ratio(2, 1);
        (&one + &two * a - a * a) / (&two * (&one + a * a))
    };
    let d = ratio(83, 40000);
    let t = &d * ratio(200, 1);
    let a = &t - &d / ratio(2, 1);
    let far = &t + &d / ratio(2, 1);
    assert!(rho(&far) < rho(&a));
    let value = json!({"n": 3, "L": "3", "B": "9/10", "points": [],
        "rectangles": [{"rectangle": [0, 0, 1, 1], "mass": 1}]});
    let cert = admit_value(&value, 3).unwrap();
    assert_eq!(domain_upper(&cert, 200).unwrap(), ratio(3, 1) - rho(&a));
}

// ------------------------------------------------- non-finite intermediates

/// The certificate of finding S1, as JSON: a band of density 2 that every
/// centre on the domain's lower edge captures in full, plus twenty slivers of
/// height 2^-1000 ending at ordinate `top` whose summed slope steps overflow in
/// the axis sweep, with weight `weight` each. At `(3.5, 3.5)`, inside the r = 0
/// domain `[2, 3.55]^2`, the exact capture is zero.
fn overflow_value(top: &BigRational, weight: &str) -> Value {
    let den = BigInt::from(1) << 1000usize;
    let y1 = top - BigRational::new(BigInt::from(1), den);
    let mut rects = vec![json!(["0", "3/2", "4", "5/2"])];
    let mut weights = vec![json!("16")];
    for k in 0..20 {
        rects.push(json!([
            text(&ratio(k, 1000)),
            text(&y1),
            text(&(ratio(4, 1) - ratio(k, 1000))),
            text(top)
        ]));
        weights.push(json!(weight));
    }
    json!({"L": "4", "B": "9/10", "rectangles": rects, "weights": weights})
}

/// The S1 certificate past admission. Lemma F3's density cap refuses it, so it
/// is admitted with tiny sliver weights and the slivers' densities are then
/// raised to about 1.5e307 in place: the sweep itself meets the overflow.
fn overflow_cert(top: &BigRational) -> Certificate {
    let light = overflow_value(top, &format!("1/{}", BigInt::from(1) << 950usize));
    let mut cert = admit_value(&light, 1_000_000_000).expect("the light version is admissible");
    let huge = ratio(15, 1) * BigRational::from_integer(BigInt::from(10).pow(306));
    for (exact, rect) in cert.exact.iter_mut().zip(cert.rects.iter_mut()) {
        if &exact.y2 - &exact.y1 < ratio(1, 1_000_000) {
            exact.density = huge.clone();
            rect.rho = sqverify_fast::interval::Iv::point(1.5e307);
        }
    }
    cert
}

#[test]
fn admission_refuses_the_overflow_densities() {
    // Lemma F3's cap: the slivers' densities, about 1.5e307, exceed 2^96.
    let value = overflow_value(&ratio(49, 20), "22000000");
    let error = admit_value(&value, 1_000_000_000).expect_err("the S1 certificate was admitted");
    assert!(error.contains("density"), "{error}");
}

#[test]
fn overflow_certificate_has_an_uncovered_centre() {
    // The witness half of S1: a centre of the r = 0 domain captures nothing.
    let cert = overflow_cert(&ratio(49, 20));
    assert!(domain_upper(&cert, 0).unwrap() >= ratio(71, 20));
    let exact = coverage(
        &cert,
        &ratio(7, 2),
        &ratio(7, 2),
        &ratio(1, 1),
        &ratio(0, 1),
    );
    assert_eq!(exact, ratio(0, 1));
}

#[test]
fn axis_sweep_refuses_the_overflow_certificate() {
    // The slivers' steps lie just below the domain: the overflow is in the
    // initial slope.
    let cert = overflow_cert(&ratio(49, 20));
    let threshold = parse_rational("1").unwrap();
    let report = sqverify_fast::run_direction(&cert, 0, &threshold, LIMITS, false).unwrap();
    assert!(!report.verified, "direction 0 verified: {}", report.receipt);
    assert_eq!(
        report.receipt["verdict"], "non-finite",
        "{}",
        report.receipt
    );
}

#[test]
fn axis_sweep_refuses_an_overflow_inside_the_domain() {
    // The second reproducer: slivers ending at ordinate 3 put their steps at
    // about 2.55, inside the domain [2, 3.55], so the overflow arises in a
    // column's step list rather than its initial slope.
    let cert = overflow_cert(&ratio(3, 1));
    let threshold = parse_rational("1").unwrap();
    let report = sqverify_fast::run_direction(&cert, 0, &threshold, LIMITS, false).unwrap();
    assert!(!report.verified, "direction 0 verified: {}", report.receipt);
    assert_eq!(
        report.receipt["verdict"], "non-finite",
        "{}",
        report.receipt
    );
}

#[test]
fn a_fault_injected_run_is_never_verified() {
    // Finding S2: with the audit sampled too sparsely to see it, an injected
    // fault must still not yield a verified receipt, and the receipt names it.
    let value = json!({"L": "3", "B": "9/10",
        "rectangles": [[0, 0, 3, 3]], "weights": [8]});
    let cert = admit_value(&value, 9).unwrap();
    let threshold = parse_rational("1/2").unwrap();
    let limits = Limits {
        audit_every: 1 << 40,
        inject_fault_at: Some(2),
        ..LIMITS
    };
    for index in [0u32, 1, 100] {
        let report = sqverify_fast::run_direction(&cert, index, &threshold, limits, false).unwrap();
        assert!(!report.verified, "r={index}: {}", report.receipt);
        assert_eq!(
            report.receipt["fault_injected_at_box"], 2,
            "{}",
            report.receipt
        );
        let clean = sqverify_fast::run_direction(&cert, index, &threshold, LIMITS, false).unwrap();
        assert!(
            clean.verified,
            "r={index} clean run refused: {}",
            clean.receipt
        );
    }
}

// ------------------------------------- findings of the 3 October testing review

/// Writes `bytes` to a fresh temporary file and reads it as a candidate.
fn read_bytes(name: &str, bytes: &[u8]) -> Result<(), String> {
    let dir = std::env::temp_dir().join(format!("sqverify-rb-{}-{name}", std::process::id()));
    std::fs::create_dir_all(&dir).expect("a temporary directory");
    let path = dir.join("candidate.json.gz");
    std::fs::write(&path, bytes).expect("a temporary file");
    let result = sqverify_fast::certificate::read_json(&path)
        .map(|_| ())
        .map_err(|error| error.0);
    std::fs::remove_dir_all(&dir).expect("the temporary directory removed");
    result
}

fn gzip(bytes: &[u8]) -> Vec<u8> {
    use std::io::Write;
    let mut encoder = flate2::write::GzEncoder::new(Vec::new(), flate2::Compression::default());
    encoder.write_all(bytes).expect("gzip in memory");
    encoder.finish().expect("gzip in memory")
}

#[test]
fn gzip_input_must_be_one_member_and_nothing_else() {
    // Finding TI-2: Python's reader refuses a second member or trailing bytes, so
    // this reader must too, or the two would see different inputs.
    let json = br#"{"L": "3", "B": "9/10", "rectangles": [[0, 0, 1, 1]], "weights": [1]}"#;
    let one = gzip(json);
    assert!(read_bytes("one", &one).is_ok());
    let mut two = one.clone();
    two.extend(gzip(json));
    assert!(
        read_bytes("two", &two)
            .unwrap_err()
            .contains("after its first member")
    );
    let mut trailing = one.clone();
    trailing.extend(b"garbage");
    assert!(
        read_bytes("trailing", &trailing)
            .unwrap_err()
            .contains("after its first member")
    );
}

#[test]
fn format_l_and_m_nets_cannot_be_overridden() {
    // Finding TI-3: certificate metadata may restate the fixed net, never change it.
    let linear = |metadata: Value| {
        json!({"schema": "point_line_rectangle_v1", "L": "3", "B": "1/2",
            "net": {"step": "83/40000", "last": 200},
            "primitives": [{"kind": "point", "geometry": [1, 1], "mass": 1}],
            "certificate": metadata})
    };
    let error = admit_value(&linear(json!({"D": "9/20", "angle_count": 3})), 2).unwrap_err();
    assert!(error.contains("net"), "{error}");
    assert!(admit_value(&linear(json!({"D": "83/40000", "angle_count": 201})), 2).is_ok());
    let mixed = json!({"n": 2, "L": "3", "B": "1/2", "points": [],
        "rectangles": [{"rectangle": [0, 0, 1, 1], "mass": 1}],
        "certificate": {"angle_count": 150}});
    assert!(admit_value(&mixed, 2).is_err());
}

fn declared_net(b: &str, net: &Value) -> Value {
    json!({"n": 2, "L": "3", "B": b, "points": [], "proof_net": net,
        "rectangles": [{"rectangle": [0, 0, 1, 1], "mass": 1}]})
}

#[test]
fn a_format_m_candidate_may_declare_a_finer_uniform_net() {
    // B = 999/1000 with step 1/1001 and 416 directions, as in the fine-net
    // rectangle certificates; the per-bin domain follows the declared step.
    let cert = admit_value(
        &declared_net("999/1000", &json!({"step": "1/1001", "last": 415})),
        2,
    )
    .unwrap();
    assert_eq!(cert.step, ratio(1, 1001));
    assert_eq!(cert.angle_count, 416);
    let one = ratio(1, 1);
    let a = ratio(415, 1001) - ratio(1, 2002);
    let rho = (&one + ratio(2, 1) * &a - &a * &a) / (ratio(2, 1) * (&one + &a * &a));
    assert_eq!(domain_upper(&cert, 415).unwrap(), ratio(3, 1) - rho);
}

#[test]
fn a_declared_net_must_pass_every_net_premise() {
    let refused = |b: &str, net: Value| admit_value(&declared_net(b, &net), 2).unwrap_err();
    // B (1 + D) >= 1.
    let error = refused("9995/10000", json!({"step": "1/1001", "last": 415}));
    assert!(error.contains("B (1 + D)"), "{error}");
    // (1 + 413/1001)^2 < 2: the net stops short of pi/4.
    let error = refused("999/1000", json!({"step": "1/1001", "last": 413}));
    assert!(error.contains("pi/4"), "{error}");
    // last * step > 1/2 (lemma F3).
    let error = refused("1/2", json!({"step": "1/10", "last": 6}));
    assert!(error.contains("F3"), "{error}");
    // Exactly the two fields, a nonnegative integer last.
    for net in [
        json!({"step": "1/1001"}),
        json!({"step": "1/1001", "last": 415, "count": 416}),
        json!({"step": "1/1001", "last": -1}),
        json!({"step": "1/1001", "last": "415"}),
        json!([1, 415]),
    ] {
        assert!(admit_value(&declared_net("999/1000", &net), 2).is_err());
    }
    // Metadata still may not touch a net, declared or not (finding TI-3).
    let mut both = declared_net("999/1000", &json!({"step": "1/1001", "last": 415}));
    both["certificate"] = json!({"D": "1/1001", "angle_count": 416});
    assert!(admit_value(&both, 2).is_err());
    // Only format M reads proof_net.
    let tokoharu = json!({"L": "3", "B": "999/1000", "rectangles": [[0, 0, 1, 1]],
        "weights": [1], "proof_net": {"step": "1/1001", "last": 415}});
    let error = admit_value(&tokoharu, 2).unwrap_err();
    assert!(error.contains("proof_net"), "{error}");
}

#[test]
fn the_per_bin_domain_checks_the_tangent_form_of_the_shrink_premise() {
    // The testing review's question: with bins of half-width D/2 in t, the angle
    // may differ from theta_r by 2 atan(D/2), whose tangent is D/(1 - D^2/4).
    // Admission checks B (1 + D/(1 - D^2/4)) < 1 for format M. The two limits on
    // B are about 0.99792929449 and 0.99792929671; a B between them passes
    // B (1 + D) < 1 and must still be refused for format M, and admitted for T.
    let d = ratio(83, 40000);
    let one = ratio(1, 1);
    let between = ratio(997_929_295, 1_000_000_000);
    assert!(&between * (&one + &d) < one);
    assert!(&between * (&one + &d / (&one - &d * &d / ratio(4, 1))) >= one);
    let b = text(&between);
    let mixed = json!({"n": 2, "L": "3", "B": b, "points": [],
        "rectangles": [{"rectangle": [0, 0, 1, 1], "mass": 1}]});
    let error = admit_value(&mixed, 2).unwrap_err();
    assert!(error.contains("per-bin"), "{error}");
    let tokoharu = json!({"L": "3", "B": b, "rectangles": [[0, 0, 1, 1]], "weights": [1]});
    assert!(admit_value(&tokoharu, 2).is_ok());
    // The retained certificates' B = 9977/10000 clears both forms exactly.
    let retained = ratio(9977, 10000);
    assert!(&retained * (&one + &d / (&one - &d * &d / ratio(4, 1))) < one);
}

// ------------------------------------------- re-review of 3 October, evening

/// Limits for the re-review's searches: small, since only the verdict's kind
/// matters, never the time to reach it.
const SMALL: Limits = Limits {
    max_nodes: 20_000,
    max_depth: 40,
    audit_every: 1,
    inject_fault_at: None,
};

#[test]
fn overflow_in_the_rotated_search_is_never_verified() {
    // S1's raised densities in the branch and bound (r = 1, 100, 200) and in its
    // direction-zero branch (a point mass forces it): each must refuse, and any
    // non-finite value must stop the search rather than drop out.
    let threshold = parse_rational("1").unwrap();
    let cert = overflow_cert(&ratio(49, 20));
    for index in [1u32, 100, 200] {
        let report = sqverify_fast::run_direction(&cert, index, &threshold, SMALL, false).unwrap();
        assert!(!report.verified, "r={index} verified: {}", report.receipt);
    }
    let mut with_point = cert;
    with_point.points.push(sqverify_fast::certificate::Point {
        x: 0.5,
        y: 0.5,
        mass: sqverify_fast::interval::Iv::point(1e-9),
    });
    let report = sqverify_fast::run_direction(&with_point, 0, &threshold, SMALL, false).unwrap();
    assert!(
        !report.verified,
        "r=0 (branch and bound) verified: {}",
        report.receipt
    );
}

/// The S1 shape with every sliver at just under lemma F3's density cap and of
/// height 2^-60, below a unit in the last place of its ordinate: the steps of
/// about 2^96 meet event widths that straddle zero.
fn capped_overflow_value() -> Value {
    let y2 = ratio(49, 20);
    let y1 = &y2 - BigRational::new(BigInt::from(1), BigInt::from(1) << 60usize);
    let mut rects = vec![json!(["0", "3/2", "4", "5/2"])];
    let mut weights = vec![json!("16")];
    for k in 0..20 {
        rects.push(json!([
            text(&ratio(k, 1000)),
            text(&y1),
            text(&(ratio(4, 1) - ratio(k, 1000))),
            text(&y2)
        ]));
        // 0.99 * 2^40: the merged density w / (4 area) stays below 2^96.
        weights.push(json!("1088516511498"));
    }
    json!({"L": "4", "B": "9/10", "rectangles": rects, "weights": weights})
}

#[test]
fn the_s1_shape_at_the_density_cap_is_refused_and_finite() {
    let cert = admit_value(&capped_overflow_value(), 1_000_000_000_000_000)
        .expect("densities at the cap are admissible");
    let exact = coverage(
        &cert,
        &ratio(7, 2),
        &ratio(7, 2),
        &ratio(1, 1),
        &ratio(0, 1),
    );
    assert_eq!(exact, ratio(0, 1));
    let threshold = parse_rational("1").unwrap();
    for index in [0u32, 1, 200] {
        let report = sqverify_fast::run_direction(&cert, index, &threshold, SMALL, false).unwrap();
        assert!(!report.verified, "r={index} verified: {}", report.receipt);
        // Lemma F3: an admitted certificate never produces a non-finite value.
        assert_ne!(
            report.receipt["verdict"], "non-finite",
            "r={index}: {}",
            report.receipt
        );
    }
}

#[test]
fn lemma_f3_holds_at_its_extremes() {
    // Side 1000, the finest net the caps admit (2^16 directions, so the smallest
    // step and the smallest s_1), and rectangles at the density cap: every
    // searched direction must end without a non-finite value.
    let side = 1000;
    let mut rects = Vec::new();
    let mut weights = Vec::new();
    for k in 0..8 {
        // [500 + k, 500 + k + 1/2] x [600, 600 + 2^-40]: area 2^-41, density
        // w / (8 area) = 2^96 at w = 2^58.
        let y2 = ratio(600, 1) + BigRational::new(BigInt::from(1), BigInt::from(1) << 40usize);
        rects.push(json!([
            text(&ratio(1000 + 2 * k, 2)),
            "600",
            text(&ratio(1001 + 2 * k, 2)),
            text(&y2)
        ]));
        weights.push(json!((1u64 << 58).to_string()));
    }
    // t_max = (N - 1) D just past tan(pi/8) with N = 2^16: the smallest D.
    let count = 1u32 << 16;
    let step = BigRational::new(
        BigInt::from(41_422),
        BigInt::from(100_000u64 * u64::from(count - 1)),
    );
    let value = json!({"L": side.to_string(), "B": "9/10", "rectangles": rects, "weights": weights,
        "certificate": {"D": text(&step), "angle_count": count}});
    let cert = admit_value(&value, u64::MAX).expect("the extreme certificate is admissible");
    let threshold = parse_rational("1").unwrap();
    for index in [0u32, 1, 2, count - 1] {
        let report = sqverify_fast::run_direction(&cert, index, &threshold, SMALL, false).unwrap();
        assert_ne!(
            report.receipt["verdict"], "non-finite",
            "r={index}: {}",
            report.receipt
        );
        assert!(!report.verified, "r={index} verified: {}", report.receipt);
    }
}

#[test]
fn fmin_and_fmax_are_exact_on_finite_operands_and_poison_on_failure() {
    use sqverify_fast::interval::{fmax, fmin};
    for (a, b) in [
        (1.0, 2.0),
        (2.0, 1.0),
        (-0.0, 0.0),
        (-3.5, -3.5),
        (1e300, -1e300),
    ] {
        assert_eq!(fmin(a, b), f64::min(a, b));
        assert_eq!(fmax(a, b), f64::max(a, b));
    }
    for bad in [f64::NAN, f64::INFINITY, f64::NEG_INFINITY] {
        assert!(fmin(bad, 1.0).is_nan() && fmax(bad, 1.0).is_nan());
    }
    assert!(fmin(1.0, f64::NAN).is_nan() && fmax(1.0, f64::NAN).is_nan());
    // An infinite second operand selects correctly; it cannot arise on the
    // certification path (lemma F3), and a wrong selection is not possible.
    assert_eq!(fmin(1.0, f64::INFINITY), 1.0);
    assert_eq!(fmax(1.0, f64::NEG_INFINITY), 1.0);
}
