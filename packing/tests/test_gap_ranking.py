"""`devtools.gap_ranking` ranks the cases open in the verified lane, whatever was reported.

Until 2026-10-12 the tool skipped every case whose *reported* status was not open (D-520).
A case can be reported proved while its verified lane stays open: T-081 made n = 96 and
eight other k^2 - 4 counts so on 2026-10-03, and T-153 made n = 17 so on 2026-10-12. The
tool therefore dropped n = 96 from frontier/README.md's Smallest Open Gaps table and would
have dropped n = 17, the narrowest gap, from its head. Nothing compared the table with
the tool, so the loss went unseen for nine days.

The tests hold the filter on synthetic records that mirror the three shapes (reported and
verified open; reported proved, verified open; proved in both lanes), the relation
between the tool and the record's verified status and corpus count, and the README table
against the tool's output.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from devtools import gap_ranking
from sqpack.cli.validate import FRONTIER_COUNTS
from sqpack.known_best import KNOWN_BEST_CORPUS
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "frontier" / "README.md"

#: How many rows the README's table shows, and the counts it ranks.
README_ROWS = 6
README_LAST_N = 100


def _write_case(directory: Path, n: int, *, status: str, reported_status: str) -> None:
    upper = n**0.5 + 0.5
    lower = n**0.5 + 0.25
    (directory / f"n-{n:03d}.md").write_text(
        "---\n"
        "packing:\n"
        f"  n: {n}\n"
        f"  reported_status: {reported_status}\n"
        f"  status: {status}\n"
        "  reported_upper_bound:\n"
        f"    value: '{upper}'\n"
        "    construction_method: grid\n"
        "  verified_lower_bound:\n"
        f"    value: '{lower}'\n"
        "---\n"
        "Body.\n",
        encoding="utf-8",
    )


def test_a_case_reported_proved_but_open_in_the_verified_lane_is_ranked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _write_case(tmp_path, 11, status="proved", reported_status="proved")
    _write_case(tmp_path, 17, status="open", reported_status="proved")
    _write_case(tmp_path, 44, status="open", reported_status="open")
    _write_case(tmp_path, 96, status="open", reported_status="proved")
    monkeypatch.setattr(gap_ranking, "FRONTIER", tmp_path)

    ranked = {case.n for case in gap_ranking.open_cases()}

    assert ranked == {17, 44, 96}


def _records() -> list[dict[str, object]]:
    return [
        safe_load(path.read_text(encoding="utf-8").split("---\n")[1])["packing"]
        for path in sorted(gap_ranking.FRONTIER.glob("n-*.md"))
    ]


def test_the_ranked_cases_are_exactly_the_verified_open_cases_of_the_record() -> None:
    records = _records()
    verified_open = {record["n"] for record in records if record["status"] == "open"}
    reported_only = {
        record["n"]
        for record in records
        if record["status"] == "open" and record["reported_status"] != "open"
    }
    proved = {record["n"] for record in records if record["status"] == "proved"}

    ranked = [case.n for case in gap_ranking.open_cases()]

    assert len(ranked) == len(set(ranked))
    assert set(ranked) == verified_open
    assert len(ranked) == FRONTIER_COUNTS[KNOWN_BEST_CORPUS.label][0]
    # The defect's shape must exist in the record for the relation above to bite.
    assert reported_only, "no case is reported closed and verified open any more"
    assert reported_only <= set(ranked)
    assert proved.isdisjoint(ranked)


def _readme_table() -> list[tuple[int, str]]:
    text = README.read_text(encoding="utf-8")
    section = text.split("### Smallest Open Gaps", 1)[1].split("\n#", 1)[0]
    rows = re.findall(r"^\| (\d+) \| (\d\.\d{4}) \|", section, flags=re.MULTILINE)
    return [(int(n), gap) for n, gap in rows]


def test_the_readme_table_is_the_tools_head_of_the_ranking() -> None:
    expected = [
        (case.n, f"{case.gap:.4f}")
        for case in gap_ranking.open_cases()
        if case.n <= README_LAST_N
    ][:README_ROWS]

    assert _readme_table() == expected
