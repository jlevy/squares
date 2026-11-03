"""The axis vertex sweep's enclosure at one vertex, recomputed by `devtools.sqverify_fast_axis`.

The census control judges an axis refusal against the enclosure `[l', u']` this module
recomputes, tied to the crate by `l'` equal to the crate's certified bound to the bit
(F-1 of the 14 October review). These tests hold the two facts that rule rests on: the
directed steps reach the adjacent binary64 values, as lemma I1 needs, and the walk is
the crate's on a retained certificate, for the original and for the 99/100 mutant.
"""

from __future__ import annotations

import gzip
import json
import math
import random
from fractions import Fraction

from devtools import sqverify_fast_axis as axis
from devtools import sqverify_fast_census as census
from devtools.check_sqverify_fast import mixed_exact, read_raw

#: The retained fine-net certificate with its candidate, census receipts and control.
NAME = "mixed_n37_L64975"
PACKET = "wand125-fine-net-n37-n39-n44-2026-10-13"
CANDIDATE = census.WEB / PACKET / "release/certificates" / NAME / "candidate.json.gz"
RECEIPTS = census.CENSUS_ROOT / "census-mixed" / PACKET
#: The 14 October review's own emulation of the sweep at the mutant's least vertex.
REVIEW = census.WEB / PACKET / "review/outputs/sweep_emulation-n37-scaled-99-100.json"


def test_the_directed_steps_reach_the_adjacent_values() -> None:
    """Lemma I1, as `interval.rs`'s own test states it: `dn` and `up` move a value past
    its neighbours, and by no more than three of them."""
    rng = random.Random(20261103)
    values = [0.0, -0.0, 1.0, -1.0, 0.1, -0.3, 5e-324, 1e-310, 4096.0, 0.9999999999999999]
    values += [rng.uniform(-200.0, 200.0) for _ in range(10_000)]
    for x in values:
        assert axis.up(x) >= math.nextafter(x, math.inf), x
        assert axis.dn(x) <= math.nextafter(x, -math.inf), x
        third = math.nextafter(math.nextafter(math.nextafter(x, math.inf), math.inf), math.inf)
        assert axis.up(x) <= third, x


def test_a_rational_is_enclosed_by_its_two_neighbours() -> None:
    """Lemma I2: the tight enclosure of an exact rational, a point where it is binary64."""
    assert axis.enclose(Fraction(1, 2)) == (0.5, 0.5)
    for q in (Fraction(1, 3), Fraction(-2, 7), Fraction(533, 80), Fraction(10**20 + 1, 10**20)):
        low, high = axis.enclose(q)
        assert Fraction(low) < q < Fraction(high)
        assert high == math.nextafter(low, math.inf)


def test_the_walk_is_the_crates_at_the_least_axis_vertex() -> None:
    """At the census row's axis vertex for the original and the control's for the 99/100
    mutant, the recomputed enclosure's lower end is the crate's certified bound to the bit,
    and it holds the exact capture evaluated apart from the crate. The mutant's is the
    14 October review's emulation to the bit."""
    raw = read_raw(CANDIDATE)
    upper = census.domain_bounds(raw, 0)[1]
    rows = [
        json.loads(line)
        for line in gzip.decompress((RECEIPTS / f"{NAME}.jsonl.gz").read_bytes()).splitlines()
        if line
    ]
    original = next(row for row in rows if row.get("r") == 0)
    control = json.loads((RECEIPTS / f"{NAME}.control.json").read_text(encoding="utf-8"))
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
        assert Fraction(low) <= factor * mixed_exact(raw, x, y, 0) <= Fraction(high)
    review = json.loads(REVIEW.read_text(encoding="utf-8"))
    x, y = (Fraction(value) for value in mutant["pose"])
    enclosure = axis.column_enclosure(raw, census.CONTROL_SCALE, x, y, upper)
    assert list(enclosure or ()) == review["enclosure_at_vertex"]


def test_no_enclosure_where_the_sweep_would_not_run() -> None:
    """Off the ordinate events, or for a measure with a point mass, there is no enclosure
    to recompute, and the census fails the refusal closed."""
    raw = read_raw(CANDIDATE)
    upper = census.domain_bounds(raw, 0)[1]
    side = Fraction(raw["L"])
    assert (
        axis.column_enclosure(raw, Fraction(1), side / 2, side / 2 + Fraction(1, 10**30), upper)
        is None
    )
    linear = {
        "schema": "point_line_rectangle_v1",
        "L": raw["L"],
        "B": raw["B"],
        "primitives": [{"kind": "point", "geometry": ["1", "1"], "mass": "1"}],
    }
    assert axis.column_enclosure(linear, Fraction(1), side / 2, side / 2, upper) is None
