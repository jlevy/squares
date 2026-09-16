#!/usr/bin/env python3
"""Summarise the annealing benchmark's per-trial rows into `summaries.json`.

    uv run --frozen --all-extras --group dev squares-workbench-summarize-annealing --check
    uv run --frozen --all-extras --group dev squares-workbench-summarize-annealing --overlaps
    uv run --frozen --all-extras --group dev squares-workbench-summarize-annealing \
        --rows DIR --out PATH

The historical harness, `devtools.bench_annealing` at each round's recorded commit, wrote
one JSON line per trial under `campaign/results/annealing/`. Those rows are not retained in
Git: a round is tens of thousands of lines, and the first night's were 185 MB. Each
round's recorded command, run at that commit, regenerates its rows, and this tool turns
them into the committed summary. It moved from `packing/devtools/` into the workbench
package on 2026-09-15; its output is unchanged.

This is the code that wrote `summaries.json` on 2026-09-12 (`6e191a35`). It was run
inline then and recovered from that session's transcript; what it computes is unchanged.
On 2026-09-14 its `--out` over the 59 local run files was byte-identical to the
committed file. `--check` compares each run file present with its committed entry,
leaving out the median milliseconds, which a regenerated row does not reproduce.

**What a cell holds.** One cell per run file and `n`: the trial count, the record and
grid it was scored against, the median, minimum and maximum of `closed`, the best of the
first k seeds for each k the file reaches, the median milliseconds per trial, and the
parameters of the file's first row.

**What `resolved` means.** A cell is `resolved: true` when its first row carries
`resolved_side`, which the harness writes once it repairs each run to a packing before
scoring. `closed` is then scored on the repaired side; otherwise it is scored on the raw
side, a bounding box around overlapping squares, and the cell is void. The flag does not
mean rows were filtered: this tool counts every row it is given and refuses none.

**What `--overlaps` reports.** Over the run files whose every cell is resolved, the
deepest pairwise overlap before repair, once per distinct run, and the checks X-034
cites from those rows: how many runs ended within the tolerance, whether every repaired
overlap is finite, and whether each (n, level) runs contiguously from seed 0.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

#: `packing/`, where the rows and the committed summaries live.
ROOT = Path(__file__).resolve().parents[4] / "packing"
ROWS = ROOT / "campaign/results/annealing"
SUMMARIES = ROWS / "summaries.json"

#: The k at which a ladder is recorded: the best of the FIRST k seeds of one ordered
#: stream, so one observation per k and not a distribution.
BEST_OF = (1, 10, 100, 1000, 10_000)

#: The deepest overlap, in unit sides, below which the historical rounds counted a final
#: arrangement as a packing, kept so `--overlaps` reproduces the figures X-034 cites. Chosen,
#: not measured: the snapped control said to set it was run once and never kept
#: (`think-2ngs`). The package benchmark admits nothing at this value: it checks geometry
#: under the workbench's validity contract, 1e-9 (`packing_contracts.py`).
TOLERANCE = 1e-5

Row = Mapping[str, Any]


def _closed(row: Row, *, n: int, record: float, resolved: bool) -> float:
    """The fraction of the record-to-grid gap a run closed: 1 is the record, 0 the grid."""
    grid = math.ceil(math.sqrt(n))
    gap = (grid / record - 1) * 100
    if gap <= 0:
        msg = f"n = {n}: the record {record} leaves no gap to the grid {grid} to score"
        raise ValueError(msg)
    excess = (row["resolved_side"] / record - 1) * 100 if resolved else row["excess"]
    return 1 - excess / gap


def summarize_cell(n: int, rows: list[Row]) -> dict[str, Any]:
    """One cell. The record, the parameters and `resolved` are read from the first row."""
    record = rows[0]["record"]
    resolved = "resolved_side" in rows[0]
    closed = [_closed(row, n=n, record=record, resolved=resolved) for row in rows]
    ordered = sorted(zip((row["seed"] for row in rows), closed, strict=True))
    return {
        "trials": len(rows),
        "record": record,
        "grid": math.ceil(math.sqrt(n)),
        "resolved": resolved,
        "closed_median": round(statistics.median(closed), 6),
        "closed_min": round(min(closed), 6),
        "closed_max": round(max(closed), 6),
        "best_of": {
            str(k): round(max(value for _, value in ordered[:k]), 6)
            for k in BEST_OF
            if k <= len(ordered)
        },
        "ms_median": round(statistics.median(row["ms"] for row in rows), 3),
        "params": rows[0].get("params", {}),
    }


def summarize_rows(rows: Iterable[Row]) -> dict[str, dict[str, Any]]:
    """Every `n` in one run file, keyed by `n` as a string, in increasing `n`."""
    by_n: dict[int, list[Row]] = {}
    for row in rows:
        by_n.setdefault(row["n"], []).append(row)
    return {str(n): summarize_cell(n, cells) for n, cells in sorted(by_n.items())}


def _read(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return [json.loads(line) for line in lines if line.strip()]


def summarize(directory: Path) -> dict[str, dict[str, dict[str, Any]]]:
    """Every non-empty `*.jsonl` file in `directory`, keyed by file name."""
    summary: dict[str, dict[str, dict[str, Any]]] = {}
    for path in sorted(directory.glob("*.jsonl")):
        rows = _read(path)
        if rows:
            summary[path.name] = summarize_rows(rows)
    return summary


def render(summary: Mapping[str, Any]) -> str:
    """The committed file's exact serialisation."""
    return json.dumps(summary, indent=1, sort_keys=True) + "\n"


@dataclass(frozen=True)
class OverlapReport:
    """The deepest overlap before repair, once per distinct run."""

    rows: int
    runs: int
    at_or_below_tolerance: int
    overlap_min: float
    overlap_median: float
    overlap_max: float
    repaired_overlap_max: float
    repaired_all_finite: bool
    seeds_contiguous: bool


def overlaps(rows: Iterable[Row]) -> OverlapReport:
    """Distinct runs by (n, level, inflation, style, seed); replays must agree."""
    seen: dict[tuple[Any, ...], float] = {}
    repaired: list[float] = []
    count = 0
    for row in rows:
        count += 1
        params = row.get("params", {})
        key = (row["n"], params.get("anneal"), params.get("inflate"), row["style"], row["seed"])
        if key in seen and seen[key] != row["overlap"]:
            msg = f"two rows for run {key} disagree on its overlap"
            raise ValueError(msg)
        seen[key] = row["overlap"]
        repaired.append(row["resolved_overlap"])
    if not seen:
        msg = "no rows to report"
        raise ValueError(msg)
    values = list(seen.values())
    streams: dict[tuple[Any, ...], list[int]] = {}
    for n, anneal, inflate, style, seed in seen:
        streams.setdefault((n, anneal, inflate, style), []).append(seed)
    return OverlapReport(
        rows=count,
        runs=len(values),
        at_or_below_tolerance=sum(value <= TOLERANCE for value in values),
        overlap_min=min(values),
        overlap_median=statistics.median(values),
        overlap_max=max(values),
        repaired_overlap_max=max(repaired),
        repaired_all_finite=all(math.isfinite(value) for value in repaired),
        seeds_contiguous=all(
            sorted(seeds) == list(range(len(seeds))) for seeds in streams.values()
        ),
    )


#: Cell fields that measure the machine rather than the run. A regenerated row carries the
#: same geometry and a different `ms`, so these are left out of `check`.
TIMING = frozenset({"ms_median"})


def _reproducible(cells: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {n: {k: v for k, v in cell.items() if k not in TIMING} for n, cell in cells.items()}


def check(summary: Mapping[str, Any], committed: Mapping[str, Any]) -> list[str]:
    """Each run file summarised here against its committed entry, timing aside.

    Rows are regenerated a round at a time, so a directory rarely holds all of them and
    absent files are skipped. The caller reports how many files were compared, so a
    partial check never reads as a full one.
    """
    problems = []
    for name, cells in summary.items():
        if name not in committed:
            problems.append(f"{name}: not in {SUMMARIES.name}")
        elif _reproducible(committed[name]) != _reproducible(cells):
            problems.append(f"{name}: cells differ")
    return problems


def _repaired_files(directory: Path) -> list[Path]:
    """The run files whose every cell is resolved, read from the summary of `directory`."""
    return [
        directory / name
        for name, cells in summarize(directory).items()
        if all(cell["resolved"] for cell in cells.values())
    ]


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Summarise the annealing rows into summaries.json."
    )
    parser.add_argument("--rows", type=Path, default=ROWS, help="directory of *.jsonl rows")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--out", type=Path, help="write the summary here")
    mode.add_argument(
        "--check",
        action="store_true",
        help=f"compare each run file present with its entry in {SUMMARIES.relative_to(ROOT)}",
    )
    mode.add_argument(
        "--overlaps", action="store_true", help="report overlaps over the repaired files"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if not any(args.rows.glob("*.jsonl")):
        print(
            f"no rows under {args.rows}; regenerate them with each round's recorded "
            "command (see campaign/results/annealing/README.md)"
        )
        return 1
    if args.overlaps:
        files = _repaired_files(args.rows)
        report = overlaps(row for path in files for row in _read(path))
        print(f"{len(files)} repaired run files, {report.rows:,} rows, {report.runs:,} runs")
        print(f"runs ending at or below {TOLERANCE:g}: {report.at_or_below_tolerance}")
        print(
            f"deepest overlap before repair: min {report.overlap_min:.4f}, "
            f"median {report.overlap_median:.4f}, max {report.overlap_max:.4f}"
        )
        print(
            f"repaired overlap: all finite {report.repaired_all_finite}, "
            f"max {report.repaired_overlap_max:.3g}"
        )
        print(f"seeds contiguous from 0 in every stream: {report.seeds_contiguous}")
        return 0
    summary = summarize(args.rows)
    text = render(summary)
    if args.check:
        committed_text = SUMMARIES.read_text(encoding="utf-8")
        problems = check(summary, json.loads(committed_text))
        for problem in problems:
            print(f"MISMATCH {problem}")
        print(
            f"{len(summary)} of {len(json.loads(committed_text))} committed run files have "
            f"rows under {args.rows}; {len(problems)} mismatch(es)"
        )
        return 1 if problems else 0
    if args.out is None:
        sys.stdout.write(text)
    else:
        args.out.write_text(text, encoding="utf-8")
        print(f"{len(json.loads(text))} run files summarised -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
