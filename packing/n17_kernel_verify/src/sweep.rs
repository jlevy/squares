//! Exact closed-set coverage by vertical sweep events and sections.
use crate::exact::{Plane, Point, Poly, Q, dot};
use crate::geom::{hull, planes_of};
use crate::int::Int;
use crate::{Result, malformed, require};
use std::collections::{BTreeMap, BTreeSet};
/// Homogeneous Cartesian coordinates `(x, y, z)` with positive denominator z.
pub type HPoint = (Int, Int, Int);
/// A numerator and denominator pair; ordered operations require a positive denominator.
pub type Ratio = (Int, Int);
/// An exact integer normal direction `(nx, ny)`.
pub type Direction = (Int, Int);
/// A normal and support bound `(nx, ny, numerator, denominator)`.
pub type Facet = (Int, Int, Int, Int);
/// A closed ordinate interval `(low, high)`.
pub type Section = (Ratio, Ratio);
/// A polygon index and the ordinate bounds of one vertical edge.
pub type Vertical = (usize, Ratio, Ratio);
/// Vertical edge spans grouped by their normalized abscissa.
pub type Verticals = BTreeMap<Ratio, Vec<Vertical>>;
/// Convert an exact point to a common positive denominator.
#[must_use]
pub fn homogeneous(p: &Point) -> HPoint {
    let dx = Int::from(p.0.denom());
    let dy = Int::from(p.1.denom());
    if dx == dy {
        return (p.0.numer().into(), p.1.numer().into(), dx);
    }
    let z = (&dx / &dx.clone().gcd(&dy)) * &dy;
    (
        Int::from(p.0.numer()) * (&z / &dx),
        Int::from(p.1.numer()) * (&z / &dy),
        z,
    )
}
/// Compare ratios strictly by exact cross products.
#[must_use]
pub fn ratio_lt(a: &Ratio, b: &Ratio) -> bool {
    Int::cmp_products(&a.0, &b.1, &b.0, &a.1).is_lt()
}
/// Order ratios by exact cross products, assuming positive denominators.
#[must_use]
pub fn ratio_cmp(a: &Ratio, b: &Ratio) -> std::cmp::Ordering {
    Int::cmp_products(&a.0, &b.1, &b.0, &a.1)
}
/// Reduce a ratio and make its denominator positive, rejecting zero.
pub fn normalised(mut n: Int, mut d: Int) -> Result<Ratio> {
    if d == 0 {
        return Err(malformed("zero denominator"));
    }
    if d < 0 {
        n = -n;
        d = -d;
    }
    let g = n.clone().gcd(&d);
    if g == 1 {
        return Ok((n, d));
    }
    Ok((n / g.clone(), d / g))
}
/// Construct an exact rational strictly between two ordered positive-denominator ratios.
#[expect(
    clippy::similar_names,
    reason = "Paired endpoint and row names preserve the replay formula notation."
)]
pub fn between(a: &Ratio, b: &Ratio) -> Result<Ratio> {
    require(
        a.1 > 0 && b.1 > 0 && ratio_lt(a, b),
        "malformed coverage interval",
    )?;
    // Iterative continued fractions avoid recursion depth depending on input size.
    let (mut an, mut ad) = a.clone();
    let (mut bn, mut bd) = b.clone();
    let mut wholes = vec![];
    let (mut n, mut d) = loop {
        let whole = an.clone().div_floor(&ad);
        if (whole.clone() + 1) * &bd < bn {
            break (whole + 1, Int::from(1));
        }
        let rest_an = an - &whole * &ad;
        let rest_bn = bn - &whole * &bd;
        if rest_an == 0 {
            let k: Int = bd.div_floor(&rest_bn) + 1;
            break (whole * k.clone() + 1, k);
        }
        wholes.push(whole);
        an = bd;
        bn = ad;
        ad = rest_bn;
        bd = rest_an;
    };
    for w in wholes.into_iter().rev() {
        let nn = w * &n + d;
        d = n;
        n = nn;
    }
    Ok((n, d))
}
/// Return the exact minimum and maximum of a nonempty ratio sequence.
pub fn ratio_extremes(values: &[Ratio]) -> Result<(Ratio, Ratio)> {
    let first = values
        .first()
        .ok_or_else(|| malformed("empty ratio sequence"))?;
    let (mut low, mut high) = (first, first);
    for v in &values[1..] {
        if ratio_lt(v, low) {
            low = v;
        } else if ratio_lt(high, v) {
            high = v;
        }
    }
    Ok((low.clone(), high.clone()))
}
/// Derive primitive boundary normals, rejecting zero-length edges.
pub fn directions(p: &[HPoint]) -> Result<Vec<Direction>> {
    let mut out = vec![];
    for i in 0..p.len() {
        let (px, py, pz) = &p[i];
        let (qx, qy, qz) = &p[(i + 1) % p.len()];
        let nx = qy * pz - py * qz;
        let ny = px * qz - qx * pz;
        let g = nx.clone().gcd(&ny);
        if g == 0 {
            return Err(malformed("zero edge direction"));
        }
        out.push((nx / g.clone(), ny / g));
    }
    Ok(out)
}
/// Return the extreme linear form over homogeneous vertices; empty input yields (0, 0).
#[must_use]
pub fn support(p: &[HPoint], nx: &Int, ny: &Int, largest: bool) -> Ratio {
    let (mut n, mut d) = (Int::from(0), Int::from(0));
    for (x, y, z) in p {
        let v = nx * x + ny * y;
        let better = if d == 0 {
            true
        } else if largest {
            Int::cmp_products(&v, &d, &n, z).is_gt()
        } else {
            Int::cmp_products(&v, &d, &n, z).is_lt()
        };
        if better {
            n = v;
            d = z.clone();
        }
    }
    (n, d)
}
/// Compile exact support facets for the partner-minus-core hull.
pub fn difference_facets(partner: &[HPoint], core: &[HPoint]) -> Result<Vec<Facet>> {
    let mut normals = directions(partner)?;
    normals.extend(directions(core)?.into_iter().map(|(x, y)| (-x, -y)));
    let mut seen = BTreeSet::new();
    let mut out = vec![];
    for (nx, ny) in normals {
        if !seen.insert((nx.clone(), ny.clone())) {
            continue;
        }
        let (tn, td) = support(partner, &nx, &ny, true);
        let (ln, ld) = support(core, &nx, &ny, false);
        out.push((nx, ny, tn * &ld - ln * &td, td * ld));
    }
    Ok(out)
}
#[derive(Clone, Debug)]
/// A nonvertical boundary segment with positive line coefficient b.
pub struct Edge {
    /// Index of the source polygon in the compiled polygon list.
    pub polygon: usize,
    /// Closed left abscissa of the segment.
    pub lo: Ratio,
    /// Closed right abscissa of the segment.
    pub hi: Ratio,
    /// X coefficient of the supporting line.
    pub a: Int,
    /// Positive Y coefficient of the supporting line.
    pub b: Int,
    /// Constant coefficient of the supporting line.
    pub c: Int,
}
/// Compile nonvertical lines and vertical spans while retaining polygon identity.
pub fn compile_edges(polygons: &[Vec<HPoint>]) -> Result<(Vec<Edge>, Verticals)> {
    let mut edges = vec![];
    let mut verticals: Verticals = BTreeMap::new();
    for (index, p) in polygons.iter().enumerate() {
        for i in 0..p.len() {
            let (px, py, pz) = &p[i];
            let (qx, qy, qz) = &p[(i + 1) % p.len()];
            let (mut a, mut b, mut c) = (py * qz - qy * pz, qx * pz - px * qz, px * qy - qx * py);
            if b == 0 {
                let (low, high) =
                    ratio_extremes(&[(py.clone(), pz.clone()), (qy.clone(), qz.clone())])?;
                verticals
                    .entry(normalised(px.clone(), pz.clone())?)
                    .or_default()
                    .push((index, low, high));
                continue;
            }
            if b < 0 {
                a = -a;
                b = -b;
                c = -c;
            }
            // A positive common scale changes neither the line nor its ordinates.
            let g = a.clone().gcd(&b).gcd(&c);
            if g != 1 {
                a = a / &g;
                b = b / &g;
                c = c / &g;
            }
            let (lo, hi) = ratio_extremes(&[(px.clone(), pz.clone()), (qx.clone(), qz.clone())])?;
            edges.push(Edge {
                polygon: index,
                lo,
                hi,
                a,
                b,
                c,
            });
        }
    }
    Ok((edges, verticals))
}
/// Collect vertex and segment-crossing abscissae inside the closed sweep interval.
pub fn sweep_events(
    polygons: &[Vec<HPoint>],
    edges: &[Edge],
    left: &Ratio,
    right: &Ratio,
) -> Result<Vec<Ratio>> {
    let mut events = BTreeSet::new();
    for p in polygons {
        for (x, _, z) in p {
            let r = (x.clone(), z.clone());
            if !ratio_lt(&r, left) && !ratio_lt(right, &r) {
                events.insert(normalised(x.clone(), z.clone())?);
            }
        }
    }
    // Identical segments only repeat crossings already contributed by the first.
    // Polygon identity is irrelevant to the event set (but retained for probes).
    let mut seen = BTreeSet::new();
    let mut order: Vec<_> = (0..edges.len())
        .filter(|&i| {
            let e = &edges[i];
            seen.insert((&e.a, &e.b, &e.c, &e.lo, &e.hi))
        })
        .collect();
    order.sort_by(|&i, &j| ratio_cmp(&edges[i].lo, &edges[j].lo));
    let mut active: Vec<usize> = vec![];
    for i in order {
        let e = &edges[i];
        if ratio_lt(&e.hi, left) || ratio_lt(right, &e.lo) {
            continue;
        }
        active.retain(|&j| !ratio_lt(&edges[j].hi, &e.lo));
        for &j in &active {
            let o = &edges[j];
            let mut det = &e.a * &o.b - &e.b * &o.a;
            if det == 0 {
                continue;
            }
            let mut xn = &e.b * &o.c - &e.c * &o.b;
            if det < 0 {
                xn = -xn;
                det = -det;
            }
            let start = [&e.lo, &o.lo, left]
                .into_iter()
                .max_by(|a, b| ratio_cmp(a, b))
                .expect("three fixed sweep lower bounds form a nonempty iterator");
            let stop = [&e.hi, &o.hi, right]
                .into_iter()
                .min_by(|a, b| ratio_cmp(a, b))
                .expect("three fixed sweep upper bounds form a nonempty iterator");
            let r = (xn, det);
            if !ratio_lt(&r, start) && !ratio_lt(stop, &r) {
                events.insert(normalised(r.0, r.1)?);
            }
        }
        active.push(i);
    }
    let mut out: Vec<_> = events.into_iter().collect();
    out.sort_by(ratio_cmp);
    Ok(out)
}
/// Require positive denominators and correctly ordered closed section endpoints.
#[must_use]
pub fn well_formed(s: &Section) -> bool {
    s.0.1 > 0 && s.1.1 > 0 && !ratio_lt(&s.1, &s.0)
}
/// Test closed target coverage by merging exact closed spans.
pub fn section_covered(target: &Section, mut spans: Vec<Section>) -> Result<bool> {
    section_covered_slice(target, &mut spans)
}
fn section_covered_slice(target: &Section, spans: &mut [Section]) -> Result<bool> {
    require(
        well_formed(target) && spans.iter().all(well_formed),
        "malformed coverage interval",
    )?;
    spans.sort_by(|a, b| ratio_cmp(&a.0, &b.0));
    let mut cursor = &target.0;
    for (low, high) in spans.iter() {
        if ratio_lt(high, cursor) {
            continue;
        }
        if ratio_lt(cursor, low) {
            return Ok(false);
        }
        if ratio_lt(cursor, high) {
            cursor = high;
        }
        if !ratio_lt(cursor, &target.1) {
            return Ok(true);
        }
    }
    Ok(false)
}
/// Expand an optional section to contain the given low and high ordinates.
#[must_use]
pub fn widen(found: Option<Section>, low: Ratio, high: Ratio) -> Section {
    match found {
        None => (low, high),
        Some((a, b)) => (
            if ratio_lt(&low, &a) { low } else { a },
            if ratio_lt(&b, &high) { high } else { b },
        ),
    }
}
/// Check all event sections and intervening slabs for exact closed-set coverage.
pub fn covered_by_sweep(domain: &[Point], regions: &[Poly]) -> Result<(bool, Option<Q>)> {
    let mut polygons = vec![domain.iter().map(homogeneous).collect::<Vec<_>>()];
    polygons.extend(
        regions
            .iter()
            .filter(|r| r.len() >= 3)
            .map(|r| r.iter().map(homogeneous).collect::<Vec<_>>()),
    );
    let (left, right) = ratio_extremes(
        &polygons[0]
            .iter()
            .map(|(x, _, z)| (x.clone(), z.clone()))
            .collect::<Vec<_>>(),
    )?;
    let (edges, verticals) = compile_edges(&polygons)?;
    let positions = sweep_events(&polygons, &edges, &left, &right)?;
    require(
        positions.first() == Some(&normalised(left.0, left.1)?)
            && positions.last() == Some(&normalised(right.0, right.1)?),
        "row domain endpoint missing",
    )?;
    let first = positions
        .first()
        .ok_or_else(|| malformed("no sweep events"))?;
    let mut probes = vec![first.clone()];
    for ab in positions.windows(2) {
        probes.push(between(&ab[0], &ab[1])?);
        probes.push(ab[1].clone());
    }
    let mut starts: Vec<_> = (0..edges.len()).collect();
    let mut ends = starts.clone();
    starts.sort_by(|&a, &b| ratio_cmp(&edges[a].lo, &edges[b].lo));
    ends.sort_by(|&a, &b| ratio_cmp(&edges[a].hi, &edges[b].hi));
    let (mut started, mut ended) = (0, 0);
    let mut live = BTreeSet::new();
    let mut sections = vec![None; polygons.len()];
    let mut spans = Vec::with_capacity(polygons.len());
    for probe in probes {
        while started < starts.len() && !ratio_lt(&probe, &edges[starts[started]].lo) {
            live.insert(starts[started]);
            started += 1;
        }
        while ended < ends.len() && ratio_lt(&edges[ends[ended]].hi, &probe) {
            live.remove(&ends[ended]);
            ended += 1;
        }
        sections.fill(None);
        spans.clear();
        for &i in &live {
            let e = &edges[i];
            // Multiply every ordinate at this probe by its positive denominator.
            // This cancels the same factor from every nonvertical denominator.
            let ordinate = (-(&e.a * &probe.0 + &e.c * &probe.1), e.b.clone());
            let s = widen(sections[e.polygon].take(), ordinate.clone(), ordinate);
            sections[e.polygon] = Some(s);
        }
        if let Some(vs) = verticals.get(&probe) {
            for (p, lo, hi) in vs {
                let low = (&lo.0 * &probe.1, lo.1.clone());
                let high = (&hi.0 * &probe.1, hi.1.clone());
                let s = widen(sections[*p].take(), low, high);
                sections[*p] = Some(s);
            }
        }
        require(sections[0].is_some(), "coverage probe outside domain")?;
        let target = sections[0]
            .take()
            .ok_or_else(|| malformed("missing section"))?;
        spans.extend(sections[1..].iter_mut().filter_map(Option::take));
        if !section_covered_slice(&target, &mut spans)? {
            return Ok((
                false,
                Some(Q::from((
                    rug::Integer::from(probe.0),
                    rug::Integer::from(probe.1),
                ))),
            ));
        }
    }
    Ok((true, None))
}
/// Derive half-planes for polygons, segments, and points without losing boundaries.
pub fn closed_planes(region: &[Point]) -> Result<Vec<Plane>> {
    let ends = hull(region);
    if ends.len() >= 3 {
        return planes_of(&ends);
    }
    if ends.len() == 2 {
        let (x0, y0) = &ends[0];
        let (x1, y1) = &ends[1];
        let dx = x1.clone() - x0;
        let dy = y1.clone() - y0;
        let on = Q::from(&dy * x0) - Q::from(&dx * y0);
        return Ok(vec![
            (dy.clone(), -dx.clone(), on.clone()),
            (-dy.clone(), dx.clone(), -on),
            (
                dx.clone(),
                dy.clone(),
                Q::from(&dx * x1) + Q::from(&dy * y1),
            ),
            (-dx.clone(), -dy.clone(), -(dx * x0 + dy * y0)),
        ]);
    }
    let (x, y) = ends
        .first()
        .ok_or_else(|| malformed("empty closed region"))?;
    Ok(vec![
        (Q::from(1), Q::new(), x.clone()),
        (Q::from(-1), Q::new(), -x.clone()),
        (Q::new(), Q::from(1), y.clone()),
        (Q::new(), Q::from(-1), -y.clone()),
    ])
}
/// Check point or segment domains against a union of closed convex regions.
pub fn degenerate_covered(domain: &[Point], regions: &[Poly]) -> Result<bool> {
    let ends = hull(domain);
    require(
        (1..=2).contains(&ends.len()),
        "a degenerate domain is a point or a segment",
    )?;
    let start = &ends[0];
    let end = &ends[ends.len() - 1];
    let delta = (end.0.clone() - &start.0, end.1.clone() - &start.1);
    let mut spans = vec![];
    for r in regions {
        if r.is_empty() {
            continue;
        }
        let (mut lo, mut hi) = (Q::new(), Q::from(1));
        for (a, b, c) in closed_planes(r)? {
            let value = dot(&a, &b, start) - c;
            let rate = dot(&a, &b, &delta);
            if rate > 0 {
                hi = hi.min(-value / rate);
            } else if rate < 0 {
                lo = lo.max(-value / rate);
            } else if value > 0 {
                lo = Q::from(1);
                hi = Q::new();
            }
            if hi < lo {
                break;
            }
        }
        if lo <= hi {
            spans.push((
                (lo.numer().into(), lo.denom().into()),
                (hi.numer().into(), hi.denom().into()),
            ));
        }
    }
    section_covered(&((0.into(), 1.into()), (1.into(), 1.into())), spans)
}
