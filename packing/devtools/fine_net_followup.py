"""Check a reported wand125 certificate kept outside Git, and price its replay.

wand125's fine-net certificates of jlevy/squares#446 and its follow-ups are retained as
authored facts and hash references (`resources/web/wand125-fine-net-*`): the release
asset that holds the candidate, its logs and the adapted verifier's source stays outside
live Git, since the nested verifier carries no licence of its own. This tool reads a
local copy of that asset beside the certificate's documents from the pinned tree, and
writes the receipts a packet keeps. Its check2 commands run no program of the source.

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
  directory, member by member, and records both README editions and whether the
  pre-publication receipt is the run record the check2 receipt embeds. A refusal by the
  check2 reader, a field it reads that a receipt of another shape lacks included, is
  recorded as ``CHECK2_READER_REFUSED`` with its message, and the custody checks still
  run. It decides no coverage.
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

A linear certificate of points, segments and rectangles on the 201-angle net (T-080's
kind) whose release asset is likewise kept outside Git is read by the T-080 route's own
functions, `devtools.audit_wand125_linear`, given the files and their digests instead of
a packet's retained copies:

- ``linear-premises`` unpacks the pinned asset beside the pinned documents and runs
  `linear_certificate`, `bundle_bindings` and `check_inputs` at all 201 angles. It runs
  no program of the source and decides no coverage.
- ``linear-sample`` replays chosen angles as ``linear-replay`` does, with the source's
  replay function and unchanged checker from this repository's retained, reviewed copies
  (never the asset's ``code/``), and prices the complete replay and the route's control
  from the source's per-angle seconds. It is a diagnostic of the angles it ran.

From ``packing/``::

    .venv/bin/python3 -m devtools.fine_net_followup premises \\
        --asset ASSET.tar.gz --sha256 HEX --bytes N --documents CERT_DIR \\
        --name mixed_n29_L582 --n 29 --side 291/50 --work WORK --out RECEIPT
    .venv/bin/python3 -m devtools.fine_net_followup sample \\
        --binary sqverify_fast/target/release/sqverify-fast \\
        --candidate WORK/certificates/mixed_n29_L582/candidate.json --n 29 --side 291/50 \\
        --directions 0,296,592 --workers 2 --source-run WORK/.../check2/run.jsonl.gz \\
        --out RECEIPT
    .venv/bin/python3 -m devtools.fine_net_followup linear-premises \\
        --asset ASSET.tar.gz --sha256 HEX --bytes N --documents CERT_DIR \\
        --name mixed_n122_L1126 --n 122 --side 563/50 --orbits 502,1268,3 \\
        --candidate-digest HEX --bundle n122-L11.26-proof-bundle.tar.gz \\
        --work WORK --out RECEIPT
    .venv/bin/python3 -m devtools.fine_net_followup linear-sample ... \\
        --directions 37,108 --workers 2 --out RECEIPT
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
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from fractions import Fraction
from pathlib import Path, PurePosixPath
from typing import Any

from devtools import audit_wand125_linear as linear
from devtools import audit_wand125_point_and_mixed as mixed
from devtools.audit_wand125_declared_net import (
    PREPUBLICATION,
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
from devtools.audit_wand125_linear import (
    _replay_direction,  # pyright: ignore[reportPrivateUsage]
)
from devtools.audit_wand125_point_and_mixed import (
    _passes,  # pyright: ignore[reportPrivateUsage]
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
#: What the check2 reader raises when it refuses: its own refusal, or a field it reads
#: that a receipt of another shape lacks. Either is recorded as a refusal, never passed.
READER_REFUSALS = (AuditError, KeyError, TypeError, ValueError)
CHECK2_READER_REFUSED = "CHECK2_READER_REFUSED"
#: The suffix of the proof bundle a linear certificate directory ships.
PROOF_BUNDLE_SUFFIX = "-proof-bundle.tar.gz"
#: The linear control: the original and two mutations at one oblique direction, each run
#: to at most the stored node count (`devtools.audit_wand125_linear.linear_control`).
LINEAR_CONTROL_RUNS = 3


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


def prepublication(directory: Path) -> dict[str, Any] | None:
    """The source's pre-publication receipt beside the run its check2 receipt records.

    The check2 reader takes the pre-publication receipt as a second run on the published
    bytes. Its shape is named here, and whether it is the very run record
    ``check2/receipt.json`` embeds under ``receipt``, with both runs' seconds, so that a
    packet can say when the two receipts are one run.
    """
    path = directory / PREPUBLICATION
    if not path.is_file():
        return None
    second = load_json(path.read_bytes())
    receipt = load_json((directory / "check2/receipt.json").read_bytes())
    embedded = receipt.get("receipt")
    shape = second.get("schema") or ("build" if "build" in second else "unnamed")
    return {
        "sha256": file_digest(path),
        "shape": shape,
        "seconds": second.get("seconds"),
        "check2_wall_seconds": receipt.get("verifier_summary", {}).get("wall_seconds"),
        "check2_embeds_a_run_record": embedded is not None,
        "identical_to_the_embedded_run_record": embedded == second,
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
    try:
        audit = audit_check2(view, stated, pins=pins)
    except READER_REFUSALS as error:
        audit = {"status": CHECK2_READER_REFUSED, "refusal": f"{type(error).__name__}: {error}"}
    audit_wall = time.perf_counter() - start
    listed = load_json((directory / "files-sha256.json").read_bytes())
    sealed = sealed_bundle(directory, listed, asset_files)
    pinned_readme = file_digest(directory / "README.md")
    side = stated.side
    return {
        "kind": "fine-net-followup-premises/v1",
        "certificate": stated.name,
        "claim": f"s({stated.n}) >= {side.numerator}/{side.denominator}",
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
        "prepublication": prepublication(directory),
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


# --------------------------------------------------------------------------- linear


def linear_stated(
    name: str,
    n: int,
    side: Fraction,
    *,
    orbits: tuple[int, int, int],
    digest: str,
    tarball: str,
) -> linear.LinearCertificate:
    """A linear certificate as the source states it: count, side, point, segment and
    rectangle orbits, candidate digest and proof bundle.

    Its packet and revision are only named: the maintained readers, given the files and
    their digests (`linear_prepare`), read neither.
    """
    points, segments, rectangles = orbits
    return linear.LinearCertificate(
        name=name,
        packet=mixed.WEB,
        revision="",
        directory=Path("certificates", name),
        n=n,
        side=side,
        rectangles=rectangles,
        candidate_digest=digest,
        tarball=tarball,
        source_audit=True,
        points=points,
        segments=segments,
    )


def linear_prepare(
    asset: Path, *, sha256: str, size: int, documents: Path, name: str, work: Path
) -> tuple[Path, list[str], list[str], dict[Path, str], str]:
    """The pinned asset unpacked with the pinned documents laid beside it.

    Returns the certificate directory, the asset's files, the documents' files, every
    file's SHA-256 by its upstream path (the tree the maintained readers take) and the
    name of the one proof bundle the directory ships.
    """
    directory = unpack_asset(asset, sha256, size, name, work)
    asset_files = sorted(
        p.relative_to(directory).as_posix() for p in directory.rglob("*") if p.is_file()
    )
    laid = lay_documents(documents, directory)
    tree = {
        Path("certificates", name, p.relative_to(directory)): file_digest(p)
        for p in sorted(directory.rglob("*"))
        if p.is_file()
    }
    bundles = sorted(directory.glob(f"*{PROOF_BUNDLE_SUFFIX}"))
    require(len(bundles) == 1, f"{len(bundles)} proof bundles in {directory}")
    return directory, asset_files, laid, tree, bundles[0].name


def linear_premises(
    asset: Path,
    stated: linear.LinearCertificate,
    *,
    sha256: str,
    size: int,
    documents: Path,
    work: Path,
) -> dict[str, Any]:
    """Every exact premise of a linear certificate, by the T-080 route's readers.

    `devtools.audit_wand125_linear.linear_certificate` reads the measure, its D4
    invariance, digest, net, centre domains, checker and code identity, 201 records and
    the source's audit; `bundle_bindings` holds the proof bundle's 810 files to them; and
    `check_inputs` binds every angle's input to the exact candidate. None of them imports
    or runs a program of the source, and none decides coverage.
    """
    directory, asset_files, laid, tree, tarball = linear_prepare(
        asset,
        sha256=sha256,
        size=size,
        documents=documents,
        name=stated.directory.name,
        work=work,
    )
    require(tarball == stated.tarball, f"the directory ships {tarball}, not {stated.tarball}")
    files = {name: (directory / name).read_bytes() for name in mixed.MIXED_FILES}
    start = time.perf_counter()
    audit = linear.linear_certificate(stated, files, tree)
    audit_wall = time.perf_counter() - start
    bundle = mixed.unpack_bundle(stated, directory / tarball, work / "unpacked")
    bindings = linear.bundle_bindings(stated, bundle, tree)
    shipped = load_json(files["certificate.json"])["results"]
    start = time.perf_counter()
    inputs = linear.check_inputs(
        bundle, tree[stated.directory / "candidate.json"], range(linear.LAST + 1), shipped
    )
    inputs_wall = time.perf_counter() - start
    return {
        "kind": "fine-net-followup-linear-premises/v1",
        "certificate": stated.directory.name,
        "claim": f"s({stated.n}) >= {stated.side.numerator}/{stated.side.denominator}",
        "asset": {"sha256": sha256, "bytes": size, "files": inventory(directory, asset_files)},
        "documents": inventory(directory, laid),
        "linear_certificate": audit,
        "linear_certificate_wall_seconds": audit_wall,
        "bundle": {
            "name": tarball,
            "sha256": tree[stated.upstream_tarball],
            "bytes": (directory / tarball).stat().st_size,
            **bindings,
        },
        "inputs": inputs,
        "inputs_wall_seconds": inputs_wall,
        "entrypoints": [
            "audit_wand125_linear.linear_certificate",
            "audit_wand125_point_and_mixed.unpack_bundle",
            "audit_wand125_linear.bundle_bindings",
            "audit_wand125_linear.check_inputs",
        ],
        "author_code_executed": False,
        "status": "EXACT_PREMISES_HOLD",
        "scope": (
            "Exact premises and source-byte custody only, from the pinned asset and"
            " documents, by the readers of the T-080 route; no coverage is decided and no"
            " program of the source is run."
        ),
    }


def linear_price(
    rows: list[dict[str, Any]], seconds: dict[int, float], nodes: dict[int, int], workers: int
) -> dict[str, Any]:
    """The sample's price of a complete replay and of the T-080 route's control.

    The replay is priced twice: this host's CPU over the source's seconds on the same
    angles, times the source's total, and this host's CPU per node times the certificate's
    nodes. The larger stands. The control is `LINEAR_CONTROL_RUNS` runs of the oblique
    angle with the fewest nodes, at the ratio. No complete replay is shorter in wall than
    its costliest angle, which bounds the wall from below.
    """
    ours = sum(row["cpu_seconds"] for row in rows)
    theirs = sum(seconds[row["index"]] for row in rows)
    ratio = ours / theirs
    by_ratio = ratio * sum(seconds.values())
    by_nodes = ours / sum(nodes[row["index"]] for row in rows) * sum(nodes.values())
    replay = max(by_ratio, by_nodes)
    oblique = min((index for index in nodes if index), key=lambda index: (nodes[index], index))
    control = LINEAR_CONTROL_RUNS * ratio * seconds[oblique]
    total = replay + control
    longest = max(seconds, key=lambda index: seconds[index])
    return {
        "sample_angles": len(rows),
        "net_angles": len(seconds),
        "sample_cpu_seconds": ours,
        "source_seconds_on_sample": theirs,
        "source_seconds_whole_net": sum(seconds.values()),
        "ratio_to_source": ratio,
        "full_replay_cpu_seconds_by_ratio": by_ratio,
        "full_replay_cpu_seconds_by_nodes": by_nodes,
        "full_replay_cpu_seconds": replay,
        "control_angle": oblique,
        "control_cpu_seconds": control,
        "total_cpu_seconds": total,
        "total_cpu_hours": total / 3600,
        "costliest_angle": longest,
        "costliest_angle_cpu_seconds": ratio * seconds[longest],
        "workers": workers,
        "total_wall_seconds_at_workers": max(total / workers, ratio * seconds[longest]),
        "limit_cpu_seconds": FULL_CAPTURE_LIMIT_CPU_SECONDS,
        "full_replay_within_limit": total <= FULL_CAPTURE_LIMIT_CPU_SECONDS,
    }


def linear_sample(
    asset: Path,
    stated: linear.LinearCertificate,
    *,
    sha256: str,
    size: int,
    documents: Path,
    work: Path,
    indices: list[int],
    workers: int,
) -> dict[str, Any]:
    """Chosen angles replayed by the T-080 route, and the price of the rest.

    As `devtools.audit_wand125_linear.linear_replay` does for a registered certificate:
    the pinned asset unpacked afresh, the proof bundle bound to it, the shipped ``code/``
    assembled from this repository's retained copies (never the asset's), the driver's
    preconditions, each sampled input bound to the candidate, the checker built by the
    shipped ``compile_verifier``, and each angle replayed by the shipped ``replay_angle``
    in a pool of at most ``workers`` processes, each timed by its own and its children's
    CPU. An angle passes when it returns the certificate's own record. A sample decides
    only the angles it ran.
    """
    require(1 <= workers <= 2, "at most two workers on a shared host")
    require(all(0 <= index <= linear.LAST for index in indices), "an angle is off the net")
    runtime = mixed.replay_runtime()
    directory, _, _, tree, tarball = linear_prepare(
        asset,
        sha256=sha256,
        size=size,
        documents=documents,
        name=stated.directory.name,
        work=work,
    )
    require(tarball == stated.tarball, f"the directory ships {tarball}, not {stated.tarball}")
    bundle = mixed.unpack_bundle(stated, directory / tarball, work / "unpacked")
    bindings = linear.bundle_bindings(stated, bundle, tree)
    code = linear.assemble_code(stated, work / "code", tree)
    driver = linear.driver_preconditions(bundle, code)
    require(driver.digest == stated.candidate_digest, "the bundle's candidate differs")
    shipped = load_json((directory / "certificate.json").read_bytes())["results"]
    inputs = linear.check_inputs(
        driver.root, tree[stated.directory / "candidate.json"], indices, shipped
    )
    binary = work / "replay-verify"
    driver.verifier.compile_verifier(binary)
    summary = load_json((bundle / "summary.json").read_bytes())["records"]
    seconds = {int(index): float(record["seconds"]) for index, record in summary.items()}
    nodes = {int(index): int(record["nodes"]) for index, record in shipped.items()}
    before = os.getloadavg()[0]
    start = time.monotonic()
    jobs = [(driver.code, str(driver.root), index, str(binary)) for index in indices]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(_replay_direction, jobs))
    wall = time.monotonic() - start
    for row in rows:
        row["passes"] = _passes(row, shipped)
        row["source_seconds"] = seconds[row["index"]]
        row["nodes"] = nodes[row["index"]]
    passing = all(row["passes"] for row in rows)
    return {
        "kind": "fine-net-followup-linear-sample/v1",
        "certificate": stated.directory.name,
        "candidate_digest": driver.digest,
        "angles": indices,
        "rows": rows,
        "bindings": bindings,
        "preconditions": driver.facts(),
        "inputs": {key: inputs[key] for key in ("status", "inputs", "images")},
        "binary_sha256": file_digest(binary),
        "compile": "the shipped compile_verifier",
        "environment": runtime,
        "host": mixed.host_facts() | {"load_before": before, "load_after": os.getloadavg()[0]},
        "workers": workers,
        "wall_seconds": wall,
        "price": linear_price(rows, seconds, nodes, workers),
        "ran_at": utc_now(),
        "status": "DIAGNOSTIC_SAMPLE" if passing else "SAMPLE_REFUSED",
        "scope": (
            "A diagnostic sample: the source's replay function and unchanged checker, from"
            " this repository's retained copies, at the angles it ran; it decides only"
            " those angles and is not a replay. No control was run."
        ),
    }


def parse_orbits(text: str) -> tuple[int, int, int]:
    """``502,1268,3`` as the point, segment and rectangle orbit counts."""
    points, segments, rectangles = (int(part) for part in text.split(","))
    return points, segments, rectangles


def parse_directions(text: str) -> list[int]:
    """``0,296,592`` as a sorted list of distinct direction indices."""
    return sorted({int(part) for part in text.split(",")})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    commands = parser.add_subparsers(dest="command", required=True)
    first = commands.add_parser("premises", help="custody and exact premises")
    second = commands.add_parser("sample", help="sqverify-fast at chosen directions")
    third = commands.add_parser("linear-premises", help="a linear certificate's premises")
    fourth = commands.add_parser("linear-sample", help="a linear certificate's angles")
    for command in (first, third, fourth):
        command.add_argument("--asset", type=Path, required=True)
        command.add_argument("--sha256", required=True)
        command.add_argument("--bytes", type=int, required=True)
        command.add_argument("--documents", type=Path, required=True)
        command.add_argument("--name", required=True)
        command.add_argument("--work", type=Path, required=True)
    for command in (third, fourth):
        command.add_argument("--orbits", type=parse_orbits, required=True)
        command.add_argument("--candidate-digest", required=True)
        command.add_argument("--bundle", required=True)
    second.add_argument("--binary", type=Path, required=True)
    second.add_argument("--candidate", type=Path, required=True)
    second.add_argument("--source-run", type=Path)
    for command in (second, fourth):
        command.add_argument("--directions", type=parse_directions, required=True)
        command.add_argument("--workers", type=int, default=1)
    for command in (first, second, third, fourth):
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
        elif args.command == "sample":
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
        else:
            stated = linear_stated(
                args.name,
                args.n,
                Fraction(args.side),
                orbits=args.orbits,
                digest=args.candidate_digest,
                tarball=args.bundle,
            )
            common = {
                "sha256": args.sha256,
                "size": args.bytes,
                "documents": args.documents,
                "work": args.work,
            }
            if args.command == "linear-premises":
                receipt = linear_premises(args.asset, stated, **common)
                passing = "EXACT_PREMISES_HOLD"
            else:
                receipt = linear_sample(
                    args.asset,
                    stated,
                    **common,
                    indices=args.directions,
                    workers=args.workers,
                )
                passing = "DIAGNOSTIC_SAMPLE"
    except (AuditError, ValueError) as error:
        print(f"refused: {error}", file=sys.stderr)
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    text = retained_json.dumps(receipt)
    args.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if receipt["status"] == passing else 1


if __name__ == "__main__":
    raise SystemExit(main())
