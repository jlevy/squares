"""Francisco Couzo's verified-bounds index at 487b058, first committed with no issue.

One exact certificate inside the case corpus, at 211, retained and replayed; 296 beyond
it, pinned by digest as bulk data (OR-18) and compared from their exact header sides in
the packet's review record. These tests read the retained packet only.
"""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports

PACKET = "couzo-verified-bounds-2026-10-14"
SIDE = Fraction(7496774813149710519467765230441, 5 * 10**29)
PRINTED = "14.993549626300"
FIRST = "2026-10-14T17:45:39Z"
#: Issue #586's certificate at 211 (b85dee2), the smallest earlier report.
ISSUE_586 = Fraction(7496779456987003085666602828823, 5 * 10**29)


def _packet() -> Path:
    return reports.packet_path(PACKET)


def _review(name: str) -> dict[str, Any]:
    return json.loads((_packet() / "review" / name).read_text("utf-8"))


def test_custody_admits_the_211_certificate_at_the_side_the_source_prints() -> None:
    certificates = reports.read_facts(_packet())
    assert list(certificates) == [211]
    assert len(certificates[211].poses) == 211
    assert certificates[211].side == SIDE
    (row,) = reports.load_declaration(_packet())["certificates"]
    assert row["offered"] == PRINTED == legacy.ceiling_decimal(SIDE, 12)
    assert row["first_committed"] == FIRST


def test_211_is_the_smallest_report_and_below_586_by_its_margin() -> None:
    (row,) = reports.check_claims(_packet())["results"]
    assert row["smallest"] == reports.THIS
    assert row["case"]["result"] == "T-149"
    assert all(other["relation"] == "below" for other in [row["case"], *row["pending"]])
    (issue,) = [other for other in row["pending"] if other["report"] == "#586"]
    assert Fraction(issue["exact_side"]) == ISSUE_586
    assert Fraction(issue["difference"]) == ISSUE_586 - SIDE
    assert Fraction(9, 10**6) < ISSUE_586 - SIDE < Fraction(10, 10**6)


def test_the_receipt_admits_both_routes_and_refuses_both_controls() -> None:
    packet = _packet()
    positives = reports.check_certification(packet)
    assert list(positives) == [211]
    _declaration, facts = reports.replayed_facts(packet)
    parts = reports.receipt_parts(packet, facts)
    record = {"cases": [row for part, _ in parts for row in part["cases"]]}
    assert [(row["n"], row["control"]) for row in record["cases"]] == [
        (211, control) for control in reports.JOBS
    ]
    assert reports.receipt_summary(record)["pair_decisions"] == 3 * 211 * 210
    margins = reports.margins(positives)[211]
    for field in ("containment_clearance", "best_pair_gap"):
        assert margins[f"exact_verify_{field}"] == margins[f"independent_{field}"]
    assert Fraction(margins["exact_verify_containment_clearance"]) == Fraction(1, 2 * 10**20)


def test_the_beyond_horizon_certificates_are_pinned_and_compared_not_retained() -> None:
    record = json.loads((_packet() / "acquisition/sources.json").read_text("utf-8"))
    (source,) = record["sources"]
    pinned = {item["path"] for item in source["pinned_only"]}
    beyond = sorted(
        int(path[len("certificates/n") : -len(".cert")])
        for path in pinned
        if path.startswith("certificates/n") and path.endswith(".cert")
    )
    assert len(beyond) == 296
    assert min(beyond) > reports.HORIZON
    assert source["retained_file_count"] == 1
    comparison = _review("beyond-horizon-comparison.json")
    assert [row["n"] for row in comparison["rows"]] == beyond
    assert comparison["tally"] == {"recorded": 294, "not recorded: above": 2}
    assert comparison["pair_decisions_for_replay"] == sum(3 * n * (n - 1) for n in beyond)
    # Every row is superseded later, by #607 or the 4e4c8ce index.
    assert all(row["superseded_by_later"] for row in comparison["rows"])


def test_the_claims_record_states_each_recorded_side_as_the_source_prints_it() -> None:
    comparison = {row["n"]: row for row in _review("beyond-horizon-comparison.json")["rows"]}
    claims = _review("beyond-horizon-claims.json")
    assert claims["revision"] == "487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d"
    recorded = [n for n, row in comparison.items() if row["verdict"] == "recorded"]
    assert [row["n"] for row in claims["results"]] == recorded
    for row in claims["results"]:
        side = Fraction(row["exact_side"])
        printed = Fraction(row["offered_side"])
        assert printed - Fraction(1, 10**12) < side <= printed
        assert side < math.isqrt(row["n"] - 1) + 1
        assert row["offered_side"] == comparison[row["n"]]["printed"]
