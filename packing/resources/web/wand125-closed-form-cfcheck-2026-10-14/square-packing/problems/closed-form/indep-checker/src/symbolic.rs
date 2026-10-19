//! Guarded rational functions over exact real algebraic interval boundaries.
use crate::{
    poly::{Algebraic, Poly},
    rat::{int, midpoint, Q},
    refuse, Result,
};
use num_traits::{One, Zero};
use std::{cmp::Ordering, collections::BTreeSet};
#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub struct RF {
    pub n: Poly,
    pub d: Poly,
}
impl RF {
    pub fn new(n: Poly, d: Poly) -> Self {
        if d.is_zero() {
            return Self { n, d };
        }
        if n.is_zero() {
            return Self::q(Q::zero());
        }
        if d == Poly::one() {
            return Self { n, d };
        }
        let g = if n.degree() == 0 {
            Poly::one()
        } else {
            n.gcd(&d)
        };
        let n = n.exact_div(&g);
        let d = d.exact_div(&g);
        let scale = Q::one() / d.leading();
        Self {
            n: n.scale(&scale),
            d: d.scale(&scale),
        }
    }
    pub fn q(v: Q) -> Self {
        Self {
            n: Poly::constant(v),
            d: Poly::one(),
        }
    }
    pub fn i(v: i64) -> Self {
        Self::q(int(v))
    }
    pub fn u() -> Self {
        Self {
            n: Poly::new(vec![int(0), int(1)]),
            d: Poly::one(),
        }
    }
    pub fn add(&self, b: &Self) -> Self {
        if self.n.is_zero() {
            return b.clone();
        }
        if b.n.is_zero() {
            return self.clone();
        }
        if self.d == b.d {
            let n = self.n.add(&b.n);
            if n.is_zero() {
                Self::i(0)
            } else {
                Self {
                    n,
                    d: self.d.clone(),
                }
            }
        } else {
            let g = self.d.gcd(&b.d);
            let left = b.d.exact_div(&g);
            let right = self.d.exact_div(&g);
            Self::new(self.n.mul(&left).add(&b.n.mul(&right)), self.d.mul(&left))
        }
    }
    pub fn neg(&self) -> Self {
        Self {
            n: self.n.neg(),
            d: self.d.clone(),
        }
    }
    pub fn sub(&self, b: &Self) -> Self {
        self.add(&b.neg())
    }
    pub fn mul(&self, b: &Self) -> Self {
        if self.d == Poly::one() && self.n.degree() == 0 {
            return b.scale(&self.n.eval(&int(0)));
        }
        if b.d == Poly::one() && b.n.degree() == 0 {
            return self.scale(&b.n.eval(&int(0)));
        }
        Self::new(self.n.mul(&b.n), self.d.mul(&b.d))
    }
    pub fn div(&self, b: &Self) -> Self {
        Self::new(self.n.mul(&b.d), self.d.mul(&b.n))
    }
    pub fn scale(&self, b: &Q) -> Self {
        if b.is_zero() {
            Self::i(0)
        } else {
            Self {
                n: self.n.scale(b),
                d: self.d.clone(),
            }
        }
    }
    pub fn canonical(&self) -> Self {
        Self::new(self.n.clone(), self.d.clone())
    }
    pub fn sign_poly(&self) -> Poly {
        self.n.mul(&self.d)
    }
}
#[derive(Clone, Debug)]
pub enum Bound {
    R(Q),
    A(Algebraic),
}
impl Bound {
    pub fn lo(&self) -> Q {
        match self {
            Self::R(q) => q.clone(),
            Self::A(a) => a.lo.clone(),
        }
    }
    pub fn hi(&self) -> Q {
        match self {
            Self::R(q) => q.clone(),
            Self::A(a) => a.hi.clone(),
        }
    }
    pub fn refine(&mut self) {
        if let Self::A(a) = self {
            a.refine();
        }
    }
    pub fn cmp(&self, b: &Self) -> Ordering {
        match (self, b) {
            (Self::R(a), Self::R(b)) => a.cmp(b),
            (Self::A(a), Self::A(b)) => a.compare(b),
            (Self::R(q), Self::A(a)) => {
                let p = Poly::new(vec![-q.clone(), int(1)]);
                Algebraic {
                    polynomial: p,
                    lo: q.clone(),
                    hi: q.clone(),
                }
                .compare(a)
            }
            (Self::A(_), Self::R(_)) => b.cmp(self).reverse(),
        }
    }
}
pub fn sample(a: &Bound, b: &Bound) -> Q {
    let (mut a, mut b) = (a.clone(), b.clone());
    loop {
        if a.hi() < b.lo() {
            return midpoint(&a.hi(), &b.lo());
        }
        a.refine();
        b.refine();
    }
}
pub fn roots(p: &Poly, a: &Bound, b: &Bound) -> Vec<Bound> {
    if p.degree() == 0 {
        return vec![];
    }
    let lo = a.lo();
    let hi = b.hi();
    p.isolate(&lo, &hi)
        .into_iter()
        .map(Bound::A)
        .filter(|r| r.cmp(a).is_gt() && r.cmp(b).is_lt())
        .collect()
}
pub fn nonneg(p: &Poly, a: &Bound, b: &Bound) -> bool {
    if p.is_zero() {
        return true;
    }
    let odd = p
        .square_free()
        .into_iter()
        .filter(|(_, m)| m % 2 == 1)
        .fold(Poly::one(), |p, (q, _)| p.mul(&q));
    if !roots(&odd, a, b).is_empty() {
        return false;
    }
    let mut x = sample(a, b);
    for _ in 0..=p.degree() {
        let y = p.eval_sign(&x);
        if y != 0 {
            return y > 0;
        }
        x = sample(&Bound::R(x), b);
    }
    false
}
#[derive(Clone, Debug)]
pub enum EvalError {
    Resample,
    Invalid(String),
}
pub type EResult<T> = std::result::Result<T, EvalError>;
pub struct Eval {
    pub sample: Q,
    pub guards: BTreeSet<Vec<num_bigint::BigInt>>,
}
impl Eval {
    pub fn new(sample: Q) -> Self {
        Self {
            sample,
            guards: BTreeSet::new(),
        }
    }
    pub fn sign(&mut self, r: &RF) -> EResult<i8> {
        let key = (r.clone(), self.sample.clone());
        if let Some((sign, guard)) = SIGNS.with(|c| c.borrow().get(&key).cloned()) {
            if let Some(g) = guard {
                self.guards.insert(g);
            }
            return sign;
        }
        let mut e = Eval::new(self.sample.clone());
        let result = e.sign_uncached(r);
        let guard = e.guards.into_iter().next();
        if let Some(g) = &guard {
            self.guards.insert(g.clone());
        }
        SIGNS.with(|c| {
            c.borrow_mut().insert(key, (result.clone(), guard));
        });
        result
    }
    fn sign_uncached(&mut self, r: &RF) -> EResult<i8> {
        if r.d.is_zero() {
            return Err(EvalError::Invalid(
                "identically zero symbolic denominator".into(),
            ));
        }
        if r.n.is_zero() {
            return Ok(0);
        }
        let p = r.sign_poly();
        let value = p.eval_sign(&self.sample);
        if value == 0 {
            return Err(EvalError::Resample);
        }
        let key = p.coeff.clone();
        crate::profile::update(|s| {
            s.guards.insert(key.clone());
        });
        self.guards.insert(key);
        Ok(value)
    }
    pub fn min(&mut self, a: RF, b: RF) -> EResult<RF> {
        if self.sign(&a.sub(&b))? <= 0 {
            Ok(a)
        } else {
            Ok(b)
        }
    }
    pub fn max(&mut self, a: RF, b: RF) -> EResult<RF> {
        if self.sign(&a.sub(&b))? >= 0 {
            Ok(a)
        } else {
            Ok(b)
        }
    }
}
// The closure must emit every required threshold-subtracted value, and guard every branch.
pub fn prove<F>(u0: &Q, u1: &Q, mut compute: F) -> Result<()>
where
    F: FnMut(&mut Eval) -> EResult<Vec<RF>>,
{
    crate::profile::update(|s| s.prove_calls += 1);
    let _timer = crate::profile::stage("prove");
    let mut pending = vec![(Bound::R(u0.clone()), Bound::R(u1.clone()))];
    let mut components = 0;
    while let Some((a, b)) = pending.pop() {
        components += 1;
        if components >= 2000 {
            return Err(refuse("guard component limit exhausted"));
        }
        let mut s = sample(&a, &b);
        let mut result = None;
        for _ in 0..60 {
            let mut e = Eval::new(s.clone());
            match compute(&mut e) {
                Ok(values) => {
                    result = Some((e, values));
                    break;
                }
                Err(EvalError::Resample) => s = sample(&Bound::R(s), &b),
                Err(EvalError::Invalid(msg)) => return Err(refuse(msg)),
            }
        }
        let (e, values) =
            result.ok_or_else(|| refuse("60 symbolic resampling attempts exhausted"))?;
        let mut l = a.clone();
        let mut r = b.clone();
        let sb = Bound::R(e.sample.clone());
        for c in e.guards {
            for root in roots(&Poly::from_integers(c), &a, &b) {
                if root.cmp(&sb).is_lt() && root.cmp(&l).is_gt() {
                    l = root;
                } else if root.cmp(&sb).is_gt() && root.cmp(&r).is_lt() {
                    r = root;
                }
            }
        }
        for v in values {
            let p = v.sign_poly();
            let valid = if let Some(sign) = p.bernstein_sign(&l.lo(), &r.hi()) {
                sign > 0
            } else {
                nonneg(&p, &l, &r)
            };
            if v.d.is_zero() || !valid {
                return Err(refuse("guarded polynomial value is below threshold"));
            }
        }
        if r.cmp(&b).is_lt() {
            pending.push((r, b));
        }
        if a.cmp(&l).is_lt() {
            pending.push((a, l));
        }
    }
    Ok(())
}
pub type RP = [RF; 2];
pub fn point(p: &crate::geom::Point) -> RP {
    [RF::q(p[0].clone()), RF::q(p[1].clone())]
}
pub fn dot(a: &RP, b: &RP) -> RF {
    a[0].mul(&b[0]).add(&a[1].mul(&b[1]))
}
pub fn sub(a: &RP, b: &RP) -> RP {
    [a[0].sub(&b[0]), a[1].sub(&b[1])]
}
pub fn normals() -> [RP; 4] {
    static NORMALS: std::sync::OnceLock<[RP; 4]> = std::sync::OnceLock::new();
    NORMALS
        .get_or_init(|| {
            let u = RF::u();
            let u2 = u.mul(&u);
            let d = RF::i(1).add(&u2);
            let c = RF::i(1).sub(&u2).div(&d);
            let s = u.scale(&int(2)).div(&d);
            [
                [c.clone(), s.clone()],
                [s.neg(), c.clone()],
                [c.neg(), s.neg()],
                [s, c.neg()],
            ]
        })
        .clone()
}
pub fn vertices() -> [RP; 4] {
    let n = normals();
    std::array::from_fn(|i| {
        [
            n[i][0].add(&n[(i + 1) % 4][0]).scale(&crate::rat::q(1, 2)),
            n[i][1].add(&n[(i + 1) % 4][1]).scale(&crate::rat::q(1, 2)),
        ]
    })
}
pub fn clip(p: &[RP], n: &RP, b: &RF, e: &mut Eval) -> EResult<Vec<RP>> {
    let mut out = vec![];
    if p.is_empty() {
        return Ok(out);
    }
    for i in 0..p.len() {
        let a = &p[i];
        let c = &p[(i + 1) % p.len()];
        let fa = dot(n, a).sub(b);
        let fc = dot(n, c).sub(b);
        let sa = e.sign(&fa)?;
        let sc = e.sign(&fc)?;
        if sa <= 0 {
            out.push(a.clone());
        }
        if sa * sc < 0 {
            let t = fa.div(&fa.sub(&fc));
            out.push([
                a[0].add(&t.mul(&c[0].sub(&a[0]))),
                a[1].add(&t.mul(&c[1].sub(&a[1]))),
            ]);
        }
    }
    Ok(out)
}
pub fn area(p: &[RP]) -> RF {
    if p.len() < 3 {
        return RF::i(0);
    }
    let mut a = RF::i(0);
    for i in 0..p.len() {
        let j = (i + 1) % p.len();
        a = a.add(&p[i][0].mul(&p[j][1]).sub(&p[i][1].mul(&p[j][0])));
    }
    a.scale(&crate::rat::q(1, 2))
}
pub fn square_area(poly: &crate::geom::Polygon, center: &RP, e: &mut Eval) -> EResult<RF> {
    let key = (poly.clone(), center.clone(), e.sample.clone());
    if let Some((v, guards)) = AREAS.with(|c| c.borrow().get(&key).cloned()) {
        e.guards.extend(guards);
        return v;
    }
    let mut local = Eval::new(e.sample.clone());
    let v = square_area_uncached(poly, center, &mut local);
    e.guards.extend(local.guards.iter().cloned());
    AREAS.with(|c| {
        c.borrow_mut().insert(key, (v.clone(), local.guards));
    });
    v
}
fn square_area_uncached(poly: &crate::geom::Polygon, center: &RP, e: &mut Eval) -> EResult<RF> {
    let mut p: Vec<_> = poly.iter().map(point).collect();
    for n in normals() {
        p = clip(&p, &n, &RF::q(crate::rat::q(1, 2)).add(&dot(&n, center)), e)?;
    }
    Ok(area(&p))
}
pub fn width(a: &RP, b: &RP, center: &RP, e: &mut Eval) -> EResult<Option<RF>> {
    let key = ([a.clone(), b.clone(), center.clone()], e.sample.clone());
    if let Some((v, guards)) = WIDTHS.with(|c| c.borrow().get(&key).cloned()) {
        e.guards.extend(guards);
        return v;
    }
    let mut local = Eval::new(e.sample.clone());
    let v = width_uncached(a, b, center, &mut local);
    e.guards.extend(local.guards.iter().cloned());
    WIDTHS.with(|c| {
        c.borrow_mut().insert(key, (v.clone(), local.guards));
    });
    v
}
// Pure symbolic projections are independent of clipping branches and samples.
// Exact point keys allow all CORE1 corners and arrangement vertices to share them.
fn projections(p: &RP) -> [RF; 4] {
    PROJECTIONS.with(|cache| {
        let mut cache = cache.borrow_mut();
        cache
            .entry(p.clone())
            .or_insert_with(|| {
                let ns = normals();
                std::array::from_fn(|i| dot(&ns[i], p))
            })
            .clone()
    })
}
fn width_uncached(a: &RP, b: &RP, center: &RP, e: &mut Eval) -> EResult<Option<RF>> {
    let mut lo = RF::i(0);
    let mut hi = RF::i(1);
    let pa = projections(a);
    let pb = projections(b);
    let pc = projections(center);
    for i in 0..4 {
        let num = RF::q(crate::rat::q(1, 2)).sub(&pa[i]).add(&pc[i]);
        let den = pb[i].sub(&pa[i]);
        match e.sign(&den)? {
            1 => hi = e.min(hi, num.div(&den))?,
            -1 => lo = e.max(lo, num.div(&den))?,
            _ => {
                if e.sign(&num)? < 0 {
                    return Ok(None);
                }
            }
        }
    }
    Ok(Some(hi.sub(&lo)))
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn shared_projections_preserve_clipping() {
        // Compare to the original direct dot-product clipping on varying exact
        // segments, centers, and samples, including unavailable/negative widths.
        for k in 0..40 {
            let a = point(&[crate::rat::q(k - 20, 7), crate::rat::q(k % 5, 3)]);
            let b = point(&[crate::rat::q(k - 10, 7), crate::rat::q(k % 5, 3)]);
            let center = [RF::u().add(&RF::i(1)), RF::q(crate::rat::q(k % 7, 4))];
            let sample = crate::rat::q(k + 1, 100);
            let mut old = Eval::new(sample.clone());
            let direct = (|| -> EResult<Option<RF>> {
                let mut lo = RF::i(0);
                let mut hi = RF::i(1);
                let delta = sub(&b, &a);
                for n in normals() {
                    let num = RF::q(crate::rat::q(1, 2)).sub(&dot(&n, &sub(&a, &center)));
                    let den = dot(&n, &delta);
                    match old.sign(&den)? {
                        1 => hi = old.min(hi, num.div(&den))?,
                        -1 => lo = old.max(lo, num.div(&den))?,
                        _ => {
                            if old.sign(&num)? < 0 {
                                return Ok(None);
                            }
                        }
                    }
                }
                Ok(Some(hi.sub(&lo)))
            })();
            let mut new = Eval::new(sample);
            let cached = width_uncached(&a, &b, &center, &mut new);
            match (direct, cached) {
                (Ok(a), Ok(b)) => assert_eq!(a.map(|v| v.canonical()), b.map(|v| v.canonical())),
                (Err(EvalError::Resample), Err(EvalError::Resample)) => {}
                _ => panic!("clipping outcome changed"),
            }
            assert_eq!(old.guards, new.guards);
        }
        clear_caches();
    }
    #[test]
    fn guarded_split() {
        let r = prove(&int(-1), &int(1), |e| {
            let u = RF::u();
            let v = if e.sign(&u)? < 0 { u.neg() } else { u };
            Ok(vec![v])
        });
        assert!(r.is_ok());
    }
    #[test]
    fn negative_even_square() {
        assert!(prove(&int(-1), &int(1), |_| Ok(vec![RF::u().mul(&RF::u()).neg()])).is_err());
    }
    #[test]
    fn denominator_sign() {
        let r = RF::i(-1).div(&RF::u());
        assert!(prove(&int(-2), &int(-1), |_| Ok(vec![r.clone()])).is_ok());
    }
}
/// The specified B4U frontier/cap discipline, including its asymmetric run limits.
pub fn prove_frontier<F>(u0: &Q, u1: &Q, mut compute: F) -> Result<()>
where
    F: FnMut(&mut Eval) -> EResult<Vec<RF>>,
{
    let start = Bound::R(u0.clone());
    let end = Bound::R(u1.clone());
    let mut frontier = start.clone();
    let mut cap = u1.clone();
    let mut runs = 0usize;
    let mut attempts = 0usize;
    while frontier.cmp(&end).is_lt() {
        while frontier.hi() >= cap {
            frontier.refine();
        }
        let lo = frontier.hi();
        let mut s = midpoint(&lo, &cap);
        let mut found = None;
        while attempts < 60 {
            attempts += 1;
            let mut e = Eval::new(s.clone());
            match compute(&mut e) {
                Ok(v) => {
                    found = Some((e, v));
                    break;
                }
                Err(EvalError::Resample) => s = &lo + (&s - &lo) * crate::rat::q(2, 3),
                Err(EvalError::Invalid(m)) => return Err(refuse(m)),
            }
        }
        let (e, values) = found.ok_or_else(|| refuse("B4U 60-attempt sampling limit exhausted"))?;
        let sb = Bound::R(e.sample);
        let mut l = start.clone();
        let mut r = end.clone();
        for c in e.guards {
            for root in roots(&Poly::from_integers(c), &start, &end) {
                if root.cmp(&sb).is_lt() && root.cmp(&l).is_gt() {
                    l = root;
                } else if root.cmp(&sb).is_gt() && root.cmp(&r).is_lt() {
                    r = root;
                }
            }
        }
        if l.cmp(&frontier).is_gt() {
            if runs + 1 >= 2000 {
                return Err(refuse("B4U cap-reduction run limit exhausted"));
            }
            while l.lo() <= frontier.hi() {
                l.refine();
                frontier.refine();
            }
            cap = l.lo();
            continue;
        }
        for v in values {
            if v.d.is_zero() || !nonneg(&v.sign_poly(), &l, &r) {
                return Err(refuse("B4U edge critical value below 1"));
            }
        }
        frontier = r;
        runs += 1;
        if runs >= 2000 {
            return Err(refuse("B4U completed-component limit exhausted"));
        }
        cap = u1.clone();
        attempts = 0;
    }
    if frontier.cmp(&end).is_eq() {
        Ok(())
    } else {
        Err(refuse("B4U frontier did not reach upper endpoint"))
    }
}

// These caches store the full branch guards, not just numerical answers. A hit
// must merge the guards into the current Eval before the caller uses its value.
// Geometry keys include the exact sample; all caches are cleared per leaf.
type SignCache = std::collections::HashMap<(RF, Q), (EResult<i8>, Option<Vec<num_bigint::BigInt>>)>;
type WidthCache = std::collections::HashMap<
    ([RP; 3], Q),
    (EResult<Option<RF>>, BTreeSet<Vec<num_bigint::BigInt>>),
>;
type AreaCache = std::collections::HashMap<
    (crate::geom::Polygon, RP, Q),
    (EResult<RF>, BTreeSet<Vec<num_bigint::BigInt>>),
>;
thread_local! {
    static PROJECTIONS: std::cell::RefCell<std::collections::HashMap<RP, [RF; 4]>> = std::cell::RefCell::new(std::collections::HashMap::new());
    static AREAS: std::cell::RefCell<AreaCache> = std::cell::RefCell::new(std::collections::HashMap::new());
    static SIGNS: std::cell::RefCell<SignCache> = std::cell::RefCell::new(std::collections::HashMap::new());
    static WIDTHS: std::cell::RefCell<WidthCache> = std::cell::RefCell::new(std::collections::HashMap::new());
}
pub fn clear_caches() {
    PROJECTIONS.with(|c| c.borrow_mut().clear());
    AREAS.with(|c| c.borrow_mut().clear());
    SIGNS.with(|c| c.borrow_mut().clear());
    WIDTHS.with(|c| c.borrow_mut().clear());
}
