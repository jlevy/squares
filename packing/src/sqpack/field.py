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
import math
from collections.abc import Iterable, Sequence
from fractions import Fraction
from itertools import pairwise

Rat = Fraction

# A modular certificate is cheap when one exists.  The bound limits certificate search;
# it is not treated as a proof of reducibility when the search finds nothing.
IRREDUCIBILITY_PRIME_SEARCH_LIMIT = 257


class FieldPreconditionError(ValueError):
    """A field declaration did not prove the assumptions exact arithmetic needs."""


def _trim(poly: list[Rat]) -> list[Rat]:
    """Remove high zero coefficients from a low-to-high rational polynomial."""
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def _poly_divmod(a: Sequence[Rat], b: Sequence[Rat]) -> tuple[list[Rat], list[Rat]]:
    """Exact polynomial division, with coefficients stored low degree first."""
    divisor = _trim(list(b))
    if divisor == [0]:
        raise ZeroDivisionError("polynomial division by zero")
    remainder = _trim(list(a))
    quotient = [Rat(0)] * max(1, len(remainder) - len(divisor) + 1)
    while remainder != [0] and len(remainder) >= len(divisor):
        degree = len(remainder) - len(divisor)
        scale = remainder[-1] / divisor[-1]
        quotient[degree] = scale
        for index, coefficient in enumerate(divisor):
            remainder[index + degree] -= scale * coefficient
        _trim(remainder)
    return _trim(quotient), remainder


def _sturm_sequence(poly: Sequence[Rat]) -> list[list[Rat]]:
    """Build the exact Sturm sequence for a square-free rational polynomial."""
    first = _trim(list(poly))
    derivative = _trim([Rat(index) * value for index, value in enumerate(first)][1:])
    sequence = [first, derivative]
    while sequence[-1] != [0]:
        _, remainder = _poly_divmod(sequence[-2], sequence[-1])
        if remainder == [0]:
            break
        sequence.append([-value for value in remainder])
    return sequence


def _eval_poly(poly: Sequence[Rat], value: Rat) -> Rat:
    result = Rat(0)
    for coefficient in reversed(poly):
        result = result * value + coefficient
    return result


def _sign_variations(sequence: Sequence[Sequence[Rat]], value: Rat) -> int:
    signs: list[int] = []
    for poly in sequence:
        evaluated = _eval_poly(poly, value)
        if evaluated:
            signs.append(1 if evaluated > 0 else -1)
    return sum(left != right for left, right in pairwise(signs))


def _root_count(poly: Sequence[Rat], lo: Rat, hi: Rat) -> int:
    sequence = _sturm_sequence(poly)
    return _sign_variations(sequence, lo) - _sign_variations(sequence, hi)


def _primitive_integer_poly(high_to_low: Sequence[Rat]) -> list[int]:
    """Clear denominators and content without changing rational irreducibility."""
    denominator = 1
    for coefficient in high_to_low:
        denominator = math.lcm(denominator, coefficient.denominator)
    integers = [
        coefficient.numerator * (denominator // coefficient.denominator)
        for coefficient in high_to_low
    ]
    content = 0
    for coefficient in integers:
        content = math.gcd(content, abs(coefficient))
    integers = [coefficient // content for coefficient in integers]
    if integers[0] < 0:
        integers = [-coefficient for coefficient in integers]
    return integers


def _trim_mod(poly: list[int], prime: int) -> list[int]:
    for index, coefficient in enumerate(poly):
        poly[index] = coefficient % prime
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def _mod_divmod(a: Sequence[int], b: Sequence[int], prime: int) -> tuple[list[int], list[int]]:
    divisor = _trim_mod(list(b), prime)
    if divisor == [0]:
        raise ZeroDivisionError("polynomial division by zero")
    remainder = _trim_mod(list(a), prime)
    quotient = [0] * max(1, len(remainder) - len(divisor) + 1)
    inverse = pow(divisor[-1], -1, prime)
    while remainder != [0] and len(remainder) >= len(divisor):
        degree = len(remainder) - len(divisor)
        scale = remainder[-1] * inverse % prime
        quotient[degree] = scale
        for index, coefficient in enumerate(divisor):
            remainder[index + degree] = (
                remainder[index + degree] - scale * coefficient
            ) % prime
        _trim_mod(remainder, prime)
    return _trim_mod(quotient, prime), remainder


def _mod_mul(
    a: Sequence[int], b: Sequence[int], modulus: Sequence[int], prime: int
) -> list[int]:
    product = [0] * (len(a) + len(b) - 1)
    for left_index, left in enumerate(a):
        for right_index, right in enumerate(b):
            product[left_index + right_index] = (
                product[left_index + right_index] + left * right
            ) % prime
    return _mod_divmod(product, modulus, prime)[1]


def _mod_pow(
    base: Sequence[int], exponent: int, modulus: Sequence[int], prime: int
) -> list[int]:
    result = [1]
    power = _trim_mod(list(base), prime)
    while exponent:
        if exponent & 1:
            result = _mod_mul(result, power, modulus, prime)
        power = _mod_mul(power, power, modulus, prime)
        exponent >>= 1
    return result


def _mod_gcd(a: Sequence[int], b: Sequence[int], prime: int) -> list[int]:
    left, right = _trim_mod(list(a), prime), _trim_mod(list(b), prime)
    while right != [0]:
        left, right = right, _mod_divmod(left, right, prime)[1]
    inverse = pow(left[-1], -1, prime)
    return [(coefficient * inverse) % prime for coefficient in left]


def _prime_divisors(value: int) -> set[int]:
    divisors: set[int] = set()
    factor = 2
    while factor * factor <= value:
        if value % factor == 0:
            divisors.add(factor)
            while value % factor == 0:
                value //= factor
        factor += 1
    if value > 1:
        divisors.add(value)
    return divisors


def _is_prime(value: int) -> bool:
    if value < 2:
        return False
    return all(value % divisor for divisor in range(2, math.isqrt(value) + 1))


def _irreducible_mod_prime(high_to_low: Sequence[int], prime: int) -> bool:
    """Rabin's exact irreducibility test over the finite field F_prime."""
    if high_to_low[0] % prime == 0:
        return False
    low_to_high = [coefficient % prime for coefficient in reversed(high_to_low)]
    inverse = pow(low_to_high[-1], -1, prime)
    modulus = [(coefficient * inverse) % prime for coefficient in low_to_high]
    degree = len(modulus) - 1
    x_poly = [0, 1]
    for divisor in _prime_divisors(degree):
        power = _mod_pow(x_poly, prime ** (degree // divisor), modulus, prime)
        difference = _trim_mod(
            [
                (power[index] if index < len(power) else 0)
                - (x_poly[index] if index < len(x_poly) else 0)
                for index in range(max(len(power), len(x_poly)))
            ],
            prime,
        )
        if len(_mod_gcd(modulus, difference, prime)) > 1:
            return False
    power = _mod_pow(x_poly, prime**degree, modulus, prime)
    difference = _trim_mod(
        [
            (power[index] if index < len(power) else 0)
            - (x_poly[index] if index < len(x_poly) else 0)
            for index in range(max(len(power), len(x_poly)))
        ],
        prime,
    )
    return difference == [0]


def _irreducibility_prime(high_to_low: Sequence[Rat]) -> int | None:
    integer_poly = _primitive_integer_poly(high_to_low)
    for prime in range(2, IRREDUCIBILITY_PRIME_SEARCH_LIMIT + 1):
        if _is_prime(prime) and _irreducible_mod_prime(integer_poly, prime):
            return prime
    return None


def _signed_divisors(value: int) -> list[int]:
    """Return every positive and negative divisor of one nonzero integer."""
    if value == 0:
        raise ValueError("zero has infinitely many divisors")
    positive: set[int] = set()
    for candidate in range(1, math.isqrt(abs(value)) + 1):
        if value % candidate == 0:
            positive.add(candidate)
            positive.add(abs(value) // candidate)
    return sorted(positive | {-divisor for divisor in positive})


def _monic_integer_quartic_irreducible(high_to_low: Sequence[Rat]) -> bool | None:
    """Decide irreducibility for a monic integer quartic by exact factor exclusion.

    Gauss's lemma makes this finite: a reducible monic integer quartic has either an
    integer root or a factorisation into two monic integer quadratics.  ``None`` means
    that the polynomial is outside this deliberately narrow complete fallback.
    """
    if (
        len(high_to_low) != 5
        or high_to_low[0] != 1
        or any(coefficient.denominator != 1 for coefficient in high_to_low)
    ):
        return None
    _, a, b, c, d = (int(coefficient) for coefficient in high_to_low)
    reducible = d == 0

    # A linear factor of a monic integer polynomial supplies an integer root dividing
    # the constant term.
    if not reducible:
        for root in _signed_divisors(d):
            if _eval_poly(list(reversed(high_to_low)), Rat(root)) == 0:
                reducible = True
                break

    # Exclude (x^2 + p*x + q)(x^2 + r*x + s) for every q*s = d.
    if not reducible:
        for q in _signed_divisors(d):
            s = d // q
            if s != q:
                numerator = c - q * a
                denominator = s - q
                if numerator % denominator:
                    continue
                p = numerator // denominator
                r = a - p
                if q + s + p * r == b:
                    reducible = True
                    break
                continue

            if c != q * a:
                continue
            product = b - 2 * q
            discriminant = a * a - 4 * product
            if discriminant < 0:
                continue
            root = math.isqrt(discriminant)
            if root * root == discriminant and (a + root) % 2 == 0:
                reducible = True
                break
    return not reducible


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
        if self.degree < 1:
            raise FieldPreconditionError(
                "a number field needs a polynomial of degree at least one"
            )
        self._high_to_low = [c / coeffs[0] for c in coeffs]
        self._low_to_high = self._high_to_low[::-1]  # monic, low->high

        lo, hi = Rat(isolating[0]), Rat(isolating[1])
        if lo >= hi:
            raise ValueError("isolating interval must be nonempty")
        endpoint_values = self._eval_min_poly(lo), self._eval_min_poly(hi)
        if 0 in endpoint_values:
            raise FieldPreconditionError("an isolating-interval endpoint is a polynomial root")

        if self.degree == 1:
            irreducibility_method = "degree-one"
            irreducibility_prime = None
        else:
            irreducibility_method = "irreducible-reduction-mod-prime"
            irreducibility_prime = _irreducibility_prime(self._high_to_low)
            if irreducibility_prime is None:
                quartic_decision = _monic_integer_quartic_irreducible(self._high_to_low)
                if quartic_decision is False:
                    raise FieldPreconditionError("polynomial is reducible over Q")
                if quartic_decision is True:
                    irreducibility_method = "monic-integer-quartic-factor-exclusion"
                else:
                    raise FieldPreconditionError(
                        "irreducibility over Q was not established by an irreducible "
                        "reduction modulo any searched prime or a supported complete "
                        "factor-exclusion method"
                    )

        root_count = _root_count(self._low_to_high, lo, hi)
        if root_count != 1:
            raise FieldPreconditionError(
                f"isolating interval must contain exactly one real root; found {root_count}"
            )

        self._declared_lo, self._declared_hi = lo, hi
        self._irreducibility_method = irreducibility_method
        self._irreducibility_prime = irreducibility_prime
        self._root_count = root_count
        if self.degree == 1:
            root = -self._high_to_low[1]
            self._lo = self._hi = root
            self._sign_at_lo = 0
        else:
            self._lo, self._hi = lo, hi
            self._sign_at_lo = 1 if endpoint_values[0] > 0 else -1
        self.refinements = 0

    def precondition_certificate(self) -> dict[str, object]:
        """Return the exact facts checked before field arithmetic was enabled."""
        return {
            "normalized_minimal_polynomial": [str(value) for value in self._high_to_low],
            "irreducible_over_q": True,
            "irreducibility_method": self._irreducibility_method,
            "irreducibility_prime": self._irreducibility_prime,
            "declared_isolating_interval": [str(self._declared_lo), str(self._declared_hi)],
            "root_count_method": "sturm-sequence-over-q",
            "root_count_in_open_interval": self._root_count,
            "endpoints_are_not_roots": True,
        }

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
        if self.degree == 1:
            return
        mid = (self._lo + self._hi) / 2
        v = self._eval_min_poly(mid)
        if v == 0:
            raise RuntimeError(
                "an irreducible polynomial of degree above one had a rational root"
            )
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

    def enclose(self, e: FieldElement) -> tuple[Rat, Rat]:
        """Rigorous rational enclosure of `e`, at the current refinement.

        Public for the same reason as :meth:`root_bounds`: a caller bridging exact
        field arithmetic into interval arithmetic legitimately needs an enclosure of an
        *element*, not only of the root, and reaching into the private evaluator to get
        one couples it to how refinement is stored.  Call :meth:`refine_to` first if a
        tighter enclosure is wanted; this never widens one.
        """
        return self._enclose(e.coeffs)

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
        lo, hi = self._enclose(e.coeffs)

        def as_dec(q: Rat) -> decimal.Decimal:
            return decimal.Decimal(q.numerator) / decimal.Decimal(q.denominator)

        # `decimal` keeps precision in a THREAD-GLOBAL context, so setting it here
        # without restoring it would silently rewiden every unrelated Decimal in the
        # process. It did: one refinement at 30 digits left the context at 50, and the
        # atlas renderer -- which computes its coordinates in Decimal -- then emitted
        # different SVG bytes depending on whether a test had refined a field first
        # (D-359). The working precision is this method's business alone.
        with decimal.localcontext() as context:
            context.prec = digits + 20
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
            self.field,
            self.field._reduce(_poly_mul(self.coeffs, other.coeffs)),  # pyright: ignore[reportPrivateUsage]
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
            columns.append(
                f._reduce(_poly_mul(self.coeffs, basis))  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
            )
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
        lo, hi = self.field._enclose(self.coeffs)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
        return float((lo + hi) / 2)

    def __repr__(self) -> str:
        return f"FieldElement({[str(c) for c in self.coeffs]})"
