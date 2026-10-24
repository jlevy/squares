"""Couzo's 8 October decimal reports at six counts, decided exactly (think-rx26).

`devtools.couzo_decimal_decisions` reads the retained decimal facts and the 9 October
certificates and decides four readings at each count. These tests hold the receipt to a
fresh decision and pin what it found at 335, the count whose row f1ceee4 supersedes.
"""

from __future__ import annotations

import json
from fractions import Fraction

from devtools import couzo_decimal_decisions as decisions


def _receipt() -> dict:
    return json.loads(decisions.RECEIPT.read_text(encoding="utf-8"))


def test_the_receipt_is_a_fresh_decision() -> None:
    assert decisions.check() == []


def test_335_packs_at_its_print_only_with_the_near_axis_angles_read_as_zero() -> None:
    """Read literally, a wall fails by 7.77e-16 at square 2, whose angle is -1.55e-15
    radians; with the 196 angles below 1e-10 read as 0, the angles the 9 October
    certificate sets to 0, the poses pack exactly at 18.822875655543559."""
    (row,) = [row for row in _receipt()["rows"] if row["n"] == 335]
    assert row["printed_side"] == "18.822875655543559"
    literal = row["literal"]
    assert (literal["verdict"], literal["walls_outside"], literal["pairs_overlapping"]) == (
        "not-a-packing",
        21,
        0,
    )
    assert literal["least_wall_square"] == 2
    low, high = (Fraction(value) for value in literal["least_wall_clearance"])
    assert Fraction(-778, 10**18) < low <= high < Fraction(-777, 10**18)
    assert len(row["near_axis_squares"]) == 196
    assert row["near_axis_read_as_zero"]["verdict"] == "packing"
    assert row["certificate_rotations"]["verdict"] == "packing"
    assert row["certificate_rotations"]["zero_rotations"] == 284
    assert row["certificate"]["verdict"] == "packing"


def test_the_other_five_certificates_are_other_packings() -> None:
    """At 336, 337, 341, 373 and 374 the 9 October certificate is another packing, below
    the print, so its rotations are not read against the decimal poses."""
    rows = {row["n"]: row for row in _receipt()["rows"]}
    assert sorted(rows) == list(decisions.COUNTS)
    verdicts = {
        n: (row["near_axis_read_as_zero"]["verdict"], row["certificate_rotations"]["verdict"])
        for n, row in rows.items()
        if n != 335
    }
    assert verdicts == {
        336: ("not-a-packing", "not-applicable"),
        337: ("not-a-packing", "not-applicable"),
        341: ("packing", "not-applicable"),
        373: ("packing", "not-applicable"),
        374: ("packing", "not-applicable"),
    }
    assert all(row["literal"]["verdict"] == "not-a-packing" for row in rows.values())
    assert all(row["certificate"]["verdict"] == "packing" for row in rows.values())
