"""The upper-bound imports of the intake pass of 31 October 2026, lane L2 (think-3guf).

Seven packets, all read by the ``evand-cert`` adapter: Francisco Couzo's #843 (130), his
a5a5d76 publication (260, 307) and #844 (232, 260, 307); Evan Daniel's #845 (172, 204, 260,
293) and his update to #824 (299); and Mykhailo Polkovskyi's certificates of 23 October
(e386aab to fbc1749, no issue) and of #846. The general importer's checks run on each packet
through ``test_upper_bound_reports``; these hold what is particular to them: the digests the
reports print, the side of each certificate and its print, the house readers that rebuild
them, the ledger's verdicts, the retained sharp controls and the identity measurements the
register's notes cite. Every test reads the packets and the ledger only; none needs the
network.
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

LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-843-846-20261031"

#: Each packet with its source key, the counts it requests and the counts it replays.
PACKETS: dict[str, tuple[str, list[int], list[int]]] = {
    "mishapolk-1023-refinements-2026-10-30": (
        "[Mishapolk refinements 2026-10-23]",
        [154, 155, 183, 211, 227, 236, 237, 241, 271],
        [88, 126, 152, 154, 155, 183, 211, 227, 236, 237, 241, 270, 271],
    ),
    "couzo-issue843-2026-10-28": ("[Couzo n130 2026-10-27]", [130], [130]),
    "couzo-a5a5d76-2026-10-28": ("[Couzo a5a5d76 2026-10-28]", [260, 307], [260, 307]),
    "couzo-issue844-2026-10-28": (
        "[Couzo issue 844 2026-10-28]",
        [232, 260, 307],
        [232, 260, 307],
    ),
    "evand-issue845-2026-10-29": (
        "[Daniel issue 845 2026-10-29]",
        [172, 204, 260, 293],
        [172, 204, 260, 293],
    ),
    "evand-n299-update-2026-10-29": ("[Daniel n299 update 2026-10-29]", [299], [299]),
    "mishapolk-issue846-2026-10-30": (
        "[Mishapolk issue 846 2026-10-30]",
        [105, 130, 146, 156, 229, 308],
        [105, 130, 146, 156, 182, 204, 211, 229, 241, 260, 268, 299, 304, 308],
    ),
}

CANDIDATES = "search/packer/candidates"
#: The SHA-256 digests the issues and the #824 update print, by packet and upstream path.
PRINTED_DIGESTS = {
    "couzo-issue843-2026-10-28": {
        "certificates/n130.cert": (
            "a2618e1a7a2961cf63bf5a23ac0b006d18ef0dde00dad562b005d82a509c7fcd"
        ),
        "n130.txt": "6d4121d429165db50532a8ee5b1d0a20f9d49df5e9be51c614b1464e37708099",
    },
    "couzo-issue844-2026-10-28": {
        "certificates/best/n232.cert": (
            "23b035c34a5a93a3bf23eccaddc49e8d6e5e4003ec5e97c036153b2ca5ddbe54"
        ),
        "certificates/n260.cert": (
            "abd3b4e3bc4411de8b32e400f424645ad66f376dcba52ea8ba748ecdf83a0b11"
        ),
        "n260.txt": "acab77d3986f0cc497b716a2eb9c9c5b7a4652dd5418e1bfbe80854ae4347d2d",
        "certificates/n307.cert": (
            "1fd01ff42e7679f1e5b2c8eb8af59e51d3cca0392772b81bb4d78d67a26214e9"
        ),
        "n307.txt": "7629bb297f4aabcf43111b28959c0578cdf35384758c507b608e4a0651c39843",
    },
    "evand-issue845-2026-10-29": {
        f"{CANDIDATES}/s172_1028.cert": (
            "1e16ad2789538610a42ebec7f735d932fdbe8125a7c991801e644b6f072352b9"
        ),
        f"{CANDIDATES}/s172_1028_regularized.cert": (
            "0ab41bff6847fc3929e91253b9a2db021db0f9406915d32b6eec40d523d2eb1a"
        ),
        f"{CANDIDATES}/s204_1028.cert": (
            "2b371e81d568ad5c4490257dcfdb87cd1e238232bb60bd1ece4844340af0a2c3"
        ),
        f"{CANDIDATES}/s260_1028.cert": (
            "d6d6f45f600f6552416ea3708d8ee04416cfe88820ee4c3c422d8e131d7cdf87"
        ),
        f"{CANDIDATES}/s293_1028.cert": (
            "236bc05f057a28df402c09453f4ccce35d63b518f4f0305419889612f07c42bc"
        ),
    },
    "evand-n299-update-2026-10-29": {
        f"{CANDIDATES}/s299_1028.cert": (
            "ccb323dd6d69bee141d59cae4c605f45136b998dfecce1248e200b678b253db5"
        ),
    },
}

#: The ledger's verdict at each count it walks for these packets, by the report that holds it.
RECORDED = {
    130: ["#843", "#846"],
    154: ["Mishapolk/square-packing-records@6664afc"],
    172: ["#845"],
    204: ["#845"],
    232: ["#844"],
    260: ["franciscouzo/square-packing@a5a5d76", "#844", "#845"],
    293: ["#845"],
    299: ["#824 update"],
    307: ["franciscouzo/square-packing@a5a5d76", "#844"],
}
NOT_RECORDED = {88, 126, 182, 268, 270, 304}


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
def test_the_packets_hold_the_files_whose_digests_the_reports_print(name: str) -> None:
    manifest = _manifest(name)
    for path, digest in PRINTED_DIGESTS[name].items():
        assert manifest[path] == digest, path


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_certificate_rounds_up_to_its_print_and_its_reader_rebuilds_it(name: str) -> None:
    key, requested, replayed = PACKETS[name]
    declaration = reports.load_declaration(reports.packet_path(name))
    assert declaration["source_key"] == key
    assert (declaration["requested"], declaration["replayed"]) == (requested, replayed)
    certificates = reports.read_facts(reports.packet_path(name))
    for row in declaration["certificates"]:
        side = certificates[row["n"]].side
        places = len(row["offered"].partition(".")[2])
        assert Fraction(math.ceil(side * 10**places), 10**places) == Fraction(
            Decimal(row["offered"])
        )
        assert reports.house_side(key, row["n"]) == side


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_every_requested_certificate_is_the_smallest_report_its_claim_record_reads(
    name: str,
) -> None:
    _key, requested, _replayed = PACKETS[name]
    rows = {row["n"]: row for row in reports.check_claims(reports.packet_path(name))["results"]}
    for n in requested:
        assert rows[n]["smallest"] == reports.THIS, n
        assert rows[n]["case"]["relation"] == "below", n


def test_the_ledger_records_what_the_register_records_and_nothing_else() -> None:
    """The verdicts stage 3 registered: at each count the reports recorded, in report order,
    and at 88, 126, 182, 268, 270 and 304 none; 152 is undecided against T-122's exact
    side."""
    ledger = _json(LEDGER / "ledger.json")
    recorded: dict[int, list[str]] = {}
    for count in ledger["counts"]:
        for claim in count["steps"]:
            if claim["verdict"] == "recorded":
                recorded.setdefault(count["n"], []).append(claim["report"])
    for n, holders in RECORDED.items():
        assert recorded[n] == holders, n
    assert not NOT_RECORDED & set(recorded)
    assert 152 not in recorded
    for n in (105, 146, 156, 229, 308):
        assert recorded[n] == ["#846"]
    for n in (155, 183, 211, 227, 236, 237, 241, 271):
        (holder,) = recorded[n]
        assert holder.startswith("Mishapolk/square-packing-records@")


def _sharp_records(name: str) -> list[dict[str, Any]]:
    receipts = reports.packet_path(name) / "receipts"
    single = receipts / "sharp-controls.json"
    if single.exists():
        return [_json(single)]
    return [_json(path) for path in sorted(receipts.glob("sharp-controls-n*.json"))]


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(name: str) -> None:
    _key, _requested, replayed = PACKETS[name]
    records = _sharp_records(name)
    assert sorted(record["n"] for record in records) == replayed
    for record in records:
        assert (record["packet"], record["all_as_expected"]) == (name, True)
        assert record["epsilon"] == str(kernel.SHARP_EPSILON)
        controls = {row["control"] for row in record["controls"]}
        assert controls == set(sharp.CONTROLS)
        for row in record["controls"]:
            assert row["as_expected"] is True
            assert set(row["routes"]) == set(kernel.ROUTES)


@pytest.mark.parametrize("name", sorted(PACKETS))
def test_each_requested_count_has_its_identity_measurement(name: str) -> None:
    _key, requested, _replayed = PACKETS[name]
    measure = reports.packet_path(name) / "measure"
    for n in requested:
        single = measure / "identity.json"
        path = single if single.exists() else measure / f"identity-n{n:03d}.json"
        record = _json(path)
        assert record["n"] == n
        assert record["pairs"]
