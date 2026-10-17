"""Run Evan Daniel's own exact checkers on an import packet's certificates, with controls.

Evan Daniel's certificates (issues #375 to #664) are checked at the source by two
standard-library programs, ``search/exact/verify_cert.py`` (separating axes) and
``verify_cert2.py`` (polygon intersection). A packet under ``packing/resources/web/``
that retains them beside its ``evand-cert`` certificates can have them run here, as the
stage 4 replay's source lane (``packing/campaign/result-import.md``, "Stage 4: Validate"):

- **custody.** The packet must pass ``acquire_source --check``. Each checker and each
  input is read from the packet's retained copy and refused unless its SHA-256 is the one
  the packet's manifest pins for its upstream path, so the programs that run are the
  bytes the pinned commit holds. They were read before this module first ran them.
- **positives.** Every certificate the import declaration lists, and the regularized
  display view the source ships beside it (``<stem>_regularized.cert``) where the packet
  retains one: each must exit 0 and print the checker's own word for a valid
  certificate, ``VALID: s(n) <=`` for ``verify_cert.py`` and ``VALID:`` for
  ``verify_cert2.py`` (a ``grep VALID`` would also match ``INVALID``).
- **controls.** Each certificate mutated five ways, every one of which both checkers must
  refuse but the last, which they must accept where the side's least top or right
  clearance exceeds one unit of its denominator: the maintained kernel's two
  (``devtools.evand_arrangement_reports``), square 1 replaced by square 0 and square 0
  translated by the side plus 2, and the three sharp ones of
  ``devtools.evand_exact_certificates`` (the tightest pair overlapped by its exact gap
  plus one unit, the box shrunk past its least clearance by one unit, and by one unit
  alone).
- **runs.** Each in its own ``python -I`` child of this interpreter, at most
  ``--workers`` at a time, its CPU time read from the child's own resource usage. A
  mutant is written to a scratch directory, run, and deleted; its SHA-256 is recorded.

``check`` needs no run: it holds the committed receipt to the packet, the checkers' and
inputs' digests to the manifest, each mutant's digest to the mutant this module rebuilds
from the retained certificate, and each verdict to what it must be. The tests run it.

No geometry is decided here: the verdicts are the source's programs' own. From
``packing/``, with the project interpreter::

    python -m devtools.evand_source_checkers PACKET run [--workers 2]
    python -m devtools.evand_source_checkers PACKET check
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Callable, Sequence
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import Any, cast

from strif import atomic_output_file

from devtools import acquire_source
from devtools import evand_exact_certificates as legacy
from devtools import upper_bound_reports as reports

MODULE = "devtools.evand_source_checkers"
FORMAT = "evand-source-checkers-receipt-v1"
RECEIPT = Path("receipts/source-checkers.json")
EXACT = PurePosixPath("search/exact")
CHECKERS = ("verify_cert.py", "verify_cert2.py")
#: The last line each checker prints for a certificate it accepts.
ACCEPTS = {"verify_cert.py": "VALID: s(n) <=", "verify_cert2.py": "VALID:"}
POSITIVE = "positive"
REGULARIZED = "regularized-view"
CONTROLS = (
    "duplicate-square-overlap",
    "square-translated-outside-container",
    "tightest-pair-overlapped",
    "side-shrunk-past-clearance",
    "side-shrunk-one-unit",
)
TIMEOUT = 900
MAX_WORKERS = 2


class CheckerError(ValueError):
    """A packet, input or receipt this module refuses."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise CheckerError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest(packet: Path) -> dict[str, str]:
    """The packet's subtree manifest, upstream path to SHA-256."""
    text = (packet / acquire_source.MANIFEST).read_text(encoding="utf-8")
    rows = (line.split("  ", 1) for line in text.splitlines() if line.strip())
    return {path.removeprefix("./"): digest for digest, path in rows}


@functools.cache
def _source(packet: Path) -> Path:
    """The packet's retained source tree, after its custody check."""
    return reports.REPO / reports.acquisition(packet)["archived_path"]


def _retained(packet: Path, upstream: str) -> bytes:
    """A retained file's bytes, refused unless they are the manifest's for its path."""
    pinned = manifest(packet)
    _require(upstream in pinned, f"{upstream}: not in the packet's manifest")
    data = (_source(packet) / upstream).read_bytes()
    _require(sha256(data) == pinned[upstream], f"{upstream}: not the pinned bytes")
    return data


def inputs(packet: Path) -> list[dict[str, Any]]:
    """Each positive input: the declared certificates and their retained regularized views."""
    declaration = reports.load_declaration(packet)
    pinned = manifest(packet)
    rows: list[dict[str, Any]] = []
    for row in declaration["certificates"]:
        _require(row["format"] == "evand-cert", f"n={row['n']}: not an evand-cert row")
        rows.append({"n": row["n"], "kind": POSITIVE, "path": row["path"]})
        stem = PurePosixPath(row["path"])
        view = str(stem.with_name(f"{stem.stem}_regularized{stem.suffix}"))
        if view in pinned and (_source(packet) / view).is_file():
            rows.append({"n": row["n"], "kind": REGULARIZED, "path": view})
    return rows


def mutants(text: str, n: int) -> list[tuple[str, str, dict[str, Any]]]:
    """Each control's certificate text, its kind and how it was made."""
    certificate = legacy.parse(text, expected_n=n)
    poses = list(certificate.poses)
    made: list[tuple[str, legacy.Certificate, dict[str, Any]]] = []
    duplicate = [*poses]
    duplicate[1] = duplicate[0]
    made.append(
        (
            CONTROLS[0],
            legacy.Certificate(n, certificate.side, tuple(duplicate)),
            {"expect": "refused", "how": "square 1 replaced by square 0"},
        )
    )
    outside = [*poses]
    first = outside[0]
    outside[0] = legacy.Pose(first.x + certificate.side + 2, first.y, first.t)
    made.append(
        (
            CONTROLS[1],
            legacy.Certificate(n, certificate.side, tuple(outside)),
            {"expect": "refused", "how": "square 0 translated by the side plus 2 in x"},
        )
    )
    overlapped, about = legacy.overlap_control(certificate)
    made.append((CONTROLS[2], overlapped, {"expect": "refused", **about}))
    for shrunk, about in legacy.shrink_controls(certificate):
        made.append((str(about["control"]), shrunk, dict(about)))
    _require([kind for kind, _, _ in made] == list(CONTROLS), "the controls changed")
    return [(kind, legacy.serialize(mutant), about) for kind, mutant, about in made]


def interpreter() -> str:
    return f"{platform.python_implementation()} {platform.python_version()}"


def run_one(checker: Path, certificate: Path) -> dict[str, Any]:
    """One checker on one file, as an isolated child process, with its own CPU time."""
    command = [sys.executable, "-I", str(checker), str(certificate)]
    started = time.monotonic()
    child = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )
    timer = threading.Timer(TIMEOUT, child.kill)
    timer.start()
    try:
        assert child.stdout is not None
        output = child.stdout.read()
        child.stdout.close()
        # Reap the child here, not in Popen, so its own resource usage is read.
        _, status, usage = os.wait4(child.pid, 0)
    finally:
        timer.cancel()
    child.returncode = os.waitstatus_to_exitcode(status)
    lines = [line.strip() for line in output.strip().splitlines()]
    return {
        "exit_status": child.returncode,
        "last_line": lines[-1] if lines else "",
        "wall_seconds": round(time.monotonic() - started, 3),
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 3),
    }


def verdict(checker: str, row: dict[str, Any]) -> str:
    accepted = row["exit_status"] == 0 and str(row["last_line"]).startswith(ACCEPTS[checker])
    return "accepted" if accepted else "refused"


def run(packet: Path, workers: int) -> dict[str, Any]:
    _require(1 <= workers <= MAX_WORKERS, f"at most {MAX_WORKERS} workers")
    checkers = {name: _retained(packet, str(EXACT / name)) for name in CHECKERS}
    started_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    started = time.monotonic()
    jobs: list[tuple[dict[str, Any], str, bytes]] = []
    for item in inputs(packet):
        data = _retained(packet, item["path"])
        jobs.append(
            ({**item, "control": None, "expect": "accepted", "sha256": sha256(data)}, "", data)
        )
        if item["kind"] == POSITIVE:
            for kind, text, about in mutants(data.decode("utf-8"), item["n"]):
                encoded = text.encode("utf-8")
                row = {
                    "n": item["n"],
                    "kind": "control",
                    "path": item["path"],
                    "control": kind,
                    "expect": about.pop("expect"),
                    "made": about,
                    "sha256": sha256(encoded),
                }
                jobs.append((row, kind, encoded))
    rows: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory() as scratch:
        root = Path(scratch)
        programs = {}
        for name, data in checkers.items():
            programs[name] = root / name
            programs[name].write_bytes(data)
        tasks: list[tuple[dict[str, Any], str, Path]] = []
        for index, (row, _kind, data) in enumerate(jobs):
            path = root / f"input-{index:03d}.cert"
            path.write_bytes(data)
            tasks.extend((row, name, path) for name in CHECKERS)

        def decide(task: tuple[dict[str, Any], str, Path]) -> dict[str, Any]:
            row, name, path = task
            result = run_one(programs[name], path)
            return {
                **row,
                "checker": name,
                **result,
                "verdict": verdict(name, result),
            }

        with ThreadPoolExecutor(max_workers=workers) as pool:
            rows = list(pool.map(decide, tasks))
    cpu = sum(row["cpu_seconds"] for row in rows)
    for row in rows:
        row["as_expected"] = row["verdict"] == row["expect"]
    return {
        "format": FORMAT,
        "tool": f"python -m {MODULE} {packet.name} run --workers {workers}",
        "packet": packet.name,
        "interpreter": interpreter(),
        "isolation": (
            "python -I, one child per run, checkers and inputs copied to a scratch directory"
        ),
        "checkers": {
            name: {"path": str(EXACT / name), "sha256": sha256(data)}
            for name, data in checkers.items()
        },
        "started_utc": started_at,
        "workers": workers,
        "wall_seconds": round(time.monotonic() - started, 1),
        "cpu_seconds": round(cpu, 1),
        "all_as_expected": all(row["as_expected"] for row in rows),
        "rows": rows,
    }


def write(packet: Path, receipt: dict[str, Any]) -> None:
    path = packet / RECEIPT
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        Path(temporary).write_text(
            json.dumps(receipt, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
        )


def check(packet: Path) -> dict[str, Any]:
    """The committed receipt, held to the packet without running anything."""
    receipt = cast("dict[str, Any]", json.loads((packet / RECEIPT).read_text(encoding="utf-8")))
    _require(receipt.get("format") == FORMAT, "unknown receipt format")
    _require(receipt.get("packet") == packet.name, "the receipt names another packet")
    for name in CHECKERS:
        data = _retained(packet, str(EXACT / name))
        _require(receipt["checkers"][name]["sha256"] == sha256(data), f"{name}: digest")
    expected: list[tuple[Any, ...]] = []
    for item in inputs(packet):
        data = _retained(packet, item["path"])
        expected.append((item["n"], item["kind"], item["path"], None, "accepted", sha256(data)))
        if item["kind"] == POSITIVE:
            for kind, text, about in mutants(data.decode("utf-8"), item["n"]):
                expected.append(
                    (
                        item["n"],
                        "control",
                        item["path"],
                        kind,
                        about["expect"],
                        sha256(text.encode("utf-8")),
                    )
                )
    found = sorted(
        {
            (row["n"], row["kind"], row["path"], row["control"], row["expect"], row["sha256"])
            for row in receipt["rows"]
        },
        key=repr,
    )
    _require(
        found == sorted(set(expected), key=repr), "the receipt's inputs are not the packet's"
    )
    for row in receipt["rows"]:
        _require(row["checker"] in CHECKERS, "an unknown checker")
        _require(
            row["verdict"] == verdict(row["checker"], row),
            f"{row['path']} {row['control']}: verdict does not follow from the exit and line",
        )
        _require(
            row["verdict"] == row["expect"] and row["as_expected"],
            f"{row['checker']} on {row['path']} ({row['control'] or row['kind']}): "
            f"{row['verdict']}, not {row['expect']}",
        )
    pairs = {(row["sha256"], row["checker"]) for row in receipt["rows"]}
    _require(len(pairs) == len(receipt["rows"]), "a run is recorded twice")
    _require(len(receipt["rows"]) == len(expected) * len(CHECKERS), "a run is missing")
    _require(receipt["all_as_expected"] is True, "the receipt does not say every run passed")
    return receipt


def summary(receipt: dict[str, Any]) -> str:
    rows = receipt["rows"]
    accepted = sum(row["verdict"] == "accepted" for row in rows)
    return (
        f"{receipt['packet']}: {len(rows)} runs of {', '.join(CHECKERS)} under "
        f"{receipt['interpreter']}, {accepted} accepted and {len(rows) - accepted} refused, "
        f"each as expected; {receipt['cpu_seconds']} CPU s, {receipt['wall_seconds']} s wall"
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog=f"python -m {MODULE}", description=__doc__)
    parser.add_argument("packet")
    commands = parser.add_subparsers(dest="command", required=True)
    runner = commands.add_parser("run", help="run both checkers and write the receipt")
    runner.add_argument("--workers", type=int, default=1)
    commands.add_parser("check", help="hold the committed receipt to the packet")
    arguments = parser.parse_args(argv)
    packet = reports.packet_path(arguments.packet)
    commands_by_name: dict[str, Callable[[], dict[str, Any]]] = {
        "run": lambda: run(packet, arguments.workers),
        "check": lambda: check(packet),
    }
    try:
        receipt = commands_by_name[arguments.command]()
        if arguments.command == "run":
            write(packet, receipt)
            receipt = check(packet)
    except (CheckerError, reports.ReportError, legacy.CertificateError, OSError) as error:
        print(f"{MODULE}: {error}", file=sys.stderr)
        return 1
    print(summary(receipt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
