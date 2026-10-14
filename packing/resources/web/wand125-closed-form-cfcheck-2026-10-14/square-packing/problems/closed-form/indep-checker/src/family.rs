use crate::{
    geom::{cross, rect, sub, Point, Polygon},
    parse_error,
    rat::{array, int, q, value, Q},
    refuse,
    report::Report,
    require, Result,
};
use num_traits::{One, ToPrimitive, Zero};
use serde_json::{json, Value};
use std::{
    collections::{BTreeMap, BTreeSet},
    path::Path,
};
#[derive(Clone, Debug, PartialEq, Eq)]
pub struct Segment {
    pub a: Point,
    pub b: Point,
    pub mass: Q,
}
impl Segment {
    pub fn vertical(&self) -> bool {
        self.a[0] == self.b[0]
    }
    pub fn length(&self) -> Q {
        (&self.b[0] - &self.a[0]).abs() + (&self.b[1] - &self.a[1]).abs()
    }
    pub fn density(&self) -> Q {
        &self.mass / self.length()
    }
    pub fn shift(&self, d: &Q) -> Self {
        let mut s = self.clone();
        s.a[0] += d;
        s.b[0] += d;
        s
    }
    pub fn transpose(&self) -> Self {
        Self {
            a: [self.a[1].clone(), self.a[0].clone()],
            b: [self.b[1].clone(), self.b[0].clone()],
            mass: self.mass.clone(),
        }
    }
}
#[derive(Clone)]
pub struct Variable {
    pub xl: Q,
    pub y: Q,
    pub rho: Q,
}
#[derive(Clone)]
pub struct Family {
    pub d0: Q,
    pub d1: Q,
    pub ua: Q,
    pub f: Vec<Segment>,
    pub t: Vec<Segment>,
    pub v: Vec<Variable>,
    pub u: Option<Polygon>,
    pub raw: Value,
    pub extra_keys: Vec<String>,
}
impl Family {
    pub fn parse(raw: Value) -> Result<Self> {
        let obj = raw
            .as_object()
            .ok_or_else(|| parse_error("family must be an object"))?;
        let allowed = [
            "d0",
            "d1",
            "UA",
            "F",
            "T",
            "V",
            "U",
            "eps",
            "bumps",
            "note",
            "edge_variant",
            "target",
            "S_d0",
            "S_d1",
        ];
        let required = ["d0", "d1", "UA", "F", "T", "V", "U"];
        let mut extra_keys = vec![];
        for k in obj.keys() {
            if !required.contains(&k.as_str()) {
                extra_keys.push(k.clone());
            }
            require(
                allowed.contains(&k.as_str()),
                format!("unknown family key {k}"),
            )?;
        }
        let d0 = value(&raw["d0"])?;
        let d1 = value(&raw["d1"])?;
        let ua = value(&raw["UA"])?;
        require(d0 < d1, "family d0 must be less than d1")?;
        require(
            d0 >= Q::zero() && d1 <= Q::one(),
            "family delta outside [0,1]",
        )?;
        require(ua == q(9, 5), "UA must equal 9/5")?;
        let mut groups = vec![];
        for key in ["F", "T"] {
            let mut ss = vec![];
            for (i, row) in raw[key]
                .as_array()
                .ok_or_else(|| parse_error(format!("missing {key} array")))?
                .iter()
                .enumerate()
            {
                let a = array(row, 5)?;
                let s = Segment {
                    a: [a[0].clone(), a[1].clone()],
                    b: [a[2].clone(), a[3].clone()],
                    mass: a[4].clone(),
                };
                require(
                    s.mass > Q::zero(),
                    format!("{key}[{i}] mass must be positive"),
                )?;
                require(s.a != s.b, format!("{key}[{i}] zero-length segment"))?;
                require(
                    s.a[0] == s.b[0] || s.a[1] == s.b[1],
                    format!("{key}[{i}] is not axis-parallel"),
                )?;
                ss.push(s);
            }
            groups.push(ss);
        }
        let mut v = vec![];
        for (i, row) in raw["V"]
            .as_array()
            .ok_or_else(|| parse_error("missing V array"))?
            .iter()
            .enumerate()
        {
            let a = array(row, 3)?;
            require(a[2] >= Q::zero(), format!("V[{i}] negative density"))?;
            require(a[0] <= int(2) + &d0, format!("V[{i}] negative length"))?;
            v.push(Variable {
                xl: a[0].clone(),
                y: a[1].clone(),
                rho: a[2].clone(),
            });
        }
        let u = if let Some(u) = raw.get("U") {
            let p: Polygon = u
                .as_array()
                .ok_or_else(|| parse_error("U must be array"))?
                .iter()
                .map(|x| {
                    let a = array(x, 2)?;
                    Ok([a[0].clone(), a[1].clone()])
                })
                .collect::<Result<_>>()?;
            require(p.len() >= 3, "U has fewer than 3 vertices")?;
            require(
                crate::geom::area(&p) > Q::zero(),
                "U must have positive counterclockwise area",
            )?;
            let mut unique = BTreeSet::new();
            for a in &p {
                require(unique.insert(a.clone()), "duplicate U vertex")?;
            }
            for i in 0..p.len() {
                let d = sub(&p[(i + 1) % p.len()], &p[i]);
                for a in &p {
                    require(
                        cross(&d, &sub(a, &p[i])) >= Q::zero(),
                        "U is not a convex counterclockwise polygon",
                    )?;
                }
            }
            Some(p)
        } else {
            None
        };
        Ok(Self {
            d0,
            d1,
            ua,
            f: groups.remove(0),
            t: groups.remove(0),
            v,
            u,
            raw,
            extra_keys,
        })
    }
    pub fn polygon(&self, side: i64) -> Polygon {
        self.u
            .clone()
            .unwrap_or_else(|| rect(self.ua.clone(), int(side), self.ua.clone(), int(side)))
    }
    pub fn variables(&self, d: &Q) -> Vec<Segment> {
        self.v
            .iter()
            .filter_map(|v| {
                let length = int(2) + d - &v.xl;
                if length.is_zero() || v.rho.is_zero() {
                    None
                } else {
                    Some(Segment {
                        a: [v.xl.clone(), v.y.clone()],
                        b: [int(2) + d, v.y.clone()],
                        mass: &v.rho * length,
                    })
                }
            })
            .collect()
    }
    pub fn variant(&self, x: bool) -> Self {
        let mut f = self.clone();
        if x {
            f.f.retain(|s| !(s.a[0] == f.ua && s.b[0] == f.ua));
            f.u = Some(rect(int(-1000), int(1000), f.ua.clone(), int(1000)));
        } else {
            f.f.retain(|s| !(s.a[1] == f.ua && s.b[1] == f.ua));
            f.t.retain(|s| !(s.a[1] == f.ua && s.b[1] == f.ua));
            f.v.retain(|s| s.y != f.ua);
            f.u = Some(rect(f.ua.clone(), int(1000), int(-1000), int(1000)));
        }
        f
    }
}
// A canonical measure consists of maximal open intervals of constant density on support lines.
// Endpoints have no point mass; adjacent equal-density intervals are merged.
pub fn canonical(ss: &[Segment]) -> Vec<Segment> {
    let mut lines: BTreeMap<(bool, Q), BTreeMap<Q, Q>> = BTreeMap::new();
    for s in ss {
        if s.a == s.b || s.mass.is_zero() {
            continue;
        }
        let vert = s.vertical();
        let j = if vert { 1 } else { 0 };
        let pos = s.a[1 - j].clone();
        let lo = s.a[j].clone().min(s.b[j].clone());
        let hi = s.a[j].clone().max(s.b[j].clone());
        let density = s.density();
        let es = lines.entry((vert, pos)).or_default();
        *es.entry(lo).or_default() += &density;
        *es.entry(hi).or_default() -= density;
    }
    let mut out: Vec<Segment> = vec![];
    for ((vert, pos), events) in lines {
        let mut density = Q::zero();
        let mut prev: Option<Q> = None;
        let mut pending: Option<Segment> = None;
        for (x, change) in events {
            if let Some(lo) = prev {
                if !density.is_zero() {
                    let (a, b) = if vert {
                        ([pos.clone(), lo.clone()], [pos.clone(), x.clone()])
                    } else {
                        ([lo.clone(), pos.clone()], [x.clone(), pos.clone()])
                    };
                    if let Some(s) = pending.as_mut() {
                        if s.b == a && s.density() == density {
                            s.b = b;
                            s.mass += &density * (&x - &lo);
                        } else {
                            out.push(pending.take().unwrap());
                            pending = Some(Segment {
                                a,
                                b,
                                mass: &density * (&x - &lo),
                            });
                        }
                    } else {
                        pending = Some(Segment {
                            a,
                            b,
                            mass: &density * (&x - &lo),
                        });
                    }
                } else if let Some(s) = pending.take() {
                    out.push(s);
                }
            }
            density += change;
            prev = Some(x);
        }
        if let Some(s) = pending {
            out.push(s);
        }
    }
    out
}
fn subtract(a: &[Segment], b: &[Segment]) -> Result<Vec<Segment>> {
    let mut ss = a.to_vec();
    ss.extend(b.iter().cloned().map(|mut s| {
        s.mass = -s.mass;
        s
    }));
    let out = canonical(&ss);
    require(
        out.iter().all(|s| s.mass > Q::zero()),
        "wall subtraction produces a negative corner measure",
    )?;
    Ok(out)
}
fn crop(ss: &[Segment], cap: &Q) -> Vec<Segment> {
    let mut out = vec![];
    for s in ss {
        let vertical = s.vertical();
        let j = if vertical { 1 } else { 0 };
        if s.a[1 - j] < Q::zero() || s.a[1 - j] > *cap {
            continue;
        }
        let lo = s.a[j].clone().min(s.b[j].clone()).max(Q::zero());
        let hi = s.a[j].clone().max(s.b[j].clone()).min(cap.clone());
        if lo < hi {
            let mut z = s.clone();
            z.a[j] = lo.clone();
            z.b[j] = hi.clone();
            z.mass = s.density() * (hi - lo);
            out.push(z);
        }
    }
    canonical(&out)
}
fn grid(x: &Q) -> bool {
    (x * int(5)).is_integer()
}
pub fn structure(f: &Family) -> Result<(Vec<Segment>, Vec<Segment>, Vec<Segment>, Q)> {
    require(
        f.u.is_none(),
        "global family assembly requires standard U (custom U relation unspecified)",
    )?;
    let mut period = vec![];
    for s in &f.t {
        let lo = s.a[0].clone().min(s.b[0].clone());
        let hi = s.a[0].clone().max(s.b[0].clone());
        if (s.vertical() && lo >= int(3) && lo < int(4))
            || (!s.vertical() && lo >= int(3) && hi <= int(4))
        {
            period.push(s.shift(&int(-3)));
        }
    }
    let period = canonical(&period);
    require(
        period.iter().map(|s| s.mass.clone()).sum::<Q>() == q(9, 5),
        "wall period mass is not 9/5",
    )?;
    for s in &period {
        require(
            s.a.iter().chain(s.b.iter()).all(grid),
            "wall piece is not on the 1/5 grid",
        )?;
        let xmin = s.a[0].clone().min(s.b[0].clone());
        let xmax = s.a[0].clone().max(s.b[0].clone());
        let ymin = s.a[1].clone().min(s.b[1].clone());
        let ymax = s.a[1].clone().max(s.b[1].clone());
        require(
            xmin >= Q::zero() && xmax <= Q::one() && ymin >= Q::zero() && ymax <= q(9, 5),
            "wall support outside model",
        )?;
        require(
            if s.vertical() {
                xmax < Q::one()
            } else {
                ymin >= q(1, 5)
            },
            "wall phase or horizontal height invalid",
        )?;
    }
    let reflected: Vec<_> = period
        .iter()
        .map(|s| {
            let mut z = s.clone();
            if s.vertical() && s.a[0].is_zero() {
                return z;
            }
            z.a[0] = int(1) - &s.a[0];
            z.b[0] = int(1) - &s.b[0];
            z
        })
        .collect();
    require(
        canonical(&reflected) == period,
        "wall reversal identities fail",
    )?;
    let terminal: Vec<_> = period
        .iter()
        .filter(|s| s.vertical() && s.a[0].is_zero())
        .cloned()
        .collect();
    let mv = terminal.iter().map(|s| s.mass.clone()).sum();
    // The supported export shape has whole periods from 2 through its common integral endpoint.
    let tx =
        f.t.iter()
            .flat_map(|s| [s.a[0].clone(), s.b[0].clone()])
            .max()
            .ok_or_else(|| refuse("no T wall"))?;
    let fy =
        f.f.iter()
            .flat_map(|s| [s.a[1].clone(), s.b[1].clone()])
            .max()
            .ok_or_else(|| refuse("no F wall"))?;
    require(
        tx == fy && tx.is_integer(),
        "local walls must have a common integral endpoint",
    )?;
    let end = tx
        .to_integer()
        .to_i64()
        .ok_or_else(|| refuse("wall extent too large"))?;
    require((6..=100).contains(&end), "unsupported local wall extent")?;
    let mut bottom = vec![];
    for n in 2..end {
        bottom.extend(period.iter().map(|s| s.shift(&int(n))));
    }
    let left: Vec<_> = bottom.iter().map(Segment::transpose).collect();
    let cf = subtract(&f.f, &left)?;
    let ct = subtract(&f.t, &bottom)?;
    for s in &cf {
        for p in [&s.a, &s.b] {
            require(
                p[0] >= Q::zero() && p[0] <= int(2) + &f.d0 && p[1] >= Q::zero() && p[1] <= int(2),
                "fixed corner support outside corner rectangle",
            )?;
        }
    }
    for s in &ct {
        require(
            s.vertical() && s.a[0] == int(2),
            "translated corner must be the x=2 boundary line",
        )?;
        require(
            s.a[1] >= Q::zero() && s.a[1] <= int(2) && s.b[1] >= Q::zero() && s.b[1] <= int(2),
            "translated corner outside vertical extent",
        )?;
    }
    for v in &f.v {
        require(
            v.xl >= Q::zero() && v.y >= Q::zero() && v.y <= int(2),
            "variable corner support outside rectangle",
        )?;
    }
    Ok((period, cf, ct, mv))
}
pub fn check_pair(f: &Family, right: &Family, entry: &Value) -> Result<Value> {
    require(
        f.d0 == value(&entry["d0"])? && f.d1 == value(&entry["d1"])?,
        "family endpoints disagree with interval",
    )?;
    require(
        right.f == f.t && right.t.is_empty() && right.v.is_empty(),
        "right-side rows do not match original T row for row",
    )?;
    require(
        right.d0 == f.d0 && right.d1 == f.d1 && right.ua == f.ua,
        "right-side metadata mismatch",
    )?;
    require(
        right.u.is_none(),
        "right-side custom U inclusion is unsupported",
    )?;
    let (period, cf, ct, mv) = structure(f)?;
    let fixed = cf
        .iter()
        .chain(ct.iter())
        .map(|s| s.mass.clone())
        .sum::<Q>();
    let mut savings = vec![];
    for (d, key) in [(&f.d0, "S_d0"), (&f.d1, "S_d1")] {
        let mc = &fixed + f.v.iter().map(|v| &v.rho * (int(2) + d - &v.xl)).sum::<Q>();
        let s = q(99, 25) + q(9, 5) * d - &mc - &mv;
        let stored = value(&f.raw[key])?;
        let line = value(&entry["certified_line"]["alpha"])? * d
            + value(&entry["certified_line"]["beta"])?;
        require(
            s >= stored,
            format!("recomputed {key} is below stored saving"),
        )?;
        require(
            s >= line,
            format!("recomputed {key} is below certified line"),
        )?;
        savings.push(json!({"delta":d.to_string(),"M_C":mc.to_string(),"saving":s.to_string(),"stored_relation":if s==stored{"equal"}else{"greater"}}));
    }
    let terminal: Vec<_> = period
        .iter()
        .filter(|s| s.vertical() && s.a[0].is_zero())
        .cloned()
        .collect();
    for k in [7, 8, 9] {
        for d in [&f.d0, &f.d1] {
            let a = int(k) + d;
            let w = int(2) + d;
            let cap = &a / int(2) + q(7072, 10000);
            require(
                a > int(2) * &w + int(2) * q(7072, 10000),
                "opposing corner interference",
            )?;
            require(cap < &a - &f.ua, "global U truncation reaches local window")?;
            let mut base = cf.clone();
            base.extend(ct.iter().map(|s| s.shift(d)));
            base.extend(f.variables(d));
            for n in 0..k - 4 {
                base.extend(period.iter().map(|s| s.shift(&(&w + int(n)))));
            }
            base.extend(terminal.iter().map(|s| s.shift(&(&w + int(k - 4)))));
            let mut global = vec![];
            for s in base {
                let mut z = s;
                for _ in 0..4 {
                    global.push(z.clone());
                    z.a = [&a - &z.a[1], z.a[0].clone()];
                    z.b = [&a - &z.b[1], z.b[0].clone()];
                }
            }
            let mut local = f.f.clone();
            local.extend(f.t.iter().map(|s| s.shift(d)));
            local.extend(f.variables(d));
            require(
                crop(&global, &cap) == crop(&local, &cap),
                format!("global/local segment measures disagree for k={k}, delta={d}"),
            )?;
        }
    }
    let regions = &entry["regions"];
    let end = q(251, 100) + &f.d1;
    for (name, want, fname) in [
        (
            "left",
            vec![int(0), q(167, 100), int(0), q(19, 5)],
            "family.json",
        ),
        (
            "straddle",
            vec![q(167, 100), end.clone(), int(0), q(272, 100)],
            "family.json",
        ),
        (
            "top",
            vec![q(167, 100), end, q(272, 100), q(19, 5)],
            "family.json",
        ),
        (
            "right",
            vec![q(251, 100), q(19, 5), int(0), q(19, 5)],
            "family_right.json",
        ),
    ] {
        require(
            array(&regions[name]["bounds"], 4)? == want,
            format!("{name} bounds do not tile required local window"),
        )?;
        require(
            regions[name]["family"].as_str() == Some(fname),
            format!("{name} uses wrong family"),
        )?;
    }
    Ok(
        json!({"m_v":mv.to_string(),"M_fixed":fixed.to_string(),"savings":savings,"extra_keys":{"family":f.extra_keys,"family_right":right.extra_keys},"global_local_cases":6}),
    )
}
pub fn run(dir: &Path, intervals: &Path, index: usize, report: &mut Report) -> Result<()> {
    let iv = report.read_json(intervals)?;
    let entry = crate::coverage::rows(&iv)?
        .get(index.wrapping_sub(1))
        .ok_or_else(|| parse_error("interval index outside range"))?;
    require(
        entry["index"].as_u64() == Some(index as u64),
        "interval index field disagrees with selected position",
    )?;
    let f = Family::parse(report.read_json(&dir.join("family.json"))?)?;
    let right = Family::parse(report.read_json(&dir.join("family_right.json"))?)?;
    report.details = check_pair(&f, &right, entry)?;
    Ok(())
}
