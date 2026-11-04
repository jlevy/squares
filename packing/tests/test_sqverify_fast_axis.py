"""The axis vertex sweep's enclosure at one vertex, recomputed by `devtools.sqverify_fast_axis`.

The census control judges an axis refusal against the enclosure `[l', u']` this module
recomputes, tied to the crate by `l'` equal to the crate's certified bound to the bit
(F-1 of the 14 October review). These tests hold what that rule rests on: the directed
steps reach the adjacent binary64 values across the whole range, as lemma I1 needs; the
walk's lower end is the crate's on two retained certificates, s(37)'s and s(94)'s, for
the original and for the 99/100 mutant; and its upper end, which no lower end witnesses,
is the one a build of the crate instrumented to report it gave (review A of #892), there
and on a measure whose images coincide.
"""

from __future__ import annotations

import gzip
import json
import math
import random
import struct
from fractions import Fraction

import pytest

from devtools import sqverify_fast_axis as axis
from devtools import sqverify_fast_census as census
from devtools.check_sqverify_fast import COINCIDENT_AXIS, mixed_exact, read_raw

#: The retained fine-net certificate with its candidate, census receipts and control.
NAME = "mixed_n37_L64975"
PACKET = "wand125-fine-net-n37-n39-n44-2026-10-13"
CANDIDATE = census.WEB / PACKET / "release/certificates" / NAME / "candidate.json.gz"
RECEIPTS = census.CENSUS_ROOT / "census-mixed" / PACKET
#: T-262's dilated certificate (#890), whose 600-direction control passed under this rule.
N94 = "mixed_n94_L9965"
#: The 14 October review's own emulation of the sweep at the mutant's least vertex.
REVIEW = census.WEB / PACKET / "review/outputs/sweep_emulation-n37-scaled-99-100.json"
#: The upper ends `value.hi` at the axis sweep's least vertex that a build of the reviewed
#: crate source `d97758bb` instrumented to report them gave, with lower ends and argmins
#: equal to the reviewed build's: mixed_n37_L64975's and mixed_n94_L9965's originals and
#: 99/100 mutants (review A of #892, and again in its lane on 3 November; both again in
#: intake lane L37 on 4 November), and `COINCIDENT_AXIS`'s.
CRATE_UPPER = {
    (NAME, Fraction(1)): 1.002369279185975,
    (NAME, Fraction(99, 100)): 0.9923455863941246,
    (N94, Fraction(1)): 1.0031171867987096,
    (N94, Fraction(99, 100)): 0.9930860149308234,
    ("coincident", Fraction(1)): 0.2625000000000111,
    ("coincident", Fraction(99, 100)): 0.25987500000001146,
}
#: The axis sweep's bound and least vertex on `COINCIDENT_AXIS`, from the reviewed build.
COINCIDENT_ROWS = {
    Fraction(1): (0.26249999999998913, ("27/20", "2")),
    Fraction(99, 100): (0.25987499999998875, ("27/20", "2")),
}


def neighbours(x: float, direction: float, count: int) -> float:
    for _ in range(count):
        x = math.nextafter(x, direction)
    return x


def binary64_samples() -> list[float]:
    """Every power of two with its neighbours, both signs; zero, the subnormals and the
    boundary of the normal range; the normal values below 2^-970, where `|x| 2^-52` is
    itself subnormal; values near the top of the range; and finite random bit patterns,
    as `interval.rs`'s own test draws them."""
    tiny, smallest_normal, largest = 5e-324, 2.2250738585072014e-308, 1.7976931348623157e308
    values = [0.0, 1e300, 0.1, 0.9999999999999999, tiny, 1e-310, 2.0**-970, 2.0**-1000]
    values += [smallest_normal, math.nextafter(smallest_normal, 0.0), largest]
    values += [math.ldexp(1.0, k) for k in range(-1074, 1024)]
    values += [neighbours(v, d, 1) for v in list(values) for d in (0.0, math.inf)]
    rng = random.Random(20261104)
    for _ in range(100_000):
        x = struct.unpack("<d", struct.pack("<Q", rng.getrandbits(64)))[0]
        if math.isfinite(x):
            values.append(x)
    return [v for x in values if math.isfinite(x) for v in (x, -x)]


def test_the_directed_steps_reach_the_adjacent_values() -> None:
    """Lemma I1, as `interval.rs`'s own test states it, across binary64: `dn` and `up`
    move a value past its neighbour, and by no more than three of them. At the top of
    the range `up` overflows to infinity, which fails the walk's finiteness check."""
    for x in binary64_samples():
        assert axis.up(x) >= math.nextafter(x, math.inf), x.hex()
        assert axis.dn(x) <= math.nextafter(x, -math.inf), x.hex()
        assert axis.up(x) <= neighbours(x, math.inf, 3), x.hex()
        assert axis.dn(x) >= neighbours(x, -math.inf, 3), x.hex()


def test_a_rational_is_enclosed_by_its_two_neighbours() -> None:
    """Lemma I2: the tight enclosure of an exact rational, a point where it is binary64."""
    assert axis.enclose(Fraction(1, 2)) == (0.5, 0.5)
    for q in (Fraction(1, 3), Fraction(-2, 7), Fraction(533, 80), Fraction(10**20 + 1, 10**20)):
        low, high = axis.enclose(q)
        assert Fraction(low) < q < Fraction(high)
        assert high == math.nextafter(low, math.inf)


@pytest.mark.parametrize("name", [NAME, N94])
def test_the_walk_is_the_crates_at_the_least_axis_vertex(name: str) -> None:
    """At the census row's axis vertex for the original and the control's for the 99/100
    mutant, the recomputed enclosure's lower end is the crate's certified bound to the bit
    and its upper end the instrumented crate's, and it holds the exact capture evaluated
    apart from the crate: at s(37) and at s(94), whose control receipt is the one the
    enclosure rule passed. s(37)'s mutant is the 14 October review's emulation to the bit."""
    case = {case.certificate: case for case in census.mixed_cases()}[name]
    receipts = census.CENSUS_ROOT / "census-mixed" / case.packet
    raw = read_raw(case.candidate)
    upper = census.domain_bounds(raw, 0)[1]
    rows = [
        json.loads(line)
        for line in gzip.decompress((receipts / f"{name}.jsonl.gz").read_bytes()).splitlines()
        if line
    ]
    original = next(row for row in rows if row.get("r") == 0)
    control = json.loads((receipts / f"{name}.control.json").read_text(encoding="utf-8"))
    sweep = next(run["sweep"] for run in control["runs"] if "sweep" in run)
    mutant = next(item for item in sweep["refused"] if item["r"] == 0)
    for factor, pose, bound in (
        (Fraction(1), original["argmin"], original["min_certified_lower_bound"]),
        (census.CONTROL_SCALE, mutant["pose"], mutant["crate_lower_bound"]),
    ):
        x, y = (Fraction(value) for value in pose)
        enclosure = axis.column_enclosure(raw, factor, x, y, upper)
        assert enclosure is not None
        low, high = enclosure
        assert low == bound
        assert high == CRATE_UPPER[name, factor]
        assert Fraction(low) <= factor * mixed_exact(raw, x, y, 0) <= Fraction(high)
    if name != NAME:
        return
    assert case.candidate == CANDIDATE
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    x, y = (Fraction(value) for value in mutant["pose"])
    enclosure = axis.column_enclosure(raw, census.CONTROL_SCALE, x, y, upper)
    assert list(enclosure or ()) == review["enclosure_at_vertex"]


@pytest.mark.parametrize("factor", sorted(COINCIDENT_ROWS))
def test_coincident_images_are_merged_as_admission_merges_them(factor: Fraction) -> None:
    """`COINCIDENT_AXIS` puts images on one another: a row symmetric in the diagonal, a
    centred square, two rows of one orbit in another order, and a row of zero mass.
    They merge by exact key in first-seen order with their densities summed and the mass
    kept, and the walk at the crate's least vertex gives the crate's bound and the
    instrumented crate's upper end, with the exact capture inside.
    `devtools.check_sqverify_fast` holds the lower end to a live build in the gate."""
    raw = COINCIDENT_AXIS
    merged = axis.images(raw, factor)
    keys = [key for key, _density in merged]
    assert (
        len(keys) == len(set(keys)) < 8 * sum(row["mass"] != "0" for row in raw["rectangles"])
    )
    side = Fraction(raw["L"])
    centred = (Fraction(1), Fraction(1), Fraction(3, 2), Fraction(3, 2))
    assert dict(merged)[centred] == factor * Fraction(1, 2) / Fraction(1, 4)
    mass = sum(((x2 - x1) * (y2 - y1) * d for (x1, y1, x2, y2), d in merged), Fraction(0))
    assert mass == factor * Fraction(raw["total_mass"])
    bound, pose = COINCIDENT_ROWS[factor]
    x, y = (Fraction(value) for value in pose)
    enclosure = axis.column_enclosure(raw, factor, x, y, side - Fraction(1, 2))
    high = CRATE_UPPER["coincident", factor]
    assert enclosure == (bound, high)
    assert Fraction(bound) <= factor * mixed_exact(raw, x, y, 0) <= Fraction(high)


def test_no_enclosure_where_the_sweep_would_not_run() -> None:
    """Off the abscissa or the ordinate events, or for a measure with a point mass, there
    is no enclosure to recompute, and the census fails the refusal closed."""
    raw = read_raw(CANDIDATE)
    upper = census.domain_bounds(raw, 0)[1]
    side = Fraction(raw["L"])
    tiny = Fraction(1, 10**30)
    assert axis.column_enclosure(raw, Fraction(1), side / 2, side / 2, upper) is not None
    assert axis.column_enclosure(raw, Fraction(1), side / 2, side / 2 + tiny, upper) is None
    assert axis.column_enclosure(raw, Fraction(1), side / 2 + tiny, side / 2, upper) is None
    linear = {
        "schema": "point_line_rectangle_v1",
        "L": raw["L"],
        "B": raw["B"],
        "primitives": [{"kind": "point", "geometry": ["1", "1"], "mass": "1"}],
    }
    assert axis.column_enclosure(linear, Fraction(1), side / 2, side / 2, upper) is None
