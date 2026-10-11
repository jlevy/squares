"""Evan Daniel's display-regularized record lists: fifteen certificates below the register.

The lists hold one exact certificate per count for ``n = 1..324``; the packet retains
the fifteen whose sides were below every value the register held when they were read,
each as its upstream gzip beside its 50-digit JSON. The general importer's checks run
on the packet through ``test_upper_bound_reports``; these hold what is particular to it.
Every test reads retained packets only.
"""

from __future__ import annotations

import gzip
import json
from fractions import Fraction
from pathlib import PurePosixPath
from typing import Any

from devtools import upper_bound_reports as reports

REGULARIZED = "evand-regularized-2026-10-10"
COUNTS = (70, 102, 103, 123, 129, 146, 153, 236, 258, 263, 269, 292, 295, 302, 303)
CERTS = "search/regularize/lists/certs"
#: Each pending report the claim record reads from its own packet, and where.
EXACT_READS = {
    "#470": (103, 258, 302, 303),
    "#476": (263, 269, 303),
    "#481": (153, 236, 263, 269, 292, 302, 303),
    "#483": (70,),
    "#488": (303,),
}
READERS = {
    "#470": "[Mishapolk decimal poses 2026-10-09]",
    "#476": "[Couzo exact certificates 2026-10-09]",
    "#481": "[SQUISH third request 2026-10-09]",
    "#483": "[Deleeuw n70 refinement 2026-10-10]",
    "#488": "[Couzo certificates 2026-10-10]",
}


def _source() -> dict[str, Any]:
    path = reports.packet_path(REGULARIZED) / "acquisition/sources.json"
    (source,) = json.loads(path.read_text("utf-8"))["sources"]
    return source


def _rows() -> dict[int, dict[str, Any]]:
    rows = reports.check_claims(reports.packet_path(REGULARIZED))["results"]
    return {row["n"]: row for row in rows}


def test_the_packet_retains_the_fifteen_certificates_and_their_json_as_upstream_gzip() -> None:
    source = _source()
    expected = [
        f"source/{CERTS}/n-{n:03d}.{kind}.gz" for n in COUNTS for kind in ("cert", "json")
    ]
    assert source["original_gzip"] == expected
    assert source["compressed"] == []
    pinned = {item["path"]: item for item in source["pinned_only"]}
    assert sorted(pinned) == [
        "search/exact/verify_cert.py",
        "search/exact/verify_cert2.py",
        "search/regularize/lists/best.csv",
        "search/regularize/lists/best.json",
        "site/data/records2026.json",
    ]
    issue_399 = (
        "packing/resources/web/evand-new-arrangements-2026-10-07/source/s12/search/exact"
    )
    for name in ("verify_cert.py", "verify_cert2.py"):
        twin = pinned[f"search/exact/{name}"]["identical_to"]
        assert twin == f"{issue_399}/{name}"
    others = ("search/regularize/lists/best.csv", "search/regularize/lists/best.json")
    assert not any("identical_to" in pinned[path] for path in others)


def test_each_certificate_states_the_side_its_json_prints_and_disclaims_a_new_bound() -> None:
    """The row offers the exact ``S_cert``; the JSON says the view is not a new bound."""
    packet = reports.packet_path(REGULARIZED)
    declaration = reports.load_declaration(packet)
    certificates = reports.read_facts(packet)
    archived = reports.REPO / str(_source()["archived_path"])
    assert [row["n"] for row in declaration["certificates"]] == list(COUNTS)
    for row in declaration["certificates"]:
        n = row["n"]
        json_path = f"{CERTS}/n-{n:03d}.json.gz"
        assert row["path"] == f"{CERTS}/n-{n:03d}.cert.gz"
        assert PurePosixPath(row.get("printed_in", "")).name == f"n-{n:03d}.json.gz"
        assert row["first_committed"] == "2026-10-10T18:05:38Z"
        printed = json.loads(gzip.decompress((archived / json_path).read_bytes()))
        assert printed["n"] == n
        assert Fraction(printed["S_cert"]) == certificates[n].side == Fraction(row["offered"])
        assert printed["note"] == (
            "regularized display view of a certified packing at the same side; not a new bound"
        )
        # The certificate scales the exact point by about 1 + 1e-20 (REGULARIZE.md).
        ratio = certificates[n].side / Fraction(printed["S_exact"]) - 1
        assert Fraction(99, 10**22) < ratio < Fraction(101, 10**22)


def test_the_claims_find_each_certificate_below_its_house_and_every_pending_report() -> None:
    rows = _rows()
    assert sorted(rows) == list(COUNTS)
    for n, row in rows.items():
        assert row["smallest"] == reports.THIS, n
        assert row["case"]["relation"] == "below", n
        assert all(other["relation"] == "below" for other in row["pending"]), n
    smallest_held = {
        n: min(
            [Fraction(row["case"]["exact_side"])]
            + [Fraction(other["exact_side"]) for other in row["pending"]]
        )
        - Fraction(row["exact_side"])
        for n, row in rows.items()
    }
    assert min(smallest_held.values()) == smallest_held[302] > 0
    assert max(smallest_held.values()) == smallest_held[295]
    assert f"{float(smallest_held[302]):.2e}" == "2.21e-17"
    assert f"{float(smallest_held[295]):.2e}" == "7.82e-10"


def test_each_pending_report_is_read_at_its_exact_side_from_its_own_packet() -> None:
    """Every pending report has a retained packet, so none is compared at a print."""
    read = {
        (n, other["report"]): other for n, row in _rows().items() for other in row["pending"]
    }
    assert sorted(read) == sorted(
        (n, report) for report, counts in EXACT_READS.items() for n in counts
    )
    for (n, report), other in read.items():
        assert "printed" not in other
        assert Fraction(other["exact_side"]) == reports.house_side(READERS[report], n)


def test_the_plan_registers_all_fifteen_counts_at_the_lists_first_commit() -> None:
    plan = reports.register_plan(reports.packet_path(REGULARIZED))
    result = plan["results.yaml"]
    assert result["scope"]["n_values"] == list(COUNTS)
    assert result["attribution"]["published"] == "2026-10-10"
    assert "the issue does not name" not in result["notes"]
    assert not plan["source-coverage.yaml"]["beyond_horizon_claims"]
    bibliography = plan["bibliography.yaml"]
    assert bibliography["lineage"] == "builds-on-project"
    assert "Levy" in bibliography["credit"]
