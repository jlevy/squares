"""Check a reported fine-net check2 certificate kept outside Git, and price its replay.

wand125's fine-net certificates of jlevy/squares#446 and its follow-ups are retained as
authored facts and hash references (`resources/web/wand125-fine-net-*`): the release
asset that holds the candidate, its logs and the adapted verifier's source stays outside
live Git, since the nested verifier carries no licence of its own. This tool reads a
local copy of that asset beside the certificate's documents from the pinned tree, and
writes the receipts a packet keeps. It runs no program of the source.

- ``premises`` refuses the asset unless its size and SHA-256 are the pinned ones, unpacks
  it safely (plain files and directories under ``certificates/<name>/`` only), lays the
  pinned tree's documents beside it as the source's ``ASSET.json`` says, and runs the
  maintained check2 reader on the result,
  `devtools.audit_wand125_declared_net.audit_check2`, as a packet would hold it: every
  file ``files-sha256.json`` lists must be present, and each upstream ``.gz`` file is
  given to the reader by the raw digest of the asset's bytes (`packet_view`), as an
  acquisition record pins it. It also times the three narrower
  readers the 8 October n = 27 follow-up ran (``measure``, ``declared_net``,
  ``semantic_digest``), compares the sealed inner bundle with the manifest and with the
  directory, member by member, and records both README editions. It decides no
  coverage.
- ``sample`` runs this repository's ``sqverify-fast`` at chosen directions of the
  candidate's declared net, one process per direction, one thread each, with
  ``--confirm``, at most ``--workers`` at a time. Each direction's verdict, nodes and
  thread CPU come from the binary's own row, and its process CPU (``wait4``, user plus
  system) and wall from here, beside the source's verdict, nodes, least certified bound
  and CPU on the same direction from its run log, with the directions where nodes and
  bound agree. It prices a complete capture twice, by the ratio of the two CPUs on the
  sample times the source's whole-net CPU and by the sample's mean, keeping the larger,
  and the whole-net controls of the 6 October soundness review and its
  FC-1 re-check (the 99/100 mutant at every direction, the original and the
  near-threshold mutant at the least-bound direction) at one more full sweep and two
  directions. A sample is a diagnostic: it decides only the directions it ran, and its
  status says so.

From ``packing/``::

    .venv/bin/python3 -m devtools.fine_net_followup premises \\
        --asset ASSET.tar.gz --sha256 HEX --bytes N --documents CERT_DIR \\
        --name mixed_n29_L582 --n 29 --side 291/50 --work WORK --out RECEIPT
    .venv/bin/python3 -m devtools.fine_net_followup sample \\
        --binary sqverify_fast/target/release/sqverify-fast \\
        --candidate WORK/certificates/mixed_n29_L582/candidate.json --n 29 --side 291/50 \\
        --directions 0,296,592 --workers 2 --source-run WORK/.../check2/run.jsonl.gz \\
        --out RECEIPT
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import platform
import shutil
import sys
import tarfile
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any

from devtools.audit_wand125_declared_net import (
    AuditError,
    Certificate,
    audit_check2,
    declared_net,
    load_json,
    measure,
    require,
    semantic_digest,
    utc_now,
)
from devtools.retained_data import git_blob
from sqpack import retained_json

#: The budget the intake brief sets: a full capture runs in the import's own branch only
#: when its price is at most this many CPU seconds.
FULL_CAPTURE_LIMIT_CPU_SECONDS = 20 * 60
#: Bounds on the asset and on each member it unpacks to, before and after decoding.
MAX_ASSET_BYTES = 64 * 1024 * 1024
MAX_MEMBER_BYTES = 64 * 1024 * 1024
#: The suffix of the sealed inner bundle a check2 directory ships.
BUNDLE_SUFFIX = "-check2-bundle.tar.gz"
#: How long one direction may run before the sample is abandoned.
DIRECTION_TIMEOUT = 3600


def file_digest(path: Path) -> str:
    """The SHA-256 of a file, read in blocks."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_members(archive: tarfile.TarFile, root: PurePosixPath) -> list[tarfile.TarInfo]:
    """Every member, refused unless each is a plain file or directory under ``root``,
    within the member bound."""
    members = archive.getmembers()
    for member in members:
        name = PurePosixPath(member.name)
        require(
            not name.is_absolute()
            and ".." not in name.parts
            and name.parts[: len(root.parts)] == root.parts
            and (member.isfile() or member.isdir())
            and member.size <= MAX_MEMBER_BYTES,
            f"unexpected archive member: {member.name}",
        )
    return members


def unpack_asset(asset: Path, sha256: str, size: int, name: str, work: Path) -> Path:
    """The pinned asset, unpacked afresh under ``work``; the certificate directory."""
    require(asset.stat().st_size == size <= MAX_ASSET_BYTES, f"{asset} is not {size} bytes")
    require(file_digest(asset) == sha256, f"{asset} is not the pinned asset")
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    with tarfile.open(asset, "r:gz") as archive:
        safe_members(archive, PurePosixPath("certificates", name))
        archive.extractall(work, filter="data")
    return work / "certificates" / name


def inventory(directory: Path, names: list[str]) -> list[dict[str, Any]]:
    """Each named file's size, SHA-256 and Git blob."""
    rows = []
    for name in names:
        data = (directory / name).read_bytes()
        rows.append(
            {
                "path": name,
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
                "git_blob": git_blob(data),
            }
        )
    return rows


def lay_documents(documents: Path, directory: Path) -> list[str]:
    """Copy the pinned tree's documents into the unpacked directory, refusing any that
    the asset already holds: the two are disjoint by the source's layout."""
    laid = []
    for path in sorted(p for p in documents.rglob("*") if p.is_file()):
        relative = path.relative_to(documents)
        target = directory / relative
        require(not target.exists(), f"{relative} is in both the asset and the documents")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
        laid.append(relative.as_posix())
    return laid


def packet_view(directory: Path, name: str, view: Path) -> dict[str, str]:
    """The directory as a packet holds it, and the digests of what it pins only.

    A packet stores an upstream file whose own name ends in ``.gz`` by digest alone
    (`devtools.acquire_source`), and the check2 reader decompresses any ``.gz`` it finds,
    so the reader is given a copy of every other file under ``view`` and the raw
    SHA-256 of each ``.gz`` file by its upstream path, as an acquisition record's
    pinned-only files would give it.
    """
    pins: dict[str, str] = {}
    if view.exists():
        shutil.rmtree(view)
    for path in sorted(p for p in directory.rglob("*") if p.is_file()):
        relative = path.relative_to(directory)
        if path.name.endswith(".gz"):
            pins[f"certificates/{name}/{relative.as_posix()}"] = file_digest(path)
            continue
        target = view / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    return pins


def sealed_bundle(
    directory: Path, listed: dict[str, str], asset_files: list[str]
) -> dict[str, Any]:
    """The sealed inner bundle beside the manifest it carries and the asset around it.

    Every name ``files-sha256.json`` lists must be a member of the bundle's one top-level
    directory with that digest, and every regular member must be listed or be the
    manifest itself. Members byte-identical to the outer asset's file at the same path
    are the repeated payloads.
    """
    bundles = sorted(directory.glob(f"*{BUNDLE_SUFFIX}"))
    require(len(bundles) == 1, f"{len(bundles)} sealed bundles in {directory}")
    top = PurePosixPath(bundles[0].name.removesuffix(".tar.gz"))
    inner: dict[str, str] = {}
    sizes: dict[str, int] = {}
    with tarfile.open(bundles[0], "r:gz") as archive:
        for member in safe_members(archive, top):
            if member.isfile():
                stream = archive.extractfile(member)
                require(stream is not None, f"{member.name} cannot be read")
                assert stream is not None
                relative = PurePosixPath(member.name).relative_to(top).as_posix()
                inner[relative] = hashlib.sha256(stream.read()).hexdigest()
                sizes[relative] = member.size
    require(
        all(inner.get(name) == value for name, value in listed.items()),
        "a listed file is not the sealed bundle's",
    )
    require(
        set(inner) <= {*listed, "files-sha256.json"},
        f"the sealed bundle holds unlisted files: {sorted(set(inner) - {*listed})}",
    )
    repeated = sorted(
        name
        for name, value in inner.items()
        if name in asset_files and file_digest(directory / name) == value
    )
    return {
        "name": bundles[0].name,
        "sha256": file_digest(bundles[0]),
        "bytes": bundles[0].stat().st_size,
        "regular_members": len(inner),
        "members": [
            {"path": name, "bytes": sizes[name], "sha256": inner[name]}
            for name in sorted(inner)
        ],
        "listed_hashes_matching": len(listed),
        "repeated_payloads": repeated,
        "sealed_readme_sha256": inner.get("README.md"),
    }


def premises(
    asset: Path,
    stated: Certificate,
    *,
    sha256: str,
    size: int,
    documents: Path,
    work: Path,
) -> dict[str, Any]:
    """Every exact premise of the unpacked certificate, with its custody facts."""
    directory = unpack_asset(asset, sha256, size, stated.name, work)
    asset_files = sorted(
        p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()
    )
    laid = lay_documents(documents, directory)
    raw = (directory / "candidate.json").read_bytes()
    start = time.perf_counter()
    candidate = load_json(raw)
    total, positive = measure(candidate, stated)
    step, count, facts, checks = declared_net(candidate)
    digest = semantic_digest(candidate)
    narrow_wall = time.perf_counter() - start
    view = work / "view" / stated.name
    pins = packet_view(directory, stated.name, view)
    start = time.perf_counter()
    audit = audit_check2(view, stated, pins=pins)
    audit_wall = time.perf_counter() - start
    listed = load_json((directory / "files-sha256.json").read_bytes())
    sealed = sealed_bundle(directory, listed, asset_files)
    pinned_readme = file_digest(directory / "README.md")
    return {
        "kind": "fine-net-followup-premises/v1",
        "certificate": stated.name,
        "claim": audit["claim"],
        "asset": {
            "sha256": sha256,
            "bytes": size,
            "files": inventory(directory, asset_files),
        },
        "documents": inventory(directory, laid),
        "candidate_sha256": hashlib.sha256(raw).hexdigest(),
        "candidate_digest": digest,
        "maintained_input_premises": {
            "candidate_rows": len(candidate["rectangles"]),
            "positive_rows": positive,
            "mass": str(total),
            "core": str(Fraction(candidate["B"])),
            "step": str(step),
            "directions": count,
            "checks": checks,
            "facts": {name: str(value) for name, value in facts.items()},
            "entrypoints": [
                "audit_wand125_declared_net.measure",
                "audit_wand125_declared_net.declared_net",
                "audit_wand125_declared_net.semantic_digest",
            ],
            "wall_seconds": narrow_wall,
        },
        "check2_audit": audit,
        "check2_audit_wall_seconds": audit_wall,
        "pinned_only": pins,
        "sealed_bundle": sealed,
        "readme_editions": {
            "sealed_sha256": sealed["sealed_readme_sha256"],
            "pinned_sha256": pinned_readme,
            "different": sealed["sealed_readme_sha256"] != pinned_readme,
        },
        "author_code_executed": False,
        "status": audit["status"],
        "scope": (
            "Exact input premises and source-byte custody only, from the pinned asset and"
            " documents; no coverage is decided and no program of the source is run."
        ),
    }


# --------------------------------------------------------------------------- the sample


def source_rows(run_log: Path) -> dict[int, dict[str, Any]]:
    """The source's row at each direction, from its run log."""
    with gzip.open(run_log, "rt", encoding="utf-8") as stream:
        rows = [json.loads(line) for line in stream if line.strip()]
    return {int(row["r"]): row for row in rows if "r" in row}


def direction(binary: Path, candidate: Path, n: int, side: str, index: int) -> dict[str, Any]:
    """One direction at one thread with ``--confirm``, timed by ``wait4``."""
    argv = [str(binary.resolve()), "--candidate", str(candidate), "--n", str(n)]
    argv += ["--side", side, "--directions", str(index), "--threads", "1", "--confirm"]
    with tempfile.TemporaryFile() as stdout, tempfile.TemporaryFile() as stderr:
        start = time.monotonic()
        pid = os.posix_spawn(
            argv[0],
            argv,
            os.environ,
            file_actions=[
                (os.POSIX_SPAWN_DUP2, stdout.fileno(), 1),
                (os.POSIX_SPAWN_DUP2, stderr.fileno(), 2),
            ],
        )
        _, status, usage = os.wait4(pid, 0)
        wall = time.monotonic() - start
        stdout.seek(0)
        stderr.seek(0)
        lines = [json.loads(line) for line in stdout.read().decode().splitlines() if line]
        error_text = stderr.read().decode(errors="replace")
    row = next((line for line in lines if line.get("r") == index), {})
    summary = next(
        (line for line in lines if line.get("kind") == "sqverify-fast-summary/v1"), {}
    )
    return {
        "r": index,
        "returncode": os.waitstatus_to_exitcode(status),
        "verdict": row.get("verdict"),
        "method": row.get("method"),
        "nodes": row.get("nodes"),
        "min_certified_lower_bound": row.get("min_certified_lower_bound"),
        "thread_cpu_seconds": row.get("cpu_seconds"),
        "process_cpu_seconds": usage.ru_utime + usage.ru_stime,
        "wall_seconds": wall,
        "summary_status": summary.get("status"),
        "premises": summary.get("premises"),
        "build": summary.get("build"),
        "stderr_tail": error_text[-500:],
    }


def price(
    rows: list[dict[str, Any]], source: dict[int, float], count: int, workers: int
) -> dict[str, Any]:
    """The sample's price of a complete capture and of the whole-net controls.

    The capture is priced twice: the sample's process CPU over the source's CPU on the
    same directions, times the source's total over the net, and the sample's mean times
    the net's count. The larger stands. The controls are one more full sweep (the 99/100
    mutant at every direction, FC-1) and two runs of the costliest sampled direction
    (the original and the near-threshold mutant at the least-bound direction).
    """
    ours = sum(row["process_cpu_seconds"] for row in rows)
    theirs = sum(source[row["r"]] for row in rows) if source else None
    total_source = sum(source.values()) if source else None
    ratio = ours / theirs if theirs else None
    by_ratio = ratio * total_source if ratio is not None and total_source else None
    by_mean = ours / len(rows) * count
    capture = max(value for value in (by_ratio, by_mean) if value is not None)
    controls = capture + 2 * max(row["process_cpu_seconds"] for row in rows)
    total = capture + controls
    return {
        "sample_directions": len(rows),
        "net_directions": count,
        "sample_process_cpu_seconds": ours,
        "source_cpu_seconds_on_sample": theirs,
        "source_cpu_seconds_whole_net": total_source,
        "ratio_to_source": ratio,
        "full_capture_cpu_seconds_by_ratio": by_ratio,
        "full_capture_cpu_seconds_by_mean": by_mean,
        "full_capture_cpu_seconds": capture,
        "controls_cpu_seconds": controls,
        "total_cpu_seconds": total,
        "total_cpu_hours": total / 3600,
        "workers": workers,
        "total_wall_seconds_at_workers": total / workers,
        "limit_cpu_seconds": FULL_CAPTURE_LIMIT_CPU_SECONDS,
        "full_capture_within_limit": total <= FULL_CAPTURE_LIMIT_CPU_SECONDS,
    }


def sample(
    binary: Path,
    candidate: Path,
    *,
    n: int,
    side: str,
    indices: list[int],
    workers: int,
    run_log: Path | None,
) -> dict[str, Any]:
    """The sampled directions, their walls and the price of the rest."""
    data = load_json(candidate.read_bytes())
    _step, count, _facts, _checks = declared_net(data)
    require(all(0 <= index < count for index in indices), "a direction is off the net")
    require(1 <= workers <= 2, "at most two workers on a shared host")
    logged = source_rows(run_log) if run_log is not None else {}
    source = {r: float(row["cpu_seconds"]) for r, row in logged.items()}
    before = os.getloadavg()[0]
    start = time.monotonic()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(lambda r: direction(binary, candidate, n, side, r), indices))
    wall = time.monotonic() - start
    for row in rows:
        theirs = logged.get(row["r"], {})
        row["source_cpu_seconds"] = theirs.get("cpu_seconds")
        row["source_verdict"] = theirs.get("verdict")
        row["source_nodes"] = theirs.get("nodes")
        row["source_min_certified_lower_bound"] = theirs.get("min_certified_lower_bound")
    verified = all(row["verdict"] == "verified" and row["returncode"] == 0 for row in rows)
    agreeing = [
        row["r"]
        for row in rows
        if logged
        and row["nodes"] == row["source_nodes"]
        and row["min_certified_lower_bound"] == row["source_min_certified_lower_bound"]
    ]
    builds = {json.dumps(row["build"], sort_keys=True) for row in rows}
    return {
        "kind": "fine-net-followup-sample/v1",
        "candidate_sha256": file_digest(candidate),
        "candidate_digest": semantic_digest(data),
        "n": n,
        "L": side,
        "directions": indices,
        "rows": rows,
        "build": rows[0]["build"] if len(builds) == 1 else None,
        "binary_sha256": file_digest(binary),
        "threads_per_direction": 1,
        "workers": workers,
        "wall_seconds": wall,
        "host": {
            "cpu_count": os.cpu_count(),
            "machine": platform.machine(),
            "load_before": before,
            "load_after": os.getloadavg()[0],
        },
        "agree_with_source_log": agreeing,
        "price": price(rows, source, count, workers),
        "ran_at": utc_now(),
        "status": "DIAGNOSTIC_SAMPLE" if verified else "SAMPLE_REFUSED",
        "scope": (
            "A diagnostic sample: it decides only the directions it ran, at one thread each,"
            " and is not a replay. No control was run."
        ),
    }


def parse_directions(text: str) -> list[int]:
    """``0,296,592`` as a sorted list of distinct direction indices."""
    return sorted({int(part) for part in text.split(",")})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    first = commands.add_parser("premises", help="custody and exact premises")
    first.add_argument("--asset", type=Path, required=True)
    first.add_argument("--sha256", required=True)
    first.add_argument("--bytes", type=int, required=True)
    first.add_argument("--documents", type=Path, required=True)
    first.add_argument("--name", required=True)
    first.add_argument("--work", type=Path, required=True)
    second = commands.add_parser("sample", help="sqverify-fast at chosen directions")
    second.add_argument("--binary", type=Path, required=True)
    second.add_argument("--candidate", type=Path, required=True)
    second.add_argument("--directions", type=parse_directions, required=True)
    second.add_argument("--workers", type=int, default=1)
    second.add_argument("--source-run", type=Path)
    for command in (first, second):
        command.add_argument("--n", type=int, required=True)
        command.add_argument("--side", required=True)
        command.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "premises":
            stated = Certificate(
                args.name, args.work, args.name, args.n, Fraction(args.side), "", kind="check2"
            )
            receipt = premises(
                args.asset,
                stated,
                sha256=args.sha256,
                size=args.bytes,
                documents=args.documents,
                work=args.work,
            )
            passing = "EXACT_PREMISES_HOLD"
        else:
            receipt = sample(
                args.binary,
                args.candidate,
                n=args.n,
                side=args.side,
                indices=args.directions,
                workers=args.workers,
                run_log=args.source_run,
            )
            passing = "DIAGNOSTIC_SAMPLE"
    except AuditError as error:
        print(f"refused: {error}", file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    text = retained_json.dumps(receipt)
    args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if receipt["status"] == passing else 1


if __name__ == "__main__":
    raise SystemExit(main())
