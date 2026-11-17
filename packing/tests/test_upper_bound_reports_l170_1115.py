"""The upper-bound import of the intake pass's lane L170 of 15 November 2026 (think-i8y9).

One packet, read by the ``evand-cert`` adapter: jazivxt's packing of 90 squares, reported in
#989 by the account dpre4ai (dpre4ai/n90-square-packing, pinned at f9b31b4, whose parent
179fcba the issue names), the first packing below the 10 x 10 grid at 90. The issue says it
is a window of two shifted copies of a crop of Joost de Winter's 157 (T-293). Its side is a
rational that terminates at 12 places, and the issue prints it exactly. The general
importer's checks run on the packet through ``test_upper_bound_reports``; these hold what is
particular to it: the digests the issue and the source print, the print against the exact
side, the grid it is compared with and the gain the issue states, the ledger's verdict, the
retained sharp controls, the identity measurement, the contraction margins and the L-step
scan the register's notes cite. Every test reads the packet and the ledger only; none needs
the network.
"""

from __future__ import annotations

import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-989-20261115"
NAME = "jazivxt-s90-upper-bound-2026-11-15"
ISSUE = 989
N = 90
#: The certificate's side, which the issue and README print exactly, and the gain on the
#: grid's 10 the issue states.
SIDE = Fraction(4999138583463, 500000000000)
PRINTED = "9.998277166926"
GAIN = "0.001722833074"
#: The SHA-256 the issue prints for the certificate, and SHA256SUMS's digests, which
#: predate the construction figure the pinned head adds.
CERTIFICATE_DIGEST = "88c93b2f1d1f3061d1e6815f790d13f3d8f174dd3431f50d8d4d9d4383b3d466"
SUMMED = ("README.md", "n90.cert", "n90.csv", "n90.png", "DONOR-LICENSE.txt")


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


def test_the_packet_holds_the_files_whose_digests_the_issue_and_source_print() -> None:
    manifest = _manifest()
    assert manifest["n90.cert"] == CERTIFICATE_DIGEST
    # SHA256SUMS states five of the seven files; the construction figure came after it.
    summed = {
        path: digest
        for digest, path in (
            line.split(maxsplit=1)
            for line in (reports.packet_path(NAME) / "source/SHA256SUMS")
            .read_text("utf-8")
            .splitlines()
        )
    }
    assert sorted(summed) == sorted(SUMMED)
    assert all(manifest[path] == digest for path, digest in summed.items())
    assert set(manifest) == {*SUMMED, "SHA256SUMS", "n90-construction.png"}


def test_the_print_is_its_exact_side_and_its_reader_rebuilds_it() -> None:
    declaration = reports.load_declaration(reports.packet_path(NAME))
    assert declaration["source_key"] == f"[jazivxt s{N} upper bound {NAME[-10:]}]"
    assert declaration["issue"].endswith(f"/issues/{ISSUE}")
    assert (declaration["requested"], declaration["replayed"]) == ([N], [N])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (N, "evand-cert", PRINTED)
    side = _side()
    assert side == SIDE == Fraction(Decimal(PRINTED))
    assert reports.house_side(declaration["source_key"], N) == side


def test_the_certificate_is_below_the_grid_by_the_gain_the_issue_states() -> None:
    side = _side()
    assert reports.grid_side(N) == 10
    assert reports.grid_side(N) - side == Fraction(Decimal(GAIN))
    (row,) = reports.check_claims(reports.packet_path(NAME))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (N, reports.THIS, "below")
    assert (row["case"]["source_key"], row["case"]["holders"]) == ("[Kingbird]", "trivial grid")
    assert Fraction(row["case"]["difference"]) == Fraction(Decimal(GAIN))
    assert row["pending"] == []


def test_the_ledger_records_the_claim_as_a_new_packing() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
                assert claim["packing"]["kind"] == "new packing"
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
    # The least-gap pair is squares 79 and 81, about 1.194e-12 apart, the separation the
    # issue states; no square touches a wall, the least clearance about 2.1e-15, so the
    # enlargement to the wall grows square 28 and is refused at contact for shape alone.
    pair = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.TIGHTEST_PAIR and row["where"] == "at-contact"
    )
    assert (pair["detail"]["square"], pair["detail"]["partner"]) == (81, 79)
    assert f"{float(Fraction(pair['detail']['moved_by'])):.5e}" == "1.19448e-12"
    wall = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.ENLARGED_WALL and row["where"] == "at-contact"
    )
    assert wall["detail"]["square"] == 28
    assert Fraction(wall["detail"]["wall_clearance"]) == Fraction(21000000001021, 10**28)
    assert (wall["expected"], wall["expected_failures"]) == ("refused", ["shape"])


def test_the_identity_measurement_the_notes_cite() -> None:
    """Measured against the grid house: no symmetry pairs it one to one with the grid, the
    optimal assignment moves 52 squares beyond a tenth (largest 1.33219), and 44 squares are
    tilted beyond a degree, 22.6 to 31.6 degrees, all one way."""
    record = _json(reports.packet_path(NAME) / "measure/identity.json")
    assert record["n"] == N
    (pair,) = record["pairs"]
    assert (pair["view"], pair["against"]) == ("JAZIVXT", "grid")
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["moved_beyond"]["1e-3"] == N
    assert pair["assignment"]["moved_beyond"]["1e-1"] == 52
    assert pair["assignment"]["largest_move"] == "1.33219"
    tilts = record["tilts"]["JAZIVXT"]
    assert (tilts["tilted_beyond_1_degree"], tilts["tilted_negative"]) == (44, 44)
    assert tilts["tilted_positive"] == 0
    assert [round(a, 1) for a in tilts["tilt_range_degrees"]] == [22.6, 31.6]
    assert record["tilts"]["grid"]["exactly_turned"] == 0


def test_the_gain_lies_wholly_outside_the_grid_s_contraction_margin() -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. The grid
    has none, its squares touching, so the entry is not held for it. This certificate's own
    margin is about 1.1e-11, and the side it would contract to is not a bound anyone
    reported."""
    gain = reports.grid_side(N) - _side()
    record = _json(reports.packet_path(NAME) / f"measure/contraction-n{N:03d}.json")
    assert (record["n"], record["certificate"]["label"]) == (N, "grid")
    assert record["routes_accept"] is True
    assert Fraction(record["margin"]) == 0
    assert record["against"]["within_margin"] is False
    assert Fraction(record["against"]["gain"]) == gain
    own = _json(reports.packet_path(NAME) / f"measure/contraction-n{N:03d}-own.json")
    assert own["routes_accept"] is True
    assert own["binding_pair"] == [79, 81]
    assert 0 < Fraction(own["margin"]) < Fraction(2, 10**11)
    assert gain > 10**8 * Fraction(own["margin"])


def test_the_l_step_scan_stands_the_side_in_and_carries_it_nowhere() -> None:
    """With the side stood in, the L step from 90 lands at 109 above its ceiling, and the
    L-extension of the grid at 90 to 111 lapses; monotonicity carries nothing."""
    record = _json(reports.packet_path(NAME) / "measure/l-step-scan.json")
    assert Fraction(record["with"][str(N)]) == _side()
    assert record["replaced"] == {str(N): "10"}
    assert all(row["from"] != N for row in record["l_step"]["improves"])
    assert all(row["from"] != N for row in record["l_step"]["extensions"])
    assert N not in {row["n"] for row in record["l_step"]["improves"]}
    assert record["monotonicity"]["improves"] == []
