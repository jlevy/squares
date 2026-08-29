"""Separating-axis verification over enclosures, where "undecided" is a real answer.

This is the last stage before a witness, and the one that decides what an interval
certificate is actually allowed to say.

**What it can prove, and what it cannot.**  An enclosure of positive width can certify
a *strict* inequality and can never certify an equality.  So this module can prove a
pair strictly disjoint and can prove a corner strictly inside the container, and it can
prove neither of those things about a pair touching at exactly zero separation.  Trump's
`n = 11` packing has 14 such pairs out of 55.  That is not a limitation to engineer
around; it is the reason a certified *upper bound* is stated against a side slightly
above the optimum, where every inequality has margin, rather than at the optimum, where
half of them are equalities.

**Why this does not simply pass `interval_sign` into `verify_packing`.**  The seam is
real -- that function takes an injected `sign` and its geometry is scalar-agnostic --
but substituting an interval sign directly is measurably too strict, in two places:

- :func:`sqpack.verify.project` finds a projection's extent by comparing corner
  projections, and two enclosures that overlap have no decidable order, so the
  projection refuses before any separation question is asked.  An enclosure of the
  extent needs no comparison at all and is computed here instead.
- :func:`sqpack.verify.separated` folds all four axes together, so an undecided sign on
  the first axis discards a pair that the third axis separates strictly.  A pair is
  separated when *some* axis separates it, which means each axis has to be allowed to
  fail on its own.

Both are properties of a float-shaped fold rather than errors in that module, and
neither is visible until a sign can refuse.  The geometry itself -- which axes to try,
how a square projects, what separation means -- is unchanged and still comes from
:func:`sqpack.verify.edge_axes`.

Every verdict is one of three, and they are kept apart on purpose: `separated` is
proved, `overlapping` is proved, and `undecided` is the honest remainder.  Folding
`undecided` into either of the other two is the whole failure mode this route exists to
avoid.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from dataclasses import field as _dc_field

import mpmath as mp

from sqpack.promote.enclose import SquareBox
from sqpack.promote.interval import Interval, from_endpoints
from sqpack.verify import edge_axes

SEPARATED = "separated"
OVERLAPPING = "overlapping"
UNDECIDED = "undecided"


@dataclass(frozen=True)
class IntervalReport:
    """What could and could not be certified about one layout at one side.

    `certified` is true only when every pair is *proved* disjoint and every corner is
    *proved* inside.  An undecided pair leaves it false while `overlaps` stays empty,
    which is the distinction between "this packing is invalid" and "these enclosures
    are too wide to say".
    """

    certified: bool
    n: int
    side: str
    pairs_tested: int
    separated_pairs: int
    undecided_pairs: list[tuple[int, int]] = _dc_field(default_factory=list)
    overlapping_pairs: list[tuple[int, int]] = _dc_field(default_factory=list)
    container_failures: list[str] = _dc_field(default_factory=list)
    undecided_container: list[str] = _dc_field(default_factory=list)

    def refusal_reason(self) -> str | None:
        """One sentence naming why this is not a certificate, or `None` if it is."""
        if self.certified:
            return None
        if self.overlapping_pairs:
            pair = self.overlapping_pairs[0]
            return (
                f"squares {pair[0]} and {pair[1]} are proved to overlap, so this layout "
                "is not a packing at this side"
            )
        if self.container_failures:
            return self.container_failures[0]
        if self.undecided_pairs:
            pair = self.undecided_pairs[0]
            return (
                f"separation of squares {pair[0]} and {pair[1]} is undecided at these "
                f"enclosures, along with {len(self.undecided_pairs) - 1} other pair(s); "
                "a tighter pose box or a larger side would decide it, and no tolerance "
                "will"
            )
        if self.undecided_container:
            return self.undecided_container[0]
        return "nothing was certified and nothing was refuted"

    def __str__(self) -> str:
        head = "CERTIFIED" if self.certified else "NOT CERTIFIED"
        lines = [
            (
                f"{head}: {self.n} squares in [0, {self.side}]^2, "
                f"{self.pairs_tested} pairs tested"
            ),
            (
                f"  pairs:     {self.separated_pairs} strictly separated, "
                f"{len(self.undecided_pairs)} undecided, "
                f"{len(self.overlapping_pairs)} overlapping"
            ),
        ]
        reason = self.refusal_reason()
        if reason:
            lines.append(f"  REFUSED: {reason}")
        return "\n".join(lines)


def _projection_extent(
    square: SquareBox, axis: tuple[Interval, Interval]
) -> tuple[Interval, Interval]:
    """Enclosures of the least and greatest projection of a square onto `axis`.

    No comparison of enclosures happens here.  The least projection lies between the
    least of the lower endpoints and the least of the upper ones, and symmetrically for
    the greatest, which encloses both extremes without deciding any order.
    """
    values = [axis[0] * x + axis[1] * y for x, y in square]
    lows = [mp.mpf(v.a) for v in values]
    highs = [mp.mpf(v.b) for v in values]
    return from_endpoints(min(lows), min(highs)), from_endpoints(max(lows), max(highs))


def pair_verdict(first: SquareBox, second: SquareBox) -> str:
    """Whether two corner boxes are provably separated, provably overlapping, or neither.

    Each of the four candidate axes is tried independently.  One axis proving strict
    separation settles the pair; only when no axis proves separation *and* every axis
    proves interpenetration is an overlap proved.
    """
    axes = edge_axes(first) + edge_axes(second)
    all_axes_overlap = True
    for axis in axes:
        first_low, first_high = _projection_extent(first, axis)
        second_low, second_high = _projection_extent(second, axis)
        forward = second_low - first_high
        backward = first_low - second_high
        if mp.mpf(forward.a) > 0 or mp.mpf(backward.a) > 0:
            return SEPARATED
        # This axis fails to separate only if both gaps are proved negative; an
        # enclosure straddling zero leaves the axis undecided, not overlapping.
        if not (mp.mpf(forward.b) < 0 and mp.mpf(backward.b) < 0):
            all_axes_overlap = False
    return OVERLAPPING if all_axes_overlap else UNDECIDED


def verify_interval(
    squares: Sequence[SquareBox], side: Interval, *, side_label: str | None = None
) -> IntervalReport:
    """Certify that `squares` is a packing of unit squares in `[0, side]^2`.

    `side` is an enclosure and is used at its **upper** endpoint for containment, since
    the claim being built is an upper bound: a layout that fits inside the largest side
    the enclosure admits fits inside every larger one.  Shape checking is not performed
    and cannot be -- see :mod:`sqpack.promote.enclose` for why a unit square is a matter
    of construction here rather than of measurement.
    """
    limit = mp.mpf(side.b)
    label = side_label or str(mp.nstr(limit, 20))
    report_container: list[str] = []
    report_undecided_container: list[str] = []

    for index, square in enumerate(squares):
        for corner, (x, y) in enumerate(square):
            for value, edge in ((x, "x"), (y, "y")):
                low, high = mp.mpf(value.a), mp.mpf(value.b)
                if high < 0 or low > limit:
                    report_container.append(
                        f"square {index} corner {corner} is proved outside the "
                        f"container on {edge}"
                    )
                elif not (low >= 0 and high <= limit):
                    report_undecided_container.append(
                        f"square {index} corner {corner} has {edge} in "
                        f"[{mp.nstr(low, 8)}, {mp.nstr(high, 8)}], which is not proved "
                        f"inside [0, {mp.nstr(limit, 8)}]"
                    )

    undecided: list[tuple[int, int]] = []
    overlapping: list[tuple[int, int]] = []
    separated = 0
    tested = 0
    count = len(squares)
    for i in range(count):
        for j in range(i + 1, count):
            tested += 1
            verdict = pair_verdict(squares[i], squares[j])
            if verdict == SEPARATED:
                separated += 1
            elif verdict == OVERLAPPING:
                overlapping.append((i, j))
            else:
                undecided.append((i, j))

    certified = not (undecided or overlapping or report_container or report_undecided_container)
    return IntervalReport(
        certified=certified,
        n=count,
        side=label,
        pairs_tested=tested,
        separated_pairs=separated,
        undecided_pairs=undecided,
        overlapping_pairs=overlapping,
        container_failures=report_container,
        undecided_container=report_undecided_container,
    )
