"""The review's two Markdown tables, printed on standard output.

1. The per-count verdict table, from `recompute.py`'s verdict rows (by default the retained
   `recompute-output.txt` beside this file).
2. The provenance sample: 15 claims of `ledger.yaml` drawn with seed 20261014, each with
   the lane row or the issue print it was checked against.

The lane rows behind the sample are read from the packet on `main` where it is there and
otherwise from `PINNED/lanes/<lane>/<packet>/`; issue #593's text from
`PINNED/github/issue-593.json`. From `packing/`, with the project interpreter::

    python campaign/issue-intake/upper-bounds-20261014/review/tables.py PINNED [OUTPUT]
"""

from __future__ import annotations

import ast
import json
import random
import re
import sys
from pathlib import Path
from typing import Any

import yaml

#: The repository root: this file is packing/campaign/issue-intake/<directory>/review/.
REPO = Path(__file__).resolve().parents[5]
PACKETS = REPO / "packing/resources/web"
LEDGER_DIR = REPO / "packing/campaign/issue-intake/upper-bounds-20261014"
LANE_FILES = {
    "#593": ("mishapolk", "mishapolk-records-2026-10-14", "claims.json"),
    "PR #574": ("pr574", "pingyou-pr574-certificates-2026-10-13", "claims.json"),
    "PR #574 alg": ("pr574", "pingyou-pr574-certificates-2026-10-13", "algebraic-claims.json"),
    "franciscouzo/square-packing@4596670": (
        "couzo",
        "couzo-certificates-2026-10-13",
        "claims.json",
    ),
}
SOURCES = {
    "#593": "mishapolk lane claims.json at d4c198d0d + issue #593 table",
    "PR #574": "pr574 lane {record} at f817bf191 + PR commit dates",
    "franciscouzo/square-packing@4596670": (
        "couzo lane claims.json at f8ecf2173 + commit 4596670 date"
    ),
}


def verdict_rows(output: Path) -> list[tuple[Any, ...]]:
    """`recompute.py`'s verdict rows: (n, report, ledger, mine, agree[, note])."""
    rows = []
    for line in output.read_text(encoding="utf-8").splitlines():
        if not (line.startswith("  (") and line.strip().endswith(")") and "'" in line):
            continue
        try:
            row = ast.literal_eval(line.strip())
        except ValueError, SyntaxError:
            continue
        if (
            isinstance(row, tuple)
            and len(row) >= 5
            and isinstance(row[0], int)
            and isinstance(row[4], bool)
        ):
            rows.append(row)
    return rows


def verdict_table(rows: list[tuple[Any, ...]]) -> list[str]:
    by_n: dict[int, list[tuple[Any, ...]]] = {}
    for row in rows:
        by_n.setdefault(row[0], []).append(row)
    table = ["| n | report: ledger verdict → recomputed | agree |", "| ---: | --- | --- |"]
    for n in sorted(by_n):
        cells = []
        for row in by_n[n]:
            if row[2] == row[3]:
                cells.append(f"{row[1]}: {row[2]}")
                continue
            note = row[5:6]
            mark = " (interval cannot prove equality)" if note and note[0] else " **DISAGREE**"
            cells.append(f"{row[1]}: {row[2]} → {row[3]}{mark}")
        agree = all(row[4] for row in by_n[n])
        table.append(f"| {n} | {'; '.join(cells)} | {'yes' if agree else 'NO'} |")
    disagreeing = [n for n in by_n if not all(row[4] for row in by_n[n])]
    table.append("")
    table.append(
        f"verdict table: {len(rows)} steps at {len(by_n)} counts; disagreeing counts: "
        f"{disagreeing}"
    )
    return table


def lane_row(pinned: Path, report: str, n: int, *, exact: bool) -> dict[str, Any]:
    key = report if (exact or report != "PR #574") else "PR #574 alg"
    lane, packet, record = LANE_FILES[key]
    on_main = PACKETS / packet / "acquisition" / record
    path = on_main if on_main.is_file() else pinned / "lanes" / lane / packet / record
    data = json.loads(path.read_text(encoding="utf-8"))
    return next(row for row in data["results"] if int(row["n"]) == n)


def checks(
    claim: dict[str, Any], report: str, row: dict[str, Any], prints: dict[int, str]
) -> tuple[list[str], str]:
    """What the sample row's ledger fields were checked against, one phrase each."""
    found = []
    if "exact" in claim:
        found.append(
            "exact==lane exact_side" if row["exact_side"] == claim["exact"] else "EXACT DIFFERS"
        )
    if report == "#593":
        same = prints.get(claim["n"]) == claim["printed"]
        found.append("printed==issue table" if same else "PRINT DIFFERS")
    elif "offered_side" in row:
        found.append(
            "printed==lane offered_side"
            if row["offered_side"] == claim["printed"]
            else f"printed {claim['printed']} vs lane {row['offered_side']}"
        )
    else:
        same = row["side_decimal"] == claim["printed"]
        found.append("printed==lane side_decimal" if same else "PRINT DIFFERS")
    lane_time = row["first_committed"]
    found.append(
        "first_committed==lane"
        if lane_time == claim.get("first_committed")
        else f"first_committed {claim.get('first_committed')} vs lane {lane_time}"
    )
    return found, lane_time


def provenance_sample(pinned: Path) -> list[str]:
    ledger = yaml.safe_load((LEDGER_DIR / "ledger.yaml").read_text(encoding="utf-8"))
    body = json.loads((pinned / "github/issue-593.json").read_text(encoding="utf-8"))["body"]
    prints = {
        int(m.group(1)): m.group(2)
        for m in re.finditer(r"\|\s*\*\*(\d+)\*\*\s*\|\s*(\d+\.\d+)\s*\|", body)
    }
    claims = [(r["report"], c) for r in ledger["reports"] for c in r["claims"]]
    random.seed(20261014)
    sample = [(report, claim["n"]) for report, claim in random.sample(claims, 15)]
    table = [
        (
            "| # | report, n | ledger: printed (rounding) / exact? / first_committed / "
            "reported_at | source read here | match |"
        ),
        "| ---: | --- | --- | --- | --- |",
    ]
    for index, (report, n) in enumerate(sample, 1):
        entry = next(r for r in ledger["reports"] if r["report"] == report)
        claim = next(c for c in entry["claims"] if c["n"] == n)
        exact = "exact" in claim
        row = lane_row(pinned, report, n, exact=exact)
        found, lane_time = checks(claim, report, row, prints)
        expected = entry["reported_at"]
        if (report == "PR #574" and lane_time > expected) or report.startswith("franciscouzo/"):
            expected = lane_time
        actual = claim.get("reported_at", entry["reported_at"])
        found.append(
            "reported_at as expected"
            if actual == expected
            else f"reported_at {actual} vs expected {expected}"
        )
        record = "claims.json" if exact else "algebraic-claims.json"
        source = SOURCES[report].format(record=record)
        printed = claim["printed"][:22] + ("…" if len(claim["printed"]) > 22 else "")
        fields = (
            f"{printed} ({claim['rounding']}) / {'yes' if exact else 'no'} / "
            f"{claim.get('first_committed')} / {actual}"
        )
        table.append(f"| {index} | {report}, {n} | {fields} | {source} | {'; '.join(found)} |")
    return table


def main() -> None:
    pinned = Path(sys.argv[1])
    output = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else Path(__file__).with_name("recompute-output.txt")
    )
    for line in verdict_table(verdict_rows(output)):
        print(line)
    print()
    for line in provenance_sample(pinned):
        print(line)


if __name__ == "__main__":
    main()
