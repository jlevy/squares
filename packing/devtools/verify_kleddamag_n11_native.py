"""Retain native parent-core interval pilots and complete verification receipts.

The three pilot rows are the first, weakest and last source intervals. A pilot
is never a complete certificate. Use ``--all`` to select every interval only
after measuring pilot time and allocation behavior.
"""

from __future__ import annotations

import argparse
import json
import platform
import resource
import subprocess
import sys
import time
import tracemalloc
from dataclasses import asdict
from pathlib import Path
from typing import Any, TextIO

from strif import atomic_output_file

from sqpack.fractional.parent_core import load_kleddamag_parent_core
from sqpack.fractional.parent_core_interval import verify_parent_core_rows
from sqpack.fractional.threshold_interval import ThresholdAtomData

REPO = Path(__file__).resolve().parents[2]
SOURCE = (
    REPO
    / "packing/resources/web/external-square-certificates-2026-09-22/kleddamag-11"
    / "global-certificate.json"
)
REVIEWED_SHA256 = "57e9927da5c13f42dd8bcbf8f08c84363635fece626657ee63a810c61cd44458"


def _git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()


def run(
    certificate_path: Path,
    rows: tuple[int, ...] | None,
    batch_size: int,
    workers: int = 1,
    *,
    trace_allocations: bool = True,
    journal: TextIO | None = None,
    source_state: tuple[str, bool] | None = None,
) -> dict[str, Any]:
    """Record source binding, allocations and every selected row's honest verdict."""
    started = time.monotonic()
    certificate = load_kleddamag_parent_core(certificate_path, expected_sha256=REVIEWED_SHA256)
    data = ThresholdAtomData.of(certificate, batch_size=batch_size)
    if source_state is None:
        source_state = _git("rev-parse", "HEAD"), bool(_git("status", "--porcelain"))
    provenance = {
        "git_commit": source_state[0],
        "dirty": source_state[1],
        "python": sys.version,
        "platform": platform.platform(),
        "command": sys.argv,
        "certificate_sha256": REVIEWED_SHA256,
    }
    if journal is not None:
        journal.write(
            json.dumps(
                {
                    "schema": "NativeParentCoreRowJournal/v1",
                    "status": "INCOMPLETE_ROW_JOURNAL",
                    "provenance": provenance,
                    "batch_size": batch_size,
                    "workers": workers,
                    "selected_rows": list(range(len(certificate.rows)))
                    if rows is None
                    else rows,
                }
            )
            + "\n"
        )
        journal.flush()
    row_times: dict[int, float] = {}

    def progress(index: int, outcome: Any, elapsed: float) -> None:
        row_times[index] = elapsed
        if journal is not None:
            journal.write(
                json.dumps(dict(asdict(outcome), index=index, seconds=elapsed)) + "\n"
            )
            journal.flush()
        print(
            f"row {index}: {outcome.status}, {outcome.boxes} boxes, "
            f"{outcome.stalled} stalled, {row_times[index]:.3f}s",
            flush=True,
        )

    if trace_allocations:
        tracemalloc.start()
    verdict = verify_parent_core_rows(
        certificate, rows, batch_size=batch_size, workers=workers, progress=progress
    )
    traced_peak: int | None = None
    if trace_allocations:
        _, traced_peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
    peak_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_child_rss = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    if sys.platform != "darwin":
        peak_rss *= 1024
        peak_child_rss *= 1024
    return {
        "schema": "NativeParentCoreIntervalReceipt/v1",
        "status": "PASS_COMPLETE"
        if verdict.accepted
        else "PASS_PARTIAL"
        if verdict.covered
        else "UNRESOLVED",
        "method": "directed-rounding box branch-and-bound with direct threshold counts",
        "provenance": provenance,
        "bound": str(certificate.outer_side / certificate.parent_side),
        "parent_side": str(certificate.parent_side),
        "minimum_charge": str(certificate.minimum_charge),
        "budget": str(certificate.budget),
        "scale": verdict.scale,
        "threshold_units": verdict.threshold_units,
        "catalogue_rows": len(certificate.rows),
        "complete": verdict.complete,
        "accepted": verdict.accepted,
        "premises": asdict(verdict.premises),
        "batch": {
            "boxes": batch_size,
            "workers": workers,
            "sites": len(data.sites.xlo),
            "features": len(data.members),
            "member_slots": data.members.size,
            "site_mask_bytes": batch_size * len(data.sites.xlo),
            "gathered_member_bytes": batch_size * data.members.size,
            "int16_count_bytes": batch_size * len(data.members) * 2,
        },
        "allocation_tracing": trace_allocations,
        "peak_parent_traced_bytes": traced_peak,
        "peak_parent_process_rss_bytes": peak_rss,
        "peak_child_process_rss_bytes": peak_child_rss,
        "rss_scope": "largest individual process per role; not combined resident memory",
        "seconds": time.monotonic() - started,
        "rows": [
            dict(asdict(outcome), index=index, seconds=row_times[index])
            for index, outcome in zip(verdict.indices, verdict.directions, strict=True)
        ],
        "refutations": [asdict(witness) for witness in verdict.refutations],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=SOURCE)
    select = parser.add_mutually_exclusive_group(required=True)
    select.add_argument("--rows", nargs="+", type=int)
    select.add_argument("--pilot", action="store_true")
    select.add_argument("--all", action="store_true")
    parser.add_argument("--batch-size", type=int, default=2048)
    parser.add_argument("--workers", type=int, choices=(1, 2), default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = None if args.all else (0, 11962, 12027) if args.pilot else tuple(args.rows)
    # Output creation must not make an otherwise clean frozen implementation
    # appear dirty in its own provenance receipt.
    source_state = _git("rev-parse", "HEAD"), bool(_git("status", "--porcelain"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # The append-only journal survives interruption but never claims a completed
    # proof. A run cannot silently reuse or overwrite another run's row journal.
    journal_path = args.output.with_suffix(".rows.jsonl")
    with journal_path.open("x", encoding="utf-8") as journal:
        result = run(
            args.certificate,
            rows,
            args.batch_size,
            args.workers,
            trace_allocations=not args.all,
            journal=journal,
            source_state=source_state,
        )
    with atomic_output_file(args.output) as handle:
        handle.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(f"{result['status']}: {args.output}")
    return 0 if result["status"] in ("PASS_COMPLETE", "PASS_PARTIAL") else 1


if __name__ == "__main__":
    raise SystemExit(main())
