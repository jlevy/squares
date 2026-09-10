"""Tests for the threshold-certificate net-refinement measurement.

Three properties, on a fixture small enough to sweep in a second:

- the crossing shrink is monotone in the net, because the nets are nested and a finer
  net's least charge is a minimum over a superset of directions;
- the weights rescaled by ``1 / m`` give a record the decide tool reads back with a
  least cell charge of exactly 1, and with every declaration it makes intact;
- the largest grid shrink the sharpened test admits is the exact grid value, decided by
  rational inequalities either side of it.

The fixture is a nine-point square lattice together with its image under a rotation by
eleven sixteenths of the arc, an angle no net here contains. Both ends of the arc are
then well covered and the worst direction is interior and off centre, which is what
makes a finer net strictly harder here, as it is on the real certificate; a rotation by
the arc's own end angle makes the profile symmetric and every net crosses together. One
2-of-3 threshold atom of weight ``1/4`` rides along, so the sweep under test is the
threshold sweep and not the point sweep.
"""

# The decide tool's own declaration checker and exact route are what a rescaled record
# has to satisfy, so they are called here rather than reimplemented; the repository's
# own modules use this suppression for the same reason.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

from devtools.decide_threshold_certificate import _declarations, _exact_route, load
from devtools.dilation_corollary import sharp_dilation_ceiling
from devtools.measure_net_refinement import (
    largest_sharp_side,
    sharp_containment,
    uniform_net,
)
from devtools.measure_threshold_net_refinement import (
    Knowledge,
    at,
    crossing,
    decimal_places,
    dilation_supremum,
    full_sweep,
    rescaled_record,
)
from sqpack.fractional.certificate import Certificate
from sqpack.fractional.model import Atom
from sqpack.fractional.threshold import ThresholdAtom, ThresholdCertificate

LIMIT = Fraction(1, 5)
FIXTURE_N = 30
FIXTURE_THRESHOLD = Fraction(11, 2)
LOWER = Fraction(50, 100)
UPPER = Fraction(56, 100)
RESOLUTION = Fraction(1, 10**5)


def fixture(side: Fraction, steps: int) -> ThresholdCertificate:
    """The lattice, its rotated image, and one 2-of-3 threshold atom."""

    centre = Fraction(1, 2)
    tangent = LIMIT * 11 / 16
    cosine = (1 - tangent * tangent) / (1 + tangent * tangent)
    sine = 2 * tangent / (1 + tangent * tangent)
    coordinates = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4))
    base = [(x, y) for x in coordinates for y in coordinates]
    rotated = [
        (
            centre + cosine * (x - centre) - sine * (y - centre),
            centre + sine * (x - centre) + cosine * (y - centre),
        )
        for x, y in base
    ]
    points = sorted(set(base) | set(rotated))
    return ThresholdCertificate(
        n=FIXTURE_N,
        outer_side=Fraction(1),
        square_side=side,
        atoms=tuple(Atom(f"a{k}", x, y, Fraction(1)) for k, (x, y) in enumerate(points)),
        threshold_atoms=(ThresholdAtom(tuple(base[0:3]), 2, Fraction(1, 4)),),
        half_tangents=uniform_net(LIMIT, steps),
    )


def crossing_shrink(steps: int, work: Path) -> Fraction:
    """The least grid shrink in ``(LOWER, UPPER]`` whose net is charged above threshold."""

    certificate = fixture(LOWER, steps)
    knowledge = Knowledge(FIXTURE_THRESHOLD)
    _, passing, _ = crossing(
        certificate,
        certificate.half_tangents,
        LOWER,
        UPPER,
        steps=steps,
        knowledge=knowledge,
        work=work,
        workers=1,
        resolution=RESOLUTION,
    )
    return passing


def test_crossing_shrink_is_monotone_in_the_net(tmp_path: Path) -> None:
    coarse = crossing_shrink(4, tmp_path)
    middle = crossing_shrink(8, tmp_path)
    fine = crossing_shrink(16, tmp_path)
    assert coarse <= middle
    assert middle <= fine
    assert coarse < fine


def test_the_brackets_really_bracket(tmp_path: Path) -> None:
    """``LOWER`` fails and ``UPPER`` passes at the finest net, so the bisection is valid."""

    knowledge = Knowledge(FIXTURE_THRESHOLD)
    certificate = fixture(LOWER, 16)
    least_low, _, _ = full_sweep(
        certificate,
        certificate.half_tangents,
        LOWER,
        knowledge=knowledge,
        work=tmp_path,
        steps=16,
        workers=1,
    )
    least_high, _, _ = full_sweep(
        certificate,
        certificate.half_tangents,
        UPPER,
        knowledge=knowledge,
        work=tmp_path,
        steps=16,
        workers=1,
    )
    assert least_low <= FIXTURE_THRESHOLD
    assert least_high > FIXTURE_THRESHOLD


def test_rescaled_record_has_least_cell_charge_exactly_one(tmp_path: Path) -> None:
    steps = 8
    side = crossing_shrink(steps, tmp_path)
    certificate = at(fixture(LOWER, steps), uniform_net(LIMIT, steps), side)
    knowledge = Knowledge(FIXTURE_THRESHOLD)
    least, _, _ = full_sweep(
        certificate,
        certificate.half_tangents,
        side,
        knowledge=knowledge,
        work=tmp_path,
        steps=steps,
        workers=1,
    )
    assert least > FIXTURE_THRESHOLD

    record = {
        "id": "fixture",
        "variant": "threshold",
        "n": FIXTURE_N,
        "claim": "s(30) >= 1",
        "outer_side": "1",
        "square_side": str(LOWER),
        "angle_limit": str(LIMIT),
        "direction_steps": 1,
        "symmetry": "D4",
        "total_budget": "0",
        "least_cell_charge": "0",
        "atoms": [[str(a.x), str(a.y), str(a.weight)] for a in certificate.atoms],
        "threshold_atoms": [t.to_record() for t in certificate.threshold_atoms],
        "provenance": {"tool": "fixture"},
    }
    rescaled = rescaled_record(record, steps, side, 1 / least)
    path = tmp_path / "rescaled.json"
    path.write_text(json.dumps(rescaled, indent=1) + "\n", encoding="utf-8")

    loaded, read_back = load(path.read_bytes())
    problems, declared = _declarations(loaded, read_back)
    assert problems == []
    assert declared == Fraction(1)
    assert loaded.square_side == side
    assert len(loaded.half_tangents) == steps + 1
    assert loaded.total_budget == certificate.total_budget / least

    exact_least, exact_problems = _exact_route(loaded, workers=1)
    assert exact_problems == []
    assert exact_least == Fraction(1)


def test_largest_sharp_side_is_exact() -> None:
    """``B^2 (1 + D)^2 < 1 + D^2`` at ``D = 1/2`` puts the grid value at 7453559/10^7."""

    gap = Fraction(1, 2)
    side = largest_sharp_side(gap)
    assert side == Fraction(7_453_559, 10**7)
    assert (side * (1 + gap)) ** 2 < 1 + gap * gap
    assert side.denominator <= 10**7
    higher = Fraction(side.numerator * (10**7 // side.denominator) + 1, 10**7)
    assert (higher * (1 + gap)) ** 2 >= 1 + gap * gap
    assert sharp_containment(side, gap)
    assert not sharp_containment(higher, gap)
    # The exact statement behind the grid value: 9 B^2 < 5 with B = 7453559/10^7.
    assert 9 * 7_453_559**2 < 5 * 10**14
    assert 9 * 7_453_560**2 > 5 * 10**14


def test_dilation_supremum_agrees_with_the_repository_form() -> None:
    """``dilation_supremum`` is `sharp_dilation_ceiling` scaled by ``L``."""

    side = Fraction(9977, 10000)
    outer = Fraction(191, 50)
    half_tangents = uniform_net(Fraction(207107, 500000), 180)
    point = Certificate(
        n=11,
        outer_side=outer,
        square_side=side,
        atoms=(Atom("a", Fraction(1, 2), Fraction(1, 2), Fraction(1)),),
        half_tangents=half_tangents,
    )
    gap = point.largest_half_gap_tangent
    mine = dilation_supremum(outer, side, gap)
    theirs = sharp_dilation_ceiling(point).scaled(outer)
    assert mine.squared == theirs.squared
    assert mine.exact == theirs.exact
    assert decimal_places(mine.squared, 20).startswith("3.82")


def test_decimal_places_truncates_a_known_root() -> None:
    assert decimal_places(Fraction(2), 20) == "1.41421356237309504880"
    assert decimal_places(Fraction(4), 5) == "2.00000"
