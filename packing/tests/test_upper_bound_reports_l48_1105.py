"""The upper-bound import of the intake pass's lane L48 of 5 November 2026 (think-3guf).

One packet, read by the ``evand-cert`` adapter: Kaelan Yim's #895 at 260
(vitamoon/vitamoon d11a8a1, where ``n260.cert`` is unchanged since its first commit,
e7cab3a). The general importer's checks run on it through ``test_upper_bound_reports``;
these hold what is particular to it: the pin and the digest recorded here, since the
author named a branch and stated no digest; the licence his reply gives; the side the
issue states; the house reader that rebuilds it; the ledger's verdict at 260 from the
packet's claim record; the retained sharp controls; and the identity measurement the
register's notes cite. Every test reads the packet and the ledger only; none needs the
network.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_arrangement_reports as kernel
from devtools import upper_bound_houses as houses
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp

NAME = "yim-s260-upper-bound-2026-11-05"
KEY = "[Yim s260 upper bound 2026-11-05]"
HOUSE = "[Daniel issue 845 2026-10-29]"
LEDGER = reports.ROOT / "campaign/issue-intake/upper-bounds-893-895-20261104"
#: The commit main named when the lane read the repository, and the file's first commit.
PIN = "d11a8a1ce798f7c0b4f801e922e242d22cedcd73"
FIRST_COMMIT = "e7cab3ac67e6d7c22970e7b8ffb121c1d96016a5"
#: Measured on the clone at the pin; the author stated none.
SHA256 = "c9e83969169f2ceec6014bc7fcd18418067209d485816c9b899b2e8b2a86ccbb"
#: The side #895 states, which is the certificate's header side.
SIDE = Fraction(
    1045817814143413714427921537528704162855767253933,
    62872364692131569638734867237718772414897487626,
)
#: T-257's side at 260, Evan Daniel's #845 certificate.
T257 = Fraction(8316991251060941991251052624833, 5 * 10**29)


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def test_the_packet_pins_the_branch_head_and_the_digest_measured_here() -> None:
    packet = reports.packet_path(NAME)
    record = _json(packet / "acquisition/sources.json")
    (source,) = record["sources"]
    assert (source["source_commit"], source["subtree_scope"]) == (PIN, ["n260.cert"])
    assert FIRST_COMMIT in record["git_scope"]
    assert "no digest" in record["git_scope"]
    manifest = (packet / "acquisition/upstream-subtree.sha256").read_text("utf-8")
    assert manifest.split() == [SHA256, "./n260.cert"]


def test_the_licence_is_the_one_the_authors_reply_gives() -> None:
    (source,) = _json(reports.packet_path(NAME) / "acquisition/sources.json")["sources"]
    assert source["license"].startswith("CC BY 4.0, with attribution to Kaelan Yim")
    assert "issuecomment-6650567350" in source["license"]


def test_the_side_is_the_issues_fraction_and_its_reader_rebuilds_it() -> None:
    packet = reports.packet_path(NAME)
    declaration = reports.load_declaration(packet)
    assert declaration["source_key"] == KEY
    assert (declaration["requested"], declaration["replayed"]) == ([260], [260])
    (row,) = declaration["certificates"]
    assert (row["n"], row["format"], Fraction(row["offered"])) == (260, "evand-cert", SIDE)
    certificate = reports.read_facts(packet)[260]
    assert (certificate.n, len(certificate.poses), certificate.side) == (260, 260, SIDE)
    assert reports.house_side(KEY, 260) == SIDE


def test_the_certificate_is_below_t257_by_about_2e10() -> None:
    assert reports.house_side(HOUSE, 260) == T257
    assert Fraction(199, 10**12) < T257 - SIDE < Fraction(2, 10**10)
    (row,) = reports.check_claims(reports.packet_path(NAME))["results"]
    assert (row["n"], row["smallest"], row["case"]["relation"]) == (260, reports.THIS, "below")
    assert (row["case"]["source_key"], row["case"]["result"]) == (HOUSE, "T-257")
    assert Fraction(row["case"]["difference"]) == T257 - SIDE


def test_the_ledger_walks_895_from_the_packets_claim_record() -> None:
    ledger = _json(LEDGER / "ledger.json")
    (count,) = [count for count in ledger["counts"] if count["n"] == 260]
    (step,) = count["steps"]
    assert (step["report"], step["verdict"], step["exact"]) == ("#895", "recorded", True)
    assert step["first_committed"] == "2026-11-05T05:27:47Z"
    assert "26 squares beyond 0.1" in step["measured"]
    sources = (LEDGER / "ledger.yaml").read_text(encoding="utf-8")
    assert f"packing/resources/web/{NAME}/acquisition/claims.json" in sources


def test_the_retained_sharp_controls_meet_contact_and_refuse_1e30_past_it() -> None:
    record = _json(reports.packet_path(NAME) / "receipts/sharp-controls.json")
    assert (record["n"], record["packet"], record["all_as_expected"]) == (260, NAME, True)
    assert record["epsilon"] == str(kernel.SHARP_EPSILON)
    assert {row["control"] for row in record["controls"]} == set(sharp.CONTROLS)
    for row in record["controls"]:
        assert row["as_expected"] is True
        assert set(row["routes"]) == set(kernel.ROUTES)
    # Row 253 touches the right wall (the top clears by 4.32e-13), so lowering the side to
    # its least far-wall contact lowers it by nothing.
    (lowered,) = [
        row
        for row in record["controls"]
        if row["control"] == "side-lowered-past-wall-contact" and row["where"] == "at-contact"
    ]
    assert lowered["detail"]["lowered_by"] == "0"


def test_the_identity_measurement_the_notes_cite() -> None:
    record = _json(reports.packet_path(NAME) / "measure/identity.json")
    assert record["n"] == 260
    (pair,) = record["pairs"]
    assert (pair["view"], pair["against"]) == ("YIM", "T-257")
    assert pair["nearest_centre"]["one_to_one"] is True
    assignment = pair["assignment"]
    assert assignment["symmetry"] == 0
    assert assignment["moved_beyond"]["1e-1"] == 26
    assert assignment["moved_beyond"]["1e-2"] == 64
    assert assignment["turned_beyond_1e-6"] == 14
    assert assignment["largest_move"] == "0.382307"
    yim, daniel = record["tilts"]["YIM"], record["tilts"]["T-257"]
    assert (yim["tilted_beyond_1_degree"], daniel["tilted_beyond_1_degree"]) == (105, 104)
    assert (yim["exactly_turned"], daniel["exactly_turned"]) == (260, 121)


REVIEW = reports.packet_path(NAME) / "review/review-2026-11-05"


def test_the_review_programs_are_the_ones_its_receipts_name() -> None:
    """The 5 November review's programs are retained byte for byte: each receipt names the
    digest of the program that wrote it, and programs.sha256 lists each program's."""
    listed = {
        path.removeprefix("programs/"): digest
        for digest, path in (
            line.split(maxsplit=1)
            for line in (REVIEW / "programs.sha256").read_text("utf-8").splitlines()
        )
    }
    for name, digest in listed.items():
        assert hashlib.sha256((REVIEW / "programs" / name).read_bytes()).hexdigest() == digest
    for receipt in sorted((REVIEW / "out").glob("*.json")):
        record = _json(receipt)
        assert listed[record["program"]] == record["program_sha256"], receipt.name
    accepted = _json(REVIEW / "out/check-yim-n260-ccw.json")
    assert (accepted["verdict"], accepted["program_sha256"]) == (
        "accepted",
        listed["certcheck.py"],
    )
    assert _json(REVIEW / "out/check-yim-n260-cw.json")["verdict"] == "refused"
    assert _json(REVIEW / "out/controls.json")["all_as_expected"] is True


def test_the_case_adopts_t265_at_260() -> None:
    assert houses.ADOPTED[260] == "T-265"
    assert 260 in houses.LATER_PASSES["2026-11-05"]
