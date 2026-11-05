"""The upper-bound import of the intake pass's lane L51 of 5 November 2026 (think-3guf).

Evan Daniel's #914: seven certificates at 175, 204, 260, 268, 293, 303 and 304, and six
regularized views at the same sides, all first committed at evand/square-packing bb4cc78
and read by the ``evand-cert`` adapter. The certificates and their companion files are
retained in one packet; the views are pinned in a second against the first one's copies,
so that both maintained exact routes decide each view as they decide the certificates.
The general importer's checks run on both packets through ``test_upper_bound_reports``;
these hold what is particular to them: the thirteen digests the issue prints, the licence,
the sides the issue prints and the house reader that rebuilds them, each certificate's
place below its house, each view's tie with its certificate, the ledger's verdicts, the
retained sharp controls, and the identity measurements the register's notes cite. Every
test reads the packets and the ledger only; none needs the network.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

NAME = "evand-issue914-2026-11-05"
VIEWS = "evand-issue914-views-2026-11-05"
KEY = "[Daniel issue 914 2026-11-05]"
LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-914-20261105"
PIN = "bb4cc78e5b35103c1f177db55e9cf08974e66563"
CANDIDATES = "search/packer/candidates"
#: The thirteen SHA-256 digests #914 prints: each set's certificate, then its regularized
#: view where it has one.
SETS = {
    "s175_1105": (
        "32749cb2cc072a1fa70231b68908c1a255092c032748ff5c33c1ccfe018ea916",
        "786519adb0c0f103b7130eae165b65feaa4e59d3b02591cdd67c37e2f615c1d4",
    ),
    "s204_trig1": (
        "17ed0e5b7c4e69ca8558195886be7d7a149e9c09a8f60caf57bef160f75cf687",
        "55007aca9181eeb8ac53b9e48705c716974ede0bb0feee183ac6b8c493d9d107",
    ),
    "s260_ks_1105": ("24edcc0b45e4b3b57b6632bbe0430d2574425205c0b127e8f96f16fc3e38b663",),
    "s268_1105": (
        "50f9704860c186e47e30244226b983cccd36b3ff27ba3fd23bad31ce146a1844",
        "cfb1f7a793884bb938f29f10aa7dcd93b0c078700141af98a3bceb70ec69c0b2",
    ),
    "s293_1105": (
        "0fc702287dc5a79360da89379822b42ef12de0d54f0d9b7b13f2f765ba659f28",
        "76d57b853e3e332b2e65084f07af863135dc74a1b0b179ba4a4e4d310cae9ab1",
    ),
    "s303_1105": (
        "2f53c049a5f7feb793181e99282d0b36922b7c6f7fe9eece008f888c06a5c9a3",
        "42a8ecd958c7f381a5ca82131b3df1f8fe237605bb44d4cb2facca07443f1940",
    ),
    "s304_1105": (
        "440402323670057e763ab6edac7cb4ba971222929d235a587b130f96d6d595cf",
        "ee95b657f24d0f93b2b02c073922147b36faed4996fcdd6df587f713fccad065",
    ),
}
DIGESTS = {
    f"{stem}{suffix}": digest
    for stem, digests in SETS.items()
    for suffix, digest in zip((".cert", "_regularized.cert"), digests, strict=False)
}
#: Each certificate's exact header side, and the 12-place print #914 gives it.
SIDES = {
    175: (Fraction(13764050051543175143919941166751, 10**30), "13.764050051544"),
    204: (Fraction(7402180691825929362760144937013, 5 * 10**29), "14.804361383652"),
    260: (Fraction(8316760475444266760475435949833, 5 * 10**29), "16.633520950889"),
    268: (Fraction(2109062439766878830759866953431, 125 * 10**27), "16.872499518136"),
    293: (Fraction(17623065212060701770633564247069, 10**30), "17.623065212061"),
    303: (Fraction(17901832750854048761575294038467, 10**30), "17.901832750855"),
    304: (Fraction(17920944093340242061198022152503, 10**30), "17.920944093341"),
}
#: The house each certificate is below on main 249bb82e7, its result and its holders' reader.
HOUSES = {
    175: ("T-186", "[Mishapolk KKT refinements 2026-10-14]"),
    204: ("T-264", "[Özden s204 upper bound 2026-11-03]"),
    260: ("T-265", "[Yim s260 upper bound 2026-11-05]"),
    268: ("T-242", "[Daniel Kaggle descents 2026-10-24]"),
    293: ("T-257", "[Daniel issue 845 2026-10-29]"),
    303: ("T-240", "[Couzo issue 763 2026-10-23]"),
    304: ("T-242", "[Daniel Kaggle descents 2026-10-24]"),
}
VIEWED = [175, 204, 268, 293, 303, 304]


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _manifest(name: str) -> dict[str, str]:
    text = (reports.packet_path(name) / "acquisition/upstream-subtree.sha256").read_text(
        "utf-8"
    )
    return {
        path.removeprefix("./"): digest
        for digest, path in (line.split() for line in text.splitlines())
    }


def test_both_packets_pin_bb4cc78_and_the_issues_thirteen_digests() -> None:
    for name in (NAME, VIEWS):
        (source,) = _json(reports.packet_path(name) / "acquisition/sources.json")["sources"]
        assert source["source_commit"] == PIN
    retained = _manifest(NAME)
    pinned = _manifest(VIEWS)
    for file, digest in DIGESTS.items():
        assert retained[f"{CANDIDATES}/{file}"] == digest
        if file.endswith("_regularized.cert"):
            assert pinned[f"{CANDIDATES}/{file}"] == digest
    assert len([path for path in retained if path.startswith(CANDIDATES)]) == 56
    assert sorted(pinned) == sorted(
        ["LICENSE", *(f"{CANDIDATES}/{f}" for f in DIGESTS if f.endswith("_regularized.cert"))]
    )


def test_the_licence_is_the_sources_mit_and_the_views_pin_it_against_the_first_packet() -> None:
    (source,) = _json(reports.packet_path(NAME) / "acquisition/sources.json")["sources"]
    assert source["license"].startswith("MIT, copyright (c) 2026 Evan Daniel")
    (views,) = _json(reports.packet_path(VIEWS) / "acquisition/sources.json")["sources"]
    assert views["retained_file_count"] == 0
    assert {row["identical_to"].split("/")[3] for row in views["pinned_only"]} == {NAME}


def test_each_certificate_is_admitted_at_the_issues_print_and_its_reader_rebuilds_it() -> None:
    packet = reports.packet_path(NAME)
    declaration = reports.load_declaration(packet)
    assert declaration["source_key"] == KEY
    assert declaration["requested"] == declaration["replayed"] == list(SIDES)
    offered = {row["n"]: row["offered"] for row in declaration["certificates"]}
    certificates = reports.read_facts(packet)
    for n, (side, printed) in SIDES.items():
        assert offered[n] == printed
        assert (certificates[n].n, len(certificates[n].poses), certificates[n].side) == (
            n,
            n,
            side,
        )
        assert reports.house_side(KEY, n) == side


def test_each_certificate_is_below_its_house_and_smallest() -> None:
    rows = {row["n"]: row for row in reports.check_claims(reports.packet_path(NAME))["results"]}
    assert sorted(rows) == list(SIDES)
    for n, (result, key) in HOUSES.items():
        row = rows[n]
        assert (row["smallest"], row["case"]["relation"]) == (reports.THIS, "below")
        assert (row["case"]["result"], row["case"]["source_key"]) == (result, key)
        assert Fraction(row["case"]["difference"]) == reports.house_side(key, n) - SIDES[n][0]
    margins = {n: Fraction(rows[n]["case"]["difference"]) for n in SIDES}
    assert Fraction(124, 10**6) < min(margins.values()) == margins[175] < Fraction(125, 10**6)
    assert Fraction(109, 10**4) < max(margins.values()) == margins[293] < Fraction(11, 10**3)


def test_each_view_states_its_certificates_side_and_ties_it() -> None:
    packet = reports.packet_path(VIEWS)
    declaration = reports.load_declaration(packet)
    assert declaration["source_key"] == KEY
    assert declaration["requested"] == declaration["replayed"] == VIEWED
    views = reports.read_facts(packet)
    certificates = reports.read_facts(reports.packet_path(NAME))
    rows = {row["n"]: row for row in reports.check_claims(packet)["results"]}
    for n in VIEWED:
        assert views[n].side == certificates[n].side == SIDES[n][0]
        assert views[n] != certificates[n]
        (other,) = rows[n]["pending"]
        assert (other["relation"], rows[n]["smallest"]) == ("equal", None)


def test_the_ledger_records_all_seven_from_the_packets_claim_record() -> None:
    ledger = _json(LEDGER / "ledger.json")
    steps = {count["n"]: count["steps"] for count in ledger["counts"]}
    assert sorted(steps) == list(SIDES)
    for n in SIDES:
        (step,) = steps[n]
        assert (step["report"], step["verdict"], step["exact"]) == ("#914", "recorded", True)
        assert step["first_committed"] == "2026-11-05T18:29:13Z"
    sources = (LEDGER / "ledger.yaml").read_text(encoding="utf-8")
    assert f"packing/resources/web/{NAME}/acquisition/claims.json" in sources


@pytest.mark.parametrize(
    ("name", "n"), [(NAME, n) for n in SIDES] + [(VIEWS, n) for n in VIEWED]
)
def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it(
    name: str, n: int
) -> None:
    record = _json(reports.packet_path(name) / f"receipts/sharp-controls-n{n}.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (n, name, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)
