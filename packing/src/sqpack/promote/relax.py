"""A certified upper bound, obtained by opening every contact a measurable amount.

This module answers the question block 1 left standing.
:mod:`sqpack.promote.interval_verify` refuses on a tight packing, correctly: a record
packing's contacts are exact zeros, and no enclosure of positive width certifies an
equality.  So an interval checker pointed at a record *as it stands* can never say yes,
and that is not a defect to engineer around.

The way out is to certify a different, slightly worse packing whose validity is a
strict inequality everywhere.  Scale the centres apart by `1 + eps`, leaving every
square exactly unit and exactly as oriented:

```
p  ->  p + eps * c        (p a corner, c its square's centre)
```

Three things follow, and each is checked here rather than assumed:

- **Nothing moves toward the origin.**  Centres are positive, so every coordinate only
  increases and the `x, y >= 0` half of containment cannot be broken by the relaxation.
- **Every contact opens.**  Two squares with disjoint interiors have their centres on
  opposite sides of a separating line, so moving the centres apart along that line
  strictly increases the gap.  Touching pairs become strictly separated.
- **The container grows by a bounded amount.**  Every centre lies within the original
  side `s`, so no corner exceeds `(1 + eps) s`.

What comes out is a genuine theorem of the form `s(n) <= S`, with `S` a decimal that is
strictly above the optimum and approaches it as `eps` falls.  It is weaker than the
exact route, which reaches the optimum itself, and it needs no minimal polynomial --
which is the whole reason it exists, since at `n = 29` nobody has one.

**The relaxation is reported, never hidden.**  A bound whose `eps` is not stated is
indistinguishable from a claim about the optimum, and the two are different claims.
:func:`relaxation_series` exists so the gap can be watched closing rather than asserted
to be small.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from itertools import pairwise

import mpmath as mp

from sqpack.promote.enclose import SquareBox
from sqpack.promote.interval import Interval, decimal_string, from_endpoints, interval
from sqpack.promote.interval_verify import IntervalReport, verify_interval


class RelaxationError(ValueError):
    """A typed failure from the relaxation route, carrying a `kind` to branch on."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True)
class CertifiedBound:
    """One certified upper bound, with the relaxation that bought it."""

    n: int
    relaxation: str
    bound: str
    certified: bool
    report: IntervalReport

    def claim(self) -> str:
        """The statement this bound supports, in the only form it supports it."""
        if not self.certified:
            return (
                f"no bound: {self.report.refusal_reason()}"
                if self.report.refusal_reason()
                else "no bound"
            )
        return (
            f"s({self.n}) <= {self.bound}, by interval certification of a packing "
            f"relaxed by eps = {self.relaxation}"
        )


def centre_of(square: SquareBox) -> tuple[Interval, Interval]:
    """The centre of a corner box, as the mean of its four corners."""
    quarter = interval("0.25")
    x = (square[0][0] + square[1][0] + square[2][0] + square[3][0]) * quarter
    y = (square[0][1] + square[1][1] + square[2][1] + square[3][1]) * quarter
    return x, y


def relax(squares: Sequence[SquareBox], epsilon: str) -> list[SquareBox]:
    """Move every square outward from the origin by `epsilon` times its centre.

    Shapes and orientations are untouched -- only centres move -- so the result is still
    a set of unit squares, and it is still one this module never has to re-check for
    shape.
    """
    scale = interval(epsilon)
    if mp.mpf(scale.a) <= 0:
        raise RelaxationError(
            "non-positive-relaxation",
            f"eps must be strictly positive to open a contact, got {epsilon}",
        )
    relaxed = []
    for square in squares:
        centre_x, centre_y = centre_of(square)
        shift_x, shift_y = scale * centre_x, scale * centre_y
        relaxed.append([(x + shift_x, y + shift_y) for x, y in square])
    return relaxed


def containing_side(squares: Sequence[SquareBox]) -> Interval:
    """The smallest side this layout is proved to fit inside, outward-rounded up."""
    highs = [mp.mpf(value.b) for square in squares for pair in square for value in pair]
    lows = [mp.mpf(value.a) for square in squares for pair in square for value in pair]
    if min(lows) < 0:
        raise RelaxationError(
            "outside-the-first-quadrant",
            f"a corner encloses a coordinate as low as {mp.nstr(min(lows), 8)}, so the "
            "layout is not anchored at the origin and this side is not its container",
        )
    return from_endpoints(max(highs), max(highs))


def certified_upper_bound(
    squares: Sequence[SquareBox], *, epsilon: str, digits: int = 30
) -> CertifiedBound:
    """Certify `s(n) <= S` for the smallest `S` this relaxed layout is proved to fit.

    The side is read off the relaxed corners rather than supplied, so the bound is the
    tightest one this construction supports and cannot be quietly inflated until the
    verification passes.
    """
    relaxed = relax(squares, epsilon)
    side = containing_side(relaxed)
    bound = decimal_string(mp.mpf(side.b), digits, upward=True)
    report = verify_interval(relaxed, interval(bound), side_label=bound)
    return CertifiedBound(
        n=len(squares),
        relaxation=epsilon,
        bound=bound,
        certified=report.certified,
        report=report,
    )


def relaxation_series(
    squares: Sequence[SquareBox], ladder: Sequence[str], *, digits: int = 30
) -> list[dict[str, str]]:
    """Certify at each `eps` in `ladder` and report the bound each one buys.

    A single impressive-looking bound says nothing on its own: it could be the tightest
    this construction reaches, or it could be one rung of a sequence that was stopped
    early.  Watching the bound fall as `eps` falls is what distinguishes a relaxation
    that is converging on the optimum from one that has hit a floor somewhere else.
    """
    rows: list[dict[str, str]] = []
    for epsilon in ladder:
        result = certified_upper_bound(squares, epsilon=epsilon, digits=digits)
        rows.append(
            {
                "epsilon": epsilon,
                "bound": result.bound,
                "certified": "yes" if result.certified else "no",
                "undecided_pairs": str(len(result.report.undecided_pairs)),
            }
        )
    return rows


def bound_falls(series: Sequence[dict[str, str]]) -> bool:
    """Whether every rung certifies and each bound improves on the one below it."""
    if len(series) < 2:
        return False
    if any(row["certified"] != "yes" for row in series):
        return False
    values = [mp.mpf(row["bound"]) for row in series]
    return all(later < earlier for earlier, later in pairwise(values))
