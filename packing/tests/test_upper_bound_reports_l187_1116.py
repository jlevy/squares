"""The upper-bound import of the intake pass's lane L187 of 16 November 2026 (think-0y9m).

One packet, read by the ``witness-corners`` adapter: JoeGun's five corner Witness/v2
certificates of #1001, at 127, 204, 232, 264 and 305, which the issue says are Tomáš
Kodaj's public Kaggle packings improved further, their exact coordinates made by this
repository's ``packing-witness promote``. Each side is a rational the issue prints rounded
up at 12 places. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it: the digests the issue
lists, each print against its exact side, the house each is compared with and the gain,
the ledger's verdicts, the retained sharp controls, the identity measurements, the
contraction margins and the L-step scan the register's notes cite. The source's later
revision adds a numerical local-minimum check, which the ``joegun-local-minimum-2026-11-16``
packet retains; one test holds it against the regularization driver's solves of the same
five witnesses. Every test reads the packets, the ledger and the driver's retained reports
only; none needs the network.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from decimal import ROUND_CEILING, Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import regularize_evand as evand
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-1001-20261116"
NAME = "joegun-upper-bounds-2026-11-16"
ISSUE = 1001
COUNTS = (127, 204, 232, 264, 305)
#: The side #1001 prints at each count, its exact side rounded up at 12 places.
PRINTED = {
    127: "11.801753890487",
    204: "14.802646843107",
    232: "15.759531627557",
    264: "16.773807598002",
    305: "17.945762359659",
}
#: The SHA-256 of each certificate as #1001 and the source's README list it.
LISTED = {
    127: "9bde48b76afce9ab7d20d6d180650d0a6bbe46b7f106573f8155dfe9ed9d06f0",
    204: "1daa0e09b5b403e4e47048104c760f3d8a9b6997d77d26a30930bf1e257ea90c",
    232: "93d856c25c9f75842ca5e36552ccb726e87884440689c9ce4100d2a58d5a279d",
    264: "14fef8f163b2cdb9062f714cdd41d81dce2447691a2de55e3797810cdcd676ee",
    305: "14d2e37e22218defb238e0b0e657f139bab0c2873cc3d05f781b0f3b13a75494",
}
#: Each count's house when the lane read main 31ddae6fe: its reader, its result and the
#: gain the certificate makes on it, at four significant figures.
HOUSES = {
    127: ("[PingYou PR 574 certificates 2026-10-13]", "T-174", "9.1249e-03"),
    204: ("[Daniel issue 914 2026-11-05]", "T-268", "1.7145e-03"),
    232: ("[Özden s232 upper bound 2026-11-09]", "T-275", "1.8780e-03"),
    264: ("[Mishapolk KKT refinements 2026-10-14]", "T-186", "9.2753e-04"),
    305: ("[PingYou PR 574 certificates 2026-10-13]", "T-174", "4.7041e-03"),
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _sides() -> dict[int, Fraction]:
    facts = reports.read_facts(reports.packet_path(NAME))
    return {n: facts[n].side for n in COUNTS}


def test_the_packet_holds_the_files_whose_digests_the_issue_lists() -> None:
    text = (reports.packet_path(NAME) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    manifest = {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }
    for n, digest in LISTED.items():
        assert manifest[f"n-{n}-candidate.yaml"] == digest
    assert len(manifest) == 17
    assert {path for path in manifest if path.endswith("-decimal-pose.yaml")} == {
        f"n-{n}-decimal-pose.yaml" for n in COUNTS
    }


def test_each_print_is_its_exact_side_rounded_up() -> None:
    declaration = reports.load_declaration(reports.packet_path(NAME))
    assert declaration["source_key"] == "[JoeGun upper bounds 2026-11-16]"
    assert declaration["issue"].endswith(f"/issues/{ISSUE}")
    assert declaration["requested"] == declaration["replayed"] == list(COUNTS)
    rows = {row["n"]: row for row in declaration["certificates"]}
    assert set(rows) == set(COUNTS)
    sides = _sides()
    for n in COUNTS:
        assert (rows[n]["format"], rows[n]["offered"]) == ("witness-corners", PRINTED[n])
        side = sides[n]
        exact = Decimal(side.numerator) / Decimal(side.denominator)
        assert exact != Decimal(PRINTED[n])
        rounded = exact.quantize(Decimal("1e-12"), rounding=ROUND_CEILING)
        assert str(rounded) == PRINTED[n]
    # The 232 side terminates at 15 places; the others are rationals of 300 to 430 digits.
    assert sides[232] == Fraction(15759531627556573, 10**15)


def test_each_certificate_is_below_its_house_by_the_gain() -> None:
    sides = _sides()
    rows = {row["n"]: row for row in reports.check_claims(reports.packet_path(NAME))["results"]}
    for n, (reader, result, gain) in HOUSES.items():
        house = reports.house_side(reader, n)
        row = rows[n]
        assert (row["smallest"], row["case"]["relation"]) == (reports.THIS, "below")
        assert row["case"]["result"] == result
        assert Fraction(row["case"]["difference"]) == house - sides[n]
        assert f"{float(house - sides[n]):.4e}" == gain
        assert row["pending"] == []


def test_the_ledger_records_all_five_and_walks_nothing_at_270() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
                assert claim["packing"]["kind"] == "new packing"
                assert "Tomáš Kodaj" in claim["packing"]["continues"]
    assert recorded == {n: [f"#{ISSUE}"] for n in COUNTS}
    assert 270 not in {count["n"] for count in ledger["counts"]}
    assert [item["issue"] for item in ledger["other_items"]] == [f"#{ISSUE}"]


@pytest.mark.parametrize("n", COUNTS)
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(n: int) -> None:
    """Squares touch the box at every count, so the side is lowered by 0, the near-wall
    move is 0 and the enlargement to a wall grows a touching square by 0: accepted at
    contact and refused past it for the wall and its shape, the branch the plan stated."""
    record = _json(sharp.receipt_path(reports.packet_path(NAME), COUNTS, n))
    assert (record["n"], record["packet"], record["all_as_expected"]) == (n, NAME, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    assert len(record["controls"]) == 11
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)
    lowered = [row for row in record["controls"] if row["control"] == sharp.SIDE_LOWERED]
    assert [Fraction(row["detail"]["lowered_by"]) for row in lowered] == [
        0,
        kernel.SHARP_EPSILON,
    ]
    wall = [row for row in record["controls"] if row["control"] == sharp.ENLARGED_WALL]
    assert Fraction(wall[0]["detail"]["wall_clearance"]) == 0
    assert [(row["expected"], row["expected_failures"]) for row in wall] == [
        ("accepted", []),
        ("refused", ["container", "shape"]),
    ]
    pair = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.ENLARGED_PAIR and row["where"] == "at-contact"
    )
    assert (pair["expected_failures"], pair["detail"]["clean"]) == (["shape"], True)


def test_the_identity_measurements_the_notes_cite() -> None:
    """At every count no symmetry pairs the certificate one to one with its house's
    packing by nearest centres, and the optimal assignment moves dozens of squares beyond
    a tenth: a new arrangement relative to the record's packing, as Kodaj's would be. The
    house witness measures as the house's packet at each count."""
    beyond = {127: 70, 204: 73, 232: 35, 264: 44, 305: 113}
    for n, (_reader, result, _gain) in HOUSES.items():
        record = _json(reports.packet_path(NAME) / f"measure/identity-n{n}.json")
        assert record["n"] == n
        pairs = {pair["against"]: pair for pair in record["pairs"]}
        house = pairs[result]
        assert house["nearest_centre"]["one_to_one"] is False
        assert house["assignment"]["moved_beyond"]["1e-1"] == beyond[n]
        assert pairs["house-witness"]["assignment"] == house["assignment"]
        assert pairs["regularized"]["nearest_centre"]["one_to_one"] is False


def test_each_gain_lies_wholly_outside_its_house_contraction_margin() -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. Each
    house's margin, wall slack included, is at most about 3.0e-12 and each gain at least
    9.3e-4. Each certificate's own margin is about 1.2e-10 or less, and the side it would
    contract to is not a bound anyone reported."""
    sides = _sides()
    measure = reports.packet_path(NAME) / "measure"
    for n, (reader, result, _gain) in HOUSES.items():
        record = _json(measure / f"contraction-n{n:03d}.json")
        assert (record["n"], record["certificate"]["label"]) == (n, result)
        assert record["routes_accept"] is True
        assert Fraction(record["margin"]) < Fraction(3, 10**12)
        assert record["against"]["within_margin"] is False
        assert Fraction(record["against"]["gain"]) == reports.house_side(reader, n) - sides[n]
        own = _json(measure / f"contraction-n{n:03d}-own.json")
        assert own["routes_accept"] is True
        assert 0 < Fraction(own["margin"]) < Fraction(2, 10**10)


def test_the_l_step_scan_stands_the_sides_in_and_carries_them_nowhere() -> None:
    record = _json(reports.packet_path(NAME) / "measure/l-step-scan.json")
    sides = _sides()
    assert {int(n): Fraction(side) for n, side in record["with"].items()} == sides
    steps = record["l_step"]["improves"] + record["l_step"]["extensions"]
    assert not [row for row in steps if row["n"] in COUNTS or row["from"] in COUNTS]
    assert record["monotonicity"]["improves"] == []


#: The source's later revision, which adds `local-minimum/`: Evan Daniel's exactsolve.py
#: run by the author on each binary64 pose, with its inputs, logs, reports and certificates.
LOCAL_MINIMUM = "joegun-local-minimum-2026-11-16"
#: The regularization driver's run on the five new houses (think-0y9m), whose KKT solves
#: the record holds at row 3 for RV-3 (think-ruu2).
DRIVER = (
    reports.ROOT
    / "cases/regularized_drawings/think-0y9m-2026-11-16/adopt-2026-11-16-n127-305-evand"
)
#: The fields of the driver's solve block (`regularize_evand.solve_block`) that say how a
#: solve went and what it found; timings, attempts and rungs are the run's own.
SOLVE_FIELDS = (
    "status",
    "gate",
    "newton_converged",
    "cert_valid",
    "S_exact",
    "S_cert",
    "free",
    "promoted",
    "second_order",
    "vv_milp_dS",
)
#: The flat motions the source reports at each exact point, and how far below each
#: certificate's exact side the point lies, at the four significant figures the register's
#: notes print for the driver's held solves.
FLAT_MOTIONS = {127: 52, 232: 110, 264: 155, 305: 132}
HELD_BELOW = {127: "1.2175e-10", 232: "4.0164e-09", 264: "1.9066e-11", 305: "1.9146e-10"}


def test_the_sources_local_minimum_check_reaches_the_points_the_driver_holds() -> None:
    """#1001's local-minimum check, added after the filing, against the driver's solves.

    The author ran exactsolve.py at one pin of evand/square-packing from each binary64
    pose; the driver ran it at another from each exact certificate, so no input is shared.
    Read through the driver's own `solve_block`, the two agree wherever they solve, in
    every digit both print and in the second-order verdict, and both fail at 204. This is
    context for RV-3 (think-ruu2): nothing here registers a point or changes a rung."""
    retained = reports.packet_path(LOCAL_MINIMUM) / "source/local-minimum"
    receipt = {row["n"]: row for row in _json(DRIVER / "receipt.json")["counts"]}
    sides = _sides()
    for n in COUNTS:
        source = evand.solve_block(_json(retained / f"n-{n}-input.json"))
        report = json.loads(gzip.decompress((DRIVER / f"n-{n}/report.json.gz").read_bytes()))
        held = report["solve"]
        assert {key: source[key] for key in SOLVE_FIELDS} == {
            key: held[key] for key in SOLVE_FIELDS
        }
        written = hashlib.sha256((retained / f"n-{n}-input.txt").read_bytes()).hexdigest()
        assert written != report["input"]["sha256"]
        if n == 204:
            assert source["status"] == held["status"] == "solve failed"
            assert receipt[n]["decision"] == "no-view"
            continue
        assert (source["status"], source["gate"]) == ("KKT local min", "certified")
        assert (receipt[n]["row"], receipt[n]["decision"]) == (3, "held")
        assert f"strict modulo {FLAT_MOTIONS[n]} exact flat motions" in source["second_order"]
        assert Fraction(source["S_cert"]) == Fraction(report["outputs"]["solved"]["side_exact"])
        below = sides[n] - Fraction(source["S_exact"])
        assert f"{float(below):.4e}" == HELD_BELOW[n]
