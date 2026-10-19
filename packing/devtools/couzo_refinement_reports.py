"""Bind all eight #451 certificates and replay the maintained exact arrangement routes.

Original certificate and decimal-pose bytes remain separate factual inputs. Only the
rational certificates enter the geometry decisions; decimal poses are retained source
context. No source program, optimizer, KKT or local/global optimality claim is replayed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools.retained_data import read_retained_bytes

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/couzo-exact-refinements-2026-10-08"
SOURCE = "https://github.com/franciscouzo/square-packing"
REVISION = "ffd900dfff6d2674ad995359208c2f0714915c82"
NUMBERS = (105, 108, 127, 131, 155, 180, 228, 306)
SOURCE_KEY = "[Couzo exact refinements 2026-10-08]"
EXACT_EVIDENCE = "E-couzo-451-exact-feasibility"
FACT_FORMAT = "couzo-451-complete-source-facts-v1"
RECEIPT_FORMAT = "couzo-451-complete-exact-replay-v1"
WITNESS_PREFIX = "W-couzo-451-n"
CLAIM_LIMITATIONS = (
    "Complete #451 rational centre/half-angle certificate converted exactly. "
    "Finite construction feasibility only; no optimizer, KKT, local minimum, rigidity, "
    "novelty, priority or global optimality claim."
)
MAX_SOURCE_BYTES = 1_000_000
MAX_LITERAL_CHARS = 128
MAX_SCALAR_BITS = 512
JOB_TIMEOUT = 45
JOBS = kernel.JOBS
ROUTES = kernel.ROUTES
CASE_INPUTS_SHA256 = "67495e4cb9400d9db6c86aa6ac4e3ec578b515de063cc927b2ecd334369e624e"


def ensure_private(path: Path) -> None:
    if path.is_symlink() or not path.resolve().is_relative_to(REPO.resolve()):
        raise kernel.ReportError("scientific custody/output must remain private")


def unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise kernel.ReportError("duplicate JSON key")
        result[key] = value
    return result


def source_pins() -> dict[int, Any]:
    path = PACKET / "acquisition/case-inputs.json"
    ensure_private(path)
    with path.open("rb") as stream:
        raw = stream.read(MAX_SOURCE_BYTES + 1)
    if len(raw) > MAX_SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != CASE_INPUTS_SHA256:
        raise kernel.ReportError("external original-source acquisition roster differs")
    value = json.loads(raw, object_pairs_hook=unique)
    if (
        value["revision"] != REVISION
        or value["source"] != SOURCE
        or [row["n"] for row in value["cases"]] != list(NUMBERS)
    ):
        raise kernel.ReportError("incomplete eight-certificate acquisition roster")
    return {row["n"]: row for row in value["cases"]}


def fact_path() -> Path:
    return PACKET / "facts/complete-certificates-and-decimal-poses.json.xz"


def receipt_path() -> Path:
    return PACKET / "receipts/exact-certification.json.xz"


def admit_decimal_pose(text: str, n: int) -> None:
    counts = re.findall(r"^# n = ([0-9]+)$", text, re.MULTILINE)
    sides = re.findall(r"^# s = (\S+)$", text, re.MULTILINE)
    rows = [
        line.split()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if counts != [str(n)] or len(sides) != 1 or len(rows) != n:
        raise kernel.ReportError("incomplete decimal source pose or count")
    if any(len(row) != 3 for row in rows):
        raise kernel.ReportError("decimal source pose must retain every x/y/angle")
    tokens = [sides[0], *(token for row in rows for token in row)]
    try:
        values = [Decimal(token) for token in tokens if len(token) <= MAX_LITERAL_CHARS]
    except InvalidOperation as error:
        raise kernel.ReportError("invalid decimal source literal") from error
    if len(values) != len(tokens) or any(not value.is_finite() for value in values):
        raise kernel.ReportError("unbounded or non-finite decimal source literal")
    if values[0] <= 0:
        raise kernel.ReportError("decimal source side must be positive")


def admit_original(n: int, row: Any, pins: dict[int, Any]) -> legacy.Certificate:
    if (
        type(row) is not dict
        or set(row)
        != {"n", "source_path", "source_certificate", "decimal_pose_path", "decimal_pose"}
        or type(row["n"]) is not int
        or row["n"] != n
    ):
        raise kernel.ReportError("incomplete original certificate/decimal-pose fact")
    pin = pins[n]
    for field, path_key, original in (
        ("source_certificate", "source_path", "certificate"),
        ("decimal_pose", "decimal_pose_path", "decimal_pose"),
    ):
        expected = pin[original]
        if row[path_key] != expected["path"] or type(row[field]) is not str:
            raise kernel.ReportError("wrong original source path or text")
        raw = row[field].encode()
        if (
            len(raw) > MAX_SOURCE_BYTES
            or len(raw) != expected["size"]
            or hashlib.sha256(raw).hexdigest() != expected["sha256"]
        ):
            raise kernel.ReportError("complete original bytes differ from acquired source")
    text = row["source_certificate"]
    if any(
        len(token) > MAX_LITERAL_CHARS
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
        for token in line.split()
    ):
        raise kernel.ReportError("certificate literal exceeds bounded source profile")
    certificate = legacy.parse(text, expected_n=n)
    if any(
        max(abs(value.numerator).bit_length(), value.denominator.bit_length()) > MAX_SCALAR_BITS
        for value in (
            certificate.side,
            *(value for pose in certificate.poses for value in (pose.x, pose.y, pose.t)),
        )
    ):
        raise kernel.ReportError("certificate scalar exceeds bounded source profile")
    admit_decimal_pose(row["decimal_pose"], n)
    return certificate


def import_facts() -> None:
    ensure_private(fact_path())
    pins = source_pins()
    cases = []
    for n in NUMBERS:
        row: dict[str, Any] = {"n": n}
        for field, path_key, original in (
            ("source_certificate", "source_path", "certificate"),
            ("decimal_pose", "decimal_pose_path", "decimal_pose"),
        ):
            path = PACKET / "source" / pins[n][original]["path"]
            ensure_private(path)
            ensure_private(path.with_name(path.name + ".gz"))
            raw = read_retained_bytes(path, limit=MAX_SOURCE_BYTES)
            row[path_key] = pins[n][original]["path"]
            row[field] = raw.decode()
        admit_original(n, row, pins)
        cases.append(row)
    ensure_private(fact_path())
    kernel.save_xz(
        fact_path(),
        {"format": FACT_FORMAT, "source": SOURCE, "revision": REVISION, "cases": cases},
    )


def read_facts() -> dict[int, legacy.Certificate]:
    ensure_private(fact_path())
    value = kernel.read_xz(fact_path())
    if (
        type(value) is not dict
        or set(value) != {"format", "source", "revision", "cases"}
        or (value["format"], value["source"], value["revision"])
        != (FACT_FORMAT, SOURCE, REVISION)
        or type(value["cases"]) is not list
        or len(value["cases"]) != len(NUMBERS)
    ):
        raise kernel.ReportError("incomplete eight-original fact envelope")
    pins = source_pins()
    return {
        n: admit_original(n, row, pins) for n, row in zip(NUMBERS, value["cases"], strict=True)
    }


def validate_certification(value: Any, facts: dict[int, legacy.Certificate]) -> dict[int, Any]:
    if (
        type(value) is not dict
        or set(value) != {"format", "routes", "cases"}
        or value["format"] != RECEIPT_FORMAT
        or value["routes"] != list(ROUTES)
        or type(value["cases"]) is not list
        or len(value["cases"]) != len(NUMBERS) * len(JOBS)
        or list(facts) != list(NUMBERS)
    ):
        raise kernel.ReportError("incomplete twenty-four-job exact receipt envelope")
    positives = {}
    for (n, control), row in zip(
        ((n, control) for n in NUMBERS for control in JOBS), value["cases"], strict=True
    ):
        kernel.validate_job(
            row,
            facts[n],
            control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=CLAIM_LIMITATIONS,
        )
        if control == "positive":
            positives[n] = row
    return positives


def check_certification() -> dict[int, Any]:
    facts = read_facts()
    ensure_private(receipt_path())
    return validate_certification(kernel.read_xz(receipt_path()), facts)


def private_input_paths() -> tuple[Path, ...]:
    """Complete original-byte map, all eight source contexts and all24 deciding jobs."""
    return (PACKET / "acquisition/case-inputs.json", fact_path(), receipt_path())


def run_child(job: tuple[int, str], directory: Path, timeout: int) -> dict[str, Any]:
    n, control = job
    if type(n) is not int or n not in NUMBERS or control not in JOBS:
        raise kernel.ReportError("job outside the complete certificate/control roster")
    if type(timeout) is not int or not 1 <= timeout <= JOB_TIMEOUT:
        raise kernel.ReportError("invalid bounded worker/deadline selection")
    path = directory / f"n{n}-{control}.json"
    if path.exists():
        raise kernel.ReportError("refusing to overwrite a deciding job")
    command = [
        sys.executable,
        "-m",
        "devtools.couzo_refinement_reports",
        "decide-job",
        "--n",
        str(n),
        "--control",
        control,
        "--output",
        str(path),
    ]
    try:
        completed = subprocess.run(command, capture_output=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as error:
        path.with_suffix(".stdout.log").write_bytes(error.stdout or b"")
        path.with_suffix(".stderr.log").write_bytes(error.stderr or b"")
        raise kernel.ReportError(
            f"full native job {n}/{control} exceeded {timeout}s"
        ) from error
    path.with_suffix(".stdout.log").write_bytes(completed.stdout)
    path.with_suffix(".stderr.log").write_bytes(completed.stderr)
    if completed.returncode:
        raise kernel.ReportError(f"full native job {n}/{control} exited {completed.returncode}")
    with path.open("rb") as stream:
        raw = stream.read(kernel.MAX_BYTES + 1)
    if len(raw) > kernel.MAX_BYTES:
        raise kernel.ReportError("native job exceeds existing receipt ceiling")
    value = json.loads(raw, object_pairs_hook=unique)
    if type(value) is not dict:
        raise kernel.ReportError("complete native job object required")
    return value


def certify(directory: Path, *, workers: int = 2, timeout: int = JOB_TIMEOUT) -> None:
    if (
        type(workers) is not int
        or not 1 <= workers <= 2
        or type(timeout) is not int
        or not 1 <= timeout <= JOB_TIMEOUT
    ):
        raise kernel.ReportError("invalid bounded worker/deadline selection")
    ensure_private(receipt_path())
    facts = read_facts()
    if directory.exists():
        raise kernel.ReportError("native job directory must be a fresh attempt")
    directory.mkdir(parents=True)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        cases = list(
            pool.map(
                lambda job: run_child(job, directory, timeout),
                ((n, control) for n in NUMBERS for control in JOBS),
            )
        )
    value = {"format": RECEIPT_FORMAT, "routes": list(ROUTES), "cases": cases}
    validate_certification(value, facts)
    ensure_private(receipt_path())
    kernel.save_xz(receipt_path(), value)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("import-facts")
    sub.add_parser("check")
    campaign = sub.add_parser("certify")
    campaign.add_argument("--jobs-dir", type=Path, required=True)
    campaign.add_argument("--workers", type=int, default=2)
    campaign.add_argument("--timeout", type=int, default=JOB_TIMEOUT)
    job = sub.add_parser("decide-job")
    job.add_argument("--n", type=int, choices=NUMBERS, required=True)
    job.add_argument("--control", choices=JOBS, required=True)
    job.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.action == "import-facts":
        import_facts()
    elif args.action == "check":
        positives = check_certification()
        print(f"all {len(positives)} complete certificates and twenty-four full jobs admitted")
    elif args.action == "certify":
        certify(args.jobs_dir, workers=args.workers, timeout=args.timeout)
    else:
        certificate = read_facts()[args.n]
        row = kernel.run_case(
            certificate,
            args.control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=CLAIM_LIMITATIONS,
        )
        kernel.validate_job(
            row,
            certificate,
            args.control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=CLAIM_LIMITATIONS,
        )
        if args.output.exists():
            raise kernel.ReportError("refusing to overwrite an actual deciding job")
        with atomic_output_file(args.output) as temporary:
            temporary.write_text(json.dumps(row, separators=(",", ":"), allow_nan=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
