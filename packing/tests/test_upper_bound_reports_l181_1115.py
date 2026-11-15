"""The upper-bound import of the intake pass's lane L181 of 15 November 2026 (think-32cl).

One packet, read by the ``center-direction-json`` adapter: Joost de Winter's packing of 90
squares, reported in #996 (JoostdeWinter/square-packing, pinned at 64d5ee7, the commit the
issue names), which the issue says a local search found from T-303, jazivxt's packing of
#989, the house at 90. Its side is a rational that does not terminate at 12 places, and the
issue prints it rounded up there. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it: the digests the source's
later checksum file states, the print against the exact side, the house it is compared with
and the gain, the ledger's verdict, the retained sharp controls, the identity measurement,
the contraction margins and the L-step scan the register's notes cite. Every test reads the
packet and the ledger only; none needs the network.
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

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-996-20261115"
NAME = "de-winter-s90-upper-bound-2026-11-15"
HOUSE = "jazivxt-s90-upper-bound-2026-11-15"
ISSUE = 996
N = 90
#: The certificate's side, the issue's print of it rounded up at 12 places, and T-303's side.
SIDE = Fraction(199880777150913904183, 20000000000000000000)
PRINTED = "9.994038857546"
T303 = Fraction(4999138583463, 500000000000)
#: The SHA-256 that n90/SHA256SUMS states at the source's head, 9cafa33, for the seven files
#: of n90/ the pin holds besides its README, which the head changes.
SUMMED = {
    "n90/n90_exact.json": "3adcc363dc2d2cd5e52c1d0196536d137c2039de532de52b5eab39ba7a98e2dc",
    "n90/n90_witness.yaml": "3a28f570aaabfa5cb443d1c270925733d714009850deee852abde5f63e809aa6",
    "n90/n90_record.png": "3955cfcc451016e29358dded3a9319811c6be67dc9c70e1eb1a601c39bfeada0",
    "n90/n90_before_after.png": (
        "ac0042fbc501f164c5ff89349b3487a2d149abdd399429f393e1e0950a2d2ff9"
    ),
    "n90/verify_exact.py": "76119299b04f801fa39123a74d0e9c3e28d1f90fb0a55339abc6374c2514d189",
    "n90/check_area.py": "fc123d58a710229eb6f0c57014e1140e6820eeb04316d8b62f56890e78c1d81f",
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest() -> dict[str, str]:
    text = (reports.packet_path(NAME) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def _side() -> Fraction:
    return reports.read_facts(reports.packet_path(NAME))[N].side


def test_the_packet_holds_the_files_whose_digests_the_source_states_later() -> None:
    manifest = _manifest()
    assert all(manifest[path] == digest for path, digest in SUMMED.items())
    assert set(manifest) == {*SUMMED, "LICENSE", "README.md", "n90/README.md"}


def test_the_print_is_its_exact_side_rounded_up_and_its_reader_rebuilds_it() -> None:
    declaration = reports.load_declaration(reports.packet_path(NAME))
    assert declaration["source_key"] == f"[de Winter s{N} upper bound {NAME[-10:]}]"
    assert declaration["issue"].endswith(f"/issues/{ISSUE}")
    assert (declaration["requested"], declaration["replayed"]) == ([N], [N])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (N, "center-direction-json", PRINTED)
    side = _side()
    assert side == SIDE
    assert Decimal(side.numerator) / Decimal(side.denominator) != Decimal(PRINTED)
    rounded = (Decimal(side.numerator) / Decimal(side.denominator)).quantize(
        Decimal("1e-12"), rounding=ROUND_CEILING
    )
    assert str(rounded) == PRINTED


def test_the_certificate_is_below_t303_the_house_by_the_gain() -> None:
    side = _side()
    assert reports.house_side("[jazivxt s90 upper bound 2026-11-15]", N) == T303
    (row,) = reports.check_claims(reports.packet_path(NAME))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (N, reports.THIS, "below")
    assert (row["case"]["result"], row["case"]["holders"]) == ("T-303", "jazivxt")
    assert Fraction(row["case"]["difference"]) == T303 - side
    assert f"{float(T303 - side):.3e}" == "4.238e-03"
    assert row["pending"] == []


def test_the_ledger_records_the_claim_continuing_t303() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
                assert claim["packing"]["kind"] == "new packing"
                assert "(T-303)" in claim["packing"]["continues"]
    assert recorded == {N: [f"#{ISSUE}"]}


def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it() -> None:
    record = _json(reports.packet_path(NAME) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (N, NAME, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    assert len(record["controls"]) == 11
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)
    # The least-gap pair is squares 2 and 40, about 1.0641e-12 apart, the gap of about 1e-12
    # the issue states. Squares touch the left or bottom wall exactly, so the near-wall move is
    # 0 and the enlargement to the wall grows square 10, already touching, by 0: accepted at
    # contact, and refused past it for the wall and its shape.
    pair = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.TIGHTEST_PAIR and row["where"] == "at-contact"
    )
    assert (pair["detail"]["square"], pair["detail"]["partner"]) == (40, 2)
    assert f"{float(Fraction(pair['detail']['moved_by'])):.5e}" == "1.06410e-12"
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
    """Measured against T-303, the house: no symmetry pairs it one to one by nearest
    centres, the optimal assignment under the identity moves 6 squares beyond a tenth
    (largest 0.646081), and its 40 tilted squares each pair with one T-303 tilts the same
    way; the house witness measures as T-303's packet. The source's corner witness, whose
    corners start at the vertex opposite the one `pose_corners` starts at, is the JSON's
    packing square for square, no square moved or turned modulo a quarter turn."""
    record = _json(reports.packet_path(NAME) / "measure/identity.json")
    assert record["n"] == N
    pairs = {pair["against"]: pair for pair in record["pairs"]}
    assert set(pairs) == {"T-303", "regularized", "house-witness", "twin"}
    twin = pairs["twin"]
    assert twin["side_difference_exact"] == "0"
    assert twin["nearest_centre"]["one_to_one"] is True
    assert twin["nearest_centre"]["symmetry"] == 0
    assert set(twin["nearest_centre"]["moved_beyond"].values()) == {0}
    assert twin["nearest_centre"]["largest_turn_degrees"] == "0"
    assert twin["nearest_centre"]["turned_beyond_1e-6"] == 0
    pair = pairs["T-303"]
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["symmetry"] == 0
    assert pair["assignment"]["moved_beyond"]["1e-1"] == 6
    assert pair["assignment"]["largest_move"] == "0.646081"
    assert pair["bands"]["tilted_paired_same_sign"] == 40
    assert pair["bands"]["tilted_paired_opposite_sign"] == 0
    assert pair["bands"]["tilted_paired_with_untilted"] == 0
    assert pairs["house-witness"]["assignment"] == pair["assignment"]
    tilts = record["tilts"]["DEWINTER"]
    assert (tilts["tilted_beyond_1_degree"], tilts["tilted_negative"]) == (40, 40)
    assert tilts["near_upright"] == 50
    assert tilts["near_upright_beyond_1e-3_degrees"] == []
    assert record["tilts"]["T-303"]["tilted_beyond_1_degree"] == 44


def test_the_gain_lies_wholly_outside_t303_s_contraction_margin() -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. T-303's
    margin, wall slack included, is about 1.0988e-11, and the gain is about 3.9e8 times it,
    so the entry is not held for it. This certificate's own margin is about 9.5e-12, and the
    side it would contract to is not a bound anyone reported."""
    gain = T303 - _side()
    record = _json(reports.packet_path(NAME) / f"measure/contraction-n{N:03d}.json")
    assert (record["n"], record["certificate"]["packet"]) == (N, HOUSE)
    assert record["routes_accept"] is True
    assert record["binding_pair"] == [79, 81]
    assert record["margin_float"] == "1.098813e-11"
    assert record["against"]["within_margin"] is False
    assert Fraction(record["against"]["gain"]) == gain
    assert gain > 10**8 * Fraction(record["margin"])
    own = _json(reports.packet_path(NAME) / f"measure/contraction-n{N:03d}-own.json")
    assert own["routes_accept"] is True
    assert own["binding_pair"] == [2, 40]
    assert own["margin_float"] == "9.532970e-12"


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
