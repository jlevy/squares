//! Outward-rounded binary64 arithmetic.
//!
//! Every operation is evaluated in the hardware's round-to-nearest mode and the
//! result is then moved outward by at least one representable value. Lemma I1
//! of `SOUNDNESS.md` proves that `dn(fl(x)) <= x <= up(fl(x))` for every real `x`
//! whose rounding `fl(x)` is finite, so each helper here returns a valid bound
//! on the exact real result of its operands. Rust performs no implicit fused
//! multiply-add and x86-64 uses SSE2, so every operation is a single correctly
//! rounded IEEE 754 operation.
//!
//! The step is branch-free: `up(x) = fl(x + fl(fl(|x| 2^-52) + 2^-1074))`. The
//! added amount is at least the gap from `x` to the next binary64 value above it
//! (lemma I1), so the result is at least that next value; it may be two values
//! up, which costs nothing measurable.

/// `2^-52`: no gap between adjacent binary64 values exceeds `2^-52 |x|`.
const GAP: f64 = 1.0 / 4_503_599_627_370_496.0;
/// The smallest positive subnormal, the gap at and below the normal range.
const TINY: f64 = 5e-324;

/// The smaller of two values, or `NaN` when either is `NaN` or `a` is
/// infinite; `f64::min` would return the other operand and turn a failed
/// computation into a finite, wrong one (lemma F3).
///
/// The select returns `b` whenever the comparison fails, so a `NaN` in `b`
/// survives it; `a * 0` is zero for finite `a` and `NaN` otherwise, which
/// carries a `NaN` (or an overflow) in `a`. Three instructions, branch-free.
#[inline]
#[must_use]
pub fn fmin(a: f64, b: f64) -> f64 {
    (if a < b { a } else { b }) + a * 0.0
}

/// The larger of two values, or `NaN` when either is `NaN` or `a` is infinite.
#[inline]
#[must_use]
pub fn fmax(a: f64, b: f64) -> f64 {
    (if a > b { a } else { b }) + a * 0.0
}

/// A lower bound on the exact real result `x` from its rounded value.
#[inline]
#[must_use]
pub fn dn(x: f64) -> f64 {
    x - (x.abs() * GAP + TINY)
}

/// An upper bound on the exact real result `x` from its rounded value.
#[inline]
#[must_use]
pub fn up(x: f64) -> f64 {
    x + (x.abs() * GAP + TINY)
}

/// A lower bound on `a + b`.
#[inline]
#[must_use]
pub fn add_dn(a: f64, b: f64) -> f64 {
    dn(a + b)
}

/// An upper bound on `a + b`.
#[inline]
#[must_use]
pub fn add_up(a: f64, b: f64) -> f64 {
    up(a + b)
}

/// A lower bound on `a - b`.
#[inline]
#[must_use]
pub fn sub_dn(a: f64, b: f64) -> f64 {
    dn(a - b)
}

/// An upper bound on `a - b`.
#[inline]
#[must_use]
pub fn sub_up(a: f64, b: f64) -> f64 {
    up(a - b)
}

/// A lower bound on `a * b`.
#[inline]
#[must_use]
pub fn mul_dn(a: f64, b: f64) -> f64 {
    dn(a * b)
}

/// An upper bound on `a * b`.
#[inline]
#[must_use]
pub fn mul_up(a: f64, b: f64) -> f64 {
    up(a * b)
}

/// A closed interval `[lo, hi]` of reals, with `lo <= hi` for any interval built
/// by this module from valid operands.
#[derive(Clone, Copy, Debug, PartialEq)]
pub struct Iv {
    /// Lower endpoint.
    pub lo: f64,
    /// Upper endpoint.
    pub hi: f64,
}

impl Iv {
    /// The degenerate interval holding one representable value exactly.
    #[inline]
    #[must_use]
    pub const fn point(x: f64) -> Self {
        Self { lo: x, hi: x }
    }

    /// An interval from two endpoints.
    #[inline]
    #[must_use]
    pub const fn new(lo: f64, hi: f64) -> Self {
        Self { lo, hi }
    }

    /// The enclosure of a sum.
    #[inline]
    #[must_use]
    pub fn plus(self, other: Self) -> Self {
        Self::new(add_dn(self.lo, other.lo), add_up(self.hi, other.hi))
    }

    /// The enclosure of a difference.
    #[inline]
    #[must_use]
    pub fn minus(self, other: Self) -> Self {
        Self::new(sub_dn(self.lo, other.hi), sub_up(self.hi, other.lo))
    }

    /// The enclosure of a product, by the four endpoint products.
    #[inline]
    #[must_use]
    pub fn times(self, other: Self) -> Self {
        let a = self.lo * other.lo;
        let b = self.lo * other.hi;
        let c = self.hi * other.lo;
        let d = self.hi * other.hi;
        Self::new(
            dn(fmin(fmin(a, b), fmin(c, d))),
            up(fmax(fmax(a, b), fmax(c, d))),
        )
    }

    /// The enclosure of the product with a nonnegative interval `k`.
    ///
    /// For `k >= 0` the product is monotone in each factor's sign, which saves
    /// two of the four products.
    #[inline]
    #[must_use]
    pub fn mul_nonneg(self, k: Self) -> Self {
        let lo = if self.lo >= 0.0 {
            self.lo * k.lo
        } else {
            self.lo * k.hi
        };
        let hi = if self.hi >= 0.0 {
            self.hi * k.hi
        } else {
            self.hi * k.lo
        };
        Self::new(dn(lo), up(hi))
    }

    /// The pointwise minimum of two enclosed quantities.
    #[inline]
    #[must_use]
    pub fn min(self, other: Self) -> Self {
        Self::new(fmin(self.lo, other.lo), fmin(self.hi, other.hi))
    }

    /// The pointwise maximum of two enclosed quantities.
    #[inline]
    #[must_use]
    pub fn max(self, other: Self) -> Self {
        Self::new(fmax(self.lo, other.lo), fmax(self.hi, other.hi))
    }

    /// The enclosure of the positive part `max(x, 0)`.
    #[inline]
    #[must_use]
    pub fn pos(self) -> Self {
        Self::new(fmax(self.lo, 0.0), fmax(self.hi, 0.0))
    }

    /// The largest absolute value in the interval.
    #[inline]
    #[must_use]
    pub fn mag(self) -> f64 {
        fmax(self.lo.abs(), self.hi.abs())
    }

    /// Whether both endpoints are finite and ordered.
    #[inline]
    #[must_use]
    pub fn is_valid(self) -> bool {
        self.lo.is_finite() && self.hi.is_finite() && self.lo <= self.hi
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn nan_is_never_dropped() {
        let nan = Iv::new(f64::NAN, 1.0);
        let one = Iv::point(1.0);
        for value in [
            nan.min(one),
            one.min(nan),
            nan.max(one),
            one.max(nan),
            nan.pos(),
            nan.times(one),
            one.times(nan),
            nan.plus(one),
            nan.minus(one),
            nan.mul_nonneg(one),
        ] {
            assert!(
                value.lo.is_nan() || value.hi.is_nan(),
                "{value:?} lost its NaN"
            );
            assert!(!value.is_valid());
        }
        assert!(nan.mag().is_nan());
        assert!(fmin(f64::NAN, 0.0).is_nan() && fmax(0.0, f64::NAN).is_nan());
        // Overflow becomes NaN, never a finite bound: dn(+inf) and up(-inf).
        assert!(add_dn(f64::MAX, f64::MAX).is_nan());
        assert!(sub_up(-f64::MAX, f64::MAX).is_nan());
    }

    #[test]
    fn directed_steps_bracket_exact_sums() {
        // 0.1 + 0.2 is not representable; the bracket must contain it.
        let lo = add_dn(0.1, 0.2);
        let hi = add_up(0.1, 0.2);
        assert!(lo < hi);
        assert!(lo <= 0.300_000_000_000_000_04);
        assert!(hi >= 0.300_000_000_000_000_04);
    }

    #[test]
    fn steps_reach_the_adjacent_values() {
        for x in [
            0.0,
            -0.0,
            1.0,
            -1.0,
            1.5,
            0.1,
            -0.3,
            2.0,
            -2.0,
            1e-310,
            -1e-310,
            5e-324,
            1e300,
            0.999_999_999_999_999_9,
            4096.0,
            -4096.0,
        ] {
            assert!(
                up(x) >= x.next_up(),
                "up({x}) = {} below {}",
                up(x),
                x.next_up()
            );
            assert!(
                dn(x) <= x.next_down(),
                "dn({x}) = {} above {}",
                dn(x),
                x.next_down()
            );
            assert!(up(x) <= x.next_up().next_up().next_up());
        }
        let mut state = 1u64;
        for _ in 0..100_000 {
            state = state
                .wrapping_mul(6_364_136_223_846_793_005)
                .wrapping_add(1);
            let x = f64::from_bits(state >> 2);
            if !x.is_finite() || x.abs() > 1e300 {
                continue;
            }
            assert!(up(x) >= x.next_up() && dn(x) <= x.next_down(), "{x:e}");
        }
    }

    #[test]
    fn interval_product_covers_sign_changes() {
        let a = Iv::new(-2.0, 3.0);
        let b = Iv::new(-5.0, 7.0);
        let p = a.times(b);
        assert!(p.lo <= -15.0 && p.hi >= 21.0);
        let q = a.mul_nonneg(Iv::new(2.0, 4.0));
        assert!(q.lo <= -8.0 && q.hi >= 12.0);
    }
}
