"""The upper-bound imports of the intake pass's lane w6-dewinter-1118 of 18 November 2026.

Bead think-zqot. Three packets, one per pinned revision of Joost de Winter's watched
repository, each a centre-direction JSON at 127 (``center-direction-json``): #1015's at
35b576a, #1017's at cc20a26, 1.9556e-6 smaller, and #1020's at a1ba501, 1.7976e-13 smaller
still, all filed on the evening of 17 November. The general importer's checks run on the
packets through ``test_upper_bound_reports``; these hold what is particular to them: the
digests the sources list, each print against its exact side, the house each is compared
with and the earlier reports, the ledger's verdicts in report order, the retained sharp
controls, the identity measurements, the contraction margins on which the owner's option D
of 17 November (think-b0w5) decides each step a new result, and the L-step scan. Every test
reads the packets and the ledger only; none needs the network.
"""

from __future__ import annotations

import json
from decimal import ROUND_CEILING, Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-1015-1020-20261118"
P1015 = "de-winter-s127-issue1015-2026-11-17"
P1017 = "de-winter-s127-issue1017-2026-11-17"
P1020 = "de-winter-s127-issue1020-2026-11-17"
#: Each packet's issue, the side the issue prints (its exact side rounded up at 12
#: places), the SHA-256 the source lists for the certificate (at the pin for #1015, in
#: the next commit's SHA256SUMS for #1017 and #1020), and the earlier reports it holds as
#: pending.
PACKETS: dict[str, tuple[int, str, str, tuple[str, ...]]] = {
    P1015: (
        1015,
        "11.800795682214",
        "a4c9beb8b7b656072fa60150c70d2ea685907bc0e10e19e77963464c0f946772",
        (),
    ),
    P1017: (
        1017,
        "11.800793726616",
        "bb883631dc01343198a07826d2a84faf029789b13beb88403478db736ac27c9b",
        ("#1015",),
    ),
    P1020: (
        1020,
        "11.800793726615",
        "3a66f38276be9e986fc46fa1f859de54754ec77fc4694b3442de58381056a835",
        ("#1015", "#1017"),
    ),
}
#: The gain on T-305, the house when the lane read main eb50f54e9, at four figures.
GAINS = {P1015: "9.5821e-04", P1017: "9.6016e-04", P1020: "9.6016e-04"}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _side(name: str) -> Fraction:
    return reports.read_facts(reports.packet_path(name), {127})[127].side


def _claim(name: str) -> dict[str, Any]:
    (row,) = reports.check_claims(reports.packet_path(name))["results"]
    return row


@pytest.mark.parametrize("name", PACKETS)
def test_each_packet_holds_the_certificate_whose_digest_the_source_lists(name: str) -> None:
    text = (reports.packet_path(name) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    manifest = {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }
    assert manifest["n127/n127_exact.json"] == PACKETS[name][2]


@pytest.mark.parametrize("name", PACKETS)
def test_each_print_is_its_exact_side_rounded_up(name: str) -> None:
    issue, shown, _digest, _pending = PACKETS[name]
    declaration = reports.load_declaration(reports.packet_path(name))
    assert declaration["issue"].endswith(f"/issues/{issue}")
    assert declaration["requested"] == declaration["replayed"] == [127]
    (row,) = declaration["certificates"]
    assert row["offered"] == shown
    side = _side(name)
    exact = Decimal(side.numerator) / Decimal(side.denominator)
    assert exact != Decimal(shown)
    assert str(exact.quantize(Decimal("1e-12"), rounding=ROUND_CEILING)) == shown


def test_1017s_side_is_the_fraction_its_issue_states() -> None:
    assert _side(P1017) == Fraction(5900396863307571, 500000000000000)


def test_the_three_sides_fall_in_report_order() -> None:
    """Each later certificate is below the one before: by 1.9556e-6, then by 1.7976e-13,
    and the two prints of #1017 and #1020 differ in the 12th place."""
    s1015, s1017, s1020 = (_side(name) for name in PACKETS)
    assert s1015 > s1017 > s1020
    assert f"{float(s1015 - s1017):.4e}" == "1.9556e-06"
    assert f"{float(s1017 - s1020):.4e}" == "1.7976e-13"


@pytest.mark.parametrize("name", PACKETS)
def test_each_certificate_is_below_t305_and_the_earlier_reports(name: str) -> None:
    row = _claim(name)
    case = row["case"]
    assert (row["smallest"], case["relation"], case["result"]) == (
        reports.THIS,
        "below",
        "T-305",
    )
    assert f"{float(Fraction(case['difference'])):.4e}" == GAINS[name]
    pending = {item["report"]: item for item in row["pending"]}
    assert tuple(pending) == PACKETS[name][3]
    for report, item in pending.items():
        assert item["relation"] == "below"
        earlier = next(packet for packet, value in PACKETS.items() if f"#{value[0]}" == report)
        assert Fraction(item["difference"]) == _side(earlier) - _side(name)


def test_the_ledger_records_all_three_reports_in_order() -> None:
    ledger = _json(LEDGER / "ledger.json")
    (count,) = ledger["counts"]
    assert count["n"] == 127
    assert [(claim["report"], claim["verdict"]) for claim in count["steps"]] == [
        ("#1015", "recorded"),
        ("#1017", "recorded"),
        ("#1020", "recorded"),
    ]
    for claim in count["steps"]:
        assert claim["packing"]["kind"] == "new packing"


#: #1020's least wall clearance. #1017's squares touch the box, while #1015's and #1020's
#: clear every wall, so their near-wall move and wall enlargement take the branch of a
#: clearing square, which the plan did not expect and whose verdicts are the ones it stated.
CLEARANCE_1020 = Fraction(1, 5 * 10**59)


@pytest.mark.parametrize("name", PACKETS)
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(name: str) -> None:
    record = _json(sharp.receipt_path(reports.packet_path(name), [127], 127))
    assert (record["n"], record["packet"], record["all_as_expected"]) == (127, name, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    assert len(record["controls"]) == 11
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)
    near = [row for row in record["controls"] if row["control"] == sharp.NEAR_WALL]
    moved = Fraction(near[0]["detail"]["moved_by"])
    wall = [row for row in record["controls"] if row["control"] == sharp.ENLARGED_WALL]
    if name == P1017:
        assert moved == 0
        assert Fraction(wall[0]["detail"]["wall_clearance"]) == 0
        assert wall[0]["expected"] == "accepted"
    else:
        assert moved > 0
        assert Fraction(wall[0]["detail"]["wall_clearance"]) > 0
        assert (wall[0]["expected"], wall[0]["expected_failures"]) == ("refused", ["shape"])
    if name == P1020:
        assert moved == CLEARANCE_1020
    assert [(row["expected"], row["expected_failures"]) for row in wall][1] == (
        "refused",
        ["container", "shape"],
    )


#: Each identity measurement the notes cite: the packing it is measured against, whether
#: nearest centres pair the two one to one, and the squares the optimal assignment moves
#: beyond a tenth.
IDENTITY = {
    (P1015, "T-305"): (False, 10),
    (P1015, "house-witness"): (False, 10),
    (P1017, "T-305"): (False, 11),
    (P1017, "DEWINTER-1015"): (True, 5),
    (P1020, "T-305"): (False, 9),
    (P1020, "DEWINTER-1017"): (True, 1),
    (P1020, "DEWINTER-1015"): (True, 5),
}


@pytest.mark.parametrize(("name", "against"), IDENTITY)
def test_the_identity_measurements_the_notes_cite(name: str, against: str) -> None:
    """No symmetry pairs any of the three one to one with T-305's packing; #1017's is
    #1015's arrangement moved and #1020's is #1017's, one to one under the identity."""
    record = _json(reports.packet_path(name) / "measure/identity.json")
    pair = {pair["against"]: pair for pair in record["pairs"]}[against]
    one_to_one, beyond = IDENTITY[name, against]
    assert pair["nearest_centre"]["one_to_one"] is one_to_one
    assert pair["assignment"]["symmetry"] == 0
    assert pair["assignment"]["moved_beyond"]["1e-1"] == beyond


#: Each contraction receipt: the certificate contracted, its binding pair, the margin at
#: four figures, and, against a later certificate, its label and the gain over the margin.
CONTRACTIONS = {
    (P1015, "contraction-n127.json"): ("T-305", [89, 93], "1.2099e-10", "DEWINTER-1015"),
    (P1015, "contraction-n127-own.json"): ("DEWINTER-1015", [31, 34], "7.7394e-63", None),
    (P1017, "contraction-n127.json"): ("T-305", [89, 93], "1.2099e-10", "DEWINTER-1017"),
    (P1017, "contraction-n127-1015.json"): (
        "DEWINTER-1015",
        [31, 34],
        "7.7394e-63",
        "DEWINTER-1017",
    ),
    (P1017, "contraction-n127-own.json"): ("DEWINTER-1017", [35, 88], "4.1903e-14", None),
    (P1020, "contraction-n127.json"): ("T-305", [89, 93], "1.2099e-10", "DEWINTER-1020"),
    (P1020, "contraction-n127-1017.json"): (
        "DEWINTER-1017",
        [35, 88],
        "4.1903e-14",
        "DEWINTER-1020",
    ),
    (P1020, "contraction-n127-own.json"): ("DEWINTER-1020", [84, 99], "1.8203e-58", None),
}


@pytest.mark.parametrize(("name", "receipt"), CONTRACTIONS)
def test_each_step_lies_outside_the_padding_option_d_measures_it_against(
    name: str, receipt: str
) -> None:
    """Option D (think-b0w5): a re-certification is a new result only if its side is below
    its predecessor shrunk to first contact. Every step here is: #1020's over #1017's, the
    narrowest, by 4.29 times #1017's margin."""
    label, pair, margin, later = CONTRACTIONS[name, receipt]
    record = _json(reports.packet_path(name) / "measure" / receipt)
    assert (record["certificate"]["label"], record["binding_pair"]) == (label, pair)
    assert record["routes_accept"] is True
    assert f"{float(Fraction(record['margin'])):.4e}" == margin
    if later is None:
        assert "against" not in record
        return
    against = record["against"]
    assert against["certificate"]["label"] == later
    assert against["within_margin"] is False
    assert Fraction(against["gain"]) > Fraction(record["margin"])
    if receipt == "contraction-n127-1017.json":
        assert f"{float(Fraction(against['gain_over_margin'])):.3f}" == "4.290"


@pytest.mark.parametrize("name", PACKETS)
def test_the_l_step_scan_stands_the_side_in_and_carries_it_nowhere(name: str) -> None:
    record = _json(reports.packet_path(name) / "measure/l-step-scan.json")
    assert {int(n): Fraction(side) for n, side in record["with"].items()} == {127: _side(name)}
    steps = record["l_step"]["improves"] + record["l_step"]["extensions"]
    assert not [row for row in steps if 127 in (row["n"], row["from"])]
    assert record["monotonicity"]["improves"] == []
