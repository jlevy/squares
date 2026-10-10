"""Issue #488: an Evan Daniel format release, imported by declaration.

Francisco Couzo's #488 commit changes nine certificates and keeps 54 unchanged since
#476. The general importer's checks run on it through ``test_upper_bound_reports``;
these hold what is particular to it. Every test reads retained packets only.
"""

from __future__ import annotations

import json
from pathlib import PurePosixPath
from typing import Any

from devtools import upper_bound_reports as reports

COUZO_488 = "couzo-certificates-2026-10-10"
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


def test_the_488_plan_registers_six_counts_and_names_three_it_does_not() -> None:
    plan = reports.register_plan(reports.packet_path(COUZO_488))
    result = plan["results.yaml"]
    assert result["scope"]["n_values"] == [132, 175, 209, 237, 270, 305]
    assert not plan["source-coverage.yaml"]["beyond_horizon_claims"]
    assert "the issue does not name, at n = 303, 338 and 340" in result["notes"]
