"""Issues #488 and #489: two Evan Daniel format releases, imported by declaration.

Francisco Couzo's #488 commit changes nine certificates and keeps 54 unchanged since
#476; Evan Daniel's #489 commit holds five Hunt 3 certificates, two of them beyond the
case corpus. The general importer's checks run on both through
``test_upper_bound_reports``; these hold what is particular to them. Every test reads
retained packets only.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import PurePosixPath
from typing import Any

from devtools import check_source_coverage as coverage_check
from devtools import upper_bound_reports as reports

COUZO_488 = "couzo-certificates-2026-10-10"
HUNT3 = "evand-record-hunt3-2026-10-10"
COUZO_476 = "couzo-exact-certificates-2026-10-09"
#: The certificates commit 3ef7634 adds (209) or changes; every other one is unchanged.
CHANGED = (132, 175, 209, 237, 270, 303, 305, 338, 340)


def _smallest(name: str) -> dict[int, Any]:
    rows = reports.check_claims(reports.packet_path(name))["results"]
    return {row["n"]: row["smallest"] or row.get("undecided_among") for row in rows}


def test_the_488_packet_retains_what_the_commit_changes_and_pins_the_rest_to_476() -> None:
    record = json.loads(
        (reports.packet_path(COUZO_488) / "acquisition/sources.json").read_text("utf-8")
    )
    (source,) = record["sources"]
    retained = sorted(
        int(path.name[1:-5])
        for path in (reports.REPO / source["archived_path"] / "certificates").glob("*.cert")
    )
    assert retained == list(CHANGED)
    twins = {
        item["path"]: item["identical_to"]
        for item in source["pinned_only"]
        if "identical_to" in item
    }
    assert len(twins) == 54
    prior = f"packing/resources/web/{COUZO_476}/source/certificates"
    for path, twin in twins.items():
        assert PurePosixPath(path).parent.as_posix() == "certificates"
        assert twin == f"{prior}/{PurePosixPath(path).name}"
    assert not {int(PurePosixPath(path).name[1:-5]) for path in twins} & set(CHANGED)


def test_the_488_claims_find_489_smaller_at_132_and_481_smaller_only_at_303() -> None:
    assert _smallest(COUZO_488) == {
        132: "#489",
        175: reports.THIS,
        209: reports.THIS,
        237: reports.THIS,
        270: reports.THIS,
        303: "#481",
        305: reports.THIS,
        338: reports.THIS,
        340: reports.THIS,
    }


def test_the_489_claims_leave_305_undecided_against_488_at_its_printed_side() -> None:
    assert _smallest(HUNT3) == {
        132: reports.THIS,
        305: [reports.THIS, "#488"],
        308: reports.THIS,
        343: reports.THIS,
        344: reports.THIS,
    }
    # The printed comparison cannot decide it: the two exact sides are one number.
    couzo = reports.read_facts(reports.packet_path(COUZO_488))[305]
    hunt = reports.read_facts(reports.packet_path(HUNT3))[305]
    assert couzo.side == hunt.side == Fraction(8975569886103498772971256586313, 5 * 10**29)
    assert couzo.poses != hunt.poses


def test_the_hunt3_plan_records_343_and_344_as_dated_beyond_horizon_rows() -> None:
    plan = reports.register_plan(reports.packet_path(HUNT3))
    assert plan["results.yaml"]["scope"]["n_values"] == [132, 308]
    coverage = plan["source-coverage.yaml"]
    (source,) = coverage["sources"]
    assert source["claims_record"] == (
        f"resources/web/{HUNT3}/acquisition/beyond-horizon-claims.json"
    )
    assert [
        (row["n"], row["value"], row["disposition"])
        for row in coverage["beyond_horizon_claims"]
    ] == [
        (343, "18.978232523635611279730512106023", "tracked-outside-case-corpus"),
        (344, "18.994450514277401521114135796864", "tracked-outside-case-corpus"),
    ]
    claims = coverage_check.load_claims(reports.ROOT / source["claims_record"])
    assert {row["n"]: row["value"] for row in coverage["beyond_horizon_claims"]} == claims


def test_the_488_plan_registers_six_counts_and_names_three_it_does_not() -> None:
    plan = reports.register_plan(reports.packet_path(COUZO_488))
    result = plan["results.yaml"]
    assert result["scope"]["n_values"] == [132, 175, 209, 237, 270, 305]
    assert not plan["source-coverage.yaml"]["beyond_horizon_claims"]
    assert "the issue does not name, at n = 303, 338 and 340" in result["notes"]
