"""Exact-rational interval arithmetic for the strongest-tier review of 2 November 2026.

Standard library only. An `Iv` is a closed interval [lo, hi] with `Fraction` end
points. Every operation encloses its exact result: the four field operations are
exact on the end points and then rounded outward to the dyadic grid 2**-PREC, and
each transcendental function adds an explicit bound on the series remainder.

Written for this review from the mathematics alone; it imports no third-party
library and shares no code with the source's programs or with any maintained
checker of this repository.
"""

from __future__ import annotations

import math
from fractions import Fraction

PREC = 480
_SCALE = 1 << PREC
_EPS = Fraction(1, _SCALE)
# Series stop once a term falls below 2**-(PREC - 20): far above the rounding grid,
# so a term rounded up to the grid always drops below it.
_TOL = Fraction(1 << 20, _SCALE)


def _down(q: Fraction) -> Fraction:
    return Fraction(math.floor(q * _SCALE), _SCALE)


def _up(q: Fraction) -> Fraction:
    return Fraction(math.ceil(q * _SCALE), _SCALE)


def Q(x: object) -> Fraction:
    """An exact rational from an int, a Fraction or a decimal string."""
    if isinstance(x, Fraction):
        return x
    if isinstance(x, int):
        return Fraction(x)
    if isinstance(x, str):
        return Fraction(x)
    raise TypeError(f"refusing to convert {type(x).__name__} exactly: {x!r}")


class Iv:
    """A closed interval with exact rational end points."""

    __slots__ = ("lo", "hi")

    def __init__(self, lo: object, hi: object | None = None) -> None:
        lo_q = Q(lo)
        hi_q = lo_q if hi is None else Q(hi)
        if lo_q > hi_q:
            raise ValueError("empty interval")
        self.lo = lo_q
        self.hi = hi_q

    @staticmethod
    def of(x: object) -> Iv:
        return x if isinstance(x, Iv) else Iv(x)

    def _round(self) -> Iv:
        return Iv(_down(self.lo), _up(self.hi))

    def __add__(self, other: object) -> Iv:
        o = Iv.of(other)
        return Iv(self.lo + o.lo, self.hi + o.hi)._round()

    __radd__ = __add__

    def __neg__(self) -> Iv:
        return Iv(-self.hi, -self.lo)

    def __sub__(self, other: object) -> Iv:
        o = Iv.of(other)
        return Iv(self.lo - o.hi, self.hi - o.lo)._round()

    def __rsub__(self, other: object) -> Iv:
        return Iv.of(other) - self

    def __mul__(self, other: object) -> Iv:
        o = Iv.of(other)
        ps = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Iv(min(ps), max(ps))._round()

    __rmul__ = __mul__

    def inv(self) -> Iv:
        if self.lo <= 0 <= self.hi:
            raise ZeroDivisionError("interval contains 0")
        return Iv(1 / self.hi, 1 / self.lo)._round()

    def __truediv__(self, other: object) -> Iv:
        return self * Iv.of(other).inv()

    def __rtruediv__(self, other: object) -> Iv:
        return Iv.of(other) * self.inv()

    def __pow__(self, n: int) -> Iv:
        if not isinstance(n, int):
            raise TypeError("integer powers only; use root() for fractional ones")
        if n < 0:
            return (self ** (-n)).inv()
        if n == 0:
            return Iv(1)
        if self.lo >= 0:
            return Iv(self.lo**n, self.hi**n)._round()
        if self.hi <= 0:
            a, b = self.hi**n, self.lo**n
            return Iv(min(a, b), max(a, b))._round()
        if n % 2:
            return Iv(self.lo**n, self.hi**n)._round()
        return Iv(0, max(self.lo**n, self.hi**n))._round()

    def width(self) -> Fraction:
        return self.hi - self.lo

    def mid(self) -> Fraction:
        return (self.lo + self.hi) / 2

    def __repr__(self) -> str:
        return f"Iv[{float(self.lo)!r}, {float(self.hi)!r}]"

    def hull(self, other: Iv) -> Iv:
        return Iv(min(self.lo, other.lo), max(self.hi, other.hi))


# Certified comparisons: True when proved, False when the opposite is proved, None
# when the enclosures overlap.


def lt(a: object, b: object) -> bool | None:
    x, y = Iv.of(a), Iv.of(b)
    if x.hi < y.lo:
        return True
    if x.lo >= y.hi:
        return False
    return None


def le(a: object, b: object) -> bool | None:
    x, y = Iv.of(a), Iv.of(b)
    if x.hi <= y.lo:
        return True
    if x.lo > y.hi:
        return False
    return None


def gt(a: object, b: object) -> bool | None:
    return lt(b, a)


def ge(a: object, b: object) -> bool | None:
    return le(b, a)


# Roots of nonnegative rationals.


def _iroot(n: int, k: int) -> int:
    """floor(n ** (1/k)) for an integer n >= 0, exactly."""
    if n < 0:
        raise ValueError("negative radicand")
    if n < 2:
        return n
    x = 1 << ((n.bit_length() + k - 1) // k)
    while True:
        y = ((k - 1) * x + n // x ** (k - 1)) // k
        if y >= x:
            break
        x = y
    while x**k > n:
        x -= 1
    while (x + 1) ** k <= n:
        x += 1
    return x


def _root_point(q: Fraction, k: int) -> Iv:
    if q < 0:
        raise ValueError("negative radicand")
    n = math.floor(q * (_SCALE**k))
    m = _iroot(n, k)
    lo = Fraction(m, _SCALE)
    hi = Fraction(m + 1, _SCALE)
    if not (lo**k <= q <= hi**k):
        raise ArithmeticError("root enclosure failed")
    return Iv(lo, hi)


def root(x: object, k: int) -> Iv:
    """The principal k-th root of a nonnegative interval."""
    v = Iv.of(x)
    if v.lo < 0:
        raise ValueError("negative interval under a root")
    return Iv(_root_point(v.lo, k).lo, _root_point(v.hi, k).hi)


def sqrt(x: object) -> Iv:
    return root(x, 2)


def rpow(x: object, num: int, den: int) -> Iv:
    """x ** (num/den) for a positive interval x (den > 0)."""
    v = Iv.of(x)
    if v.lo <= 0:
        raise ValueError("rpow needs a positive interval")
    r = root(v, den)
    return r**num


# Series for elementary functions at a rational point, with explicit remainders.


def _series_cos(x: Fraction) -> Iv:
    x = abs(x)
    if x > 1:
        h = _series_cos(x / 2)
        return 2 * h * h - 1
    total = Iv(0)
    term = Iv(1)
    x2 = Iv(x) * Iv(x)
    j = 0
    while True:
        total = total + (term if j % 2 == 0 else -term)
        j += 1
        term = term * x2 / ((2 * j - 1) * (2 * j))
        if term.hi < _TOL:
            break
    return total + Iv(-term.hi, term.hi)


def _series_sin(x: Fraction) -> Iv:
    if x < 0:
        return -_series_sin(-x)
    if x > 1:
        h = x / 2
        return 2 * _series_sin(h) * _series_cos(h)
    total = Iv(0)
    term = Iv(x)
    x2 = Iv(x) * Iv(x)
    j = 0
    while True:
        total = total + (term if j % 2 == 0 else -term)
        j += 1
        term = term * x2 / ((2 * j) * (2 * j + 1))
        if term.hi < _TOL:
            break
    return total + Iv(-term.hi, term.hi)


def _series_atan(x: Fraction) -> Iv:
    if x < 0:
        return -_series_atan(-x)
    if x > Fraction(1, 2):
        # atan x = 2 atan(x / (1 + sqrt(1 + x^2))): halve the argument, on intervals.
        s = sqrt(1 + Iv(x) * Iv(x))
        y = Iv(x) / (1 + s)
        return 2 * Iv(_series_atan(y.lo).lo, _series_atan(y.hi).hi)
    total = Iv(0)
    power = Iv(x)
    x2 = Iv(x) * Iv(x)
    n = 0
    while True:
        term = power / (2 * n + 1)
        if term.hi < _TOL:
            return total + Iv(-term.hi, term.hi)
        total = total + (term if n % 2 == 0 else -term)
        power = power * x2
        n += 1


def _series_log(x: Fraction) -> Iv:
    if x <= 0:
        raise ValueError("log of a nonpositive number")
    # x = m * 2**e with 1 <= m < 2, exactly.
    e = x.numerator.bit_length() - x.denominator.bit_length()
    m = x / (Fraction(2) ** e)
    while m >= 2:
        m /= 2
        e += 1
    while m < 1:
        m *= 2
        e -= 1
    return _atanh2((m - 1) / (m + 1)) + e * LOG2


def _atanh2(z: Fraction) -> Iv:
    """2 atanh(z) for 0 <= z < 1/2, with the geometric tail bound."""
    if z == 0:
        return Iv(0)
    total = Iv(0)
    power = Iv(z)
    z2 = Iv(z) * Iv(z)
    n = 0
    while True:
        term = 2 * power / (2 * n + 1)
        if term.hi < _TOL:
            # the remaining terms sum to at most term / (1 - z^2)
            tail = term / (1 - z2)
            return total + Iv(0, tail.hi)
        total = total + term
        power = power * z2
        n += 1


LOG2 = _atanh2(Fraction(1, 3))
PI = 16 * _series_atan(Fraction(1, 5)) - 4 * _series_atan(Fraction(1, 239))


# Interval versions, by monotonicity where the arguments of this review lie.


def cos(x: object) -> Iv:
    """cos on an interval inside [0, pi]; decreasing there."""
    v = Iv.of(x)
    if v.lo < 0 or v.hi > Fraction(3):
        raise ValueError("cos() is implemented for intervals inside [0, 3]")
    return Iv(_series_cos(v.hi).lo, _series_cos(v.lo).hi)


def sin(x: object) -> Iv:
    """sin on an interval inside [-1.5, 1.5]; increasing there."""
    v = Iv.of(x)
    if v.lo < Fraction(-3, 2) or v.hi > Fraction(3, 2):
        raise ValueError("sin() is implemented for intervals inside [-1.5, 1.5]")
    return Iv(_series_sin(v.lo).lo, _series_sin(v.hi).hi)


def tan(x: object) -> Iv:
    """tan on an interval inside [0, 1.5]; increasing there."""
    v = Iv.of(x)
    if v.lo < 0 or v.hi > Fraction(3, 2):
        raise ValueError("tan() is implemented for intervals inside [0, 1.5]")
    lo = _series_sin(v.lo) / _series_cos(v.lo)
    hi = _series_sin(v.hi) / _series_cos(v.hi)
    return Iv(lo.lo, hi.hi)


def atan(x: object) -> Iv:
    v = Iv.of(x)
    return Iv(_series_atan(v.lo).lo, _series_atan(v.hi).hi)


def log(x: object) -> Iv:
    v = Iv.of(x)
    return Iv(_series_log(v.lo).lo, _series_log(v.hi).hi)


def arcsin(x: object) -> Iv:
    """arcsin on an interval inside [0, 0.99]; increasing there."""
    v = Iv.of(x)
    if v.lo < 0 or v.hi >= Fraction(99, 100):
        raise ValueError("arcsin() is implemented for intervals inside [0, 0.99)")

    def at(q: Fraction) -> Iv:
        s = sqrt(1 - Iv(q) * Iv(q))
        y = Iv(q) / s
        return Iv(_series_atan(y.lo).lo, _series_atan(y.hi).hi)

    return Iv(at(v.lo).lo, at(v.hi).hi)


def arccos(x: object) -> Iv:
    """arccos on an interval inside [0, 0.99]; decreasing there."""
    v = Iv.of(x)
    return PI / 2 - arcsin(v)


def ceil_int(x: Iv) -> int | None:
    """The integer ceiling of the value enclosed by x, when the enclosure decides it."""
    lo, hi = math.ceil(x.lo), math.ceil(x.hi)
    return lo if lo == hi else None


def digits_trunc(x: Iv, places: int) -> str | None:
    """The decimal truncation of the enclosed value to `places` digits after the point,
    when the enclosure decides it (both end points truncate alike)."""
    s = 10**places
    lo, hi = math.floor(x.lo * s), math.floor(x.hi * s)
    if lo != hi:
        return None
    sign = "-" if lo < 0 else ""
    a = abs(lo)
    return f"{sign}{a // s}.{a % s:0{places}d}"


def self_test() -> dict[str, bool]:
    """Checks against values known to many digits, and identities."""
    pi_ref = Fraction("3.14159265358979323846264338327950288419716939937510582097494459230781640628620899")
    ln2_ref = Fraction("0.693147180559945309417232121458176568075500134360255254120680009493393621969694715")
    e1 = Fraction("2.71828182845904523536028747135266249775724709369995957496696762772407663035354759")
    out: dict[str, bool] = {}
    out["pi"] = PI.lo <= pi_ref + Fraction(1, 10**78) and pi_ref - Fraction(1, 10**78) <= PI.hi and PI.width() < Fraction(1, 10**100)
    out["log2"] = LOG2.lo <= ln2_ref + Fraction(1, 10**78) and ln2_ref - Fraction(1, 10**78) <= LOG2.hi
    le_ = log(e1)
    out["log e"] = le_.lo < 1 + Fraction(1, 10**75) and le_.hi > 1 - Fraction(1, 10**75)
    c, s = _series_cos(Fraction(7, 10)), _series_sin(Fraction(7, 10))
    pyth = c * c + s * s
    out["cos^2+sin^2"] = pyth.lo <= 1 <= pyth.hi and pyth.width() < Fraction(1, 10**100)
    a1 = atan(Fraction(1))
    out["atan 1 = pi/4"] = a1.lo <= PI.hi / 4 and PI.lo / 4 <= a1.hi
    r = root(Fraction(2), 4) ** 4
    out["2^(1/4)^4"] = r.lo <= 2 <= r.hi
    ac = arccos(Fraction(1, 2))
    out["arccos 1/2 = pi/3"] = ac.lo <= PI.hi / 3 and PI.lo / 3 <= ac.hi
    t = tan(Fraction(1, 3))
    out["tan via sin/cos"] = (t * _series_cos(Fraction(1, 3)) - _series_sin(Fraction(1, 3))).width() < Fraction(1, 10**90)
    return out


if __name__ == "__main__":
    res = self_test()
    for k, v in res.items():
        print(f"{k}: {'ok' if v else 'FAIL'}")
    raise SystemExit(0 if all(res.values()) else 1)
