"""Complete #438 source custody and bounded native finite-feasibility replay.

Retain all seventeen original certificates and complete comparators, including the
three source withdrawals. Reuse only the maintained exact native arrangement routes;
no upstream author program or optimizer executes. Admission does not assign assurance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools.retained_data import read_retained_bytes

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/gupta-square-packing-refinements-2026-10-08"
SOURCE = "https://github.com/SidG2k1/square-packing-refinements"
REVISION = "9643cb5a78c1d4dcfc867c80a6920c3a6219d05a"
NUMBERS = (88, 108, 123, 129, 130, 153, 154, 179, 180, 199, 207, 208, 209, 236, 237, 238, 239)
SELECTED = (88, 130, 153, 154, 179, 180, 199, 207, 208, 209, 236, 237, 238, 239)
WITHDRAWN = (108, 123, 129)
SOURCE_KEY = "[Gupta rational refinements 2026-10-08]"
EXACT_EVIDENCE = "E-gupta-438-exact-feasibility"
FACT_FORMAT = "gupta-438-complete-source-facts-v1"
RECEIPT_FORMAT = "gupta-438-complete-exact-replay-v1"
WITNESS_PREFIX = "W-gupta-438-n"
CLAIM_LIMITATIONS = (
    "Complete #438 rational centre/half-angle certificate converted exactly. "
    "Finite construction feasibility only; no optimizer, local minimum, rigidity, "
    "novelty, priority or global optimality claim."
)
MAX_SOURCE_BYTES = 1_000_000
CASE_INPUTS_SHA256 = "38a48556b13f79d9a4bbb89dfe4702721e3e50cb2973660af316dcc07b84c283"
JOBS = kernel.JOBS
ROUTES = kernel.ROUTES
JOB_TIMEOUT = kernel.JOB_TIMEOUT


def _count(n: int) -> None:
    if type(n) is not int or n not in NUMBERS:
        raise kernel.ReportError("count outside the complete seventeen-certificate scope")


def ensure_private(path: Path) -> None:
    if not path.resolve().is_relative_to(REPO.resolve()):
        raise kernel.ReportError(
            "scientific custody/output must remain inside private repository"
        )


def json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, separators=(",", ":"), allow_nan=False, sort_keys=True) + "\n"
    ).encode()


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
    if value["revision"] != REVISION or [row["n"] for row in value["cases"]] != list(NUMBERS):
        raise kernel.ReportError("incomplete external source roster")
    return {row["n"]: row for row in value["cases"]}


def fact_path() -> Path:
    return PACKET / "facts/complete-certificates-and-comparators.json.xz"


def receipt_path() -> Path:
    return PACKET / "receipts/exact-certification.json.xz"


def save_xz(path: Path, value: Any) -> None:
    ensure_private(path)
    data = json_bytes(value)
    if len(data) > kernel.MAX_BYTES:
        raise kernel.ReportError("uncompressed evidence exceeds existing receipt ceiling")
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(lzma.compress(data, preset=6))


def admit_original(n: int, row: Any, pins: dict[int, Any]) -> legacy.Certificate:
    pin = pins[n]
    if (
        type(row) is not dict
        or set(row)
        != {"n", "source_path", "source_certificate", "comparator_path", "source_comparator"}
        or type(row["n"]) is not int
        or row["n"] != n
        or row["source_path"] != pin["certificate"]
        or row["comparator_path"] != pin["comparator"]
    ):
        raise kernel.ReportError("missing, extra, duplicate or mistyped original fact")
    for field, digest in (
        ("source_certificate", "certificate_sha256"),
        ("source_comparator", "comparator_sha256"),
    ):
        text = row[field]
        if type(text) is not str:
            raise kernel.ReportError("complete original source text required")
        raw = text.encode()
        if len(raw) > MAX_SOURCE_BYTES or hashlib.sha256(raw).hexdigest() != pin[digest]:
            raise kernel.ReportError("complete original bytes differ from acquired source")
    certificate = legacy.parse(row["source_certificate"], expected_n=n)
    comparator = json.loads(row["source_comparator"], object_pairs_hook=unique)
    if (
        type(comparator) is not dict
        or type(comparator.get("n")) is not int
        or comparator["n"] != n
        or type(comparator.get("squares")) is not list
        or len(comparator["squares"]) != n
        or str(certificate.side) != pin["side_exact"]
    ):
        raise kernel.ReportError("complete certificate/comparator roster or side differs")
    previous = Fraction(comparator["s_exact"])
    if (n in SELECTED and certificate.side >= previous) or (
        n in WITHDRAWN and certificate.side <= previous
    ):
        raise kernel.ReportError("source comparison disposition differs")
    return certificate


def import_facts() -> None:
    pins = source_pins()
    cases = []
    for n in NUMBERS:
        pin = pins[n]
        row = {"n": n, "source_path": pin["certificate"], "comparator_path": pin["comparator"]}
        for field, path in (
            ("source_certificate", pin["certificate"]),
            ("source_comparator", pin["comparator"]),
        ):
            raw = read_retained_bytes(PACKET / "source" / path, limit=MAX_SOURCE_BYTES)
            row[field] = raw.decode()
        admit_original(n, row, pins)
        cases.append(row)
    save_xz(
        fact_path(),
        {"format": FACT_FORMAT, "source": SOURCE, "revision": REVISION, "cases": cases},
    )


def read_facts() -> dict[int, legacy.Certificate]:
    path = fact_path()
    ensure_private(path)
    pins = source_pins()
    value = kernel.read_xz(path)
    if (
        type(value) is not dict
        or set(value) != {"format", "source", "revision", "cases"}
        or (value["format"], value["source"], value["revision"])
        != (FACT_FORMAT, SOURCE, REVISION)
        or type(value["cases"]) is not list
        or len(value["cases"]) != len(NUMBERS)
    ):
        raise kernel.ReportError("incomplete seventeen-original fact envelope")
    return {
        n: admit_original(n, row, pins) for n, row in zip(NUMBERS, value["cases"], strict=True)
    }


def read_fact(n: int) -> legacy.Certificate:
    _count(n)
    return read_facts()[n]


def validate_job(row: Any, certificate: legacy.Certificate, control: str) -> None:
    kernel.validate_job(
        row,
        certificate,
        control,
        witness_prefix=WITNESS_PREFIX,
        claim_limitations=CLAIM_LIMITATIONS,
    )


def check_certification() -> dict[int, Any]:
    facts = read_facts()
    path = receipt_path()
    ensure_private(path)
    value = kernel.read_xz(path)
    if (
        type(value) is not dict
        or set(value) != {"format", "routes", "cases"}
        or value["format"] != RECEIPT_FORMAT
        or value["routes"] != list(ROUTES)
        or type(value["cases"]) is not list
        or len(value["cases"]) != len(NUMBERS) * len(JOBS)
    ):
        raise kernel.ReportError("incomplete fifty-one-job native receipt envelope")
    positives = {}
    for (n, control), row in zip(
        ((n, c) for n in NUMBERS for c in JOBS), value["cases"], strict=True
    ):
        validate_job(row, facts[n], control)
        if control == "positive":
            positives[n] = row
    return positives


def run_child(job: tuple[int, str], directory: Path, timeout: int) -> dict[str, Any]:
    n, control = job
    path = directory / f"n{n}-{control}.json"
    command = [
        sys.executable,
        "-m",
        "devtools.gupta_refinement_reports",
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
        path.with_suffix(".failure.json").write_bytes(
            json_bytes(
                {"n": n, "control": control, "status": "timeout", "timeout_seconds": timeout}
            )
        )
        raise kernel.ReportError(
            f"n={n} {control}: deciding child exceeded {timeout}s"
        ) from error
    path.with_suffix(".stdout.log").write_bytes(completed.stdout)
    path.with_suffix(".stderr.log").write_bytes(completed.stderr)
    if completed.returncode:
        raise kernel.ReportError(
            f"n={n} {control}: deciding child exited {completed.returncode}"
        )
    with path.open("rb") as stream:
        raw = stream.read(kernel.MAX_BYTES + 1)
    if len(raw) > kernel.MAX_BYTES:
        raise kernel.ReportError("native child receipt exceeds existing ceiling")
    return json.loads(raw, object_pairs_hook=unique)


def certify(directory: Path, *, workers: int = 2, timeout: int = JOB_TIMEOUT) -> None:
    if not 1 <= workers <= 3 or not 1 <= timeout <= JOB_TIMEOUT:
        raise kernel.ReportError("invalid bounded replay allocation")
    facts = read_facts()
    directory.mkdir(parents=True, exist_ok=True)
    jobs = [(n, control) for n in NUMBERS for control in JOBS]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        pending = [pool.submit(run_child, job, directory, timeout) for job in jobs]
        rows = [future.result() for future in pending]
    for (n, control), row in zip(jobs, rows, strict=True):
        validate_job(row, facts[n], control)
    save_xz(receipt_path(), {"format": RECEIPT_FORMAT, "routes": list(ROUTES), "cases": rows})
    check_certification()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("import-facts")
    commands.add_parser("check")
    replay = commands.add_parser("certify")
    replay.add_argument("--jobs-dir", type=Path, required=True)
    replay.add_argument("--workers", type=int, default=2)
    replay.add_argument("--timeout", type=int, default=JOB_TIMEOUT)
    child = commands.add_parser("decide-job")
    child.add_argument("--n", type=int, required=True)
    child.add_argument("--control", choices=JOBS, required=True)
    child.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "import-facts":
        import_facts()
    elif args.command == "certify":
        certify(args.jobs_dir, workers=args.workers, timeout=args.timeout)
    elif args.command == "check":
        check_certification()
        print("#438: seventeen positives and thirty-four complete native controls admitted")
    else:
        certificate = read_fact(args.n)
        row = kernel.run_case(
            certificate,
            args.control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=CLAIM_LIMITATIONS,
        )
        validate_job(row, certificate, args.control)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(args.output) as temporary:
            temporary.write_bytes(json_bytes(row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
