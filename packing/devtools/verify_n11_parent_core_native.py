"""Run the native n11 parent-core checker on an n11 certificate other than Kleddamag's.

`devtools.verify_kleddamag_n11_native` already reads the parent side ``A``, every row's
core side ``B``, the charges, the budget and the minimum charge from the certificate; the
container side ``191/50`` and ``n = 11`` are fixed by the loader, and every n11
certificate retained here keeps them. Its one Kleddamag-specific constant is the SHA-256
pin ``REVIEWED_SHA256``, which binds that tool to Kleddamag's release. This tool clears
the pin for one run and calls the same ``run`` unchanged; the certificate is identified by
its repository path and the Git revision in the receipt's provenance. The receipt adds
``certificate``, that path, and ``proof_inputs``, which names ``PROOF_COMMIT`` -- the
revision of the retained complete Kleddamag run -- and, for information only, which of
that run's inputs have changed since (`proof_input_drift` in
`devtools.audit_kleddamag_n11_native`; ``null`` when this checkout cannot tell).

A certificate retained as ``X.gz`` is read through `devtools.retained_data`, and one inside
the Wang and Li archive through `devtools.audit_wang_li_n11.read_bytes`; either is handed
to the loader as a temporary plain file with the same bytes.

Usage, from ``packing/``::

    .venv/bin/python3 -m devtools.verify_n11_parent_core_native --pilot --output OUT.json
    .venv/bin/python3 -m devtools.verify_n11_parent_core_native --all --workers 2 \\
        --output OUT.json
    .venv/bin/python3 -m devtools.verify_n11_parent_core_native --controls --output OUT.json
"""

from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any
from unittest import mock

from strif import atomic_output_file

from devtools import audit_wang_li_n11 as audit
from devtools import verify_kleddamag_n11_native as frozen
from devtools.audit_kleddamag_n11_native import PROOF_COMMIT, proof_input_drift
from devtools.retained_data import read_retained_bytes
from sqpack.fractional.parent_core import (
    ParentCoreCertificate,
    load_kleddamag_parent_core,
)
from sqpack.fractional.parent_core_interval import verify_parent_core_rows

REPO = frozen.REPO
#: A path inside the retained archive, read from the zip (`audit.read_bytes`).
WANG_LI = audit.IMPROVED
#: The first, the source's weakest, and the last row, as in the frozen pilot.
PILOT_ROWS = (0, 11962, 12027)


def _git(*arguments: str) -> str:
    return subprocess.run(
        ["git", *arguments], cwd=REPO, check=True, capture_output=True, text=True
    ).stdout.strip()


def _relative(path: Path) -> str:
    resolved = path.resolve()
    return str(resolved.relative_to(REPO)) if resolved.is_relative_to(REPO) else str(path)


def run_certificate(
    path: Path,
    rows: tuple[int, ...] | None,
    batch_size: int,
    workers: int,
    *,
    journal_path: Path,
    source_state: tuple[str, bool],
) -> dict[str, Any]:
    """Run the checker without its release pin and note its drift since `PROOF_COMMIT`."""
    drift = proof_input_drift()
    proof_inputs: dict[str, Any] = {
        "proof_commit": PROOF_COMMIT,
        "changed_since": None if drift is None else list(drift),
    }
    with tempfile.TemporaryDirectory(prefix="n11-native-") as scratch:
        plain = Path(scratch) / "certificate.json"
        plain.write_bytes(
            audit.read_bytes(path)
            if path.is_relative_to(audit.RELEASE)
            else read_retained_bytes(path)
        )
        with (
            mock.patch.object(frozen, "REVIEWED_SHA256", None),
            journal_path.open("x", encoding="utf-8") as journal,
        ):
            result = frozen.run(
                plain,
                rows,
                batch_size,
                workers,
                trace_allocations=rows is not None,
                journal=journal,
                source_state=source_state,
            )
    result["certificate"] = _relative(path)
    result["proof_inputs"] = proof_inputs
    return result


def _row_verdict(certificate: ParentCoreCertificate, row: int) -> dict[str, Any]:
    started = time.monotonic()
    try:
        verdict = verify_parent_core_rows(certificate, (row,), workers=1)
    except ValueError as error:
        return {"refused": True, "by": "premises", "error": str(error)}
    except ArithmeticError as error:
        # An interval refutation whose exact witness fails: not accepted, not refuted.
        return {"refused": True, "by": "undecided", "error": str(error)}
    outcome = verdict.directions[0]
    return {
        "refused": not verdict.covered,
        "by": None if verdict.covered else "coverage",
        "status": outcome.status,
        "lower": outcome.lower,
        "boxes": outcome.boxes,
        "stalled": outcome.stalled,
        "threshold_units": verdict.threshold_units,
        "refutations": [asdict(witness) for witness in verdict.refutations],
        "seconds": time.monotonic() - started,
    }


def controls(path: Path) -> dict[str, Any]:
    """Each mutation of `devtools.audit_wang_li_n11.MUTATIONS`, on its rows, must be refused.

    A mutation is written as a temporary certificate and read by the same loader; every
    premise and coverage decision is the frozen code's.
    """
    improved = audit.load(path)
    source = audit.load(audit.SOURCE)
    results: dict[str, Any] = {}
    with tempfile.TemporaryDirectory(prefix="n11-native-control-") as scratch:
        for name, (description, expected, rows, build) in audit.MUTATIONS.items():
            mutated_path = Path(scratch) / f"{name}.json"
            mutated_path.write_text(json.dumps(build(improved, source)))
            started = time.monotonic()
            try:
                certificate = load_kleddamag_parent_core(mutated_path)
            except ValueError as error:
                verdicts = {"load": {"refused": True, "by": "loader", "error": str(error)}}
                bound = None
            else:
                verdicts = {str(row): _row_verdict(certificate, row) for row in rows}
                bound = str(certificate.outer_side / certificate.parent_side)
            results[name] = {
                "description": description,
                "expected_refusal": expected,
                "bound": bound,
                "rows": verdicts,
                "refused": any(verdict["refused"] for verdict in verdicts.values()),
                "seconds": time.monotonic() - started,
            }
    return {
        "schema": "NativeParentCoreControls/v1",
        "certificate": _relative(path),
        "controls": results,
        "status": "PASS_ALL_CONTROLS_REFUSED"
        if all(result["refused"] for result in results.values())
        else "FAIL_A_CONTROL_WAS_ACCEPTED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate", type=Path, default=WANG_LI)
    select = parser.add_mutually_exclusive_group(required=True)
    select.add_argument("--rows", nargs="+", type=int)
    select.add_argument("--pilot", action="store_true")
    select.add_argument("--all", action="store_true")
    select.add_argument("--controls", action="store_true")
    parser.add_argument("--batch-size", type=int, default=2048)
    parser.add_argument("--workers", type=int, choices=(1, 2), default=1)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.controls:
        result = controls(args.certificate)
        with atomic_output_file(args.output, make_parents=True) as handle:
            handle.write_text(json.dumps(result, indent=2, default=str) + "\n")
        print(f"{result['status']}: {args.output}")
        return 0 if result["status"] == "PASS_ALL_CONTROLS_REFUSED" else 1
    rows = None if args.all else PILOT_ROWS if args.pilot else tuple(args.rows)
    # As in the frozen tool: record the source state before any output exists.
    source_state = _git("rev-parse", "HEAD"), bool(_git("status", "--porcelain"))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result = run_certificate(
        args.certificate,
        rows,
        args.batch_size,
        args.workers,
        journal_path=args.output.with_suffix(".rows.jsonl"),
        source_state=source_state,
    )
    with atomic_output_file(args.output) as handle:
        handle.write_text(json.dumps(result, indent=2, default=str) + "\n")
    print(f"{result['status']}: {args.output}")
    return 0 if result["status"] in ("PASS_COMPLETE", "PASS_PARTIAL") else 1


if __name__ == "__main__":
    raise SystemExit(main())
