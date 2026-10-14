//! Canonical exact rationals with checked i128 arithmetic and arbitrary precision fallback.
use num_bigint::BigInt;
use num_rational::BigRational;
use num_traits::{One, Signed, ToPrimitive, Zero};
use std::{
    cmp::Ordering,
    fmt,
    hash::{Hash, Hasher},
    iter::Sum,
    ops::*,
};
#[derive(Clone, Debug)]
// Small values are coprime, have positive denominators, and exclude i128::MIN
// numerators. Big values cannot be represented by that canonical small form.
enum Repr {
    Small(i128, i128),
    Big(BigRational),
}
#[derive(Clone, Debug)]
pub struct Rational(Repr);
fn gcd(mut a: i128, mut b: i128) -> i128 {
    while b != 0 {
        let r = a % b;
        a = b;
        b = r;
    }
    a
}
impl Rational {
    fn small(n: i128, d: i128) -> Option<Self> {
        if d == 0 {
            panic!("zero rational denominator");
        }
        let (n, d) = if d < 0 {
            (n.checked_neg()?, d.checked_neg()?)
        } else {
            (n, d)
        };
        let g = gcd(n.checked_abs()?, d);
        Some(Self(Repr::Small(n / g, d / g)))
    }
    pub fn from_big(v: BigRational) -> Self {
        if let (Some(n), Some(d)) = (v.numer().to_i128(), v.denom().to_i128()) {
            if let Some(q) = Self::small(n, d) {
                return q;
            }
        }
        Self(Repr::Big(v))
    }
    pub fn big(&self) -> BigRational {
        match &self.0 {
            Repr::Small(n, d) => BigRational::new_raw((*n).into(), (*d).into()),
            Repr::Big(v) => v.clone(),
        }
    }
    pub fn new(n: BigInt, d: BigInt) -> Self {
        Self::from_big(BigRational::new(n, d))
    }
    pub fn from_integer(n: BigInt) -> Self {
        Self::from_big(BigRational::from_integer(n))
    }
    pub fn from_i64(n: i64) -> Self {
        Self(Repr::Small(n as i128, 1))
    }
    pub fn ratio(n: i64, d: i64) -> Self {
        Self::small(n as i128, d as i128).unwrap()
    }
    pub fn numer(&self) -> BigInt {
        match &self.0 {
            Repr::Small(n, _) => (*n).into(),
            Repr::Big(v) => v.numer().clone(),
        }
    }
    pub fn denom(&self) -> BigInt {
        match &self.0 {
            Repr::Small(_, d) => (*d).into(),
            Repr::Big(v) => v.denom().clone(),
        }
    }
    pub fn is_integer(&self) -> bool {
        match &self.0 {
            Repr::Small(_, d) => *d == 1,
            Repr::Big(v) => v.is_integer(),
        }
    }
    pub fn to_integer(&self) -> BigInt {
        match &self.0 {
            Repr::Small(n, d) => (*n / *d).into(),
            Repr::Big(v) => v.to_integer(),
        }
    }
    pub fn is_positive(&self) -> bool {
        match &self.0 {
            Repr::Small(n, _) => *n > 0,
            Repr::Big(v) => v.is_positive(),
        }
    }
    pub fn is_negative(&self) -> bool {
        match &self.0 {
            Repr::Small(n, _) => *n < 0,
            Repr::Big(v) => v.is_negative(),
        }
    }
    pub fn abs(&self) -> Self {
        if self.is_negative() {
            -self
        } else {
            self.clone()
        }
    }
    fn binary(&self, b: &Self, op: u8) -> Self {
        if let (Repr::Small(a, d), Repr::Small(c, e)) = (&self.0, &b.0) {
            let calc = || -> Option<Self> {
                match op {
                    0 | 1 => {
                        let g = gcd(*d, *e);
                        let l = e / g;
                        let r = d / g;
                        let x = a.checked_mul(l)?;
                        let y = c.checked_mul(r)?;
                        Self::small(
                            if op == 0 {
                                x.checked_add(y)?
                            } else {
                                x.checked_sub(y)?
                            },
                            d.checked_mul(l)?,
                        )
                    }
                    2 => {
                        let g = gcd(a.checked_abs()?, *e);
                        let h = gcd(c.checked_abs()?, *d);
                        Self::small((a / g).checked_mul(c / h)?, (d / h).checked_mul(e / g)?)
                    }
                    _ => {
                        if *c == 0 {
                            panic!("zero rational divisor");
                        }
                        let g = gcd(a.checked_abs()?, c.checked_abs()?);
                        let h = gcd(*d, *e);
                        Self::small((a / g).checked_mul(e / h)?, (d / h).checked_mul(c / g)?)
                    }
                }
            };
            if let Some(v) = calc() {
                return v;
            }
        }
        let (a, b) = (self.big(), b.big());
        Self::from_big(match op {
            0 => a + b,
            1 => a - b,
            2 => a * b,
            _ => a / b,
        })
    }
}
impl Default for Rational {
    fn default() -> Self {
        Self::zero()
    }
}
impl Zero for Rational {
    fn zero() -> Self {
        Self::from_i64(0)
    }
    fn is_zero(&self) -> bool {
        match &self.0 {
            Repr::Small(n, _) => *n == 0,
            Repr::Big(v) => v.is_zero(),
        }
    }
}
impl One for Rational {
    fn one() -> Self {
        Self::from_i64(1)
    }
}
impl PartialEq for Rational {
    fn eq(&self, b: &Self) -> bool {
        self.cmp(b) == Ordering::Equal
    }
}
impl Eq for Rational {}
impl PartialOrd for Rational {
    fn partial_cmp(&self, b: &Self) -> Option<Ordering> {
        Some(self.cmp(b))
    }
}
impl Ord for Rational {
    fn cmp(&self, b: &Self) -> Ordering {
        if let (Repr::Small(a, d), Repr::Small(c, e)) = (&self.0, &b.0) {
            if d == e {
                return a.cmp(c);
            }
            if let (Some(x), Some(y)) = (a.checked_mul(*e), c.checked_mul(*d)) {
                return x.cmp(&y);
            }
        }
        self.big().cmp(&b.big())
    }
}
// Construction always returns representable values to Small, so equal numbers
// cannot occupy different variants; hashing the tag is therefore consistent.
impl Hash for Rational {
    fn hash<H: Hasher>(&self, h: &mut H) {
        match &self.0 {
            Repr::Small(n, d) => {
                0u8.hash(h);
                n.hash(h);
                d.hash(h);
            }
            Repr::Big(v) => {
                1u8.hash(h);
                v.hash(h);
            }
        }
    }
}
impl fmt::Display for Rational {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match &self.0 {
            Repr::Small(n, 1) => write!(f, "{n}"),
            Repr::Small(n, d) => write!(f, "{n}/{d}"),
            Repr::Big(v) => v.fmt(f),
        }
    }
}
impl Neg for &Rational {
    type Output = Rational;
    fn neg(self) -> Rational {
        match &self.0 {
            Repr::Small(n, d) => Rational(Repr::Small(-n, *d)),
            Repr::Big(v) => Rational::from_big(-v),
        }
    }
}
impl Neg for Rational {
    type Output = Self;
    fn neg(self) -> Self {
        -&self
    }
}
macro_rules! op {
    ($trait:ident,$method:ident,$assign:ident,$am:ident,$code:expr) => {
        impl $trait<&Rational> for &Rational {
            type Output = Rational;
            fn $method(self, b: &Rational) -> Rational {
                self.binary(b, $code)
            }
        }
        impl $trait<Rational> for &Rational {
            type Output = Rational;
            fn $method(self, b: Rational) -> Rational {
                self.binary(&b, $code)
            }
        }
        impl $trait<&Rational> for Rational {
            type Output = Rational;
            fn $method(self, b: &Rational) -> Rational {
                self.binary(b, $code)
            }
        }
        impl $trait<Rational> for Rational {
            type Output = Rational;
            fn $method(self, b: Rational) -> Rational {
                self.binary(&b, $code)
            }
        }
        impl $assign<&Rational> for Rational {
            fn $am(&mut self, b: &Rational) {
                *self = self.binary(b, $code);
            }
        }
        impl $assign<Rational> for Rational {
            fn $am(&mut self, b: Rational) {
                *self = self.binary(&b, $code);
            }
        }
    };
}
op!(Add, add, AddAssign, add_assign, 0);
op!(Sub, sub, SubAssign, sub_assign, 1);
op!(Mul, mul, MulAssign, mul_assign, 2);
op!(Div, div, DivAssign, div_assign, 3);
impl Sum for Rational {
    fn sum<I: Iterator<Item = Self>>(i: I) -> Self {
        i.fold(Self::zero(), |a, b| a + b)
    }
}
impl<'a> Sum<&'a Rational> for Rational {
    fn sum<I: Iterator<Item = &'a Rational>>(i: I) -> Self {
        i.fold(Self::zero(), |a, b| a + b)
    }
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn random_and_overflow() {
        let mut seed = 47u64;
        let mut next = || {
            seed = seed.wrapping_mul(6364136223846793005).wrapping_add(1);
            (seed >> 32) as i64
        };
        for _ in 0..10000 {
            let a = Rational::ratio(next() % 100000 - 50000, next() % 10000 + 1);
            let b = Rational::ratio(next() % 100000 - 50000, next() % 10000 + 1);
            assert_eq!((&a + &b).big(), a.big() + b.big());
            assert_eq!((&a - &b).big(), a.big() - b.big());
            assert_eq!((&a * &b).big(), a.big() * b.big());
            if !b.is_zero() {
                assert_eq!((&a / &b).big(), a.big() / b.big());
            }
            assert_eq!(a.cmp(&b), a.big().cmp(&b.big()));
        }
        for n in [
            BigInt::from(i128::MIN),
            BigInt::from(i128::MAX),
            BigInt::one() << 300,
        ] {
            let a = Rational::from_integer(n);
            let b = &a * &a;
            assert_eq!(b.big(), a.big() * a.big());
            assert_eq!((&b + &a).big(), b.big() + a.big());
            assert_eq!((-&a).big(), -a.big());
            assert_eq!((&b / &a).big(), a.big());
        }
    }
}
