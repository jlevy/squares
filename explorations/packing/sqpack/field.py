"""Exact arithmetic in a real algebraic number field Q(alpha).

An element is a polynomial in `alpha` of degree < deg(m) with rational
coefficients, reduced modulo the minimal polynomial `m`.  Two decisions are
exact and together are complete:

- **equality**: `beta == 0` iff its reduced representative is the zero
  polynomial, since `m` is the minimal polynomial of `alpha`.
- **sign**: for `beta != 0`, evaluate the representative over a rational
  isolating interval for `alpha` with interval arithmetic, bisecting the
  interval until the enclosure excludes zero.  This terminates precisely
  because `deg(beta) < deg(m)` and `beta != 0` force `beta(alpha) != 0`.

No floating point appears in either decision.  That matters for packings:
a tight packing has squares that touch exactly, so validity depends on
certifying equalities, which floating point and interval arithmetic can
never do.
"""

from __future__ import annotations

import decimal
from collections.abc import Iterable, Sequence
from fractions import Fraction

Rat = Fraction


def _poly_mul(a: Sequence[Rat], b: Sequence[Rat]) -> list[Rat]:
    out = [Rat(0)] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        if ai:
            for j, bj in enumerate(b):
                if bj:
                    out[i + j] += ai * bj
    return out


class NumberField:
    """Q(alpha) for a real root `alpha` of an irreducible polynomial.

    Args:
        min_poly: coefficients of the minimal polynomial, highest degree
            first.  Need not be monic; it is normalised internally.
        isolating: a rational interval (lo, hi) containing exactly one real
            root of `min_poly`, namely the intended `alpha`.
    """

    def __init__(self, min_poly: Iterable, isolating: tuple):
        coeffs = [Rat(c) for c in min_poly]
        if not coeffs or coeffs[0] == 0:
            raise ValueError("leading coefficient must be nonzero")
        self.degree = len(coeffs) - 1
        self._high_to_low = [c / coeffs[0] for c in coeffs]
        self._low_to_high = self._high_to_low[::-1]  # monic, low->high

        lo, hi = Rat(isolating[0]), Rat(isolating[1])
        if lo >= hi:
            raise ValueError("isolating interval must be nonempty")
        if self._eval_min_poly(lo) * self._eval_min_poly(hi) >= 0:
            raise ValueError("min_poly does not change sign on the interval")
        self._lo, self._hi = lo, hi
        self._sign_at_lo = 1 if self._eval_min_poly(lo) > 0 else -1
        self.refinements = 0

    # -- construction ------------------------------------------------------

    def element(self, coeffs) -> FieldElement:
        """Element from coefficients of a polynomial in alpha, low degree first."""
        if isinstance(coeffs, (int, Fraction)):
            coeffs = [coeffs]
        c = [Rat(x) for x in coeffs]
        return FieldElement(self, self._reduce(c))

    def rational(self, value) -> FieldElement:
        return self.element([Rat(value)])

    @property
    def alpha(self) -> FieldElement:
        return self.element([0, 1])

    @property
    def zero(self) -> FieldElement:
        return self.rational(0)

    @property
    def one(self) -> FieldElement:
        return self.rational(1)

    # -- internals ---------------------------------------------------------

    def _eval_min_poly(self, x: Rat) -> Rat:
        acc = Rat(0)
        for c in self._high_to_low:
            acc = acc * x + c
        return acc

    def _reduce(self, p: list[Rat]) -> list[Rat]:
        d, mod = self.degree, self._low_to_high
        p = list(p)
        for i in range(len(p) - 1, d - 1, -1):
            c = p[i]
            if c:
                p[i] = Rat(0)
                for k in range(d):
                    p[i - d + k] -= c * mod[k]
        p = p[:d]
        return p + [Rat(0)] * (d - len(p))

    def _bisect(self) -> None:
        mid = (self._lo + self._hi) / 2
        v = self._eval_min_poly(mid)
        if v == 0:
            raise RuntimeError("min_poly has a rational root; it is not irreducible")
        if (1 if v > 0 else -1) == self._sign_at_lo:
            self._lo = mid
        else:
            self._hi = mid
        self.refinements += 1

    def _enclose(self, coeffs: Sequence[Rat]) -> tuple[Rat, Rat]:
        """Rigorous enclosure of the polynomial over the isolating interval."""
        lo, hi = self._lo, self._hi
        a = b = Rat(0)
        for c in reversed(coeffs):
            products = (a * lo, a * hi, b * lo, b * hi)
            a, b = min(products) + c, max(products) + c
        return a, b

    def sign(self, e: FieldElement) -> int:
        """Exact sign of `e`: -1, 0 or +1."""
        if e.is_zero():
            return 0
        while True:
            a, b = self._enclose(e.coeffs)
            if a > 0:
                return 1
            if b < 0:
                return -1
            self._bisect()

    def refine_to(self, digits: int) -> None:
        """Narrow the isolating interval below 10**-digits."""
        target = Rat(1, 10**digits)
        while self._hi - self._lo > target:
            self._bisect()

    def root_bounds(self) -> tuple[Rat, Rat]:
        """
        The current rigorous enclosure `(lo, hi)` of the field's root.

        Public because callers legitimately need the numeric value -- exporting a
        packing to `f64`, for instance -- and reaching into the enclosure directly
        couples them to how refinement is stored.
        """
        return self._lo, self._hi

    def root_approx(self) -> float:
        """
        Midpoint of the current enclosure, as a float.

        A ONE-WAY DOOR out of exact arithmetic: nothing computed from this may claim
        exactness, and `refine_to` should be called first if the caller needs more
        digits than the current enclosure carries.
        """
        return float((self._lo + self._hi) / 2)

    def decimal(self, e: FieldElement, digits: int = 30) -> str:
        """Decimal digits of `e` that are certain, from a rigorous enclosure."""
        self.refine_to(digits + 8)
        decimal.getcontext().prec = digits + 20
        lo, hi = self._enclose(e.coeffs)

        def as_dec(q: Rat) -> decimal.Decimal:
            return decimal.Decimal(q.numerator) / decimal.Decimal(q.denominator)

        slo, shi = str(+as_dec(lo)), str(+as_dec(hi))
        shared = 0
        for x, y in zip(slo, shi, strict=False):
            if x != y:
                break
            shared += 1
        return slo[:shared]


class FieldElement:
    """An element of a :class:`NumberField`.  Immutable."""

    __slots__ = ("coeffs", "field")

    def __init__(self, field: NumberField, coeffs: list[Rat]):
        self.field = field
        self.coeffs = coeffs

    def _check(self, other: FieldElement) -> None:
        if other.field is not self.field:
            raise ValueError("elements come from different number fields")

    def __add__(self, other):
        other = self._coerce(other)
        return FieldElement(
            self.field, [a + b for a, b in zip(self.coeffs, other.coeffs, strict=True)]
        )

    def __sub__(self, other):
        other = self._coerce(other)
        return FieldElement(
            self.field, [a - b for a, b in zip(self.coeffs, other.coeffs, strict=True)]
        )

    def __neg__(self):
        return FieldElement(self.field, [-a for a in self.coeffs])

    def __mul__(self, other):
        other = self._coerce(other)
        return FieldElement(
            self.field, self.field._reduce(_poly_mul(self.coeffs, other.coeffs))
        )

    __radd__ = __add__
    __rmul__ = __mul__

    def __rsub__(self, other):
        return self._coerce(other) - self

    def __truediv__(self, other):
        return self * self._coerce(other).inverse()

    def __rtruediv__(self, other):
        return self._coerce(other) * self.inverse()

    def _coerce(self, other):
        if isinstance(other, FieldElement):
            self._check(other)
            return other
        return self.field.rational(other)

    def is_zero(self) -> bool:
        return all(c == 0 for c in self.coeffs)

    def __eq__(self, other):
        return (self - self._coerce(other)).is_zero()

    def __hash__(self):
        return hash(tuple(self.coeffs))

    def inverse(self) -> FieldElement:
        """Multiplicative inverse, by exact Gaussian elimination.

        Solves ``x * self == 1`` using the matrix of "multiplication by self"
        in the basis ``{1, alpha, ..., alpha^(d-1)}``.
        """
        f = self.field
        d = f.degree
        if self.is_zero():
            raise ZeroDivisionError("zero is not invertible")
        columns = []
        for k in range(d):
            basis = [Rat(0)] * d
            basis[k] = Rat(1)
            columns.append(f._reduce(_poly_mul(self.coeffs, basis)))  # noqa: SLF001
        rows = [
            [columns[k][r] for k in range(d)] + [Rat(1) if r == 0 else Rat(0)] for r in range(d)
        ]
        for col in range(d):
            pivot = next((r for r in range(col, d) if rows[r][col] != 0), None)
            if pivot is None:
                raise ZeroDivisionError("not invertible")
            rows[col], rows[pivot] = rows[pivot], rows[col]
            scale = rows[col][col]
            rows[col] = [x / scale for x in rows[col]]
            for r in range(d):
                if r != col and rows[r][col] != 0:
                    factor = rows[r][col]
                    rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col], strict=True)]
        return FieldElement(f, [rows[r][d] for r in range(d)])

    def sign(self) -> int:
        return self.field.sign(self)

    def __float__(self) -> float:
        """Midpoint of a rigorous enclosure. For display and bucketing only."""
        self.field.refine_to(30)
        lo, hi = self.field._enclose(self.coeffs)  # noqa: SLF001
        return float((lo + hi) / 2)

    def __repr__(self) -> str:
        return f"FieldElement({[str(c) for c in self.coeffs]})"
