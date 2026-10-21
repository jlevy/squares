"""Decide issue #686's 100 rational upper bounds beyond the corpus, from derived facts.

Darius Muglich's issue #686 attaches ``01-squares-100-certificates-and-poses.zip``, pinned
only by its address and SHA-256: an issue attachment has no commit, so
``devtools.acquire_source`` cannot take it. The packet follows SQUISH #401's attachment
(``squish-401-2026-10-07``): it keeps derived facts and the archive's address and digest,
not the archive's bytes. Its README says what is retained, the credit and the licence.

- ``derive --archive ZIP`` reads a local copy of the attachment as data, refuses it unless
  its size and SHA-256 are the issue's, parses the 100 certificates in Evan Daniel's
  ``n S`` / ``x y t`` format, admits each only where its exact side rounds up to the
  issue's print at 15 places, and writes ``facts/n-NNN.json.gz`` (side, centres and
  half-angle tangents, exactly) and ``acquisition/sources.json`` (every member's path,
  size and SHA-256). ``--check`` rebuilds both from the archive and compares.
- ``claims-record`` writes ``acquisition/beyond-horizon-claims.json``, which
  ``check_source_coverage`` reads each beyond-horizon row against.
- ``certify`` runs a positive, a duplicate-square and an outside-container job per count
  through the two exact routes of ``devtools.evand_arrangement_reports`` (every pair, no
  filter), each job in its own child process, and writes one receipt per count as soon as
  its three jobs pass, ``receipts/exact-replay-nNNN.json.xz``. It is resumable: a count
  whose receipt is admitted is skipped, and a finished job in ``--jobs-dir`` is reused.
- ``check`` admits facts, claims record and receipts; ``--replay`` decides again.

From ``packing/``, with the project interpreter::

    python -m devtools.muglich_686_import derive --archive ZIP [--check]
    python -m devtools.muglich_686_import claims-record [--check]
    nice -n 10 python -m devtools.muglich_686_import certify --jobs-dir DIR --workers 2
    python -m devtools.muglich_686_import check [--n N ...] [--replay]

A finite packing certifies an upper bound and nothing more: novelty, priority, rigidity
and optimality are not decided here. No program from the archive runs.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from collections.abc import Collection
from concurrent.futures import ThreadPoolExecutor, as_completed
from fractions import Fraction
from pathlib import Path
from typing import Any, cast

from strif import atomic_output_file

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools.retained_data import read_retained_bytes
from devtools.upper_bound_reports import BEYOND_FORMAT, DISPLAY_PLACES, HORIZON

MODULE = "devtools.muglich_686_import"
ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
PACKET = ROOT / "resources/web/muglich-issue686-2026-10-19"
ISSUE_RECORD = PACKET / "acquisition/issue-686.json"
SOURCES = PACKET / "acquisition/sources.json"
BEYOND = PACKET / "acquisition/beyond-horizon-claims.json"
#: The per-case provenance the issue asks to keep, as attribution metadata in one file.
CREDITS = PACKET / "acquisition/provenance.json.gz"
ISSUE_URL = "https://github.com/jlevy/squares/issues/686"
ARCHIVE_NAME = "01-squares-100-certificates-and-poses.zip"
ARCHIVE_URLS = tuple(
    f"https://github.com/user-attachments/files/{number}/{ARCHIVE_NAME}"
    for number in (33685905, 33685972)
)
ARCHIVE_BYTES = 8_824_142
ARCHIVE_SHA256 = "6b711d6e80c9828497ba09d44673ee490c00ccae51b80587ec591d940722a874"
ARCHIVE_MEMBERS = 808
PUBLISHED = "2026-10-19T20:43:04Z"
RETRIEVED = "2026-10-20"
COUNTS = (
    *(328, 330, 339, 344, 365, *range(377, 382), 404, 412, *range(417, 423), 453),
    *(*range(459, 465), 496, *range(502, 507), 508, 548, *range(550, 555), 595),
    *(*range(597, 604), *range(647, 653), 654, *range(700, 707), *range(755, 761)),
    *(*range(810, 818), *range(868, 876), *range(927, 931), *range(932, 936)),
    *range(989, 999),
)
PLACES = 15
SOURCES_FORMAT = "muglich-686-attachment-sources-v1"
CREDITS_FORMAT = "muglich-686-provenance-v1"
FACT_FORMAT = "muglich-686-certificate-fact-v1"
RECEIPT_FORMAT = "muglich-686-exact-replay-v1"
WITNESS_PREFIX = "W-muglich-686-n"
CLAIM_LIMITATIONS = (
    "Complete #686 rational centre/half-angle certificate converted exactly. Certifies "
    "this feasible upper-bound construction, not novelty, priority, rigidity, local "
    "minimality or global optimality."
)
PROFILE = {"witness_prefix": WITNESS_PREFIX, "claim_limitations": CLAIM_LIMITATIONS}
MAX_MEMBER_BYTES = 2_000_000
#: The kernel's own ceiling is 600 s; a 998-square job takes about 184 CPU-s, and a
#: niced child on a shared host gets less than a whole CPU, so the wall allowance is wider.
JOB_TIMEOUT = 1800
MAX_WORKERS = 2
_ROW = re.compile(r"^\| (\d+) \| (\d+\.\d{15}) \| `[0-9/]+` \|$", re.MULTILINE)


class Muglich686Error(ValueError):
    """Refuse a changed archive, an unadmitted certificate, fact, record or receipt."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise Muglich686Error(message)


def _private(path: Path) -> Path:
    _require(
        not path.is_symlink() and path.resolve().is_relative_to(REPO.resolve()),
        f"{path}: retained evidence must be a private repository file",
    )
    return path


def _json_text(value: Any) -> str:
    return json.dumps(value, indent=1, ensure_ascii=False) + "\n"


def fact_path(n: int) -> Path:
    return PACKET / f"facts/n-{n:03d}.json.gz"


def receipt_path(n: int) -> Path:
    return PACKET / f"receipts/exact-replay-n{n:03d}.json.xz"


def member_path(n: int) -> str:
    return f"certificates/n{n}.cert"


def printed_sides() -> dict[int, str]:
    """The side the issue prints at each count, read from the frozen issue record."""
    record = json.loads(_private(ISSUE_RECORD).read_text(encoding="utf-8"))
    _require(
        record.get("html_url") == ISSUE_URL and record.get("created_at") == PUBLISHED,
        "the frozen issue record is not issue 686 as opened",
    )
    printed = {int(n): side for n, side in _ROW.findall(record["body"])}
    _require(tuple(printed) == COUNTS, "the issue's table is not the 100 declared counts")
    return printed


def admit(certificate: legacy.Certificate, printed: str) -> None:
    """The exact side must round up to the issue's print: ``P - 10^-15 < S <= P``."""
    bound = Fraction(printed)
    _require(
        bound - Fraction(1, 10**PLACES) < certificate.side <= bound,
        f"n={certificate.n}: the exact side does not round up to the issue's {printed}",
    )


def fact_bytes(certificate: legacy.Certificate) -> bytes:
    """A certificate's derived fact: its exact side and poses, as deterministic gzip."""
    fact = {
        "format": FACT_FORMAT,
        "n": certificate.n,
        "side": legacy.literal(certificate.side),
        "poses": [
            [legacy.literal(pose.x), legacy.literal(pose.y), legacy.literal(pose.t)]
            for pose in certificate.poses
        ],
    }
    text = json.dumps(fact, separators=(",", ":")) + "\n"
    return gzip.compress(text.encode("ascii"), compresslevel=9, mtime=0)


def read_fact(n: int) -> legacy.Certificate:
    """Admit one fact: parsed by the certificate format's own reader, and its own rebuild."""
    _require(n in COUNTS, f"n={n} is not one of issue 686's counts")
    path = _private(fact_path(n))
    raw = path.read_bytes()
    fact: Any = json.loads(read_retained_bytes(path), object_pairs_hook=kernel.unique_object)
    _require(
        type(fact) is dict
        and set(fact) == {"format", "n", "side", "poses"}
        and fact["format"] == FACT_FORMAT
        and fact["n"] == n
        and type(fact["poses"]) is list,
        f"n={n}: malformed derived fact",
    )
    poses = cast("list[list[str]]", fact["poses"])
    rows = [f"{n} {fact['side']}", *(" ".join(pose) for pose in poses)]
    certificate = legacy.parse("\n".join(rows) + "\n", expected_n=n)
    _require(fact_bytes(certificate) == raw, f"n={n}: derived fact differs from its rebuild")
    return certificate


def read_facts(numbers: Collection[int] = COUNTS) -> dict[int, legacy.Certificate]:
    """Admit the selected facts, each against the side the issue prints and the manifest."""
    printed = printed_sides()
    members = {row["n"]: row for row in json.loads(SOURCES.read_text("utf-8"))["members"]}
    certificates = {}
    for n in numbers:
        certificate = read_fact(n)
        admit(certificate, printed[n])
        _require(
            members[n]["side"] == legacy.literal(certificate.side),
            f"n={n}: the manifest's side is not the fact's",
        )
        certificates[n] = certificate
    return certificates


# --------------------------------------------------------------------------- custody


def archive_bytes(path: Path) -> bytes:
    with path.open("rb") as stream:
        data = stream.read(ARCHIVE_BYTES + 1)
    _require(
        len(data) == ARCHIVE_BYTES and hashlib.sha256(data).hexdigest() == ARCHIVE_SHA256,
        "the archive is not the attachment issue 686 pins by size and SHA-256",
    )
    return data


def derive(archive: Path) -> tuple[dict[str, Any], dict[int, bytes], bytes]:
    """The manifest, every fact and the provenance record, from the attachment's bytes."""
    printed = printed_sides()
    with zipfile.ZipFile(io.BytesIO(archive_bytes(archive))) as bundle:
        infos = bundle.infolist()
        _require(len(infos) == ARCHIVE_MEMBERS, "unexpected archive member count")
        manifest, facts, sides, origins = [], {}, {}, {}
        for info in sorted(infos, key=lambda item: item.filename):
            name = info.filename
            _require(
                not name.startswith("/") and ".." not in name.split("/") and not info.is_dir(),
                f"{name}: not a plain member path",
            )
            _require(info.file_size <= MAX_MEMBER_BYTES * 10, f"{name}: oversized member")
            data = bundle.read(info)
            manifest.append(
                {"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            )
            credit = re.fullmatch(r"prepared/cases/n0*([1-9]\d*)/provenance\.json", name)
            if credit is not None:
                origins[int(credit.group(1))] = json.loads(data.decode("utf-8"))
            match = re.fullmatch(r"certificates/n([1-9]\d*)\.cert", name)
            if match is None:
                continue
            n = int(match.group(1))
            _require(len(data) <= MAX_MEMBER_BYTES, f"{name}: oversized certificate")
            certificate = legacy.parse(data.decode("ascii"), expected_n=n)
            admit(certificate, printed[n])
            facts[n] = fact_bytes(certificate)
            sides[n] = (manifest[-1], legacy.literal(certificate.side))
    _require(tuple(sorted(facts)) == COUNTS, "the archive's certificates are not the 100")
    _require(tuple(sorted(origins)) == COUNTS, "the archive's provenance is not the 100")
    provenance = {
        "format": CREDITS_FORMAT,
        "cases": [
            {
                "n": n,
                "member": f"prepared/cases/n{n:04d}/provenance.json",
                "provenance": origins[n],
            }
            for n in COUNTS
        ],
    }
    text = json.dumps(provenance, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    packed = gzip.compress((text + "\n").encode("utf-8"), compresslevel=9, mtime=0)
    record = {
        "format": SOURCES_FORMAT,
        "issue": ISSUE_URL,
        "published": PUBLISHED,
        "archive": {
            "name": ARCHIVE_NAME,
            "urls": list(ARCHIVE_URLS),
            "bytes": ARCHIVE_BYTES,
            "sha256": ARCHIVE_SHA256,
            "retrieved": RETRIEVED,
            "raw_asset_retained": False,
        },
        "members": [
            {
                "n": n,
                "path": member_path(n),
                "bytes": sides[n][0]["bytes"],
                "sha256": sides[n][0]["sha256"],
                "side": sides[n][1],
                "printed": printed[n],
                "fact": fact_path(n).relative_to(PACKET).as_posix(),
            }
            for n in COUNTS
        ],
        "provenance": CREDITS.relative_to(PACKET).as_posix(),
        "archive_manifest": manifest,
    }
    return record, facts, packed


def write_derived(archive: Path, *, check: bool) -> None:
    record, facts, packed = derive(archive)
    if check:
        _require(SOURCES.read_text("utf-8") == _json_text(record), "manifest differs")
        _require(_private(CREDITS).read_bytes() == packed, "provenance record differs")
        for n, data in facts.items():
            _require(_private(fact_path(n)).read_bytes() == data, f"n={n}: fact differs")
        return
    for n, data in facts.items():
        fact_path(n).parent.mkdir(parents=True, exist_ok=True)
        with atomic_output_file(_private(fact_path(n))) as temporary:
            temporary.write_bytes(data)
    with atomic_output_file(_private(CREDITS)) as temporary:
        temporary.write_bytes(packed)
    with atomic_output_file(_private(SOURCES)) as temporary:
        temporary.write_text(_json_text(record), encoding="utf-8")


def check_manifest() -> None:
    """The manifest pins the attachment and names the 100 certificates and their facts.

    The facts and the provenance record are this repository's files, identified by Git
    and their paths (OR-16); ``derive --check`` is what binds them to the attachment.
    """
    record = json.loads(SOURCES.read_text("utf-8"))
    _require(record["format"] == SOURCES_FORMAT, "unknown manifest format")
    _require(record["archive"]["raw_asset_retained"] is False, "the archive is not retained")
    _require([row["n"] for row in record["members"]] == list(COUNTS), "manifest roster")
    paths = {row["path"] for row in record["archive_manifest"]}
    _require(len(paths) == ARCHIVE_MEMBERS, "the archive manifest is incomplete")
    _require(
        record["provenance"] == CREDITS.relative_to(PACKET).as_posix()
        and _private(CREDITS).is_file(),
        "the provenance record is missing",
    )
    for row in record["members"]:
        _require(
            row["path"] in paths
            and row["path"] == member_path(row["n"])
            and _private(fact_path(row["n"])).is_file(),
            f"n={row['n']}: the manifest does not name its member and fact",
        )


# --------------------------------------------------------------------------- claims


def claims_record(certificates: dict[int, legacy.Certificate]) -> dict[str, Any]:
    """The beyond-horizon record: each count's print, exact side and 16-place ceiling."""
    printed = printed_sides()
    _require(min(COUNTS) > HORIZON, "every count lies beyond the case corpus")
    return {
        "format": BEYOND_FORMAT,
        "issue": ISSUE_URL,
        "source": ARCHIVE_URLS[0],
        "revision": f"sha256:{ARCHIVE_SHA256}",
        "horizon": HORIZON,
        "results": [
            {
                "n": n,
                "offered_side": printed[n],
                "exact_side": legacy.literal(certificates[n].side),
                "ceiling": legacy.ceiling_decimal(certificates[n].side, DISPLAY_PLACES),
            }
            for n in COUNTS
        ],
    }


# --------------------------------------------------------------------------- replay


def job_output(directory: Path, n: int, control: str) -> Path:
    return directory / f"n{n}-{control}.json"


def run_job(job: tuple[int, str], directory: Path, timeout: int) -> dict[str, Any]:
    """Run one job as ``python -m MODULE decide-job`` in its own child process."""
    n, control = job
    path = job_output(directory, n, control)
    command = [sys.executable, "-m", MODULE, "decide-job", "--n", str(n)]
    command += ["--control", control, "--output", str(path)]
    try:
        completed = subprocess.run(
            command, capture_output=True, timeout=timeout, check=False, cwd=ROOT
        )
    except subprocess.TimeoutExpired as error:
        path.with_suffix(".stderr.log").write_bytes(error.stderr or b"")
        raise Muglich686Error(f"n={n} {control}: deciding child exceeded {timeout}s") from error
    path.with_suffix(".stderr.log").write_bytes(completed.stderr)
    _require(completed.returncode == 0, f"n={n} {control}: child exited {completed.returncode}")
    return read_job(path)


def read_job(path: Path) -> dict[str, Any]:
    with path.open("rb") as stream:
        data = stream.read(kernel.MAX_BYTES + 1)
    _require(len(data) <= kernel.MAX_BYTES, "a job's row exceeds the kernel's ceiling")
    return json.loads(data, object_pairs_hook=kernel.unique_object)


def receipt_admitted(n: int, certificate: legacy.Certificate) -> dict[str, Any] | None:
    """The count's positive row if its receipt exists and is admitted, else None."""
    path = receipt_path(n)
    if not path.exists():
        return None
    record = kernel.read_xz(_private(path))
    positives = kernel.validate_receipt(
        record, {n: certificate}, receipt_format=RECEIPT_FORMAT, **PROFILE
    )
    return positives[n]


def finished_job(directory: Path, n: int, control: str, certificate: legacy.Certificate):
    """A job row an earlier run left, if it is complete and admitted, else None."""
    path = job_output(directory, n, control)
    if not path.exists():
        return None
    try:
        row = read_job(path)
        kernel.validate_job(row, certificate, control, **PROFILE)
    except ValueError, OSError:
        return None
    return row


def save_receipt(n: int, certificate: legacy.Certificate, rows: dict[str, Any]) -> None:
    record = {
        "format": RECEIPT_FORMAT,
        "routes": list(kernel.ROUTES),
        "cases": [rows[control] for control in kernel.JOBS],
    }
    kernel.validate_receipt(record, {n: certificate}, receipt_format=RECEIPT_FORMAT, **PROFILE)
    kernel.save_xz(_private(receipt_path(n)), record)


def certify(
    directory: Path,
    numbers: Collection[int] = COUNTS,
    *,
    workers: int = MAX_WORKERS,
    timeout: int = JOB_TIMEOUT,
) -> list[int]:
    """Decide every job of the selected counts not yet receipted; return those written."""
    _require(1 <= workers <= MAX_WORKERS and 1 <= timeout <= JOB_TIMEOUT, "invalid allocation")
    directory.mkdir(parents=True, exist_ok=True)
    certificates = read_facts(numbers)
    pending: dict[int, dict[str, Any]] = {}
    for n, certificate in certificates.items():
        if receipt_admitted(n, certificate) is not None:
            continue
        pending[n] = {
            control: row
            for control in kernel.JOBS
            if (row := finished_job(directory, n, control, certificate)) is not None
        }
    jobs = [(n, c) for n, rows in pending.items() for c in kernel.JOBS if c not in rows]
    print(f"{len(pending)} counts to receipt, {len(jobs)} jobs to run", flush=True)
    written = []
    for n in [n for n, rows in pending.items() if len(rows) == len(kernel.JOBS)]:
        save_receipt(n, certificates[n], pending[n])
        written.append(n)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(run_job, job, directory, timeout): job for job in jobs}
        for future in as_completed(futures):
            n, control = futures[future]
            pending[n][control] = future.result()
            row = pending[n][control]
            print(f"n={n} {control} {sum(row['cpu_seconds'].values()):.1f} CPU-s", flush=True)
            if len(pending[n]) == len(kernel.JOBS):
                save_receipt(n, certificates[n], pending[n])
                written.append(n)
                print(f"n={n} receipted", flush=True)
    return written


def check(numbers: Collection[int] = COUNTS, *, replay: bool = False) -> dict[str, Any]:
    """Admit manifest, facts, claims record and receipts; with ``replay``, decide again.

    Returns what the receipts hold: jobs, pair decisions, route CPU and job wall seconds,
    the longest job, and the least wall clearance and pair gap of any positive job.
    """
    check_manifest()
    certificates = read_facts(numbers)
    if set(numbers) == set(COUNTS):
        stored = json.loads(_private(BEYOND).read_text("utf-8"))
        _require(stored == claims_record(certificates), "the claims record differs")
    rows = []
    for n, certificate in certificates.items():
        _require(receipt_admitted(n, certificate) is not None, f"n={n}: no receipt")
        record = kernel.read_xz(receipt_path(n))
        if replay:
            kernel.replay_receipt(record, {n: certificate}, {n}, **PROFILE)
        rows.extend(record["cases"])
    positives = [row for row in rows if row["control"] == "positive"]

    def least(field: str) -> str:
        value = min(Fraction(row[route][field]) for row in positives for route in kernel.ROUTES)
        return f"{float(value):.3e}"

    return {
        "counts": len(certificates),
        "jobs": len(rows),
        "pairs": sum(row[route]["pairs_tested"] for row in rows for route in kernel.ROUTES),
        "route_cpu_seconds": round(sum(sum(row["cpu_seconds"].values()) for row in rows), 2),
        "job_wall_seconds": round(sum(row["wall_seconds"] for row in rows), 2),
        "longest_job_seconds": round(max(row["wall_seconds"] for row in rows), 2),
        "least_wall_clearance": least("minimum_containment_clearance"),
        "least_pair_gap": least("minimum_best_pair_gap"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    deriving = commands.add_parser("derive")
    deriving.add_argument("--archive", type=Path, required=True)
    deriving.add_argument("--check", action="store_true")
    claims = commands.add_parser("claims-record")
    claims.add_argument("--check", action="store_true")
    certifying = commands.add_parser("certify")
    certifying.add_argument("--jobs-dir", type=Path, required=True)
    certifying.add_argument("--n", type=int, nargs="+", default=list(COUNTS))
    certifying.add_argument("--workers", type=int, default=MAX_WORKERS)
    certifying.add_argument("--timeout", type=int, default=JOB_TIMEOUT)
    checking = commands.add_parser("check")
    checking.add_argument("--n", type=int, nargs="+", default=list(COUNTS))
    checking.add_argument("--replay", action="store_true")
    child = commands.add_parser("decide-job")
    child.add_argument("--n", type=int, required=True)
    child.add_argument("--control", choices=kernel.JOBS, required=True)
    child.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "derive":
        write_derived(args.archive, check=args.check)
        print("derived facts " + ("match the archive" if args.check else "written"))
    elif args.command == "claims-record":
        record = claims_record(read_facts())
        if args.check:
            stored = json.loads(_private(BEYOND).read_text("utf-8"))
            _require(stored == record, "the claims record differs from its rebuild")
        else:
            with atomic_output_file(_private(BEYOND)) as temporary:
                temporary.write_text(_json_text(record), encoding="utf-8")
        print(f"claims record: {len(record['results'])} rows")
    elif args.command == "certify":
        written = certify(args.jobs_dir, args.n, workers=args.workers, timeout=args.timeout)
        print(f"receipted {len(written)} counts")
    elif args.command == "check":
        print(json.dumps(check(args.n, replay=args.replay)))
    else:
        _require(not args.output.exists(), "refusing to overwrite a deciding job")
        kernel.decide_job(read_fact(args.n), args.control, args.output, **PROFILE)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
