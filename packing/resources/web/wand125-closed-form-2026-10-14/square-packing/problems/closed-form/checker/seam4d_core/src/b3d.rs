//! Rust implementation of stage B (certify3).
//!
//! Mirrors the Python reference implementation of certify3, check_value3, mass3 and their helpers:
//! RF, Ctx, Resample, squarefree, sturm, count_roots, isolate, roots_open;
//! Alg, alg_cmp, strip0, root_free, rf_const, sign_poly, roots_in, sorted_unique;
//! between, nonneg_open, roots_in_alg, frame, point_mass, Local.
//! Each function mirrors its Python counterpart. All arithmetic uses exact GMP rationals, without floating point.
//!
//! Polynomial P uses flint's fmpq_poly representation: integer coefficients and a positive common denominator,
//! reduced with no trailing zeros. This canonical form makes == structural. Rational functions RF use Python's
//! reduction rules (divide by the gcd and make the denominator monic), yielding identical (n, d) pairs.
//! Alg uses Rc<RefCell<..>> to mirror Python's shared objects and in-place refinement.

use rug::ops::NegAssign;
use rug::{Integer, Rational};
use std::cell::RefCell;
use std::cmp::Ordering;
use std::collections::{HashMap, HashSet};
use std::rc::Rc;

pub type Q = Rational;
pub type Pt = (Q, Q);

/// Python exception mappings: Resample to rf.Resample, ZeroDiv to ZeroDivisionError, Assert to AssertionError,
/// and Runtime to RuntimeError.
#[derive(Debug, Clone)]
pub enum BErr {
    Resample,
    ZeroDiv,
    Assert(String),
    Runtime(String),
}
type R<T> = Result<T, BErr>;


// ---------------------------------------------------------------- Profiling (feature "prof" only)
#[cfg(feature = "prof")]
pub mod prof {
    use std::cell::RefCell;
    thread_local! { pub static T: RefCell<std::collections::BTreeMap<&'static str, (u64, u64)>> = RefCell::new(Default::default()); }
    pub struct G(&'static str, std::time::Instant);
    impl G { pub fn new(n: &'static str) -> G { G(n, std::time::Instant::now()) } }
    impl Drop for G { fn drop(&mut self) { let e = self.1.elapsed().as_nanos() as u64; T.with(|t| { let mut t = t.borrow_mut(); let x = t.entry(self.0).or_insert((0, 0)); x.0 += 1; x.1 += e; }); } }
    pub fn dump() -> Vec<(String, u64, f64)> { T.with(|t| t.borrow().iter().map(|(k, v)| (k.to_string(), v.0, v.1 as f64 * 1e-9)).collect()) }
}
macro_rules! prof { ($n:expr) => { #[cfg(feature = "prof")] let _g = prof::G::new($n); }; }

#[inline]
fn qi(n: i64) -> Q {
    Q::from(n)
}

// ================================================================ Polynomials (fmpq_poly)

#[derive(Clone, PartialEq, Eq, Hash, Debug)]
pub struct P {
    c: Vec<Integer>,
    den: Integer,
}

fn is_zero_vec(c: &[Integer]) -> bool {
    c.is_empty()
}

fn trim(c: &mut Vec<Integer>) {
    while matches!(c.last(), Some(v) if v.cmp0() == Ordering::Equal) {
        c.pop();
    }
}

/// Divide integer coefficients by their content (nonnegative gcd), preserving the sign.
fn primitive(mut c: Vec<Integer>) -> Vec<Integer> {
    trim(&mut c);
    if c.is_empty() {
        return c;
    }
    let mut g = Integer::new();
    for v in c.iter() {
        g.gcd_mut(v);
        if g == 1 {
            return c;
        }
    }
    for v in c.iter_mut() {
        v.div_exact_mut(&g);
    }
    c
}

/// Integer pseudo-division: lc(b)^(deg a − deg b + 1) · a = q · b + r when deg a ≥ deg b.
/// If deg a < deg b, q = 0, r = a, and the multiplier is 1. Returns (q, r, multiplier).
fn pdivrem_z(a: &[Integer], b: &[Integer]) -> (Vec<Integer>, Vec<Integer>, Integer) {
    prof!("pdivrem_z");
    let m = a.len() as i64 - 1;
    let n = b.len() as i64 - 1;
    if m < n {
        return (Vec::new(), a.to_vec(), Integer::from(1));
    }
    let (m, n) = (m as usize, n as usize);
    let lcb = &b[n];
    let mut r = a.to_vec();
    let mut q = vec![Integer::new(); m - n + 1];
    let mut mult = Integer::from(1);
    for j in (0..=(m - n)).rev() {
        let t = r[n + j].clone();
        if *lcb != 1 {
            for qq in q.iter_mut().skip(j + 1) {
                *qq *= lcb;
            }
            for rk in r.iter_mut().take(n + j) {
                *rk *= lcb;
            }
            mult *= lcb;
        }
        if t.cmp0() != Ordering::Equal {
            for k in 0..n {
                r[j + k] -= Integer::from(&t * &b[k]);
            }
        }
        r[n + j] = Integer::new();
        q[j] = t;
    }
    trim(&mut r);
    (q, r, mult)
}

impl P {
    pub fn zero() -> P {
        P { c: Vec::new(), den: Integer::from(1) }
    }
    pub fn one() -> P {
        P { c: vec![Integer::from(1)], den: Integer::from(1) }
    }
    pub fn x() -> P {
        P { c: vec![Integer::new(), Integer::from(1)], den: Integer::from(1) }
    }
    pub fn constq(q: &Q) -> P {
        P::from_parts(vec![q.numer().clone()], q.denom().clone())
    }
    pub fn from_parts(c: Vec<Integer>, den: Integer) -> P {
        let mut p = P { c, den };
        p.canon();
        p
    }
    fn canon(&mut self) {
        trim(&mut self.c);
        if self.c.is_empty() {
            self.den = Integer::from(1);
            return;
        }
        if self.den.cmp0() == Ordering::Less {
            self.den.neg_assign();
            for v in self.c.iter_mut() {
                v.neg_assign();
            }
        }
        if self.den == 1 {
            return;
        }
        let mut g = self.den.clone();
        for v in self.c.iter() {
            g.gcd_mut(v);
            if g == 1 {
                return;
            }
        }
        for v in self.c.iter_mut() {
            v.div_exact_mut(&g);
        }
        self.den.div_exact_mut(&g);
    }
    #[inline]
    pub fn deg(&self) -> i64 {
        self.c.len() as i64 - 1
    }
    #[inline]
    pub fn is_zero(&self) -> bool {
        is_zero_vec(&self.c)
    }
    #[inline]
    fn is_one(&self) -> bool {
        self.c.len() == 1 && self.c[0] == 1 && self.den == 1
    }
    /// Coefficient p[i], or 0 if out of range.
    pub fn coeff(&self, i: usize) -> Q {
        if i < self.c.len() {
            Q::from((self.c[i].clone(), self.den.clone()))
        } else {
            qi(0)
        }
    }
    fn lead(&self) -> Q {
        self.coeff(self.c.len() - 1)
    }
    fn is_monic(&self) -> bool {
        match self.c.last() {
            Some(l) => *l == self.den,
            None => false,
        }
    }
    fn addsub(&self, o: &P, subtract: bool) -> P {
    prof!("paddsub");
        let n = self.c.len().max(o.c.len());
        let mut c = Vec::with_capacity(n);
        if self.den == o.den {
            for i in 0..n {
                let mut v = if i < self.c.len() { self.c[i].clone() } else { Integer::new() };
                if i < o.c.len() {
                    if subtract {
                        v -= &o.c[i];
                    } else {
                        v += &o.c[i];
                    }
                }
                c.push(v);
            }
            P::from_parts(c, self.den.clone())
        } else {
            for i in 0..n {
                let mut v = if i < self.c.len() { Integer::from(&self.c[i] * &o.den) } else { Integer::new() };
                if i < o.c.len() {
                    if subtract {
                        v -= Integer::from(&o.c[i] * &self.den);
                    } else {
                        v += Integer::from(&o.c[i] * &self.den);
                    }
                }
                c.push(v);
            }
            P::from_parts(c, Integer::from(&self.den * &o.den))
        }
    }
    pub fn add(&self, o: &P) -> P {
        self.addsub(o, false)
    }
    pub fn sub(&self, o: &P) -> P {
        self.addsub(o, true)
    }
    pub fn neg(&self) -> P {
        let mut r = self.clone();
        for v in r.c.iter_mut() {
            v.neg_assign();
        }
        r
    }
    pub fn mul(&self, o: &P) -> P {
    prof!("pmul");
        if self.is_zero() || o.is_zero() {
            return P::zero();
        }
        let mut c = vec![Integer::new(); self.c.len() + o.c.len() - 1];
        for (i, a) in self.c.iter().enumerate() {
            if a.cmp0() == Ordering::Equal {
                continue;
            }
            for (j, b) in o.c.iter().enumerate() {
                c[i + j] += Integer::from(a * b);
            }
        }
        P::from_parts(c, Integer::from(&self.den * &o.den))
    }
    pub fn mul_q(&self, q: &Q) -> P {
        if q.cmp0() == Ordering::Equal || self.is_zero() {
            return P::zero();
        }
        let c = self.c.iter().map(|v| Integer::from(v * q.numer())).collect();
        P::from_parts(c, Integer::from(&self.den * q.denom()))
    }
    /// q ≠ 0
    pub fn div_q(&self, q: &Q) -> P {
        let c = self.c.iter().map(|v| Integer::from(v * q.denom())).collect();
        P::from_parts(c, Integer::from(&self.den * q.numer()))
    }
    pub fn derivative(&self) -> P {
        if self.c.len() <= 1 {
            return P::zero();
        }
        let c = (1..self.c.len()).map(|i| Integer::from(&self.c[i] * (i as u64))).collect();
        P::from_parts(c, self.den.clone())
    }
    /// (Σ c_i pn^i qd^(n−i), qd^n): p(x) = first / (second · den).
    fn horner(&self, x: &Q) -> (Integer, Integer) {
        let n = self.c.len() - 1;
        let pn = x.numer();
        let qd = x.denom();
        let mut acc = self.c[n].clone();
        let mut qp = Integer::from(1);
        if *qd == 1 {
            for i in (0..n).rev() {
                acc *= pn;
                acc += &self.c[i];
            }
            return (acc, qp);
        }
        for i in (0..n).rev() {
            qp *= qd;
            acc *= pn;
            acc += Integer::from(&self.c[i] * &qp);
        }
        (acc, qp)
    }
    /// Sign of p(x): -1, 0, or 1.
    pub fn sign_at(&self, x: &Q) -> i32 {
        if self.c.is_empty() {
            return 0;
        }
        match self.horner(x).0.cmp0() {
            Ordering::Less => -1,
            Ordering::Equal => 0,
            Ordering::Greater => 1,
        }
    }
    #[allow(dead_code)]
    pub fn eval(&self, x: &Q) -> Q {
        if self.c.is_empty() {
            return qi(0);
        }
        let (acc, qp) = self.horner(x);
        Q::from((acc, qp * &self.den))
    }
    /// Make monic (leading coefficient 1, as in flint's gcd result).
    fn monic(&self) -> P {
        if self.is_zero() || self.is_monic() {
            return self.clone();
        }
        P::from_parts(self.c.clone(), self.c[self.c.len() - 1].clone())
    }
}

/// (a // b, a % b): division over the rationals (b ≠ 0).
pub fn divrem(a: &P, b: &P) -> (P, P) {
    if b.is_zero() {
        panic!("polynomial division by zero");
    }
    if a.deg() < b.deg() {
        return (P::zero(), a.clone());
    }
    let (q, r, mult) = pdivrem_z(&a.c, &b.c);
    let d = Integer::from(&mult * &a.den);
    let qq = P::from_parts(q.into_iter().map(|v| v * &b.den).collect(), d.clone());
    let rr = P::from_parts(r, d);
    (qq, rr)
}

/// a // b, used only for exact division by a gcd. By Gauss's lemma, dividing a's integer numerator A
/// by b's primitive part Bp yields integer coefficients, so each division step is exact over the integers.
/// Fall back to general divrem if the remainder is nonzero (not expected).
pub fn pdiv(a: &P, b: &P) -> P {
    if b.is_zero() {
        panic!("polynomial division by zero");
    }
    if a.is_zero() || a.deg() < b.deg() {
        return divrem(a, b).0;
    }
    // b = cb · Bp / db (Bp is primitive).
    let mut cb = Integer::new();
    for v in b.c.iter() {
        cb.gcd_mut(v);
        if cb == 1 {
            break;
        }
    }
    let bp: Vec<Integer> = if cb == 1 { b.c.clone() } else { b.c.iter().map(|v| Integer::from(v.div_exact_ref(&cb))).collect() };
    let n = bp.len() - 1;
    let m = a.c.len() - 1;
    let lcb = &bp[n];
    let mut r = a.c.clone();
    let mut q = vec![Integer::new(); m - n + 1];
    for j in (0..=(m - n)).rev() {
        let t = std::mem::take(&mut r[n + j]);
        if t.cmp0() == Ordering::Equal {
            continue;
        }
        let (qj, rem) = t.div_rem_ref(lcb).into();
        let (qj, rem): (Integer, Integer) = (qj, rem);
        if rem.cmp0() != Ordering::Equal {
            return divrem(a, b).0;
        }
        for k in 0..n {
            r[j + k] -= Integer::from(&qj * &bp[k]);
        }
        q[j] = qj;
    }
    if r.iter().any(|v| v.cmp0() != Ordering::Equal) {
        return divrem(a, b).0;
    }
    // a / b = (A / Bp) · db / (da · cb)
    let qq: Vec<Integer> = q.into_iter().map(|v| v * &b.den).collect();
    P::from_parts(qq, Integer::from(&a.den * &cb))
}

pub fn prem(a: &P, b: &P) -> P {
    divrem(a, b).1
}

const PRIMES: [u32; 3] = [2147483647, 2147483629, 2147483587];

fn powmod(mut b: u64, mut e: u64, p: u64) -> u64 {
    let mut r = 1u64;
    b %= p;
    while e > 0 {
        if e & 1 == 1 {
            r = r * b % p;
        }
        b = b * b % p;
        e >>= 1;
    }
    r
}

/// Degree of gcd(a, b) mod p; None if p divides either leading coefficient.
fn modp_gcd_deg(a: &[Integer], b: &[Integer], p: u32) -> Option<usize> {
    let pp = p as u64;
    let red = |c: &[Integer]| -> Vec<u64> { c.iter().map(|v| v.mod_u(p) as u64).collect() };
    let mut x = red(a);
    let mut y = red(b);
    if *x.last().unwrap() == 0 || *y.last().unwrap() == 0 {
        return None;
    }
    let tr = |v: &mut Vec<u64>| {
        while matches!(v.last(), Some(0)) {
            v.pop();
        }
    };
    if x.len() < y.len() {
        std::mem::swap(&mut x, &mut y);
    }
    while !y.is_empty() {
        // x ← x mod y
        let n = y.len() - 1;
        let inv = powmod(y[n], pp - 2, pp);
        while x.len() >= y.len() {
            let m = x.len() - 1;
            let f = x[m] * inv % pp;
            if f != 0 {
                for k in 0..=n {
                    let s = f * y[k] % pp;
                    let i = m - n + k;
                    x[i] = (x[i] + pp - s) % pp;
                }
            }
            x.pop();
            tr(&mut x);
        }
        std::mem::swap(&mut x, &mut y);
    }
    Some(x.len() - 1)
}

/// Sufficient for integer polynomials a, b (degree ≥ 1) to be coprime over Q: gcd mod p is constant
/// for a prime p dividing neither leading coefficient. The gcd h over Q retains its degree modulo p and divides the modular gcd.
/// False is inconclusive; the caller then uses Euclid's algorithm.
fn modp_coprime(a: &[Integer], b: &[Integer]) -> bool {
    for &p in PRIMES.iter() {
        if let Some(d) = modp_gcd_deg(a, b, p) {
            return d == 0;
        }
    }
    false
}

/// Exact flint fmpq_poly.gcd semantics: monic, or 0 if both inputs are 0. Uses a primitive Euclidean remainder sequence.
pub fn gcd(a: &P, b: &P) -> P {
    prof!("gcd");
    if a.is_zero() && b.is_zero() {
        return P::zero();
    }
    if a.is_zero() {
        return b.monic();
    }
    if b.is_zero() {
        return a.monic();
    }
    if a.deg() > 0 && b.deg() > 0 && modp_coprime(&a.c, &b.c) {
        return P::one();
    }
    let mut x = primitive(a.c.clone());
    let mut y = primitive(b.c.clone());
    if x.len() < y.len() {
        std::mem::swap(&mut x, &mut y);
    }
    loop {
        if y.len() == 1 {
            return P::one();
        }
        let (_, r, _) = pdivrem_z(&x, &y);
        if r.is_empty() {
            break;
        }
        x = y;
        y = primitive(r);
    }
    let l = y[y.len() - 1].clone();
    P::from_parts(y, l)
}

// ================================================================ Rational functions (rf.RF) and Ctx

/// B3_PLAIN_RF=1 uses Python's RF arithmetic steps: form products/sums, then reduce by the full gcd.
/// The reduced form is unique; this option cross-checks that both paths produce identical decisions.
fn plain_rf() -> bool {
    use std::sync::OnceLock;
    static PLAIN: OnceLock<bool> = OnceLock::new();
    *PLAIN.get_or_init(|| std::env::var("B3_PLAIN_RF").map(|v| v == "1").unwrap_or(false))
}

#[derive(Clone, PartialEq, Eq, Hash, Debug)]
pub struct RF {
    pub n: P,
    pub d: P,
}

impl RF {
    /// RF(n, d, reduce=True)
    pub fn reduce(mut n: P, mut d: P) -> RF {
    prof!("rf_reduce");
        if (d.deg() > 0 || n.deg() > 0) && d.deg() > 0 {
            // For nonzero constant d, gcd(n, d) = 1, so Python also does nothing.
            let g = gcd(&n, &d);
            if g.deg() > 0 {
                n = pdiv(&n, &g);
                d = pdiv(&d, &g);
            }
        }
        if !d.is_monic() {
            let lc = d.lead();
            n = n.div_q(&lc);
            d = d.div_q(&lc);
        }
        RF { n, d }
    }
    pub fn konst(q: &Q) -> RF {
        RF { n: P::constq(q), d: P::one() }
    }
    pub fn ki(v: i64) -> RF {
        RF::konst(&qi(v))
    }
    pub fn var() -> RF {
        RF { n: P::x(), d: P::one() }
    }
    #[inline]
    fn is_const(&self) -> bool {
        self.n.deg() <= 0 && self.d.is_one()
    }
    #[inline]
    pub fn is_zero(&self) -> bool {
        self.n.is_zero()
    }
    // Arithmetic yields Python's RF(..., reduce=True) form: coprime numerator and denominator, with a monic denominator.
    // This form is unique for each value. Henrici's method uses reduced inputs to obtain it with smaller gcds.
    // The B3_PLAIN_RF path (plain_*) follows Python's steps exactly for cross-checking.
    pub fn add(&self, o: &RF) -> RF {
        self.addsub(o, false)
    }
    pub fn sub(&self, o: &RF) -> RF {
        self.addsub(o, true)
    }
    fn addsub(&self, o: &RF, subtract: bool) -> RF {
        if plain_rf() {
            return self.plain_addsub(o, subtract);
        }
        if o.n.is_zero() {
            return self.clone();
        }
        if self.n.is_zero() {
            return if subtract { o.neg() } else { o.clone() };
        }
        let comb = |a: &P, b: &P| if subtract { a.sub(b) } else { a.add(b) };
        if self.d == o.d {
            return RF::reduce(comb(&self.n, &o.n), self.d.clone());
        }
        if self.d.is_one() || o.d.is_one() {
            // If one denominator is 1, gcd(n1·d2 ± n2·d1, d1·d2) = 1; for d1 = 1, n1·d2 ± n2 and d2 are coprime.
            let n = comb(&self.n.mul(&o.d), &o.n.mul(&self.d));
            if n.is_zero() {
                return RF::ki(0);
            }
            return RF { n, d: self.d.mul(&o.d) };
        }
        let g = gcd(&self.d, &o.d);
        if g.deg() <= 0 {
            let n = comb(&self.n.mul(&o.d), &o.n.mul(&self.d));
            if n.is_zero() {
                return RF::ki(0);
            }
            return RF { n, d: self.d.mul(&o.d) };
        }
        let d1g = pdiv(&self.d, &g);
        let d2g = pdiv(&o.d, &g);
        let n = comb(&self.n.mul(&d2g), &o.n.mul(&d1g));
        if n.is_zero() {
            return RF::ki(0);
        }
        // gcd(n, d1·d2/g) = gcd(n, g) (Henrici).
        let g2 = gcd(&n, &g);
        if g2.deg() > 0 {
            RF { n: pdiv(&n, &g2), d: pdiv(&self.d, &g2).mul(&d2g) }
        } else {
            RF { n, d: self.d.mul(&d2g) }
        }
    }
    fn plain_addsub(&self, o: &RF, subtract: bool) -> RF {
        let comb = |a: &P, b: &P| if subtract { a.sub(b) } else { a.add(b) };
        if self.d == o.d {
            RF::reduce(comb(&self.n, &o.n), self.d.clone())
        } else {
            RF::reduce(comb(&self.n.mul(&o.d), &o.n.mul(&self.d)), self.d.mul(&o.d))
        }
    }
    pub fn neg(&self) -> RF {
        RF { n: self.n.neg(), d: self.d.clone() }
    }
    /// (n1/d1)·(n2/d2): for reduced inputs, cancel g1 = gcd(n1, d2) and g2 = gcd(n2, d1) to obtain coprime factors.
    /// Make the denominator monic, including division cases where d1 or d2 is not monic.
    fn mul_parts(n1: &P, d1: &P, n2: &P, d2: &P) -> RF {
        if n1.is_zero() || n2.is_zero() {
            return RF::ki(0);
        }
        let (a, dd2) = if d2.deg() > 0 && n1.deg() > 0 {
            let g1 = gcd(n1, d2);
            if g1.deg() > 0 { (pdiv(n1, &g1), pdiv(d2, &g1)) } else { (n1.clone(), d2.clone()) }
        } else {
            (n1.clone(), d2.clone())
        };
        let (b, dd1) = if d1.deg() > 0 && n2.deg() > 0 {
            let g2 = gcd(n2, d1);
            if g2.deg() > 0 { (pdiv(n2, &g2), pdiv(d1, &g2)) } else { (n2.clone(), d1.clone()) }
        } else {
            (n2.clone(), d1.clone())
        };
        let mut n = a.mul(&b);
        let mut d = dd1.mul(&dd2);
        if !d.is_monic() {
            let lc = d.lead();
            n = n.div_q(&lc);
            d = d.div_q(&lc);
        }
        RF { n, d }
    }
    pub fn mul(&self, o: &RF) -> RF {
        // Constant scaling preserves the reduced form: gcd(c·n, d) = gcd(n, d) = 1 and d stays monic, matching reduce.
        if o.is_const() {
            if o.n.is_zero() {
                return RF::ki(0);
            }
            return RF { n: self.n.mul(&o.n), d: self.d.clone() };
        }
        if self.is_const() {
            if self.n.is_zero() {
                return RF::ki(0);
            }
            return RF { n: o.n.mul(&self.n), d: o.d.clone() };
        }
        if plain_rf() {
            return RF::reduce(self.n.mul(&o.n), self.d.mul(&o.d));
        }
        RF::mul_parts(&self.n, &self.d, &o.n, &o.d)
    }
    pub fn mulq(&self, q: &Q) -> RF {
        self.mul(&RF::konst(q))
    }
    pub fn div(&self, o: &RF) -> R<RF> {
        if o.n.is_zero() {
            return Err(BErr::ZeroDiv);
        }
        if plain_rf() {
            return Ok(RF::reduce(self.n.mul(&o.d), self.d.mul(&o.n)));
        }
        Ok(RF::mul_parts(&self.n, &self.d, &o.d, &o.n))
    }
    pub fn half(&self) -> RF {
        self.mulq(&Q::from((1, 2)))
    }
    /// Python reference: sign_poly
    pub fn sign_poly(&self) -> P {
        self.n.mul(&self.d)
    }
}

/// rf.Ctx: sample u and recorded guard polynomials, deduplicated in insertion order.
pub struct Ctx {
    pub u: Q,
    pub guards: Vec<P>,
    seen: HashSet<P>,
}

impl Ctx {
    pub fn new(u: Q) -> Ctx {
        Ctx { u, guards: Vec::new(), seen: HashSet::new() }
    }
    /// RF.sign()
    pub fn sign(&mut self, v: &RF) -> R<i32> {
    prof!("ctx_sign");
        if v.n.is_zero() {
            return Ok(0);
        }
        // value() = n(u)/d(u): raise ZeroDivisionError if d(u) = 0.
        let sd = v.d.sign_at(&self.u);
        if sd == 0 {
            return Err(BErr::ZeroDiv);
        }
        let sn = v.n.sign_at(&self.u);
        if sn == 0 {
            return Err(BErr::Resample);
        }
        let g = v.n.mul(&v.d);
        if !self.seen.contains(&g) {
            self.seen.insert(g.clone());
            self.guards.push(g);
        }
        Ok(sn * sd)
    }
}

// ================================================================ Real roots

pub fn squarefree(p: &P) -> P {
    let g = gcd(p, &p.derivative());
    if g.deg() > 0 {
        pdiv(p, &g)
    } else {
        p.clone()
    }
}

// Cache only immutable Sturm coefficients, never Alg objects or refined endpoints.
// P's canonical coefficients and denominator are the full key (Hash + exact Eq).
// The scope restores an outer cache on nested calls and drops this leaf's entries
// on every exit, including errors and unwinding.
type SturmCache = HashMap<P, Vec<P>>;
thread_local! {
    static STURM_CACHE: RefCell<Option<SturmCache>> = const { RefCell::new(None) };
}
struct SturmScope(Option<SturmCache>);
impl SturmScope {
    fn new() -> Self {
        Self(STURM_CACHE.with(|c| c.replace(Some(HashMap::new()))))
    }
}
impl Drop for SturmScope {
    fn drop(&mut self) {
        STURM_CACHE.with(|c| { c.replace(self.0.take()); });
    }
}

pub fn sturm(p: &P) -> Vec<P> {
    prof!("sturm");
    if let Some(seq) = STURM_CACHE.with(|c| {
        c.borrow().as_ref().and_then(|m| m.get(p)).cloned()
    }) {
        return seq;
    }
    let seq = sturm_uncached(p);
    STURM_CACHE.with(|c| {
        if let Some(m) = c.borrow_mut().as_mut() {
            // Bound retained entries even for unusually large arrangements.
            if m.len() >= 256 { m.clear(); }
            m.insert(p.clone(), seq.clone());
        }
    });
    seq
}

fn sturm_uncached(p: &P) -> Vec<P> {
    prof!("sturm_uncached");
    let mut seq = vec![p.clone(), p.derivative()];
    while seq[seq.len() - 1].deg() > 0 {
        let r = prem(&seq[seq.len() - 2], &seq[seq.len() - 1]).neg();
        if r.is_zero() {
            break;
        }
        seq.push(r);
    }
    seq
}

fn var_at(seq: &[P], x: &Q) -> i64 {
    let mut cnt = 0;
    let mut last = 0;
    for q in seq {
        let s = q.sign_at(x);
        if s == 0 {
            continue;
        }
        if last != 0 && s != last {
            cnt += 1;
        }
        last = s;
    }
    cnt
}

pub fn count_roots(seq: &[P], lo: &Q, hi: &Q) -> i64 {
    prof!("count_roots");
    var_at(seq, lo) - var_at(seq, hi)
}

pub fn isolate(p: &P, lo: &Q, hi: &Q) -> Vec<(Q, Q)> {
    prof!("isolate");
    let p = squarefree(p);
    if p.deg() <= 0 {
        return Vec::new();
    }
    let seq = sturm(&p);
    let mut out = Vec::new();
    let mut stack = vec![(lo.clone(), hi.clone())];
    while let Some((l, r)) = stack.pop() {
        let k = count_roots(&seq, &l, &r);
        if k == 0 {
            continue;
        }
        if k == 1 {
            out.push((l, r));
            continue;
        }
        let mut m = Q::from(&l + &r) / 2u32;
        while p.sign_at(&m) == 0 {
            m = Q::from(&l + Q::from(&m * 2u32)) / 3u32;
        }
        stack.push((l, m.clone()));
        stack.push((m, r));
    }
    out.sort();
    out
}

pub fn roots_open(p: &P, lo: &Q, hi: &Q) -> Vec<(Q, Q)> {
    let mut out = isolate(p, lo, hi);
    if p.sign_at(hi) == 0 {
        out.retain(|iv| iv.1 != *hi);
    }
    out
}

// ================================================================ Algebraic numbers

pub struct AlgI {
    p: Option<P>,
    l: Q,
    r: Q,
    seq: Vec<P>,
}
pub type Alg = Rc<RefCell<AlgI>>;

impl AlgI {
    fn count(&self, a: &Q, b: &Q) -> i64 {
        let p = self.p.as_ref().unwrap();
        count_roots(&self.seq, a, b) - if p.sign_at(b) == 0 { 1 } else { 0 }
    }
    fn refine(&mut self) {
        let p = match &self.p {
            None => return,
            Some(p) => p,
        };
        let m = Q::from(&self.l + &self.r) / 2u32;
        let v = p.sign_at(&m);
        if v == 0 {
            self.p = None;
            self.l = m.clone();
            self.r = m;
        } else if (p.sign_at(&self.l) > 0) != (v > 0) {
            self.r = m;
        } else {
            self.l = m;
        }
    }
    fn width(&self) -> Q {
        Q::from(&self.r - &self.l)
    }
}

pub fn alg_rat(x: Q) -> Alg {
    Rc::new(RefCell::new(AlgI { p: None, l: x.clone(), r: x, seq: Vec::new() }))
}

/// Alg(p, l, r)
pub fn alg_new(p: P, l: Q, r: Q) -> R<Alg> {
    prof!("alg_new");
    let seq = sturm(&p);
    let mut a = AlgI { p: Some(p), l, r, seq };
    let pz = |a: &AlgI, x: &Q| a.p.as_ref().unwrap().sign_at(x) == 0;
    if pz(&a, &a.r) && count_roots(&a.seq, &a.l, &a.r) == 1 {
        a.p = None;
        a.l = a.r.clone();
        return Ok(Rc::new(RefCell::new(a)));
    }
    let c = count_roots(&a.seq, &a.l, &a.r) - if pz(&a, &a.r) { 1 } else { 0 };
    if c != 1 {
        return Err(BErr::Assert("Alg: not isolating".into()));
    }
    while pz(&a, &a.l) || pz(&a, &a.r) {
        let m = Q::from(&a.l + &a.r) / 2u32;
        if pz(&a, &m) && a.count(&a.l, &m) == 0 && a.count(&m, &a.r) == 0 {
            a.p = None;
            a.l = m.clone();
            a.r = m;
            return Ok(Rc::new(RefCell::new(a)));
        }
        if a.count(&a.l, &m) == 1 {
            a.r = m;
        } else {
            a.l = m;
        }
    }
    Ok(Rc::new(RefCell::new(a)))
}

/// alg_cmp(A, B): -1, 0, or 1; A and B may be the same object.
pub fn alg_cmp(av: &Alg, bv: &Alg) -> R<i32> {
    prof!("alg_cmp");
    for _ in 0..400 {
        let refine_a = {
            let a = av.borrow();
            let b = bv.borrow();
            let (an, bn) = (a.p.is_none(), b.p.is_none());
            if a.r < b.l || (an && !bn && a.r <= b.l) || (an && bn && a.r < b.l) {
                return Ok(-1);
            }
            if b.r < a.l || (bn && !an && b.r <= a.l) || (an && bn && b.r < a.l) {
                return Ok(1);
            }
            if an && bn {
                return Ok(match a.l.cmp(&b.l) {
                    Ordering::Equal => 0,
                    Ordering::Less => -1,
                    Ordering::Greater => 1,
                });
            }
            if let (Some(pa), Some(pb)) = (&a.p, &b.p) {
                let g = gcd(pa, pb);
                if g.deg() > 0 {
                    let lo = if a.l >= b.l { &a.l } else { &b.l };
                    let hi = if a.r <= b.r { &a.r } else { &b.r };
                    if lo < hi
                        && count_roots(&sturm(&squarefree(&g)), lo, hi) - if g.sign_at(hi) == 0 { 1 } else { 0 } > 0
                    {
                        return Ok(0);
                    }
                }
            }
            if let (Some(pa), true) = (&a.p, bn) {
                if a.l < b.l && b.l < a.r && pa.sign_at(&b.l) == 0 {
                    return Ok(0);
                }
            }
            if let (Some(pb), true) = (&b.p, an) {
                if b.l < a.l && a.l < b.r && pb.sign_at(&a.l) == 0 {
                    return Ok(0);
                }
            }
            a.width() >= b.width()
        };
        if refine_a {
            av.borrow_mut().refine();
        } else {
            bv.borrow_mut().refine();
        }
    }
    Err(BErr::Runtime("alg_cmp did not separate".into()))
}

pub fn strip0(p: &P) -> P {
    let mut k = 0;
    while p.c[k].cmp0() == Ordering::Equal {
        k += 1;
    }
    if k == 0 {
        return p.clone();
    }
    P::from_parts(p.c[k..].to_vec(), p.den.clone())
}

/// root_free(p, lo, hi): for coefficients t_i of p(x + lo), test |t_0| > Σ_{i≥1} |t_i| w^i, where w = hi − lo.
/// Over integers: lo = s/t, W(z) = Σ c_i t^(n−i) (z + s)^i, hence t_i = W_i t^i / (den t^n).
/// With w = wn/wd, multiply by den t^n wd^n > 0 to get |W_0| wd^n > Σ |W_i| (t wn)^i wd^(n−i).
pub fn root_free(p: &P, lo: &Q, hi: &Q) -> bool {
    prof!("root_free");
    if p.c.is_empty() {
        return false; // abs(t[0]) = 0 > s = 0 is false.
    }
    let n = p.c.len() - 1;
    if n == 0 {
        return true; // |c0| > 0
    }
    let s = lo.numer();
    let t = lo.denom();
    let mut w: Vec<Integer> = Vec::with_capacity(n + 1);
    w.push(p.c[n].clone());
    let mut tp = Integer::from(1);
    for i in (0..n).rev() {
        tp *= t;
        // w ← w·(z + s) + c_i t^(n−i)
        w.push(Integer::new());
        for k in (1..w.len()).rev() {
            let prev = w[k - 1].clone();
            let cur = &mut w[k];
            *cur *= s;
            *cur += prev;
        }
        w[0] *= s;
        w[0] += Integer::from(&p.c[i] * &tp);
    }
    let wq = Q::from(hi - lo);
    let wn = wq.numer();
    let wd = wq.denom();
    let tw = Integer::from(t * wn);
    // rhs = Σ_{i=1..n} |W_i| tw^i wd^(n−i): use Horner's rule to form (...(|W_n| tw + |W_{n-1}| wd) tw + ...).
    // Σ_{i=1..n} |W_i| tw^i wd^(n−i) = tw · Σ_{i=1..n} |W_i| tw^(i−1) wd^(n−i)
    let mut acc = Integer::from(w[n].abs_ref());
    let mut wdp = Integer::from(1);
    for i in (1..n).rev() {
        wdp *= wd;
        acc *= &tw;
        acc += Integer::from(w[i].abs_ref()) * &wdp;
    }
    let rhs = acc * &tw;
    wdp *= wd; // wd^n
    let lhs = Integer::from(w[0].abs_ref()) * &wdp;
    lhs > rhs
}

// ================================================================ Root intervals and signs

pub fn roots_in(p: &P, a: &Q, b: &Q) -> R<Vec<Alg>> {
    prof!("roots_in");
    let mut out = Vec::new();
    if p.deg() <= 0 {
        return Ok(out);
    }
    let stripped;
    let mut p = p;
    if a.cmp0() == Ordering::Equal || b.cmp0() == Ordering::Equal {
        stripped = strip0(p);
        p = &stripped;
        if p.deg() <= 0 {
            return Ok(out);
        }
    }
    if root_free(p, a, b) {
        return Ok(out);
    }
    let sq = squarefree(p);
    for (l, r) in roots_open(&sq, a, b) {
        out.push(alg_new(sq.clone(), l, r)?);
    }
    Ok(out)
}

pub fn sorted_unique(mut algs: Vec<Alg>) -> R<Vec<Alg>> {
    prof!("sorted_unique");
    // sorted(algs, key=lambda z: z.l), stable.
    algs.sort_by(|x, y| x.borrow().l.cmp(&y.borrow().l));
    let mut out: Vec<Alg> = Vec::new();
    for x in algs {
        let mut k = out.len();
        while k > 0 && alg_cmp(&out[k - 1], &x)? > 0 {
            k -= 1;
        }
        if k > 0 && alg_cmp(&out[k - 1], &x)? == 0 {
            continue;
        }
        out.insert(k, x);
    }
    Ok(out)
}

pub fn between(av: &Alg, bv: &Alg) -> R<Q> {
    for _ in 0..400 {
        let which = {
            let a = av.borrow();
            let b = bv.borrow();
            if a.r < b.l {
                return Ok(Q::from(&a.r + &b.l) / 2u32);
            }
            if a.width() >= b.width() && a.p.is_some() {
                0
            } else if b.p.is_some() {
                1
            } else {
                0
            }
        };
        if which == 0 {
            av.borrow_mut().refine();
        } else {
            bv.borrow_mut().refine();
        }
    }
    Err(BErr::Runtime("between".into()))
}

/// Product of odd-multiplicity factors from p.factor_squarefree(), up to a nonzero constant; only root locations matter.
/// Yun's method: a = Π f_i^i, c = gcd(a, a′), w = a/c, y = gcd(w, c), f_i = w/y, ...
fn odd_part(p: &P) -> P {
    if p.deg() <= 0 {
        return P::one();
    }
    let mut c = gcd(p, &p.derivative());
    let mut w = pdiv(p, &c);
    let mut i = 1;
    let mut odd = P::one();
    while w.deg() > 0 {
        let y = gcd(&w, &c);
        let z = pdiv(&w, &y);
        if i % 2 == 1 && z.deg() > 0 {
            odd = odd.mul(&z);
        }
        i += 1;
        c = pdiv(&c, &y);
        w = y;
    }
    odd
}

pub fn nonneg_open(p: &P, av: &Alg, bv: &Alg) -> R<bool> {
    nonneg_open_impl(p,av,bv,false)
}

// The edge chain uses the reference nonneg_open of the two-edge chain, not the one of the B3D chain:
// no root_free shortcut, and samples move right past an even zero.
fn nonneg_open_impl(p: &P, av: &Alg, bv: &Alg, edge_reference: bool) -> R<bool> {
    prof!("nonneg_open");
    if p.is_zero() {
        return Ok(true);
    }
    let lo = av.borrow().l.clone();
    let hi = bv.borrow().r.clone();
    // Shortcut: if root_free proves [lo, hi] ⊇ (A, B) has no roots, the sign is constant and one sample suffices.
    // This matches the general path: there are no odd-multiplicity roots, and the sample is not a root.
    if !edge_reference && root_free(p, &lo, &hi) {
        let s = between(av, bv)?;
        return Ok(p.sign_at(&s) > 0);
    }
    let odd = odd_part(p);
    if odd.deg() > 0 {
        for (l, r) in isolate(&odd, &lo, &hi) {
            let mut rr = alg_new(squarefree(&odd), l, r.clone())?;
            if odd.sign_at(&r) == 0 {
                rr = alg_rat(r);
            }
            if alg_cmp(av, &rr)? < 0 && alg_cmp(&rr, bv)? < 0 {
                return Ok(false);
            }
        }
    }
    // Resample if s is an even-multiplicity root (p(s) = 0). Since p ≢ 0, it has finitely many roots.
    let mut s = between(av, bv)?;
    loop {
        let sg = p.sign_at(&s);
        if sg != 0 {
            return Ok(sg > 0);
        }
        s = if edge_reference {between(&alg_rat(s),bv)?} else {between(av,&alg_rat(s))?};
    }
}

pub fn roots_in_alg(g: &P, av: &Alg, bv: &Alg) -> R<Vec<Alg>> {
    prof!("roots_in_alg");
    let lo = av.borrow().l.clone();
    let hi = bv.borrow().r.clone();
    let mut out = Vec::new();
    for r in roots_in(g, &lo, &hi)? {
        if alg_cmp(av, &r)? < 0 && alg_cmp(&r, bv)? < 0 {
            out.push(r);
        }
    }
    for x in [lo, hi] {
        if !g.is_zero() && g.sign_at(&x) == 0 {
            let rr = alg_rat(x);
            if alg_cmp(av, &rr)? < 0 && alg_cmp(&rr, bv)? < 0 {
                out.push(rr);
            }
        }
    }
    Ok(out)
}

// ================================================================ Local geometry and mass

pub struct Frame {
    pub c: RF,
    pub s: RF,
    pub verts: Vec<(RF, RF)>,
    pub normals: Vec<(RF, RF)>,
}

/// solver.frame(u): u is the variable itself; construct once since the result is sample-independent.
pub fn frame() -> R<Frame> {
    let u = RF::var();
    let uu = u.mul(&u);
    let d = RF::ki(1).add(&uu);
    let c = RF::ki(1).sub(&uu).div(&d)?;
    let s = u.mulq(&qi(2)).div(&d)?;
    let mut verts = Vec::new();
    for (a, b) in [(1i64, 1i64), (-1, 1), (-1, -1), (1, -1)] {
        let vx = c.mulq(&qi(a)).sub(&s.mulq(&qi(b))).half();
        let vy = s.mulq(&qi(a)).add(&c.mulq(&qi(b))).half();
        verts.push((vx, vy));
    }
    let normals = vec![(c.clone(), s.clone()), (s.neg(), c.clone()), (c.neg(), s.neg()), (s.clone(), c.neg())];
    Ok(Frame { c, s, verts, normals })
}

/// solver.Local for covers without polygons or points: local segments, mass lines, and density breakpoints.
pub struct Loc {
    pub pts: Vec<(Q, Q, Q)>,
    pub segs: Vec<(Pt, Pt, Q)>,
    pub lines: Vec<(Q, Q, Q)>,
    pub bps: Vec<Pt>,
}

pub fn local(cov: &[(Pt, Pt, Q)], x0: &Q, x1: &Q, y0: &Q, y1: &Q) -> Loc {
    let reach = Q::from((7072, 10000));
    let bx0 = Q::from(x0 - &reach);
    let bx1 = Q::from(x1 + &reach);
    let by0 = Q::from(y0 - &reach);
    let by1 = Q::from(y1 + &reach);
    let hit = |a: &Pt, b: &Pt| {
        let mxx = if a.0 >= b.0 { &a.0 } else { &b.0 };
        let mnx = if a.0 <= b.0 { &a.0 } else { &b.0 };
        let mxy = if a.1 >= b.1 { &a.1 } else { &b.1 };
        let mny = if a.1 <= b.1 { &a.1 } else { &b.1 };
        !(*mxx < bx0 || *mnx > bx1 || *mxy < by0 || *mny > by1)
    };
    let segs: Vec<(Pt, Pt, Q)> = cov.iter().filter(|(a, b, _)| hit(a, b)).cloned().collect();
    // lin[(key, lo, hi)] += w / L, per[key] = [(lo, hi, d)], where key = ('v', x) or ('h', y).
    let mut lin: Vec<((bool, Q, Q, Q), Q)> = Vec::new(); // (is_v, v, lo, hi) -> d
    for ((ax, ay), (bx, by), w) in cov.iter() {
        let l = Q::from(Q::from(bx - ax).abs() + Q::from(by - ay).abs());
        let key = if ax == bx {
            (true, ax.clone(), if ay <= by { ay.clone() } else { by.clone() }, if ay >= by { ay.clone() } else { by.clone() })
        } else {
            (false, ay.clone(), if ax <= bx { ax.clone() } else { bx.clone() }, if ax >= bx { ax.clone() } else { bx.clone() })
        };
        let dv = Q::from(w / &l);
        match lin.iter_mut().find(|(k, _)| *k == key) {
            Some((_, d)) => *d += dv,
            None => lin.push((key, dv)),
        }
    }
    let mut per: Vec<((bool, Q), Vec<(Q, Q, Q)>)> = Vec::new();
    for ((isv, v, lo, hi), d) in lin.into_iter() {
        let k = (isv, v);
        match per.iter_mut().find(|(kk, _)| *kk == k) {
            Some((_, list)) => list.push((lo, hi, d)),
            None => per.push((k, vec![(lo, hi, d)])),
        }
    }
    let mut lines: Vec<(Q, Q, Q)> = Vec::new();
    let mut bps: Vec<Pt> = Vec::new();
    for ((isv, v), pieces) in per.iter() {
        let mut ts: Vec<Q> = pieces.iter().flat_map(|(lo, hi, _)| [lo.clone(), hi.clone()]).collect();
        ts.sort();
        ts.dedup();
        let dens = |t: &Q| -> Q {
            let mut s = qi(0);
            for (lo, hi, d) in pieces.iter() {
                if lo < t && t < hi {
                    s += d;
                }
            }
            s
        };
        for i in 0..ts.len() {
            let t = &ts[i];
            let left = if i > 0 { dens(&(Q::from(&ts[i - 1] + t) / 2u32)) } else { qi(0) };
            let right = if i + 1 < ts.len() { dens(&(Q::from(t + &ts[i + 1]) / 2u32)) } else { qi(0) };
            if left != right {
                let p = if *isv { (v.clone(), t.clone()) } else { (t.clone(), v.clone()) };
                if bx0 <= p.0 && p.0 <= bx1 && by0 <= p.1 && p.1 <= by1 && !bps.contains(&p) {
                    bps.push(p);
                }
            }
        }
        let inwin = if *isv { bx0 <= *v && *v <= bx1 } else { by0 <= *v && *v <= by1 };
        if inwin {
            let l = if *isv { (qi(1), qi(0), v.clone()) } else { (qi(0), qi(1), v.clone()) };
            if !lines.contains(&l) {
                lines.push(l);
            }
        }
    }
    lines.sort();
    bps.sort();
    Loc { segs, lines, bps, pts: Vec::new() }
}

/// Polygon part of solver.Local. Do not normalize edges or refilter vertices by the window.
fn add_u(loc: &mut Loc, bx: &[Q; 6], a: &Q, side: &Q) -> R<Vec<Pt>> {
    let reach = Q::from((7072, 10000));
    if a >= side || *side < Q::from(&bx[0] - &reach) || *a > Q::from(&bx[1] + &reach)
        || *side < Q::from(&bx[2] - &reach) || *a > Q::from(&bx[3] + &reach) {
        return Err(BErr::Assert("expected one local U polygon".into()));
    }
    let vs = vec![(a.clone(),a.clone()),(side.clone(),a.clone()),
                  (side.clone(),side.clone()),(a.clone(),side.clone())];
    for i in 0..vs.len() {
        let (p,r)=(&vs[i],&vs[(i+1)%vs.len()]);
        let la=Q::from(&r.1-&p.1); let lb=Q::from(&p.0-&r.0);
        let lk=Q::from(&la*&p.0)+Q::from(&lb*&p.1);
        loc.lines.push((la,lb,lk)); loc.bps.push(p.clone());
    }
    loc.lines.sort(); loc.lines.dedup(); loc.bps.sort(); loc.bps.dedup();
    Ok(vs)
}

/// Represent the two-edge lower bound's half-plane {x >= a} (kind 'x') or {y >= a} ('y') as a quadrilateral in [0, side]² (SPEC.md §5.5).
/// Add its edge support lines and vertices to loc, as in add_u.
fn add_half(loc: &mut Loc, a: &Q, side: &Q, kind: char) -> Vec<Pt> {
    let z=qi(0);
    let vs = if kind=='x' { vec![(a.clone(),z.clone()),(side.clone(),z.clone()),(side.clone(),side.clone()),(a.clone(),side.clone())] }
             else { vec![(z.clone(),a.clone()),(side.clone(),a.clone()),(side.clone(),side.clone()),(z.clone(),side.clone())] };
    for i in 0..vs.len() {
        let (p,r)=(&vs[i],&vs[(i+1)%vs.len()]);
        let la=Q::from(&r.1-&p.1); let lb=Q::from(&p.0-&r.0);
        let lk=Q::from(&la*&p.0)+Q::from(&lb*&p.1);
        loc.lines.push((la,lb,lk)); loc.bps.push(p.clone());
    }
    loc.lines.sort(); loc.lines.dedup(); loc.bps.sort(); loc.bps.dedup();
    vs
}

/// solver.clip: closed half-plane; record guards in Python's short-circuit comparison order.
fn clip(poly: &[(RF,RF)], a: &Q, b: &Q, k: &Q, ctx: &mut Ctx) -> R<Vec<(RF,RF)>> {
    let mut out=Vec::new();
    for i in 0..poly.len() {
        let (p,r)=(&poly[i],&poly[(i+1)%poly.len()]);
        let fp=p.0.mulq(a).add(&p.1.mulq(b)).sub(&RF::konst(k));
        let fr=r.0.mulq(a).add(&r.1.mulq(b)).sub(&RF::konst(k));
        if ctx.sign(&fp)? <= 0 { out.push(p.clone()); }
        if (ctx.sign(&fp)? < 0 && ctx.sign(&fr)? > 0)
            || (ctx.sign(&fr)? < 0 && ctx.sign(&fp)? > 0) {
            let t=fp.div(&fp.sub(&fr))?;
            out.push((p.0.add(&t.mul(&r.0.sub(&p.0))),p.1.add(&t.mul(&r.1.sub(&p.1)))));
        }
    }
    Ok(out)
}

fn area(poly: &[(RF,RF)]) -> RF {
    let mut s=RF::ki(0);
    for i in 0..poly.len() {
        let (p,r)=(&poly[i],&poly[(i+1)%poly.len()]);
        s=s.add(&p.0.mul(&r.1)).sub(&r.0.mul(&p.1));
    }
    s.half()
}

/// solver.poly_mass for one B3U polygon of density 1.
fn poly_mass(vs: &[Pt], x: &RF, y: &RF, fr: &Frame, ctx: &mut Ctx) -> R<RF> {
    let mut poly: Vec<_>=fr.verts.iter().map(|(vx,vy)|(x.add(vx),y.add(vy))).collect();
    for i in 0..vs.len() {
        let (p,r)=(&vs[i],&vs[(i+1)%vs.len()]);
        let a=Q::from(&r.1-&p.1); let b=Q::from(&p.0-&r.0);
        let k=Q::from(&a*&p.0)+Q::from(&b*&p.1);
        poly=clip(&poly,&a,&b,&k,ctx)?;
        if poly.is_empty() { break; }
    }
    Ok(if poly.len()>=3 {area(&poly)} else {RF::ki(0)})
}

pub fn half_w_max(a: &Q, b: &Q) -> Q {
    let m=a.clone().abs().max(b.clone().abs());
    if m<=Q::from((2,5)) {
        let mm=Q::from(&m*&m);
        (qi(1)-&mm+Q::from(&m*2))/( (qi(1)+mm)*2 )
    } else { Q::from((7072,10000)) }
}
/// Python reference diag_max: upper bound of max(|cos θ|, |sin θ|) for u in [a, b] (0 not interior, |u| <= 1).
pub fn diag_max(a: &Q, b: &Q) -> Q {
    let (aa,ab)=(a.clone().abs(),b.clone().abs());
    let lo = if *a<0 && *b>0 {qi(0)} else if aa<=ab {aa.clone()} else {ab.clone()};
    let hi = if aa>=ab {aa} else {ab};
    if hi>qi(1) { return qi(1); }
    let l2=Q::from(&lo*&lo); let h2=Q::from(&hi*&hi);
    let c=Q::from(&(qi(1)-&l2)/&(qi(1)+&l2)); let s=Q::from(&Q::from(&hi*2)/&(qi(1)+&h2));
    if c>=s {c} else {s}
}
pub fn concave_ok(bx: &[Q;6], a: &Q, b: &Q, concave: &(char,Q)) -> bool {
    let (kind,ua)=concave; let h=half_w_max(a,b);
    match kind {
        'x'=>bx[0]>=*ua && Q::from(&bx[2]-&h)>=*ua,
        'y'=>bx[2]>=*ua && Q::from(&bx[0]-&h)>=*ua,
        // 'b' = the Python reference 'xy' (SPEC.md §5.5): center inside both edges and x0 + y0 - D >= 2·UA, so the two cut-offs are disjoint
        'b'=>bx[0]>=*ua && bx[2]>=*ua && Q::from(&Q::from(&bx[0]+&bx[2])-&diag_max(a,b))>=Q::from(ua*2),
        // 'h' = the Python reference 'xyh' (SPEC.md §5.5): center inside both edges (no disjointness needed, inclusion-exclusion lower bound)
        'h'=>bx[0]>=*ua && bx[2]>=*ua,
        'X'=>bx[1]<=*ua && bx[2]>=*ua, // TxHy
        'Y'=>bx[3]<=*ua && bx[0]>=*ua, // TyHx
        _=>false,
    }
}

/// Python reference tangent_ok: equality belongs to the permitted side.
pub fn tangent_ok(bx: &[Q;6], a: &Q, b: &Q, tangent: &(char,Q)) -> bool {
    let (kind,ua)=tangent; let h=half_w_max(a,b);
    match kind {
        'x'=>bx[1]<=*ua && Q::from(&bx[2]-&h)>=*ua,
        'y'=>bx[3]<=*ua && Q::from(&bx[0]-&h)>=*ua,
        _=>false,
    }
}

type Tangent = (char,Q,Q,Q);
/// Python reference tangent_term. Area first, chord second, in the same guard context.
fn tangent_term(t: &Tangent, px: &RF, py: &RF, fr: &Frame, ctx: &mut Ctx) -> R<RF> {
    let (kind,a,cs,co)=t;
    let (vs,line,x,y,p)=if *kind=='x' {
        (vec![(a.clone(),qi(-1000)),(qi(1000),qi(-1000)),(qi(1000),qi(1000)),(a.clone(),qi(1000))],
         ((a.clone(),qi(-1000)),(a.clone(),qi(1000)),qi(2000)),RF::konst(cs),RF::konst(co),px)
    } else {
        (vec![(qi(-1000),a.clone()),(qi(1000),a.clone()),(qi(1000),qi(1000)),(qi(-1000),qi(1000))],
         ((qi(-1000),a.clone()),(qi(1000),a.clone()),qi(2000)),RF::konst(co),RF::konst(cs),py)
    };
    let area=poly_mass(&vs,&x,&y,fr,ctx)?;
    let xn=fr.normals.iter().map(|(n0,n1)|n0.mul(&x).add(&n1.mul(&y))).collect::<Vec<_>>();
    let chord=point_mass(&[pseg_const(fr,&line)],&xn,ctx)?;
    Ok(area.add(&chord.mul(&p.sub(&RF::konst(cs)))))
}

/// Store point_mass segments with sample- and center-independent terms precomputed.
/// Python: num = HALF − (n0·(A0 − x) + n1·(A1 − y)), den = n0·d0 + n1·d1 (d = B − A).
/// Here num = kn[k] + xn[k], where kn[k] = HALF − n0·A0 − n1·A1 and xn[k] = n0·x + n1·y.
/// RF's unique reduced form gives Python's (n, d) for equal values, preserving comparison order, signs, and guards.
pub struct PSeg {
    kn: Vec<RF>,
    den: Vec<RF>,
    w: RF,
}

fn kn_of(fr: &Frame, ax: &Q, ay: &Q) -> Vec<RF> {
    let half = RF::konst(&Q::from((1, 2)));
    fr.normals.iter().map(|(n0, n1)| half.sub(&n0.mulq(ax).add(&n1.mulq(ay)))).collect()
}

fn pseg_const(fr: &Frame, s: &(Pt, Pt, Q)) -> PSeg {
    let ((ax, ay), (bx, by), w) = s;
    let dx = Q::from(bx - ax);
    let dy = Q::from(by - ay);
    PSeg {
        kn: kn_of(fr, ax, ay),
        den: fr.normals.iter().map(|(n0, n1)| n0.mulq(&dx).add(&n1.mulq(&dy))).collect(),
        w: RF::konst(w),
    }
}

/// solver.point_mass for segments only. xn[k] = n0·x + n1·y for normal k and center (x, y); all comparisons record guards via ctx.sign.
/// None represents the initial Python ints t0 = 0 and t1 = 1; comparisons between ints create no guards.
fn point_mass(segs: &[PSeg], xn: &[RF], ctx: &mut Ctx) -> R<RF> {
    let one = RF::ki(1);
    let mut m = RF::ki(0);
    for sg in segs {
        let mut t0: Option<RF> = None;
        let mut t1: Option<RF> = None;
        let mut empty = false;
        for k in 0..4 {
            let num = sg.kn[k].add(&xn[k]);
            let den = &sg.den[k];
            if den.is_zero() {
                if ctx.sign(&num)? < 0 {
                    empty = true;
                    break;
                }
            } else if ctx.sign(den)? > 0 {
                let q = num.div(den)?;
                let less = match &t1 {
                    None => ctx.sign(&q.sub(&one))? < 0,
                    Some(t) => ctx.sign(&q.sub(t))? < 0,
                };
                if less {
                    t1 = Some(q);
                }
            } else {
                let q = num.div(den)?;
                let greater = match &t0 {
                    None => ctx.sign(&q)? > 0,
                    Some(t) => ctx.sign(&q.sub(t))? > 0,
                };
                if greater {
                    t0 = Some(q);
                }
            }
            // t1 <= t0
            let le = match (&t1, &t0) {
                (None, None) => false,                           // 1 <= 0 (both ints).
                (None, Some(b)) => ctx.sign(&b.sub(&one))? >= 0, // 1 <= t0 → t0.__ge__(1)
                (Some(a), None) => ctx.sign(a)? <= 0,            // t1 <= 0
                (Some(a), Some(b)) => ctx.sign(&a.sub(b))? <= 0,
            };
            if le {
                empty = true;
                break;
            }
        }
        if !empty {
            let tt1 = t1.unwrap_or_else(|| one.clone());
            let len = match &t0 {
                None => tt1,
                Some(b) => tt1.sub(b),
            };
            m = m.add(&sg.w.mul(&len));
        }
    }
    Ok(m)
}

// ================================================================ Three-dimensional certification

pub struct B3In<'a> {
    pub vsegs: &'a [(Q, Q, Q)],
    pub polys: Vec<Vec<Pt>>,
    pub pf: Vec<PSeg>,
    pub pt: Vec<PSeg>,
    pub vkn: Vec<Vec<RF>>,
    pub fr: Frame,
}

/// mass3: F at center (x, y) + T0 at (x − d, y) + V on [x_l, 2 + d] × {y_V}, with mass ρ·(2 + d − x_l).
/// Evaluate the three point_mass terms in this order, matching Python's comparison order.
fn mass3(inp: &B3In, x: &RF, y: &RF, d: &RF, ctx: &mut Ctx) -> R<RF> {
    prof!("mass3");
    let nm = &inp.fr.normals;
    let xn: Vec<RF> = nm.iter().map(|(n0, n1)| n0.mul(x).add(&n1.mul(y))).collect();
    let mut m = point_mass(&inp.pf, &xn, ctx)?;
    for pl in inp.polys.iter() { m = m.add(&poly_mass(pl, x, y, &inp.fr, ctx)?); }
    let xd = x.sub(d);
    let xnt: Vec<RF> = nm.iter().map(|(n0, n1)| n0.mul(&xd).add(&n1.mul(y))).collect();
    m = m.add(&point_mass(&inp.pt, &xnt, ctx)?);
    let xr = RF::ki(crate::w0()).add(d);      // Right endpoint of V: w₀ + d (default w₀ = 2).
    let mut vs = Vec::with_capacity(inp.vsegs.len());
    for ((xl, _yv, rho), kn) in inp.vsegs.iter().zip(inp.vkn.iter()) {
        let dx = xr.sub(&RF::konst(xl)); // B − A = (w₀ + d − x_l, 0)
        vs.push(PSeg { kn: kn.clone(), den: nm.iter().map(|(n0, _)| n0.mul(&dx)).collect(), w: dx.mulq(rho) });
    }
    m = m.add(&point_mass(&vs, &xn, ctx)?);
    Ok(m)
}

fn check_value3(inp: &B3In, pt: &(RF, RF, RF), av: &Alg, bv: &Alg, smp: Q, thr: &Q, tangent: Option<&Tangent>) -> R<bool> {
    prof!("check_value3");
    let mut pieces: Vec<(Alg, Alg, Q)> = vec![(av.clone(), bv.clone(), smp)];
    while let Some((a1, b1, mut s1)) = pieces.pop() {
        let mut got: Option<(RF, Ctx)> = None;
        for attempt in 0..60 {
            let mut ctx = Ctx::new(s1.clone());
            let value = (|| {
                let v=mass3(inp, &pt.0, &pt.1, &pt.2, &mut ctx)?;
                match tangent {
                    Some(t)=>Ok(v.add(&tangent_term(t,&pt.0,&pt.1,&inp.fr,&mut ctx)?)),
                    None=>Ok(v),
                }
            })();
            match value {
                Ok(v) => {
                    got = Some((v, ctx));
                    break;
                }
                Err(BErr::Resample) => {
                    s1 = if attempt % 2 == 1 {
                        between(&alg_rat(s1.clone()), &b1)?
                    } else {
                        between(&a1, &alg_rat(s1.clone()))?
                    };
                }
                Err(e) => return Err(e),
            }
        }
        let (v, ctx) = match got {
            None => return Ok(false),
            Some(x) => x,
        };
        let mut brk = Vec::new();
        for g in ctx.guards.iter() {
            brk.extend(roots_in_alg(g, &a1, &b1)?);
        }
        let brk = sorted_unique(brk)?;
        if !brk.is_empty() {
            let mut ends = vec![a1.clone()];
            ends.extend(brk);
            ends.push(b1.clone());
            for w in ends.windows(2) {
                let s = between(&w[0], &w[1])?;
                pieces.push((w[0].clone(), w[1].clone(), s));
            }
            continue;
        }
        let pol = v.n.sub(&v.d.mul_q(thr)).mul(&v.d);
        if !nonneg_open(&pol, &a1, &b1)? {
            return Ok(false);
        }
    }
    Ok(true)
}

pub struct B3Out {
    pub ok: bool,
    pub why: String,
    pub planes: usize,
    pub dropped: usize,
    pub triples: usize,
    pub values: usize,
    pub edge_runs: Option<usize>,
    pub triple: Option<(usize, usize, usize)>,
    pub at: Option<String>,
}

type Plane = [RF; 4];

/// certify3: fcov and tcov contain scaled cover segments with w > 0; box = (x0, x1, y0, y1, e0, e1).
#[allow(clippy::too_many_arguments)]
pub fn certify3(
    fcov: &[(Pt, Pt, Q)],
    tcov: &[(Pt, Pt, Q)],
    vsegs: &[(Q, Q, Q)],
    side: &Q,
    bx: &[Q; 6],
    a: &Q,
    b: &Q,
    thr: &Q,
    concave: Option<(char, Q)>,
    tangent: Option<(char, Q)>,
) -> R<B3Out> {
    certify3_impl(fcov, tcov, vsegs, side, bx, a, b, thr, concave, tangent, None)
}

#[allow(clippy::too_many_arguments)]
fn certify3_impl(
    fcov: &[(Pt, Pt, Q)],
    tcov: &[(Pt, Pt, Q)],
    vsegs: &[(Q, Q, Q)],
    side: &Q,
    bx: &[Q; 6],
    a: &Q,
    b: &Q,
    thr: &Q,
    concave: Option<(char, Q)>,
    tangent: Option<(char, Q)>,
    general: Option<&[Pt]>,
) -> R<B3Out> {
    let _sturm_scope = SturmScope::new();
    let [x0, x1, y0, y1, e0, e1] = bx;
    let tan_full = if let Some(ref t)=tangent {
        if *thr!=1 || concave.is_some() {return Err(BErr::Assert("tangent requires thr == 1 and concave == None".into()));}
        if !tangent_ok(bx,a,b,t) {
            return Ok(B3Out {ok:false,why:"tangent-cond".into(),planes:0,dropped:0,
                            triples:0,values:0,edge_runs:None,triple:None,at:None});
        }
        Some(if t.0=='x' {(t.0,t.1.clone(),Q::from(x0+x1)/2,y0.clone())}
             else {(t.0,t.1.clone(),Q::from(y0+y1)/2,x0.clone())})
    } else {None};
    let mut loc_f = local(fcov, x0, x1, y0, y1);
    let polys = if let Some(vs) = general {
        add_general_u(&mut loc_f, bx, vs)?;
        vec![vs.to_vec()]
    } else if let Some(ref c) = concave {
        // 'h' = the Python reference 'xyh' (SPEC.md §5.5): two half-planes {x >= a}, {y >= a} of density 1, threshold 2
        let vs = if c.0=='h' {
            if *thr != 2 { return Err(BErr::Assert("concave xyh requires thr == 2".into())); }
            vec![add_half(&mut loc_f,&c.1,side,'x'), add_half(&mut loc_f,&c.1,side,'y')]
        } else {
            if *thr != 1 { return Err(BErr::Assert("concave requires thr == 1".into())); }
            vec![add_u(&mut loc_f,bx,&c.1,side)?]
        };
        if !concave_ok(bx,a,b,c) {
            return Ok(B3Out {ok:false,why:"concave-cond".into(),planes:0,dropped:0,
                            triples:0,values:0,edge_runs:None,triple:None,at:None});
        }
        vs
    } else {Vec::new()};
    let loc_t = local(tcov, &Q::from(x0 - e1), &Q::from(x1 - e0), y0, y1);
    if general.is_some() {
        validate_b4u(&loc_f, &loc_t, &polys.iter().cloned().map(|v| (v,qi(1))).collect::<Vec<_>>(), &[])?;
    }
    let pos = a.cmp0() != Ordering::Less;
    if !(pos || b.cmp0() != Ordering::Greater) {
        return Err(BErr::Assert(String::new()));
    }
    #[cfg(feature = "prof")]
    let _g0 = prof::G::new("cand");
    let fr = frame()?;
    let k = RF::konst;
    let k0 = RF::ki(0);
    let k1 = RF::ki(1);
    let halfq = Q::from((1, 2));
    let lo = if pos { fr.c.add(&fr.s).half() } else { fr.c.sub(&fr.s).half() };
    let hi = RF::konst(side).sub(&lo);
    let mut cand: Vec<Plane> = Vec::new();
    for (la, lb, lk) in loc_f.lines.iter() {
        for (vx, vy) in fr.verts.iter() {
            cand.push([k(la), k(lb), k0.clone(), k(lk).sub(&vx.mulq(la)).sub(&vy.mulq(lb))]);
        }
    }
    for (la, lb, lk) in loc_t.lines.iter() {
        for (vx, vy) in fr.verts.iter() {
            cand.push([k(la), k(lb), k(&Q::from(-la)), k(lk).sub(&vx.mulq(la)).sub(&vy.mulq(lb))]);
        }
    }
    let bp_k = |n: &(RF, RF), px: &Q, py: &Q| n.0.mulq(px).add(&n.1.mulq(py)).sub(&k(&halfq));
    for pt in loc_f.bps.iter() {
        for n in fr.normals.iter() {
            cand.push([n.0.clone(), n.1.clone(), k0.clone(), bp_k(n, &pt.0, &pt.1)]);
        }
    }
    for pt in loc_t.bps.iter() {
        for n in fr.normals.iter() {
            cand.push([n.0.clone(), n.1.clone(), n.0.neg(), bp_k(n, &pt.0, &pt.1)]);
        }
    }
    for (xl, yv, _rho) in vsegs.iter() {
        for (_vx, vy) in fr.verts.iter() {
            cand.push([k0.clone(), k1.clone(), k0.clone(), k(yv).sub(vy)]);
        }
        for n in fr.normals.iter() {
            cand.push([n.0.clone(), n.1.clone(), k0.clone(), bp_k(n, xl, yv)]);
            cand.push([n.0.clone(), n.1.clone(), n.0.neg(), bp_k(n, &qi(crate::w0()), yv)]);   // Moving endpoint (w₀ + δ, yv).
        }
    }
    let mut lpl: Vec<Plane> = vec![
        [k1.clone(), k0.clone(), k0.clone(), k(x0)],
        [k1.clone(), k0.clone(), k0.clone(), k(x1)],
        [k0.clone(), k1.clone(), k0.clone(), k(y0)],
        [k0.clone(), k1.clone(), k0.clone(), k(y1)],
        [k0.clone(), k0.clone(), k1.clone(), k(e0)],
        [k0.clone(), k0.clone(), k1.clone(), k(e1)],
        [k1.clone(), k0.clone(), k0.clone(), lo.clone()],
        [k1.clone(), k0.clone(), k0.clone(), hi.clone()],
        [k0.clone(), k1.clone(), k0.clone(), lo.clone()],
        [k0.clone(), k1.clone(), k0.clone(), hi.clone()],
    ];
    let mut corners = Vec::new();
    for px in [x0, x1] {
        for py in [y0, y1] {
            for pd in [e0, e1] {
                corners.push((px.clone(), py.clone(), pd.clone()));
            }
        }
    }
    let strict_sign = |p: &P| -> i32 {
        if p.is_zero() || !root_free(p, a, b) {
            return 0;
        }
        if p.sign_at(a) > 0 {
            1
        } else {
            -1
        }
    };
    let mut seen: HashSet<Plane> = HashSet::new();
    let mut dropped = 0usize;
    for l in cand.into_iter() {
        if seen.contains(&l) {
            continue;
        }
        seen.insert(l.clone());
        let ss: Vec<i32> = corners
            .iter()
            .map(|q| strict_sign(&l[0].mulq(&q.0).add(&l[1].mulq(&q.1)).add(&l[2].mulq(&q.2)).sub(&l[3]).sign_poly()))
            .collect();
        if ss.iter().all(|&x| x == 1) || ss.iter().all(|&x| x == -1) {
            dropped += 1;
            continue;
        }
        lpl.push(l);
    }
    #[cfg(feature = "prof")]
    drop(_g0);
    let a0 = alg_rat(a.clone());
    let b0 = alg_rat(b.clone());
    let inp = B3In {
        polys,
        vsegs,
        pf: loc_f.segs.iter().map(|sg| pseg_const(&fr, sg)).collect(),
        pt: loc_t.segs.iter().map(|sg| pseg_const(&fr, sg)).collect(),
        vkn: vsegs.iter().map(|(xl, yv, _)| kn_of(&fr, xl, yv)).collect(),
        fr,
    };
    let (x0r, x1r, y0r, y1r, e0r, e1r) = (k(x0), k(x1), k(y0), k(y1), k(e0), k(e1));
    let mut ntrip = 0usize;
    let mut nvals = 0usize;
    let n = lpl.len();
    for i in 0..n {
        let [a1, b1, g1, k1_] = &lpl[i];
        for j in (i + 1)..n {
            let [a2, b2, g2, k2] = &lpl[j];
            let cr0 = b1.mul(g2).sub(&g1.mul(b2));
            let cr1 = g1.mul(a2).sub(&a1.mul(g2));
            let cr2 = a1.mul(b2).sub(&b1.mul(a2));
            if cr0.is_zero() && cr1.is_zero() && cr2.is_zero() {
                continue;
            }
            for kk in (j + 1)..n {
                let [a3, b3, g3, k3] = &lpl[kk];
                // det = a1 (b2 g3 − g2 b3) − b1 (a2 g3 − g2 a3) + g1 (a2 b3 − b2 a3)
                prof!("triple_rf");
                let m_bg = b2.mul(g3).sub(&g2.mul(b3));
                let m_ag = a2.mul(g3).sub(&g2.mul(a3));
                let m_ab = a2.mul(b3).sub(&b2.mul(a3));
                let det = a1.mul(&m_bg).sub(&b1.mul(&m_ag)).add(&g1.mul(&m_ab));
                if det.is_zero() {
                    continue;
                }
                let m_kg = k2.mul(g3).sub(&g2.mul(k3));
                let m_kb = k2.mul(b3).sub(&b2.mul(k3));
                let m_ak = a2.mul(k3).sub(&k2.mul(a3));
                let m_bk = b2.mul(k3).sub(&k2.mul(b3));
                let dx = k1_.mul(&m_bg).sub(&b1.mul(&m_kg)).add(&g1.mul(&m_kb));
                let dy = a1.mul(&m_kg).sub(&k1_.mul(&m_ag)).add(&g1.mul(&m_ak));
                let dd = a1.mul(&m_bk).sub(&b1.mul(&m_ak)).add(&k1_.mul(&m_ab));
                let px = dx.div(&det)?;
                let py = dy.div(&det)?;
                let pd = dd.div(&det)?;
                let conds = [
                    px.sub(&x0r),
                    x1r.sub(&px),
                    py.sub(&y0r),
                    y1r.sub(&py),
                    pd.sub(&e0r),
                    e1r.sub(&pd),
                    px.sub(&lo),
                    hi.sub(&px),
                    py.sub(&lo),
                    hi.sub(&py),
                ];
                let polys: Vec<P> = conds.iter().map(|v| v.sign_poly()).collect();
                if polys.iter().any(|p| !p.is_zero() && root_free(p, a, b) && p.sign_at(a) < 0) {
                    continue;
                }
                ntrip += 1;
                prof!("triple_brk");
                let mut brk = Vec::new();
                for p in polys.iter() {
                    brk.extend(roots_in(p, a, b)?);
                }
                brk.extend(roots_in(&det.sign_poly(), a, b)?);
                let mut ends = vec![a0.clone()];
                ends.extend(sorted_unique(brk)?);
                ends.push(b0.clone());
                let pt = (px, py, pd);
                for w in ends.windows(2) {
                    let smp = between(&w[0], &w[1])?;
                    if !polys.iter().all(|p| p.sign_at(&smp) >= 0) {
                        continue;
                    }
                    let ok = check_value3(&inp, &pt, &w[0], &w[1], smp.clone(), thr, tan_full.as_ref())?;
                    if !ok {
                        return Ok(B3Out {
                            ok: false,
                            why: "value".into(),
                            planes: 0,
                            dropped: 0,
                            triples: 0,
                            values: 0,
                            edge_runs: None,
                            triple: Some((i, j, kk)),
                            at: Some(smp.to_string()),
                        });
                    }
                    nvals += 1;
                }
            }
        }
    }
    let edge_runs = if general.is_some() {
        let (ok, why, at, runs) = edge_chain(&inp, &lpl, bx, &lo, &hi, a, b)?;
        if !ok {
            return Ok(B3Out { ok, why: format!("edge:{why}"), at, edge_runs: None,
                planes: 0, dropped: 0, triples: 0, values: 0, triple: None });
        }
        Some(runs)
    } else { None };
    Ok(B3Out {
        ok: true,
        why: String::new(),
        planes: n,
        dropped,
        triples: ntrip,
        values: nvals,
        edge_runs,
        triple: None,
        at: None,
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn tangent_conditions_and_contract() {
        let bx=[qi(0),qi(1),Q::from((3,2)),qi(2),qi(0),qi(1)];
        assert!(tangent_ok(&bx,&qi(0),&qi(0),&('x',qi(1))));
        let mut outside=bx.clone(); outside[1]+=Q::from((1,1000000));
        assert!(!tangent_ok(&outside,&qi(0),&qi(0),&('x',qi(1))));
        outside=bx.clone(); outside[2]-=Q::from((1,1000000));
        assert!(!tangent_ok(&outside,&qi(0),&qi(0),&('x',qi(1))));
        let by=[bx[2].clone(),bx[3].clone(),bx[0].clone(),bx[1].clone(),qi(0),qi(1)];
        assert!(tangent_ok(&by,&qi(0),&qi(0),&('y',qi(1))));
        assert!(!tangent_ok(&by,&qi(0),&qi(0),&('z',qi(1))));
        for (thr,concave) in [(qi(0),None),(qi(1),Some(('x',qi(1))))] {
            assert!(matches!(certify3(&[],&[],&[],&qi(20),&bx,&qi(0),&qi(1),&thr,concave,Some(('x',qi(1)))),Err(BErr::Assert(_))));
        }
        let r=certify3(&[],&[],&[],&qi(20),&outside,&qi(0),&qi(0),&qi(1),None,Some(('x',qi(1)))).unwrap();
        assert!(!r.ok); assert_eq!(r.why,"tangent-cond");
    }

    #[test]
    fn concave_conditions_exact_boundaries() {
        let mut bx=[qi(1),qi(2),Q::from((3,2)),qi(2),qi(0),qi(1)];
        assert_eq!(half_w_max(&qi(0),&qi(0)),Q::from((1,2)));
        assert_eq!(half_w_max(&Q::from((-2,5)),&qi(0)),Q::from((41,58)));
        assert_eq!(half_w_max(&qi(0),&Q::from((401,1000))),Q::from((7072,10000)));
        assert!(concave_ok(&bx,&qi(0),&qi(0),&('x',qi(1))));
        bx[2]-=Q::from((1,1000000));
        assert!(!concave_ok(&bx,&qi(0),&qi(0),&('x',qi(1))));
        bx[0]=Q::from((3,2)); bx[2]=qi(1);
        assert!(concave_ok(&bx,&qi(0),&qi(0),&('y',qi(1))));
        assert!(!concave_ok(&bx,&qi(0),&qi(0),&('z',qi(1))));
    }

    #[test]
    fn clip_closed_boundary_and_symbolic_guard() {
        let k=RF::ki;
        let poly=vec![(k(0),k(0)),(k(1),k(0)),(k(1),k(1)),(k(0),k(1))];
        let mut ctx=Ctx::new(Q::from((1,4)));
        let clipped=clip(&poly,&qi(1),&qi(0),&qi(0),&mut ctx).unwrap();
        assert_eq!(clipped.len(),2); // Boundary vertices kept, no spurious intersections.
        assert!(area(&clipped).is_zero());
        let shifted=poly.iter().map(|(x,y)|(x.add(&RF::var()),y.clone())).collect::<Vec<_>>();
        let clipped=clip(&shifted,&qi(1),&qi(0),&qi(1),&mut ctx).unwrap();
        assert_eq!(area(&clipped),k(1).sub(&RF::var()));
        assert!(!ctx.guards.is_empty());
        let mut at_root=Ctx::new(qi(0));
        assert!(matches!(clip(&shifted,&qi(1),&qi(0),&qi(1),&mut at_root),Err(BErr::Resample)));
    }

    #[test]
    fn local_u_includes_all_vertices_and_unnormalized_edges() {
        let bx=[qi(1),qi(2),qi(2),qi(3),qi(0),qi(1)];
        let mut loc=local(&[],&bx[0],&bx[1],&bx[2],&bx[3]);
        let vs=add_u(&mut loc,&bx,&qi(1),&qi(20)).unwrap();
        assert_eq!(vs.len(),4); assert_eq!(loc.bps.len(),4);
        assert!(loc.bps.contains(&(qi(20),qi(20))));
        assert!(loc.lines.contains(&(qi(0),qi(-19),qi(-19))));
    }

    fn pz(v: &[i64]) -> P {
        P::from_parts(v.iter().map(|&x| Integer::from(x)).collect(), Integer::from(1))
    }
    #[test]
    fn sturm_cache_exact_and_scoped() {
        let p = pz(&[-2, 0, 1]);
        let expected = sturm_uncached(&p);
        assert!(STURM_CACHE.with(|c| c.borrow().is_none()));
        {
            let _scope = SturmScope::new();
            assert_eq!(sturm(&p), expected);
            // Returned vectors are independent, just as Alg refinement must be.
            let mut modified = sturm(&p);
            modified[0] = P::zero();
            assert_eq!(sturm(&p), expected);
            let scaled = p.mul_q(&Q::from((2, 3)));
            assert_eq!(sturm(&scaled), sturm_uncached(&scaled));
            {
                let _nested = SturmScope::new();
                assert!(STURM_CACHE.with(|c| c.borrow().as_ref().unwrap().is_empty()));
                sturm(&pz(&[1, 1]));
            }
            assert_eq!(STURM_CACHE.with(|c| c.borrow().as_ref().unwrap().len()), 2);
            // Eviction affects work only, not the exact sequence.
            for i in 1..260 { sturm(&pz(&[i, 1])); }
            assert_eq!(sturm(&p), expected);
        }
        assert!(STURM_CACHE.with(|c| c.borrow().is_none()));
        let _ = std::panic::catch_unwind(|| {
            let _scope = SturmScope::new();
            sturm(&p);
            panic!("scope cleanup");
        });
        assert!(STURM_CACHE.with(|c| c.borrow().is_none()));
    }

    #[test]
    fn gcd_div() {
        let a = pz(&[2, 4]);
        let b = pz(&[6, 12, 6]);
        assert_eq!(gcd(&a, &b), P::one());
        assert_eq!(gcd(&P::zero(), &b), pz(&[1, 2, 1]));
        let (q, r) = divrem(&pz(&[1, 0, 0, 1]), &pz(&[1, 2]));
        // x^3 + 1 = (x + 1/2)(...) ...
        let back = q.mul(&pz(&[1, 2])).add(&r);
        assert_eq!(back, pz(&[1, 0, 0, 1]));
        assert!(r.deg() < 1);
    }
    #[test]
    fn rootfree() {
        // (x − 1/3): no roots in [0, 1/4]; inconclusive on [0, 1/2].
        let p = pz(&[-1, 3]);
        assert!(root_free(&p, &qi(0), &Q::from((1, 4))));
        assert!(!root_free(&p, &qi(0), &Q::from((1, 2))));
        let iv = isolate(&pz(&[-2, 0, 1]), &qi(0), &qi(2));
        assert_eq!(iv.len(), 1);
    }
}

/// Family-level U contribution for CORE1.
#[derive(Clone, Debug)]
pub enum Core1UTerm {
    None,
    PolyU,
    PolyH,
    Tan(char, Q, Q, Q),
    /// Tangent at the box midpoint, plus the opposite half-plane.
    TanHalf(char),
    /// Same contribution with the caller's explicit tangent center (Python API).
    TanHalfAt(char, Q, Q),
}

/// Python ('poly', locP) / ('tan', tangent), after resolving family geometry.
pub enum Core1Term {
    None,
    Poly(Vec<Vec<Pt>>),
    Tan(Tangent),
    TanHalf(Tangent, Vec<Pt>),
}

/// Python _seg_h: keep negative widths and closed-boundary zero widths.
fn seg_h(a: &(RF, RF), b: &(RF, RF), x: &RF, y: &RF,
         normals: &[(RF, RF)], ctx: &mut Ctx) -> R<Option<RF>> {
    let d = (b.0.sub(&a.0), b.1.sub(&a.1));
    let (mut t0, mut t1) = (RF::ki(0), RF::ki(1));
    for (nx, ny) in normals {
        let num = RF::ki(1).half().sub(&nx.mul(&a.0.sub(x)).add(&ny.mul(&a.1.sub(y))));
        let den = nx.mul(&d.0).add(&ny.mul(&d.1));
        if ctx.sign(&den)? == 0 {
            if ctx.sign(&num)? < 0 { return Ok(None); }
        } else if ctx.sign(&den)? > 0 {
            let q = num.div(&den)?;
            if ctx.sign(&q.sub(&t1))? < 0 { t1 = q; }
        } else {
            let q = num.div(&den)?;
            if ctx.sign(&q.sub(&t0))? > 0 { t0 = q; }
        }
    }
    Ok(Some(t1.sub(&t0)))
}

/// Python core1_value; corners are ordered x, then y, then delta.
pub fn core1_value(loc_f: &Loc, loc_t: &Loc, vsegs: &[(Q, Q, Q)],
                   corners: &[(RF, RF, RF); 8], fr: &Frame,
                   uterm: &Core1Term, ctx: &mut Ctx) -> R<Vec<RF>> {
    let mut hs = Vec::new();
    for (loc, moving) in [(loc_f, false), (loc_t, true)] {
        for (a, b, w) in &loc.segs {
            let a = (RF::konst(&a.0), RF::konst(&a.1));
            let b = (RF::konst(&b.0), RF::konst(&b.1));
            let mut hv = Vec::new();
            for (px, py, pd) in corners {
                let x = if moving { px.sub(pd) } else { px.clone() };
                match seg_h(&a, &b, &x, py, &fr.normals, ctx)? {
                    Some(h) if ctx.sign(&h)? >= 0 => hv.push(h),
                    _ => break,
                }
            }
            if hv.len() == 8 { hs.push((w, hv)); }
        }
    }
    let mut vh = Vec::new();
    for (xl, yv, rho) in vsegs {
        let mut hv = Vec::new();
        for (px, py, pd) in corners {
            let a = (RF::konst(xl), RF::konst(yv));
            let b = (RF::ki(crate::w0()).add(pd), RF::konst(yv));
            match seg_h(&a, &b, px, py, &fr.normals, ctx)? {
                Some(h) if ctx.sign(&h)? >= 0 => hv.push(h.mulq(rho).mul(&b.0.sub(&a.0))),
                _ => break,
            }
        }
        if hv.len() == 8 { vh.push(hv); }
    }
    let mut pts_w = qi(0);
    'points: for (qx, qy, w) in &loc_f.pts {
        for (px, py, _) in corners {
            for (nx, ny) in &fr.normals {
                let v = nx.mul(&RF::konst(qx).sub(px)).add(&ny.mul(&RF::konst(qy).sub(py)));
                if ctx.sign(&v.sub(&RF::ki(1).half()))? > 0 { continue 'points; }
            }
        }
        pts_w += w;
    }
    let mut vals = Vec::new();
    for (k, (px, py, _)) in corners.iter().enumerate() {
        let mut v = RF::konst(&pts_w);
        for (w, hv) in &hs { v = v.add(&hv[k].mulq(w)); }
        for hv in &vh { v = v.add(&hv[k]); }
        match uterm {
            Core1Term::None => {},
            Core1Term::Poly(polys) => for poly in polys { v = v.add(&poly_mass(poly, px, py, fr, ctx)?); },
            Core1Term::Tan(t) => v = v.add(&tangent_term(t, px, py, fr, ctx)?),
            Core1Term::TanHalf(t, poly) => {
                // Python combo order matters for the shared guard context.
                v = v.add(&tangent_term(t, px, py, fr, ctx)?);
                v = v.add(&poly_mass(poly, px, py, fr, ctx)?);
            },
        }
        vals.push(v);
    }
    Ok(vals)
}

/// Python certify_core1, sharing certify3's exact guards and root machinery.
#[allow(clippy::too_many_arguments)]
pub fn certify_core1(loc_f: &Loc, loc_t: &Loc, vsegs: &[(Q, Q, Q)], side: &Q,
                     bx: &[Q; 6], a: &Q, b: &Q, thr: &Q, uterm: &Core1Term) -> R<B3Out> {
    let _sturm_scope = SturmScope::new();
    if *a < 0 && *b > 0 { return Err(BErr::Assert("CORE1 contains u=0".into())); }
    let mut out = B3Out { ok: false, why: String::new(), planes: 0, dropped: 0,
        triples: 0, values: 0, edge_runs: None, triple: None, at: None };
    let h = half_w_max(a, b);
    let hi = Q::from(side - &h);
    if bx[0] < h || bx[2] < h || bx[1] > hi || bx[3] > hi {
        out.why = "core1-domain".into(); return Ok(out);
    }
    let corners = std::array::from_fn(|i| (RF::konst(&bx[i / 4]),
        RF::konst(&bx[2 + (i / 2) % 2]), RF::konst(&bx[4 + i % 2])));
    let fr = frame()?;
    let (av, bv) = (alg_rat(a.clone()), alg_rat(b.clone()));
    let smp = between(&av, &bv)?;
    let mut pieces = vec![(av, bv, smp)];
    while let Some((a1, b1, mut s1)) = pieces.pop() {
        let mut got = None;
        for attempt in 0..60 {
            let mut ctx = Ctx::new(s1.clone());
            match core1_value(loc_f, loc_t, vsegs, &corners, &fr, uterm, &mut ctx) {
                Ok(vals) => { got = Some((vals, ctx)); break; },
                Err(BErr::Resample) => {
                    s1 = if attempt % 2 == 1 { between(&alg_rat(s1), &b1)? }
                         else { between(&a1, &alg_rat(s1))? };
                },
                Err(e) => return Err(e),
            }
        }
        let (vals, ctx) = match got {
            Some(v) => v,
            None => { out.why = "resample".into(); return Ok(out); },
        };
        let mut brk = Vec::new();
        for g in &ctx.guards { brk.extend(roots_in_alg(g, &a1, &b1)?); }
        let brk = sorted_unique(brk)?;
        if !brk.is_empty() {
            let mut ends = vec![a1]; ends.extend(brk); ends.push(b1);
            for w in ends.windows(2) {
                pieces.push((w[0].clone(), w[1].clone(), between(&w[0], &w[1])?));
            }
            continue;
        }
        for v in vals {
            let pol = v.n.sub(&v.d.mul_q(thr)).mul(&v.d);
            if !nonneg_open(&pol, &a1, &b1)? {
                out.why = "value".into(); out.at = Some(s1.to_string()); return Ok(out);
            }
            out.values += 1;
        }
    }
    out.ok = true;
    Ok(out)
}

impl super::FamilyCore {
    #[allow(clippy::too_many_arguments)]
    pub fn certify_core1(&self, bx: &[Q; 6], a: &Q, b: &Q, thr: &Q, scale: &Q,
                         uterm: Core1UTerm) -> R<B3Out> {
        let fc = Self::cover(&self.f_raw, scale);
        let tc = Self::cover(&self.t_raw, scale);
        let vs = self.v.iter().map(|(xl,y,rho)| (xl.clone(),y.clone(),Q::from(rho*scale))).collect::<Vec<_>>();
        let loc_f = local(&fc, &bx[0], &bx[1], &bx[2], &bx[3]);
        let loc_t = local(&tc, &Q::from(&bx[0]-&bx[5]), &Q::from(&bx[1]-&bx[4]), &bx[2], &bx[3]);
        // Polygon-only Local in Python: no spatial filtering. add_u's filtering is
        // specific to certify3, so PolyU uses the family's actual U polygon.
        let uterm = match uterm {
            Core1UTerm::TanHalf(k) => {
                let (cs,co) = if k=='x' {(Q::from(&bx[0]+&bx[1])/2,bx[2].clone())}
                              else {(Q::from(&bx[2]+&bx[3])/2,bx[0].clone())};
                Core1UTerm::TanHalfAt(k,cs,co)
            },
            other => other,
        };
        let term = match uterm {
            Core1UTerm::None => Core1Term::None,
            Core1UTerm::PolyU => Core1Term::Poly(vec![self.u_lower.clone()]),
            Core1UTerm::PolyH => {
                let mut loc = local(&[], &bx[0], &bx[1], &bx[2], &bx[3]);
                Core1Term::Poly(vec![add_half(&mut loc, &self.ua, &qi(20), 'x'),
                                     add_half(&mut loc, &self.ua, &qi(20), 'y')])
            },
            Core1UTerm::Tan(k,a,cs,co) => Core1Term::Tan((k,a,cs,co)),
            Core1UTerm::TanHalfAt(k,cs,co) => {
                let opposite = match k {
                    'x' => 'y', 'y' => 'x',
                    _ => return Err(BErr::Assert("tan_half kind must be x or y".into())),
                };
                let mut loc = local(&[], &bx[0], &bx[1], &bx[2], &bx[3]);
                Core1Term::TanHalf((k,self.ua.clone(),cs,co),
                    add_half(&mut loc, &self.ua, &qi(20), opposite))
            },
            Core1UTerm::TanHalf(_) => unreachable!(),
        };
        certify_core1(&loc_f, &loc_t, &vs, &qi(20), bx, a, b, thr, &term)
    }
}

#[cfg(test)]
mod core1_tests {
    use super::*;
    fn empty() -> Loc { local(&[], &qi(0), &qi(4), &qi(0), &qi(4)) }
    fn axis_frame() -> Frame {
        Frame { c: RF::ki(1), s: RF::ki(0),
            verts: [(-1,-1),(1,-1),(1,1),(-1,1)].iter()
                .map(|(x,y)| (RF::konst(&Q::from((*x,2))),RF::konst(&Q::from((*y,2))))).collect(),
            normals: vec![(RF::ki(1), RF::ki(0)), (RF::ki(0), RF::ki(1)),
                          (RF::ki(-1), RF::ki(0)), (RF::ki(0), RF::ki(-1))] }
    }
    #[test]
    fn core1_family_poly_threshold_domain_and_zero() {
        let f = super::super::load_family_text(r#"{"d0":0,"d1":1,"UA":1,"F":[],"T":[],"V":[]}"#).unwrap();
        let bx = [qi(2),qi(3),qi(2),qi(3),qi(0),qi(1)];
        for (a,b) in [(qi(0),Q::from((1,10))), (Q::from((-1,10)),qi(0))] {
            let r = f.certify_core1(&bx,&a,&b,&qi(1),&qi(1),Core1UTerm::PolyU).unwrap();
            assert!(r.ok); assert_eq!(r.values,8);
            let r = f.certify_core1(&bx,&a,&b,&Q::from((1001,1000)),&qi(1),Core1UTerm::PolyU).unwrap();
            assert!(!r.ok); assert_eq!(r.why,"value");
            assert!(f.certify_core1(&bx,&a,&b,&qi(2),&qi(1),Core1UTerm::PolyH).unwrap().ok);
            for i in 0..4 {
                let mut outside = bx.clone(); outside[i] = if i%2==0 {qi(0)} else {qi(20)};
                let r = f.certify_core1(&outside,&a,&b,&qi(1),&qi(1),Core1UTerm::PolyU).unwrap();
                assert!(!r.ok); assert_eq!(r.why,"core1-domain");
            }
        }
        assert!(matches!(f.certify_core1(&bx,&Q::from((-1,10)),&Q::from((1,10)),&qi(1),&qi(1),Core1UTerm::None),Err(BErr::Assert(_))));
    }
    #[test]
    fn core1_tan_half_hand_values_and_conditions() {
        let f = super::super::load_family_text(r#"{"d0":0,"d1":1,"UA":1,"F":[],"T":[],"V":[]}"#).unwrap();
        for (k,condition) in [('x','X'),('y','Y')] {
            let mut bx = [Q::from((4,5)),Q::from((9,10)),qi(1),Q::from((11,10)),qi(0),qi(1)];
            if k=='y' { bx.swap(0,2); bx.swap(1,3); }
            let opposite = if k=='x' {'y'} else {'x'};
            let poly = add_half(&mut empty(),&qi(1),&qi(20),opposite);
            let term = Core1Term::TanHalf((k,qi(1),Q::from((17,20)),qi(1)),poly);
            let corners = std::array::from_fn(|i| (RF::konst(&bx[i/4]),RF::konst(&bx[2+(i/2)%2]),RF::konst(&bx[4+i%2])));
            let vals = core1_value(&empty(),&empty(),&[],&corners,&axis_frame(),&term,&mut Ctx::new(qi(0))).unwrap();
            // Python combo at u=0: tangent = outside_center - 1/2,
            // opposite half area = inside_center - 1/2; hence x+y-1.
            for (i,v) in vals.iter().enumerate() {
                assert_eq!(*v,RF::konst(&(Q::from(&bx[i/4]+&bx[2+(i/2)%2])-1)));
            }
            for (a,b) in [(qi(0),Q::from((1,10))),(Q::from((-1,10)),qi(0))] {
                assert!(concave_ok(&bx,&a,&b,&(condition,qi(1))));
                let r = f.certify_core1(&bx,&a,&b,&qi(2),&qi(1),Core1UTerm::TanHalf(k)).unwrap();
                assert!(!r.ok); assert_eq!(r.why,"value");
                assert!(f.certify_core1(&bx,&a,&b,&qi(0),&qi(1),Core1UTerm::TanHalf(k)).unwrap().ok);
                let (outer_hi,inner_lo) = if k=='x' {(1,2)} else {(3,0)};
                let mut edge = bx.clone(); edge[outer_hi]=qi(1);
                assert!(concave_ok(&edge,&a,&b,&(condition,qi(1))));
                edge[outer_hi]=Q::from((101,100));
                assert!(!concave_ok(&edge,&a,&b,&(condition,qi(1))));
                edge=bx.clone(); edge[inner_lo]=Q::from((99,100));
                assert!(!concave_ok(&edge,&a,&b,&(condition,qi(1))));
            }
        }
    }

    #[test]
    fn core1_closed_width_and_parallel_miss() {
        let fr = axis_frame(); let mut ctx = Ctx::new(qi(0));
        let p = |x,y| (RF::ki(x),RF::ki(y));
        let h = seg_h(&p(1,0),&p(2,0),&RF::ki(0),&RF::ki(0),&fr.normals,&mut ctx).unwrap().unwrap();
        assert_eq!(h, RF::konst(&Q::from((-1,2))));
        assert!(seg_h(&p(0,1),&p(1,1),&RF::ki(0),&RF::ki(0),&fr.normals,&mut ctx).unwrap().is_none());
        let h = seg_h(&p(0,0),&p(1,0),&RF::konst(&Q::from((3,2))),&RF::ki(0),&fr.normals,&mut ctx).unwrap().unwrap();
        assert!(h.is_zero());
    }
    #[test]
    fn core1_common_pieces_translation_v_and_points() {
        let mut f = empty(); let mut t = empty();
        f.segs = vec![((qi(0),qi(0)),(qi(4),qi(0)),qi(4)),
                      ((qi(0),qi(0)),(qi(1),qi(0)),qi(100))];
        t.segs = vec![((qi(0),qi(0)),(qi(2),qi(0)),qi(4))];
        f.pts = vec![(Q::from((3,2)),qi(0),qi(3)),(qi(1),qi(0),qi(100))];
        let corners = std::array::from_fn(|i| (RF::ki(if i/4==0 {1} else {2}), RF::ki(0),RF::ki(1)));
        let vals = core1_value(&f,&t,&[(qi(0),qi(0),qi(2))],&corners,&axis_frame(),&Core1Term::None,&mut Ctx::new(qi(0))).unwrap();
        // First F: 1, rejected F: 0; T: 1 or 2 after translation;
        // V: length 1 times density 2; common boundary point: 3.
        for (i,v) in vals.iter().enumerate() { assert_eq!(*v,RF::ki(if i<4 {7} else {8})); }
    }
    #[test]
    fn core1_guard_resampling_and_splitting() {
        let f = local(&[((qi(0),qi(2)),(qi(4),qi(2)),qi(8))],&qi(2),&qi(2),&qi(2),&qi(2));
        let bx = [qi(2),qi(2),qi(2),qi(2),qi(0),qi(0)];
        // At u=1 a normal is parallel to the segment only at the sample:
        // Resample must move it, then the guard root splits the interval.
        let r = certify_core1(&f,&empty(),&[],&qi(20),&bx,&Q::from((9,10)),&Q::from((11,10)),&qi(1),&Core1Term::None).unwrap();
        assert!(r.ok); assert!(r.values>=16);
    }
}

/// Local's polygon selection uses the same conservative rational reach as its segments.
fn add_general_u(loc: &mut Loc, bx: &[Q; 6], vs: &[Pt]) -> R<()> {
    let reach = Q::from((7072, 10000));
    if vs.len() < 3 || vs.iter().all(|p| p.0 < Q::from(&bx[0]-&reach))
        || vs.iter().all(|p| p.0 > Q::from(&bx[1]+&reach))
        || vs.iter().all(|p| p.1 < Q::from(&bx[2]-&reach))
        || vs.iter().all(|p| p.1 > Q::from(&bx[3]+&reach)) {
        return Err(BErr::Assert("B4U: expected one local U polygon".into()));
    }
    for (p,r) in vs.iter().zip(vs.iter().cycle().skip(1)) {
        let a=Q::from(&r.1-&p.1); let b=Q::from(&p.0-&r.0);
        loc.lines.push((a.clone(),b.clone(),Q::from(&a*&p.0)+Q::from(&b*&p.1)));
        loc.bps.push(p.clone());
    }
    loc.lines.sort(); loc.lines.dedup(); loc.bps.sort(); loc.bps.dedup();
    Ok(())
}

/// Preconditions (a), (b), (c) and the common no-points requirement.
/// Family preparation supplies density one and an empty T polygon list explicitly.
fn validate_b4u(f: &Loc, t: &Loc, polys: &[(Vec<Pt>,Q)], tpolys: &[(Vec<Pt>,Q)]) -> R<()> {
    if !tpolys.is_empty() || polys.len()!=1 || polys[0].1!=1 {
        return Err(BErr::Assert("B4U: expected one density-one F polygon and no T polygon".into()));
    }
    if !f.pts.is_empty() || !t.pts.is_empty() {
        return Err(BErr::Assert("B4U: points".into()));
    }
    let vs=&polys[0].0;
    for (p,r) in vs.iter().zip(vs.iter().cycle().skip(1)) {
        let a=Q::from(&r.1-&p.1); let b=Q::from(&p.0-&r.0);
        if !f.lines.contains(&(a.clone(),b.clone(),Q::from(&a*&p.0)+Q::from(&b*&p.1))) || !f.bps.contains(p) {
            return Err(BErr::Assert("B4U: missing polygon boundary".into()));
        }
    }
    Ok(())
}

impl crate::FamilyCore {
    /// B4U: retain the actual family U, with density one, without a concavity test.
    /// The threshold parameter supports the specified direct negative test; replay fixes it to one.
    pub fn certify_b4u(&self, bx: &[Q;6], a: &Q, b: &Q, thr: &Q) -> R<B3Out> {
        if a >= b || (0..6).step_by(2).any(|i| bx[i]>=bx[i+1]) {
            return Err(BErr::Assert("B4U: nonpositive box interval".into()));
        }
        let fc=Self::cover(&self.f_raw,&qi(1));
        let tc=Self::cover(&self.t_raw,&qi(1));
        certify3_impl(&fc,&tc,&self.v,&qi(20),bx,a,b,thr,None,None,Some(&self.u_lower))
    }
}

type EdgePt = (RF, RF, RF);
fn cross_planes(p: &Plane, q: &Plane) -> [RF;3] {
    [p[1].mul(&q[2]).sub(&p[2].mul(&q[1])),
     p[2].mul(&q[0]).sub(&p[0].mul(&q[2])),
     p[0].mul(&q[1]).sub(&p[1].mul(&q[0]))]
}
fn intersection(p: &Plane, q: &Plane, r: &Plane) -> R<Option<EdgePt>> {
    let c=cross_planes(q,r);
    let det=p[0].mul(&c[0]).add(&p[1].mul(&c[1])).add(&p[2].mul(&c[2]));
    if det.is_zero() { return Ok(None); }
    let kg=q[3].mul(&r[2]).sub(&q[2].mul(&r[3]));
    let kb=q[3].mul(&r[1]).sub(&q[1].mul(&r[3]));
    let ak=q[0].mul(&r[3]).sub(&q[3].mul(&r[0]));
    let x=p[3].mul(&c[0]).sub(&p[1].mul(&kg)).add(&p[2].mul(&kb));
    let y=p[0].mul(&kg).add(&p[3].mul(&c[1])).add(&p[2].mul(&ak));
    let z=p[0].mul(&kb.neg()).sub(&p[1].mul(&ak)).add(&p[3].mul(&c[2]));
    Ok(Some((x.div(&det)?,y.div(&det)?,z.div(&det)?)))
}
fn edge_in_r(p: &EdgePt, bx: &[Q;6], lo: &RF, hi: &RF, ctx: &mut Ctx) -> R<bool> {
    // Python's box lower bound uses reflected RF.__ge__, while the wall
    // lower bound is RF.__le__. Preserve operands as well as short circuits.
    for (v,l,h) in [(&p.0,&bx[0],&bx[1]),(&p.1,&bx[2],&bx[3]),(&p.2,&bx[4],&bx[5])] {
        if ctx.sign(&v.sub(&RF::konst(l)))?<0 || ctx.sign(&v.sub(&RF::konst(h)))?>0 {return Ok(false);}
    }
    for v in [&p.0,&p.1] {
        if ctx.sign(&lo.sub(v))?>0 || ctx.sign(&v.sub(hi))?>0 {return Ok(false);}
    }
    Ok(true)
}

fn edge_mass(inp: &B3In, p: &EdgePt, ctx: &mut Ctx, cache: &mut HashMap<EdgePt,RF>, poly: bool) -> R<RF> {
    if let Some(v)=cache.get(p) {return Ok(v.clone());}
    let v=if poly {
        let mut v=RF::ki(0);
        for pl in &inp.polys {v=v.add(&poly_mass(pl,&p.0,&p.1,&inp.fr,ctx)?);}
        v
    } else {mass3(inp,&p.0,&p.1,&p.2,ctx)?};
    cache.insert(p.clone(),v.clone()); Ok(v)
}
/// Lemma B4': quadratic critical values on adjacent arrangement-edge segments.
#[cfg(test)]
fn edge_runner3(inp: &B3In, planes: &[Plane], bx: &[Q;6], lo: &RF, hi: &RF, ctx: &mut Ctx) -> R<Vec<RF>> {
    edge_runner3_cached(inp,planes,bx,lo,hi,ctx,&mut HashMap::new())
}

type Intersections = HashMap<[usize;3],Option<EdgePt>>;
fn edge_runner3_cached(inp: &B3In, planes: &[Plane], bx: &[Q;6], lo: &RF, hi: &RF,
                       ctx: &mut Ctx, intersections: &mut Intersections) -> R<Vec<RF>> {
    let mut membership=HashMap::new();
    let mut out=Vec::new(); let mut cache=HashMap::new(); let mut gcache=HashMap::new();
    for i in 0..planes.len() { for j in i+1..planes.len() {
        let d=cross_planes(&planes[i],&planes[j]);
        if d.iter().all(RF::is_zero) {continue;}
        let mut pts=Vec::new();
        for k in 0..planes.len() {
            if k==i || k==j {continue;}
            let mut key=[i,j,k]; key.sort();
            // Intersections are symbolic and sample-independent. Membership is not:
            // cache it only within this Ctx, retaining the first occurrence's guards.
            if !intersections.contains_key(&key) {
                intersections.insert(key,intersection(&planes[i],&planes[j],&planes[k])?);
            }
            if let Some(p)=&intersections[&key] {
                let inside=if let Some(inside)=membership.get(&key) {*inside} else {
                    let inside=edge_in_r(p,bx,lo,hi,ctx)?;
                    membership.insert(key,inside); inside
                };
                if inside {pts.push(p.clone());}
            }
        }
        if pts.len()<2 {continue;}
        let key=|p: &EdgePt| p.0.mul(&d[0]).add(&p.1.mul(&d[1])).add(&p.2.mul(&d[2]));
        let mut keyed: Vec<(RF,EdgePt)>=pts.into_iter().map(|p|(key(&p),p)).collect();
        edge_sort(&mut keyed,ctx)?;
        for w in keyed.windows(2) {
            let (p,q)=(&w[0].1,&w[1].1); if p==q {continue;}
            let m=(p.0.add(&q.0).half(),p.1.add(&q.1).half(),p.2.add(&q.2).half());
            let gp=edge_mass(inp,p,ctx,&mut gcache,true)?;
            let gm=edge_mass(inp,&m,ctx,&mut gcache,true)?;
            let gq=edge_mass(inp,q,ctx,&mut gcache,true)?;
            let aa=gp.sub(&gm.mulq(&qi(2))).add(&gq).mulq(&qi(2));
            if ctx.sign(&aa)? > 0 {
                let fp=edge_mass(inp,p,ctx,&mut cache,false)?;
                let fq=edge_mass(inp,q,ctx,&mut cache,false)?;
                let bb=fq.sub(&fp).sub(&aa);
                let t=bb.neg().div(&aa.mulq(&qi(2)))?;
                if ctx.sign(&t)? > 0 && ctx.sign(&t.sub(&RF::ki(1)))? < 0 {
                    out.push(fp.add(&bb.mul(&t)).add(&aa.mul(&t).mul(&t)));
                }
            }
        }
    }}
    Ok(out)
}

#[path = "b3d_sort.rs"]
mod edge_sort_impl;
fn edge_sort(items: &mut [(RF,EdgePt)],ctx: &mut Ctx) -> R<()> {
    edge_sort_impl::sort(items,|a,b|Ok(ctx.sign(&a.0.sub(&b.0))?<0))
}

/// Lemmas B1/B2: traverse the root-free component containing each guarded run.
fn edge_chain(inp: &B3In, planes: &[Plane], bx: &[Q;6], lo: &RF, hi: &RF,
              a: &Q, b: &Q) -> R<(bool,String,Option<String>,usize)> {
    let mut intersections=HashMap::new();
    edge_chain_run(a,b,2000,|ctx|edge_runner3_cached(inp,planes,bx,lo,hi,ctx,&mut intersections))
}

fn edge_chain_run<F>(a: &Q, b: &Q, max_runs: usize, mut run: F) -> R<(bool,String,Option<String>,usize)>
where F: FnMut(&mut Ctx) -> R<Vec<RF>> {
    // Python reference chain: caps and failed samples are not completed runs.
    let mut frontier=alg_rat(a.clone()); let mut runs=0;
    loop {
        if { let f=frontier.borrow(); f.p.is_none() && f.l==*b } {break;}
        let mut cap=b.clone();
        let (sample, vals, l, r)=loop {
            while {let f=frontier.borrow(); f.p.is_some() && f.r>=cap} {
                frontier.borrow_mut().refine();
            }
            let lo=frontier.borrow().r.clone();
            let mut sample=Q::from(&lo+&cap)/2u32;
            let mut success=None;
            for _ in 0..60 {
                let mut ctx=Ctx::new(sample.clone());
                match run(&mut ctx) {
                    Ok(vals)=>{success=Some((ctx,vals));break;},
                    Err(BErr::Resample)=>sample=&lo+Q::from(&sample-&lo)*Q::from((2,3)),
                    Err(e)=>return Err(e),
                }
            }
            let (ctx,vals)=match success {
                Some(v)=>v,
                None=>return Ok((false,"resample".into(),Some(sample.to_string()),runs)),
            };
            // guard_roots preserves guard/isolation order (no sorting/dedup).
            // Unlike the Python reference roots_in, it strips zero only when a == 0.
            let mut roots=Vec::new();
            for guard in &ctx.guards {
                let g=if *a==0 {strip0(guard)} else {guard.clone()};
                if g.deg()<=0 || root_free(&g,a,b) {continue;}
                let sq=squarefree(&g);
                for (lo,hi) in roots_open(&sq,a,b) {
                    let root=alg_new(sq.clone(),lo,hi.clone())?;
                    roots.push(if sq.sign_at(&hi)==0 {alg_rat(hi)} else {root});
                }
            }
            let s=alg_rat(sample.clone()); let mut l=alg_rat(a.clone()); let mut r=alg_rat(b.clone());
            for root in roots {
                let c=alg_cmp(&root,&s)?;
                if c<0 && alg_cmp(&root,&l)?>0 {l=root;}
                else if c>0 && alg_cmp(&root,&r)?<0 {r=root;}
            }
            if alg_cmp(&l,&frontier)?<=0 {break (sample,vals,l,r);}
            while {let ll=l.borrow(); ll.p.is_some() && ll.l<=frontier.borrow().r} {
                l.borrow_mut().refine();
                if frontier.borrow().p.is_some() {frontier.borrow_mut().refine();}
            }
            cap=l.borrow().l.clone();
            if runs+1>=max_runs {return Ok((false,"max_runs".into(),None,runs));}
        };
        let mut ok=true;
        for v in vals {
            if !nonneg_open_impl(&v.n.sub(&v.d).mul(&v.d),&l,&r,true)? {ok=false;break;}
        }
        runs+=1; // Python appends the failed value run as well.
        if !ok {return Ok((false,"value".into(),Some(sample.to_string()),runs));}
        frontier=r;
        if runs>=max_runs {return Ok((false,"max_runs".into(),None,runs));}
    }
    Ok((true,String::new(),None,runs))
}

#[cfg(test)]
mod b4u_tests {
    use super::*;
    #[test]
    fn edge_chain_algebraic_components_resampling_and_limit() {
        let mut samples=Vec::new();
        let result=edge_chain_run(&qi(0),&qi(1),2000,|ctx| {
            samples.push(ctx.u.clone());
            let u=RF::var();
            ctx.sign(&u.mul(&u).sub(&RF::konst(&Q::from((1,2)))))?;
            Ok(vec![RF::ki(1)])
        }).unwrap();
        assert!(result.0); assert_eq!(result.3,2);
        assert_eq!(samples,vec![Q::from((1,2)),Q::from((7,8))]);
        let result=edge_chain_run(&qi(0),&qi(1),2000,|ctx| {
            let s=ctx.sign(&RF::var().sub(&RF::konst(&Q::from((1,2)))))?;
            Ok(vec![RF::ki(if s<0 {1} else {0})])
        }).unwrap();
        assert!(!result.0); assert_eq!(result.1,"value"); // right component cannot be skipped
        assert_eq!(result.2,Some("3/4".into())); assert_eq!(result.3,2);
        let mut retries=0;
        let result=edge_chain_run(&qi(0),&qi(1),2,|_|{retries+=1;Err(BErr::Resample)}).unwrap();
        assert!(!result.0); assert_eq!(result.1,"resample");
        assert_eq!(result.3,0); assert_eq!(retries,60);
        assert_eq!(result.2,Some("576460752303423488/42391158275216203514294433201".into()));
        // Python checks the completed-run limit even when R == b.
        let result=edge_chain_run(&qi(0),&qi(1),1,|_|Ok(vec![RF::ki(1)])).unwrap();
        assert_eq!(result,(false,"max_runs".into(),None,1));
        // Approaching a component does not consume the completed-run budget.
        let mut samples=Vec::new();
        let result=edge_chain_run(&qi(0),&qi(1),2000,|ctx| {
            samples.push(ctx.u.clone());
            ctx.sign(&RF::var().sub(&RF::konst(&Q::from((1,4)))))?;
            Ok(vec![RF::ki(1)])
        }).unwrap();
        assert!(result.0);assert_eq!(result.3,2);
        assert_eq!(samples,vec![Q::from((1,2)),Q::from((1,8)),Q::from((5,8))]);
    }

    #[test]
    fn all_b4u_preconditions_fail_closed() {
        let bx=[qi(1),qi(2),qi(1),qi(2),qi(0),qi(1)];
        let empty=||local(&[],&bx[0],&bx[1],&bx[2],&bx[3]);
        let mut f=empty(); let mut t=empty();
        let vs=add_u(&mut f,&bx,&qi(1),&qi(20)).unwrap();
        let one=vec![(vs.clone(),qi(1))];
        assert!(validate_b4u(&f,&t,&one,&[]).is_ok());
        assert!(validate_b4u(&f,&t,&[],&[]).is_err());
        assert!(validate_b4u(&f,&t,&[one[0].clone(),one[0].clone()],&[]).is_err());
        assert!(validate_b4u(&f,&t,&[(vs,qi(2))],&[]).is_err());
        assert!(validate_b4u(&f,&t,&one,&one).is_err());
        let line=f.lines.pop().unwrap();
        assert!(validate_b4u(&f,&t,&one,&[]).is_err()); f.lines.push(line);
        let point=f.bps.pop().unwrap();
        assert!(validate_b4u(&f,&t,&one,&[]).is_err()); f.bps.push(point);
        f.pts.push((qi(1),qi(1),qi(1)));
        assert!(validate_b4u(&f,&t,&one,&[]).is_err()); f.pts.clear();
        t.pts.push((qi(1),qi(1),qi(1)));
        assert!(validate_b4u(&f,&t,&one,&[]).is_err());
    }

    #[test]
    fn edge_critical_value_below_both_endpoints() {
        let k=RF::konst;
        let fr=Frame { c: RF::ki(1), s: RF::ki(0),
            verts: [(-1,-1),(1,-1),(1,1),(-1,1)].iter()
                .map(|(x,y)| (k(&Q::from((*x,2))),k(&Q::from((*y,2))))).collect(),
            normals: vec![(RF::ki(1),RF::ki(0)),(RF::ki(0),RF::ki(1)),
                (RF::ki(-1),RF::ki(0)),(RF::ki(0),RF::ki(-1))] };
        let y=Q::from((3,4));
        let segments=vec![((qi(-1),y.clone()),(qi(1),y.clone()),qi(1)),
                          ((qi(-1),y.clone()),(qi(3),y),qi(2))];
        let inp=B3In { vsegs:&[], polys:vec![vec![(qi(1),qi(1)),(qi(20),qi(1)),
            (qi(20),qi(20)),(qi(1),qi(20))]],
            pf:segments.iter().map(|sg| pseg_const(&fr,sg)).collect(),pt:vec![],vkn:vec![],fr };
        let half=Q::from((1,2));
        let bx=[half.clone(),qi(1),half.clone(),qi(1),qi(0),qi(1)];
        let planes=vec![ [RF::ki(1),RF::ki(-1),RF::ki(0),RF::ki(0)],
            [RF::ki(0),RF::ki(0),RF::ki(1),RF::ki(0)],
            [RF::ki(1),RF::ki(0),RF::ki(0),k(&half)],
            [RF::ki(1),RF::ki(0),RF::ki(0),RF::ki(1)] ];
        let mut ctx=Ctx::new(Q::from((1,10)));
        for x in [half.clone(),qi(1)] {
            assert_eq!(mass3(&inp,&k(&x),&k(&x),&RF::ki(0),&mut ctx).unwrap(),RF::ki(1));
        }
        let values=edge_runner3(&inp,&planes,&bx,&k(&half),&RF::ki(19),&mut ctx).unwrap();
        assert_eq!(values,vec![k(&Q::from((15,16)))]);
        let (ok,why,_,_)=edge_chain(&inp,&planes,&bx,&k(&half),&RF::ki(19),&qi(0),&Q::from((1,10))).unwrap();
        assert!(!ok); assert_eq!(why,"value");
    }
}
