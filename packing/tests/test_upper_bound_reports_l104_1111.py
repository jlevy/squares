"""The upper-bound imports of the intake pass's lane L104 of 11 November 2026 (think-bcfs).

Two packets, each read by the ``witness-center-basis-bare`` adapter: Joost de Winter's
pinwheels at 132 and 157 of #958, in his watched repository JoostdeWinter/square-packing,
first committed at a491dad and pinned at the head 6617869, which the issue names.
Each folder's ``SHA256SUMS`` states the digests of its other five files, and the root
README prints each side rounded up at 12 places. The general importer's checks run on each
packet through ``test_upper_bound_reports``; these hold what is particular to them: the
stated digests, each print against its exact side, the house each is compared with and the
improvement the source states, the ledger's verdicts, the retained sharp controls, the
identity measurements and the contraction margins the register's notes cite. Every test
reads the packets and the ledger only; none needs the network.
"""

from __future__ import annotations

import json
import math
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-de-winter-132-157-20261111"
PIN = "6617869a3491b5872c6ecdff55db05cbee57d516"

#: Each packet with its count, the house it is compared with, that house's register entry
#: (none for the grid), the root README's 12-place print, the improvement the folder's
#: README states and the gain to four significant figures.
PACKETS: dict[str, tuple[int, str, str | None, str, str, str]] = {
    "de-winter-s132-upper-bound-2026-11-11": (
        132,
        "[PingYou PR 574 certificates 2026-10-13]",
        "T-174",
        "11.976048383604",
        "0.0096",
        "9.632e-03",
    ),
    "de-winter-s157-upper-bound-2026-11-11": (
        157,
        "grid",
        None,
        "12.993302611344",
        "0.0067",
        "6.697e-03",
    ),
}
#: Each certificate's side rounded up at 16 places, as its claim record prints it.
CEILINGS = {132: "11.9760483836034076", 157: "12.9933026113432237"}
#: Each certificate's own uniform-contraction margin, which the folder's README states as
#: the side's distance above its 250-digit solution (1.3e-59 and 1.4e-59).
OWN_MARGINS = {132: "1.248e-59", 157: "1.349e-59"}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _name(n: int) -> str:
    return next(name for name, row in PACKETS.items() if row[0] == n)


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


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_folder_s_stated_digests_hold_for_the_files_at_the_pin(name: str) -> None:
    n = PACKETS[name][0]
    record = _json(reports.packet_path(name) / "acquisition/sources.json")
    (source,) = record["sources"]
    assert source["source_commit"] == PIN
    manifest = _manifest(name)
    stated = reports.packet_path(name) / f"source/n{n}/SHA256SUMS"
    rows = [line.split() for line in stated.read_text("utf-8").splitlines()]
    stated_paths = [f"n{n}_exact.json", f"n{n}_witness.yaml", f"n{n}_record.png"]
    assert sorted(path for _digest, path in rows) == sorted(
        [*stated_paths, "verify_exact.py", "README.md"]
    )
    for digest, path in rows:
        assert manifest[f"n{n}/{path}"] == digest


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_print_is_its_exact_side_rounded_up_and_its_reader_rebuilds_it(name: str) -> None:
    """Each 12-place print is the side rounded up, and the JSON states the same packing as
    the witness (the declaration's ``same_packing``, which ``read_facts`` holds)."""
    n, _house, _result, printed, _stated, _gain = PACKETS[name]
    declaration = reports.load_declaration(reports.packet_path(name))
    assert declaration["source_key"] == f"[de Winter s{n} upper bound 2026-11-11]"
    assert declaration["issue"] == "https://github.com/jlevy/squares/issues/958"
    assert (declaration["requested"], declaration["replayed"]) == ([n], [n])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (
        n,
        "witness-center-basis-bare",
        printed,
    )
    assert row["first_committed"] == "2026-11-11T20:49:44Z"
    assert [other["path"] for other in row.get("same_packing", [])] == [f"n{n}/n{n}_exact.json"]
    side = reports.read_facts(reports.packet_path(name))[n].side
    assert _up(side, 12) == Fraction(Decimal(printed))
    assert _up(side, 16) == Fraction(Decimal(CEILINGS[n]))
    assert reports.house_side(declaration["source_key"], n) == side


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_certificate_is_below_its_house_by_the_improvement_the_source_states(
    name: str,
) -> None:
    n, house, result, _printed, stated, gain = PACKETS[name]
    side = reports.read_facts(reports.packet_path(name))[n].side
    difference = reports.house_side(house, n) - side
    assert difference > 0
    assert f"{float(difference):.3e}" == gain
    assert f"{float(difference):.4f}" == stated
    (row,) = reports.check_claims(reports.packet_path(name))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (n, reports.THIS, "below")
    assert row["case"].get("result") == result
    assert Fraction(row["case"]["difference"]) == difference


def test_157_is_below_the_grid_at_k_squared_less_k_plus_one() -> None:
    """157 = 13^2 - 13 + 1: the first packing on record of k^2 - k + 1 squares below k at
    k = 13, where 183 (k = 14, T-220) was the smallest such count before."""
    side = reports.read_facts(reports.packet_path(_name(157)))[157].side
    assert 13**2 - 13 + 1 == 157
    assert side < 13


def test_the_ledger_records_each_claim_as_a_new_packing() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
                assert claim["packing"]["kind"] == "new packing"
    assert recorded == {132: ["#958"], 157: ["#958"]}
    (report,) = ledger["reports"]
    assert (report["reported_at"], report["kind"]) == ("2026-11-11T20:56:18Z", "issue")
    for count in ledger["counts"]:
        (step,) = count["steps"]
        assert step["first_committed"] == "2026-11-11T20:49:44Z"


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(name: str) -> None:
    n = PACKETS[name][0]
    record = _json(reports.packet_path(name) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (n, name, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)


#: Each count's identity measurement against its house: the label it is measured against,
#: the squares the optimal assignment moves beyond a tenth, and the squares tilted beyond a
#: degree in the new packing and in the house's.
IDENTITY: dict[int, tuple[str, int, tuple[int, int]]] = {
    132: ("T-174", 84, (53, 39)),
    157: ("grid", 100, (61, 0)),
}


@pytest.mark.parametrize("n", sorted(IDENTITY))
def test_the_identity_measurement_the_notes_cite(n: int) -> None:
    against, beyond_tenth, tilted = IDENTITY[n]
    record = _json(reports.packet_path(_name(n)) / "measure/identity.json")
    assert record["n"] == n
    pair = record["pairs"][0]
    assert (pair["view"], pair["against"]) == ("DEWINTER", against)
    assert pair["nearest_centre"]["one_to_one"] is False
    assert pair["assignment"]["moved_beyond"]["1e-1"] == beyond_tenth
    tilts = record["tilts"]
    assert (
        tilts["DEWINTER"]["tilted_beyond_1_degree"],
        tilts[against]["tilted_beyond_1_degree"],
    ) == tilted
    for other in record["pairs"][1:]:
        assert other["assignment"]["moved_beyond"] == pair["assignment"]["moved_beyond"]


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_gain_lies_outside_its_predecessor_s_padding(name: str) -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin. T-174's
    margin at 132 is 0, a pair touching, and so is the grid's at 157, so no entry here is
    held for it."""
    n, house, _result, _printed, _stated, _gain = PACKETS[name]
    record = _json(reports.packet_path(name) / f"measure/contraction-n{n}.json")
    assert record["n"] == n
    assert record["routes_accept"] is True
    assert Fraction(record["margin"]) == 0
    assert record["against"]["within_margin"] is False
    side = reports.read_facts(reports.packet_path(name))[n].side
    assert Fraction(record["against"]["gain"]) == reports.house_side(house, n) - side
    own = _json(reports.packet_path(name) / f"measure/contraction-n{n}-own.json")
    assert own["routes_accept"] is True
    assert f"{float(Fraction(own['margin'])):.3e}" == OWN_MARGINS[n]


def test_the_l_step_scan_finds_what_main_finds_but_one_extension() -> None:
    """With both sides stood in, the L step carries neither bound to another count: from 132
    it lands at 155 at S + 1 = 12.976..., above 155's 12.952..., and from 157 at 182 at
    13.993..., above 182's 13.971...; only 184's L-extension from the grid at 157 lapses."""
    scan = _json(reports.packet_path(_name(132)) / "measure/l-step-scan.json")
    assert sorted(scan["with"]) == ["132", "157"]
    landings = {(row["n"], row["from"]) for row in scan["l_step"]["improves"]}
    assert not landings & {(155, 132), (182, 157)}
    assert (184, 157) not in {(row["n"], row["from"]) for row in scan["l_step"]["extensions"]}
    assert scan["monotonicity"]["improves"] == []
