"""The upper-bound import of the intake pass's lane L76 of 9 November 2026 (think-3guf).

One packet, read by the ``witness-corners`` adapter: Doğa Özden's #938 at 199
(kenaznia-doga/s199-upper-bound d03ee0b). Its witness is his #935 certificate at 172 (T-282),
its rational corners unchanged, with an L of 27 axis-aligned unit squares at side
``S172 + 1``: the L step of DS7, section 2, which `devtools.construction_checker` writes out
as its lemma states it. The grid squares touch each other and the walls exactly, so the
replay's least pair gap and wall clearance are both 0. The general importer's checks run on
the packet through ``test_upper_bound_reports``; these hold what is particular to it: the
digests the issue and README print, the print against the exact side, the construction
pose for pose, the house and the improvement the issue states, the ledger's verdict, the
retained sharp controls, contraction margins and identity measurement, and the exact
L-step scan (`devtools.l_step_scan`) with the receipts the register's notes cite. Every
test reads the packets, the ledger and stand-in ceilings only; none needs the network.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import construction_checker as construction
from devtools import evand_arrangement_reports as kernel
from devtools import exact_sides
from devtools import l_step_scan as scan
from devtools import select_houses as houses
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

PACKET = "ozden-s199-upper-bound-2026-11-09"
PARENT = "ozden-s172-upper-bound-2026-11-09"
LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-938-20261109"
#: The digests the issue (the witness) and the README and .meta.json (both files) print.
PRINTED_DIGESTS = (
    "8a85b4c3536757a77fd51e2a0e361de1ecef36b38d59ed3111611672e6a78aca",
    "88d20ae206367d2029b05221d4a9975c86f8a71ffd51ac065aeebf168f4a6cb8",
)
PRINTED = "14.614689853287"
CEILING = "14.6146898532862152"
HOUSE = "[Gupta rational refinements 2026-10-08]"
GAIN = "2.882e-03"


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


def _up(side: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(side * 10**places), 10**places)


def _certificate(name: str, n: int) -> Any:
    return reports.read_facts(reports.packet_path(name), {n})[n]


def test_the_packet_holds_the_files_whose_digests_the_issue_prints() -> None:
    manifest = _manifest(PACKET)
    assert (manifest["n-199-candidate.yaml"], manifest["n199-witness.json"]) == PRINTED_DIGESTS
    # The decimal pose the witness's source.path names, and the lab's metadata, beside it.
    assert {"n-199-decimal-pose.yaml", ".meta.json"} <= set(manifest)


def test_the_print_is_the_exact_side_rounded_up_and_the_reader_rebuilds_it() -> None:
    declaration = reports.load_declaration(reports.packet_path(PACKET))
    assert declaration["source_key"] == "[Özden s199 upper bound 2026-11-09]"
    assert declaration["issue"].endswith("/issues/938")
    assert (declaration["requested"], declaration["replayed"]) == ([199], [199])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (199, "witness-corners", PRINTED)
    assert [other["path"] for other in row.get("same_packing", [])] == ["n199-witness.json"]
    side = _certificate(PACKET, 199).side
    assert _up(side, 12) == Fraction(Decimal(PRINTED))
    assert _up(side, 16) == Fraction(Decimal(CEILING))
    assert reports.house_side(declaration["source_key"], 199) == side


def test_the_certificate_is_t282s_with_the_l_step_pose_for_pose() -> None:
    """Squares 1 to 172 are T-282's retained certificate and the other 27 the row of 14 and
    the column of 13 the construction checker's lemma writes at ``S172 + 1``."""
    parent = _certificate(PARENT, 172)
    found = _certificate(PACKET, 199)
    recipe = construction.Recipe(
        n=199,
        kind=construction.TILING,
        source_n=172,
        parent=f"packing/resources/web/{PARENT}/source/n-172-candidate.yaml",
        parent_sha256=_manifest(PARENT)["n-172-candidate.yaml"],
        bound=parent.side + 1,
        layers=1,
    )
    assert math.floor(parent.side) == 13
    assert construction.capacity(recipe, parent.side) == 199
    assert found.side == parent.side + 1
    assert found == construction.write_out(recipe, parent)
    assert found.poses[:172] == parent.poses


def test_the_certificate_is_below_the_house_by_the_improvement_the_issue_states() -> None:
    side = _certificate(PACKET, 199).side
    difference = reports.house_side(HOUSE, 199) - side
    assert difference > 0
    assert f"{float(difference):.3e}" == GAIN
    (row,) = reports.check_claims(reports.packet_path(PACKET))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (199, reports.THIS, "below")
    assert (row["case"]["source_key"], row["case"]["result"]) == (HOUSE, "T-127")
    assert Fraction(row["case"]["difference"]) == difference
    # Below the two re-certifications of the house's packing pending adoption as well.
    assert [(item["result"], item["relation"]) for item in row["pending"]] == [
        ("T-174", "below"),
        ("T-193", "below"),
    ]


def test_the_ledger_records_the_claim() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded = [
        (count["n"], claim["report"])
        for count in ledger["counts"]
        for claim in count["steps"]
        if claim["verdict"] == "recorded"
    ]
    assert recorded == [(199, "#938")]


def test_the_sharp_controls_meet_the_grid_contacts_and_refuse_1e30_past_them() -> None:
    """The least gap is 0, between two squares of the L's top row, so the at-contact control
    moves them by nothing and only its 1e-30 half is a mutant, as at the 293 L strip."""
    record = _json(reports.packet_path(PACKET) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (199, PACKET, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)
    closed = {
        row["where"]: row["detail"]
        for row in record["controls"]
        if row["control"] == "tightest-pair-closed-past-contact"
    }
    assert {closed["at-contact"]["square"], closed["at-contact"]["partner"]} <= set(
        range(173, 187)
    )
    assert closed["at-contact"]["moved_by"] == "0"
    assert closed["past-contact"]["moved_by"] == str(kernel.SHARP_EPSILON)


def test_the_contraction_margins_the_notes_cite() -> None:
    """T-127 loses 1.46e-19 to uniform contraction; this certificate loses nothing."""
    measure = reports.packet_path(PACKET) / "measure"
    house = _json(measure / "contraction-n199.json")
    assert (house["certificate"]["label"], house["one_minus_lambda_star"]) == (
        "T-127",
        "1.000000e-20",
    )
    assert house["margin_float"] == "1.461757e-19"
    assert (house["against"]["gain_float"], house["against"]["within_margin"]) == (
        "2.882320e-03",
        False,
    )
    own = _json(measure / "contraction-n199-own.json")
    assert (own["lambda_star"], own["margin"], own["routes_accept"]) == ("1", "0", True)


def test_the_identity_measurement_the_notes_cite() -> None:
    record = _json(reports.packet_path(PACKET) / "measure/identity.json")
    assert record["n"] == 199
    pair = record["pairs"][0]
    assert (pair["view"], pair["against"]) == ("OZDEN", "T-127")
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["moved_beyond"]["1e-1"] == 81
    assert (
        record["tilts"]["OZDEN"]["tilted_beyond_1_degree"],
        record["tilts"]["T-127"]["tilted_beyond_1_degree"],
    ) == (49, 47)


def test_the_scan_shifts_an_algebraic_side_by_one_exactly() -> None:
    """9 + 4 sqrt(2) is the root of s^2 - 18 s + 49 in (14, 15); one more is the root of
    s^2 - 20 s + 68 in (15, 16)."""
    side = exact_sides.algebraic([1, -18, 49], [Fraction(14), Fraction(15)])
    stepped = scan.plus_one(side)
    assert isinstance(stepped, exact_sides.Algebraic)
    assert stepped.polynomial == (1, -20, 68)
    assert (stepped.low, stepped.high) == (15, 16)
    assert stepped == exact_sides.algebraic([1, -20, 68], [Fraction(15), Fraction(16)])
    assert (scan.floor(side), scan.floor(stepped)) == (14, 15)
    assert scan.plus_one(Fraction(7, 2)) == Fraction(9, 2)


def test_the_scan_decides_each_step_on_stand_in_ceilings(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ceilings = {1: Fraction(1), 2: Fraction(2), 3: Fraction(3), 4: Fraction(5, 2)}

    def load(n: int) -> houses.Case:
        return houses.Case(n, ceilings[n], ceilings[n], "", ())

    monkeypatch.setattr(houses, "load_case", load)
    found = scan.scan(range(1, 5), {})
    # The L step from 1 lands at 1 + 2 + 1 = 4 at side 2, below its ceiling of 5/2, and
    # monotonicity carries 4's 5/2 down to 3.
    assert [
        (row["n"], row["from"], row["same_print"]) for row in found["l_step"]["improves"]
    ] == [(4, 1, False)]
    assert [(row["n"], row["from"]) for row in found["monotonicity"]["improves"]] == [(3, 4)]
    adopted = scan.scan(range(1, 5), {4: Fraction(2)})
    assert adopted["replaced"] == {"4": "5/2"}
    assert adopted["l_step"]["improves"] == []
    assert adopted["l_step"]["extensions"] == [{"n": 4, "from": 1}]
    with pytest.raises(scan.ScanError):
        scan.scan(range(1, 5), {5: Fraction(1)})
    # A candidate at a count whose ceiling is unread is refused, not ignored.
    monkeypatch.setattr(
        houses,
        "load_case",
        lambda n: houses.Case(
            n, ceilings[n], ceilings[n], "", (), "stand-in" if n == 3 else None
        ),
    )
    assert scan.scan(range(1, 5), {})["unread"] == {"3": "stand-in"}
    with pytest.raises(scan.ScanError, match="unread"):
        scan.scan(range(1, 5), {3: Fraction(1)})


def test_the_retained_scans_find_only_199_across_its_print() -> None:
    """On main 200f2ebc1 the L step from T-282 at 172 is the one consequence that crosses
    its count's 12-place print; once this side stands at 199 there is none, and 199 is an
    L-extension of 172."""
    side = _certificate(PACKET, 199).side
    measure = reports.packet_path(PACKET) / "measure"
    record = _json(measure / "l-step-scan.json")
    across = [row for row in record["l_step"]["improves"] if not row["same_print"]]
    assert [(row["n"], row["from"]) for row in across] == [(199, 172)]
    assert Fraction(across[0]["bound"]) == side
    assert record["monotonicity"]["improves"] == []
    adopted = _json(measure / "l-step-scan-adopted.json")
    assert Fraction(adopted["with"]["199"]) == side
    assert all(row["same_print"] for row in adopted["l_step"]["improves"])
    assert {"n": 199, "from": 172} in adopted["l_step"]["extensions"]
    assert adopted["monotonicity"]["improves"] == []
