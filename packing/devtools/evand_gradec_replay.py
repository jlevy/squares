"""Replay Evan Daniel's gradec.py on the 233 grade-C configurations, with controls.

T-261 records Daniel's report that 233 configurations of field degree at most 4 are local
minima of the side, by Theorem C of ``grade-C.md``, as ``gradec.py`` checks it.  His
release ``exact-data-2026-10-12`` publishes ``gradec-233.tar.zst``: for each count, the
contacts file the checker read and the certificate it wrote, with the run logs.  The
``evand-exact-data-2026-10-12`` packet retains that archive and the 233 exact forms
``n-N.minpoly.json.gz``; the ``evand-exact-and-local-reports-2026-10-12`` packet retains
``gradec.py`` and the three modules it imports, at ``ad86d42``.

This module is the **same-implementation** route of ``result-import.md`` stage 4 (bead
``think-mtah``): it runs the author's checker, unchanged, on every count the archive
certifies, 230 and 261 with ``GRADEC_DROPZERO=1`` as the release ran them, and compares
each certificate it writes with the published one, byte for byte.  It proves nothing
gradec.py does not; what it adds is a reproduction from the retained bytes on another
machine, a comparison of every run log with the release's (paths and timings aside), and
the three rejection tests the source builds in (``GRADEC_MUTATE=tight``, ``droprow`` and
``neghess``), each of which must make the checker refuse n = 10.

Each run copies its two inputs to a fresh directory, outside the repository, and runs
``gradec.py`` from a fresh copy of the four modules under the given interpreter (a separate
virtual environment with ``env.sh``'s pinned packages), with ``-E -s``, an empty working
directory and the input path as its argument.  Isolated mode's ``-P`` is left out because
gradec.py imports its three modules from its own directory, the copy, which holds nothing
else.  Nothing here imports from the source.

The work is resumable: each finished run appends one line to ``WORK/runs.jsonl``, and a
later invocation with the same ``--work`` skips every run recorded there.  Runs are
started longest first, by the build time the release's log prints, and no run starts once
the recorded CPU time reaches ``--cpu-cap-hours``.  The receipt written to ``--out`` holds
the environment and every run's record; its ``complete`` says whether all ran.

Run it from ``packing/``::

    nice -n 10 uv run --frozen --all-extras --group dev python -m devtools.evand_gradec_replay \
        --python VENV/bin/python --work SCRATCH --jobs 2 \
        --out resources/web/evand-exact-data-2026-10-12/receipts/gradec-replay-233.json
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import re
import shutil
import subprocess
import tarfile
import threading
import time
from collections.abc import Iterable, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
DATA_PACKET = ROOT / "resources/web/evand-exact-data-2026-10-12"
ARCHIVE = DATA_PACKET / "acquisition/release/gradec-233.tar.zst"
MINPOLY_DIR = DATA_PACKET / "source/search/exact/minpoly/data"
COUNTS_FILE = DATA_PACKET / "review/counts.txt"
SCRIPTS_DIR = (
    ROOT / "resources/web/evand-exact-and-local-reports-2026-10-12/source/search/exact"
)
MODULES = ("gradec.py", "localmin.py", "verify_exact.py", "geom.py")
UPSTREAM_REVISION = "ad86d42d0f743076d735036702ba04a41ce24a8c"
MEMBER_PREFIX = "gradec-233/"

#: The two counts the release certifies only after dropping zero-force rows.
DROPZERO = frozenset({230, 261})

#: The source's own rejection tests, each run at this count, where it must refuse.
CONTROL_COUNT = 10
CONTROLS = ("tight", "droprow", "neghess")

#: Per-run limit: about six times the release's longest run (313, 1,741 s).
DEFAULT_TIMEOUT = 3 * 3600
DEFAULT_CPU_CAP_HOURS = 40.0
TAIL_LINES = 3

_TIME = re.compile(r"\((\d+(?:\.\d+)?) s\)")
_VALID_LINE = "=> grade C certificate VALID"


@dataclass(frozen=True)
class Run:
    """One gradec.py run: a replay of count ``n``, or a rejection test at it."""

    n: int
    control: str | None = None

    @property
    def key(self) -> str:
        return f"control-{self.control}-n-{self.n}" if self.control else f"n-{self.n}"

    @property
    def env(self) -> dict[str, str]:
        env = {"GRADEC_DROPZERO": "1"} if self.n in DROPZERO and not self.control else {}
        if self.control:
            env["GRADEC_MUTATE"] = self.control
        return env


@dataclass
class Release:
    """What the archive publishes, per count: the input, the certificate and the log."""

    contacts: dict[int, bytes]
    certificates: dict[int, bytes]
    logs: dict[int, str]


def read_counts(path: Path = COUNTS_FILE) -> list[int]:
    return [int(token) for token in path.read_text().split()]


def read_release(counts: Iterable[int], archive: Path = ARCHIVE) -> Release:
    """Read each count's contacts file, certificate and log from the archive, in memory.

    The log is the one whose run wrote the published certificate: ``n-N.dropzero.log``
    for the two counts run with ``GRADEC_DROPZERO=1``, ``n-N.log`` otherwise.
    """
    wanted = set(counts)
    contacts: dict[int, bytes] = {}
    certificates: dict[int, bytes] = {}
    logs: dict[int, str] = {}
    with tarfile.open(archive, "r:zst") as tar:
        for member in tar.getmembers():
            name = member.name.removeprefix(MEMBER_PREFIX)
            match = re.fullmatch(
                r"(certs|logs)/n-(\d+)\.(contacts\.json|gradec\.json|log|dropzero\.log)", name
            )
            if not match or int(match[2]) not in wanted:
                continue
            n, suffix = int(match[2]), match[3]
            handle = tar.extractfile(member)
            if handle is None:
                continue
            data = handle.read()
            if suffix == "contacts.json":
                contacts[n] = data
            elif suffix == "gradec.json":
                certificates[n] = data
            elif suffix == ("dropzero.log" if n in DROPZERO else "log"):
                logs[n] = data.decode()
    missing = sorted(wanted - (contacts.keys() & certificates.keys() & logs.keys()))
    if missing:
        raise SystemExit(f"the archive lacks inputs, certificates or logs at {missing}")
    return Release(contacts, certificates, logs)


def release_seconds(log: str) -> float | None:
    """The build time the release's VALID line prints, or None."""
    for line in log.splitlines():
        if _VALID_LINE in line and (found := _TIME.findall(line)):
            return float(found[-1])
    return None


def normalized_log(text: str, base: str, n: int) -> list[str]:
    """A log's lines with the input path written as ``n-N`` and every time as ``T``."""
    return [
        _TIME.sub("(T s)", line.replace(base, f"n-{n}")).rstrip()
        for line in text.splitlines()
        if line.strip()
    ]


def schedule(counts: Sequence[int], release: Release) -> list[Run]:
    """The controls first, then every replay, longest release build time first."""
    replays = sorted(
        (Run(n) for n in counts),
        key=lambda run: (-(release_seconds(release.logs[run.n]) or 0.0), run.n),
    )
    controls = [Run(CONTROL_COUNT, c) for c in CONTROLS] if CONTROL_COUNT in counts else []
    return controls + replays


def copy_modules(destination: Path, source: Path = SCRIPTS_DIR) -> None:
    """Copy the retained modules out; Git holds them, so they are copied, not compared."""
    if destination.exists():
        for name in MODULES:
            if (destination / name).read_bytes() != (source / name).read_bytes():
                raise SystemExit(f"{destination / name} differs from the retained copy")
        return
    destination.mkdir(parents=True)
    for name in MODULES:
        shutil.copyfile(source / name, destination / name)


def interpreter_versions(python: str) -> dict[str, str]:
    probe = (
        "import json, sys, numpy, scipy, mpmath, sympy, flint; print(json.dumps({"
        "'python': sys.version.split()[0], 'numpy': numpy.__version__, "
        "'scipy': scipy.__version__, 'mpmath': mpmath.__version__, "
        "'sympy': sympy.__version__, 'python-flint': flint.__version__}))"
    )
    result = subprocess.run(
        [python, "-I", "-c", probe], capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)


def differing_keys(output: bytes, published: bytes) -> list[str]:
    """The top-level certificate fields whose values differ, for a run that is not identical."""
    try:
        ours, theirs = json.loads(output), json.loads(published)
    except ValueError:
        return ["<unparsable>"]
    keys = sorted(set(ours) | set(theirs))
    return [key for key in keys if ours.get(key) != theirs.get(key)]


def execute(
    run: Run,
    *,
    python: str,
    modules: Path,
    work: Path,
    release: Release,
    timeout: float,
    minpoly_dir: Path = MINPOLY_DIR,
) -> dict[str, Any]:
    """Run gradec.py once in a fresh directory and judge what it wrote."""
    directory = work / "runs" / run.key
    if directory.exists():
        shutil.rmtree(directory)
    cwd = directory / "cwd"
    cwd.mkdir(parents=True)
    base = directory / f"n-{run.n}"
    with gzip.open(minpoly_dir / f"n-{run.n}.minpoly.json.gz", "rb") as handle:
        Path(f"{base}.minpoly.json").write_bytes(handle.read())
    Path(f"{base}.contacts.json").write_bytes(release.contacts[run.n])
    env = {
        "PATH": "/usr/bin:/bin",
        "HOME": str(cwd),
        "OPENBLAS_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
        **run.env,
    }
    log_path = directory / f"n-{run.n}.log"
    started = datetime.now(UTC)
    wall = time.monotonic()
    with log_path.open("w") as log:
        process = subprocess.Popen(
            [python, "-E", "-s", str(modules / "gradec.py"), str(base)],
            cwd=cwd,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
        )
        timer = threading.Timer(timeout, process.kill)
        timer.start()
        try:
            _, status, usage = os.wait4(process.pid, 0)
        finally:
            timer.cancel()
        process.returncode = os.waitstatus_to_exitcode(status)
    wall_seconds = time.monotonic() - wall
    timed_out = wall_seconds >= timeout and process.returncode != 0
    text = log_path.read_text(errors="replace")
    lines = [line for line in text.splitlines() if line.strip()]
    output_path = Path(f"{base}.gradec.json")
    output = output_path.read_bytes() if output_path.exists() else None
    record: dict[str, Any] = {
        "key": run.key,
        "n": run.n,
        "control": run.control,
        "env": run.env,
        "started_utc": started.isoformat(timespec="seconds"),
        "wall_seconds": round(wall_seconds, 1),
        "cpu_seconds": round(usage.ru_utime + usage.ru_stime, 1),
        "max_rss_mb": round(usage.ru_maxrss / 1024, 1),
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "last_lines": [line.replace(str(directory), "WORK") for line in lines[-TAIL_LINES:]],
    }
    if run.control:
        refused = (
            process.returncode != 0
            and output is None
            and "AssertionError" in text
            and not timed_out
        )
        record["refused"] = refused
        record["passed"] = refused
        return record
    published = release.certificates[run.n]
    identical = output == published
    record["output_bytes"] = None if output is None else len(output)
    record["valid"] = None if output is None else bool(json.loads(output).get("valid"))
    record["identical_to_published"] = identical
    if output is not None and not identical:
        record["differing_keys"] = differing_keys(output, published)
    ours = normalized_log(text, str(base), run.n)
    theirs = normalized_log(release.logs[run.n], f"minpoly/solve/n-{run.n}", run.n)
    record["log_matches_release"] = ours == theirs
    record["release_build_seconds"] = release_seconds(release.logs[run.n])
    record["passed"] = process.returncode == 0 and identical and bool(record["valid"])
    return record


def load_records(path: Path) -> dict[str, dict[str, Any]]:
    """The runs a previous invocation finished, by key; a torn last line is ignored."""
    records: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return records
    for line in path.read_text().splitlines():
        try:
            record = json.loads(line)
        except ValueError:
            continue
        records[record["key"]] = record
    return records


def summarize(
    runs: Sequence[Run],
    records: Mapping[str, Mapping[str, Any]],
    header: Mapping[str, Any],
) -> dict[str, Any]:
    """The receipt: the header, the totals and every run's record, controls first."""
    ordered = [records[run.key] for run in runs if run.key in records]
    controls = [record for record in ordered if record["control"]]
    replays = sorted((r for r in ordered if not r["control"]), key=lambda r: r["n"])
    expected = sum(1 for run in runs if not run.control)
    starts = [record["started_utc"] for record in ordered]
    return {
        **header,
        "complete": len(ordered) == len(runs),
        "summary": {
            "replays_expected": expected,
            "replays_run": len(replays),
            "valid": sum(1 for r in replays if r.get("valid")),
            "identical_to_published": sum(
                1 for r in replays if r.get("identical_to_published")
            ),
            "logs_match_release": sum(1 for r in replays if r.get("log_matches_release")),
            "timed_out": sorted(r["n"] for r in replays if r.get("timed_out")),
            "failed": sorted(r["n"] for r in replays if not r["passed"]),
            "controls_refused": sum(1 for r in controls if r["passed"]),
            "controls_run": len(controls),
            "cpu_seconds_total": round(sum(float(r["cpu_seconds"]) for r in ordered), 1),
            "cpu_seconds_replays": round(sum(float(r["cpu_seconds"]) for r in replays), 1),
            "release_build_seconds_total": round(
                sum(float(r.get("release_build_seconds") or 0.0) for r in replays), 1
            ),
            "first_run_started_utc": min(starts) if starts else None,
            "all_passed": len(ordered) == len(runs) and all(r["passed"] for r in ordered),
        },
        "controls": controls,
        "replays": replays,
    }


def write_receipt(path: Path, receipt: Mapping[str, Any]) -> None:
    """Indented JSON with each run's record on one line, so a diff reads by run."""
    head = {key: value for key, value in receipt.items() if key not in ("controls", "replays")}
    text = json.dumps(head, indent=2)[:-2]
    for name in ("controls", "replays"):
        rows = ",\n".join("    " + json.dumps(record) for record in receipt[name])
        text += f',\n  "{name}": [\n{rows}\n  ]'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text + "\n}\n")


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").split("\n\n")[0])
    parser.add_argument(
        "--python", required=True, help="interpreter of the author's pinned environment"
    )
    parser.add_argument(
        "--work",
        type=Path,
        required=True,
        help="a scratch directory outside the repository; reused to resume",
    )
    parser.add_argument("--out", type=Path, required=True, help="the receipt JSON to write")
    parser.add_argument("--jobs", type=int, default=2)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--cpu-cap-hours", type=float, default=DEFAULT_CPU_CAP_HOURS)
    parser.add_argument(
        "--counts", type=int, nargs="*", default=None, help="replay only these counts"
    )
    parser.add_argument(
        "--no-controls", action="store_true", help="skip the three rejection tests"
    )
    args = parser.parse_args(argv)

    work = args.work.resolve()
    if work.is_relative_to(REPO):
        raise SystemExit("--work must be outside the repository")
    work.mkdir(parents=True, exist_ok=True)
    counts = read_counts()
    if args.counts:
        unknown = sorted(set(args.counts) - set(counts))
        if unknown:
            raise SystemExit(f"not among the archive's 233 counts: {unknown}")
        counts = [n for n in counts if n in set(args.counts)]
    release = read_release(counts)
    runs = schedule(counts, release)
    if args.no_controls:
        runs = [run for run in runs if not run.control]
    modules = work / "modules"
    copy_modules(modules)
    ledger = work / "runs.jsonl"
    records = load_records(ledger)
    lock = threading.Lock()
    cap = args.cpu_cap_hours * 3600
    started = datetime.now(UTC)

    def spent() -> float:
        return sum(float(record["cpu_seconds"]) for record in records.values())

    def perform(run: Run) -> None:
        with lock:
            if run.key in records or spent() >= cap:
                return
        record = execute(
            run,
            python=args.python,
            modules=modules,
            work=work,
            release=release,
            timeout=args.timeout,
        )
        with lock:
            records[run.key] = record
            with ledger.open("a") as handle:
                handle.write(json.dumps(record) + "\n")
        print(
            f"{run.key}: passed={record['passed']} cpu={record['cpu_seconds']}s "
            f"wall={record['wall_seconds']}s",
            flush=True,
        )

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        list(pool.map(perform, runs))
    header = {
        "format": "evand-gradec-replay/1",
        "route": "same-implementation",
        "bead": "think-mtah",
        "last_invocation": {
            "started_utc": started.isoformat(timespec="seconds"),
            "finished_utc": datetime.now(UTC).isoformat(timespec="seconds"),
        },
        "program": {
            "retained": str(SCRIPTS_DIR.relative_to(REPO)),
            "modules": list(MODULES),
            "upstream_revision": UPSTREAM_REVISION,
            "ran_from": "a fresh copy of the four modules outside the repository",
        },
        "inputs": {
            "archive": str(ARCHIVE.relative_to(REPO)),
            "exact_forms": str(MINPOLY_DIR.relative_to(REPO)),
            "counts": str(COUNTS_FILE.relative_to(REPO)),
            "dropzero": sorted(DROPZERO),
        },
        "environment": {
            **interpreter_versions(args.python),
            "packages_source": "env.sh's pins, installed into a fresh virtual environment",
            "flags": "-E -s, an empty working directory, the input path as the argument",
            "threads": "OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1, as env.sh sets",
            "machine": {"cpus": os.cpu_count(), "jobs": args.jobs, "niceness": os.nice(0)},
            "timeout_seconds": args.timeout,
            "cpu_cap_hours": args.cpu_cap_hours,
        },
        "comparison": (
            "each certificate byte for byte with the archive's n-N.gradec.json; each log, "
            "with the input path written n-N and every '(... s)' time as T, line for line "
            "with the archive's n-N.log (n-N.dropzero.log at 230 and 261)"
        ),
    }
    receipt = summarize(runs, records, header)
    write_receipt(args.out, receipt)
    summary = receipt["summary"]
    print(json.dumps(summary))
    return 0 if summary["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
