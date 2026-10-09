//! Exact convex geometry and strict ownership predicates.
use crate::exact::{Plane, Point, Poly, Q, dot};
use crate::{Result, require};
/// Return the exact signed orientation of three points.
#[must_use]
pub fn cross(o: &Point, a: &Point, b: &Point) -> Q {
    Q::from(&a.0 - &o.0) * Q::from(&b.1 - &o.1) - Q::from(&a.1 - &o.1) * Q::from(&b.0 - &o.0)
}
/// Return the convex hull, removing duplicate and collinear interior points.
#[must_use]
pub fn hull(points: &[Point]) -> Poly {
    let mut pts: Vec<_> = points.iter().collect();
    pts.sort();
    pts.dedup();
    if pts.len() <= 2 {
        return pts.into_iter().cloned().collect();
    }
    let hp: Vec<_> = pts.iter().map(|p| crate::sweep::homogeneous(p)).collect();
    let nonleft = |o: usize, a: usize, b: usize| {
        let (ox, oy, oz) = &hp[o];
        let (ax, ay, az) = &hp[a];
        let (bx, by, bz) = &hp[b];
        // The rational cross product multiplied by oz^2 * az * bz > 0.
        !crate::int::Int::cmp_products(
            &(ax * oz - ox * az),
            &(by * oz - oy * bz),
            &(ay * oz - oy * az),
            &(bx * oz - ox * bz),
        )
        .is_gt()
    };
    let mut lower = Vec::with_capacity(pts.len());
    let mut upper = Vec::with_capacity(pts.len());
    for i in 0..pts.len() {
        while lower.len() >= 2 && nonleft(lower[lower.len() - 2], lower[lower.len() - 1], i) {
            lower.pop();
        }
        lower.push(i);
    }
    for i in (0..pts.len()).rev() {
        while upper.len() >= 2 && nonleft(upper[upper.len() - 2], upper[upper.len() - 1], i) {
            upper.pop();
        }
        upper.push(i);
    }
    lower.pop();
    upper.pop();
    lower.extend(upper);
    lower.into_iter().map(|i| pts[i].clone()).collect()
}
/// Return twice the unsigned polygon area, or zero for fewer than three vertices.
#[must_use]
pub fn area2(p: &[Point]) -> Q {
    if p.len() < 3 {
        return Q::new();
    }
    let mut sum = Q::new();
    for i in 0..p.len() {
        let a = &p[i];
        let b = &p[(i + 1) % p.len()];
        sum += a.0.clone() * &b.1 - b.0.clone() * &a.1;
    }
    sum.abs()
}
/// Clip a polygon to `a*x + b*y <= c`, retaining boundary points.
#[must_use]
#[expect(
    clippy::many_single_char_names,
    reason = "Coordinate and polynomial symbols match the exact geometric formulas."
)]
pub fn clip_closed(polygon: &[Point], a: &Q, b: &Q, c: &Q) -> Poly {
    let mut out = vec![];
    let values: Vec<_> = polygon.iter().map(|p| dot(a, b, p) - c).collect();
    for i in 0..polygon.len() {
        let p = &polygon[i];
        let q = &polygon[(i + 1) % polygon.len()];
        let fp = &values[i];
        let fq = &values[(i + 1) % polygon.len()];
        if fp <= &0 {
            out.push(p.clone());
        }
        if (fp < &0 && fq > &0) || (fq < &0 && fp > &0) {
            let t = Q::from(fp / Q::from(fp - fq));
            out.push((
                p.0.clone() + t.clone() * (q.0.clone() - &p.0),
                p.1.clone() + t * (q.1.clone() - &p.1),
            ));
        }
    }
    out.dedup();
    if out.len() > 1 && out.first() == out.last() {
        out.pop();
    }
    out
}
/// Derive closed inward half-planes from a nondegenerate convex hull.
#[expect(
    clippy::many_single_char_names,
    reason = "Coordinate and polynomial symbols match the exact geometric formulas."
)]
pub fn planes_of(polygon: &[Point]) -> Result<Vec<Plane>> {
    let h = hull(polygon);
    require(h.len() >= 3, "planes of a degenerate polygon")?;
    Ok((0..h.len())
        .map(|i| {
            let p = &h[i];
            let q = &h[(i + 1) % h.len()];
            let a = q.1.clone() - &p.1;
            let b = p.0.clone() - &q.0;
            let c = dot(&a, &b, p);
            (a, b, c)
        })
        .collect())
}
/// Test membership in the closed convex hull, including its boundary.
pub fn inside(polygon: &[Point], pt: &Point) -> Result<bool> {
    Ok(planes_of(polygon)?
        .iter()
        .all(|(a, b, c)| dot(a, b, pt) <= *c))
}
/// Compare convex hulls as exact geometric sets.
#[must_use]
pub fn same_set(a: &[Point], b: &[Point]) -> bool {
    hull(a) == hull(b)
}
/// Return rational cosine and sine for the half-angle tangent parameter.
#[must_use]
pub fn trig(t: &Q) -> (Q, Q) {
    let tt = t.clone() * t;
    (
        (Q::from(1) - &tt) / (Q::from(1) + &tt),
        t.clone() * 2 / (Q::from(1) + tt),
    )
}
/// Construct the interval wall box at the declared side cap.
#[must_use]
#[expect(
    clippy::many_single_char_names,
    reason = "Coordinate and polynomial symbols match the exact geometric formulas."
)]
pub fn wall_box(lo: &Q, hi: &Q, cap: &Q) -> Poly {
    let (c, s) = trig(lo);
    let (d, t) = trig(hi);
    let h: Q = (c + s).min(d + t) / 2;
    let far = cap.clone() - &h;
    vec![
        (h.clone(), h.clone()),
        (far.clone(), h.clone()),
        (far.clone(), far.clone()),
        (h, far),
    ]
}
/// Intersect with the closed half-planes of the other convex hull.
pub fn intersect_convex(polygon: &[Point], other: &[Point]) -> Result<Poly> {
    let mut p = polygon.to_vec();
    for (a, b, c) in planes_of(other)? {
        p = clip_closed(&p, &a, &b, &c);
        if p.is_empty() {
            break;
        }
    }
    Ok(p)
}
/// Test strict quadratic positivity at endpoints and any interior minimum.
#[must_use]
pub fn quad_min_positive(a0: &Q, a1: &Q, a2: &Q, lo: &Q, hi: &Q) -> bool {
    let eval = |t: &Q| a0.clone() + a1.clone() * t + a2.clone() * t * t;
    if eval(lo) <= 0 || eval(hi) <= 0 {
        return false;
    }
    if a2 > &Q::new() {
        let tv = -a1.clone() / (a2.clone() * 2);
        if lo < &tv && &tv < hi && eval(&tv) <= 0 {
            return false;
        }
    }
    true
}
/// Test every core vertex for strict inclusion over the angle interval.
#[must_use]
pub fn core_strict(core: &[Point], lo: &Q, hi: &Q) -> bool {
    let half = Q::from((1, 2));
    for (x, y) in core {
        for sg in [1, -1] {
            if !quad_min_positive(
                &(half.clone() - x.clone() * sg),
                &(y.clone() * (-2 * sg)),
                &(half.clone() + x.clone() * sg),
                lo,
                hi,
            ) || !quad_min_positive(
                &(half.clone() - y.clone() * sg),
                &(x.clone() * (2 * sg)),
                &(half.clone() + y.clone() * sg),
                lo,
                hi,
            ) {
                return false;
            }
        }
    }
    true
}
/// Return the convex hull of all pairwise point differences.
#[must_use]
pub fn minkowski_diff(first: &[Point], second: &[Point]) -> Poly {
    hull(
        &first
            .iter()
            .flat_map(|a| {
                second
                    .iter()
                    .map(move |b| (a.0.clone() - &b.0, a.1.clone() - &b.1))
            })
            .collect::<Poly>(),
    )
}
/// Certify strict ownership by interval bounds, bisecting to depth eighteen.
pub fn owned(cell: &[Point], pt: &Point, cap: &Q, lo: &Q, hi: &Q, depth: usize) -> Result<bool> {
    let legal = intersect_convex(cell, &wall_box(lo, hi, cap))?;
    if legal.is_empty() {
        return Ok(true);
    }
    let (cl, sl) = trig(lo);
    let (ch, sh) = trig(hi);
    let mut ok = true;
    for (vx, vy) in legal {
        let dx = pt.0.clone() - vx;
        let dy = pt.1.clone() - vy;
        for (a, d) in [(dx.clone(), dy.clone()), (dy, -dx)] {
            for cc in [&cl, &ch] {
                for ss in [&sl, &sh] {
                    if (a.clone() * cc + d.clone() * ss).abs() >= Q::from((1, 2)) {
                        ok = false;
                    }
                }
            }
            if !ok {
                break;
            }
        }
        if !ok {
            break;
        }
    }
    if ok {
        return Ok(true);
    }
    if depth >= 18 {
        return Ok(false);
    }
    let mid = (lo.clone() + hi) / 2;
    Ok(owned(cell, pt, cap, lo, &mid, depth + 1)? && owned(cell, pt, cap, &mid, hi, depth + 1)?)
}
#[cfg(test)]
/// Subtract a closed convex region for the area-based test oracle.
pub fn subtract_pieces(pieces: Vec<Poly>, region: &[Point]) -> Result<Vec<Poly>> {
    let planes = planes_of(region)?;
    let mut out = vec![];
    for mut rest in pieces {
        for (a, b, c) in &planes {
            let outside = clip_closed(&rest, &-a.clone(), &-b.clone(), &-c.clone());
            if !outside.is_empty() && area2(&outside) > 0 {
                out.push(outside);
            }
            rest = clip_closed(&rest, a, b, c);
            if rest.is_empty() || area2(&rest) == 0 {
                break;
            }
        }
    }
    Ok(out)
}
#[cfg(test)]
/// Use exact remaining area as an independent full-dimensional test oracle.
pub fn covered_by_area(domain: &[Point], regions: &[Poly]) -> Result<(bool, usize)> {
    let mut pieces = vec![domain.to_vec()];
    for r in regions {
        if hull(r).len() < 3 {
            continue;
        }
        pieces = subtract_pieces(pieces, r)?;
        if pieces.is_empty() {
            return Ok((true, 0));
        }
    }
    Ok((
        pieces.iter().map(|p| area2(p)).sum::<Q>() == 0,
        pieces.len(),
    ))
}
