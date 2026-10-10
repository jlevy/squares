"""Replay #399's three complete rational packings with two independent exact routes.

The separate 7eef24f source packet remains distinct from #375's historical packet.
Each retained job contains its complete rational centre/half-angle input and full
native results. Feasibility certifies an upper bound; source novelty, KKT, local
minimality and global optimality claims are not decided here.

From packing/: ``python -m devtools.evand_arrangement_reports import-facts``;
``certify --jobs-dir EXTERNAL_SCRATCH --workers 2``; ``check [--replay]``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import lzma
import math
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import evand_exact_certificates as legacy

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/evand-new-arrangements-2026-10-07"
NUMBERS = (266, 270, 272)
REVISION = "7eef24f7221b8c3371d6171dd664b52541bbd479"
SOURCE = "https://github.com/evand/square-packing"
SOURCE_KEY = "[Daniel new arrangements 2026-10-07]"
EXACT_EVIDENCE = "E-evand-399-exact-feasibility"
FACT_FORMAT = "evand-399-complete-source-facts-v1"
RECEIPT_FORMAT = "evand-399-complete-exact-replay-v1"
JOBS = ("positive", "duplicate-square-overlap", "square-translated-outside-container")
ROUTES = ("exact_verify", "independent")
MAX_BYTES = 4_000_000
MAX_XZ_MEMORY = 32 * 1024 * 1024
JOB_TIMEOUT = 600
WITNESS_PREFIX = "W-evand-399-n"
CLAIM_LIMITATIONS = (
    "Complete #399 rational centre/half-angle certificate converted exactly. "
    "Certifies this feasible upper-bound construction, not novelty, KKT, local "
    "minimality or global optimality."
)
SOURCE_NAMES = {266: "dc1_n266.cert", 270: "sw2_n270.cert", 272: "rd1_n272.cert"}
# Digests apply only to original downloaded third-party bytes, the acquisition boundary.
SOURCE_SHA256 = {
    266: "72a764513e0eef50cad798184ead0334f3d4bc5428fc878c6da59e9718781f3e",
    270: "c0310361895273cef4ae6c85c87c0569120a5c4201cb65ca67733f53b3294f97",
    272: "286e186ef21e4a4fd9fd84c69a39d52bc322b35e1111c096115e3561ad99ec89",
}
EXACT_KEYS = {
    "operation",
    "id",
    "coordinate_provenance",
    "method",
    "verification_passed",
    "n",
    "side",
    "pairs_tested",
    "minimum_containment_clearance",
    "minimum_best_pair_gap",
    "field_certificate",
    "failures",
    "limitations",
}
INDEPENDENT_KEYS = {
    "verification_passed",
    "coordinate_provenance",
    "method",
    "field",
    "n",
    "side",
    "pairs_tested",
    "minimum_containment_clearance",
    "minimum_best_pair_gap",
    "failures",
    "limitations",
}


class ReportError(ValueError):
    """Refuse incomplete source, geometry, coverage or custody."""


def _count(n: int) -> None:
    if type(n) is not int or n not in NUMBERS:
        raise ReportError("count outside the three complete #399 certificates")


def source_path(n: int) -> str:
    _count(n)
    return f"s12/search/exact/results/sw2/{SOURCE_NAMES[n]}"


def fact_path() -> Path:
    return PACKET / "facts/complete-certificates.json.xz"


def receipt_path() -> Path:
    return PACKET / "receipts/exact-certification.json.xz"


def _unique(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReportError("duplicate JSON key")
        result[key] = value
    return result


def _json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, separators=(",", ":"), allow_nan=False, sort_keys=True) + "\n"
    ).encode()


def read_xz(path: Path) -> Any:
    """One bounded XZ stream, with bounded output, memory and strict JSON keys."""
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ReportError("compressed evidence exceeds existing receipt ceiling")
    decoder = lzma.LZMADecompressor(memlimit=MAX_XZ_MEMORY)
    try:
        data = decoder.decompress(raw, max_length=MAX_BYTES + 1)
    except lzma.LZMAError as error:
        raise ReportError("invalid or memory-exceeding XZ evidence") from error
    if len(data) > MAX_BYTES or not decoder.eof or decoder.unused_data:
        raise ReportError("oversized, truncated or trailing XZ evidence")
    return json.loads(data, object_pairs_hook=_unique)


def save_xz(path: Path, value: Any) -> None:
    """Producers write private outputs; linked outside paths never become outputs."""
    if not path.resolve().is_relative_to(REPO.resolve()):
        raise ReportError("retained evidence output must remain inside the repository")
    data = _json_bytes(value)
    if len(data) > MAX_BYTES:
        raise ReportError("uncompressed evidence exceeds existing receipt ceiling")
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_bytes(lzma.compress(data, preset=6))


def import_facts() -> None:
    cases = []
    for n in NUMBERS:
        path = PACKET / "source" / source_path(n)
        with path.open("rb") as stream:
            data = stream.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES or hashlib.sha256(data).hexdigest() != SOURCE_SHA256[n]:
            raise ReportError("downloaded source certificate differs from acquisition")
        text = data.decode()
        legacy.parse(text, expected_n=n)
        cases.append({"n": n, "source_path": source_path(n), "source_certificate": text})
    save_xz(
        fact_path(),
        {"format": FACT_FORMAT, "source": SOURCE, "revision": REVISION, "cases": cases},
    )


def read_facts() -> dict[int, legacy.Certificate]:
    if not fact_path().resolve().is_relative_to(REPO.resolve()):
        raise ReportError("source facts must remain private to this repository")
    record = read_xz(fact_path())
    if type(record) is not dict or set(record) != {"format", "source", "revision", "cases"}:
        raise ReportError("invalid complete source fact envelope")
    if (record["format"], record["source"], record["revision"]) != (
        FACT_FORMAT,
        SOURCE,
        REVISION,
    ):
        raise ReportError("wrong source fact namespace")
    cases = record["cases"]
    if type(cases) is not list or len(cases) != len(NUMBERS):
        raise ReportError("incomplete source fact roster")
    result = {}
    for n, row in zip(NUMBERS, cases, strict=True):
        if (
            type(row) is not dict
            or set(row) != {"n", "source_path", "source_certificate"}
            or type(row["n"]) is not int
            or row["n"] != n
            or row["source_path"] != source_path(n)
            or type(row["source_certificate"]) is not str
        ):
            raise ReportError("missing, extra, duplicate or mistyped source fact")
        text = row["source_certificate"]
        if hashlib.sha256(text.encode()).hexdigest() != SOURCE_SHA256[n]:
            raise ReportError("complete source bytes differ from acquired certificate")
        result[n] = legacy.parse(text, expected_n=n)
    return result


def read_fact(n: int) -> legacy.Certificate:
    _count(n)
    return read_facts()[n]


def checker_input(certificate: legacy.Certificate) -> dict[str, Any]:
    """Every exact scalar handed to the existing half-angle conversion and deciders."""
    return {
        "n": certificate.n,
        "side": legacy.literal(certificate.side),
        "poses": [
            [legacy.literal(p.x), legacy.literal(p.y), legacy.literal(p.t)]
            for p in certificate.poses
        ],
    }


def job_input(certificate: legacy.Certificate, control: str) -> legacy.Certificate:
    if control not in JOBS:
        raise ReportError("unknown full-roster job")
    poses = list(certificate.poses)
    if control == "duplicate-square-overlap":
        if len(poses) < 2:
            raise ReportError("overlap control requires at least two squares")
        poses[1] = poses[0]
    elif control == "square-translated-outside-container":
        poses[0] = replace(poses[0], x=poses[0].x + certificate.side + 2)
    return replace(certificate, poses=tuple(poses))


def _profile(witness_prefix: str, claim_limitations: str) -> None:
    if (
        type(witness_prefix) is not str
        or len(witness_prefix) > 128
        or re.fullmatch(r"W-[a-z0-9]+(?:-[a-z0-9]+)*-n", witness_prefix) is None
    ):
        raise ReportError("invalid exact witness namespace")
    if (
        type(claim_limitations) is not str
        or not claim_limitations.strip()
        or len(claim_limitations) > 4000
    ):
        raise ReportError("invalid bounded claim limitations")


def to_witness(
    certificate: legacy.Certificate,
    *,
    witness_prefix: str = WITNESS_PREFIX,
    claim_limitations: str = CLAIM_LIMITATIONS,
) -> dict[str, Any]:
    _profile(witness_prefix, claim_limitations)
    witness = legacy.basis_witness(certificate)
    witness["id"] = f"{witness_prefix}{certificate.n:03d}"
    witness["claim"]["limitations"] = claim_limitations
    return witness


def run_case(
    certificate: legacy.Certificate,
    control: str,
    *,
    witness_prefix: str = WITNESS_PREFIX,
    claim_limitations: str = CLAIM_LIMITATIONS,
) -> dict[str, Any]:
    """Reuse the two exact routes in legacy.decide, retaining their full native results."""
    actual = job_input(certificate, control)
    started = time.monotonic()
    cpu = time.process_time()
    first, _report = legacy.exact_verify(
        to_witness(actual, witness_prefix=witness_prefix, claim_limitations=claim_limitations)
    )
    first_seconds = time.process_time() - cpu
    cpu = time.process_time()
    second = legacy.independent.check_squares(legacy.corner_squares(actual), actual.side)
    second_seconds = time.process_time() - cpu
    return json.loads(
        _json_bytes(
            {
                "n": actual.n,
                "control": control,
                "checker_input": checker_input(actual),
                "exact_verify": first,
                "independent": second,
                "cpu_seconds": {"exact_verify": first_seconds, "independent": second_seconds},
                "wall_seconds": time.monotonic() - started,
            }
        )
    )


def _seconds(value: Any) -> None:
    if type(value) not in (int, float) or not math.isfinite(value) or value < 0:
        raise ReportError("invalid measured job time")


def _rational(value: Any) -> Fraction:
    if (
        type(value) is not str
        or len(value) > 1024
        or re.fullmatch(r"-?[0-9]+(?:/[1-9][0-9]*)?", value) is None
    ):
        raise ReportError("invalid exact diagnostic")
    return Fraction(value)


def validate_job(
    row: Any,
    certificate: legacy.Certificate,
    control: str,
    *,
    witness_prefix: str = WITNESS_PREFIX,
    claim_limitations: str = CLAIM_LIMITATIONS,
) -> None:
    _profile(witness_prefix, claim_limitations)
    actual = job_input(certificate, control)
    n = certificate.n
    if (
        type(row) is not dict
        or set(row)
        != {
            "n",
            "control",
            "checker_input",
            "exact_verify",
            "independent",
            "cpu_seconds",
            "wall_seconds",
        }
        or type(row["n"]) is not int
        or row["n"] != n
        or row["control"] != control
        or _json_bytes(row["checker_input"]) != _json_bytes(checker_input(actual))
    ):
        raise ReportError("full native deciding input differs from complete source/control")
    _seconds(row["wall_seconds"])
    if type(row["cpu_seconds"]) is not dict or set(row["cpu_seconds"]) != set(ROUTES):
        raise ReportError("incomplete measured route roster")
    passed = control == "positive"
    for route in ROUTES:
        _seconds(row["cpu_seconds"][route])
        verdict = row[route]
        if (
            type(verdict) is not dict
            or set(verdict) != (EXACT_KEYS if route == "exact_verify" else INDEPENDENT_KEYS)
            or verdict["verification_passed"] is not passed
            or type(verdict["n"]) is not int
            or verdict["n"] != n
            or verdict["side"] != legacy.literal(actual.side)
            or type(verdict["pairs_tested"]) is not int
            or verdict["pairs_tested"] != n * (n - 1) // 2
            or type(verdict["failures"]) is not list
            or bool(verdict["failures"]) is passed
            or verdict["coordinate_provenance"] != ("verified" if passed else "not-established")
            or verdict["method"] != "exact-algebraic"
        ):
            raise ReportError("incomplete or inconsistent native exact route result")
        wall = _rational(verdict["minimum_containment_clearance"])
        gap = _rational(verdict["minimum_best_pair_gap"])
        if (
            (passed and (wall < 0 or gap < 0))
            or (control == "duplicate-square-overlap" and gap >= 0)
            or (control == "square-translated-outside-container" and wall >= 0)
        ):
            raise ReportError("native diagnostics disagree with required control outcome")
        if route == "exact_verify":
            if (
                verdict["operation"] != "verify"
                or verdict["id"] != f"{witness_prefix}{n:03d}"
                or verdict["field_certificate"]
                != {"field": "Q", "preconditions": "degree-one rational field"}
                or verdict["limitations"]
                != ("Verifies witness feasibility and its upper bound, not global optimality.")
            ):
                raise ReportError("wrong exact route identity, field or limitations")
        elif verdict["field"] != "Q" or verdict["limitations"] != (
            "Verifies witness feasibility and its upper bound, not optimality."
        ):
            raise ReportError("wrong independent route field or limitations")


def _stable(row: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in row.items() if key not in {"cpu_seconds", "wall_seconds"}
    }


def check_certification(
    numbers: list[int] | None = None, *, replay: bool = False
) -> dict[int, Any]:
    selected = list(NUMBERS) if numbers is None else numbers
    if not selected or len(set(selected)) != len(selected):
        raise ReportError("empty or repeated confirmation selection")
    for n in selected:
        _count(n)
    facts = read_facts()
    if not receipt_path().resolve().is_relative_to(REPO.resolve()):
        raise ReportError("actual receipt must remain private to this repository")
    record = read_xz(receipt_path())
    if (
        type(record) is not dict
        or set(record) != {"format", "routes", "cases"}
        or record["format"] != RECEIPT_FORMAT
        or record["routes"] != list(ROUTES)
        or type(record["cases"]) is not list
        or len(record["cases"]) != len(NUMBERS) * len(JOBS)
    ):
        raise ReportError("incomplete nine-job exact certification envelope")
    result: dict[int, Any] = {}
    expected = [(n, control) for n in NUMBERS for control in JOBS]
    for (n, control), row in zip(expected, record["cases"], strict=True):
        validate_job(row, facts[n], control)
        if replay and n in selected and _stable(run_case(facts[n], control)) != _stable(row):
            raise ReportError("fresh native replay differs from retained actual result")
        if control == "positive":
            result[n] = row
    return result


def confirmed_bound(n: int) -> dict[str, Any]:
    row = check_certification([n])[n]
    return {
        "value": legacy.ceiling_decimal(Fraction(row["checker_input"]["side"]), 16),
        "exact_form": row["checker_input"]["side"],
        "evidence": [EXACT_EVIDENCE],
    }


def run_child(job: tuple[int, str], directory: Path, timeout: int) -> dict[str, Any]:
    n, control = job
    path = directory / f"n{n}-{control}.json"
    command = [
        sys.executable,
        "-m",
        "devtools.evand_arrangement_reports",
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
            _json_bytes(
                {
                    "n": n,
                    "control": control,
                    "status": "timeout",
                    "timeout_seconds": timeout,
                }
            )
        )
        raise ReportError(f"n={n} {control}: deciding child exceeded {timeout}s") from error
    # Preserve partial/failure evidence even if another job refuses or times out.
    path.with_suffix(".stdout.log").write_bytes(completed.stdout)
    path.with_suffix(".stderr.log").write_bytes(completed.stderr)
    if completed.returncode != 0:
        raise ReportError(f"n={n} {control}: deciding child exited {completed.returncode}")
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ReportError("native child receipt exceeds existing ceiling")
    return json.loads(data, object_pairs_hook=_unique)


def certify(directory: Path, *, workers: int = 2, timeout: int = JOB_TIMEOUT) -> None:
    if type(workers) is not int or not 1 <= workers <= 3 or not 1 <= timeout <= JOB_TIMEOUT:
        raise ReportError("invalid bounded replay allocation")
    read_facts()
    directory.mkdir(parents=True, exist_ok=True)
    jobs = [(n, control) for n in NUMBERS for control in JOBS]
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(run_child, job, directory, timeout) for job in jobs]
        rows = [future.result() for future in futures]
    facts = read_facts()
    for (n, control), row in zip(jobs, rows, strict=True):
        validate_job(row, facts[n], control)
    save_xz(receipt_path(), {"format": RECEIPT_FORMAT, "routes": list(ROUTES), "cases": rows})
    check_certification()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("import-facts")
    certification = commands.add_parser("certify")
    certification.add_argument("--jobs-dir", type=Path, required=True)
    certification.add_argument("--workers", type=int, default=2)
    certification.add_argument("--timeout", type=int, default=JOB_TIMEOUT)
    check = commands.add_parser("check")
    check.add_argument("--n", type=int, nargs="+")
    check.add_argument("--replay", action="store_true")
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
        check_certification(args.n, replay=args.replay)
        print("#399: three complete positive packings and six full-roster controls admitted")
    else:
        row = run_case(read_fact(args.n), args.control)
        validate_job(row, read_fact(args.n), args.control)
        with atomic_output_file(args.output) as temporary:
            temporary.write_bytes(_json_bytes(row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
