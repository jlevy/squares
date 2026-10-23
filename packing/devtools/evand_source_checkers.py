"""Run Evan Daniel's own exact checkers on the certificates of issues #669 and #674.

Issues #669 (n = 155) and #674 (n = 229) each report an upper bound with exact rational
certificates in ``evand/square-packing``, and the source checks them with two standalone
checkers of its own, ``search/exact/verify_cert.py`` (separating axes) and
``search/exact/verify_cert2.py`` (exact polygons), which import only ``sys`` and
``fractions``. The record's rungs rest on this repository's two exact routes, run by
``devtools.upper_bound_reports``, which are not the author's code. On 18 October 2026 a
separate replay ran the source's two checkers on the four certificates and refused every
control, but its receipt (SHA-256 ``cab73c96…``) stayed on another machine and never
reached Git, so the record could only say it awaited integration (think-8kx2,
think-0lu6). This module is that replay, kept: each packet's own retained copies of the
two checkers, unchanged, each run in its own child process on each retained certificate
and on four controls of it, with every exit status and line of output in the packet's
``receipts/source-checker-replay.json``.

Each child is ``python -I CHECKER CERTIFICATE``. Isolated mode keeps the checker's own
directory and the working directory off ``sys.path``, ignores the ``PYTHON*`` variables
and skips the user site. It does not isolate anything else, so `run_checker` also gives
the child an empty environment (none of the parent's, which in CI holds tokens), no
standard input and a scratch working directory. The checkers read only their one
argument and write only to standard output (review A6 of #747).

The certificates, by packet:

- ``evand-n155-explorer-2026-10-17`` (#669): ``s155_ex2.cert`` and the same-side display
  view ``s155_ex2_regularized.cert``;
- ``evand-n229-dilation-2026-10-17`` (#674's opening report): ``s229.cert``;
- ``evand-n229-dilation-update-2026-10-18`` (#674's update): ``s229_v2.cert``.

The controls, written to a scratch directory as certificates in the source's format, each
of which both checkers must refuse with an ``INVALID`` line rather than a crash:

- ``duplicate-square``: square 2 replaced by square 1, so two squares coincide;
- ``square-outside``: square 1 moved ``S + 2`` to the right, wholly outside the box;
- ``sharp-far-wall``: the side lowered by the least right or top wall clearance plus
  ``10^-30``, so one square crosses the wall by exactly ``10^-30``, where a checker with a
  floating-point tolerance would accept it;
- ``sharp-near-wall``: every square moved left and down by the least left or bottom wall
  clearance plus ``10^-30``, so one square crosses that wall by exactly ``10^-30``: the
  checkers' ``x - e > 0`` branches, which the far wall leaves untested (review A8 of
  #747).

A finite packing proves an upper bound and nothing more. The checkers are the author's,
so their acceptance is same-implementation evidence: it moves no rung, and the record's
confirmation still rests on the independent routes. The two checkers share their author,
their parse and their format, so they are not independent of each other either.

Subcommands, from ``packing/``, with the project interpreter::

    python -m devtools.evand_source_checkers run --scratch DIR [--workers 2]
    python -m devtools.evand_source_checkers check

``run`` holds each packet to ``acquire_source --check`` before reading it, and writes the
three receipts; it takes a few CPU-seconds. ``check`` holds each packet to its acquisition
manifest again and reads the receipts back, offline and in about a second: each covers its
packet's certificates and records every control, every certificate is accepted by both
checkers and every control refused by both. It rebuilds no control; the test suite does
(`tests/test_evand_source_checkers.py`). The receipts record each checker's,
certificate's and control's digest for a reader; whether the files changed since is Git's
to say, not a digest compared here (OR-16).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import resource
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

from strif import atomic_output_file

from devtools import acquire_source
from devtools import evand_exact_certificates as legacy
from sqpack.retained_json import dumps as retained_dumps

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
WEB = ROOT / "resources" / "web"

#: Each packet's certificates, by their path under the packet's `source/`.
PACKETS: dict[str, tuple[str, ...]] = {
    "evand-n155-explorer-2026-10-17": (
        "search/packer/candidates/s155_ex2.cert",
        "search/packer/candidates/s155_ex2_regularized.cert",
    ),
    "evand-n229-dilation-2026-10-17": ("search/packer/candidates/s229.cert",),
    "evand-n229-dilation-update-2026-10-18": ("search/packer/candidates/s229_v2.cert",),
}
#: The source's two checkers, by their path under each packet's `source/`.
CHECKERS = ("search/exact/verify_cert.py", "search/exact/verify_cert2.py")
CONTROLS = ("duplicate-square", "square-outside", "sharp-far-wall", "sharp-near-wall")
#: How far past a wall each sharp control puts its square.
SHARP = Fraction(1, 10**30)
#: What each control does, as the receipts state it.
CONTROL_TEXT = {
    "duplicate-square": "square 2 replaced by square 1",
    "square-outside": "square 1 moved S + 2 to the right",
    "sharp-far-wall": "the side lowered by the least right or top clearance plus 10^-30",
    "sharp-near-wall": "every square moved left and down by the least left or bottom "
    "clearance plus 10^-30",
}
#: The child's working directory under the scratch directory.
CHILD_CWD = "cwd"
RECEIPT = Path("receipts") / "source-checker-replay.json"
FORMAT = "evand-source-checker-replay-v1"
TOOL = "python -m devtools.evand_source_checkers run"
TIMEOUT_SECONDS = 600


def packet_dir(name: str) -> Path:
    return WEB / name


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


# -- The controls ---------------------------------------------------------------------


def half_extent(pose: legacy.Pose) -> Fraction:
    """Half the width of a unit square's axis-aligned bounding box, `(|c| + |s|)/2`."""
    c, s = pose.basis
    return (abs(c) + abs(s)) / 2


def far_wall_clearance(certificate: legacy.Certificate) -> Fraction:
    """The least clearance of any square from the right or the top wall, exactly."""
    return min(
        certificate.side - max(pose.x, pose.y) - half_extent(pose) for pose in certificate.poses
    )


def near_wall_clearance(certificate: legacy.Certificate) -> Fraction:
    """The least clearance of any square from the left or the bottom wall, exactly."""
    return min(min(pose.x, pose.y) - half_extent(pose) for pose in certificate.poses)


def wall_clearance(certificate: legacy.Certificate) -> Fraction:
    """The least clearance of any square from any wall, exactly."""
    return min(far_wall_clearance(certificate), near_wall_clearance(certificate))


def control(certificate: legacy.Certificate, name: str) -> legacy.Certificate:
    """The certificate `name` makes of `certificate`: a packing that is not one."""
    poses = list(certificate.poses)
    if name == "duplicate-square":
        poses[1] = poses[0]
        return replace(certificate, poses=tuple(poses))
    if name == "square-outside":
        first = poses[0]
        poses[0] = replace(first, x=first.x + certificate.side + 2)
        return replace(certificate, poses=tuple(poses))
    if name == "sharp-far-wall":
        lowered = certificate.side - far_wall_clearance(certificate) - SHARP
        return replace(certificate, side=lowered)
    if name == "sharp-near-wall":
        shift = near_wall_clearance(certificate) + SHARP
        moved = tuple(replace(pose, x=pose.x - shift, y=pose.y - shift) for pose in poses)
        return replace(certificate, poses=moved)
    raise ValueError(f"no control named {name!r}")


def control_text(certificate: legacy.Certificate, name: str) -> str:
    return legacy.serialize(control(certificate, name))


# -- Running the source's checkers ----------------------------------------------------


def _children_cpu() -> float:
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return usage.ru_utime + usage.ru_stime


def run_checker(script: Path, certificate: Path, *, cwd: Path) -> dict[str, Any]:
    """One run of one of the source's checkers, unchanged, in its own child process.

    ``python -I`` keeps the checker's directory and ``cwd`` off ``sys.path``, ignores the
    ``PYTHON*`` variables and skips the user site; the child also gets an empty
    environment, no standard input and ``cwd``, a scratch directory, to work in. Both paths
    must be absolute, since the child does not start where the parent is.
    """
    if not (script.is_absolute() and certificate.is_absolute()):
        raise ValueError("run_checker takes absolute paths: the child starts in cwd")
    before, started = _children_cpu(), time.monotonic()
    completed = subprocess.run(
        (sys.executable, "-I", str(script), str(certificate)),
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
        check=False,
        env={},
        stdin=subprocess.DEVNULL,
        cwd=cwd,
    )
    lines = [line.strip() for line in completed.stdout.strip().splitlines()]
    return {
        "exit_status": completed.returncode,
        "stdout": lines,
        "stderr": completed.stderr.strip()[-400:],
        "wall_seconds": round(time.monotonic() - started, 3),
        "cpu_seconds": round(_children_cpu() - before, 3),
    }


def accepted(checker: str, result: Mapping[str, Any]) -> bool:
    """Exit 0 and the checker's own word for a valid certificate on its last line.

    `verify_cert.py` ends ``VALID: s(n) <= S``; `verify_cert2.py` ends ``VALID: ...``. A
    last line that only contains ``VALID``, such as ``INVALID``, is not acceptance.
    """
    lines = result.get("stdout") or []
    last = lines[-1] if lines else ""
    word = "VALID: s(n) <= S" if checker.endswith("verify_cert.py") else "VALID:"
    return result.get("exit_status") == 0 and last.startswith(word)


def refused(result: Mapping[str, Any]) -> bool:
    """Exit 1 with an ``INVALID`` verdict line: refused on the geometry, not a crash."""
    lines = result.get("stdout") or []
    return result.get("exit_status") == 1 and any(line.startswith("INVALID") for line in lines)


def _job(job: tuple[str, str, str]) -> dict[str, Any]:
    script, certificate, cwd = job
    return run_checker(Path(script), Path(certificate), cwd=Path(cwd))


def _map(jobs: Sequence[tuple[str, str, str]], workers: int) -> list[dict[str, Any]]:
    if workers <= 1:
        return [_job(job) for job in jobs]
    with ProcessPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(_job, jobs))


def _environment() -> dict[str, str]:
    return {
        "python": platform.python_version(),
        "implementation": platform.python_implementation(),
        "machine": platform.machine(),
        "invocation": (
            "python -I CHECKER CERTIFICATE, one child process each, with an empty "
            "environment, no standard input and a scratch working directory"
        ),
    }


def _source(packet: Path) -> Mapping[str, Any]:
    record = json.loads((packet / "acquisition" / "sources.json").read_text(encoding="utf-8"))
    entry = record["sources"][0]
    return {"url": entry["source_url"], "commit": entry["source_commit"]}


def replay(name: str, scratch: Path, workers: int) -> dict[str, Any]:
    """Both checkers on each of a packet's certificates and its four controls."""
    packet = packet_dir(name)
    problems = acquire_source.check(packet, REPO)
    if problems:
        raise ValueError(f"{name}: packet custody: " + "; ".join(problems))
    source = packet / "source"
    scratch = scratch.resolve()
    cwd = scratch / name / CHILD_CWD
    cwd.mkdir(parents=True, exist_ok=True)
    jobs: list[tuple[str, str, str]] = []
    rows: list[dict[str, Any]] = []
    for path in PACKETS[name]:
        retained = source / path
        certificate = legacy.parse(retained.read_text(encoding="utf-8"))
        controls: dict[str, str] = {}
        for kind in CONTROLS:
            text = control_text(certificate, kind)
            written = scratch / name / f"{Path(path).stem}-{kind}.cert"
            written.parent.mkdir(parents=True, exist_ok=True)
            written.write_text(text, encoding="utf-8")
            controls[kind] = text_sha256(text)
        rows.append(
            {
                "certificate": path,
                "sha256": sha256(retained),
                "n": certificate.n,
                "side": legacy.literal(certificate.side),
                "controls": {kind: {"sha256": digest} for kind, digest in controls.items()},
                "runs": {},
            }
        )
        for checker in CHECKERS:
            jobs.append((str(source / checker), str(retained), str(cwd)))
            jobs.extend(
                (
                    str(source / checker),
                    str(scratch / name / f"{Path(path).stem}-{kind}.cert"),
                    str(cwd),
                )
                for kind in CONTROLS
            )
    started_utc = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    started = time.monotonic()
    results = iter(_map(jobs, workers))
    for row in rows:
        for checker in CHECKERS:
            row["runs"][checker] = {
                "positive": next(results),
                "controls": {kind: next(results) for kind in CONTROLS},
            }
    wall = time.monotonic() - started
    all_runs = [
        run
        for row in rows
        for runs in row["runs"].values()
        for run in (runs["positive"], *runs["controls"].values())
    ]
    return {
        "format": FORMAT,
        "tool": TOOL,
        "packet": name,
        "source": _source(packet),
        "checkers": {checker: sha256(source / checker) for checker in CHECKERS},
        "controls": dict(CONTROL_TEXT),
        "environment": _environment(),
        "started_utc": started_utc,
        "workers": workers,
        "invocations": len(all_runs),
        "wall_seconds": round(wall, 3),
        "cpu_seconds": round(sum(run["cpu_seconds"] for run in all_runs), 3),
        "rows": rows,
    }


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(retained_dumps(value, sort_keys=True), encoding="utf-8")


def run(scratch: Path, workers: int, names: Sequence[str] = tuple(PACKETS)) -> list[str]:
    """Replay every packet and write its receipt; return what the receipts get wrong."""
    for name in names:
        _write(packet_dir(name) / RECEIPT, replay(name, scratch, workers))
    return check(names)


# -- Reading the receipts back --------------------------------------------------------


def receipt_problems(name: str, receipt: Mapping[str, Any]) -> list[str]:
    """What a packet's receipt gets wrong: its rows, and an outcome other than the one owed.

    The receipt is committed with the files it ran on, so Git, not a digest compared here,
    says whether they have changed since (OR-16); the digests it records are for a reader.
    """
    where = f"{name}: {RECEIPT}"
    problems: list[str] = []
    if receipt.get("format") != FORMAT or receipt.get("packet") != name:
        problems.append(f"{where} is not this packet's {FORMAT} receipt")
    if sorted(receipt.get("checkers") or ()) != sorted(CHECKERS):
        problems.append(f"{where} does not name the source's two checkers")
    rows = receipt.get("rows") or []
    if [row.get("certificate") for row in rows] != list(PACKETS[name]):
        problems.append(f"{where} does not cover exactly {', '.join(PACKETS[name])}")
        return problems
    for row in rows:
        problems.extend(_row_problems(where, row))
    return problems


def _row_problems(where: str, row: Mapping[str, Any]) -> list[str]:
    """What one row gets wrong, each as a problem line: a malformed row is reported, not
    raised (review A7 of #747)."""
    path = str(row.get("certificate"))
    problems = [
        f"{where}: {path} records no {kind} control"
        for kind in CONTROLS
        if kind not in (row.get("controls") or {})
    ]
    all_runs = row.get("runs")
    if not isinstance(all_runs, Mapping) or not all_runs:
        return [*problems, f"{where}: {path} records no runs"]
    for checker in CHECKERS:
        runs = all_runs.get(checker)
        if not isinstance(runs, Mapping):
            problems.append(f"{where}: {checker} did not run on {path}")
            continue
        positive = runs.get("positive")
        if not isinstance(positive, Mapping):
            problems.append(f"{where}: {checker} records no positive run on {path}")
        elif not accepted(checker, positive):
            problems.append(f"{where}: {checker} did not accept {path}")
        controls = runs.get("controls") or {}
        problems.extend(
            f"{where}: {checker} did not refuse {path}'s {kind} control"
            for kind in CONTROLS
            if not refused(controls.get(kind, {"exit_status": 0, "stdout": []}))
        )
    return problems


def check(names: Sequence[str] = tuple(PACKETS)) -> list[str]:
    """Each packet held to its acquisition manifest, and each receipt read back."""
    problems: list[str] = []
    for name in names:
        problems.extend(
            f"{name}: packet custody: {problem}"
            for problem in acquire_source.check(packet_dir(name), REPO)
        )
        path = packet_dir(name) / RECEIPT
        if not path.is_file():
            problems.append(f"{name}: {RECEIPT} is missing")
            continue
        problems.extend(receipt_problems(name, json.loads(path.read_text(encoding="utf-8"))))
    return problems


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n", 1)[0])
    commands = parser.add_subparsers(dest="command", required=True)
    replaying = commands.add_parser("run", help="run both checkers; write the receipts")
    replaying.add_argument("--scratch", type=Path, required=True)
    replaying.add_argument("--workers", type=int, default=1)
    commands.add_parser("check", help="read the receipts back against the packets")
    args = parser.parse_args(argv)
    action: Callable[[], list[str]] = (
        (lambda: run(args.scratch, args.workers)) if args.command == "run" else check
    )
    problems = action()
    for problem in problems:
        print(problem, file=sys.stderr)
    if not problems:
        print(f"source checker replay: {len(PACKETS)} packets, every receipt holds")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
