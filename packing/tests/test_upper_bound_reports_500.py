"""Issue #500: SQUISH's fourth request, nine exact rational packings kept as derived facts.

The source tree has no licence, so the packet keeps digests and the exact facts derived
from the pinned certificates. The general importer's checks run on the packet through
``test_upper_bound_reports``; these hold what is particular to it. Every test reads
retained packets only.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from typing import Any

from devtools import upper_bound_reports as reports

SQUISH_500 = "squish-500-fourth-request-2026-10-11"
SOURCE_KEY = "[SQUISH fourth request 2026-10-11]"
#: The 15-digit sides the issue prints, which are the exact sides cut, not rounded up.
ISSUE = {
    176: "13.812856253277056",
    181: "13.950819531022924",
    238: "15.924106785321494",
    239: "15.948443327300499",
    270: "16.928196993329016",
    271: "16.949116687815009",
    272: "16.965586474837671",
    304: "17.929657042170880",
    305: "17.950544853925636",
}
#: Each registered or retained report the claim record reads from its own packet, and where.
EXACT_READS = {
    "T-130 (#460)": (270,),
    "T-134 (#476)": (270,),
    "T-136 (#481)": (270, 305),
    "T-138 (#470)": (270,),
    "T-140 (#488)": (270, 305),
    "#470": (238, 239),
    "#476": (181, 271, 272, 304, 305),
    "#489": (305,),
}
READERS = {
    "T-130 (#460)": "[Couzo follow-up refinements 2026-10-08]",
    "T-134 (#476)": "[Couzo exact certificates 2026-10-09]",
    "T-136 (#481)": "[SQUISH third request 2026-10-09]",
    "T-138 (#470)": "[Mishapolk decimal poses 2026-10-09]",
    "T-140 (#488)": "[Couzo certificates 2026-10-10]",
    "#470": "[Mishapolk decimal poses 2026-10-09]",
    "#476": "[Couzo exact certificates 2026-10-09]",
    "#489": "[Daniel record hunt 3 2026-10-10]",
}


def _rows() -> dict[int, dict[str, Any]]:
    rows = reports.check_claims(reports.packet_path(SQUISH_500))["results"]
    return {row["n"]: row for row in rows}


def test_each_side_is_the_exact_fraction_summary_csv_prints_and_the_issue_cuts() -> None:
    packet = reports.packet_path(SQUISH_500)
    declaration = reports.load_declaration(packet)
    certificates = reports.read_facts(packet)
    assert list(certificates) == list(ISSUE) == declaration["requested"]
    for row in declaration["certificates"]:
        side = certificates[row["n"]].side
        assert side == Fraction(row["offered"])
        assert row.get("printed_in", "").endswith("/squish-submission-2026-10-11/summary.csv")
        # The issue's display lies below the side by less than its last place, so it is
        # no ceiling; the record admits the exact fraction and shows it rounded up.
        shown = Fraction(Decimal(ISSUE[row["n"]]))
        assert shown < side < shown + Fraction(1, 10**15)


def test_the_claims_find_506_smaller_only_at_304_and_305() -> None:
    rows = _rows()
    assert {n: row["smallest"] for n, row in rows.items()} == {
        176: reports.THIS,
        181: reports.THIS,
        238: reports.THIS,
        239: reports.THIS,
        270: reports.THIS,
        271: reports.THIS,
        272: reports.THIS,
        304: "#506",
        305: "#506",
    }
    assert all(row["case"]["relation"] == "below" for row in rows.values())
    assert rows[176]["case"]["reported_relation"] == "below"
    for n in (304, 305):
        (couzo,) = [other for other in rows[n]["pending"] if other["report"] == "#506"]
        assert (couzo["rounding"], couzo["relation"]) == ("up", "above")


def test_the_claims_read_every_retained_report_at_its_exact_side() -> None:
    """#481, #488 and the rest are retained, so none is compared at its print."""
    rows = _rows()
    read = {
        (n, other["report"]): other
        for n, row in rows.items()
        for other in row["pending"]
        if other["report"] in READERS
    }
    assert sorted(read) == sorted(
        (n, report) for report, counts in EXACT_READS.items() for n in counts
    )
    for (n, report), other in read.items():
        assert "printed" not in other
        assert Fraction(other["exact_side"]) == reports.house_side(READERS[report], n)
        assert other["relation"] == "below"


def test_the_fourth_request_reader_rebuilds_each_exact_side() -> None:
    certificates = reports.read_facts(reports.packet_path(SQUISH_500))
    for n, certificate in certificates.items():
        assert reports.house_side(SOURCE_KEY, n) == certificate.side


def test_the_plan_registers_all_nine_counts_on_the_pinned_commit_date() -> None:
    plan = reports.register_plan(reports.packet_path(SQUISH_500))
    result = plan["results.yaml"]
    assert result["scope"]["n_values"] == list(ISSUE)
    assert result["attribution"] == {"source_keys": [SOURCE_KEY], "published": "2026-10-11"}
    assert not plan["source-coverage.yaml"]["beyond_horizon_claims"]
    assert plan["bibliography.yaml"]["dated"] == "2026-10-11"
