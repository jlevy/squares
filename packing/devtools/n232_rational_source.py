"""Read issue 1062's original rational fact and its explicitly selected GMP native jobs.

The acquisition record is the upstream member manifest. Receipt membership is held to
all original rational coordinates and all three standard controls. This module creates
no receipt by loading a source, and a missing or experimental receipt is refused.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import TYPE_CHECKING, Any

from gmpy2 import version as gmp_version

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports
from devtools.retained_data import gunzip_bytes

if TYPE_CHECKING:
    from devtools.upper_bound_houses import Source

PACKET = reports.WEB / "de-winter-1060-1063-2026-11-21"
SOURCE_KEY = "[de Winter n232 rational certificate 2026-11-21]"
ACQUISITION = Path("acquisition/sources.json")
ORIGINAL = Path("n232/candidate.json.gz")
RECEIPT = Path("n232/receipts/native-exact-gmp.json.xz")
EXECUTION = Path("n232/receipts/native-exact-gmp-execution.json")
FORMAT = "de-winter-1062-native-exact-gmp-v1"
EXECUTION_FORMAT = "exact-rational-backend-execution-v1"
ARCHIVE_URL = "https://github.com/user-attachments/files/35205219/n232-rational.zip"
WITNESS_PREFIX = "W-de-winter-1062-n"
LIMITATIONS = (
    "Original issue 1062 rational side and poses, with exact native GMP replay. "
    "Finite feasibility only; no priority, local minimality or global optimality."
)


def _require(condition: object, message: str) -> None:
    if not condition:
        raise kernel.ReportError(message)


def certificate(n: int, packet: Path = PACKET) -> legacy.Certificate:
    """Read the original compressed member, bounded and pinned at the upstream boundary."""
    _require(type(n) is int and n == 232, "issue 1062 supplies only n=232")
    manifest = packet / ACQUISITION
    path = packet / ORIGINAL
    reports.ensure_private(manifest)
    reports.ensure_private(path)
    acquisition = json.loads(manifest.read_text(encoding="utf-8"))
    _require(acquisition["attachment"]["url"] == ARCHIVE_URL, "wrong source archive")
    members = [row for row in acquisition["members"] if row["path"] == "232/candidate.json.gz"]
    _require(len(members) == 1, "original source member is not unique")
    member = members[0]
    with path.open("rb") as stream:
        raw = stream.read(reports.MAX_SOURCE_BYTES + 1)
    _require(
        len(raw) <= reports.MAX_SOURCE_BYTES
        and len(raw) == member["bytes"]
        and member["retained_at"] == ORIGINAL.as_posix()
        and hashlib.sha256(raw).hexdigest() == member["sha256"],
        "source member differs from its original acquisition manifest",
    )
    decoded = gunzip_bytes(raw, limit=reports.MAX_SOURCE_BYTES, name=str(ORIGINAL))
    exact = reports.parse_certificate(decoded, n, "rational-supplement-json", {})
    reports.admit(exact, "15.759531623541")
    return exact


def jobs(n: int, exact: legacy.Certificate, packet: Path = PACKET) -> Mapping[str, Any]:
    """Require all real native jobs and the explicit backend execution declaration."""
    _require(exact == certificate(n, packet), "writer certificate differs from original source")
    reports.ensure_private(packet / EXECUTION)
    reports.ensure_private(packet / RECEIPT)
    execution = json.loads((packet / EXECUTION).read_text(encoding="utf-8"))
    _require(
        execution.get("format") == EXECUTION_FORMAT
        and execution.get("rational_backend") == "gmp"
        and execution.get("implementation") == "gmpy2"
        and execution.get("version") == "2.3.1"
        and execution.get("complete_standard_jobs") == list(kernel.JOBS)
        and execution.get("status") == "completed-native-replay",
        "missing completed native GMP execution declaration",
    )
    record = kernel.read_xz(packet / RECEIPT)
    kernel.validate_receipt(
        record,
        {n: exact},
        receipt_format=FORMAT,
        witness_prefix=WITNESS_PREFIX,
        claim_limitations=LIMITATIONS,
    )
    return {row["control"]: row for row in record["cases"]}


def house_source(result: str, packet: Path = PACKET) -> Source:
    """The result ID is allocated by the registering lane, not by this source reader."""
    from devtools.upper_bound_houses import Origin, Source  # noqa: PLC0415

    def origin(n: int) -> Origin:
        _require(n == 232, "issue 1062 supplies only n=232")
        return Origin(
            key=SOURCE_KEY,
            path=packet / ORIGINAL,
            url=f"{ARCHIVE_URL}#232/candidate.json.gz",
            revision="n232-rational.zip, issue 1062 attachment 35205219",
            retrieved="2026-11-21",
            author="Joost de Winter after Kodaj and JoeGun; Alex Chilton source compilation",
            licence_status="no-licence-published",
            raw_asset_retained=True,
            retention_policy=(
                "Original gzip member retained byte-for-byte; acquisition manifest pins "
                "the upstream archive and member."
            ),
        )

    def inputs(numbers: Sequence[int]) -> tuple[Path, ...]:
        _require(list(numbers) == [232], "issue 1062 custody requires exactly n=232")
        return tuple(
            packet / relative for relative in (ACQUISITION, ORIGINAL, RECEIPT, EXECUTION)
        )

    return Source(
        result=result,
        key=SOURCE_KEY,
        packet=packet,
        certificate=lambda n: certificate(n, packet),
        jobs=lambda n, exact: jobs(n, exact, packet),
        origin=origin,
        inputs=inputs,
        witness_prefix=WITNESS_PREFIX,
        claim_limitations=LIMITATIONS,
        stored=lambda _n: packet / ORIGINAL,
        receipt=lambda _n: packet / RECEIPT,
        rational_backend="gmp",
    )


def assemble(
    paths: Sequence[Path], receipt_out: Path, execution_out: Path, packet: Path = PACKET
) -> None:
    """Assemble only actual one-job outputs, with complete source/control membership."""
    exact = certificate(232, packet)
    _require(len(paths) == len(kernel.JOBS), "exactly three one-job outputs are required")
    records = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    rows = []
    for record, control in zip(records, kernel.JOBS, strict=True):
        _require(
            record.get("format") == EXECUTION_FORMAT
            and record.get("rational_backend") == "gmp"
            and record.get("implementation") == "gmpy2"
            and record.get("version") == "2.3.1",
            "one-job output lacks its explicit exact backend",
        )
        row = record["native"]
        kernel.validate_job(
            row,
            exact,
            control,
            witness_prefix=WITNESS_PREFIX,
            claim_limitations=LIMITATIONS,
        )
        rows.append(row)
    receipt = {"format": FORMAT, "routes": list(kernel.ROUTES), "cases": rows}
    kernel.validate_receipt(
        receipt,
        {232: exact},
        receipt_format=FORMAT,
        witness_prefix=WITNESS_PREFIX,
        claim_limitations=LIMITATIONS,
    )
    kernel.save_xz(receipt_out, receipt)
    execution = {
        "format": EXECUTION_FORMAT,
        "rational_backend": "gmp",
        "implementation": "gmpy2",
        "version": "2.3.1",
        "complete_standard_jobs": list(kernel.JOBS),
        "status": "completed-native-replay",
        "program": "devtools.n232_rational_source",
        "note": "Three actual outputs of the explicitly selected exact scalar backend; "
        "ordinary Fraction APIs remain unchanged. Memory/wall guard logs accompany the run.",
    }
    execution_out.write_text(json.dumps(execution, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packet", type=Path, default=PACKET)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--control", choices=kernel.JOBS)
    mode.add_argument("--assemble", nargs=3, type=Path, metavar="JOB_JSON")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--execution-out", type=Path)
    args = parser.parse_args()
    if args.assemble:
        if args.execution_out is None:
            parser.error("--assemble requires --execution-out")
        assemble(args.assemble, args.out, args.execution_out, args.packet)
        return 0
    exact = certificate(232, args.packet)
    row = kernel.run_case(
        exact,
        args.control,
        witness_prefix=WITNESS_PREFIX,
        claim_limitations=LIMITATIONS,
        rational_backend="gmp",
    )
    kernel.validate_job(
        row,
        exact,
        args.control,
        witness_prefix=WITNESS_PREFIX,
        claim_limitations=LIMITATIONS,
    )
    # External orchestration supplies the wall/memory guard and persists its journals.
    # This one-job output is never enough to satisfy jobs(), which requires the roster.
    output = {
        "format": EXECUTION_FORMAT,
        "rational_backend": "gmp",
        "implementation": "gmpy2",
        "version": gmp_version(),
        "native": row,
    }
    args.out.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"n=232 {args.control}: complete exact GMP job, {row['wall_seconds']:.3f} seconds")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
