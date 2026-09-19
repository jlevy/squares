"""Retain or refuse the A6 sites-1 checkpoint at L = 153/40.

The rows-complete covering LP at 153/40 that H-217 wants to price majority and
floor atoms against is the A6 ``sites-1`` matrix: 15,021 carried rows, 17,389
sites in 2,250 D4 orbits, 2,566 two-of-three atom orbits. Lane A3 built it from
the unretained ``spike-b/resume/lp-run4`` threshold checkpoint, scaled by
``765/764``, then one vertex-oracle round that added 300 site orbits. The
matrix itself was never committed (about 60 MB of ``sites.json`` / ``atoms.json``
/ ``rows.json`` / ``x.npy`` / ``duals.npy``).

This command is the in-tree producer for that checkpoint (OR-1). It does not
import the scratch ``.py.txt`` drivers. It does not run the H-217 covering LP.

What it can do:

- If a matching sites-1 matrix is already on disk, retain it with SHA-256
  digests and write no new matrix.
- If the matrix is absent, inspect the producer inputs and the in-tree APIs
  and refuse with a precise missing-input list. ``devtools.run_fractional_colgen``
  is the point-atom adaptive driver; it cannot emit this threshold matrix.
- ``--check`` performs that inspection and writes nothing.

What it cannot do until the missing inputs and APIs exist: regenerate the 300
oracle orbits. That round lived in scratch ``sepcore.FamilyGeometry`` and
``lp383.HighsLP``, which this repository holds only as ``.py.txt`` records.

Usage, from ``packing/``::

    python -m devtools.regenerate_sites1_checkpoint --check
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from collections.abc import Sequence
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from strif import atomic_write_text

PACKING = Path(__file__).resolve().parent.parent
REPO = PACKING.parent
RESULTS = PACKING / "campaign/series/series-000-smoke-and-calibration/results"
DEFAULT_STATE = RESULTS / "bc-200-state-191-50.json"
DEFAULT_OUTPUT_DIR = RESULTS / "agenda-037"
DEFAULT_LP_RUN4 = DEFAULT_OUTPUT_DIR / "lp-run4"
SCRATCH_PRODUCER = RESULTS / "agenda-034" / "lane-a3-lp-sites.py.txt"
TRAJECTORY_RECORD = RESULTS / "agenda-034" / "lane-a3-trajectory-153-40-sites.json"
HISTORICAL_LP_RUN4 = "spike-b/resume/lp-run4"

# The A6 sites-1 identity. Changing these is a different checkpoint.
OUTER_SIDE = Fraction(153, 40)
SQUARE_SIDE = Fraction(9977, 10000)
N = 11
EXPECTED_ROWS = 15_021
EXPECTED_SITES = 17_389
EXPECTED_SITE_ORBITS = 2_250
EXPECTED_ATOM_ORBITS = 2_566
STAGE = "sites-1"

# Scratch modules the original producer imported. They are not in-tree, and
# loading the retained ``.py.txt`` copies would promote them.
PRODUCER_GAPS = (
    "sepcore.FamilyGeometry.vertex_candidates",
    "sepcore.atom_columns",
    "lp383.HighsLP",
)

CHECKPOINT_JSON = ("sites-1-sites.json", "sites-1-atoms.json", "sites-1-rows.json")
RESUME_JSON = ("sites.json", "atoms.json", "rows.json")
LP_RUN4_JSON = ("sites.json", "atoms.json", "rows.json")

COLGEN_NOTE = (
    "devtools.run_fractional_colgen drives sqpack.fractional.colgen."
    "generate_adaptive (point-atom adaptive column generation). It does not "
    "carry two-of-three atom orbits, the 15,021 lp-run4 rows, or the "
    "arrangement-vertex site oracle, so it cannot emit the sites-1 matrix."
)


@dataclass(frozen=True, slots=True)
class CheckpointSpec:
    """Counts and side that identify one sites-1-shaped matrix."""

    outer_side: Fraction
    square_side: Fraction
    n: int
    rows: int
    sites: int
    site_orbits: int
    atom_orbits: int
    stage: str = STAGE

    def as_dict(self) -> dict[str, object]:
        return {
            "outer_side": str(self.outer_side),
            "square_side": str(self.square_side),
            "n": self.n,
            "rows": self.rows,
            "sites": self.sites,
            "site_orbits": self.site_orbits,
            "atom_orbits": self.atom_orbits,
            "stage": self.stage,
        }


SITES1 = CheckpointSpec(
    outer_side=OUTER_SIDE,
    square_side=SQUARE_SIDE,
    n=N,
    rows=EXPECTED_ROWS,
    sites=EXPECTED_SITES,
    site_orbits=EXPECTED_SITE_ORBITS,
    atom_orbits=EXPECTED_ATOM_ORBITS,
)


@dataclass(frozen=True, slots=True)
class Layout:
    """Paths the command reads and, when not ``--check``, may write."""

    state: Path
    lp_run4: Path
    output_dir: Path
    receipt: Path
    log: Path
    resume: Path | None = None
    scratch_producer: Path = SCRATCH_PRODUCER
    trajectory_record: Path = TRAJECTORY_RECORD


@dataclass(frozen=True, slots=True)
class FileRecord:
    """One path the receipt is answerable for."""

    role: str
    path: Path
    present: bool
    sha256: str | None = None
    detail: str | None = None

    def as_dict(self) -> dict[str, object]:
        record: dict[str, object] = {
            "role": self.role,
            "path": repo_relative(self.path),
            "present": self.present,
        }
        if self.sha256 is not None:
            record["sha256"] = self.sha256
        if self.detail is not None:
            record["detail"] = self.detail
        return record


@dataclass(frozen=True, slots=True)
class CheckpointCounts:
    """What a sites/atoms/rows triple actually holds."""

    rows: int
    sites: int
    site_orbits: int
    atom_orbits: int
    outer_side: str | None


@dataclass(frozen=True, slots=True)
class Receipt:
    """Source-bound record of retain, refuse, or (later) regenerate."""

    status: str
    stop_reason: str
    spec: CheckpointSpec
    checkpoint_in_repo: bool
    producer_ready: bool
    rows_complete: bool
    inputs: tuple[FileRecord, ...]
    checkpoint_files: tuple[FileRecord, ...]
    producer_gaps: tuple[str, ...]
    missing: tuple[str, ...]
    output_dir: Path
    receipt_path: Path
    log_path: Path
    observed: CheckpointCounts | None = None
    deadline_seconds: float | None = None
    seconds: float = 0.0

    def as_dict(self) -> dict[str, object]:
        return {
            "tool": "devtools.regenerate_sites1_checkpoint",
            "bead": "think-3xbr",
            "status": self.status,
            "stop_reason": self.stop_reason,
            "rows_complete": self.rows_complete,
            "checkpoint_in_repo": self.checkpoint_in_repo,
            "producer_ready": self.producer_ready,
            "expected": self.spec.as_dict(),
            "observed": None
            if self.observed is None
            else {
                "rows": self.observed.rows,
                "sites": self.observed.sites,
                "site_orbits": self.observed.site_orbits,
                "atom_orbits": self.observed.atom_orbits,
                "outer_side": self.observed.outer_side,
            },
            "scratch_producer": repo_relative(SCRATCH_PRODUCER),
            "historical_lp_run4": HISTORICAL_LP_RUN4,
            "in_tree_colgen": COLGEN_NOTE,
            "producer_gaps": list(self.producer_gaps),
            "missing": list(self.missing),
            "inputs": [item.as_dict() for item in self.inputs],
            "checkpoint_files": [item.as_dict() for item in self.checkpoint_files],
            "outputs": {
                "directory": repo_relative(self.output_dir),
                "sites": repo_relative(self.output_dir / CHECKPOINT_JSON[0]),
                "atoms": repo_relative(self.output_dir / CHECKPOINT_JSON[1]),
                "rows": repo_relative(self.output_dir / CHECKPOINT_JSON[2]),
                "receipt": repo_relative(self.receipt_path),
                "log": repo_relative(self.log_path),
            },
            "deadline_seconds": self.deadline_seconds,
            "seconds": round(self.seconds, 4),
        }


def default_layout(
    *,
    state: Path | None = None,
    lp_run4: Path | None = None,
    output_dir: Path | None = None,
    resume: Path | None = None,
    receipt: Path | None = None,
    log: Path | None = None,
) -> Layout:
    """Repository defaults: agenda-037 output, retained 191/50 state, no lp-run4."""

    out = DEFAULT_OUTPUT_DIR if output_dir is None else output_dir
    return Layout(
        state=DEFAULT_STATE if state is None else state,
        lp_run4=DEFAULT_LP_RUN4 if lp_run4 is None else lp_run4,
        output_dir=out,
        resume=resume,
        receipt=out / "sites-1-receipt.json" if receipt is None else receipt,
        log=out / "sites-1.log" if log is None else log,
    )


def repo_relative(path: Path) -> str:
    """Repository-relative POSIX path when the file sits in this checkout."""

    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO).as_posix()
    except ValueError:
        return resolved.as_posix()


def file_digest(path: Path) -> str:
    """SHA-256 of a file, chunked so a 60 MB matrix is cheap to name."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def record_file(role: str, path: Path, *, detail: str | None = None) -> FileRecord:
    present = path.is_file()
    return FileRecord(
        role=role,
        path=path,
        present=present,
        sha256=None if not present else file_digest(path),
        detail=detail,
    )


def _site_counts(path: Path) -> tuple[int, int] | None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return None
    orbits = 0
    sites = 0
    for orbit in payload:
        if not isinstance(orbit, list):
            return None
        orbits += 1
        sites += len(orbit)
    return orbits, sites


def _atom_count(path: Path) -> tuple[int, str | None] | None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        return None
    atoms = payload.get("atoms")
    if not isinstance(atoms, list):
        return None
    side = payload.get("outer_side")
    return len(atoms), None if side is None else str(side)


def _row_count(path: Path) -> int | None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return None
    return len(payload)


def read_counts(sites: Path, atoms: Path, rows: Path) -> CheckpointCounts | None:
    """Counts from a producer-style sites/atoms/rows triple, or None if unreadable."""

    try:
        site_counts = _site_counts(sites)
        atom_counts = _atom_count(atoms)
        row_count = _row_count(rows)
    except OSError, TypeError, ValueError, KeyError:
        return None
    if site_counts is None or atom_counts is None or row_count is None:
        return None
    site_orbits, n_sites = site_counts
    n_atoms, outer_side = atom_counts
    return CheckpointCounts(
        rows=row_count,
        sites=n_sites,
        site_orbits=site_orbits,
        atom_orbits=n_atoms,
        outer_side=outer_side,
    )


def counts_match(observed: CheckpointCounts, spec: CheckpointSpec) -> bool:
    if (
        observed.rows != spec.rows
        or observed.sites != spec.sites
        or observed.site_orbits != spec.site_orbits
        or observed.atom_orbits != spec.atom_orbits
    ):
        return False
    if observed.outer_side is None:
        return True
    try:
        return Fraction(observed.outer_side) == spec.outer_side
    except TypeError, ValueError, ZeroDivisionError:
        return False


def checkpoint_triple(directory: Path, names: tuple[str, str, str]) -> tuple[Path, Path, Path]:
    return directory / names[0], directory / names[1], directory / names[2]


def locate_checkpoint(layout: Layout) -> tuple[tuple[Path, Path, Path], str] | None:
    """A resume directory, then the agenda-037 ``sites-1-*`` names."""

    if layout.resume is not None:
        triple = checkpoint_triple(layout.resume, RESUME_JSON)
        if any(path.is_file() for path in triple):
            return triple, "resume"
    triple = checkpoint_triple(layout.output_dir, CHECKPOINT_JSON)
    if any(path.is_file() for path in triple):
        return triple, "output"
    return None


def producer_ready() -> bool:
    """True only when the site oracle and incremental HiGHS live in sqpack.

    The original loop imported both from scratch. Promoting the ``.py.txt``
    copies is out of scope; this stays false until those APIs exist as
    importable in-tree modules.
    """

    return False


def _verdict(
    *,
    observed: CheckpointCounts | None,
    spec: CheckpointSpec,
    inputs_present: bool,
    ready: bool,
    missing: list[str],
) -> tuple[str, str, bool, list[str]]:
    """Retain, count-mismatch, missing-inputs, or missing-producer.

    ``rows_complete`` is not a verdict this function can reach: that stop rule
    fires only after a 181-direction sweep finds no violated cell, and this
    command never runs that sweep.
    """

    if observed is not None and counts_match(observed, spec):
        return "retained", "retained-existing-checkpoint", True, []
    if observed is not None:
        mismatch = (
            f"observed rows={observed.rows} sites={observed.sites} "
            f"site_orbits={observed.site_orbits} atom_orbits="
            f"{observed.atom_orbits} outer_side={observed.outer_side}; "
            f"expected rows={spec.rows} sites={spec.sites} site_orbits="
            f"{spec.site_orbits} atom_orbits={spec.atom_orbits} outer_side="
            f"{spec.outer_side}"
        )
        return "count-mismatch", "count-mismatch", False, [mismatch, *missing]
    if not inputs_present:
        return "missing-inputs", "missing-inputs", False, missing
    if not ready:
        return "missing-producer", "missing-producer", False, missing
    missing.append("regeneration-not-implemented")
    return "missing-producer", "regeneration-not-implemented", False, missing


def inspect(
    layout: Layout,
    *,
    spec: CheckpointSpec = SITES1,
    deadline_seconds: float | None = None,
) -> Receipt:
    """Decide retain versus refuse. Never solves an LP. Never writes."""

    started = time.perf_counter()
    located = locate_checkpoint(layout)
    if located is None:
        checkpoint_paths = checkpoint_triple(layout.output_dir, CHECKPOINT_JSON)
        origin = "output"
    else:
        checkpoint_paths, origin = located
    sites_path, atoms_path, rows_path = checkpoint_paths
    checkpoint_files = (
        record_file(f"{origin}-sites", sites_path),
        record_file(f"{origin}-atoms", atoms_path),
        record_file(f"{origin}-rows", rows_path),
    )
    observed = None
    if all(path.is_file() for path in checkpoint_paths):
        observed = read_counts(sites_path, atoms_path, rows_path)

    lp_sites, lp_atoms, lp_rows = checkpoint_triple(layout.lp_run4, LP_RUN4_JSON)
    inputs = (
        record_file(
            "state-191-50",
            layout.state,
            detail="BC-200 point-LP state; the original producer asserted "
            "it as the prefix of lp-run4 sites.json",
        ),
        record_file(
            "lp-run4-sites",
            lp_sites,
            detail="191/50 threshold site orbits; unretained with lp-run4",
        ),
        record_file(
            "lp-run4-atoms",
            lp_atoms,
            detail="191/50 two-of-three atom orbits; unretained with lp-run4",
        ),
        record_file(
            "lp-run4-rows",
            lp_rows,
            detail="15,021 rows-complete rows at 191/50; unretained with lp-run4",
        ),
        record_file(
            "scratch-producer",
            layout.scratch_producer,
            detail="lane A3 site-loop record; not an importable module",
        ),
        record_file(
            "trajectory-record",
            layout.trajectory_record,
            detail="A3 sites-1 counts only; not the matrix",
        ),
    )

    missing: list[str] = []
    ready = producer_ready()
    gaps = () if ready else PRODUCER_GAPS
    if not layout.state.is_file():
        missing.append(f"state-191-50: {repo_relative(layout.state)}")
    for role, path in (
        ("lp-run4-sites", lp_sites),
        ("lp-run4-atoms", lp_atoms),
        ("lp-run4-rows", lp_rows),
    ):
        if not path.is_file():
            missing.append(f"{role}: {repo_relative(path)}")
    if not ready:
        missing.extend(gaps)

    status, stop_reason, in_repo, missing = _verdict(
        observed=observed,
        spec=spec,
        inputs_present=(
            layout.state.is_file()
            and lp_sites.is_file()
            and lp_atoms.is_file()
            and lp_rows.is_file()
        ),
        ready=ready,
        missing=missing,
    )
    return Receipt(
        status=status,
        stop_reason=stop_reason,
        spec=spec,
        checkpoint_in_repo=in_repo,
        producer_ready=ready,
        rows_complete=False,
        inputs=inputs,
        checkpoint_files=checkpoint_files,
        producer_gaps=gaps,
        missing=tuple(missing),
        output_dir=layout.output_dir,
        receipt_path=layout.receipt,
        log_path=layout.log,
        observed=observed,
        deadline_seconds=deadline_seconds,
        seconds=time.perf_counter() - started,
    )


def refusal_message(receipt: Receipt) -> str:
    """Stderr text naming every missing input and API, and nothing else."""

    lines = [
        f"sites-1 regeneration refused: {receipt.stop_reason}",
        (
            f"expected {receipt.spec.stage} at L={receipt.spec.outer_side}: "
            f"{receipt.spec.rows} rows, {receipt.spec.sites} sites in "
            f"{receipt.spec.site_orbits} D4 orbits, {receipt.spec.atom_orbits} "
            "two-of-three atom orbits"
        ),
        "missing:",
        *(f"  {item}" for item in receipt.missing),
        COLGEN_NOTE,
    ]
    return "\n".join(lines)


def log_text(receipt: Receipt) -> str:
    payload = receipt.as_dict()
    return (
        f"status: {payload['status']}\n"
        f"stop_reason: {payload['stop_reason']}\n"
        f"rows_complete: {payload['rows_complete']}\n"
        f"checkpoint_in_repo: {payload['checkpoint_in_repo']}\n"
        f"producer_ready: {payload['producer_ready']}\n" + json.dumps(payload, indent=1) + "\n"
    )


def write_receipt(receipt: Receipt) -> None:
    encoded = json.dumps(receipt.as_dict(), indent=1) + "\n"
    atomic_write_text(receipt.receipt_path, encoded, make_parents=True)
    atomic_write_text(receipt.log_path, log_text(receipt), make_parents=True)


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument(
        "--check",
        action="store_true",
        help="inspect and print the receipt; write no checkpoint, receipt, or log",
    )
    command.add_argument("--state", type=Path, default=DEFAULT_STATE)
    command.add_argument(
        "--lp-run4",
        type=Path,
        default=DEFAULT_LP_RUN4,
        help="directory holding lp-run4 sites.json, atoms.json, and rows.json",
    )
    command.add_argument(
        "--resume",
        type=Path,
        default=None,
        help="directory holding a sites.json/atoms.json/rows.json checkpoint to retain",
    )
    command.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    command.add_argument("--receipt", type=Path, default=None)
    command.add_argument("--log", type=Path, default=None)
    command.add_argument(
        "--deadline-seconds",
        type=float,
        default=None,
        help="wall clock for a regeneration; ignored until the in-tree producer exists",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    options = parser().parse_args(argv)
    if options.deadline_seconds is not None and not (
        math.isfinite(options.deadline_seconds) and options.deadline_seconds > 0
    ):
        parser().error("--deadline-seconds must be finite and positive")
    layout = default_layout(
        state=options.state,
        lp_run4=options.lp_run4,
        output_dir=options.output_dir,
        resume=options.resume,
        receipt=options.receipt,
        log=options.log,
    )
    receipt = inspect(
        layout,
        deadline_seconds=options.deadline_seconds,
    )
    print(json.dumps(receipt.as_dict(), indent=1), flush=True)
    if receipt.status != "retained":
        print(refusal_message(receipt), file=sys.stderr)
    if not options.check:
        write_receipt(receipt)
    if receipt.status == "retained":
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
