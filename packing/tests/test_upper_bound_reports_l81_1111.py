"""The upper-bound imports of the intake pass's lane L81 of 11 November 2026 (think-3guf).

Four packets, each read by the ``witness-corners`` adapter: Doğa Özden's #943 at 156
(kenaznia-doga/s156-upper-bound 87c9292), #944 at 180 (s180-upper-bound 4cfcb90), #945 at
268 (s268-upper-bound-16872029849 b027aba) and #947 at 269 (s269-upper-bound 6f93b07).
Each witness was promoted to exact rationals by this repository's ``packing-witness
promote --strategy robust-rational`` from a decimal pose the source retains, so its side is
a fraction of about 160 to 220 places, and each issue prints it rounded up at 12 places.
The general importer's checks run on each packet through ``test_upper_bound_reports``;
these hold what is particular to them: the digests the issues and READMEs print, each
print against its exact side, the house each is compared with and the improvement the
issue states, the ledger's verdicts, the retained sharp controls, the identity
measurements and the contraction margins the register's notes cite. Every test reads the
packets and the ledger only; none needs the network.
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

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-943-947-20261111"

#: Each packet with its issue, its count, the house it is compared with, that house's
#: register entry, the issue's 12-place print and the improvement the issue states.
PACKETS: dict[str, tuple[int, int, str, str, str, str]] = {
    "ozden-s156-upper-bound-2026-11-10": (
        943,
        156,
        "[Mishapolk KKT refinements 2026-10-14]",
        "T-186",
        "12.977053087498",
        "2.113e-03",
    ),
    "ozden-s180-upper-bound-2026-11-10": (
        944,
        180,
        "[PingYou PR 574 certificates 2026-10-13]",
        "T-174",
        "13.915618502791",
        "1.375e-03",
    ),
    "ozden-s268-upper-bound-2026-11-10": (
        945,
        268,
        "[Özden s268 upper bound 2026-11-09]",
        "T-276",
        "16.872029849085",
        "4.400e-04",
    ),
    "ozden-s269-upper-bound-2026-11-11": (
        947,
        269,
        "[PingYou PR 574 certificates 2026-10-13]",
        "T-174",
        "16.900994579952",
        "5.190e-04",
    ),
}
#: The SHA-256 digests the issues (the witness) and the READMEs (both files) print, by count:
#: the candidate YAML's, then its JSON copy's.
PRINTED_DIGESTS = {
    156: (
        "62b8ab1059d7407de3cbb39c3d15e06ad3eadcb153c99ba234c128e15cbc0e47",
        "fba73ec09eed27a473969219d9fc3d4bed983cacc5ff34e872f928fe2b4fee38",
    ),
    180: (
        "91447bf157126c4c62edcc6751b10892fd1cb1e0006de9a82e5020809e6676f9",
        "7ab902b0dbd3c68bf797fe396cb62c630a66edfe09c8fe57a0e7e8ae1498754d",
    ),
    268: (
        "dd973c7efe7d17ff6d18241371a852a539caf1fa8d275ea026704fa9fba0592a",
        "791286a6364c1996f4ee7156e43d74be6166692b14eb3b7406ae7a07d8c1752d",
    ),
    269: (
        "f84820a6f7ef881ab2a533a21faac2fdebf38d0e9dd17144088167e3591cbb4d",
        "915033e4484ecb4114463c3db18a5a2946d825957fcf07a524388b05b121c0dc",
    ),
}
#: Each certificate's side rounded up at 16 places, as its claim record prints it.
CEILINGS = {
    156: "12.9770530874972048",
    180: "13.9156185027900258",
    268: "16.8720298490844502",
    269: "16.9009945799513249",
}


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _name(n: int) -> str:
    return next(name for name, row in PACKETS.items() if row[1] == n)


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


@pytest.mark.parametrize("n", sorted(PRINTED_DIGESTS))
def test_the_packets_hold_the_files_whose_digests_the_issues_print(n: int) -> None:
    manifest = _manifest(_name(n))
    candidate, copy = PRINTED_DIGESTS[n]
    assert manifest[f"n-{n}-candidate.yaml"] == candidate
    assert manifest[f"n{n}-witness.json"] == copy
    # The decimal pose the witness's source.path names is retained beside it.
    assert f"n-{n}-decimal-pose.yaml" in manifest


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_print_is_its_exact_side_rounded_up_and_its_reader_rebuilds_it(name: str) -> None:
    """Each issue's 12-place print is the side rounded up, and the JSON states the same
    packing as the YAML (the declaration's ``same_packing``, which ``read_facts`` holds)."""
    issue, n, _house, _result, printed, _gain = PACKETS[name]
    declaration = reports.load_declaration(reports.packet_path(name))
    assert declaration["source_key"] == f"[Özden s{n} upper bound {name[-10:]}]"
    assert declaration["issue"].endswith(f"/issues/{issue}")
    assert (declaration["requested"], declaration["replayed"]) == ([n], [n])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], row["offered"]) == (n, "witness-corners", printed)
    assert [other["path"] for other in row.get("same_packing", [])] == [f"n{n}-witness.json"]
    side = reports.read_facts(reports.packet_path(name))[n].side
    assert _up(side, 12) == Fraction(Decimal(printed))
    assert _up(side, 16) == Fraction(Decimal(CEILINGS[n]))
    assert reports.house_side(declaration["source_key"], n) == side


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_certificate_is_below_its_house_by_the_improvement_the_issue_states(
    name: str,
) -> None:
    _issue, n, house, result, _printed, gain = PACKETS[name]
    side = reports.read_facts(reports.packet_path(name))[n].side
    difference = reports.house_side(house, n) - side
    assert difference > 0
    assert f"{float(difference):.3e}" == gain
    (row,) = reports.check_claims(reports.packet_path(name))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (n, reports.THIS, "below")
    assert (row["case"]["source_key"], row["case"]["result"]) == (house, result)
    assert Fraction(row["case"]["difference"]) == difference


def test_the_ledger_records_each_claim() -> None:
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
    assert recorded == {156: ["#943"], 180: ["#944"], 268: ["#945"], 269: ["#947"]}


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(name: str) -> None:
    _issue, n, _house, _result, _printed, _gain = PACKETS[name]
    record = _json(reports.packet_path(name) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (n, name, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)


#: Each count's identity measurement against its house's packet: whether the nearest
#: centres pair it one to one, the squares the optimal assignment moves beyond a tenth,
#: and the squares tilted beyond a degree in the new packing and in the house's.
IDENTITY: dict[int, tuple[bool, int, tuple[int, int]]] = {
    156: (False, 58, (60, 62)),
    180: (False, 49, (40, 44)),
    268: (False, 125, (43, 99)),
    269: (False, 112, (100, 49)),
}


@pytest.mark.parametrize("n", sorted(IDENTITY))
def test_the_identity_measurement_the_notes_cite(n: int) -> None:
    """Measured against the house's packet first, then its regularized view and the house
    witness, which measures the same as the packet."""
    name = _name(n)
    _issue, _n, _house, result, _printed, _gain = PACKETS[name]
    one_to_one, beyond_tenth, tilted = IDENTITY[n]
    record = _json(reports.packet_path(name) / "measure/identity.json")
    assert record["n"] == n
    pair = record["pairs"][0]
    assert (pair["view"], pair["against"]) == ("OZDEN", result)
    assert pair["nearest_centre"]["one_to_one"] is one_to_one
    assert pair["assignment"]["moved_beyond"]["1e-1"] == beyond_tenth
    tilts = record["tilts"]
    assert (
        tilts["OZDEN"]["tilted_beyond_1_degree"],
        tilts[result]["tilted_beyond_1_degree"],
    ) == tilted
    witness = next(other for other in record["pairs"] if other["against"] == "house-witness")
    assert witness["assignment"]["moved_beyond"] == pair["assignment"]["moved_beyond"]


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_gain_is_far_above_the_house_certificate_s_contraction_margin(name: str) -> None:
    """RV-3 (think-ruu2) asks about gains inside a predecessor's padding margin; none of
    these is, by many orders of magnitude, so no entry here is held for it."""
    _issue, n, house, _result, _printed, _gain = PACKETS[name]
    record = _json(reports.packet_path(name) / f"measure/contraction-n{n}.json")
    assert record["n"] == n
    assert record["routes_accept"] is True
    side = reports.read_facts(reports.packet_path(name))[n].side
    gain = reports.house_side(house, n) - side
    assert gain > 10**6 * Fraction(record["margin"])
    own = _json(reports.packet_path(name) / f"measure/contraction-n{n}-own.json")
    assert own["routes_accept"] is True
    assert gain > 10**6 * Fraction(own["margin"])
