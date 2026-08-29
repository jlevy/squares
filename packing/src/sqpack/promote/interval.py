"""Interval scalars with directed rounding, and a sign that refuses rather than guesses.

This is the arithmetic floor under the interval-certification route.  Everything above
it -- the Krawczyk operator, the layout map, the interval separating-axis test -- is
only as sound as the rounding here, which is why none of it is hand-rolled.

**Why `mpmath.iv` and not our own.**  Rounding-mode mistakes in hand-written interval
code fail silently *and in the unsafe direction*: an enclosure that is too tight still
looks like an enclosure, and the certificate built on it is simply wrong with nothing
to notice.  `mpmath.iv` supplies outward-rounded arithmetic and interval
transcendentals that have been exercised far more than anything written here would be.
It is not a formally verified library, and the assurance ladder records
`interval-certified` below `proof-assistant-checked` for exactly that reason.

**The sign contract is the load-bearing part of this module.**  An enclosure that
straddles zero does not tell you the value is zero; it tells you that you do not know.
So :func:`interval_sign` decides only what an enclosure can actually decide:

- entirely above zero, return `1`;
- entirely below zero, return `-1`;
- the degenerate interval `[0, 0]`, return `0` -- the one case where zero is *proved*,
  reachable only when exact inputs produced an exact cancellation;
- anything else, raise :class:`IntervalRefusalError`.

The fourth case is what makes the checker honest.  A tight packing has pairs touching
at exactly zero separation, and no enclosure of positive width can certify one of
those.  Refusing to say is the correct answer, and a verifier that returned `0` there
would be claiming a contact it cannot see.

**Derivatives.**  A Krawczyk operator needs `F'` over a *box*, not at a point, so
numerical differencing is not available -- it would produce a number where a rigorous
enclosure is required.  :class:`Dual` is forward-mode automatic differentiation carried
out in interval arithmetic, so the Jacobian it returns encloses every derivative value
the box contains.  A system written in the ordinary arithmetic of this module gets its
Jacobian for free and never has one transcribed by hand, which is the step that would
otherwise silently disagree with the system it is supposed to differentiate.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal, localcontext
from typing import Any

import mpmath as mp
from mpmath.libmp import to_rational

# The interval scalar type. Named rather than inlined because callers annotate against
# it and `mpmath` spells it `ivmpf`, which says nothing at a call site.
Interval = Any

Number = int | float | str | Interval


class IntervalRefusalError(ValueError):
    """A typed refusal from interval arithmetic, carrying a `kind` to branch on.

    Refusal is a first-class result on this route, not an error path.  A checker that
    cannot refuse has not been tested, and one that widens until it succeeds is worse
    than none, so every place that cannot decide raises this instead of choosing.
    """

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


def interval(lo: Number, hi: Number | None = None) -> Interval:
    """An interval from decimal strings, outward-rounded to the current precision.

    Strings rather than floats on purpose: `0.1` as a Python float is already a
    different number than the one written, and an enclosure built from it encloses the
    wrong value before any arithmetic happens.

    This and :func:`from_endpoints` are the only two places an enclosure is built, so
    `mpmath`'s constructor annotation -- which admits `int` and nothing else, though
    the implementation takes strings, floats and pairs -- is suppressed once here
    rather than at every call site.
    """
    if hi is None:
        return mp.iv.mpf(lo)  # pyright: ignore[reportArgumentType]
    return from_endpoints(lo, hi)


def from_endpoints(lo: Number, hi: Number) -> Interval:
    """An enclosure spanning `[lo, hi]`, from endpoints already computed elsewhere."""
    return mp.iv.mpf([lo, hi])  # pyright: ignore[reportArgumentType]


def endpoints(value: Interval) -> tuple[Any, Any]:
    """The `(lower, upper)` endpoints of an enclosure, as ordinary mpmath floats."""
    return mp.mpf(value.a), mp.mpf(value.b)


def width(value: Interval) -> Any:
    """How wide the enclosure is; the honest measure of what a certificate proved."""
    lo, hi = endpoints(value)
    return hi - lo


def midpoint(value: Interval) -> Any:
    """The centre of an enclosure, as an ordinary float."""
    lo, hi = endpoints(value)
    return (lo + hi) / 2


def decimal_string(value: Any, digits: int, *, upward: bool) -> str:
    """`value` as a decimal string rounded strictly outward, never to nearest.

    This exists because serializing a certificate is itself an arithmetic operation,
    and it is the one place an otherwise-rigorous enclosure is most easily lost.
    Rounding the endpoints of a certified box to nearest can move both of them past
    the root the box was proved to contain, leaving a certificate that reads correctly
    and no longer encloses anything -- a failure in exactly the flattering direction
    the defect log keeps recording.  Measured on `sqrt(2)` at 40 digits: nearest
    rounding lifts the lower endpoint to `...078570`, above the root at `...0785696`.

    An `mpf` is dyadic, so :func:`mpmath.libmp.to_rational` converts it with no loss
    and the directed rounding happens once, in `decimal`, where it is exact.
    """
    numerator, denominator = to_rational(mp.mpf(value)._mpf_)
    with localcontext() as context:
        context.prec = max(1, digits)
        context.rounding = ROUND_CEILING if upward else ROUND_FLOOR
        return str(Decimal(numerator) / Decimal(denominator))


def total(values: Sequence[Interval]) -> Interval:
    """Left-to-right sum of enclosures.

    `sum` would do, and does not type-check: `mpmath`'s interval scalar declares no
    `__add__` in its annotations even though it has one.  Accumulating here keeps that
    one quirk in a single place instead of a suppression at every dot product.
    """
    result = mp.iv.mpf(0)
    for value in values:
        result = result + value
    return result


def contains_zero(value: Interval) -> bool:
    """Whether the enclosure contains zero, and so cannot decide a sign."""
    lo, hi = endpoints(value)
    return lo <= 0 <= hi


def interval_sign(value: Interval) -> int:
    """Sign of an enclosure, or a refusal when the enclosure cannot decide one.

    This is the `sign` callable :func:`sqpack.verify.verify_packing` accepts, and
    substituting it is what turns that function from a float check into an interval
    one without changing a line of its geometry.
    """
    lo, hi = endpoints(value)
    if lo > 0:
        return 1
    if hi < 0:
        return -1
    if lo == 0 and hi == 0:
        return 0
    raise IntervalRefusalError(
        "undecided-sign",
        f"the enclosure [{mp.nstr(lo, 8)}, {mp.nstr(hi, 8)}] straddles zero, so its "
        "sign is not decided; widening precision may decide it and no tolerance can",
    )


def _as_interval(value: Number) -> Interval:
    if isinstance(value, mp.ctx_iv.ivmpf):
        return value
    return mp.iv.mpf(value)  # pyright: ignore[reportArgumentType]


class Dual:
    """One interval value carrying its partial derivatives, for forward-mode AD.

    Each instance holds an enclosure of a quantity and enclosures of that quantity's
    partial derivatives with respect to every unknown.  Evaluating a system on `Dual`
    seeds therefore produces the residual enclosures *and* the interval Jacobian in one
    pass, over whatever box the seeds describe.

    Arithmetic is the ordinary set: the contact systems this route handles are built
    from sums, products, quotients and the two trigonometric functions, with no square
    roots and no branching on a comparison, which is what makes them differentiable
    everywhere the box reaches.
    """

    __slots__ = ("derivatives", "value")

    def __init__(self, value: Number, derivatives: Sequence[Number]):
        self.value = _as_interval(value)
        self.derivatives = tuple(_as_interval(d) for d in derivatives)

    @classmethod
    def seeds(cls, values: Sequence[Number]) -> list[Dual]:
        """Independent variables: each one's derivative is 1 in its own slot."""
        count = len(values)
        out = []
        for index, value in enumerate(values):
            derivatives = [mp.iv.mpf(0)] * count
            derivatives[index] = mp.iv.mpf(1)
            out.append(cls(value, derivatives))
        return out

    def _lift(self, other: Any) -> Dual:
        if isinstance(other, Dual):
            return other
        return Dual(other, [mp.iv.mpf(0)] * len(self.derivatives))

    def __add__(self, other: Any) -> Dual:
        rhs = self._lift(other)
        return Dual(
            self.value + rhs.value,
            [a + b for a, b in zip(self.derivatives, rhs.derivatives, strict=True)],
        )

    __radd__ = __add__

    def __neg__(self) -> Dual:
        return Dual(-self.value, [-d for d in self.derivatives])

    def __sub__(self, other: Any) -> Dual:
        return self + (-self._lift(other))

    def __rsub__(self, other: Any) -> Dual:
        return self._lift(other) + (-self)

    def __mul__(self, other: Any) -> Dual:
        rhs = self._lift(other)
        return Dual(
            self.value * rhs.value,
            [
                a * rhs.value + self.value * b
                for a, b in zip(self.derivatives, rhs.derivatives, strict=True)
            ],
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> Dual:
        rhs = self._lift(other)
        if contains_zero(rhs.value):
            raise IntervalRefusalError(
                "division-by-straddling-zero",
                "a divisor enclosure contains zero, so the quotient is unbounded and "
                "no finite enclosure of it exists",
            )
        quotient = self.value / rhs.value
        return Dual(
            quotient,
            [
                (a - quotient * b) / rhs.value
                for a, b in zip(self.derivatives, rhs.derivatives, strict=True)
            ],
        )

    def __rtruediv__(self, other: Any) -> Dual:
        return self._lift(other) / self

    def __pow__(self, power: int) -> Dual:
        if not isinstance(power, int) or power < 0:
            raise IntervalRefusalError(
                "unsupported-power",
                f"only non-negative integer powers are differentiated here, got {power!r}",
            )
        result = Dual(mp.iv.mpf(1), [mp.iv.mpf(0)] * len(self.derivatives))
        for _ in range(power):
            result = result * self
        return result


def carrier(value: Number) -> Dual:
    """An enclosure that mixes cleanly with ordinary `mpmath` constants.

    `mpmath` will not promote an `mpf` to an interval: `mp.mpf(3) + enclosure` raises
    rather than widening, so a transcription written with `mp.mpf` constants -- which
    every one of them here is, because they were written for the numeric route --
    cannot be evaluated on bare enclosures at all.

    A dual carrying no derivatives is the smallest thing that fixes it.  It is an
    enclosure with the reflected operators attached, so the constants meet something
    that knows how to absorb them, and it costs nothing because there are no partials to
    propagate. Use :meth:`Dual.seeds` when the Jacobian is wanted and this when it is
    not.
    """
    return Dual(value, ())


def sin(value: Any) -> Any:
    """Interval sine, lifted over :class:`Dual` when it is handed one."""
    if isinstance(value, Dual):
        cosine = mp.iv.cos(value.value)
        return Dual(mp.iv.sin(value.value), [cosine * d for d in value.derivatives])
    return mp.iv.sin(_as_interval(value))


def cos(value: Any) -> Any:
    """Interval cosine, lifted over :class:`Dual` when it is handed one."""
    if isinstance(value, Dual):
        sine = mp.iv.sin(value.value)
        return Dual(mp.iv.cos(value.value), [-sine * d for d in value.derivatives])
    return mp.iv.cos(_as_interval(value))


def evaluate(
    system: Callable[..., Sequence], point: Sequence[Number]
) -> tuple[list[Interval], list[list[Interval]]]:
    """Residual enclosures and the interval Jacobian of `system` over `point`.

    `point` may be degenerate intervals, giving the Jacobian at a point, or wide ones,
    giving an enclosure of the Jacobian over the whole box.  The Krawczyk operator
    needs both, from the same code, which is the reason this returns them together.
    """
    seeds = Dual.seeds(point)
    residuals = system(*seeds)
    values: list[Interval] = []
    rows: list[list[Interval]] = []
    for residual in residuals:
        if isinstance(residual, Dual):
            values.append(residual.value)
            rows.append(list(residual.derivatives))
        else:
            # A residual that does not depend on any unknown is still a residual; its
            # row is zero rather than missing, so the Jacobian stays rectangular.
            values.append(_as_interval(residual))
            rows.append([mp.iv.mpf(0)] * len(point))
    return values, rows


def _radians_per_degree() -> Interval:
    """One degree in radians, as an enclosure at the ambient precision.

    Computed rather than stored: the enclosure has to be built at whatever precision the
    caller is running, and `mp.iv.pi` is a context-sensitive constant.
    """
    return _as_interval(mp.iv.pi) / _as_interval(180)


def sin_degrees(degrees: Any) -> Any:
    """Sine of an angle in degrees, over whichever scalar type it is handed.

    The `n = 29` transcription is written in degrees, because its source is, and it has
    to serve two routes now: ordinary evaluation, which checks the publication against
    itself, and interval evaluation, which is what a certificate needs.  Dispatching
    here rather than duplicating the transcription is deliberate -- a second copy of a
    six-equation contact system is a second thing to keep correct, and the first
    divergence between them would be silent.
    """
    if isinstance(degrees, Dual | mp.ctx_iv.ivmpf):
        return sin(degrees * _radians_per_degree())
    return mp.sin(mp.radians(degrees))


def cos_degrees(degrees: Any) -> Any:
    """Cosine of an angle in degrees, over whichever scalar type it is handed."""
    if isinstance(degrees, Dual | mp.ctx_iv.ivmpf):
        return cos(degrees * _radians_per_degree())
    return mp.cos(mp.radians(degrees))
