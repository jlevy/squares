#!/usr/bin/env python3
"""Contract for the layout map and interval separating-axis verification.

The check that matters most here is the one that *fails*: four unit squares packed
exactly into a side-2 container, where every contact is an exact zero, must come back
undecided rather than certified.  A verifier that passes that case has a tolerance in
it somewhere and would certify overlaps of the same size.

The controls the interval-certification spec names are all here, and one measurement it
did not anticipate: substituting an interval `sign` straight into
:func:`sqpack.verify.verify_packing` refuses on a packing this module certifies, for
two reasons that are properties of a float-shaped fold rather than of the geometry.
That is recorded as a measurement, because it is the reason
:mod:`sqpack.promote.interval_verify` reimplements the fold instead of reusing it.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any

import mpmath as mp

from sqpack.promote.enclose import corner_span, corners_from_pose, enclose_layout, widen
from sqpack.promote.interval import IntervalRefusalError, interval_sign
from sqpack.promote.interval_verify import (
    OVERLAPPING,
    SEPARATED,
    UNDECIDED,
    pair_verdict,
    verify_interval,
)
from sqpack.verify import verify_packing

PRECISION = 40


def iv(value) -> Any:
    return mp.iv.mpf(value)


@contextmanager
def pinned_precision(digits: int = PRECISION):
    """Run at a declared precision, and put the global contexts back afterwards.

    `mpmath`'s precision is process-global, so a test that raises it changes what every
    later test measures.  That is not hypothetical here: an ambient 300-digit context
    left by another module made `mp.mpf("2.1")` land just *below* the outward-rounded
    corner span this file compares against, and the comparison failed on the rounding
    rather than on the geometry.
    """
    saved = mp.iv.dps, mp.mp.dps
    mp.iv.dps = mp.mp.dps = digits
    try:
        yield
    finally:
        mp.iv.dps, mp.mp.dps = saved


def four_square_layout(gap):
    """Four axis-aligned unit squares in a 2x2 arrangement, `gap` apart."""
    step = iv("1") + gap
    return [
        (iv("0.5") + step * i, iv("0.5") + step * j, iv("0")) for i in (0, 1) for j in (0, 1)
    ]


def certifies_when_there_is_room() -> None:
    with pinned_precision():
        side = iv("2.1")
        squares = enclose_layout(four_square_layout, [iv("0.1")])
        report = verify_interval(squares, side, side_label="2.1")
        assert report.certified, str(report)
        assert report.pairs_tested == 6
        assert report.separated_pairs == 6
        assert report.refusal_reason() is None

        # Compared against the enclosure actually verified against, not against a
        # re-parsed decimal: the span is outward-rounded and may exceed the literal.
        span_x, span_y = corner_span(squares)
        limit = mp.mpf(side.b)
        assert mp.mpf(span_x.b) <= limit and mp.mpf(span_y.b) <= limit


def exact_contacts_are_undecided_not_certified() -> None:
    """The load-bearing negative result of the whole interval route.

    A tight packing's contacts are exact zeros.  No enclosure of positive width
    certifies one, so the honest verdict is `undecided` -- and a verifier that returned
    `separated` here would be accepting overlaps of the same magnitude, which is the
    exact failure the assurance boundary exists to prevent.
    """
    squares = enclose_layout(four_square_layout, [iv("0")])
    report = verify_interval(squares, iv("2"), side_label="2")
    assert not report.certified, (
        "exact contacts were certified, which no enclosure of positive width can do"
    )
    assert not report.overlapping_pairs, "a valid packing was reported as overlapping"
    assert len(report.undecided_pairs) == 6
    assert "undecided" in (report.refusal_reason() or "")


def shrinking_the_container_is_refused() -> None:
    """Spec control: a side below the packing must be refused, not accommodated."""
    squares = enclose_layout(four_square_layout, [iv("0.1")])
    report = verify_interval(squares, iv("1.5"), side_label="1.5")
    assert not report.certified
    assert report.container_failures, "a container smaller than the packing certified"
    reason = report.refusal_reason() or ""
    assert "outside the container" in reason, reason


def widening_until_undecidable_names_the_pair() -> None:
    """Spec control: wider enclosures must refuse by name, never pass silently."""
    squares = enclose_layout(four_square_layout, [iv("0.1")])
    report = verify_interval(widen(squares, "0.06"), iv("2.3"), side_label="2.3")
    assert not report.certified, "widened enclosures still certified"
    assert not report.overlapping_pairs
    assert report.undecided_pairs, "widening produced neither a refusal nor a pass"
    reason = report.refusal_reason() or ""
    first, second = report.undecided_pairs[0]
    assert f"squares {first} and {second}" in reason, reason

    # Widening far enough to actually interpenetrate is a different verdict again, and
    # the two must not be confused: one says "cannot tell", the other says "invalid".
    swamped = verify_interval(widen(squares, "0.6"), iv("4"), side_label="4")
    assert not swamped.certified


def overlap_is_proved_not_guessed() -> None:
    first = corners_from_pose(iv("0.5"), iv("0.5"), iv("0"))
    second = corners_from_pose(iv("0.7"), iv("0.6"), iv("0"))
    assert pair_verdict(first, second) == OVERLAPPING

    apart = corners_from_pose(iv("2.0"), iv("2.0"), iv("0"))
    assert pair_verdict(first, apart) == SEPARATED

    touching = corners_from_pose(iv("1.5"), iv("0.5"), iv("0"))
    assert pair_verdict(first, touching) == UNDECIDED, (
        "an exact contact was decided, which no enclosure of positive width can do"
    )


def rotation_keeps_squares_unit_by_construction() -> None:
    """Why shape checking is off: the edge-length enclosure contains 1 and is not 1."""
    with pinned_precision():
        square = corners_from_pose(iv("1"), iv("1"), iv(mp.pi) / iv(6))
        (ax, ay), (bx, by) = square[0], square[1]
        edge_squared = (bx - ax) ** 2 + (by - ay) ** 2
        low, high = mp.mpf(edge_squared.a), mp.mpf(edge_squared.b)
        assert low <= 1 <= high, "a rotated unit square stopped being unit"
        assert low < high, "an enclosure of a rotated edge came out degenerate"
        try:
            interval_sign(edge_squared - iv("1"))
            raise AssertionError(
                "the edge-length enclosure decided a sign; if that is now possible, "
                "shape checking could be turned back on"
            )
        except IntervalRefusalError as error:
            assert error.kind == "undecided-sign"


def naive_seam_is_measurably_too_strict() -> None:
    """Recorded, not worked around: why the fold is reimplemented.

    `verify_packing` accepts an injected `sign`, and passing the interval one is the
    obvious move.  Measured here, it refuses on a layout with a tenth of a unit of
    clearance on every pair -- so the refusal is not about the packing being tight.
    Two independent causes, both in the fold rather than the geometry: the projection
    step orders enclosures that overlap, and the separation step discards a pair on one
    axis's undecided sign even when another axis separates it strictly.
    """
    squares = enclose_layout(four_square_layout, [iv("0.1")])
    assert verify_interval(squares, iv("2.1")).certified

    try:
        verify_packing(squares, iv("2.1"), sign=interval_sign, check_shapes=False)
    except IntervalRefusalError as error:
        assert error.kind == "undecided-sign"
        return
    raise AssertionError(
        "verify_packing no longer refuses under an interval sign; if the fold has been "
        "made refusal-tolerant, interval_verify's reimplementation can be retired"
    )


def main() -> int:
    with pinned_precision():
        certifies_when_there_is_room()
        exact_contacts_are_undecided_not_certified()
        shrinking_the_container_is_refused()
        widening_until_undecidable_names_the_pair()
        overlap_is_proved_not_guessed()
        rotation_keeps_squares_unit_by_construction()
        naive_seam_is_measurably_too_strict()
    print("interval layout and verification contract selftest passed")
    return 0


def test_promote_interval_verify() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
