"""The upper-bound imports of the intake pass's lane L164 of 14 November 2026 (think-17ex).

Two packets of one source, Roberto Ono's RobertoOno/squares-in-square at b5636fd, read by
the ``ono-json`` adapter with each certificate's text copy held to the same packing by the
``evand-cert`` reader: #984 at 228, five band periods cut from Francisco Couzo's 404,
below T-300 (Doğa Özden's column-band packing, the house at 228 since that day's earlier
pass), and #985 at 147, one period cut from Evan Daniel's 229, below the Kingbird
catalogue's 7 + 4 sqrt(2), which T-155's exact ceiling verifies. Each issue prints its side
rounded up at 12 places. The general importer's checks run on the packets through
``test_upper_bound_reports``; these hold what is particular to them: the adapter, the
digests the issues print, the prints against the exact sides, the houses they are compared
with and the improvements the issues state, the side-only leaderboard entries they
disclose, the ledger's verdicts, the retained sharp controls, the identity measurements,
the contraction margins and the L-step scans the register's notes cite. Every test reads
the packets and the ledger only; none needs the network.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, NamedTuple

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-984-985-20261114"
RUN = "runs/2026-11-11_fable-5.2"


class Import(NamedTuple):
    """One issue's packet, and what its issue prints and the measurements found."""

    name: str
    issue: int
    n: int
    certificate: str
    #: The 12-place print, and the 30 places the issue prints before an ellipsis, a floor.
    printed: str
    printed_30: str
    #: The house the claim record compares with: the reader that rebuilds its side, the
    #: source key the case prints and its register entry.
    house: str
    house_key: str
    result: str
    #: The improvement the issue states, the exact gap's floor at its places.
    gain: str
    #: The SHA-256 the issue prints: the JSON, the text copy and the strict copy.
    digests: tuple[str, str, str]
    #: The side-only leaderboard entries the issue discloses first, and how far below the
    #: side each lies, as the issue rounds it.
    leaderboard: tuple[tuple[str, str], ...]
    #: The sharp controls' least-gap pair (moved square, partner) and wall square.
    pair: tuple[int, int]
    wall: int
    #: The certificate's own contraction margin's binding pair.
    own_binding: tuple[int, int]


ONO_984 = Import(
    name="ono-issue984-2026-11-14",
    issue=984,
    n=228,
    certificate="n228_S59604312.json",
    printed="15.596043120921",
    printed_30="15.596043120920791646977220704185",
    house="[Özden s228 upper bound 2026-11-14]",
    house_key="[Özden s228 upper bound 2026-11-14]",
    result="T-300",
    gain="0.004758613890",
    digests=(
        "98987101c5a14e84cc1bdcb7497cc139be6ef71a17f7e7ec9ce3f89c80274944",
        "be120af6c2fc1e7b6a56deb8a3cee31e2abc4606be98ecfcfebcc889ab51e3f4",
        "e243de776d011ab24f6221df42bbf6fc55de33c9c7612b92a2008777cff48569",
    ),
    leaderboard=(
        ("15.596043116631669919627353", "4.289e-09"),
        ("15.596043116646272293906688", "4.275e-09"),
    ),
    pair=(21, 8),
    wall=22,
    own_binding=(8, 21),
)
ONO_985 = Import(
    name="ono-issue985-2026-11-14",
    issue=985,
    n=147,
    certificate="n147_S65104355.json",
    printed="12.651043556588",
    printed_30="12.651043556587694471904370629016",
    house="[Daniel regularizer 2026-10-11]",
    house_key="[Kingbird]",
    result="T-155",
    gain="0.005810692904685",
    digests=(
        "fce8c8c20bf3812173c76c6a2c1295541a72b23a9c948bdf380cc905d2038135",
        "0e09260712370f6561df1e9c0c835adc04f7d9f49ad40ad0e603c6c6a8cc11af",
        "cfe0079654a433e4cb2739405f9d523c5557f7182618bc8fb33b656999a7a6ce",
    ),
    leaderboard=(("12.651043553172632772258400", "3.415e-09"),),
    pair=(108, 101),
    wall=3,
    own_binding=(145, 147),
)
IMPORTS = (ONO_984, ONO_985)
#: The issue's improvement at 228 against T-174, the house before T-300, which it names.
T174 = "[PingYou PR 574 certificates 2026-10-13]"
T174_GAIN = "0.008558354808882"


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest(item: Import) -> dict[str, str]:
    text = (reports.packet_path(item.name) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split(maxsplit=1) for line in text.splitlines())
    }


def _up(side: Fraction, places: int) -> Fraction:
    return Fraction(math.ceil(side * 10**places), 10**places)


def _down(value: Fraction, places: int) -> Fraction:
    return Fraction(math.floor(value * 10**places), 10**places)


def _side(item: Import) -> Fraction:
    return reports.read_facts(reports.packet_path(item.name))[item.n].side


def test_the_adapter_reads_centres_and_half_angles_and_refuses_unknown_fields() -> None:
    raw = (
        b'{"n": 1, "side": "1", "side_decimal_info_only": "1", '
        b'"squares": [{"cx": "1/2", "cy": "1/2", "t": "0"}]}'
    )
    certificate = reports.parse_certificate(raw, 1, "ono-json")
    assert certificate.side == 1
    assert (certificate.poses[0].x, certificate.poses[0].y) == (Fraction(1, 2), Fraction(1, 2))
    # The strict copies carry no display field; any other field, or a number in place of a
    # rational string, is refused.
    assert (
        reports.parse_certificate(
            raw.replace(b' "side_decimal_info_only": "1",', b""), 1, "ono-json"
        )
        == certificate
    )
    for bad in (
        raw.replace(b'"side": "1"', b'"side": 1'),
        raw.replace(b'"t": "0"', b'"t": "0", "u": "0"'),
        raw.replace(b'"n": 1,', b'"n": 1, "note": "",'),
    ):
        with pytest.raises(reports.ReportError):
            reports.parse_certificate(bad, 1, "ono-json")
    with pytest.raises(reports.ReportError):
        reports.parse_certificate(raw, 1, "ono-json", {"dilation": "1"})


@pytest.mark.parametrize("item", IMPORTS, ids=lambda item: item.name)
def test_the_packet_holds_the_files_whose_digests_the_issue_prints(item: Import) -> None:
    manifest = _manifest(item)
    certificate, text, strict = item.digests
    registration = f"{RUN}/evidence/registration/n{item.n}"
    assert manifest[f"{RUN}/certificates/{item.certificate}"] == certificate
    assert manifest[f"{registration}.cert"] == text
    assert manifest[f"{registration}.strict.cert"] == strict


@pytest.mark.parametrize("item", IMPORTS, ids=lambda item: item.name)
def test_the_print_is_its_exact_side_rounded_up_and_its_text_copy_agrees(item: Import) -> None:
    """The issue's 12-place print is the side rounded up and its 30 places the side's floor
    before an ellipsis; the text copy states the same packing as the JSON (the declaration's
    ``same_packing``, which ``read_facts`` holds)."""
    declaration = reports.load_declaration(reports.packet_path(item.name))
    assert declaration["source_key"] == f"[Ono issue {item.issue} 2026-11-14]"
    assert declaration["issue"].endswith(f"/issues/{item.issue}")
    assert (declaration["requested"], declaration["replayed"]) == ([item.n], [item.n])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (item.n, "ono-json", item.printed)
    assert [(other["path"], other["format"]) for other in row.get("same_packing", [])] == [
        (f"{RUN}/evidence/registration/n{item.n}.cert", "evand-cert")
    ]
    side = _side(item)
    assert _up(side, 12) == Fraction(Decimal(item.printed))
    assert _down(side, 30) == Fraction(Decimal(item.printed_30))
    assert reports.house_side(declaration["source_key"], item.n) == side


@pytest.mark.parametrize("item", IMPORTS, ids=lambda item: item.name)
def test_the_certificate_is_below_the_house_by_the_improvement_stated(item: Import) -> None:
    side = _side(item)
    difference = reports.house_side(item.house, item.n) - side
    assert difference > 0
    assert _down(difference, len(item.gain) - 2) == Fraction(Decimal(item.gain))
    (row,) = reports.check_claims(reports.packet_path(item.name))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (
        item.n,
        reports.THIS,
        "below",
    )
    assert (row["case"]["source_key"], row["case"]["result"]) == (item.house_key, item.result)
    assert Fraction(row["case"]["difference"]) == difference
    assert row["pending"] == []
    # The leaderboard's side-only entries are below the side, as the issue says first: they
    # state no packing, so they are context only.
    for entry, below in item.leaderboard:
        assert f"{float(side - Fraction(Decimal(entry))):.3e}" == below


def test_the_228_improvement_on_t174_is_the_one_the_issue_states() -> None:
    gain = reports.house_side(T174, 228) - _side(ONO_984)
    assert _down(gain, 15) == Fraction(Decimal(T174_GAIN))


def test_the_ledger_records_each_claim_as_a_new_packing() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
                assert claim["packing"] == {"kind": "new packing"}
    assert recorded == {item.n: [f"#{item.issue}"] for item in IMPORTS}


@pytest.mark.parametrize("item", IMPORTS, ids=lambda item: item.name)
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(item: Import) -> None:
    record = _json(reports.packet_path(item.name) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (
        item.n,
        item.name,
        True,
    )
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    assert len(record["controls"]) == 11
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)
    # No two squares touch, so the tightest pair's enlargement grows its square and is
    # refused at contact for its shape alone; the squares touch the walls, so the wall
    # square grows by 0 and is accepted at contact.
    pair = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.ENLARGED_PAIR and row["where"] == "at-contact"
    )
    assert (pair["expected"], pair["expected_failures"]) == ("refused", [sharp.SHAPE])
    closed = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.TIGHTEST_PAIR and row["where"] == "at-contact"
    )
    assert (closed["detail"]["square"], closed["detail"]["partner"]) == item.pair
    wall = next(
        row
        for row in record["controls"]
        if row["control"] == sharp.ENLARGED_WALL and row["where"] == "at-contact"
    )
    assert (wall["detail"]["square"], wall["detail"]["wall_clearance"]) == (item.wall, "0")
    assert wall["expected"] == "accepted"


def test_the_identity_measurements_the_notes_cite() -> None:
    """At 228 no symmetry pairs the packing one to one with T-300's, T-174's, the house
    witness or the regularized view; the optimal assignment moves 96 squares beyond a tenth
    of T-300's (largest 0.963975) and 89 of T-174's, and 55 squares tilt beyond a degree, 19
    one way and 36 the other. At 147 it is not one to one with T-155's view of the house's
    45-degree packing: 92 squares beyond a tenth, 44 tilted at 25.8 to 27.7 degrees, all one
    way, against the house's 64 at 45 degrees."""
    record = _json(reports.packet_path(ONO_984.name) / "measure/identity.json")
    pairs = {row["against"]: row for row in record["pairs"]}
    assert set(pairs) == {"T-300", "T-174", "regularized", "house-witness"}
    for row in pairs.values():
        assert row["nearest_centre"]["one_to_one"] is False
    assert pairs["T-300"]["assignment"]["moved_beyond"]["1e-1"] == 96
    assert pairs["T-300"]["assignment"]["largest_move"] == "0.963975"
    assert pairs["T-174"]["assignment"]["moved_beyond"]["1e-1"] == 89
    assert pairs["house-witness"]["assignment"] == pairs["T-300"]["assignment"]
    tilts = record["tilts"]["ONO"]
    assert (tilts["tilted_beyond_1_degree"], tilts["tilted_positive"]) == (55, 19)
    record = _json(reports.packet_path(ONO_985.name) / "measure/identity.json")
    (pair,) = record["pairs"]
    assert pair["against"] == "T-155"
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["moved_beyond"]["1e-1"] == 92
    tilts = record["tilts"]
    assert (tilts["ONO"]["tilted_beyond_1_degree"], tilts["ONO"]["tilted_positive"]) == (44, 44)
    assert tilts["T-155"]["tilt_range_degrees"] == [45.0, 45.0]


@pytest.mark.parametrize(
    ("item", "receipt", "label", "margin", "binding"),
    [
        (
            ONO_984,
            "contraction-n228-t300.json",
            "T-300",
            "1474680975215987053/500000000000101000000000000000",
            [118, 119],
        ),
        (ONO_984, "contraction-n228-t174.json", "T-174", "0", [201, 227]),
        (ONO_985, "contraction-n147-t155.json", "T-155", "0", [1, 2]),
    ],
    ids=["228-T-300", "228-T-174", "147-T-155"],
)
def test_the_gain_lies_wholly_outside_the_predecessor_s_contraction_margin(
    item: Import, receipt: str, label: str, margin: str, binding: list[int]
) -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. T-300's
    certificate has 2.949e-12 of padding, which the gain exceeds 1.6e9 times; T-174's and
    T-155's view at 147 have none, a pair touching."""
    record = _json(reports.packet_path(item.name) / "measure" / receipt)
    assert (record["n"], record["certificate"]["label"]) == (item.n, label)
    assert record["routes_accept"] is True
    assert Fraction(record["margin"]) == Fraction(margin)
    assert record["binding_pair"] == binding
    assert record["against"]["within_margin"] is False
    gain = Fraction(record["against"]["gain"])
    assert gain == reports.house_side(T174 if label == "T-174" else item.house, item.n) - _side(
        item
    )
    assert gain > 10**9 * Fraction(margin)


@pytest.mark.parametrize("item", IMPORTS, ids=lambda item: item.name)
def test_the_certificate_s_own_padding_is_a_few_nanometres(item: Import) -> None:
    """Each certificate keeps every pair apart by about 2.4e-10 and 2.6e-10, its harness's
    rounding repair, so its own contraction margin is 3.49e-9 at 228 and 2.93e-9 at 147: the
    side it would contract to, which nobody reported, is RV-3's and is not registered."""
    own = _json(reports.packet_path(item.name) / f"measure/contraction-n{item.n}-own.json")
    assert own["routes_accept"] is True
    assert own["binding_pair"] == list(item.own_binding)
    assert Fraction(1, 10**9) < Fraction(own["margin"]) < Fraction(1, 10**8)


@pytest.mark.parametrize("item", IMPORTS, ids=lambda item: item.name)
def test_the_l_step_scan_stands_the_side_in_and_carries_it_nowhere(item: Import) -> None:
    record = _json(reports.packet_path(item.name) / "measure/l-step-scan.json")
    assert Fraction(record["with"][str(item.n)]) == _side(item)
    assert all(row["from"] != item.n for row in record["l_step"]["improves"])
    assert item.n not in {row["n"] for row in record["l_step"]["improves"]}
    assert record["monotonicity"]["improves"] == []
    # At 147 the house was 124's ceiling plus one, an L extension, which the claim ends.
    extensions = {(row["from"], row["n"]) for row in record["l_step"]["extensions"]}
    assert ((124, 147) in extensions) is (item.n != 147)
