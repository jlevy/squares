"""The upper-bound import of the intake pass's lane c7-pointers of 20 November 2026.

Bead think-wvr8. One packet: Joost de Winter's corner Witness/v2 at 109 (#1012's comment of
18 November, ``witness-corners`` with ``first_id`` 0), his exact transcription of Tomáš
Kodaj's CC0 Kaggle rows. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it: the digests lane w10-1118
recorded for the attachment's members, the exact side the comment states, the house it is
compared with and the gain, the ledger's verdict, the retained control plan and sharp
controls, the identity measurements, the option D comparison with Samanyu-dev's public 109
shrunk to first contact, and the L-step scan the register's notes cite. Every test reads the
packet and the ledger only; none needs the network.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

NAME = "de-winter-kodaj-n109-2026-11-18"
LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-1012-20261120"
#: The SHA-256 of the attachment's members, as lane w10-1118 recorded them on think-wvr8 on
#: 18 November from its own retrieval of the zip.
MEMBERS = {
    "n109_kaggle/n109_tomkodaj.csv": (
        "c4f76a5a0dcf6055da754bc35a8ea23abb832109b4d0dc4c534924f47b631e8b"
    ),
    "n109_kaggle/n109_tomkodaj.yaml": (
        "56b4655fada7dfd5d54c1483b021d5b700ecb5c41beba2865a6a8ef7e223b3fb"
    ),
    "n109_kaggle/verification.txt": (
        "d9647ac120a2bfeaac88dc12f48ea60c8fddb451cd855ff007b94aec20ac38d4"
    ),
}
#: The control plan's SHA-256, recorded on think-wvr8 before any route decided the certificate.
PLAN = "323a526f22032acd4a7636381d0a170ac914192eb770329aec92a9efbfdcd49b"
#: The SHA-256 of best_fit_101_500.csv at Samanyu-dev/squares_in_squares 53551d7.
SAMANYU = "377b9177febf1b89f08d655531880fb683666e494a3b303f10645e7440996c04"
SIDE = Fraction(547464479047171949843, 50000000000000000000)


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _packet() -> Path:
    return reports.packet_path(NAME)


def test_the_packet_holds_the_attachments_members_byte_for_byte() -> None:
    text = (_packet() / "acquisition/upstream-subtree.sha256").read_text("utf-8")
    manifest = {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }
    assert {path: manifest[path] for path in MEMBERS} == MEMBERS


def test_the_side_is_the_comments_exact_fraction_read_from_squares_numbered_from_zero() -> None:
    declaration = reports.load_declaration(_packet())
    assert declaration["issue"].endswith("/issues/1012")
    assert declaration["requested"] == declaration["replayed"] == [109]
    (row,) = declaration["certificates"]
    assert row["offered"] == "547464479047171949843/50000000000000000000"
    assert reports.row_options(row) == {reports.FIRST_ID: "0"}
    assert reports.read_facts(_packet(), {109})[109].side == SIDE
    # The issue's first print, rounded to nearest, lies below the side and bounds nothing.
    assert Fraction("10.949289580943") < SIDE <= Fraction("10.949289580944")


def test_the_certificate_is_below_the_house_by_the_gain() -> None:
    row = reports.check_claims(_packet())["results"][0]
    case = row["case"]
    assert (row["smallest"], case["relation"], case["result"]) == (
        reports.THIS,
        "below",
        "T-101",
    )
    assert row["pending"] == []
    assert f"{float(Fraction(case['difference'])):.4e}" == "4.5789e-04"


def test_the_ledger_records_the_comment_as_a_new_packing() -> None:
    ledger = _json(LEDGER / "ledger.json")
    walked = {
        count["n"]: [(step["report"], step["verdict"]) for step in count["steps"]]
        for count in ledger["counts"]
    }
    assert walked == {109: [("#1012 update", "recorded")]}


def test_the_control_plan_is_the_one_hashed_on_the_bead() -> None:
    plan = (_packet() / "receipts/controls-plan-1012-n109.md").read_bytes()
    assert hashlib.sha256(plan).hexdigest() == PLAN


def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it() -> None:
    """Square 39 touches its wall, so it grows by 0 and is accepted at contact; the least
    pair gap, about 2.0e-15 at squares 60 and 70, exceeds the step, so square 70 enlarged to
    its partner is refused at contact for its shape alone."""
    record = _json(sharp.receipt_path(_packet(), [109], 109))
    assert (record["n"], record["packet"], record["all_as_expected"]) == (109, NAME, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    assert len(record["controls"]) == 11
    for row in record["controls"]:
        assert row["as_expected"] is True
        verdicts = {
            route: (
                outcome["passed"],
                tuple(outcome["failures"]),
                outcome["wall"],
                outcome["gap"],
            )
            for route, outcome in row["routes"].items()
        }
        assert set(verdicts) == set(kernel.ROUTES)
        assert len(set(verdicts.values())) == 1
    wall = [row for row in record["controls"] if row["control"] == sharp.ENLARGED_WALL]
    assert wall[0]["detail"]["square"] == 39
    assert Fraction(wall[0]["detail"]["wall_clearance"]) == 0
    pair = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.ENLARGED_PAIR and row["where"] == "at-contact"
    )
    assert (pair["detail"]["square"], pair["detail"]["partner"]) == (70, 60)
    assert pair["expected_failures"] == ["shape"]


def test_the_identity_pairs_it_with_samanyu_devs_109_and_kodajs_rows_not_the_house() -> None:
    record = _json(_packet() / "measure/identity.json")
    assert record["inputs"]["SAMANYU-53551d7"]["sha256"] == SAMANYU
    pairs = {pair["against"]: pair for pair in record["pairs"]}
    assert pairs["T-101"]["nearest_centre"]["one_to_one"] is False
    assert pairs["T-101"]["assignment"]["moved_beyond"]["1e-1"] == 56
    samanyu = pairs["SAMANYU-53551d7"]
    assert samanyu["nearest_centre"]["one_to_one"] is True
    assert samanyu["assignment"]["moved_beyond"]["1e-3"] == 37
    assert samanyu["assignment"]["moved_beyond"]["1e-1"] == 0
    rows = pairs["KODAJ-ROWS"]
    assert rows["assignment"]["moved_beyond"]["1e-9"] == 0
    assert record["tilts"]["KODAJ"]["tilted_beyond_1_degree"] == 45
    assert record["tilts"]["SAMANYU-53551d7"]["tilted_beyond_1_degree"] == 45


def test_option_d_the_certificate_lies_within_samanyu_devs_padding() -> None:
    """The owner's option D (think-b0w5): Samanyu-dev's 109, read exactly and boxed at its
    own extent, contracted uniformly to first contact has margin 1.9960e-12; the gain is
    0.9721 of it, so the contracted predecessor lies 5.57e-14 below this certificate, which
    restates it. Its own margin is 1.99e-14."""
    record = _json(_packet() / "measure/contraction-n109-samanyu.json")
    assert record["certificate"]["sha256"] == SAMANYU
    assert (record["certificate"]["label"], record["binding_pair"]) == (
        "SAMANYU-53551d7",
        [17, 73],
    )
    assert record["routes_accept"] is True
    assert all(verdict["passed"] for verdict in record["certificate_routes"].values())
    against = record["against"]
    assert against["certificate"] == {"label": "KODAJ", "input": "packet", "packet": NAME}
    assert Fraction(against["side"]) == SIDE
    assert against["within_margin"] is True
    assert against["gain_over_margin"] == "0.9721"
    below = SIDE - Fraction(record["contracted_side"])
    assert Fraction(55, 10**15) < below < Fraction(56, 10**15)
    own = _json(_packet() / "measure/contraction-n109-own.json")
    assert (own["certificate"]["label"], own["binding_pair"]) == ("KODAJ", [60, 70])
    assert 0 < Fraction(own["margin"]) < Fraction(2, 10**14)


def test_the_l_step_scan_stands_the_side_in_and_carries_it_nowhere() -> None:
    record = _json(_packet() / "measure/l-step-scan.json")
    assert {int(n): Fraction(side) for n, side in record["with"].items()} == {109: SIDE}
    steps = record["l_step"]["improves"] + record["l_step"]["extensions"]
    assert not [row for row in steps if 109 in (row["n"], row["from"])]
    assert record["monotonicity"]["improves"] == []
