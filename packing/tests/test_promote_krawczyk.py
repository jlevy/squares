#!/usr/bin/env python3
"""Behaviour and refusal contract for interval arithmetic and the Krawczyk operator.

The certificates this route emits are only worth the refusals underneath them, so the
refusals are what this file spends its length on.

Three things are checked that a passing certificate alone would not show:

- **the sign refuses.**  An enclosure straddling zero is undecided, and saying so is
  the whole reason an interval separating-axis test can be trusted at a tight packing.
- **the serialized box still encloses the root.**  Writing a certificate down is
  arithmetic too.  Rounding the endpoints to nearest is the natural thing to do and it
  is wrong: measured here, it lifts `sqrt(2)`'s lower endpoint above the root.
- **an independent implementation agrees.**  `sqpack.field` isolates the same root by
  Sturm sequences over exact rationals, sharing no code with this route, so it can
  catch the operator being confidently wrong rather than merely self-consistent.
"""

from __future__ import annotations

from fractions import Fraction

import mpmath as mp
import sympy as sp

from sqpack.field import NumberField
from sqpack.promote.interval import (
    IntervalRefusalError,
    cos,
    cos_degrees,
    decimal_string,
    evaluate,
    interval,
    interval_sign,
    sin,
    sin_degrees,
)
from sqpack.promote.krawczyk import PoseBox, certify

# sqrt(2) to more digits than any check here needs, so a seed is never the thing that
# limits precision.
SQRT2 = "1.4142135623730950488016887242096980785696718753769480731766797379907324785"


def require_refusal(call, kind: str, label: str) -> None:
    try:
        call()
    except IntervalRefusalError as error:
        assert error.kind == kind, f"{label}: expected {kind}, got {error.kind}"
        return
    raise AssertionError(f"{label}: expected a {kind} refusal and got a value")


def sign_contract() -> None:
    """A sign that decides only what an enclosure can decide."""
    assert interval_sign(interval("1")) == 1
    assert interval_sign(interval("-1")) == -1
    # The one case where zero is proved rather than merely possible.
    assert interval_sign(interval("0")) == 0

    require_refusal(
        lambda: interval_sign(interval("-1", "1")), "undecided-sign", "straddling zero"
    )
    # Touching an endpoint is still straddling: the value may be zero or may not, and
    # the difference is exactly what a contact-versus-overlap decision turns on.
    require_refusal(
        lambda: interval_sign(interval("0", "1")), "undecided-sign", "zero at the floor"
    )
    require_refusal(
        lambda: interval_sign(interval("-1", "0")), "undecided-sign", "zero at the roof"
    )


def derivatives_match_analysis() -> None:
    """Forward-mode AD over intervals, against derivatives worked out by hand."""
    previous = mp.iv.dps, mp.mp.dps
    mp.iv.dps = mp.mp.dps = 40
    try:

        def system(x, y):
            return [x**2 * y + sin(x), x / y]

        values, jacobian = evaluate(system, [interval("0.3"), interval("2")])
        expected = (
            2 * mp.mpf("0.3") * 2 + mp.cos(mp.mpf("0.3")),
            mp.mpf("0.3") ** 2,
            1 / mp.mpf(2),
            -mp.mpf("0.3") / 4,
        )
        cells = (jacobian[0][0], jacobian[0][1], jacobian[1][0], jacobian[1][1])
        for cell, want in zip(cells, expected, strict=True):
            lo, hi = mp.mpf(cell.a), mp.mpf(cell.b)
            assert lo <= want <= hi, f"{want} outside [{lo}, {hi}]"

        assert mp.mpf(values[1].a) <= mp.mpf("0.15") <= mp.mpf(values[1].b)

        # Over a *box*, the Jacobian must enclose every pointwise value inside it.
        _, wide = evaluate(system, [interval("0.2", "0.4"), interval("1.9", "2.1")])
        lo, hi = mp.mpf(wide[0][0].a), mp.mpf(wide[0][0].b)
        assert lo <= expected[0] <= hi
        assert hi - lo > 0, "a box Jacobian that is a point has not enclosed anything"

        # cos is lifted the same way, and a division by a straddling enclosure has no
        # finite result to return.
        assert interval_sign(cos(interval("0.3")) - interval("0.9")) == 1
        require_refusal(
            lambda: evaluate(lambda a: [a / (a - interval("0.3"))], [interval("0.2", "0.4")]),
            "division-by-straddling-zero",
            "divisor containing zero",
        )
    finally:
        mp.iv.dps, mp.mp.dps = previous


def outward_serialization() -> None:
    """Writing a certificate down must not round it off the root.

    This is the measurement that made the check exist: at 40 significant digits,
    nearest rounding puts both endpoints of `sqrt(2)` above `sqrt(2)`.
    """
    previous = mp.mp.dps
    mp.mp.dps = 80
    try:
        root = mp.sqrt(2)
        nearest = mp.mpf(str(mp.nstr(root, 40, strip_zeros=False)))
        assert nearest > root, "the trap this guards against has moved; recheck the fix"

        low = mp.mpf(decimal_string(root, 40, upward=False))
        high = mp.mpf(decimal_string(root, 40, upward=True))
        assert low <= root <= high, (
            "the serialized endpoints no longer enclose the root they were rounded from"
        )
        assert low < high, "outward rounding collapsed to a point"

        # Negative values round outward on the correct side too, which sign-symmetric
        # code gets wrong in exactly one direction.
        low = mp.mpf(decimal_string(-root, 30, upward=False))
        high = mp.mpf(decimal_string(-root, 30, upward=True))
        assert low <= -root <= high, (
            "the serialized endpoints no longer enclose the root they were rounded from"
        )
    finally:
        mp.mp.dps = previous


def univariate_against_an_independent_isolator() -> None:
    """The operator's box and `sqpack.field`'s Sturm isolation enclose one root."""

    def squared_minus_two(x):
        return [x * x - 2]

    previous = mp.mp.dps
    mp.mp.dps = 90
    try:
        result = certify(
            squared_minus_two,
            PoseBox.around(("x",), (SQRT2,), "1e-20"),
            digits=40,
        )
        assert result.exists, result.summary()
        assert result.unique, result.summary()
        assert result.operator == "krawczyk"

        low, high = mp.mpf(result.box.lo[0]), mp.mpf(result.box.hi[0])
        assert low <= mp.sqrt(2) <= high, "the certified box does not contain the root"

        field = NumberField([1, 0, -2], (Fraction(1), Fraction(2)))
        field.refine_to(45)
        field_low, field_high = field.root_bounds()
        as_float = lambda q: mp.mpf(q.numerator) / mp.mpf(q.denominator)  # noqa: E731
        not_enclosing = (
            "the exact isolating interval is not inside the certified box, so the two "
            "implementations are not enclosing the same root"
        )
        assert low <= as_float(field_low), not_enclosing
        assert as_float(field_high) <= high, not_enclosing
    finally:
        mp.mp.dps = previous


def two_dimensional_known_answer() -> None:
    """A 2x2 system whose root is `(1/sqrt(2), 1/sqrt(2))` by inspection."""

    def circle_and_diagonal(x, y):
        return [x * x + y * y - 1, x - y]

    previous = mp.mp.dps
    mp.mp.dps = 60
    try:
        centre = str(mp.nstr(1 / mp.sqrt(2), 40, strip_zeros=False))
        result = certify(
            circle_and_diagonal,
            PoseBox.around(("x", "y"), (centre, centre), "1e-15"),
            digits=30,
        )
        unreported = f"a verdict proved during iteration was not reported: {result.summary()}"
        assert result.exists, unreported
        assert result.unique, unreported
        for low, high in zip(result.box.lo, result.box.hi, strict=True):
            assert mp.mpf(low) <= 1 / mp.sqrt(2) <= mp.mpf(high)
    finally:
        mp.mp.dps = previous


def no_root_control() -> None:
    """A box with no root in it must not report existence."""

    def squared_minus_two(x):
        return [x * x - 2]

    result = certify(squared_minus_two, PoseBox.around(("x",), ("5.0",), "0.1"), digits=30)
    assert not result.exists, "existence claimed in a box holding no root"
    assert not result.unique


def two_root_control() -> None:
    """A box with two roots must never report uniqueness.

    `unique` is the field everything downstream reads, and this is the control that
    keeps it honest.  Recorded rather than asserted: across the three boxes below the
    operator returns *no verdict at all* rather than `exists` without `unique`.  That
    is the expected behaviour and worth writing down, because `exists and not unique`
    needs `K(X)` to land inside `X` while touching its boundary, and a contraction that
    lands on a boundary exactly is not something floating point produces.  The claim
    under test is the safety one -- never `unique` -- not which of the two failing
    shapes comes back.
    """

    def two_roots(x):
        return [(x - 1) * (x - 2)]

    for centre, radius in (("1.5", "0.9"), ("1.65", "0.95"), ("1.4", "0.7")):
        result = certify(two_roots, PoseBox.around(("x",), (centre,), radius), digits=30)
        assert not result.unique, (
            f"uniqueness claimed for a box around {centre} of radius {radius}, which "
            "contains both x = 1 and x = 2"
        )


def box_radius_is_reported_outward() -> None:
    """A reported radius may overstate the box and may never understate it."""
    previous = mp.mp.dps
    mp.mp.dps = 50
    try:
        box = PoseBox.around(("x",), (SQRT2,), "1e-12")
        assert box.max_half_width() >= mp.mpf("1e-12")
    finally:
        mp.mp.dps = previous


def one_transcription_serves_three_arithmetics() -> None:
    """`sin_degrees` and `cos_degrees` dispatch, so the `n = 29` system is written once.

    Three routes read it: ordinary floats check the publication against itself, intervals
    build a certificate, and SymPy expressions feed an elimination.  A second copy of a
    six-equation contact system would be a second thing to keep correct, and the first
    divergence between them would be silent -- so the branch that was missing is the one
    asserted here.

    The symbolic branch is a *branch*, not a fall-through: `mp.radians` raises on a SymPy
    symbol, which is how the symbolic route was unavailable without anything reporting it.
    """
    angle = 37
    numeric = mp.sin(mp.radians(angle))

    saved = mp.iv.dps
    mp.iv.dps = 40
    try:
        enclosure = sin_degrees(interval(angle))
        assert mp.mpf(enclosure.a) <= numeric <= mp.mpf(enclosure.b), (
            "the interval branch does not enclose the float branch's value"
        )
    finally:
        mp.iv.dps = saved

    symbol = sp.Symbol("theta", real=True)
    symbolic = sin_degrees(symbol)
    assert symbolic.has(sp.sin), f"the symbolic branch returned {symbolic!r}, not a sine"
    assert abs(float(symbolic.subs(symbol, angle).evalf()) - float(numeric)) < 1e-12, (
        "the symbolic branch disagrees with the float branch at 37 degrees, so the three "
        "routes are not reading the same transcription"
    )
    cosine = cos_degrees(symbol)
    assert cosine.has(sp.cos)
    assert (
        abs(float(cosine.subs(symbol, angle).evalf()) - float(mp.cos(mp.radians(angle))))
        < 1e-12
    )


def main() -> int:
    sign_contract()
    one_transcription_serves_three_arithmetics()
    derivatives_match_analysis()
    outward_serialization()
    univariate_against_an_independent_isolator()
    two_dimensional_known_answer()
    no_root_control()
    two_root_control()
    box_radius_is_reported_outward()
    print("interval arithmetic and Krawczyk contract selftest passed")
    return 0


def test_promote_krawczyk() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
