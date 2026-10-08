//! Exact integers with an allocation-free common case. Every arithmetic operation
//! is checked; overflow uses GMP and every GMP result is reduced back when it fits.
use rug::{Integer, ops::DivRounding};
use std::borrow::Cow;
use std::cmp::Ordering;
use std::ops::{Add, Div, Mul, Neg, Sub};

#[derive(Clone, Debug, Eq, PartialEq)]
/// An exact integer backed by i128 when possible and GMP otherwise.
pub struct Int(Repr);
#[derive(Clone, Debug, Eq, PartialEq)]
enum Repr {
    Small(i128),
    Big(Integer),
}
impl From<Integer> for Int {
    fn from(n: Integer) -> Self {
        match n.to_i128() {
            Some(v) => Self(Repr::Small(v)),
            None => Self(Repr::Big(n)),
        }
    }
}
impl From<&Integer> for Int {
    fn from(n: &Integer) -> Self {
        match n.to_i128() {
            Some(v) => Self(Repr::Small(v)),
            None => Self(Repr::Big(n.clone())),
        }
    }
}
impl From<i32> for Int {
    fn from(n: i32) -> Self {
        Self(Repr::Small(n.into()))
    }
}
impl From<i128> for Int {
    fn from(n: i128) -> Self {
        Self(Repr::Small(n))
    }
}
impl From<Int> for Integer {
    fn from(n: Int) -> Self {
        match n.0 {
            Repr::Small(v) => v.into(),
            Repr::Big(v) => v,
        }
    }
}
impl Int {
    fn big(&self) -> Cow<'_, Integer> {
        match &self.0 {
            Repr::Small(v) => Cow::Owned((*v).into()),
            Repr::Big(v) => Cow::Borrowed(v),
        }
    }
    /// Compare a*b with c*d without allocating even when i128 products overflow.
    #[must_use]
    pub fn cmp_products(a: &Self, b: &Self, c: &Self, d: &Self) -> Ordering {
        if let (Repr::Small(a), Repr::Small(b), Repr::Small(c), Repr::Small(d)) =
            (&a.0, &b.0, &c.0, &d.0)
        {
            if let (Some(x), Some(y)) = (a.checked_mul(*b), c.checked_mul(*d)) {
                return x.cmp(&y);
            }
            let negative_x = *a != 0 && *b != 0 && (*a < 0) != (*b < 0);
            let negative_y = *c != 0 && *d != 0 && (*c < 0) != (*d < 0);
            if negative_x != negative_y {
                return if negative_x {
                    Ordering::Less
                } else {
                    Ordering::Greater
                };
            }
            let order = wide_product(a.unsigned_abs(), b.unsigned_abs())
                .cmp(&wide_product(c.unsigned_abs(), d.unsigned_abs()));
            return if negative_x { order.reverse() } else { order };
        }
        Integer::from(&*a.big() * &*b.big()).cmp(&Integer::from(&*c.big() * &*d.big()))
    }
    /// Return the nonnegative greatest common divisor.
    #[must_use]
    pub fn gcd(self, other: &Self) -> Self {
        if let (Repr::Small(a), Repr::Small(b)) = (&self.0, &other.0) {
            let (mut a, mut b) = (a.unsigned_abs(), b.unsigned_abs());
            if let (Ok(mut x), Ok(mut y)) = (u64::try_from(a), u64::try_from(b)) {
                while y != 0 {
                    (x, y) = (y, x % y);
                }
                return i128::from(x).into();
            }
            while b != 0 {
                (a, b) = (b, a % b);
            }
            if let Ok(v) = i128::try_from(a) {
                return v.into();
            }
        }
        Integer::from(self.big().gcd_ref(&other.big())).into()
    }
    /// Divide exactly with rounding toward negative infinity; the divisor must be nonzero.
    #[must_use]
    pub fn div_floor(self, other: &Self) -> Self {
        if let (Repr::Small(a), Repr::Small(b)) = (&self.0, &other.0)
            && let Some(q) = a.checked_div(*b)
        {
            let r = a % b;
            return (if r != 0 && (r < 0) != (*b < 0) {
                q - 1
            } else {
                q
            })
            .into();
        }
        self.big().into_owned().div_floor(&*other.big()).into()
    }
}
// Exact 128 x 128 -> 256 bit multiplication. Each partial product is 64 x 64.
// Low-word overflow is explicitly propagated; the high sum cannot exceed u128::MAX.
fn wide_product(a: u128, b: u128) -> (u128, u128) {
    let mask = u128::from(u64::MAX);
    let (al, ah, bl, bh) = (a & mask, a >> 64, b & mask, b >> 64);
    let (p00, p01, p10, p11) = (al * bl, al * bh, ah * bl, ah * bh);
    let (low, carry1) = p00.overflowing_add(p01 << 64);
    let (low, carry2) = low.overflowing_add(p10 << 64);
    let high = p11 + (p01 >> 64) + (p10 >> 64) + u128::from(carry1) + u128::from(carry2);
    (high, low)
}
impl Ord for Int {
    fn cmp(&self, rhs: &Self) -> Ordering {
        match (&self.0, &rhs.0) {
            (Repr::Small(a), Repr::Small(b)) => a.cmp(b),
            (Repr::Big(a), Repr::Big(b)) => a.cmp(b),
            (Repr::Big(a), Repr::Small(b)) => a
                .partial_cmp(b)
                .expect("GMP integer and i128 comparisons are total"),
            (Repr::Small(a), Repr::Big(b)) => b
                .partial_cmp(a)
                .expect("GMP integer and i128 comparisons are total")
                .reverse(),
        }
    }
}
impl PartialOrd for Int {
    fn partial_cmp(&self, rhs: &Self) -> Option<Ordering> {
        Some(self.cmp(rhs))
    }
}
impl PartialEq<i32> for Int {
    fn eq(&self, rhs: &i32) -> bool {
        self == &Self::from(*rhs)
    }
}
impl PartialOrd<i32> for Int {
    fn partial_cmp(&self, rhs: &i32) -> Option<Ordering> {
        Some(self.cmp(&Self::from(*rhs)))
    }
}
macro_rules! binary {
    ($trait:ident, $method:ident, $checked:ident, $op:tt) => {
        impl $trait<&Int> for &Int {
            type Output = Int;
            fn $method(self, rhs: &Int) -> Int {
                if let (Repr::Small(a), Repr::Small(b)) = (&self.0, &rhs.0) {
                    if let Some(v) = a.$checked(*b) { return v.into(); }
                }
                Integer::from(&*self.big() $op &*rhs.big()).into()
            }
        }
        impl $trait<&Int> for Int {
            type Output = Int;
            fn $method(self, rhs: &Int) -> Int {
                if let (Repr::Small(a), Repr::Small(b)) = (&self.0, &rhs.0) {
                    if let Some(v) = a.$checked(*b) { return v.into(); }
                }
                (Integer::from(self) $op &*rhs.big()).into()
            }
        }
        impl $trait<Int> for Int { type Output = Int; fn $method(self, rhs: Int) -> Int { self.$method(&rhs) } }
        impl $trait<i32> for Int { type Output = Int; fn $method(self, rhs: i32) -> Int { (&self).$method(&Int::from(rhs)) } }
    }
}
binary!(Add, add, checked_add, +);
binary!(Sub, sub, checked_sub, -);
binary!(Mul, mul, checked_mul, *);
binary!(Div, div, checked_div, /);
impl Neg for Int {
    type Output = Int;
    fn neg(self) -> Int {
        if let Repr::Small(a) = &self.0
            && let Some(v) = a.checked_neg()
        {
            return v.into();
        }
        Integer::from(-&*self.big()).into()
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn arithmetic_matches_gmp_across_overflow_boundaries() {
        let mut values: Vec<Integer> = [
            i128::MIN,
            i128::MIN + 1,
            -2,
            -1,
            0,
            1,
            2,
            i128::MAX - 1,
            i128::MAX,
        ]
        .into_iter()
        .map(Integer::from)
        .collect();
        for bits in [63, 64, 126, 127, 128, 129, 200, 512] {
            let n: Integer = Integer::from(1) << bits;
            values.extend([n.clone() - 1, n.clone(), n.clone() + 1, -n]);
        }
        for a in &values {
            let x = Int::from(a);
            assert_eq!(Integer::from(-x.clone()), -a.clone());
            for b in &values {
                let y = Int::from(b);
                assert_eq!(x.cmp(&y), a.cmp(b));
                for c in [-1, 0, 1, i128::MIN, i128::MAX] {
                    let z = Int::from(c);
                    assert_eq!(
                        Int::cmp_products(&x, &y, &z, &x),
                        Integer::from(a * b).cmp(&Integer::from(a * c))
                    );
                }
                assert_eq!(Integer::from(&x + &y), Integer::from(a + b));
                assert_eq!(Integer::from(&x - &y), Integer::from(a - b));
                assert_eq!(Integer::from(&x * &y), Integer::from(a * b));
                assert_eq!(Integer::from(x.clone().gcd(&y)), a.clone().gcd(b));
                if b != &0 {
                    assert_eq!(Integer::from(&x / &y), Integer::from(a / b));
                    assert_eq!(
                        Integer::from(x.clone().div_floor(&y)),
                        a.clone().div_floor(b)
                    );
                }
            }
        }
        let big = Int::from(Integer::from(i128::MAX) + 1);
        assert!(matches!((big - 1).0, Repr::Small(i128::MAX)));
        let zero = Int::from(0);
        assert!(matches!(
            (Int::from(Integer::from(1) << 300) * zero).0,
            Repr::Small(0)
        ));
    }
}
