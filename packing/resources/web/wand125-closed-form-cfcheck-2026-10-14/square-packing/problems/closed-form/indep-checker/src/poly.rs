//! Primitive integer polynomials with rational content and exact Sturm isolation.
use crate::rat::{midpoint, Q};
use num_bigint::BigInt;
use num_integer::Integer;
use num_traits::{One, Signed, Zero};
// Nonzero coefficient vectors are primitive with positive leading coefficient.
// All scalar sign and denominator information lives in `content`. This gives
// canonical equality and permits multiplication without coefficient-wise GCDs.
#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub struct Poly {
    pub coeff: Vec<BigInt>,
    pub content: Q,
}
impl Poly {
    pub fn new(c: Vec<Q>) -> Self {
        let den = c.iter().fold(BigInt::one(), |d, c| d.lcm(&c.denom()));
        Self::parts(
            c.iter().map(|c| c.numer() * (&den / c.denom())).collect(),
            Q::new(BigInt::one(), den),
        )
    }
    fn parts(mut coeff: Vec<BigInt>, mut content: Q) -> Self {
        while coeff.last().is_some_and(Zero::is_zero) {
            coeff.pop();
        }
        if coeff.is_empty() || content.is_zero() {
            return Self::zero();
        }
        let mut g = BigInt::zero();
        for c in &coeff {
            g = g.gcd(c);
            // Further coefficients cannot change a content gcd of one.
            if g.is_one() {
                break;
            }
        }
        if coeff.last().unwrap().is_negative() {
            g = -g;
        }
        if !g.is_one() {
            for c in &mut coeff {
                *c /= &g;
            }
            content *= Q::from_integer(g);
        }
        let out = Self { coeff, content };
        out.observe();
        out
    }
    fn observe(&self) {
        crate::profile::update(|s| {
            s.max_degree = s.max_degree.max(self.degree());
            for c in self.coefficients() {
                s.max_coefficient_bits = s
                    .max_coefficient_bits
                    .max(c.numer().bits())
                    .max(c.denom().bits());
            }
        });
    }
    pub fn coefficients(&self) -> Vec<Q> {
        self.coeff
            .iter()
            .map(|c| Q::from_integer(c.clone()) * &self.content)
            .collect()
    }
    pub fn leading(&self) -> Q {
        self.coeff
            .last()
            .map_or_else(Q::zero, |c| Q::from_integer(c.clone()) * &self.content)
    }
    pub fn zero() -> Self {
        Self {
            coeff: vec![],
            content: Q::zero(),
        }
    }
    pub fn one() -> Self {
        Self::constant(Q::one())
    }
    pub fn constant(q: Q) -> Self {
        if q.is_zero() {
            Self::zero()
        } else {
            Self {
                coeff: vec![BigInt::one()],
                content: q,
            }
        }
    }
    pub fn is_zero(&self) -> bool {
        self.coeff.is_empty()
    }
    pub fn degree(&self) -> usize {
        self.coeff.len().saturating_sub(1)
    }
    /// Sign evaluation by homogeneous integer Horner arithmetic; no rational GCD.
    pub fn eval_sign(&self, x: &Q) -> i8 {
        if self.is_zero() {
            return 0;
        }
        let n = x.numer();
        let d = x.denom();
        let mut v = self.coeff.last().unwrap().clone();
        let mut power = BigInt::one();
        for c in self.coeff.iter().rev().skip(1) {
            power *= &d;
            v = v * &n + c * &power;
        }
        let sign = if v.is_zero() {
            0
        } else if v.is_positive() {
            1
        } else {
            -1
        };
        if self.content.is_negative() {
            -sign
        } else {
            sign
        }
    }
    pub fn eval(&self, x: &Q) -> Q {
        if self.is_zero() {
            return Q::zero();
        }
        let n = x.numer();
        let d = x.denom();
        let mut v = self.coeff.last().unwrap().clone();
        let mut power = BigInt::one();
        for c in self.coeff.iter().rev().skip(1) {
            power *= &d;
            v = v * &n + c * &power;
        }
        Q::new(v, power) * &self.content
    }
    pub fn add(&self, b: &Self) -> Self {
        if self.is_zero() {
            return b.clone();
        }
        if b.is_zero() {
            return self.clone();
        }
        if self.content == b.content {
            let mut out = self.coeff.clone();
            out.resize(out.len().max(b.coeff.len()), BigInt::zero());
            for (i, c) in b.coeff.iter().enumerate() {
                out[i] += c;
            }
            return Self::parts(out, self.content.clone());
        }
        let den = self.content.denom().lcm(&b.content.denom());
        let a = self.content.numer() * (&den / self.content.denom());
        let bb = b.content.numer() * (&den / b.content.denom());
        let mut out = vec![BigInt::zero(); self.coeff.len().max(b.coeff.len())];
        for (i, c) in self.coeff.iter().enumerate() {
            out[i] += &a * c;
        }
        for (i, c) in b.coeff.iter().enumerate() {
            out[i] += &bb * c;
        }
        Self::parts(out, Q::new(BigInt::one(), den))
    }
    pub fn neg(&self) -> Self {
        Self {
            coeff: self.coeff.clone(),
            content: -&self.content,
        }
    }
    pub fn sub(&self, b: &Self) -> Self {
        self.add(&b.neg())
    }
    pub fn scale(&self, c: &Q) -> Self {
        if c.is_zero() {
            Self::zero()
        } else {
            Self {
                coeff: self.coeff.clone(),
                content: &self.content * c,
            }
        }
    }
    pub fn mul(&self, b: &Self) -> Self {
        crate::budget::check();
        if self.is_zero() || b.is_zero() {
            return Self::zero();
        }
        let mut coeff = vec![BigInt::zero(); self.degree() + b.degree() + 1];
        for (i, a) in self.coeff.iter().enumerate() {
            for (j, b) in b.coeff.iter().enumerate() {
                coeff[i + j] += a * b;
            }
        }
        // Gauss's lemma: a product of primitive integer polynomials is primitive.
        let out = Self {
            coeff,
            content: &self.content * &b.content,
        };
        out.observe();
        out
    }
    pub fn derivative(&self) -> Self {
        Self::parts(
            self.coeff
                .iter()
                .enumerate()
                .skip(1)
                .map(|(i, c)| c * BigInt::from(i))
                .collect(),
            self.content.clone(),
        )
    }
    pub fn div_rem(&self, b: &Self) -> (Self, Self) {
        assert!(!b.is_zero());
        let mut r = self.coefficients();
        let bs = b.coefficients();
        let mut out = vec![Q::zero(); r.len()];
        while !r.is_empty() && r.len() >= bs.len() {
            crate::budget::check();
            let i = r.len() - bs.len();
            let c = r.last().unwrap() / bs.last().unwrap();
            out[i] = c.clone();
            for (j, x) in bs.iter().enumerate() {
                r[i + j] -= &c * x;
            }
            while r.last().is_some_and(Zero::is_zero) {
                r.pop();
            }
        }
        (Self::new(out), Self::new(r))
    }
    pub fn exact_div(&self, b: &Self) -> Self {
        assert!(!b.is_zero());
        if self.is_zero() {
            return Self::zero();
        }
        let mut r = self.coeff.clone();
        let mut out = vec![BigInt::zero(); r.len()];
        while !r.is_empty() && r.len() >= b.coeff.len() {
            crate::budget::check();
            let i = r.len() - b.coeff.len();
            let (c, rem) = r.last().unwrap().div_rem(b.coeff.last().unwrap());
            assert!(rem.is_zero());
            out[i] = c.clone();
            for (j, x) in b.coeff.iter().enumerate() {
                r[i + j] -= &c * x;
            }
            while r.last().is_some_and(Zero::is_zero) {
                r.pop();
            }
        }
        assert!(r.is_empty());
        Self::parts(out, &self.content / &b.content)
    }
    pub fn monic(&self) -> Self {
        if self.is_zero() {
            self.clone()
        } else {
            self.scale(&(Q::one() / self.leading()))
        }
    }
    pub fn gcd(&self, b: &Self) -> Self {
        let key = if self.coeff <= b.coeff {
            (self.coeff.clone(), b.coeff.clone())
        } else {
            (b.coeff.clone(), self.coeff.clone())
        };
        if let Some(g) = GCD.with(|c| c.borrow().get(&key).cloned()) {
            return g;
        }
        let (mut a, mut b) = (self.integer_key(), b.integer_key());
        while !b.is_empty() {
            let r = integer_rem(a, &b);
            a = b;
            b = r;
        }
        let g = Self::from_integers(a).monic();
        GCD.with(|c| {
            c.borrow_mut().insert(key, g.clone());
        });
        g
    }
    /// Primitive integer coefficients, preserving the polynomial's sign.
    pub fn integer_key(&self) -> Vec<BigInt> {
        if self.content.is_negative() {
            self.coeff.iter().map(|c| -c).collect()
        } else {
            self.coeff.clone()
        }
    }
    pub fn from_integers(c: Vec<BigInt>) -> Self {
        Self::parts(c, Q::one())
    }

    pub fn square_free(&self) -> Vec<(Self, usize)> {
        if self.degree() == 0 {
            return vec![];
        }
        let f = self.monic();
        let mut c = f.gcd(&f.derivative());
        let mut w = f.exact_div(&c);
        let mut i = 1;
        let mut out = vec![];
        while w.degree() > 0 {
            let y = w.gcd(&c);
            let z = w.exact_div(&y);
            if z.degree() > 0 {
                out.push((z, i));
            }
            w = y;
            c = c.exact_div(&w);
            i += 1;
        }
        out
    }
    pub fn radical(&self) -> Self {
        if self.degree() == 0 {
            Self::one()
        } else {
            self.exact_div(&self.gcd(&self.derivative())).monic()
        }
    }
    pub fn sturm(&self) -> Vec<Self> {
        let key = self.integer_key();
        if let Some(seq) = STURM.with(|c| c.borrow().get(&key).cloned()) {
            return seq;
        }
        crate::profile::update(|s| s.sturm_sequences += 1);
        let f = self.radical();
        let mut seq = vec![Self::from_integers(f.integer_key())];
        if f.degree() > 0 {
            seq.push(Self::from_integers(f.derivative().integer_key()));
            loop {
                let n = seq.len();
                let next = integer_rem(seq[n - 2].integer_key(), &seq[n - 1].integer_key());
                if next.is_empty() {
                    break;
                }
                seq.push(Self::from_integers(next.into_iter().map(|x| -x).collect()));
            }
        }
        STURM.with(|c| {
            c.borrow_mut().insert(key, seq.clone());
        });
        seq
    }

    fn side_sign(&self, x: &Q, right: bool) -> i8 {
        let mut p = self.clone();
        let mut parity = false;
        loop {
            let s = p.eval_sign(x);
            if s != 0 {
                return if parity && !right { -s } else { s };
            }
            if p.degree() == 0 {
                return 0;
            }
            p = p.derivative();
            parity = !parity;
        }
    }
    fn variations(seq: &[Self], x: &Q, right: bool) -> usize {
        let mut prev = 0;
        let mut out = 0;
        for p in seq {
            let s = p.side_sign(x, right);
            if s != 0 {
                if prev != 0 && s != prev {
                    out += 1;
                }
                prev = s;
            }
        }
        out
    }
    pub fn roots_open(&self, a: &Q, b: &Q) -> usize {
        assert!(a < b);
        if self.degree() == 0 || self.bernstein_sign(a, b).is_some() {
            return 0;
        }
        let seq = self.sturm();
        Self::variations(&seq, a, true) - Self::variations(&seq, b, false)
    }
    pub fn nonneg_open(&self, a: &Q, b: &Q) -> bool {
        if self.is_zero() {
            return true;
        }
        if let Some(sign) = self.bernstein_sign(a, b) {
            return sign > 0;
        }
        let odd = self
            .square_free()
            .into_iter()
            .filter(|(_, m)| m % 2 == 1)
            .fold(Self::one(), |p, (f, _)| p.mul(&f));
        if odd.roots_open(a, b) > 0 {
            return false;
        }
        // At most degree distinct zeros: degree+1 distinct interior rationals suffice.
        for k in 1..=self.degree() + 1 {
            let x = a + (b - a) / Q::from_integer((k + 1).into());
            let v = self.eval_sign(&x);
            if v != 0 {
                return v > 0;
            }
        }
        false
    }
    /// A strictly signed Bernstein expansion proves the open interval root-free.
    pub fn bernstein_sign(&self, a: &Q, b: &Q) -> Option<i8> {
        if self.is_zero() {
            return None;
        }
        // Transform x=(a+b*t)/(1+t). Its coefficients have the signs of
        // the Bernstein coefficients on [a,b], up to positive binomials.
        // Clear endpoint denominators first; all inner arithmetic is integer.
        let den = a.denom().lcm(&b.denom());
        let aa = a.numer() * (&den / a.denom());
        let bb = b.numer() * (&den / b.denom());
        let n = self.degree();
        let mut power = vec![BigInt::one()];
        let mut shifted = vec![self.coeff[n].clone()];
        let mut dp = BigInt::one();
        for k in (0..n).rev() {
            let mut next = vec![BigInt::zero(); shifted.len() + 1];
            for (i, c) in shifted.iter().enumerate() {
                next[i] += c * &aa;
                next[i + 1] += c * &bb;
            }
            let mut p = vec![BigInt::zero(); power.len() + 1];
            for (i, c) in power.iter().enumerate() {
                p[i] += c;
                p[i + 1] += c;
            }
            power = p;
            dp *= &den;
            for (i, c) in power.iter().enumerate() {
                next[i] += c * &self.coeff[k] * &dp;
            }
            shifted = next;
        }
        let positive = shifted.iter().all(|c| !c.is_negative());
        let negative = shifted.iter().all(|c| !c.is_positive());
        let sign = if positive && !negative {
            1
        } else if negative && !positive {
            -1
        } else {
            return None;
        };
        Some(if self.content.is_negative() {
            -sign
        } else {
            sign
        })
    }
    pub fn isolate(&self, a: &Q, b: &Q) -> Vec<Algebraic> {
        if self.degree() == 0 {
            return vec![];
        }
        let key = (self.integer_key(), a.clone(), b.clone());
        if let Some(roots) = ISOLATED.with(|c| c.borrow().get(&key).cloned()) {
            return roots;
        }
        let roots = if self.bernstein_sign(a, b).is_some() {
            vec![]
        } else {
            self.isolate_uncached(a, b)
        };
        ISOLATED.with(|c| {
            c.borrow_mut().insert(key, roots.clone());
        });
        roots
    }
    fn isolate_uncached(&self, a: &Q, b: &Q) -> Vec<Algebraic> {
        let f = self.radical();
        let mut work = vec![(a.clone(), b.clone())];
        let mut out = vec![];
        while let Some((lo, hi)) = work.pop() {
            let n = f.roots_open(&lo, &hi);
            if n == 0 {
                continue;
            }
            if n == 1 && f.eval_sign(&lo) != 0 && f.eval_sign(&hi) != 0 {
                out.push(Algebraic {
                    polynomial: f.clone(),
                    lo,
                    hi,
                });
                continue;
            }
            let m = midpoint(&lo, &hi);
            if f.eval_sign(&m) == 0 {
                out.push(Algebraic {
                    polynomial: f.clone(),
                    lo: m.clone(),
                    hi: m.clone(),
                });
            }
            work.push((m.clone(), hi));
            work.push((lo, m));
        }
        out.sort_by(|a, b| a.compare(b));
        out
    }
}
#[derive(Clone, Debug)]
pub struct Algebraic {
    pub polynomial: Poly,
    pub lo: Q,
    pub hi: Q,
}
impl Algebraic {
    pub fn refine(&mut self) {
        if self.lo == self.hi {
            return;
        }
        let m = midpoint(&self.lo, &self.hi);
        if self.polynomial.eval_sign(&m) == 0 {
            self.lo = m.clone();
            self.hi = m;
        } else if self.polynomial.roots_open(&self.lo, &m) > 0 {
            self.hi = m;
        } else {
            self.lo = m;
        }
    }
    pub fn compare(&self, b: &Self) -> std::cmp::Ordering {
        use std::cmp::Ordering::*;
        let (mut a, mut b) = (self.clone(), b.clone());
        let gcd = a.polynomial.gcd(&b.polynomial);
        loop {
            if a.hi < b.lo {
                return Less;
            }
            if b.hi < a.lo {
                return Greater;
            }
            if a.lo == a.hi && b.lo == b.hi {
                return a.lo.cmp(&b.lo);
            }
            let lo = a.lo.clone().max(b.lo.clone());
            let hi = a.hi.clone().min(b.hi.clone());
            if lo < hi && gcd.roots_open(&lo, &hi) > 0 {
                return Equal;
            }
            if a.lo == a.hi && b.polynomial.eval_sign(&a.lo) == 0 {
                return Equal;
            }
            if b.lo == b.hi && a.polynomial.eval_sign(&b.lo) == 0 {
                return Equal;
            }
            a.refine();
            b.refine();
        }
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    use crate::rat::int;
    fn x() -> Poly {
        Poly::new(vec![int(0), int(1)])
    }
    #[test]
    fn gcd_and_multiplicity() {
        let p = x().sub(&Poly::one());
        let f = p.mul(&p).mul(&x().add(&Poly::one()));
        assert_eq!(f.gcd(&f.derivative()), p);
        assert_eq!(
            f.square_free().iter().map(|(_, m)| *m).collect::<Vec<_>>(),
            vec![1, 2]
        );
        assert_eq!(f.roots_open(&int(-2), &int(2)), 2);
        assert_eq!(f.roots_open(&int(-1), &int(1)), 0);
    }
    #[test]
    fn even_root_sign() {
        let p = x().mul(&x()).neg();
        assert!(!p.nonneg_open(&int(-1), &int(1)));
        assert!(!p.nonneg_open(&int(0), &int(1)));
        assert!(p.neg().nonneg_open(&int(-1), &int(1)));
    }
    #[test]
    fn isolate_and_equality() {
        let f = x().mul(&x()).sub(&Poly::constant(int(2)));
        let rs = f.isolate(&int(-2), &int(2));
        assert_eq!(rs.len(), 2);
        assert!(rs[0].compare(&rs[1]).is_lt());
        let g = f.mul(&x().sub(&Poly::constant(int(3))));
        let r = g.isolate(&int(1), &int(2));
        assert!(rs[1].compare(&r[0]).is_eq());
    }
}

// Positive content normalization preserves every Sturm sign. At each elimination
// step abs(lc) is positive; hence this pseudo-remainder is a positive multiple
// of the ordinary rational remainder, including when lc is negative.
fn primitive(mut a: Vec<BigInt>) -> Vec<BigInt> {
    while a.last().is_some_and(Zero::is_zero) {
        a.pop();
    }
    let g = a.iter().fold(BigInt::zero(), |g, c| g.gcd(c));
    if !g.is_zero() && !g.is_one() {
        for c in &mut a {
            *c /= &g;
        }
    }
    a
}
fn integer_rem(mut a: Vec<BigInt>, b: &[BigInt]) -> Vec<BigInt> {
    assert!(!b.is_empty());
    while !a.is_empty() && a.len() >= b.len() {
        crate::budget::check();
        let shift = a.len() - b.len();
        let lc = b.last().unwrap();
        let top = a.last().unwrap().clone() * lc.signum();
        let scale = lc.abs();
        for c in &mut a {
            *c *= &scale;
        }
        for (i, c) in b.iter().enumerate() {
            a[i + shift] -= &top * c;
        }
        a = primitive(a);
    }
    a
}
thread_local! {
    static GCD: std::cell::RefCell<std::collections::HashMap<(Vec<BigInt>,Vec<BigInt>),Poly>> = std::cell::RefCell::new(std::collections::HashMap::new());
    static STURM: std::cell::RefCell<std::collections::HashMap<Vec<BigInt>,Vec<Poly>>> = std::cell::RefCell::new(std::collections::HashMap::new());
    static ISOLATED: std::cell::RefCell<std::collections::HashMap<(Vec<BigInt>,Q,Q),Vec<Algebraic>>> = std::cell::RefCell::new(std::collections::HashMap::new());
}
pub fn clear_caches() {
    GCD.with(|c| c.borrow_mut().clear());
    STURM.with(|c| c.borrow_mut().clear());
    ISOLATED.with(|c| c.borrow_mut().clear());
}
