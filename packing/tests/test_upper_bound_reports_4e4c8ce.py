"""Francisco Couzo's exact certificate at 237, first committed in 4e4c8ce with no issue.

The 15 October reads lane found it past issue #607's pin: the author's exact refinement of
his own #607 packing, 2.4e-11 below it. These tests hold what is particular to the packet
and the general importer's checks on it, reading the retained packet only.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports

PACKET = "couzo-n237-2026-10-15"
SIDE = Fraction(7951301819129798440089572127137, 5 * 10**29)
PRINTED = "15.902603638260"
#: The first commit holding the certificate, which dates the claim.
FIRST = "2026-10-15T00:31:53Z"
#: Issue #607's certificate at 237, first committed in 43ac7d2, as the issue prints it.
ISSUE_607 = ("2026-10-14T19:15:09Z", "15.902603638284")


def _packet() -> Path:
    return reports.packet_path(PACKET)


def _row() -> dict[str, Any]:
    (row,) = reports.check_claims(_packet())["results"]
    return row


def test_custody_admits_the_certificate_at_the_side_the_source_prints() -> None:
    declaration = reports.load_declaration(_packet())
    certificates = reports.read_facts(_packet())
    assert list(certificates) == [237]
    certificate = certificates[237]
    assert len(certificate.poses) == 237
    assert certificate.side == SIDE
    (row,) = declaration["certificates"]
    assert row["offered"] == PRINTED == legacy.ceiling_decimal(SIDE, 12)
    assert row["first_committed"] == FIRST


def test_the_index_copy_is_the_same_bytes_as_the_retained_certificate() -> None:
    record = json.loads((_packet() / "acquisition/sources.json").read_text("utf-8"))
    (source,) = record["sources"]
    lines = (_packet() / "acquisition/upstream-subtree.sha256").read_text("utf-8").splitlines()
    manifest = {path: digest for digest, path in (line.split("  ./", 1) for line in lines)}
    assert manifest["certificates/n237.cert"] == manifest["certificates/best/n237.cert"]
    pinned = {item["path"] for item in source["pinned_only"]}
    assert "certificates/best/n237.cert" in pinned
    assert "certificates/n237.cert" not in pinned


def test_the_certificate_is_the_smallest_report_and_follows_607() -> None:
    row = _row()
    assert Fraction(row["exact_side"]) == SIDE
    assert row["smallest"] == reports.THIS
    # #614 adopted #593's certificate (T-183) as the house at 237; T-140 (#488), the house
    # before it, is an earlier report (PR #627 review A1).
    assert row["case"]["result"] == "T-183"
    assert row["case"]["relation"] == "below"
    assert all(other["relation"] == "below" for other in row["pending"])
    assert "#593" not in [other["report"] for other in row["pending"]]
    (earlier,) = [other for other in row["pending"] if other["report"] == "#488"]
    assert earlier["result"] == "T-140"
    (issue,) = [other for other in row["pending"] if other["report"] == "#607"]
    committed, printed = ISSUE_607
    # Read at #607's exact side, through its packet, since the records lane of 15 October
    # registered it as T-189.
    assert issue["result"] == "T-189"
    exact = reports.house_side("[Couzo certificates 2026-10-14]", 237)
    assert Fraction(issue["difference"]) == exact - SIDE
    assert Fraction(239, 10**13) < exact - SIDE < Fraction(240, 10**13)
    # Below every number #607's print may be, rounded up at 12 places.
    assert Fraction(printed) - Fraction(1, 10**12) - SIDE > Fraction(23, 10**12)
    assert committed < FIRST


def test_the_receipt_admits_both_routes_and_refuses_both_controls() -> None:
    packet = _packet()
    positives = reports.check_certification(packet)
    assert list(positives) == [237]
    _declaration, facts = reports.replayed_facts(packet)
    parts = reports.receipt_parts(packet, facts)
    record = {"cases": [row for part, _ in parts for row in part["cases"]]}
    assert [(row["n"], row["control"]) for row in record["cases"]] == [
        (237, control) for control in reports.JOBS
    ]
    assert reports.receipt_summary(record)["pair_decisions"] == 3 * 237 * 236
    margins = reports.margins(positives)[237]
    for field in ("containment_clearance", "best_pair_gap"):
        assert margins[f"exact_verify_{field}"] == margins[f"independent_{field}"]
    assert Fraction(margins["exact_verify_containment_clearance"]) == Fraction(1, 2 * 10**20)
    assert 0 < Fraction(margins["exact_verify_best_pair_gap"]) < Fraction(1, 10**20)
