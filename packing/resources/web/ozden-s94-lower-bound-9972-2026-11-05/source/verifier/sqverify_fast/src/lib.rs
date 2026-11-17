//! Clean-room verifier for measure-capture lower-bound certificates.
//!
//! A certificate is a nonnegative measure on `[0, L]^2` of total mass below
//! `n`. It proves `s(n) >= L` if every unit square in the container captures
//! mass at least one. The net-and-shrink argument reduces that to finitely
//! many directions, at each of which every centre of a shrunk square of side
//! `B` must capture the threshold. `SOUNDNESS.md` beside this crate states and
//! proves every lemma the code relies on; `INDEPENDENCE.md` records what was
//! read and run while writing it.

pub mod axis;
pub mod certificate;
pub mod exact;
pub mod interval;
pub mod oracle;
pub mod rotated;

use num_rational::BigRational;
use serde_json::{Value, json};

use crate::certificate::{Certificate, direction};
use crate::exact::of_f64;
use crate::rotated::{Limits, Verdict};

/// CPU time consumed so far by the calling thread, in seconds, from Linux's
/// `/proc/thread-self/schedstat` (nanoseconds on the CPU); `None` elsewhere.
#[must_use]
pub fn thread_cpu_seconds() -> Option<f64> {
    let text = std::fs::read_to_string("/proc/thread-self/schedstat").ok()?;
    let nanos: u64 = text.split_whitespace().next()?.parse().ok()?;
    Some(nanos as f64 * 1e-9)
}

/// The implementation's identity: a digest of the sources and lockfile it was
/// built from, and its build flags.
#[must_use]
pub fn build_identity() -> Value {
    json!({
        "source_sha256": env!("SQVERIFY_FAST_SOURCE_SHA256"),
        "profile": if cfg!(debug_assertions) { "debug" } else { "release" },
        "target": env!("SQVERIFY_FAST_TARGET"),
        "rustc": env!("SQVERIFY_FAST_RUSTC"),
    })
}

/// The receipt for one direction.
#[derive(Clone, Debug)]
pub struct DirectionReport {
    /// Net index.
    pub index: u32,
    /// Whether the direction is verified.
    pub verified: bool,
    /// Wall seconds.
    pub seconds: f64,
    /// The JSON receipt.
    pub receipt: Value,
}

/// Verify one direction and build its receipt.
///
/// `threshold` is exact; the search compares against the upper end of its
/// binary64 enclosure. With `confirm`, a counterexample candidate is
/// re-evaluated in exact rationals.
///
/// # Errors
///
/// Returns a message when a constant cannot be enclosed.
pub fn run_direction(
    cert: &Certificate,
    index: u32,
    threshold: &BigRational,
    limits: Limits,
    confirm: bool,
) -> Result<DirectionReport, String> {
    let threshold_hi = crate::exact::enclose(threshold)?.hi;
    let cpu_start = thread_cpu_seconds();
    let mut report = run_direction_inner(cert, index, threshold, threshold_hi, limits, confirm)?;
    // A fault-injection control is never evidence: its receipt says so, and it is
    // never reported verified, whatever the audit caught.
    if let Some(node) = limits.inject_fault_at {
        report.receipt["fault_injected_at_box"] = json!(node);
        if report.verified {
            report.verified = false;
            report.receipt["verdict"] = json!("fault-injected");
        }
    }
    if let (Some(start), Some(end)) = (cpu_start, thread_cpu_seconds()) {
        report.receipt["cpu_seconds"] = json!(end - start);
    }
    report.receipt["threshold"] = json!(threshold.to_string());
    Ok(report)
}

fn run_direction_inner(
    cert: &Certificate,
    index: u32,
    threshold: &BigRational,
    threshold_hi: f64,
    limits: Limits,
    confirm: bool,
) -> Result<DirectionReport, String> {
    // Lemma B5: the vertex sweep needs a measure of rectangles alone.
    if index == 0 && cert.points.is_empty() && cert.segments.is_empty() {
        let start = std::time::Instant::now();
        let upper = crate::certificate::domain_upper(cert, 0)?;
        let result = crate::axis::verify_axis(cert, threshold_hi, &upper)?;
        let seconds = start.elapsed().as_secs_f64();
        let receipt = json!({
            "r": 0,
            "method": "axis-vertex-sweep",
            "verdict": if result.verified {
                "verified"
            } else if result.non_finite {
                "non-finite"
            } else {
                "refused"
            },
            "x_events": result.x_events,
            "y_events": result.y_events,
            "vertices": result.x_events * result.y_events,
            "min_certified_lower_bound": result.min_lower,
            "argmin": [result.argmin.0, result.argmin.1],
            "seconds": seconds,
        });
        return Ok(DirectionReport {
            index,
            verified: result.verified,
            seconds,
            receipt,
        });
    }
    let result = crate::rotated::verify_direction(cert, index, threshold, threshold_hi, limits)?;
    let mut receipt = json!({
        "r": index,
        "method": "interval-branch-and-bound",
        "verdict": result.verdict.as_str(),
        "nodes": result.nodes,
        "leaves": result.leaves,
        "max_depth": result.max_depth,
        "min_certified_lower_bound": if result.min_lower.is_finite() { json!(result.min_lower) } else { Value::Null },
        "mean_boundary_rectangles": result.mean_boundary,
        "audits": result.audits,
        "audit_every": limits.audit_every,
        "seconds": result.seconds,
    });
    if let Some((x, y, dx, dy)) = result.argmin {
        receipt["least_bound_box"] = json!({"x": x, "y": y, "dx": dx, "dy": dy});
    }
    if let Some((x, y, value, dx, dy)) = result.witness {
        receipt["witness"] =
            json!({"x": x, "y": y, "dx": dx, "dy": dy, "centre_lower_bound": value});
        if confirm {
            // The exact capture at the stopping box's centre and corners: a value
            // below the threshold is an exact refutation at that pose.
            let (c, s) = direction(&cert.step, index);
            let mut poses = vec![(x, y)];
            if result.verdict == Verdict::Unresolved {
                for (sx, sy) in [(-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0), (1.0, 1.0)] {
                    poses.push((x + sx * dx, y + sy * dy));
                }
            }
            let mut least: Option<(BigRational, f64, f64)> = None;
            for (px, py) in poses {
                let exact = crate::oracle::coverage(cert, &of_f64(px), &of_f64(py), &c, &s);
                if least.as_ref().is_none_or(|(v, _, _)| &exact < v) {
                    least = Some((exact, px, py));
                }
            }
            if let Some((exact, px, py)) = least {
                receipt["witness"]["exact_pose"] = json!([px, py]);
                receipt["witness"]["exact_coverage"] = json!(exact.to_string());
                receipt["witness"]["exact_below_threshold"] = json!(&exact < threshold);
            }
        }
    }
    Ok(DirectionReport {
        index,
        verified: result.verdict == Verdict::Verified,
        seconds: result.seconds,
        receipt,
    })
}

/// The certificate-level premises, for the summary receipt.
#[must_use]
pub fn premises(cert: &Certificate) -> Value {
    json!({
        "n": cert.n,
        "L": cert.side.to_string(),
        "B": cert.core.to_string(),
        "D": cert.step.to_string(),
        "angle_count": cert.angle_count,
        "net_origin": cert.net_origin,
        "net_last_tangent": (&cert.step * BigRational::from_integer(cert.angle_count.saturating_sub(1).into())).to_string(),
        "shrink_bound": (&cert.core * (crate::exact::one() + &cert.step)).to_string(),
        "mass_exact": cert.mass.to_string(),
        "mass_below_n": (BigRational::from_integer(cert.n.into()) - &cert.mass).to_string(),
        "format": cert.format,
        "centre_domain": match cert.domain {
            crate::certificate::Domain::Tokoharu => "tokoharu",
            crate::certificate::Domain::PerBin => "per-bin",
        },
        "source_rectangles": cert.source_rectangles,
        "expanded_rectangles": cert.exact.len(),
        "expanded_points": cert.points.len(),
        "expanded_segments": cert.segments.len(),
        "input_sha256": cert.input_sha256,
    })
}
