//! Dense univariate polynomials, exact Euclidean arithmetic, and Sturm isolation.
type Q = num_rational::BigRational;
fn midpoint(a: &Q, b: &Q) -> Q {
    (a + b) / Q::from_integer(2.into())
}
use num_traits::{One, Signed, Zero};
#[derive(Clone, Debug, PartialEq, Eq, Hash)]
pub struct Poly(pub Vec<Q>);
impl Poly {
    pub fn new(mut c: Vec<Q>) -> Self {
        while c.last().is_some_and(Zero::is_zero) {
            c.pop();
        }
        Self(c)
    }
    pub fn zero() -> Self {
        Self(vec![])
    }
    pub fn one() -> Self {
        Self(vec![Q::one()])
    }
    pub fn constant(q: Q) -> Self {
        Self::new(vec![q])
    }
    pub fn is_zero(&self) -> bool {
        self.0.is_empty()
    }
    pub fn degree(&self) -> usize {
        self.0.len().saturating_sub(1)
    }
    pub fn eval(&self, x: &Q) -> Q {
        self.0.iter().rev().fold(Q::zero(), |a, c| a * x + c)
    }
    pub fn add(&self, b: &Self) -> Self {
        let mut out = self.0.clone();
        out.resize(out.len().max(b.0.len()), Q::zero());
        for (i, c) in b.0.iter().enumerate() {
            out[i] += c;
        }
        Self::new(out)
    }
    pub fn neg(&self) -> Self {
        Self::new(self.0.iter().map(|x| -x).collect())
    }
    pub fn sub(&self, b: &Self) -> Self {
        self.add(&b.neg())
    }
    pub fn scale(&self, c: &Q) -> Self {
        Self::new(self.0.iter().map(|x| x * c).collect())
    }
    pub fn mul(&self, b: &Self) -> Self {
        if self.is_zero() || b.is_zero() {
            return Self::zero();
        }
        let mut out = vec![Q::zero(); self.degree() + b.degree() + 1];
        for (i, a) in self.0.iter().enumerate() {
            for (j, b) in b.0.iter().enumerate() {
                out[i + j] += a * b;
            }
        }
        Self::new(out)
    }
    pub fn derivative(&self) -> Self {
        Self::new(
            self.0
                .iter()
                .enumerate()
                .skip(1)
                .map(|(i, x)| x * Q::from_integer(i.into()))
                .collect(),
        )
    }
    pub fn div_rem(&self, b: &Self) -> (Self, Self) {
        assert!(!b.is_zero());
        let mut r = self.clone();
        let mut q = vec![Q::zero(); self.0.len()];
        while !r.is_zero() && r.degree() >= b.degree() {
            let i = r.degree() - b.degree();
            let c = r.0.last().unwrap() / b.0.last().unwrap();
            q[i] = c.clone();
            for (j, x) in b.0.iter().enumerate() {
                r.0[i + j] -= &c * x;
            }
            r = Self::new(r.0);
        }
        (Self::new(q), r)
    }
    pub fn exact_div(&self, b: &Self) -> Self {
        let (q, r) = self.div_rem(b);
        assert!(r.is_zero());
        q
    }
    pub fn monic(&self) -> Self {
        if self.is_zero() {
            self.clone()
        } else {
            self.scale(&(Q::one() / self.0.last().unwrap()))
        }
    }
    pub fn gcd(&self, b: &Self) -> Self {
        let (mut a, mut b) = (self.clone(), b.clone());
        while !b.is_zero() {
            let r = a.div_rem(&b).1;
            a = b;
            b = r;
        }
        a.monic()
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
        let f = self.radical();
        let mut seq = vec![f.clone()];
        if f.degree() == 0 {
            return seq;
        }
        seq.push(f.derivative());
        loop {
            let n = seq.len();
            let next = seq[n - 2].div_rem(&seq[n - 1]).1.neg();
            if next.is_zero() {
                break;
            } // Positive normalization controls coefficient growth without changing signs.
            let next = next.scale(&(Q::one() / next.0.last().unwrap().abs()));
            seq.push(next);
        }
        seq
    }
    fn side_sign(&self, x: &Q, right: bool) -> i8 {
        let mut p = self.clone();
        let mut parity = false;
        loop {
            let v = p.eval(x);
            if !v.is_zero() {
                let s = if v.is_positive() { 1 } else { -1 };
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
            let v = self.eval(&x);
            if !v.is_zero() {
                return v > Q::zero();
            }
        }
        false
    }
    /// A strictly signed Bernstein expansion proves the open interval root-free.
    pub fn bernstein_sign(&self, a: &Q, b: &Q) -> Option<i8> {
        if self.is_zero() {
            return None;
        }
        let n = self.degree();
        let linear = Self::new(vec![a.clone(), b - a]);
        let mut shifted = Self::zero();
        for c in self.0.iter().rev() {
            shifted = shifted.mul(&linear).add(&Self::constant(c.clone()));
        }
        let mut positive = true;
        let mut negative = true;
        let mut nonzero = false;
        for j in 0..=n {
            let mut ratio = Q::one();
            let mut coefficient = Q::zero();
            for i in 0..=j {
                if i < shifted.0.len() {
                    coefficient += &shifted.0[i] * &ratio;
                }
                if i < j {
                    ratio *= Q::new((j - i).into(), (n - i).into());
                }
            }
            positive &= coefficient >= Q::zero();
            negative &= coefficient <= Q::zero();
            nonzero |= !coefficient.is_zero();
            if !positive && !negative {
                return None;
            }
        }
        if nonzero && positive {
            Some(1)
        } else if nonzero && negative {
            Some(-1)
        } else {
            None
        }
    }
    pub fn isolate(&self, a: &Q, b: &Q) -> Vec<Algebraic> {
        let f = self.radical();
        let mut work = vec![(a.clone(), b.clone())];
        let mut out = vec![];
        while let Some((lo, hi)) = work.pop() {
            let n = f.roots_open(&lo, &hi);
            if n == 0 {
                continue;
            }
            if n == 1 && !f.eval(&lo).is_zero() && !f.eval(&hi).is_zero() {
                out.push(Algebraic {
                    polynomial: f.clone(),
                    lo,
                    hi,
                });
                continue;
            }
            let m = midpoint(&lo, &hi);
            if f.eval(&m).is_zero() {
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
        if self.polynomial.eval(&m).is_zero() {
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
            if a.lo == a.hi && b.polynomial.eval(&a.lo).is_zero() {
                return Equal;
            }
            if b.lo == b.hi && a.polynomial.eval(&b.lo).is_zero() {
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
    fn int(n: i64) -> Q {
        Q::from_integer(n.into())
    }
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
