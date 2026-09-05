#!/usr/bin/env python3
"""Calibration of the interval route against answers it cannot influence.

Two kinds of check live here, and the second is the one that would catch a wrong
implementation.

**Agreement.**  `n = 5`, `n = 10` and `n = 11` are already `verified` by the exact
route, over certified number fields.  The interval route has to land above each exact
side and approach it as the relaxation falls.  Landing *below* would be a soundness
failure; landing far above would mean the relaxation is not doing what it claims.

**Discrimination.**  Agreeing with the exact route on valid input proves nothing on its
own -- a checker that returned "valid" unconditionally would pass every agreement test
here.  So the same packings are perturbed into infeasibility by amounts far below any
float tolerance, and the checker has to catch them.  Measured: an overlap of `1e-30` is
*proved* by this route and accepted as valid by a float check at `1e-9`.

`n = 29` is separate.  Nothing about it is a known answer, so what is checked there is
internal consistency between two routes that share no code: the pairs the interval
verifier cannot decide have to be exactly the contacts BC-042 extracted.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import mpmath as mp

from cases.gobel5 import packing as gobel5
from cases.gobel10 import exact as gobel10
from cases.kingbird29 import system as kingbird_system
from cases.kingbird29.certify_interval import certify_n29
from cases.kingbird29.layout import DEFAULT_SOURCE, agrees_with_materialised, squares_at
from cases.trump11 import packing as trump11
from sqpack.promote.enclose import enclose_field_squares
from sqpack.promote.interval import Dual, carrier, from_endpoints, interval
from sqpack.promote.interval_verify import verify_interval
from sqpack.promote.krawczyk import PoseBox, certify
from sqpack.promote.refine import refine
from sqpack.promote.relax import (
    RelaxationError,
    bound_falls,
    certified_upper_bound,
    relax,
    relaxation_series,
)
from sqpack.verify import float_sign, verify_packing

PRECISION = 60
ROOT = Path(__file__).resolve().parent.parent
CONTACTS = ROOT / "atlas/known-best/contact-structures.json"
LADDER = ("1e-6", "1e-9", "1e-12", "1e-15")


@contextmanager
def pinned_precision(digits: int = PRECISION):
    saved = mp.iv.dps, mp.mp.dps
    mp.iv.dps = mp.mp.dps = digits
    try:
        yield
    finally:
        mp.iv.dps, mp.mp.dps = saved


def exact_case(build) -> tuple[list, Any]:
    squares, side, field = build()
    boxes, side_box = enclose_field_squares(field, squares, side, digits=45)
    return boxes, mp.mpf(side_box.b)


def agrees_with_the_exact_route() -> None:
    """Above the exact side, and closing on it as the relaxation falls."""
    with pinned_precision():
        for label, build in (
            ("n=5", gobel5.build),
            ("n=10", gobel10.build),
            ("n=11", trump11.build),
        ):
            boxes, exact_side = exact_case(build)
            series = relaxation_series(boxes, LADDER, digits=30)
            assert bound_falls(series), f"{label}: {series}"
            for row in series:
                bound = mp.mpf(row["bound"])
                assert bound > exact_side, (
                    f"{label}: certified {row['bound']} at eps={row['epsilon']}, which is "
                    "not above the exactly verified side; a bound below the optimum is a "
                    "soundness failure, not a tighter result"
                )
            # The relaxation buys a bound of order eps * s, so the tightest rung has to
            # be close: a construction that stalled far above would still pass the two
            # checks above while being useless.
            tightest = mp.mpf(series[-1]["bound"]) - exact_side
            assert tightest < mp.mpf("1e-13"), f"{label}: tightest gap {tightest}"


def discriminates_against_infeasible_poses() -> None:
    """The check that agreement alone cannot make: catching what a float check misses."""
    with pinned_precision():
        boxes, _ = exact_case(gobel5.build)

        def as_floats(squares):
            return [
                [(float(mp.mpf(x.a)), float(mp.mpf(y.a))) for x, y in square]
                for square in squares
            ]

        for overlap in ("1e-12", "1e-20", "1e-30"):
            bad = [list(square) for square in boxes]
            push = interval(overlap)
            bad[1] = [(x - push, y) for x, y in bad[1]]

            report = verify_interval(bad, interval("3.0"), side_label="3.0")
            assert not report.certified, (
                f"an overlap of {overlap} was certified as a valid packing"
            )
            assert report.overlapping_pairs, (
                f"an overlap of {overlap} was left undecided rather than proved"
            )

            # The contrast that says what this route is for. A float check at the usual
            # tolerance calls the same pose valid.
            loose = verify_packing(
                as_floats(bad), 3.0, sign=float_sign(1e-9), check_shapes=False
            )
            assert loose.valid, (
                "the float check no longer accepts this pose, so it no longer "
                "demonstrates the discrimination this route provides"
            )


def relaxation_refuses_what_it_cannot_do() -> None:
    with pinned_precision():
        boxes, _ = exact_case(gobel5.build)
        for bad_epsilon in ("0", "-1e-12"):
            try:
                certified_upper_bound(boxes, epsilon=bad_epsilon, digits=30)
            except RelaxationError as error:
                assert error.kind == "non-positive-relaxation"
            else:
                raise AssertionError(
                    f"eps={bad_epsilon} opened no contact and was accepted anyway"
                )

        # A side below the packing is refused rather than accommodated.
        result = certified_upper_bound(boxes, epsilon="1e-12", digits=30)
        assert result.certified
        below = mp.mpf(result.bound) - mp.mpf("1e-6")
        report = verify_interval(
            relax(boxes, "1e-12"), interval(mp.nstr(below, 32)), side_label="too small"
        )
        assert not report.certified
        assert "outside the container" in (report.refusal_reason() or "")


def trump_root_matches_the_published_polynomial() -> None:
    """The operator against algebra it cannot influence, published in 1979."""
    with pinned_precision(90):

        def published(side):
            accumulator = 0 * side
            for coefficient in trump11.S_MIN_POLY:
                accumulator = accumulator * side + coefficient
            return [accumulator]

        seed = "3.87708359002281417730789706010096270637645566846"
        result = certify(published, PoseBox.around(("s",), (seed,), "1e-20"), digits=45)
        assert result.exists, result.summary()
        assert result.unique, result.summary()

        _squares, side, field = trump11.build()
        assert trump11.side_satisfies_published_polynomial(side, field)
        field.refine_to(50)
        low, high = field.enclose(side)
        as_float = lambda q: mp.mpf(q.numerator) / mp.mpf(q.denominator)  # noqa: E731
        assert mp.mpf(result.box.lo[0]) <= as_float(low), (
            "the certified box does not contain the known algebraic root"
        )
        assert as_float(high) <= mp.mpf(result.box.hi[0])


def kingbird_layout_reproduces_the_numeric_walk() -> None:
    """The symbolic layout is the source's, not a second transcription of it."""
    assert agrees_with_materialised(DEFAULT_SOURCE, digits=40) == 29


def kingbird_undecidables_are_exactly_the_frozen_contacts() -> None:
    """Two routes that share no code agree on which pairs touch.

    The interval verifier cannot decide a pair that touches at exactly zero.  BC-042
    extracted the contact set from the reconstruction by a completely different method.
    The two sets have to be the same one, and there are 52 of them.
    """
    with pinned_precision(80):
        seed = kingbird_system.seed(DEFAULT_SOURCE)
        refinement = refine(kingbird_system.equations, seed, 60, names=kingbird_system.UNKNOWNS)
        root = certify(
            kingbird_system.equations,
            PoseBox.around(kingbird_system.UNKNOWNS, refinement.values, "1e-30"),
            digits=45,
        )
        assert root.unique
        squares = [
            [
                (
                    x.value if isinstance(x, Dual) else interval(x),
                    y.value if isinstance(y, Dual) else interval(y),
                )
                for x, y in square
            ]
            for square in squares_at(DEFAULT_SOURCE, [carrier(v) for v in root.box.intervals()])
        ]
        highest = max(mp.mpf(v.b) for square in squares for pair in square for v in pair)
        report = verify_interval(squares, from_endpoints(highest, highest))
        undecided = {tuple(sorted(pair)) for pair in report.undecided_pairs}

        structure = json.loads(CONTACTS.read_text(encoding="utf-8"))
        entry = next(s for s in structure["structures"] if s["n"] == 29)
        frozen = {
            tuple(sorted((int(c["left"]), int(c["right"])))) for c in entry["pair_contacts"]
        }
        assert len(frozen) == 52, f"the frozen structure now has {len(frozen)} contacts"
        assert undecided == frozen, (
            "the pairs interval arithmetic cannot decide are no longer exactly the "
            "extracted contacts; one of the two routes has moved"
        )


def kingbird_certificate_is_bounded_and_unpromoted() -> None:
    """The `n = 29` chain end to end, with its claim boundary asserted, not assumed."""
    result = certify_n29()
    assert result["certified"], result.get("refusal")
    assert result["squares"] == 29
    assert result["pairs_tested"] == 406
    assert result["separated_pairs"] == 406
    assert result["needs_review"] is True, (
        "an n = 29 certificate that does not carry needs_review could be promoted by a "
        "runner, which no runner may do"
    )
    # Pinned: at the ambient default these three values are one double, and the
    # comparisons below would all hold vacuously.
    with pinned_precision(60):
        bound = mp.mpf(result["bound"])
        assert bound < mp.mpf(result["standing_verified_ceiling"]), (
            "the certificate does not tighten the standing ceiling"
        )
        assert bound > mp.mpf("5.9338334626769291896894606163"), (
            "the certified bound is below the published pose, which a relaxation of a "
            "packing cannot be"
        )


def main() -> int:
    agrees_with_the_exact_route()
    discriminates_against_infeasible_poses()
    relaxation_refuses_what_it_cannot_do()
    trump_root_matches_the_published_polynomial()
    kingbird_layout_reproduces_the_numeric_walk()
    kingbird_undecidables_are_exactly_the_frozen_contacts()
    kingbird_certificate_is_bounded_and_unpromoted()
    print("interval calibration and relaxation contract selftest passed")
    return 0


def test_promote_relax() -> None:
    assert main() == 0


if __name__ == "__main__":
    raise SystemExit(main())
