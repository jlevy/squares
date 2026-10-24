"""Mykhailo Polkovskyi's lower 204 certificate: the #719 records lane of 23 October 2026.

The release's second 204 file, ``certificates/n204.cert`` at ``12fc466``, which the
author claimed on issue 719 after T-229 registered ``certificates/n-204.cert``
(think-h01y). It is retained under his written grant and read by the ``evand-cert``
adapter. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it: the digest the
release's custody record pins, the exact side and its margin below T-229, the margins the
replay found, which are below the binary64 spacing of the certificate's coordinates, the
sharp controls that meet that scale on both maintained routes, and the measured identity
with T-229's packing. Every test reads the retained packet only; none needs the network.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_reports as reports

PACKET = "mishapolk-n204-2026-10-22"
RELEASE = "mishapolk-issue719-2026-10-22"
N = 204
KEY = "[Mishapolk n204 2026-10-22]"
SIDE = Fraction(14808642830513087197802415708703, 10**30)
#: T-229's side at 204, the release's ``certificates/n-204.cert``.
T229 = Fraction(882663895519250432, 59604644775390625)
#: The SHA-256 the release's custody record pins for this file (its sources.json).
DIGEST = "9c5dabc8f2456b0c90650eac5794918c5e52ff90d9e817bd215c9816a88f3e7d"


def _packet() -> Path:
    return reports.packet_path(PACKET)


def _archived() -> Path:
    return reports.REPO / reports.acquisition(_packet())["archived_path"]


def _row() -> dict[str, Any]:
    (row,) = reports.check_claims(_packet())["results"]
    return row


def test_the_retained_file_has_the_digest_the_release_packet_pins() -> None:
    data = (_archived() / "certificates/n204.cert").read_bytes()
    assert hashlib.sha256(data).hexdigest() == DIGEST
    release = json.loads(
        (reports.packet_path(RELEASE) / "acquisition/sources.json").read_text("utf-8")
    )
    (source,) = release["sources"]
    pinned = {row["path"]: row["sha256"] for row in source["pinned_only"]}
    assert pinned["certificates/n204.cert"] == DIGEST


def test_the_certificate_states_its_side_and_the_house_reader_rebuilds_it() -> None:
    (certificate,) = reports.read_facts(_packet()).values()
    assert (certificate.n, certificate.side, len(certificate.poses)) == (N, SIDE, N)
    assert reports.house_side(KEY, N) == SIDE
    (row,) = reports.load_declaration(_packet())["certificates"]
    assert row["path"] == "certificates/n204.cert"
    assert Fraction(row["offered"]) == SIDE
    assert row["first_committed"] == "2026-10-22T05:29:48Z"


def test_the_side_is_below_t229_by_exactly_the_margin_the_records_state() -> None:
    row = _row()
    assert row["smallest"] == reports.THIS
    assert (row["case"]["result"], row["case"]["relation"]) == ("T-229", "below")
    assert Fraction(row["case"]["difference"]) == T229 - SIDE
    assert Fraction(14809457954896291297, 10**30) == T229 - SIDE
    assert {other["relation"] for other in row["pending"]} == {"below"}
    assert {other["result"] for other in row["pending"]} == {
        "T-225",
        "T-223",
        "T-228",
        "T-226",
        "T-186",
    }


def test_the_replay_clears_walls_by_5e_21_and_pairs_by_about_1e_20_on_both_routes() -> None:
    positives = reports.check_certification(_packet())
    (margins,) = reports.margins(positives).values()
    for route in kernel.ROUTES:
        assert Fraction(margins[f"{route}_containment_clearance"]) == Fraction(5, 10**21)
        gap = Fraction(margins[f"{route}_best_pair_gap"])
        assert Fraction(9999, 10**24) < gap < Fraction(1, 10**20)


def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it() -> None:
    receipt = json.loads((_packet() / "receipts/sharp-controls.json").read_text("utf-8"))
    assert receipt["all_as_expected"] is True
    assert Fraction(receipt["side"]) == SIDE
    seen = {(row["control"], row["where"]) for row in receipt["controls"]}
    controls = (*kernel.SHARP_CONTROLS, "squares-moved-past-near-wall-contact")
    assert seen == {(c, w) for c in controls for w in ("at-contact", "past-contact")}
    for row in receipt["controls"]:
        past = row["where"] == "past-contact"
        assert set(row["routes"]) == set(kernel.ROUTES)
        for verdict in row["routes"].values():
            assert verdict["passed"] is not past
            assert Fraction(verdict[row["margin"]]) == (-kernel.SHARP_EPSILON if past else 0)


def test_the_measured_identity_pairs_it_one_to_one_with_t229s_packing() -> None:
    identity = json.loads((_packet() / "measure/identity.json").read_text("utf-8"))
    pairs = {pair["against"]: pair for pair in identity["pairs"]}
    t229 = pairs["T-229 (#719 n-204.cert)"]["nearest_centre"]
    assert t229["one_to_one"] is True
    assert t229["symmetry"] == 0
    assert float(t229["largest_displacement"]) < 1e-10
    assert all(count == 0 for count in t229["moved_beyond"].values())
    t223 = pairs["T-223 (#678)"]["nearest_centre"]
    assert t223["one_to_one"] is True
    assert t223["symmetry"] == 0
    assert t223["moved_beyond"]["1e-1"] == 7
