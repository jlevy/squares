"""Retain, decide and control this project's own certificates below a case's house.

The house rule (``packing/campaign/result-import.md``, The House Rule) and the
regularization guide's Register Candidates
(``docs/project/guides/regularization-process.md``) send every exactly verified packing
below a house best packing to the register, however it was made: a regularizer's view
held at row 3, or a construction a review found. `devtools.register_regularized_bounds`
registered the batches of 12 and 13 October 2026 and writes their case records itself;
this module is the stage 2 to stage 4 half for a later batch, which the house rule
adopts once reviewed, and writes no case record.

A batch is one package, ``packing/cases/register_candidates/<name>/``, and one `Batch`
here naming its candidates (`Candidate`), each of one of two kinds:

- **view**: a regularizer's view, the Witness/v2 its run wrote, retained gzipped as
  ``views/n-NNN.yaml.gz``. ``retain`` copies it from the run directory only where its Git
  blob and exact side are those the run's report, retained under
  ``cases/regularized_drawings/``, records, so the view is the one the selection held at
  row 3; ``check`` holds the retained view to the same report again;
- **l-strip**: a house certificate at a smaller count ``m``, read through its import
  packet's custody (`devtools.upper_bound_reports.read_facts`), with one L strip of
  ``2 floor(S) + 1`` axis-aligned unit squares added in ``[S, S + 1] x [0, S + 1] u
  [0, S + 1] x [S, S + 1]``, at side ``S + 1``. The certificate is rebuilt from its parent
  wherever it is read, so the package keeps no copy of it.

Each candidate is decided by the kernel's three jobs (`devtools.evand_arrangement_reports`:
a positive, a duplicate square and a square moved outside the box) on both maintained
exact routes, ``sqpack.witness.exact_verify`` and
``devtools.check_rational_witness_independent``, each job in its own child process, into
``receipts/exact-certification-nNNN.json.xz``; and by the six sharp controls of
`devtools.upper_bound_sharp_controls`, at exact contact and 1e-30 past it, into
``receipts/sharp-controls-nNNN.json``. The routes are the ones the regularizer's run used
to decide its views, so the replay of a view reproduces the producing run's decision with
its own code. A finite certificate proves an upper bound and nothing more.

``side`` gives each candidate's exact side for `devtools.upper_bound_reports.HOUSES`.

From ``packing/``, with the project interpreter::

    python -m devtools.register_candidates BATCH retain --run-dir RUN
    python -m devtools.register_candidates BATCH certify --jobs-dir DIR [--workers 2]
    python -m devtools.register_candidates BATCH controls [--n N ...] [--check]
    python -m devtools.register_candidates BATCH check [--replay]
    python -m devtools.register_candidates BATCH table
    python -m devtools.register_candidates BATCH witness --n N --out PATH
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
import subprocess
import sys
from collections.abc import Callable, Mapping
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports
from devtools import upper_bound_sharp_controls as sharp
from devtools.retained_data import git_blob
from sqpack.witness import witness_document

MODULE = "devtools.register_candidates"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKAGES = ROOT / "cases/register_candidates"
DRAWINGS = ROOT / "cases/regularized_drawings"
RECEIPT_FORMAT = "register-candidates-exact-certification-v1"
VIEW = "view"
L_STRIP = "l-strip"
HALF = Fraction(1, 2)


class CandidateError(ValueError):
    """A view out of custody, a construction that does not count, or a receipt that differs."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise CandidateError(message)


@dataclass(frozen=True)
class Candidate:
    """One count's certificate below its house.

    - ``kind``: `VIEW` or `L_STRIP`.
    - ``house``: the register result whose certificate is the case's house at ``n``.
    - ``report``: for a view, its run's report, relative to `DRAWINGS`.
    - ``parent_packet`` and ``parent_n``: for an L strip, the import packet holding the
      certificate at the smaller count.
    """

    n: int
    kind: str
    house: str
    report: str = ""
    parent_packet: str = ""
    parent_n: int = 0


@dataclass(frozen=True)
class Batch:
    name: str
    bead: str
    witness_prefix: str
    claim_limitations: str
    candidates: tuple[Candidate, ...]

    @property
    def package(self) -> Path:
        return PACKAGES / self.name

    @property
    def profile(self) -> dict[str, str]:
        return {
            "witness_prefix": self.witness_prefix,
            "claim_limitations": self.claim_limitations,
        }

    def candidate(self, n: int) -> Candidate:
        found = [item for item in self.candidates if item.n == n]
        _require(len(found) == 1, f"{self.name}: no candidate at n={n}")
        return found[0]


#: Evan Daniel's regularizer's KKT solves at 130 and 307, held at row 3 by the runs after
#: the adoption of 31 October 2026 (think-3guf), and the 260 house plus one L strip at 293,
#: which the senior review of #852 found (A3).
RUU2 = Batch(
    name="think-ruu2-2026-10-31",
    bead="think-ruu2",
    witness_prefix="W-register-candidate-1031-n",
    claim_limitations=(
        "This project's certificate below the case's house best packing of 31 October 2026, "
        "a finite construction; it certifies an upper bound and nothing more."
    ),
    candidates=(
        Candidate(
            130,
            VIEW,
            "T-259",
            report="think-3guf-2026-10-31/adopt-2026-10-31-n130-307-evand/n-130/report.json.gz",
        ),
        Candidate(
            293, L_STRIP, "T-257", parent_packet="evand-issue845-2026-10-29", parent_n=260
        ),
        Candidate(
            307,
            VIEW,
            "T-256",
            report="think-3guf-2026-10-31/adopt-2026-10-31-n130-307-evand/n-307/report.json.gz",
        ),
    ),
)
BATCHES = {RUU2.name: RUU2}


# ------------------------------------------------------------------------------ views


def view_path(batch: Batch, n: int) -> Path:
    return batch.package / f"views/n-{n:03d}.yaml.gz"


def run_report(candidate: Candidate) -> dict[str, Any]:
    return json.loads(gzip.decompress((DRAWINGS / candidate.report).read_bytes()))


def _held_output(candidate: Candidate) -> dict[str, Any]:
    """The run's solved output, refused unless the selection held it at row 3."""
    report = run_report(candidate)
    _require(report.get("n") == candidate.n, f"n={candidate.n}: the report is another count's")
    output = report["outputs"]["solved"]
    decision = report["decisions"]["solved"]
    _require(
        decision["row"] == 3 and decision["decision"] == "held",
        f"n={candidate.n}: the run did not hold its view at row 3",
    )
    routes = output["routes"]
    _require(
        routes["exact_verify"] and routes["independent"],
        f"n={candidate.n}: the run's routes did not accept its view",
    )
    return output


def retain(batch: Batch, run_dir: Path) -> list[Path]:
    """Copy each view from its run directory, held to the run's retained report."""
    written = []
    for candidate in batch.candidates:
        if candidate.kind != VIEW:
            continue
        output = _held_output(candidate)
        source = run_dir / f"n-{candidate.n}" / output["path"]
        raw = source.read_bytes()
        _require(
            git_blob(raw) == output["git_blob"],
            f"n={candidate.n}: {source} is not the view its report names",
        )
        target = view_path(batch, candidate.n)
        target.parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(target) as temporary:
            temporary.write_bytes(gzip.compress(raw, mtime=0))
        _require(view(batch, candidate.n) is not None, f"n={candidate.n}: unreadable view")
        written.append(target)
    return written


@cache
def view(batch: Batch, n: int) -> legacy.Certificate:
    """The retained view at ``n``, held to its report's blob and exact side."""
    candidate = batch.candidate(n)
    output = _held_output(candidate)
    raw = gzip.decompress(view_path(batch, n).read_bytes())
    _require(git_blob(raw) == output["git_blob"], f"n={n}: the retained view is not the run's")
    certificate = reports.witness_center_basis(raw, n, {})
    _require(
        certificate.side == Fraction(output["side_exact"]),
        f"n={n}: the view's side is not the one its report records",
    )
    return certificate


# ---------------------------------------------------------------------------- L strip


def l_strip(parent: legacy.Certificate, n: int) -> legacy.Certificate:
    """``parent`` with one L strip of unit squares at side ``S + 1``, refused unless the
    strip brings the count to ``n`` exactly."""
    side = parent.side
    whole = math.floor(side)
    _require(parent.n + 2 * whole + 1 == n, f"n={n}: one L strip from {parent.n} gives another")
    column = [legacy.Pose(side + HALF, k + HALF, Fraction(0)) for k in range(whole)]
    row = [legacy.Pose(k + HALF, side + HALF, Fraction(0)) for k in range(whole)]
    corner = [legacy.Pose(side + HALF, side + HALF, Fraction(0))]
    return legacy.Certificate(n, side + 1, (*parent.poses, *column, *row, corner[0]))


@cache
def construction(batch: Batch, n: int) -> legacy.Certificate:
    candidate = batch.candidate(n)
    packet = reports.packet_path(candidate.parent_packet)
    parent = reports.read_facts(packet, {candidate.parent_n})[candidate.parent_n]
    return l_strip(parent, n)


def certificate(batch: Batch, n: int) -> legacy.Certificate:
    candidate = batch.candidate(n)
    return view(batch, n) if candidate.kind == VIEW else construction(batch, n)


def side(batch: Batch, n: int) -> Fraction:
    """The candidate's exact side, for `devtools.upper_bound_reports.HOUSES`."""
    return certificate(batch, n).side


def house_reader(batch: Batch) -> Callable[[int], Fraction]:
    return lambda n: side(batch, n)


# ---------------------------------------------------------------------------- deciding


def receipt_path(batch: Batch, n: int) -> Path:
    return batch.package / f"receipts/exact-certification-n{n:03d}.json.xz"


def controls_path(batch: Batch, n: int) -> Path:
    return batch.package / f"receipts/sharp-controls-n{n:03d}.json"


def decide_job(batch: Batch, n: int, control: str, output: Path) -> None:
    _require(not output.exists(), "refusing to overwrite a deciding job")
    found = certificate(batch, n)
    row = kernel.run_case(found, control, **batch.profile)
    kernel.validate_job(row, found, control, **batch.profile)
    output.write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")


def _child(batch: Batch, n: int, control: str, directory: Path) -> dict[str, Any]:
    output = directory / f"n{n}-{control}.json"
    if not output.exists():
        command = [sys.executable, "-m", MODULE, batch.name, "decide-job", "--n", str(n)]
        command += ["--control", control, "--output", str(output)]
        completed = subprocess.run(command, capture_output=True, check=False)
        output.with_suffix(".log").write_bytes(completed.stdout + completed.stderr)
        _require(completed.returncode == 0, f"n={n} {control}: child exited")
    return json.loads(output.read_text(encoding="utf-8"))


def certify(batch: Batch, directory: Path, workers: int) -> None:
    """Each candidate's three jobs on both routes, then its receipt."""
    directory.mkdir(parents=True, exist_ok=True)
    tasks = [(item.n, control) for item in batch.candidates for control in kernel.JOBS]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(lambda task: _child(batch, *task, directory), tasks))
    done = dict(zip(tasks, rows, strict=True))
    for item in batch.candidates:
        found = certificate(batch, item.n)
        cases = [done[(item.n, control)] for control in kernel.JOBS]
        for row, control in zip(cases, kernel.JOBS, strict=True):
            kernel.validate_job(row, found, control, **batch.profile)
        receipt_path(batch, item.n).parent.mkdir(parents=True, exist_ok=True)
        kernel.save_xz(
            receipt_path(batch, item.n),
            {
                "format": RECEIPT_FORMAT,
                "n": item.n,
                "routes": list(kernel.ROUTES),
                "cases": cases,
            },
        )


def check_receipt(batch: Batch, n: int, *, replay: bool = False) -> dict[str, Any]:
    found = certificate(batch, n)
    record = kernel.read_xz(receipt_path(batch, n))
    _require(
        record.get("format") == RECEIPT_FORMAT
        and record.get("n") == n
        and record.get("routes") == list(kernel.ROUTES)
        and len(record.get("cases", [])) == len(kernel.JOBS),
        f"n={n}: not this batch's receipt",
    )
    for row, control in zip(record["cases"], kernel.JOBS, strict=True):
        kernel.validate_job(row, found, control, **batch.profile)
        if replay:
            again = kernel.run_case(found, control, **batch.profile)
            _require(
                kernel.stable_row(again) == kernel.stable_row(row), f"n={n}: the replay differs"
            )
    return record


def sharp_record(batch: Batch, n: int) -> dict[str, Any]:
    found = certificate(batch, n)
    candidate = batch.candidate(n)
    if candidate.kind == VIEW:
        where = view_path(batch, n).relative_to(REPO).as_posix()
    else:
        where = (
            f"{candidate.parent_packet}'s n = {candidate.parent_n} certificate plus one L strip"
        )
    rows = sharp.control_rows(found, batch.profile)
    return {
        "format": sharp.FORMAT,
        "batch": batch.name,
        "n": n,
        "certificate": where,
        "side": legacy.literal(found.side),
        "epsilon": legacy.literal(sharp.EPSILON),
        "routes": list(sharp.ROUTES),
        "controls": rows,
        "all_as_expected": all(row["as_expected"] for row in rows),
    }


def _untimed(record: Mapping[str, Any]) -> dict[str, Any]:
    return {
        **record,
        "controls": [
            {key: value for key, value in row.items() if key != "cpu_seconds"}
            for row in record["controls"]
        ],
    }


def controls(batch: Batch, numbers: list[int], *, check: bool) -> dict[int, bool]:
    results = {}
    for n in numbers:
        path = controls_path(batch, n)
        record = sharp_record(batch, n)
        if check:
            retained = json.loads(path.read_text(encoding="utf-8"))
            _require(_untimed(retained) == _untimed(record), f"n={n}: the controls differ")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            with atomic_output_file(path) as temporary:
                temporary.write_text(json.dumps(record, indent=1) + "\n", encoding="utf-8")
        results[n] = record["all_as_expected"]
    return results


def write_witness(batch: Batch, n: int, path: Path) -> Path:
    """The candidate as a rational centre-basis Witness/v2, for ``devtools.measure_identity``'s
    ``witness-center-basis`` input; a construction is written from its parent, as it is read."""
    document = witness_document(kernel.to_witness(certificate(batch, n), **batch.profile))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document, encoding="utf-8")
    return path


def table(batch: Batch) -> list[dict[str, Any]]:
    """Each candidate's side against its house's, exactly, with both 12-place prints."""

    def up12(value: Fraction) -> str:
        q = math.ceil(value * 10**12)
        return f"{q // 10**12}.{q % 10**12:012d}"

    rows = []
    for item in batch.candidates:
        found = certificate(batch, item.n)
        house = reports.witness_center_basis(
            (ROOT / f"witnesses/known-best/n-{item.n:03d}.yaml").read_bytes(), item.n, {}
        ).side
        rows.append(
            {
                "n": item.n,
                "kind": item.kind,
                "house": item.house,
                "side": legacy.literal(found.side),
                "below_house_by": f"{float(house - found.side):.3e}",
                "print": up12(found.side),
                "house_print": up12(house),
                "same_print": up12(found.side) == up12(house),
            }
        )
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("batch", choices=sorted(BATCHES))
    sub = parser.add_subparsers(dest="action", required=True)
    keep = sub.add_parser("retain")
    keep.add_argument("--run-dir", type=Path, required=True)
    run = sub.add_parser("certify")
    run.add_argument("--jobs-dir", type=Path, required=True)
    run.add_argument("--workers", type=int, default=2)
    control = sub.add_parser("controls")
    control.add_argument("--n", type=int, nargs="+")
    control.add_argument("--check", action="store_true")
    checking = sub.add_parser("check")
    checking.add_argument("--replay", action="store_true")
    sub.add_parser("table")
    writing = sub.add_parser("witness")
    writing.add_argument("--n", type=int, required=True)
    writing.add_argument("--out", type=Path, required=True)
    job = sub.add_parser("decide-job")
    job.add_argument("--n", type=int, required=True)
    job.add_argument("--control", choices=kernel.JOBS, required=True)
    job.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    batch = BATCHES[args.batch]
    numbers = [item.n for item in batch.candidates]
    try:
        if args.action == "retain":
            for path in retain(batch, args.run_dir):
                print(path.relative_to(REPO))
        elif args.action == "certify":
            certify(batch, args.jobs_dir, args.workers)
            print(json.dumps(dict.fromkeys(numbers, "certified")))
        elif args.action == "controls":
            print(json.dumps(controls(batch, args.n or numbers, check=args.check)))
        elif args.action == "check":
            for n in numbers:
                check_receipt(batch, n, replay=args.replay)
            print(json.dumps(controls(batch, numbers, check=True)))
        elif args.action == "table":
            print(json.dumps(table(batch), indent=1))
        elif args.action == "witness":
            print(write_witness(batch, args.n, args.out))
        else:
            decide_job(batch, args.n, args.control, args.output)
    except (
        CandidateError,
        reports.ReportError,
        kernel.ReportError,
        OSError,
        KeyError,
    ) as error:
        print(f"{MODULE}: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
