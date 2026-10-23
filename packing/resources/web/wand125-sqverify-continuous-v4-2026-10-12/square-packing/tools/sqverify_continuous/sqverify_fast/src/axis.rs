//! Direction `r = 0`: the axis-aligned shrunk square.
//!
//! Lemma A1 of `SOUNDNESS.md`: with every overlap breakpoint `edge +- B/2` in
//! the event lists, the captured mass is bilinear on each cell of the event
//! grid, so its minimum over the reduced centre domain is attained at a grid
//! vertex. This module evaluates an outward-rounded enclosure of the captured
//! mass at every vertex, column by column, with an exact sweep of slope changes
//! in the ordinate (lemma A2), and reports the least lower endpoint.

use std::cmp::Ordering;

use num_bigint::BigInt;
use num_rational::BigRational;

use crate::certificate::Certificate;
use crate::exact::enclose;
use crate::interval::Iv;

/// The outcome of the axis direction.
#[derive(Clone, Debug)]
pub struct AxisResult {
    /// Number of abscissa events.
    pub x_events: usize,
    /// Number of ordinate events.
    pub y_events: usize,
    /// Least certified lower bound over all vertices.
    pub min_lower: f64,
    /// The vertex where it occurs, as decimal strings of exact rationals.
    pub argmin: (String, String),
    /// Whether every vertex cleared the threshold.
    pub verified: bool,
    /// Whether a vertex's enclosure was not finite, which refuses the
    /// direction (lemma F3 proves it cannot happen for an admitted certificate).
    pub non_finite: bool,
}

/// Where a slope step of the ordinate sweep takes effect.
#[derive(Clone, Copy)]
enum Step {
    /// Below the domain: part of the initial slope.
    Initial,
    /// At this event index.
    At(usize),
    /// Above the domain: never inside it.
    Never,
}

fn sorted_events(values: Vec<BigRational>) -> Vec<BigRational> {
    let mut values = values;
    values.sort();
    values.dedup();
    values
}

/// Index of `p` in `events`, `Err(i)` with the insertion point when absent.
fn locate(events: &[BigRational], p: &BigRational) -> Result<usize, usize> {
    events.binary_search_by(|e| e.cmp(p))
}

/// Verify the axis direction at `threshold` (an enclosure's upper end is used)
/// on the quadrant `[L/2, upper]^2`, `upper` the format's domain end.
///
/// # Errors
///
/// Returns a message if an exact event cannot be enclosed in binary64.
pub fn verify_axis(
    cert: &Certificate,
    threshold_hi: f64,
    upper: &BigRational,
) -> Result<AxisResult, String> {
    let two = BigRational::from_integer(BigInt::from(2));
    let h = &cert.core / &two;
    let lower = &cert.side / &two;
    let upper = upper.clone();
    let in_range = |p: &BigRational| p >= &lower && p <= &upper;
    let mut xs = vec![lower.clone(), upper.clone()];
    let mut ys = vec![lower.clone(), upper.clone()];
    for rect in &cert.exact {
        for edge in [&rect.x1, &rect.x2] {
            for p in [edge - &h, edge + &h] {
                if in_range(&p) {
                    xs.push(p);
                }
            }
        }
        for edge in [&rect.y1, &rect.y2] {
            for p in [edge - &h, edge + &h] {
                if in_range(&p) {
                    ys.push(p);
                }
            }
        }
    }
    let xs = sorted_events(xs);
    let ys = sorted_events(ys);
    let x_iv: Vec<Iv> = xs.iter().map(enclose).collect::<Result<_, _>>()?;
    let y_iv: Vec<Iv> = ys.iter().map(enclose).collect::<Result<_, _>>()?;
    let h_iv = enclose(&h)?;
    let m = ys.len();

    // Each rectangle's ordinate overlap is r(y+h-y1) - r(y+h-y2) - r(y-h-y1) +
    // r(y-h-y2), with r(z) = max(z, 0). Its slope steps by +1, -1, -1, +1 at
    // y1-h, y2-h, y1+h, y2+h. A step below the domain belongs to the initial
    // slope; a step above it never takes effect inside the domain.
    let mut steps: Vec<[(Step, f64); 4]> = Vec::with_capacity(cert.exact.len());
    for rect in &cert.exact {
        let points = [
            (&rect.y1 - &h, 1.0),
            (&rect.y2 - &h, -1.0),
            (&rect.y1 + &h, -1.0),
            (&rect.y2 + &h, 1.0),
        ];
        let mut row = [(Step::Never, 0.0); 4];
        for (slot, (p, sign)) in row.iter_mut().zip(points) {
            let step = match p.cmp(&lower) {
                Ordering::Less => Step::Initial,
                _ if p > upper => Step::Never,
                _ => match locate(&ys, &p) {
                    Ok(index) => Step::At(index),
                    Err(_) => {
                        return Err("an in-range breakpoint is missing from the events".into());
                    }
                },
            };
            *slot = (step, sign);
        }
        steps.push(row);
    }

    let overlap = |centre: Iv, a: Iv, b: Iv| -> Iv {
        // |[c - h, c + h] intersect [a, b]| = (min(c + h, b) - max(c - h, a))^+
        let right = centre.plus(h_iv).min(b);
        let left = centre.minus(h_iv).max(a);
        right.minus(left).pos()
    };

    let mut min_lower = f64::INFINITY;
    let mut argmin = (0usize, 0usize);
    let mut non_finite = false;
    let mut delta = vec![Iv::point(0.0); m];
    let y0 = y_iv[0];
    for (k, &x) in x_iv.iter().enumerate() {
        for d in &mut delta {
            *d = Iv::point(0.0);
        }
        let mut value = Iv::point(0.0);
        let mut slope = Iv::point(0.0);
        for (rect, row) in cert.rects.iter().zip(&steps) {
            let ox = overlap(x, rect.x1, rect.x2);
            if ox.hi <= 0.0 {
                continue;
            }
            let weight = ox.mul_nonneg(rect.rho);
            value = value.plus(weight.mul_nonneg(overlap(y0, rect.y1, rect.y2)));
            for &(step, sign) in row {
                let signed = if sign > 0.0 {
                    weight
                } else {
                    Iv::new(-weight.hi, -weight.lo)
                };
                match step {
                    Step::Initial => slope = slope.plus(signed),
                    Step::At(index) => delta[index] = delta[index].plus(signed),
                    Step::Never => {}
                }
            }
        }
        // A step at index 0 is at the domain's lower end, so it already governs
        // the first cell: fold it into the initial slope.
        slope = slope.plus(delta[0]);
        for j in 0..m {
            // A vertex whose enclosure is not finite stops the sweep: a NaN fails
            // every comparison and would otherwise drop out of the minimum.
            if !(value.lo.is_finite() && value.hi.is_finite()) {
                non_finite = true;
                min_lower = f64::NAN;
                argmin = (k, j);
                break;
            }
            if value.lo < min_lower {
                min_lower = value.lo;
                argmin = (k, j);
            }
            if j + 1 < m {
                let width = y_iv[j + 1].minus(y_iv[j]);
                value = value.plus(slope.times(width));
                slope = slope.plus(delta[j + 1]);
            }
        }
        if non_finite {
            break;
        }
    }
    Ok(AxisResult {
        x_events: xs.len(),
        y_events: ys.len(),
        min_lower,
        argmin: (xs[argmin.0].to_string(), ys[argmin.1].to_string()),
        verified: !non_finite && min_lower.is_finite() && min_lower >= threshold_hi,
        non_finite,
    })
}
