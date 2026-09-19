"""Guarded replacement-support column generation for Route F1 / H-217.

The intended loop, once the A6 sites-1 matrix exists, is checkpointed
replacement-support column generation: price weighted-majority, k-of-S, and
floor atoms on arrangement-vertex sites, then hand a terminal family to the
independent reader ``devtools.decide_relational_certificate`` and the
relational/threshold gate. This command is the OR-1 producer for that loop.
It refuses to run covering without the sites-1 matrix. It does not decide
H-217.

The matrix is unretained (15,021 rows / 17,389 sites). Inspection of that
identity is ``devtools.regenerate_sites1_checkpoint.inspect`` /
``default_layout``; this module does not duplicate those counts. A matching
matrix on disk is acknowledged and still does not run a covering LP: matrix
presence is not permission to spend the H-217 target.

What this command never does:

- Import ``sepcore``, ``lp383``, or any ``*.py.txt`` record.
- Call ``devtools.run_fractional_colgen`` / ``generate_adaptive`` as a
  substitute. That driver is point-atom only; it cannot emit replacement-support
  columns or the sites-1 covering.
- Run the H-217 covering LP.

A relational family JSON, if later present, is a dry hand-off to
``devtools.decide_relational_certificate`` that still refuses without sites-1
and does not call ``decide``.

Usage, from ``packing/`` via ``uv run --frozen --all-extras --group dev``::

    python -m devtools.run_relational_colgen --check
    python -m devtools.run_relational_colgen --output-dir DIR
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass, replace
from pathlib import Path

from strif import atomic_write_text

from devtools import decide_relational_certificate as relational_gate
from devtools.regenerate_sites1_checkpoint import (
    SITES1,
    CheckpointSpec,
    Layout,
    Receipt,
    default_layout,
    repo_relative,
)
from devtools.regenerate_sites1_checkpoint import inspect as inspect_sites1

RECEIPT_NAME = "relational-colgen-receipt.json"
LOG_NAME = "relational-colgen.log"
BEAD = "think-gyzw"
HYPOTHESIS = "H-217"
TOOL = "devtools.run_relational_colgen"
GATE = "devtools.decide_relational_certificate"

# Point-atom adaptive colgen is a different instrument. Naming it here is the
# refusal, not a call.
COLGEN_NOTE = (
    "devtools.run_fractional_colgen drives sqpack.fractional.colgen."
    "generate_adaptive (point-atom adaptive column generation). It is not a "
    "substitute for replacement-support colgen on the sites-1 matrix, and this "
    "command never calls it."
)

GUARD_NOTE = (
    "sites-1 matrix present; covering_ran is false. "
    "Matrix presence is not permission to spend the H-217 target."
)

_REFUSED_FROM_SITES1 = frozenset({"missing-inputs", "missing-producer"})


@dataclass(frozen=True, slots=True)
class ColgenReceipt:
    """Source-bound record of refuse-or-acknowledge. Covering never ran."""

    status: str
    stop_reason: str
    n: int
    sites1: Receipt
    family_handoff: dict[str, object]
    output_dir: Path
    receipt_path: Path
    log_path: Path
    seconds: float = 0.0

    def as_dict(self) -> dict[str, object]:
        return {
            "tool": TOOL,
            "bead": BEAD,
            "hypothesis": HYPOTHESIS,
            "n": self.n,
            "status": self.status,
            "stop_reason": self.stop_reason,
            "rows_complete": False,
            "covering_ran": False,
            "h217_verdict": None,
            "checkpoint_in_repo": self.sites1.checkpoint_in_repo,
            "missing": list(self.sites1.missing),
            "family_handoff": self.family_handoff,
            "gate": GATE,
            "in_tree_colgen": COLGEN_NOTE,
            "sites1": self.sites1.as_dict(),
            "outputs": {
                "directory": repo_relative(self.output_dir),
                "receipt": repo_relative(self.receipt_path),
                "log": repo_relative(self.log_path),
            },
            "seconds": round(self.seconds, 4),
        }


def default_colgen_layout(
    *,
    state: Path | None = None,
    lp_run4: Path | None = None,
    output_dir: Path | None = None,
    resume: Path | None = None,
    receipt: Path | None = None,
    log: Path | None = None,
) -> Layout:
    """Same paths as the sites-1 command, with this tool's receipt and log names."""

    layout = default_layout(
        state=state,
        lp_run4=lp_run4,
        output_dir=output_dir,
        resume=resume,
        receipt=receipt,
        log=log,
    )
    return replace(
        layout,
        receipt=(layout.output_dir / RECEIPT_NAME) if receipt is None else layout.receipt,
        log=(layout.output_dir / LOG_NAME) if log is None else layout.log,
    )


def family_handoff(
    family: Path | None,
    *,
    matrix_present: bool,
) -> dict[str, object]:
    """Dry stub for the independent reader. Does not call ``decide``; does not decide H-217."""

    present = family is not None and family.is_file()
    record: dict[str, object] = {
        "gate": GATE,
        "reader": relational_gate.__name__,
        "decided": False,
        "family_present": present,
    }
    if family is not None:
        record["path"] = repo_relative(family)
    if present and not matrix_present:
        record["status"] = "refused"
        record["reason"] = "relational family present; still refuses without sites-1"
        return record
    if present:
        record["status"] = "stub"
        record["reason"] = "this slice does not decide H-217"
        return record
    record["status"] = "no-family"
    record["reason"] = "no relational family JSON; gate not invoked"
    return record


def inspect_run(
    layout: Layout,
    *,
    spec: CheckpointSpec = SITES1,
    n: int = 11,
    family: Path | None = None,
) -> ColgenReceipt:
    """Decide refuse versus acknowledge. Never solves an LP. Never writes."""

    started = time.perf_counter()
    sites1 = inspect_sites1(layout, spec=spec)
    matrix_present = sites1.status == "retained"
    if matrix_present:
        status = "matrix-present-no-covering"
        stop_reason = "sites-1-present-covering-not-run"
    elif sites1.status in _REFUSED_FROM_SITES1:
        status = sites1.status
        stop_reason = sites1.stop_reason
    else:
        status = "refused"
        stop_reason = sites1.stop_reason
    return ColgenReceipt(
        status=status,
        stop_reason=stop_reason,
        n=n,
        sites1=sites1,
        family_handoff=family_handoff(family, matrix_present=matrix_present),
        output_dir=layout.output_dir,
        receipt_path=layout.receipt,
        log_path=layout.log,
        seconds=time.perf_counter() - started,
    )


def refusal_message(receipt: ColgenReceipt) -> str:
    """Stderr text naming every missing input, and that covering did not run."""

    if receipt.status == "matrix-present-no-covering":
        return GUARD_NOTE
    lines = [
        f"relational colgen refused: {receipt.stop_reason}",
        (
            f"n={receipt.n}; covering_ran=false; h217_verdict=null; "
            f"rows_complete=false; status={receipt.status}"
        ),
        "missing:",
        *(f"  {item}" for item in receipt.sites1.missing),
        COLGEN_NOTE,
    ]
    return "\n".join(lines)


def log_text(receipt: ColgenReceipt) -> str:
    payload = receipt.as_dict()
    return (
        f"status: {payload['status']}\n"
        f"stop_reason: {payload['stop_reason']}\n"
        f"rows_complete: {payload['rows_complete']}\n"
        f"covering_ran: {payload['covering_ran']}\n"
        f"h217_verdict: {payload['h217_verdict']}\n" + json.dumps(payload, indent=1) + "\n"
    )


def write_receipt(receipt: ColgenReceipt) -> None:
    encoded = json.dumps(receipt.as_dict(), indent=1) + "\n"
    atomic_write_text(receipt.receipt_path, encoded, make_parents=True)
    atomic_write_text(receipt.log_path, log_text(receipt), make_parents=True)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument(
        "--check",
        action="store_true",
        help="inspect and print the receipt; write no receipt or log",
    )
    command.add_argument(
        "--n",
        type=int,
        default=11,
        help="instance size; this slice still refuses covering without sites-1",
    )
    command.add_argument("--state", type=Path, default=None)
    command.add_argument(
        "--lp-run4",
        type=Path,
        default=None,
        help="directory holding lp-run4 sites.json, atoms.json, and rows.json",
    )
    command.add_argument(
        "--resume",
        type=Path,
        default=None,
        help="directory holding a sites.json/atoms.json/rows.json checkpoint",
    )
    command.add_argument("--output-dir", type=Path, default=None)
    command.add_argument("--receipt", type=Path, default=None)
    command.add_argument("--log", type=Path, default=None)
    command.add_argument(
        "--family",
        type=Path,
        default=None,
        help="optional relational family JSON; dry hand-off only, never decides H-217",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    options = parser().parse_args(argv)
    if options.n < 1:
        parser().error("--n must be a positive integer")
    layout = default_colgen_layout(
        state=options.state,
        lp_run4=options.lp_run4,
        output_dir=options.output_dir,
        resume=options.resume,
        receipt=options.receipt,
        log=options.log,
    )
    receipt = inspect_run(layout, n=options.n, family=options.family)
    print(json.dumps(receipt.as_dict(), indent=1), flush=True)
    print(refusal_message(receipt), file=sys.stderr)
    if not options.check:
        write_receipt(receipt)
    if receipt.status == "matrix-present-no-covering":
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
