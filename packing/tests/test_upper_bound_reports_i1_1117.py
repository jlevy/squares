"""The upper-bound imports of the intake pass's lane c-import-1005-1117 of 17 November 2026.

Bead think-qag8. Three packets, one per pinned revision: Doğa Özden's corner Witness/v2 at
292 (#1005, ``witness-corners``), made by this repository's ``packing-witness promote``;
Joost de Winter's centre-direction JSON at 292 (#1006), filed 11 minutes 38 seconds later
and below it; and his centre-direction JSON at 262 and 295 (#1007), whose 295 house is
T-193's algebraic side, (22 + 22√2)/3. The general importer's checks run on the packets
through ``test_upper_bound_reports``; these hold what is particular to them: the digests the
sources list, each print against its exact side, the house each is compared with and the
gain, the order of the two reports at 292 and the ledger's verdicts, the retained sharp
controls, the identity measurements, the contraction margins and the L-step scan the
register's notes cite. Every test reads the packets and the ledger only; none needs the
network.
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

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-1005-1007-20261117"
OZDEN = "ozden-s292-upper-bound-2026-11-16"
DE_WINTER_292 = "de-winter-s292-upper-bound-2026-11-16"
DE_WINTER_262_295 = "de-winter-upper-bounds-262-295-2026-11-16"
#: Each packet's issue, its counts, the side the issue prints at each (its exact side
#: rounded up at 12 places), and the SHA-256 the source lists for each certificate.
PACKETS: dict[str, tuple[int, dict[int, str], dict[int, str]]] = {
    OZDEN: (
        1005,
        {292: "17.590104218682"},
        {292: "90a0e30681821da567835ce1c9e81cf52aa899985587a953eafa0701b1829a8a"},
    ),
    DE_WINTER_292: (
        1006,
        {292: "17.590016442847"},
        {292: "3d6fb90c9b79bc9dee984ec0e4b6ecc89bb1306afb266d0b75dcecea4a972b4a"},
    ),
    DE_WINTER_262_295: (
        1007,
        {262: "16.699693441904", 295: "17.699693441716"},
        {
            262: "95875def0a2784e980ff92cacbe0508d84cc1ee03d6104130d9db4007a0ffa04",
            295: "9a0b4bc14803a43fb46e0370a3ad25faaa5a1f7f47186248455c90fae91b13a0",
        },
    ),
}
#: Where each certificate lives in its packet's source tree.
PATHS = {
    (OZDEN, 292): "n-292-candidate.yaml",
    (DE_WINTER_292, 292): "n292/n292_exact.json",
    (DE_WINTER_262_295, 262): "n262/n262_exact.json",
    (DE_WINTER_262_295, 295): "n295/n295_exact.json",
}
#: Each count's house when the lane read main f9ddfeeef: its result and the gain each
#: certificate makes on it, at four significant figures.
GAINS = {
    (OZDEN, 292): ("T-146", "1.2739e-03"),
    (DE_WINTER_292, 292): ("T-146", "1.3617e-03"),
    (DE_WINTER_262_295, 262): ("T-155", "7.4133e-03"),
    (DE_WINTER_262_295, 295): ("T-193", "4.5393e-03"),
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _side(name: str, n: int) -> Fraction:
    return reports.read_facts(reports.packet_path(name), {n})[n].side


def _claims(name: str) -> dict[int, dict[str, Any]]:
    record = reports.check_claims(reports.packet_path(name))
    return {row["n"]: row for row in record["results"]}


@pytest.mark.parametrize("name", PACKETS)
def test_each_packet_holds_the_files_whose_digests_the_source_lists(name: str) -> None:
    _issue, _printed, listed = PACKETS[name]
    text = (reports.packet_path(name) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    manifest = {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }
    for n, digest in listed.items():
        assert manifest[PATHS[name, n]] == digest


@pytest.mark.parametrize("name", PACKETS)
def test_each_print_is_its_exact_side_rounded_up(name: str) -> None:
    issue, printed, _listed = PACKETS[name]
    declaration = reports.load_declaration(reports.packet_path(name))
    assert declaration["issue"].endswith(f"/issues/{issue}")
    assert declaration["requested"] == declaration["replayed"] == list(printed)
    rows = {row["n"]: row for row in declaration["certificates"]}
    for n, shown in printed.items():
        assert rows[n]["offered"] == shown
        side = _side(name, n)
        exact = Decimal(side.numerator) / Decimal(side.denominator)
        assert exact != Decimal(shown)
        assert str(exact.quantize(Decimal("1e-12"), rounding=ROUND_CEILING)) == shown


def test_de_winters_sides_are_the_fractions_his_issues_print() -> None:
    assert _side(DE_WINTER_292, 292) == Fraction(
        33872522175917279266554668306659248043633029180856810473,
        1925667453806884053962316529711800854170000000000000000,
    )
    assert _side(DE_WINTER_262_295, 262) == Fraction(166996934419035177, 10**16)
    assert _side(DE_WINTER_262_295, 295) == Fraction(35399386883430443, 2 * 10**15)


def test_the_295_is_not_the_262_with_one_l_step() -> None:
    """#1007 says the 295 packing is the 262 one with an L of 33 axis-aligned squares, its
    side larger by exactly 1. The certificates' sides differ by 1 less 1.883e-10, so the
    295 certificate lies below the L step on the 262 one and is no such step on it."""
    gap = _side(DE_WINTER_262_295, 262) + 1 - _side(DE_WINTER_262_295, 295)
    assert gap == Fraction(1882962, 10**16)


@pytest.mark.parametrize(("name", "n"), GAINS)
def test_each_certificate_is_below_its_house_by_the_gain(name: str, n: int) -> None:
    result, gain = GAINS[name, n]
    row = _claims(name)[n]
    case = row["case"]
    assert (row["smallest"], case["relation"]) == (reports.THIS, "below")
    assert case["result"] == result
    assert f"{float(Fraction(case['difference'])):.4e}" == gain


def test_295s_house_is_t193s_algebraic_side() -> None:
    case = _claims(DE_WINTER_262_295)[295]["case"]
    assert case["algebraic"] == "evand-exact-cur-2026-10-16"
    low, high = (Fraction(value) for value in case["difference_bounds"])
    assert 0 < low <= Fraction(case["difference"]) <= high
    assert (high - low) * 10**6 <= low


def test_de_winters_292_is_below_ozdens_and_t193s() -> None:
    """Özden's #1005 came first, 11 minutes 38 seconds before #1006; de Winter's claim
    record holds it as a pending report, read from its packet, and T-193's 292 print."""
    pending = {item["report"]: item for item in _claims(DE_WINTER_292)[292]["pending"]}
    assert set(pending) == {"#1005", "T-193 (#639)"}
    assert pending["#1005"]["relation"] == pending["T-193 (#639)"]["relation"] == "below"
    assert Fraction(pending["#1005"]["difference"]) == _side(OZDEN, 292) - _side(
        DE_WINTER_292, 292
    )
    assert [item["report"] for item in _claims(OZDEN)[292]["pending"]] == ["T-193 (#639)"]


def test_the_ledger_records_both_292_reports_in_order_and_262_and_295() -> None:
    ledger = _json(LEDGER / "ledger.json")
    walked = {
        count["n"]: [(claim["report"], claim["verdict"]) for claim in count["steps"]]
        for count in ledger["counts"]
    }
    assert walked == {
        262: [("#1007", "recorded")],
        292: [("#1005", "recorded"), ("#1006", "recorded")],
        295: [("#1007", "recorded")],
    }
    for count in ledger["counts"]:
        for claim in count["steps"]:
            assert claim["packing"]["kind"] == "new packing"


@pytest.mark.parametrize(("name", "n"), GAINS)
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(
    name: str, n: int
) -> None:
    """Squares touch the box in every certificate, so the side is lowered by 0, the
    near-wall move is 0 and the enlargement to a wall grows a touching square by 0:
    accepted at contact and refused past it for the wall and its shape, the branch the
    plan stated. No pair touches, so the enlarged pair square is refused at contact for
    its shape alone."""
    _issue, printed, _listed = PACKETS[name]
    record = _json(sharp.receipt_path(reports.packet_path(name), list(printed), n))
    assert (record["n"], record["packet"], record["all_as_expected"]) == (n, name, True)
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


#: The receipt of each identity measurement, the packing it is measured against, and the
#: squares the optimal assignment moves beyond a tenth.
IDENTITY = {
    (OZDEN, "identity.json", "T-146"): 81,
    (DE_WINTER_292, "identity.json", "T-146"): 69,
    (DE_WINTER_292, "identity.json", "OZDEN-1005"): 44,
    (DE_WINTER_262_295, "identity-n262.json", "T-155"): 78,
    (DE_WINTER_262_295, "identity-n295.json", "T-146"): 209,
}


@pytest.mark.parametrize(("name", "receipt", "against"), IDENTITY)
def test_the_identity_measurements_the_notes_cite(
    name: str, receipt: str, against: str
) -> None:
    """No symmetry pairs any certificate one to one with its house's packing, or de
    Winter's 292 with Özden's, by nearest centres: each is a new arrangement relative to
    the record's packings and to the other."""
    record = _json(reports.packet_path(name) / "measure" / receipt)
    pairs = {pair["against"]: pair for pair in record["pairs"]}
    pair = pairs[against]
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["moved_beyond"]["1e-1"] == IDENTITY[name, receipt, against]
    if against == "T-146" and "house-witness" in pairs:
        assert pairs["house-witness"]["assignment"] == pair["assignment"]


#: Each contraction receipt the notes cite: the certificate contracted, the margin's
#: binding pair, and, against a later certificate, its label.
CONTRACTIONS = {
    (OZDEN, "contraction-n292.json"): ("T-146", [68, 69], "ozden-1005"),
    (OZDEN, "contraction-n292-own.json"): ("ozden-1005", [154, 155], None),
    (DE_WINTER_292, "contraction-n292.json"): ("T-146", [68, 69], "de-winter-1006"),
    (DE_WINTER_292, "contraction-n292-1005.json"): ("ozden-1005", [154, 155], "de-winter-1006"),
    (DE_WINTER_292, "contraction-n292-own.json"): ("de-winter-1006", [278, 279], None),
    (DE_WINTER_262_295, "contraction-n262.json"): ("T-155", [244, 245], "de-winter-1007"),
    (DE_WINTER_262_295, "contraction-n262-own.json"): ("de-winter-1007", [33, 179], None),
    (DE_WINTER_262_295, "contraction-n295.json"): ("T-146", [206, 220], "de-winter-1007"),
    (DE_WINTER_262_295, "contraction-n295-own.json"): ("de-winter-1007", [55, 56], None),
}


@pytest.mark.parametrize(("name", "receipt"), CONTRACTIONS)
def test_each_gain_lies_wholly_outside_the_padding_it_is_measured_against(
    name: str, receipt: str
) -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. Each
    house's margin is below 2e-19 and the step from #1005 to #1006 is about 2.6e7 times
    #1005's own margin; each certificate's own margin is below 1e-10, and the side it
    would contract to is not a bound anyone reported."""
    label, pair, later = CONTRACTIONS[name, receipt]
    record = _json(reports.packet_path(name) / "measure" / receipt)
    assert (record["certificate"]["label"], record["binding_pair"]) == (label, pair)
    assert record["routes_accept"] is True
    margin = Fraction(record["margin"])
    if later is None:
        assert 0 < margin < Fraction(1, 10**10)
        assert "against" not in record
        return
    assert record["against"]["certificate"]["label"] == later
    assert record["against"]["within_margin"] is False
    assert Fraction(record["against"]["gain"]) > 10**7 * margin


@pytest.mark.parametrize("name", PACKETS)
def test_the_l_step_scan_stands_the_sides_in_and_carries_them_nowhere(name: str) -> None:
    _issue, printed, _listed = PACKETS[name]
    record = _json(reports.packet_path(name) / "measure/l-step-scan.json")
    sides = {n: _side(name, n) for n in printed}
    assert {int(n): Fraction(side) for n, side in record["with"].items()} == sides
    steps = record["l_step"]["improves"] + record["l_step"]["extensions"]
    assert not [row for row in steps if row["n"] in sides or row["from"] in sides]
    assert record["monotonicity"]["improves"] == []
