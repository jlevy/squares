use crate::{
    family::{Family, Segment},
    geom::*,
    rat::{int, midpoint, q, Q},
    record::Box4,
    refuse, require, Result,
};
use num_traits::Zero;
use std::collections::BTreeSet;
pub fn core_polygons(b: &Box4) -> Option<(Polygon, Polygon)> {
    let w = w_min(&b[4], &b[5]) / int(2);
    let x0 = b[0].clone().max(w.clone());
    let y0 = b[2].clone().max(w);
    if x0 > b[1] || y0 > b[3] {
        return None;
    }
    let z = [midpoint(&x0, &b[1]), midpoint(&y0, &b[3])];
    let rx = (&b[1] - x0) / int(2);
    let ry = (&b[3] - y0) / int(2);
    let n0 = normals(&b[4]);
    let n1 = normals(&b[5]);
    let mut p = rect(int(-2), int(2), int(-2), int(2));
    for j in 0..4 {
        let nsum = [&n0[j][0] + &n1[j][0], &n0[j][1] + &n1[j][1]];
        let chord = dot(&nsum, &n0[j]) / int(2);
        for (n, d) in [
            (n0[j].clone(), q(1, 2)),
            (n1[j].clone(), q(1, 2)),
            (nsum, chord),
        ] {
            let rhs = d - n[0].abs() * &rx - n[1].abs() * &ry;
            p = clip(&p, &n, &rhs);
        }
    }
    for a in &mut p {
        a[0] += &z[0];
        a[1] += &z[1];
    }
    let v0 = vertices(&b[4]);
    let v1 = vertices(&b[5]);
    let mut pts = vec![];
    for j in 0..4 {
        let mut arc = vec![v0[j].clone(), v1[j].clone()];
        let det = cross(&v0[j], &v1[j]);
        if !det.is_zero() {
            arc.push([
                (&v1[j][1] - &v0[j][1]) / (int(2) * &det),
                (&v0[j][0] - &v1[j][0]) / (int(2) * det),
            ]);
        }
        for a in arc {
            for sx in [-1, 1] {
                for sy in [-1, 1] {
                    pts.push([&a[0] + &z[0] + int(sx) * &rx, &a[1] + &z[1] + int(sy) * &ry]);
                }
            }
        }
    }
    Some((p, hull(pts)))
}
pub fn poly_lower(f: &Family, b: &Box4) -> Option<Q> {
    let _timer = crate::profile::stage("core_geometry");
    let (p, o) = core_polygons(b)?;
    if p.len() < 3 {
        return Some(Q::zero());
    }
    let u = f.polygon(1000);
    Some(
        area(&intersection(&p, &u))
            .max(int(1) - area(&o) + area(&intersection(&o, &u)))
            .max(Q::zero()),
    )
}
pub fn core(f: &Family, b: &Box4) -> Option<Q> {
    let _timer = crate::profile::stage("core_geometry");
    let (p, o) = core_polygons(b)?;
    let u = f.polygon(1000);
    let lower = area(&intersection(&p, &u)).max(int(1) - area(&o) + area(&intersection(&o, &u)));
    let mass = |ss: &[Segment], p: &Polygon| -> Q {
        if p.len() < 3 {
            return Q::zero();
        }
        let xmin = p.iter().map(|p| &p[0]).min().unwrap();
        let xmax = p.iter().map(|p| &p[0]).max().unwrap();
        let ymin = p.iter().map(|p| &p[1]).min().unwrap();
        let ymax = p.iter().map(|p| &p[1]).max().unwrap();
        let constraints = planes(p);
        ss.iter()
            .filter(|s| {
                (&s.a[0]).max(&s.b[0]) >= xmin
                    && (&s.a[0]).min(&s.b[0]) <= xmax
                    && (&s.a[1]).max(&s.b[1]) >= ymin
                    && (&s.a[1]).min(&s.b[1]) <= ymax
            })
            .map(|s| {
                segment_width(&s.a, &s.b, &constraints)
                    .unwrap_or_else(Q::zero)
                    .max(Q::zero())
                    * &s.mass
            })
            .sum()
    };
    let mut p0 = p.clone();
    let mut p1 = p.clone();
    for a in &mut p0 {
        a[0] -= &b[6];
    }
    for a in &mut p1 {
        a[0] -= &b[7];
    }
    let pt = intersection(&p0, &p1);
    Some(mass(&f.f, &p) + mass(&f.t, &pt) + mass(&f.variables(&b[6]), &p) + lower)
}
pub fn dx(f: &Family, lo: &Q, hi: &Q) -> Q {
    let ss: Vec<_> =
        f.f.iter()
            .filter(|s| s.vertical() && s.a[0] == f.ua)
            .collect();
    let mut cuts = BTreeSet::from([lo.clone(), hi.clone()]);
    for s in &ss {
        for y in [&s.a[1], &s.b[1]] {
            if y > lo && y < hi {
                cuts.insert(y.clone());
            }
        }
    }
    let cuts: Vec<_> = cuts.into_iter().collect();
    cuts.windows(2)
        .map(|ab| {
            let y = midpoint(&ab[0], &ab[1]);
            ss.iter()
                .filter(|s| {
                    y > s.a[1].clone().min(s.b[1].clone()) && y < s.a[1].clone().max(s.b[1].clone())
                })
                .map(|s| s.density())
                .sum::<Q>()
        })
        .min()
        .unwrap_or_else(Q::zero)
}
pub fn dy(f: &Family, lo: &Q, hi: &Q, e0: &Q, e1: &Q) -> Q {
    let fs: Vec<_> =
        f.f.iter()
            .filter(|s| !s.vertical() && s.a[1] == f.ua)
            .collect();
    let ts: Vec<_> =
        f.t.iter()
            .filter(|s| !s.vertical() && s.a[1] == f.ua)
            .collect();
    let vs: Vec<_> = f.v.iter().filter(|v| v.y == f.ua).collect();
    let mut xs = BTreeSet::from([lo.clone(), hi.clone()]);
    let mut insert = |x: Q| {
        if &x > lo && &x < hi {
            xs.insert(x);
        }
    };
    for s in &fs {
        insert(s.a[0].clone());
        insert(s.b[0].clone());
    }
    for v in &vs {
        insert(v.xl.clone());
    }
    insert(int(2) + e0);
    insert(int(2) + e1);
    for s in &ts {
        for x in [&s.a[0], &s.b[0]] {
            insert(x + e0);
            insert(x + e1);
        }
    }
    let xs: Vec<_> = xs.into_iter().collect();
    let mut min: Option<Q> = None;
    for ab in xs.windows(2) {
        let x = midpoint(&ab[0], &ab[1]);
        let mut ds = BTreeSet::from([e0.clone(), e1.clone()]);
        let mut insert = |d: Q| {
            if &d > e0 && &d < e1 {
                ds.insert(d);
            }
        };
        insert(&x - int(2));
        for s in &ts {
            insert(&x - &s.a[0]);
            insert(&x - &s.b[0]);
        }
        let ds: Vec<_> = ds.into_iter().collect();
        for de in ds.windows(2) {
            let d = midpoint(&de[0], &de[1]);
            let inside = |s: &&Segment, xx: &Q| {
                *xx > s.a[0].clone().min(s.b[0].clone()) && *xx < s.a[0].clone().max(s.b[0].clone())
            };
            let density = fs
                .iter()
                .filter(|s| inside(s, &x))
                .map(|s| s.density())
                .sum::<Q>()
                + ts.iter()
                    .filter(|s| inside(s, &(&x - &d)))
                    .map(|s| s.density())
                    .sum::<Q>()
                + vs.iter()
                    .filter(|v| x > v.xl && x < int(2) + &d)
                    .map(|v| v.rho.clone())
                    .sum::<Q>();
            min = Some(min.map_or(density.clone(), |v| v.min(density)));
        }
    }
    min.unwrap_or_else(Q::zero)
}
fn side(f: &Family, b: &Box4, x: bool) -> bool {
    let h = hmax(&b[4], &b[5]);
    if x {
        let depth = &f.ua - &b[0] + &h;
        b[0] >= f.ua && (depth <= Q::zero() || depth <= dx(f, &(&b[2] - &h), &(&b[3] + &h)))
    } else {
        let depth = &f.ua - &b[2] + &h;
        b[2] >= f.ua
            && (depth <= Q::zero() || depth <= dy(f, &(&b[0] - &h), &(&b[1] + &h), &b[6], &b[7]))
    }
}
// Cache entries own their data; no proof state borrows from them. Release the
// payloads on every exit, including a refusal or a caught arithmetic panic, so
// idle workers do not retain the last leaf's symbolic expressions.
struct LeafCaches;
impl Drop for LeafCaches {
    fn drop(&mut self) {
        crate::symbolic::clear_caches();
        crate::poly::clear_caches();
    }
}
pub fn check(f: &Family, b: &Box4, kind: &str) -> Result<()> {
    crate::poly::clear_caches();
    crate::symbolic::clear_caches();
    let _caches = LeafCaches;
    crate::budget::check();
    crate::record::validate_box(b)?;
    require(b[6] >= f.d0 && b[7] <= f.d1, "leaf delta outside family")?;
    // Bounds are part of the geometry contract; truncation edges must be unreachable.
    let r = q(7072, 10000);
    require(
        &b[1] + &r < int(20) && &b[3] + &r < int(20),
        "local square reaches computational truncation edge",
    )?;
    match kind {
        "EMPTY" => {
            let w = w_min(&b[4], &b[5]) / int(2);
            require(b[1] < w || b[3] < w, "EMPTY strict width test fails")
        }
        "CORE" => require(
            core(f, b).is_some_and(|v| v >= int(1)),
            "CORE bound is undefined or below 1",
        ),
        "EDGE" => {
            require(f.u.is_none(), "EDGE requires standard quadrant")?;
            require(
                side(f, b, true) && side(f, b, false),
                "EDGE density or position condition fails",
            )
        }
        "EX:CORE" | "EY:CORE" => {
            require(f.u.is_none(), "EX/EY requires standard original quadrant")?;
            let x = kind.starts_with("EX");
            require(side(f, b, x), "one-sided density condition fails")?;
            require(
                core(&f.variant(x), b).is_some_and(|v| v >= int(1)),
                "variant CORE bound is undefined or below 1",
            )
        }
        _ => {
            require(
                crate::record::KINDS.contains(&kind),
                format!("unknown kind {kind}"),
            )?;
            require(
                !(b[4] < Q::zero() && b[5] > Q::zero()),
                "stage B leaf crosses u=0",
            )?;
            if let Some(mode) = kind.strip_prefix("CORE1:") {
                crate::stage_b::core1(f, b, mode)
            } else if kind == "EX:B3D" || kind == "EY:B3D" {
                require(f.u.is_none(), "EX/EY requires standard original quadrant")?;
                let x = kind.starts_with("EX");
                require(side(f, b, x), "one-sided density condition fails")?;
                crate::stage_b::arrangement(&f.variant(x), b, "B3D")
            } else {
                let mode = match kind {
                    "B3D" => "B3D",
                    "B4U" => "B4U",
                    "B3T:x" => "Tx",
                    "B3T:y" => "Ty",
                    _ => kind
                        .strip_prefix("B3U:")
                        .ok_or_else(|| refuse("unsupported stage B kind"))?,
                };
                crate::stage_b::arrangement(f, b, mode)
            }
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;
    fn f() -> Family {
        Family::parse(json!({"d0":"0","d1":"1/10","UA":"9/5","F":[["9/5","0","9/5","2","4"],["9/5","1","9/5","3","2"],["0","9/5","2","9/5","2"]],"T":[],"V":[]})).unwrap()
    }
    #[test]
    fn density_sum() {
        let f = f();
        assert_eq!(dx(&f, &q(3, 2), &int(2)), int(3));
        assert_eq!(dx(&f, &int(0), &int(3)), int(1));
        assert_eq!(dy(&f, &int(0), &int(2), &int(0), &q(1, 10)), int(1));
    }
    #[test]
    fn core_in_interior() {
        let f = f();
        let b = [
            int(3),
            q(31, 10),
            int(3),
            q(31, 10),
            q(1, 10),
            q(11, 100),
            int(0),
            q(1, 10),
        ];
        assert!(core(&f, &b).unwrap() >= int(1));
    }
}
