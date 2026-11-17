"""The upper-bound import of the intake pass's lane L181 of 15 November 2026 (think-32cl).

One packet, read by the ``center-direction-json`` adapter: Joost de Winter's packing of 90
squares, reported in #996 at 64d5ee7 and replaced by its author in #997 by the packing at
fa53fb0, 9e-8 smaller, which the issue asks to be pinned instead. The issue says a local
search found it from T-303, jazivxt's packing of #989, the house at 90. Its side is a
rational that does not terminate at 12 places, and the issue prints it rounded up there. The
superseded certificate is retained in its own packet, which this one reads only to measure
against it. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it: the digests the source's
next commit states, the print against the exact side, the house it is compared with and the
gain, the ledger's verdicts, the retained sharp controls, the identity measurement, the
contraction margins and the L-step scan the register's notes cite. Every test reads the
packets and the ledger only; none needs the network.
"""

from __future__ import annotations

import json
from decimal import ROUND_CEILING, Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-996-997-20261115"
NAME = "de-winter-s90-upper-bound-2026-11-15"
SUPERSEDED = "de-winter-s90-64d5ee7-2026-11-15"
HOUSE = "jazivxt-s90-upper-bound-2026-11-15"
ISSUE = 997
N = 90
#: The certificate's side, the issue's print of it rounded up at 12 places, T-303's side and
#: the side of the certificate #996 named, which the author replaced.
SIDE = Fraction(99940387666098521323, 10**19)
PRINTED = "9.994038766610"
T303 = Fraction(4999138583463, 500000000000)
REPLACED = Fraction(199880777150913904183, 20000000000000000000)
#: The SHA-256 that n90/SHA256SUMS states at the source's head, 6c0ad56, one commit past the
#: pin, for the files of n90/ the pin shares with it; the pin's own copy still states the
#: digests of 9cafa33's files.
SUMMED = {
    "n90/n90_exact.json": "85840c5563e023790ae32af68c62d636e041a7d34f01c0f772979450dd188a2a",
    "n90/n90_witness.yaml": "c9aa917fa0abc9bfe4ddfdd73ec391b20e474fb0c5c97252a7819ad7152c1628",
    "n90/n90_record.png": "bfae0909c9b5e6c5cb389b9e4274c9cfe0729d1b45e12d7ff3f37464ce11c357",
    "n90/n90_before_after.png": (
        "3d5133b88caf90fa3f15e0a11ee7cb06d7e3c4216c769c8ce0f455bc44cd48f9"
    ),
    "n90/verify_exact.py": "76119299b04f801fa39123a74d0e9c3e28d1f90fb0a55339abc6374c2514d189",
    "n90/check_area.py": "fc123d58a710229eb6f0c57014e1140e6820eeb04316d8b62f56890e78c1d81f",
    "n90/README.md": "51a280dc9e607b71ddf546bf1d8d7f319cb0399d597975b4d2ccc49b13c967e7",
}
#: The digest the pin's stale n90/SHA256SUMS states for n90_exact.json: #996's certificate's.
STALE = "3adcc363dc2d2cd5e52c1d0196536d137c2039de532de52b5eab39ba7a98e2dc"


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest(name: str) -> dict[str, str]:
    text = (reports.packet_path(name) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def _side() -> Fraction:
    return reports.read_facts(reports.packet_path(NAME))[N].side


def test_the_packet_holds_the_files_whose_digests_the_next_commit_states() -> None:
    manifest = _manifest(NAME)
    assert all(manifest[path] == digest for path, digest in SUMMED.items())
    assert set(manifest) == {
        *SUMMED,
        "LICENSE",
        "README.md",
        "n90/REGISTRATION.md",
        "n90/SHA256SUMS",
    }
    stale = (reports.packet_path(NAME) / "source/n90/SHA256SUMS").read_text("utf-8")
    assert f"{STALE}  n90_exact.json" in stale.splitlines()
    superseded = _manifest(SUPERSEDED)
    assert superseded["n90/n90_exact.json"] == STALE
    assert superseded["n90/verify_exact.py"] == manifest["n90/verify_exact.py"]


def test_the_print_is_its_exact_side_rounded_up_and_its_reader_rebuilds_it() -> None:
    declaration = reports.load_declaration(reports.packet_path(NAME))
    assert declaration["source_key"] == f"[de Winter s{N} upper bound {NAME[-10:]}]"
    assert declaration["issue"].endswith(f"/issues/{ISSUE}")
    assert (declaration["requested"], declaration["replayed"]) == ([N], [N])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (N, "center-direction-json", PRINTED)
    assert row.get("same_packing") == [
        {"path": "n90/n90_witness.yaml", "format": "witness-corners-opposite"}
    ]
    side = _side()
    assert side == SIDE
    exact = Decimal(side.numerator) / Decimal(side.denominator)
    assert exact != Decimal(PRINTED)
    assert str(exact.quantize(Decimal("1e-12"), rounding=ROUND_CEILING)) == PRINTED
    assert f"{float(REPLACED - side):.4e}" == "9.0936e-08"


def test_the_certificate_is_below_t303_the_house_by_the_gain() -> None:
    side = _side()
    assert reports.house_side("[jazivxt s90 upper bound 2026-11-15]", N) == T303
    (row,) = reports.check_claims(reports.packet_path(NAME))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (N, reports.THIS, "below")
    assert (row["case"]["result"], row["case"]["holders"]) == ("T-303", "jazivxt")
    assert Fraction(row["case"]["difference"]) == T303 - side
    assert f"{float(T303 - side):.4e}" == "4.2384e-03"
    assert row["pending"] == []


def test_the_ledger_records_the_replacement_and_not_the_replaced_claim() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
                assert claim["packing"]["kind"] == "new packing"
                assert "(T-303)" in claim["packing"]["continues"]
    assert recorded == {N: [f"#{ISSUE}"]}
    assert [item["issue"] for item in ledger["other_items"]] == ["#996"]


def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it() -> None:
    record = _json(reports.packet_path(NAME) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (N, NAME, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    assert len(record["controls"]) == 11
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)
    # The least-gap pair is squares 2 and 40, about 2.0264e-12 apart, the gap of 2e-12 the
    # README states. Squares touch the left or bottom wall exactly, so the near-wall move is
    # 0 and the enlargement to the wall grows square 10, already touching, by 0: accepted at
    # contact, and refused past it for the wall and its shape.
    pair = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.TIGHTEST_PAIR and row["where"] == "at-contact"
    )
    assert (pair["detail"]["square"], pair["detail"]["partner"]) == (40, 2)
    assert f"{float(Fraction(pair['detail']['moved_by'])):.5e}" == "2.02641e-12"
    near = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.NEAR_WALL and row["where"] == "at-contact"
    )
    assert Fraction(near["detail"]["moved_by"]) == 0
    wall = [row for row in record["controls"] if row["control"] == sharp.ENLARGED_WALL]
    assert [row["detail"]["square"] for row in wall] == [10, 10]
    assert Fraction(wall[0]["detail"]["wall_clearance"]) == 0
    assert [(row["expected"], row["expected_failures"]) for row in wall] == [
        ("accepted", []),
        ("refused", ["container", "shape"]),
    ]


def test_the_identity_measurement_the_notes_cite() -> None:
    """Against T-303, the house: no symmetry pairs it one to one by nearest centres, the
    optimal assignment under the identity moves 6 squares beyond a tenth (largest 0.645009),
    and each of its 40 tilted squares pairs with one T-303 tilts the same way. Against the
    certificate #996 named, which it replaces, it is one to one by nearest centres under
    the identity, no square moved beyond 0.0142. The source's corner twin, read from the
    vertex its corners start at, is the JSON's packing square for square."""
    record = _json(reports.packet_path(NAME) / "measure/identity.json")
    assert record["n"] == N
    pairs = {pair["against"]: pair for pair in record["pairs"]}
    assert set(pairs) == {"T-303", "regularized", "house-witness", "twin", "#996", "#996-twin"}
    pair = pairs["T-303"]
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["symmetry"] == 0
    assert pair["assignment"]["moved_beyond"]["1e-1"] == 6
    assert pair["assignment"]["largest_move"] == "0.645009"
    assert pair["bands"]["tilted_paired_same_sign"] == 40
    assert pair["bands"]["tilted_paired_opposite_sign"] == 0
    assert pair["bands"]["tilted_paired_with_untilted"] == 0
    assert pairs["house-witness"]["assignment"] == pair["assignment"]
    replaced = pairs["#996"]
    assert replaced["nearest_centre"]["one_to_one"] is True
    assert replaced["nearest_centre"]["symmetry"] == 0
    assert replaced["assignment"]["largest_move"] == "0.0141781"
    assert replaced["assignment"]["moved_beyond"]["1e-1"] == 0
    assert pairs["#996-twin"]["assignment"] == replaced["assignment"]
    twin = pairs["twin"]
    assert twin["side_difference_exact"] == "0"
    assert twin["nearest_centre"]["one_to_one"] is True
    assert set(twin["nearest_centre"]["moved_beyond"].values()) == {0}
    assert twin["nearest_centre"]["largest_turn_degrees"] == "0"
    tilts = record["tilts"]["DEWINTER"]
    assert (tilts["tilted_beyond_1_degree"], tilts["tilted_negative"]) == (40, 40)
    assert (tilts["exactly_turned"], tilts["near_upright"]) == (40, 0)
    assert record["tilts"]["T-303"]["tilted_beyond_1_degree"] == 44


def test_the_gain_lies_wholly_outside_the_predecessors_contraction_margins() -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. T-303's
    margin, wall slack included, is about 1.0988e-11, and the gain is about 3.9e8 times it.
    The replaced certificate's margin is about 9.53e-12, and the step from it, about
    9.09e-8, is about 9.5e3 times that. This certificate's own margin is about 1.82e-11,
    and the side it would contract to is not a bound anyone reported."""
    side = _side()
    measure = reports.packet_path(NAME) / "measure"
    record = _json(measure / f"contraction-n{N:03d}.json")
    assert (record["n"], record["certificate"]["packet"]) == (N, HOUSE)
    assert record["routes_accept"] is True
    assert record["binding_pair"] == [79, 81]
    assert record["margin_float"] == "1.098813e-11"
    assert record["against"]["within_margin"] is False
    assert Fraction(record["against"]["gain"]) == T303 - side
    replaced = _json(measure / f"contraction-n{N:03d}-996.json")
    assert replaced["routes_accept"] is True
    assert replaced["binding_pair"] == [2, 40]
    assert replaced["margin_float"] == "9.532970e-12"
    assert replaced["against"]["within_margin"] is False
    assert Fraction(replaced["against"]["gain"]) == REPLACED - side
    own = _json(measure / f"contraction-n{N:03d}-own.json")
    assert own["routes_accept"] is True
    assert own["binding_pair"] == [2, 40]
    assert own["margin_float"] == "1.818734e-11"


def test_the_l_step_scan_stands_the_side_in_and_carries_it_nowhere() -> None:
    """With the side stood in, nothing moves: the L step from 90 lands at 109 above its
    ceiling, as from T-303, and monotonicity carries nothing."""
    record = _json(reports.packet_path(NAME) / "measure/l-step-scan.json")
    assert Fraction(record["with"][str(N)]) == _side()
    assert Fraction(record["replaced"][str(N)]) == T303
    assert all(row["from"] != N for row in record["l_step"]["improves"])
    assert all(row["from"] != N for row in record["l_step"]["extensions"])
    assert N not in {row["n"] for row in record["l_step"]["improves"]}
    assert record["monotonicity"]["improves"] == []
