"""The Krawczyk operator: existence and uniqueness of a root inside a box.

This is the step that turns a high-precision *approximation* into a rigorous
*enclosure*, and it is the reason the interval route can certify a value whose minimal
polynomial nobody has recovered.  Newton refinement, which
:mod:`sqpack.promote.refine` already does, produces a point with a small residual.  A
small residual is not a root: it is consistent with a root nearby, with a root far
away, and with no root at all in an ill-conditioned system.  The operator here decides
which, over a box, with directed rounding throughout.

For `F: R^m -> R^m`, a box `X`, its midpoint `x*`, and `C` an approximate inverse of
`F'(x*)`:

```
K(X) = x* - C F(x*) + (I - C F'(X)) (X - x*)
```

Two standard facts do all the work, and this implementation depends on nothing else:

- if `K(X)` is a subset of `X`, then `F` has **at least one** root in `X`;
- if `K(X)` lies in the **interior** of `X`, that root is **unique** in `X`.

`C` is an ordinary floating-point matrix and is allowed to be a poor inverse.  It never
enters the conclusion -- a bad `C` makes the containment test fail, never makes it pass
wrongly -- which is what lets the expensive part stay in cheap arithmetic.

**`unique` is the load-bearing field, not `exists`.**  A box known to hold *a* root does
not say which pose was certified, and a box holding two roots certifies neither.  So
interior containment is tested rather than containment, and the two verdicts are
reported separately instead of being collapsed into one boolean that would hide the
difference.  Nothing downstream may promote a root that is not unique.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

import mpmath as mp

from sqpack.promote.interval import (
    Interval,
    IntervalRefusalError,
    decimal_string,
    endpoints,
    evaluate,
    from_endpoints,
    interval,
    midpoint,
    total,
    width,
)

System = Callable[..., Sequence]

# The operator is evaluated above the precision a caller asks about, so the reported
# enclosure is not the one carrying the operator's own rounding.
DEFAULT_GUARD_DIGITS = 20


class CertificationError(ValueError):
    """A typed certification failure, carrying a `kind` a caller can branch on."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True)
class PoseBox:
    """A box of unknowns, as exact decimal strings in a declared order.

    Strings rather than floats because a box is the certificate's subject: it has to
    mean the same thing when it is read back at a different precision, and a float
    endpoint means whatever the reader's precision makes of it.
    """

    names: tuple[str, ...]
    lo: tuple[str, ...]
    hi: tuple[str, ...]
    radius: str

    def __post_init__(self) -> None:
        if not (len(self.names) == len(self.lo) == len(self.hi)):
            raise CertificationError(
                "bad-request",
                f"{len(self.names)} names against {len(self.lo)} lower and "
                f"{len(self.hi)} upper endpoints",
            )

    @classmethod
    def around(cls, names: Sequence[str], centre: Sequence[str], radius: str) -> PoseBox:
        """A box of the given radius around a point, outward-rounded to strings."""
        span = mp.mpf(radius)
        digits = mp.mp.dps
        lo, hi = [], []
        for value in centre:
            point = mp.mpf(value)
            # Outward on both sides, so the box actually delivered is never narrower
            # than the radius the caller asked for.
            lo.append(decimal_string(point - span, digits, upward=False))
            hi.append(decimal_string(point + span, digits, upward=True))
        return cls(tuple(names), tuple(lo), tuple(hi), radius)

    def intervals(self) -> list[Interval]:
        """The box as interval scalars at the ambient precision."""
        return [from_endpoints(lo, hi) for lo, hi in zip(self.lo, self.hi, strict=True)]

    def max_half_width(self) -> Any:
        """The widest half-width across components; how much the box actually claims."""
        return max(
            (mp.mpf(hi) - mp.mpf(lo)) / 2 for lo, hi in zip(self.lo, self.hi, strict=True)
        )


@dataclass(frozen=True)
class CertifiedRoot:
    """What the operator decided, with everything needed to distrust it."""

    box: PoseBox
    exists: bool
    unique: bool
    operator: str
    iterations: int
    working_precision: int
    max_radius: str

    def summary(self) -> str:
        verdict = (
            "a unique root"
            if self.unique
            else ("at least one root" if self.exists else "no verdict")
        )
        return (
            f"{self.operator}: {verdict} in a box of radius {self.max_radius} "
            f"after {self.iterations} iteration(s) at {self.working_precision} digits"
        )


def _subset(inner: Interval, outer: Interval) -> bool:
    ilo, ihi = endpoints(inner)
    olo, ohi = endpoints(outer)
    return olo <= ilo and ihi <= ohi


def _interior_subset(inner: Interval, outer: Interval) -> bool:
    ilo, ihi = endpoints(inner)
    olo, ohi = endpoints(outer)
    return olo < ilo and ihi < ohi


def _approximate_inverse(rows: Sequence[Sequence[Interval]]) -> Any:
    """An ordinary floating-point inverse of the Jacobian's midpoint matrix.

    Deliberately not rigorous.  `C` is a preconditioner: it decides whether the
    operator contracts, never whether the containment it reports is true.
    """
    size = len(rows)
    centre = mp.matrix(size, size)
    for i, row in enumerate(rows):
        for j, cell in enumerate(row):
            centre[i, j] = midpoint(cell)
    try:
        return mp.inverse(centre)
    except (ZeroDivisionError, ValueError) as error:
        raise CertificationError(
            "singular-jacobian",
            "the Jacobian midpoint is numerically singular, so no preconditioner "
            f"exists and the operator cannot contract: {error}",
        ) from error


def krawczyk_image(system: System, box: Sequence[Interval]) -> list[Interval]:
    """One application of `K` to a box, in interval arithmetic throughout."""
    size = len(box)
    centre = [interval(midpoint(value)) for value in box]

    point_values, point_rows = evaluate(system, centre)
    if len(point_values) != size:
        raise CertificationError(
            "not-square",
            f"{len(point_values)} equations against {size} unknowns; the operator "
            "needs a square system",
        )
    inverse = _approximate_inverse(point_rows)
    _, box_rows = evaluate(system, list(box))

    # C F(x*)
    corrections = [
        total([interval(inverse[i, k]) * point_values[k] for k in range(size)])
        for i in range(size)
    ]
    # I - C F'(X)
    residual_matrix = [
        [
            (mp.iv.mpf(1) if i == j else mp.iv.mpf(0))
            - total([interval(inverse[i, k]) * box_rows[k][j] for k in range(size)])
            for j in range(size)
        ]
        for i in range(size)
    ]
    offsets = [box[j] - centre[j] for j in range(size)]
    return [
        centre[i]
        - corrections[i]
        + total([residual_matrix[i][j] * offsets[j] for j in range(size)])
        for i in range(size)
    ]


def certify(
    system: System,
    box: PoseBox,
    *,
    digits: int = 50,
    guard_digits: int = DEFAULT_GUARD_DIGITS,
    max_iterations: int = 12,
) -> CertifiedRoot:
    """Decide existence and uniqueness of a root of `system` inside `box`.

    The operator is applied repeatedly, each time intersecting its image with the
    current box, for as long as that contracts.  Iterating is not needed for soundness
    -- one application that lands in the interior already proves uniqueness -- but a
    box that starts slightly too wide often contracts into one that does, and the
    tighter final box is what makes the downstream separating-axis tests decidable.
    """
    if len(box.names) == 0:
        raise CertificationError("bad-request", "an empty box certifies nothing")

    working = digits + guard_digits
    previous_iv, previous_mp = mp.iv.dps, mp.mp.dps
    mp.iv.dps = working
    mp.mp.dps = working
    try:
        current = box.intervals()
        # A verdict, once earned, is a proof about a specific box and cannot be undone
        # by anything a later iteration does. Keeping the best result rather than the
        # last one matters in practice: contraction eventually drives the box so tight
        # that the operator's own rounding makes `K(X)` marginally wider than `X`, and
        # a loop that reported its final state would throw away the proof it had.
        exists = unique = False
        proved = current
        iterations = 0
        for step in range(1, max_iterations + 1):
            image = krawczyk_image(system, current)
            exists_now = all(_subset(k, x) for k, x in zip(image, current, strict=True))
            unique_now = all(
                _interior_subset(k, x) for k, x in zip(image, current, strict=True)
            )
            if not exists_now:
                # `K(X)` escaping `X` is not a refutation: it says this box proved
                # nothing, which is a different claim and the only one available.
                break
            narrowed = [
                from_endpoints(
                    max(endpoints(k)[0], endpoints(x)[0]),
                    min(endpoints(k)[1], endpoints(x)[1]),
                )
                for k, x in zip(image, current, strict=True)
            ]
            if unique_now >= unique and exists_now >= exists:
                exists, unique = exists_now, unique_now
                proved = narrowed
                iterations = step
            shrank = any(
                width(new) < width(old) for new, old in zip(narrowed, current, strict=True)
            )
            current = narrowed
            if unique and not shrank:
                break

        # Outward on every endpoint: the serialized box has to still contain what the
        # operator proved it contains, and rounding to nearest does not guarantee that.
        certified = PoseBox(
            names=box.names,
            lo=tuple(decimal_string(endpoints(v)[0], digits, upward=False) for v in proved),
            hi=tuple(decimal_string(endpoints(v)[1], digits, upward=True) for v in proved),
            radius=decimal_string(max(width(v) for v in proved) / 2, 6, upward=True),
        )
        return CertifiedRoot(
            box=certified,
            exists=exists,
            unique=unique,
            operator="krawczyk",
            iterations=iterations,
            working_precision=working,
            max_radius=certified.radius,
        )
    except IntervalRefusalError as error:
        raise CertificationError(
            "interval-refusal",
            f"interval arithmetic could not decide a step of the operator: {error}",
        ) from error
    finally:
        mp.iv.dps = previous_iv
        mp.mp.dps = previous_mp
