//! Stage-B tests. Every symbolic branch is recorded in the guard evaluator.
use crate::{
    family::{Family, Segment},
    geom::{self, Polygon},
    rat::{int, q, Q},
    record::Box4,
    require,
    symbolic::{self as sy, EResult, Eval, RF},
    Result,
};
use num_traits::Zero;
#[derive(Clone)]
struct Local {
    f: Vec<Segment>,
    t: Vec<Segment>,
    v: Vec<crate::family::Variable>,
}
fn localize(f: &Family, b: &Box4) -> Local {
    let r = q(7072, 10000);
    let keep = |s: &Segment, tx: bool| {
        let (x0, x1) = if tx {
            (&b[0] - &b[7] - &r, &b[1] - &b[6] + &r)
        } else {
            (&b[0] - &r, &b[1] + &r)
        };
        s.a[0].clone().max(s.b[0].clone()) >= x0
            && s.a[0].clone().min(s.b[0].clone()) <= x1
            && s.a[1].clone().max(s.b[1].clone()) >= &b[2] - &r
            && s.a[1].clone().min(s.b[1].clone()) <= &b[3] + &r
    };
    Local {
        f: crate::family::canonical(
            &f.f.iter()
                .filter(|s| keep(s, false))
                .cloned()
                .collect::<Vec<_>>(),
        ),
        t: crate::family::canonical(
            &f.t.iter()
                .filter(|s| keep(s, true))
                .cloned()
                .collect::<Vec<_>>(),
        ),
        v: f.v
            .iter()
            .filter(|v| {
                v.y >= &b[2] - &r
                    && v.y <= &b[3] + &r
                    && v.xl <= &b[1] + &r
                    && int(2) + &b[7] >= &b[0] - &r
            })
            .cloned()
            .collect(),
    }
}
fn diag(b: &Box4) -> Q {
    let l = b[4].abs().min(b[5].abs());
    let m = b[4].abs().max(b[5].abs());
    if m <= int(1) {
        ((int(1) - &l * &l) / (int(1) + &l * &l)).max(int(2) * &m / (int(1) + &m * &m))
    } else {
        int(1)
    }
}
fn hypotheses(f: &Family, b: &Box4, mode: &str, core1: bool) -> Result<()> {
    let h = geom::hmax(&b[4], &b[5]);
    let a = &f.ua;
    require(
        b[5] <= Q::zero() || b[4] >= Q::zero(),
        "stage B angular interval crosses zero",
    )?;
    if core1 {
        require(
            b[0] >= h && b[2] >= h && b[1] <= int(20) - &h && b[3] <= int(20) - &h,
            "CORE1 whole-box admissibility fails",
        )?;
    }
    if mode != "P" && mode != "B3D" && mode != "B4U" {
        require(f.u.is_none(), "quadrant lemma requires standard U")?;
    }
    let ok = match mode {
        "x" => b[0] >= *a && &b[2] - &h >= *a,
        "y" => b[2] >= *a && &b[0] - &h >= *a,
        "Tx" => b[1] <= *a && &b[2] - &h >= *a,
        "Ty" => b[3] <= *a && &b[0] - &h >= *a,
        "TxHy" => b[1] <= *a && b[2] >= *a,
        "TyHx" => b[3] <= *a && b[0] >= *a,
        "xy" => b[0] >= *a && b[2] >= *a && &b[0] + &b[2] - diag(b) >= int(2) * a,
        "xyh" => b[0] >= *a && b[2] >= *a,
        "P" | "B3D" | "B4U" => true,
        _ => false,
    };
    require(ok, format!("{mode} coordinate hypothesis fails"))
}
fn half(f: &Family, x: bool, side: i64) -> Polygon {
    if x {
        geom::rect(f.ua.clone(), int(side), int(0), int(side))
    } else {
        geom::rect(int(0), int(side), f.ua.clone(), int(side))
    }
}
fn tangent(f: &Family, b: &Box4, p: &[RF; 3], x: bool, e: &mut Eval) -> EResult<RF> {
    let axis = if x { 0 } else { 2 };
    let mid = (&b[axis] + &b[axis + 1]) / int(2);
    let center = if x {
        [RF::q(mid.clone()), RF::q(b[2].clone())]
    } else {
        [RF::q(b[0].clone()), RF::q(mid.clone())]
    };
    let poly = if x {
        geom::rect(f.ua.clone(), int(1000), int(-1000), int(1000))
    } else {
        geom::rect(int(-1000), int(1000), f.ua.clone(), int(1000))
    };
    let (a, z) = if x {
        (
            [RF::q(f.ua.clone()), RF::i(-1000)],
            [RF::q(f.ua.clone()), RF::i(1000)],
        )
    } else {
        (
            [RF::i(-1000), RF::q(f.ua.clone())],
            [RF::i(1000), RF::q(f.ua.clone())],
        )
    };
    let w = sy::width(&a, &z, &center, e)?.unwrap_or_else(|| RF::i(0));
    let length = e.max(w, RF::i(0))?.scale(&int(2000));
    Ok(sy::square_area(&poly, &center, e)?
        .add(&length.mul(&p[if x { 0 } else { 1 }].sub(&RF::q(mid)))))
}
fn extra(f: &Family, b: &Box4, p: &[RF; 3], mode: &str, e: &mut Eval) -> EResult<RF> {
    let center = [p[0].clone(), p[1].clone()];
    match mode {
        "P" | "B3D" => Ok(RF::i(0)),
        "x" | "y" | "xy" | "B4U" => sy::square_area(&f.polygon(20), &center, e),
        "xyh" => Ok(
            sy::square_area(&half(f, true, 20), &center, e)?.add(&sy::square_area(
                &half(f, false, 20),
                &center,
                e,
            )?),
        ),
        "Tx" => tangent(f, b, p, true, e),
        "Ty" => tangent(f, b, p, false, e),
        "TxHy" => {
            Ok(tangent(f, b, p, true, e)?.add(&sy::square_area(&half(f, false, 20), &center, e)?))
        }
        "TyHx" => {
            Ok(tangent(f, b, p, false, e)?.add(&sy::square_area(&half(f, true, 20), &center, e)?))
        }
        _ => unreachable!(),
    }
}
fn threshold(f: &Family, b: &Box4, mode: &str) -> Result<Q> {
    if mode == "P" || mode == "B3D" {
        Ok(
            int(1)
                - crate::leaf::poly_lower(f, b).ok_or_else(|| crate::refuse("undefined P_lo"))?,
        )
    } else if ["xyh", "TxHy", "TyHx"].contains(&mode) {
        Ok(int(2))
    } else {
        Ok(int(1))
    }
}
// Retention is performed per exported row, as required by CORE1; coalescing rows
// before all-corners selection would change the specified test.
pub fn core1(f: &Family, b: &Box4, mode: &str) -> Result<()> {
    hypotheses(f, b, mode, true)?;
    let threshold = threshold(f, b, mode)?;
    let corners: Vec<[RF; 3]> = [&b[0], &b[1]]
        .into_iter()
        .flat_map(|x| {
            [&b[2], &b[3]].into_iter().flat_map(move |y| {
                [&b[6], &b[7]]
                    .into_iter()
                    .map(move |d| [RF::q(x.clone()), RF::q(y.clone()), RF::q(d.clone())])
            })
        })
        .collect();
    let r = q(7072, 10000);
    let keep = |s: &Segment, t: bool| {
        let l = &b[0] - &r - if t { b[7].clone() } else { Q::zero() };
        let h = &b[1] + &r - if t { b[6].clone() } else { Q::zero() };
        s.a[0].clone().max(s.b[0].clone()) >= l
            && s.a[0].clone().min(s.b[0].clone()) <= h
            && s.a[1].clone().max(s.b[1].clone()) >= &b[2] - &r
            && s.a[1].clone().min(s.b[1].clone()) <= &b[3] + &r
    };
    let fs: Vec<_> = f.f.iter().filter(|s| keep(s, false)).collect();
    let ts: Vec<_> = f.t.iter().filter(|s| keep(s, true)).collect();
    crate::profile::update(|s| s.local_segments = fs.len() + ts.len() + f.v.len());
    sy::prove(&b[4], &b[5], |e| {
        let mut sums = vec![RF::i(0); 8];
        for (rows, t) in [(&fs, false), (&ts, true)] {
            for s in rows {
                let mut widths = vec![];
                let mut retain = true;
                for p in &corners {
                    let center = [if t { p[0].sub(&p[2]) } else { p[0].clone() }, p[1].clone()];
                    if let Some(w) = sy::width(&sy::point(&s.a), &sy::point(&s.b), &center, e)? {
                        if e.sign(&w)? < 0 {
                            retain = false;
                            break;
                        }
                        widths.push(w);
                    } else {
                        retain = false;
                        break;
                    }
                }
                if retain {
                    for i in 0..8 {
                        sums[i] = sums[i].add(&widths[i].scale(&s.mass));
                    }
                }
            }
        }
        for v in &f.v {
            if v.rho.is_zero() {
                continue;
            }
            let mut masses = vec![];
            let mut retain = true;
            for p in &corners {
                let length = RF::i(2).add(&p[2]).sub(&RF::q(v.xl.clone()));
                let a = [RF::q(v.xl.clone()), RF::q(v.y.clone())];
                let z = [RF::i(2).add(&p[2]), RF::q(v.y.clone())];
                let center = [p[0].clone(), p[1].clone()];
                if let Some(w) = sy::width(&a, &z, &center, e)? {
                    if e.sign(&w)? < 0 {
                        retain = false;
                        break;
                    }
                    masses.push(w.mul(&length).scale(&v.rho));
                } else {
                    retain = false;
                    break;
                }
            }
            if retain {
                for i in 0..8 {
                    sums[i] = sums[i].add(&masses[i]);
                }
            }
        }
        for (i, p) in corners.iter().enumerate() {
            sums[i] = sums[i]
                .add(&extra(f, b, p, mode, e)?)
                .sub(&RF::q(threshold.clone()));
        }
        Ok(sums)
    })
}
type Plane = [RF; 4];
fn det(a: &[RF; 3], b: &[RF; 3], c: &[RF; 3]) -> RF {
    a[0].mul(&b[1].mul(&c[2]).sub(&b[2].mul(&c[1])))
        .sub(&a[1].mul(&b[0].mul(&c[2]).sub(&b[2].mul(&c[0]))))
        .add(&a[2].mul(&b[0].mul(&c[1]).sub(&b[1].mul(&c[0]))))
}
fn row(p: &Plane) -> [RF; 3] {
    [p[0].clone(), p[1].clone(), p[2].clone()]
}
fn vertex(a: &Plane, b: &Plane, c: &Plane) -> Option<([RF; 3], RF)> {
    let d = det(&row(a), &row(b), &row(c));
    if d.n.is_zero() {
        return None;
    }
    let p = std::array::from_fn(|j| {
        let (mut aa, mut bb, mut cc) = (row(a), row(b), row(c));
        aa[j] = a[3].clone();
        bb[j] = b[3].clone();
        cc[j] = c[3].clone();
        det(&aa, &bb, &cc).div(&d).canonical()
    });
    Some((p, d))
}
fn width(b: &Box4) -> RF {
    let n = sy::normals();
    n[0][0]
        .add(&if b[4] >= Q::zero() {
            n[0][1].clone()
        } else {
            n[0][1].neg()
        })
        .scale(&q(1, 2))
}
fn member(p: &[RF; 3], b: &Box4, e: &mut Eval) -> EResult<bool> {
    let w = width(b);
    let cond = [
        p[0].sub(&RF::q(b[0].clone())),
        RF::q(b[1].clone()).sub(&p[0]),
        p[1].sub(&RF::q(b[2].clone())),
        RF::q(b[3].clone()).sub(&p[1]),
        p[2].sub(&RF::q(b[6].clone())),
        RF::q(b[7].clone()).sub(&p[2]),
        p[0].sub(&w),
        RF::i(20).sub(&w).sub(&p[0]),
        p[1].sub(&w),
        RF::i(20).sub(&w).sub(&p[1]),
    ];
    let mut inside = true;
    for c in cond {
        inside &= e.sign(&c)? >= 0;
    }
    Ok(inside)
}
fn segment_value(loc: &Local, p: &[RF; 3], e: &mut Eval) -> EResult<RF> {
    let mut sum = RF::i(0);
    for (ss, t) in [(&loc.f, false), (&loc.t, true)] {
        let center = [if t { p[0].sub(&p[2]) } else { p[0].clone() }, p[1].clone()];
        for s in ss {
            if let Some(w) = sy::width(&sy::point(&s.a), &sy::point(&s.b), &center, e)? {
                sum = sum.add(&e.max(w, RF::i(0))?.scale(&s.mass));
            }
        }
    }
    for v in &loc.v {
        let a = [RF::q(v.xl.clone()), RF::q(v.y.clone())];
        let z = [RF::i(2).add(&p[2]), RF::q(v.y.clone())];
        let len = z[0].sub(&a[0]);
        if e.sign(&len)? == 0 {
            continue;
        }
        if let Some(w) = sy::width(&a, &z, &[p[0].clone(), p[1].clone()], e)? {
            sum = sum.add(&e.max(w, RF::i(0))?.mul(&len).scale(&v.rho));
        }
    }
    Ok(sum)
}
fn planes(loc: &Local, f: &Family, b: &Box4, mode: &str) -> Vec<Plane> {
    let ns = sy::normals();
    let vs = sy::vertices();
    let mut out = vec![];
    let mut contacts = |a: geom::Point, z: geom::Point, t: bool| {
        let d = geom::sub(&z, &a);
        let l = [d[1].clone(), -d[0].clone()];
        let k = geom::dot(&l, &a);
        for v in &vs {
            out.push([
                RF::q(l[0].clone()),
                RF::q(l[1].clone()),
                RF::q(if t { -l[0].clone() } else { Q::zero() }),
                RF::q(k.clone())
                    .sub(&RF::q(l[0].clone()).mul(&v[0]))
                    .sub(&RF::q(l[1].clone()).mul(&v[1])),
            ]);
        }
        for p in [a, z] {
            for n in &ns {
                out.push([
                    n[0].clone(),
                    n[1].clone(),
                    if t { n[0].neg() } else { RF::i(0) },
                    sy::dot(n, &sy::point(&p)).sub(&RF::q(q(1, 2))),
                ]);
            }
        }
    };
    for (ss, t) in [(&loc.f, false), (&loc.t, true)] {
        for s in ss {
            contacts(s.a.clone(), s.b.clone(), t);
        }
    }
    let polys = match mode {
        "x" | "y" | "xy" | "B4U" => vec![f.polygon(20)],
        "xyh" => vec![half(f, true, 20), half(f, false, 20)],
        _ => vec![],
    };
    for p in polys {
        for i in 0..p.len() {
            contacts(p[i].clone(), p[(i + 1) % p.len()].clone(), false);
        }
    }
    for v in &loc.v {
        for w in &vs {
            out.push([RF::i(0), RF::i(1), RF::i(0), RF::q(v.y.clone()).sub(&w[1])]);
        }
        for n in &ns {
            out.push([
                n[0].clone(),
                n[1].clone(),
                RF::i(0),
                n[0].scale(&v.xl)
                    .add(&n[1].scale(&v.y))
                    .sub(&RF::q(q(1, 2))),
            ]);
            out.push([
                n[0].clone(),
                n[1].clone(),
                n[0].neg(),
                n[0].scale(&int(2))
                    .add(&n[1].scale(&v.y))
                    .sub(&RF::q(q(1, 2))),
            ]);
        }
    }
    for (j, axis) in [0, 2, 6].iter().enumerate() {
        for k in 0..2 {
            let mut p = [RF::i(0), RF::i(0), RF::i(0), RF::q(b[axis + k].clone())];
            p[j] = RF::i(1);
            out.push(p);
        }
    }
    let w = width(b);
    for j in 0..2 {
        for k in [w.clone(), RF::i(20).sub(&w)] {
            let mut p = [RF::i(0), RF::i(0), RF::i(0), k];
            p[j] = RF::i(1);
            out.push(p);
        }
    }
    crate::profile::update(|s| s.planes_before = out.len());
    let mut raw_seen = std::collections::HashSet::new();
    out.retain(|p| raw_seen.insert(p.clone()));
    let mut kept: Vec<Plane> = vec![];
    let mut seen = std::collections::HashSet::new();
    for mut p in out {
        let mut sign = 0;
        let mut removable = true;
        'corners: for x in [&b[0], &b[1]] {
            for y in [&b[2], &b[3]] {
                for d in [&b[6], &b[7]] {
                    let r = p[0]
                        .scale(x)
                        .add(&p[1].scale(y))
                        .add(&p[2].scale(d))
                        .sub(&p[3]);
                    let s = r.sign_poly();
                    let a = s.eval_sign(&b[4]);
                    let z = s.eval_sign(&b[5]);
                    if a == 0 || z == 0 || s.roots_open(&b[4], &b[5]) > 0 {
                        removable = false;
                        break 'corners;
                    } else {
                        let this = a;
                        if sign != 0 && sign != this {
                            removable = false;
                            break 'corners;
                        }
                        sign = this;
                    }
                }
            }
        }
        if removable {
            continue;
        }
        if let Some(j) = (0..4).find(|&j| !p[j].n.is_zero()) {
            let divisor = p[j].clone();
            for c in &mut p {
                *c = c.div(&divisor).canonical();
            }
        }
        if seen.insert(p.clone()) {
            kept.push(p);
        }
    }
    crate::profile::update(|s| s.planes_after = kept.len());
    kept
}
pub fn arrangement(f: &Family, b: &Box4, mode: &str) -> Result<()> {
    hypotheses(f, b, mode, false)?;
    let r = q(7072, 10000);
    if mode == "xy" {
        require(
            f.ua < int(20)
                && int(20) >= &b[0] - &r
                && f.ua <= &b[1] + &r
                && int(20) >= &b[2] - &r
                && f.ua <= &b[3] + &r,
            "B3U:xy local polygon guard fails",
        )?;
    }
    if mode == "B4U" {
        let p = f.polygon(20);
        require(
            p.len() >= 3
                && !(p.iter().all(|p| p[0] < &b[0] - &r)
                    || p.iter().all(|p| p[0] > &b[1] + &r)
                    || p.iter().all(|p| p[1] < &b[2] - &r)
                    || p.iter().all(|p| p[1] > &b[3] + &r)),
            "B4U local polygon guard fails",
        )?;
    }
    let timer = crate::profile::stage("localize");
    let loc = localize(f, b);
    drop(timer);
    crate::profile::update(|s| s.local_segments = loc.f.len() + loc.t.len() + loc.v.len());
    let timer = crate::profile::stage("planes");
    let planes = planes(&loc, f, b, mode);
    drop(timer);
    let _timer = crate::profile::stage("enumeration");
    let tau = threshold(f, b, mode)?;
    let mut cache_batch = 0;
    for i in 0..planes.len() {
        for j in i + 1..planes.len() {
            for k in j + 1..planes.len() {
                if let Some((p, d)) = vertex(&planes[i], &planes[j], &planes[k]) {
                    crate::profile::update(|s| s.nonzero_triples += 1);
                    sy::prove(&b[4], &b[5], |e| {
                        e.sign(&d)?;
                        if !member(&p, b, e)? {
                            return Ok(vec![]);
                        }
                        let v = segment_value(&loc, &p, e)?
                            .add(&extra(f, b, &p, mode, e)?)
                            .sub(&RF::q(tau.clone()));
                        Ok(vec![v])
                    })?;
                }
                // A completed triple leaves no live Eval or pending proof.
                // These memo tables only avoid recomputation; retaining all
                // prior vertices' geometry makes memory grow with C(n, 3).
                // Count zero-determinant triples too: constructing them can
                // populate the polynomial cache. All triples and proofs still
                // run in exactly the same order, with the same proof limits.
                cache_batch += 1;
                if cache_batch == 32 {
                    sy::clear_caches();
                    crate::poly::clear_caches();
                    cache_batch = 0;
                }
            }
        }
    }
    if mode == "B4U" {
        sy::prove_frontier(&b[4], &b[5], |e| {
            let mut values = vec![];
            for i in 0..planes.len() {
                // Keep edge memoization for one first plane, rather than all
                // groups' vertices. The accumulated guards in e and critical
                // values own their data and remain intact for the frontier
                // proof. A cache miss recomputes the same guarded expression.
                sy::clear_caches();
                crate::poly::clear_caches();
                for j in i + 1..planes.len() {
                    let a = row(&planes[i]);
                    let z = row(&planes[j]);
                    let direction = [
                        a[1].mul(&z[2]).sub(&a[2].mul(&z[1])),
                        a[2].mul(&z[0]).sub(&a[0].mul(&z[2])),
                        a[0].mul(&z[1]).sub(&a[1].mul(&z[0])),
                    ];
                    if direction.iter().all(|x| x.n.is_zero()) {
                        continue;
                    }
                    let mut points: Vec<([RF; 3], RF)> = vec![];
                    for k in 0..planes.len() {
                        if k == i || k == j {
                            continue;
                        }
                        if let Some((p, d)) = vertex(&planes[i], &planes[j], &planes[k]) {
                            e.sign(&d)?;
                            if !member(&p, b, e)? {
                                continue;
                            }
                            if points.iter().any(|(q, _)| q == &p) {
                                continue;
                            }
                            let projection =
                                (0..3).fold(RF::i(0), |v, c| v.add(&direction[c].mul(&p[c])));
                            let mut index = points.len();
                            while index > 0 && e.sign(&projection.sub(&points[index - 1].1))? < 0 {
                                index -= 1;
                            }
                            points.insert(index, (p, projection));
                        }
                    }
                    for pair in points.windows(2) {
                        let p = &pair[0].0;
                        let q = &pair[1].0;
                        if p == q {
                            continue;
                        }
                        let mid =
                            std::array::from_fn(|i| p[i].add(&q[i]).scale(&crate::rat::q(1, 2)));
                        let gp = extra(f, b, p, "B4U", e)?;
                        let gm = extra(f, b, &mid, "B4U", e)?;
                        let gq = extra(f, b, q, "B4U", e)?;
                        let fp = segment_value(&loc, p, e)?.add(&gp);
                        let fq = segment_value(&loc, q, e)?.add(&gq);
                        let aa = gp.sub(&gm.scale(&int(2))).add(&gq).scale(&int(2));
                        let bb = fq.sub(&fp).sub(&aa);
                        if e.sign(&aa)? > 0 {
                            let t = bb.neg().div(&aa.scale(&int(2)));
                            let positive = e.sign(&t)? > 0;
                            let below = e.sign(&RF::i(1).sub(&t))? > 0;
                            if positive && below {
                                values.push(
                                    fp.sub(&bb.mul(&bb).div(&aa.scale(&int(4)))).sub(&RF::i(1)),
                                );
                            }
                        }
                    }
                }
            }
            Ok(values)
        })?;
    }
    Ok(())
}

/// Root-local rows retain their original identities and masses (CORE1 selection).
/// A row outside this expanded box cannot meet any square of any child leaf.
pub fn local_family(f: &Family, b: &Box4) -> Family {
    let mut out = f.clone();
    let r = q(7072, 10000);
    let keep = |s: &Segment, t: bool| {
        let lo = &b[0] - &r - if t { b[7].clone() } else { Q::zero() };
        let hi = &b[1] + &r - if t { b[6].clone() } else { Q::zero() };
        (&s.a[0]).max(&s.b[0]) >= &lo
            && (&s.a[0]).min(&s.b[0]) <= &hi
            && (&s.a[1]).max(&s.b[1]) >= &(&b[2] - &r)
            && (&s.a[1]).min(&s.b[1]) <= &(&b[3] + &r)
    };
    out.f.retain(|s| keep(s, false));
    out.t.retain(|s| keep(s, true));
    // V rows remain unfiltered: CORE1's availability rule applies even at length zero.
    out
}
