"""The upper-bound imports of the intake pass's lane L36 of 4 November 2026 (think-3guf).

Two packets, both read by the ``witness-center-basis`` adapter: Doğa Özden's #893 at 299
(kenaznia-doga/s299-upper-bound 6486ead) and #894 at 204 (kenaznia-doga/s204-upper-bound
d4b8b05). The general importer's checks run on each packet through
``test_upper_bound_reports``; these hold what is particular to them: the digests the issues
print, the side of each certificate against its print (#893's 12-place print is below its
exact side, so the declaration offers the exact fraction the issue states), the house
readers that rebuild them, the ledger's verdicts at 204, 260 and 299, the retained sharp
controls and the identity measurements the register's notes cite. Every test reads the
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

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-893-895-20261104"

#: Each packet with its source key, its count, the house it is compared with and the side.
PACKETS: dict[str, tuple[str, int, str, Fraction]] = {
    "ozden-s299-upper-bound-2026-11-03": (
        "[Özden s299 upper bound 2026-11-03]",
        299,
        "[Daniel n299 update 2026-10-29]",
        Fraction(3560247706795812422293947620670679551, 2 * 10**35),
    ),
    "ozden-s204-upper-bound-2026-11-03": (
        "[Özden s204 upper bound 2026-11-03]",
        204,
        "[Daniel issue 845 2026-10-29]",
        Fraction(7403810497792604009019579959, 5 * 10**26),
    ),
}
#: The SHA-256 digests the issues and the sources' READMEs print, by packet and upstream path.
PRINTED_DIGESTS = {
    "ozden-s299-upper-bound-2026-11-03": {
        "n-299-candidate.yaml": (
            "2976d67f0b6da33434831a53d41c9af2a555e9d67daadb0e80ffc1a5cc6176e0"
        ),
        "n299-refill2-t000173.json": (
            "4fac4ed1b75eb0890935691045a0b395af2a762f8130bcd83cd4b3b83f0bb797"
        ),
    },
    "ozden-s204-upper-bound-2026-11-03": {
        "n-204-candidate.yaml": (
            "e3c8c7ebf80819290efa023b0fa7f6cd046b9ee01979aac9cb8d76c1ec14eeb8"
        ),
        "n204-witness.json": "613c0a668026a393f7eaebf796acdc2c8aafe6e7c9c66bc9ee68397ce13caf45",
    },
}
#: The 12-place sides the issues print as rounded up.
PRINTS = {299: "17.801238533979", 204: "14.807620995586"}
#: Kaelan Yim's #895 states this side; no certificate is retained (think-qclj).
YIM_260 = Fraction(
    1045817814143413714427921537528704162855767253933,
    62872364692131569638734867237718772414897487626,
)


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


@pytest.mark.parametrize("name", sorted(PRINTED_DIGESTS))
def test_the_packets_hold_the_files_whose_digests_the_issues_print(name: str) -> None:
    manifest = _manifest(name)
    for path, digest in PRINTED_DIGESTS[name].items():
        assert manifest[path] == digest, path


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_side_is_its_witness_and_its_reader_rebuilds_it(name: str) -> None:
    key, n, _house, side = PACKETS[name]
    declaration = reports.load_declaration(reports.packet_path(name))
    assert declaration["source_key"] == key
    assert (declaration["requested"], declaration["replayed"]) == ([n], [n])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"]) == (n, "witness-center-basis")
    certificate = reports.read_facts(reports.packet_path(name))[n]
    assert certificate.side == side
    assert reports.house_side(key, n) == side


def test_893s_print_is_below_its_side_and_204s_rounds_up() -> None:
    """#893 prints 17.801238533979 as its side rounded up at 12 places; the side is 6.21e-14
    above that print, so the declaration offers the issue's exact fraction instead. #894's
    print is its side rounded up."""
    for name, (_key, n, _house, side) in PACKETS.items():
        rounded = Fraction(math.ceil(side * 10**12), 10**12)
        printed = Fraction(Decimal(PRINTS[n]))
        offered = reports.load_declaration(reports.packet_path(name))["certificates"][0][
            "offered"
        ]
        if n == 299:
            assert printed < side < printed + Fraction(1, 10**12)
            assert rounded == Fraction(Decimal("17.801238533980"))
            assert Fraction(offered) == side
        else:
            assert rounded == printed == Fraction(Decimal(offered))


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_certificate_is_below_the_house_it_is_compared_with(name: str) -> None:
    _key, n, house, side = PACKETS[name]
    assert side < reports.house_side(house, n)
    (row,) = reports.check_claims(reports.packet_path(name))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (n, reports.THIS, "below")
    assert row["case"]["source_key"] == house


def test_the_ledger_records_each_claim_and_895_by_its_stated_side() -> None:
    """At 204 and 299 the issue is the one report; at 260 #895 is walked by the side it
    states, below T-257, and stage 3 registers nothing for it until a certificate is
    retained."""
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
    assert recorded == {204: ["#894"], 260: ["#895"], 299: ["#893"]}
    assert reports.house_side("[Daniel issue 845 2026-10-29]", 260) > YIM_260


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(name: str) -> None:
    _key, n, _house, _side = PACKETS[name]
    record = _json(reports.packet_path(name) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (n, name, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)


@pytest.mark.parametrize(
    ("name", "against", "beyond_tenth", "tilted"),
    [
        ("ozden-s299-upper-bound-2026-11-03", "T-258", 12, (85, 87)),
        ("ozden-s204-upper-bound-2026-11-03", "T-257", 6, (76, 79)),
    ],
)
def test_the_identity_measurement_the_notes_cite(
    name: str, against: str, beyond_tenth: int, tilted: tuple[int, int]
) -> None:
    _key, n, _house, _side = PACKETS[name]
    record = _json(reports.packet_path(name) / "measure/identity.json")
    assert record["n"] == n
    (pair,) = record["pairs"]
    assert (pair["view"], pair["against"]) == ("OZDEN", against)
    assert pair["nearest_centre"]["one_to_one"] is True
    assert pair["assignment"]["symmetry"] == 0
    assert pair["assignment"]["moved_beyond"]["1e-1"] == beyond_tenth
    tilts = record["tilts"]
    assert (
        tilts["OZDEN"]["tilted_beyond_1_degree"],
        tilts[against]["tilted_beyond_1_degree"],
    ) == tilted
