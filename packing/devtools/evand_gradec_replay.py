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

Each run copies its two inputs to a fresh directory of its own, one per attempt, outside
the repository, and runs ``gradec.py`` from a fresh copy of the four modules under the
given interpreter (a separate virtual environment with ``env.sh``'s pinned packages), with
``-E -s``, an empty working directory and the input path as its argument.  Isolated mode's
``-P`` is left out because gradec.py imports its three modules from its own directory, the
copy, which holds nothing else.  Nothing here imports from the source.  Each child runs in
a session of its own, and the driver kills every running child's group when it stops, so
no orphan outlives it; an attempt's directory is never reused, so an orphan of a killed
driver cannot write into a later attempt's.

**The ledger.** The work is resumable: each finished run appends one line to
``WORK/runs.jsonl``, and a later invocation with the same ``--work`` skips every run
recorded there (``--retry-failed`` runs a failed one again, and the ledger keeps both
attempts).  Only the last line may be torn, by a driver killed mid-write; it is cut off
before anything is appended, and an unreadable line anywhere else is refused.  One
invocation holds ``WORK/lock`` (``flock``) while it runs, and a second is refused.

**The environment.** ``WORK/environment.json`` names the environment the work was begun
under: the interpreter's version, the five packages ``env.sh`` pins and the platform, as
the given ``--python`` reports them.  Each run's record names the same (``interpreter``).
An invocation whose ``--python`` reports another is refused before anything runs, as is a
ledger holding a record of another, so one receipt never merges runs from two
environments; the interpreter is asked again before the receipt is written.  The module
copies are held byte for byte to the retained copy on every invocation (`copy_modules`),
and the archive and the exact forms are read from Git, which identifies them (OR-16).  A
work directory begun before records named their environment (the replay started on
1 November 2026) has records without ``interpreter`` and no ``environment.json``: it is
adopted once with ``--adopt-unstamped``, under the ``--python`` those runs were launched
with, which writes ``environment.json`` and names the records adopted; the receipt carries
the list and the basis of the adoption (``adopted_basis``, null when nothing was adopted),
since the adopted environment is asserted by that invocation, not stamped by the runs.  Records without ``interpreter`` appended after ``environment.json`` was
written, by an older driver, are refused.  An older
driver takes no lock, so this one cannot see it: point it at a work directory only once any
older driver using it has exited.

**The cap.** Runs are started longest first, by the build time the release's log prints.
A run starts only if the CPU time the ledger records, plus the worst case of every run
still going, plus its own worst case, stays within ``--cpu-cap-hours``; a run that cannot
fit even with nothing else running is not started, and the receipt is then incomplete.  The
worst case of a run is ``--timeout`` seconds of CPU, which each child is held to by
``RLIMIT_CPU`` where the platform allows (``resource.prlimit``) as well as to the same wall
time, so the recorded CPU time cannot pass the cap.  The receipt written to ``--out``
holds the environment and every run's record; its ``complete`` says whether all ran.

Run it from ``packing/``::

    nice -n 10 uv run --frozen --all-extras --group dev python -m devtools.evand_gradec_replay \
        --python VENV/bin/python --work SCRATCH --jobs 2 \
        --out resources/web/evand-exact-data-2026-10-12/receipts/gradec-replay-233.json
"""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import gzip
import json
import os
import re
import resource
import shutil
import signal
import subprocess
import tarfile
import threading
import time
import uuid
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, TextIO, cast

from strif import atomic_output_file

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

RECEIPT_FORMAT = "evand-gradec-replay/2"
ENVIRONMENT_FORMAT = "evand-gradec-replay-environment/1"
LEDGER = "runs.jsonl"
ENVIRONMENT = "environment.json"
LOCK = "lock"

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
    """The interpreter's version, the five packages ``env.sh`` pins, and its platform."""
    probe = (
        "import json, platform, sys, numpy, scipy, mpmath, sympy, flint; print(json.dumps({"
        "'python': sys.version.split()[0], 'numpy': numpy.__version__, "
        "'scipy': scipy.__version__, 'mpmath': mpmath.__version__, "
        "'sympy': sympy.__version__, 'python-flint': flint.__version__, "
        "'platform': platform.system() + ' ' + platform.machine()}))"
    )
    result = subprocess.run(
        [python, "-I", "-c", probe], capture_output=True, text=True, check=True
    )
    return dict(sorted(json.loads(result.stdout).items()))


def interpreter_differences(old: Mapping[str, Any], new: Mapping[str, Any]) -> list[str]:
    """Where two environments differ, as ``name: old -> new``."""
    return [
        f"{key}: {old.get(key)} -> {new.get(key)}"
        for key in sorted(set(old) | set(new))
        if old.get(key) != new.get(key)
    ]


def check_environment(
    work: Path,
    interpreter: Mapping[str, str],
    attempts: Sequence[Mapping[str, Any]],
    *,
    adopt_unstamped: bool,
) -> dict[str, Any]:
    """Hold the work directory to one environment, and return its ``environment.json``.

    The file is written when the work begins, or once, with ``adopt_unstamped``, for a
    ledger whose records were written before they named their environment; ``attempts``
    is every record the ledger holds.
    """
    current = dict(sorted(interpreter.items()))
    path = work / ENVIRONMENT
    header: dict[str, Any] | None = json.loads(path.read_text()) if path.exists() else None
    if header is not None and header.get("interpreter") != current:
        changes = "; ".join(interpreter_differences(header.get("interpreter") or {}, current))
        raise SystemExit(
            f"{work} was begun under another environment ({changes}); resume it under the "
            "same --python, or begin a new --work"
        )
    other = sorted(
        {
            str(record["key"])
            for record in attempts
            if record.get("interpreter") not in (None, current)
        }
    )
    if other:
        raise SystemExit(f"{work}: runs recorded under another environment: {other}")
    unstamped = sorted({str(r["key"]) for r in attempts if "interpreter" not in r})
    if header is None:
        if unstamped and not adopt_unstamped:
            raise SystemExit(
                f"{work}: {len(unstamped)} recorded runs name no environment, since they "
                "were written before the ledger recorded one; if they ran under this "
                "--python, pass --adopt-unstamped once to record it for them"
            )
        header = {
            "format": ENVIRONMENT_FORMAT,
            "interpreter": current,
            "written_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "adopted_unstamped": unstamped,
        }
        if unstamped:
            header["adopted_basis"] = (
                "asserted by the invocation that adopted them: these runs were launched "
                "under this --python, before records named their environment"
            )
        with atomic_output_file(path) as temporary:
            temporary.write_text(json.dumps(header, indent=1) + "\n")
        return header
    late = sorted(set(unstamped) - set(header.get("adopted_unstamped", [])))
    if late:
        raise SystemExit(
            f"{work}: runs without an environment were recorded after {ENVIRONMENT} was "
            f"written, so an older driver wrote to this work directory: {late}"
        )
    return header


def differing_keys(output: bytes, published: bytes) -> list[str]:
    """The top-level certificate fields whose values differ, for a run that is not identical."""
    try:
        ours, theirs = json.loads(output), json.loads(published)
    except ValueError:
        return ["<unparsable>"]
    keys = sorted(set(ours) | set(theirs))
    return [key for key in keys if ours.get(key) != theirs.get(key)]


@dataclass
class Children:
    """The process groups of the running children, so a stopping driver can end them.

    A child is listed from its start until it has exited and before it is reaped, and
    every kill is made under the lock, so no kill can reach a process that took a reaped
    child's pid.
    """

    groups: set[int] = field(default_factory=set[int])
    #: Re-entrant, since the SIGTERM handler kills from the main thread.
    lock: threading.RLock = field(default_factory=threading.RLock)
    stopping: threading.Event = field(default_factory=threading.Event)

    def discard(self, pid: int) -> None:
        with self.lock:
            self.groups.discard(pid)

    def kill(self, pid: int) -> None:
        """Kill one child's process group, if it has not exited."""
        with self.lock:
            if pid in self.groups:
                _killpg(pid)

    def kill_all(self) -> None:
        """Mark the driver stopping and kill every running child's process group."""
        self.stopping.set()
        with self.lock:
            for group in sorted(self.groups):
                _killpg(group)


def _killpg(group: int) -> None:
    with contextlib.suppress(OSError):
        os.killpg(group, signal.SIGKILL)


def hold_cpu(pid: int, seconds: float) -> bool:
    """Hold a child to ``seconds`` of CPU by ``RLIMIT_CPU``, where the platform allows."""
    limit = getattr(resource, "prlimit", None)
    if limit is None:
        return False
    soft = max(1, int(seconds))
    try:
        limit(pid, resource.RLIMIT_CPU, (soft, soft + 5))
    except OSError, ValueError:
        return False
    return True


def attempt_directory(work: Path, run: Run) -> Path:
    """A directory no other attempt uses; earlier attempts' directories are removed."""
    parent = work / "runs" / run.key
    if parent.exists():
        shutil.rmtree(parent)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return parent / f"attempt-{stamp}-{os.getpid()}-{uuid.uuid4().hex[:8]}"


def execute(
    run: Run,
    *,
    python: str,
    modules: Path,
    work: Path,
    release: Release,
    timeout: float,
    cpu_limit: float | None = None,
    minpoly_dir: Path = MINPOLY_DIR,
    children: Children | None = None,
) -> dict[str, Any]:
    """Run gradec.py once in a fresh directory and judge what it wrote.

    The child is held to ``timeout`` seconds of wall time and to ``cpu_limit`` seconds of
    CPU (``timeout`` unless given), and runs in a session of its own, whose group is
    killed at either limit.
    """
    cpu_limit = timeout if cpu_limit is None else cpu_limit
    directory = attempt_directory(work, run)
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
        status, usage, cpu_held = _supervise(
            [python, "-E", "-s", str(modules / "gradec.py"), str(base)],
            cwd=cwd,
            env=env,
            log=log,
            timeout=timeout,
            cpu_limit=cpu_limit,
            children=children,
        )
    exit_code = os.waitstatus_to_exitcode(status)
    wall_seconds = time.monotonic() - wall
    cpu_seconds = usage.ru_utime + usage.ru_stime
    timed_out = wall_seconds >= timeout and exit_code != 0
    cpu_limited = exit_code in (-signal.SIGXCPU, -signal.SIGKILL) and (
        cpu_seconds >= cpu_limit - 1
    )
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
        "cpu_seconds": round(cpu_seconds, 1),
        "max_rss_mb": round(usage.ru_maxrss / 1024, 1),
        "exit_code": exit_code,
        "timed_out": timed_out,
        "cpu_limit_seconds": cpu_limit if cpu_held else None,
        "cpu_limited": cpu_limited,
        "attempt": directory.name,
        "last_lines": [line.replace(str(directory), "WORK") for line in lines[-TAIL_LINES:]],
    }
    if run.control:
        refused = (
            exit_code != 0
            and output is None
            and "AssertionError" in text
            and not timed_out
            and not cpu_limited
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
    record["passed"] = exit_code == 0 and identical and bool(record["valid"])
    return record


def _supervise(
    command: list[str],
    *,
    cwd: Path,
    env: Mapping[str, str],
    log: TextIO,
    timeout: float,
    cpu_limit: float,
    children: Children | None,
) -> tuple[int, resource.struct_rusage, bool]:
    """Start the child in a session of its own, hold it to both limits, and reap it.

    It is waited for without being reaped first, and delisted before it is reaped, so
    the wall timer and a stopping driver kill only while its pid is still its own.
    """
    children = Children() if children is None else children
    with children.lock:
        process = subprocess.Popen(
            command,
            cwd=cwd,
            env=dict(env),
            stdout=log,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        children.groups.add(process.pid)
    cpu_held = hold_cpu(process.pid, cpu_limit)
    timer = threading.Timer(timeout, children.kill, args=(process.pid,))
    timer.start()
    try:
        if children.stopping.is_set():
            children.kill(process.pid)
        os.waitid(os.P_PID, process.pid, os.WEXITED | os.WNOWAIT)
    finally:
        timer.cancel()
        children.discard(process.pid)
    _, status, usage = os.wait4(process.pid, 0)
    process.returncode = os.waitstatus_to_exitcode(status)
    return status, usage, cpu_held


# ---------------------------------------------------------------------------- the ledger


def repair_torn_tail(path: Path) -> bool:
    """Cut a torn last line (no newline: a driver killed mid-write) before appending."""
    if not path.exists():
        return False
    data = path.read_bytes()
    if not data or data.endswith(b"\n"):
        return False
    with path.open("r+b") as handle:
        handle.truncate(data.rfind(b"\n") + 1)
    return True


def load_attempts(path: Path) -> list[dict[str, Any]]:
    """Every record the ledger holds, in order; a torn last line is ignored.

    An unreadable line anywhere else is refused, since it means the ledger was damaged
    and its records cannot be trusted to be what ran.
    """
    if not path.exists():
        return []
    text = path.read_text()
    lines = text.splitlines()
    attempts: list[dict[str, Any]] = []
    for number, line in enumerate(lines, start=1):
        try:
            record = json.loads(line)
        except ValueError:
            if number == len(lines) and not text.endswith("\n"):
                continue
            raise SystemExit(f"{path}:{number}: not a record; the ledger is damaged") from None
        if not isinstance(record, dict) or "key" not in record:
            raise SystemExit(f"{path}:{number}: not a record; the ledger is damaged")
        attempts.append(cast("dict[str, Any]", record))
    return attempts


def load_records(path: Path) -> dict[str, dict[str, Any]]:
    """The runs a previous invocation finished, by key, the last attempt of each."""
    return {str(record["key"]): record for record in load_attempts(path)}


@contextlib.contextmanager
def locked(work: Path) -> Iterator[None]:
    """Hold ``WORK/lock`` for the invocation, refusing a second one."""
    path = work / LOCK
    with path.open("a+") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            handle.seek(0)
            holder = handle.read().strip() or "another invocation"
            raise SystemExit(f"{work} is in use ({holder}); one invocation at a time") from None
        handle.seek(0)
        handle.truncate()
        handle.write(f"pid {os.getpid()}, since {datetime.now(UTC).isoformat()}\n")
        handle.flush()
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


@dataclass
class Budget:
    """The CPU cap, counting the worst case of each run still going (``reserved``)."""

    cap: float
    worst: float
    spent: float = 0.0
    reserved: float = 0.0
    condition: threading.Condition = field(default_factory=threading.Condition)

    def admit(self) -> bool:
        """Reserve a run's worst case, waiting while running runs hold the room it needs.

        False once it cannot fit even with nothing else running.
        """
        with self.condition:
            while self.spent + self.reserved + self.worst > self.cap:
                if self.reserved == 0:
                    return False
                self.condition.wait()
            self.reserved += self.worst
            return True

    def release(self, cpu_seconds: float) -> None:
        with self.condition:
            self.reserved -= self.worst
            self.spent += cpu_seconds
            self.condition.notify_all()


def run_all(
    runs: Sequence[Run],
    records: dict[str, dict[str, Any]],
    *,
    start: Callable[[Run], dict[str, Any]],
    budget: Budget,
    jobs: int,
    append: Callable[[dict[str, Any]], None],
    children: Children,
    retry_failed: bool = False,
) -> list[str]:
    """Run every run the ledger has not finished, within the budget; the keys not started.

    A run is recorded only if the driver is not stopping, so a run killed by a stopping
    driver runs again on resume.
    """
    lock = threading.Lock()
    not_started: list[str] = []

    def perform(run: Run) -> None:
        with lock:
            done = records.get(run.key)
        if children.stopping.is_set() or (
            done is not None and (done.get("passed") or not retry_failed)
        ):
            return
        if not budget.admit():
            with lock:
                not_started.append(run.key)
            return
        if children.stopping.is_set():
            budget.release(0.0)
            return
        cpu = 0.0
        try:
            record = start(run)
            cpu = float(record["cpu_seconds"])
        finally:
            budget.release(cpu)
        if children.stopping.is_set():
            return
        with lock:
            records[run.key] = record
            append(record)
        print(
            f"{run.key}: passed={record['passed']} cpu={record['cpu_seconds']}s "
            f"wall={record['wall_seconds']}s",
            flush=True,
        )

    pool = ThreadPoolExecutor(max_workers=jobs)
    try:
        list(pool.map(perform, runs))
    finally:
        # Nothing runs once the map has finished; on an interruption this ends the
        # children first, since the pool's shutdown waits for them.
        children.kill_all()
        pool.shutdown(wait=True, cancel_futures=True)
    return sorted(not_started)


def summarize(
    runs: Sequence[Run],
    records: Mapping[str, Mapping[str, Any]],
    header: Mapping[str, Any],
    attempts: Sequence[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """The receipt: the header, the totals and every run's record, controls first.

    ``attempts``, every record the ledger holds, counts the CPU of attempts a retry
    superseded; without it the records are taken to be every attempt.
    """
    ordered = [records[run.key] for run in runs if run.key in records]
    controls = [record for record in ordered if record["control"]]
    replays = sorted((r for r in ordered if not r["control"]), key=lambda r: r["n"])
    expected = sum(1 for run in runs if not run.control)
    starts = [record["started_utc"] for record in ordered]
    keys = {run.key for run in runs}
    every = (
        list(ordered)
        if attempts is None
        else [record for record in attempts if record["key"] in keys]
    )
    superseded = len(every) - len(ordered)
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
            "cpu_limited": sorted(r["n"] for r in replays if r.get("cpu_limited")),
            "failed": sorted(r["n"] for r in replays if not r["passed"]),
            "controls_refused": sum(1 for r in controls if r["passed"]),
            "controls_run": len(controls),
            "cpu_seconds_total": round(sum(float(r["cpu_seconds"]) for r in every), 1),
            "cpu_seconds_replays": round(sum(float(r["cpu_seconds"]) for r in replays), 1),
            "superseded_attempts": superseded,
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
    """Indented JSON with each run's record on one line, so a diff reads by run.

    Written to a sibling and renamed into place, so a reader never sees half a receipt.
    """
    head = {key: value for key, value in receipt.items() if key not in ("controls", "replays")}
    text = json.dumps(head, indent=2)[:-2]
    for name in ("controls", "replays"):
        rows = ",\n".join("    " + json.dumps(record) for record in receipt[name])
        text += f',\n  "{name}": [\n{rows}\n  ]'
    path.parent.mkdir(parents=True, exist_ok=True)
    with atomic_output_file(path) as temporary:
        temporary.write_text(text + "\n}\n")


def _arguments(argv: Sequence[str] | None) -> argparse.Namespace:
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
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="each run's wall limit, and its CPU limit and worst case against the cap",
    )
    parser.add_argument("--cpu-cap-hours", type=float, default=DEFAULT_CPU_CAP_HOURS)
    parser.add_argument(
        "--counts", type=int, nargs="*", default=None, help="replay only these counts"
    )
    parser.add_argument(
        "--no-controls", action="store_true", help="skip the three rejection tests"
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="run again each recorded run that failed; the ledger keeps both attempts",
    )
    parser.add_argument(
        "--adopt-unstamped",
        action="store_true",
        help=(
            "once, for a ledger written before records carried their environment: record "
            "this --python's environment for those runs, which must have run under it"
        ),
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = _arguments(argv)
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
    with locked(work):
        return _replay(args, work, release, runs)


def _replay(args: argparse.Namespace, work: Path, release: Release, runs: list[Run]) -> int:
    modules = work / "modules"
    copy_modules(modules)
    versions = interpreter_versions(args.python)
    ledger = work / LEDGER
    if repair_torn_tail(ledger):
        print(f"{ledger}: cut a torn last line", flush=True)
    attempts = load_attempts(ledger)
    environment = check_environment(
        work, versions, attempts, adopt_unstamped=args.adopt_unstamped
    )
    records = {str(record["key"]): record for record in attempts}
    started = datetime.now(UTC)
    children = Children()
    budget = Budget(
        cap=args.cpu_cap_hours * 3600,
        worst=args.timeout,
        spent=sum(float(record["cpu_seconds"]) for record in attempts),
    )

    def start(run: Run) -> dict[str, Any]:
        record = execute(
            run,
            python=args.python,
            modules=modules,
            work=work,
            release=release,
            timeout=args.timeout,
            children=children,
        )
        return {**record, "interpreter": versions}

    def append(record: dict[str, Any]) -> None:
        attempts.append(record)
        with ledger.open("a") as handle:
            handle.write(json.dumps(record) + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    def stop(signum: int, _frame: object) -> None:
        children.kill_all()
        raise SystemExit(128 + signum)

    previous = signal.signal(signal.SIGTERM, stop)
    try:
        not_started = run_all(
            runs,
            records,
            start=start,
            budget=budget,
            jobs=args.jobs,
            append=append,
            children=children,
            retry_failed=args.retry_failed,
        )
    finally:
        signal.signal(signal.SIGTERM, previous)
    for key in not_started:
        print(f"{key}: not started, its worst case would pass the CPU cap", flush=True)
    if interpreter_versions(args.python) != versions:
        raise SystemExit("the environment changed during the invocation; no receipt written")
    header = {
        "format": RECEIPT_FORMAT,
        "route": "same-implementation",
        "bead": "think-mtah",
        "last_invocation": {
            "started_utc": started.isoformat(timespec="seconds"),
            "finished_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "not_started_for_the_cap": not_started,
        },
        "program": {
            "retained": str(SCRIPTS_DIR.relative_to(REPO)),
            "modules": list(MODULES),
            "upstream_revision": UPSTREAM_REVISION,
            "ran_from": (
                "a fresh copy of the four modules outside the repository, held byte for "
                "byte to the retained copy on every invocation"
            ),
        },
        "inputs": {
            "archive": str(ARCHIVE.relative_to(REPO)),
            "exact_forms": str(MINPOLY_DIR.relative_to(REPO)),
            "counts": str(COUNTS_FILE.relative_to(REPO)),
            "dropzero": sorted(DROPZERO),
        },
        "environment": {
            **versions,
            "adopted_unstamped": environment.get("adopted_unstamped", []),
            "adopted_basis": environment.get("adopted_basis"),
            "packages_source": "env.sh's pins, installed into a fresh virtual environment",
            "flags": "-E -s, an empty working directory, the input path as the argument",
            "threads": "OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1, as env.sh sets",
            "machine": {"cpus": os.cpu_count(), "jobs": args.jobs, "niceness": os.nice(0)},
            "timeout_seconds": args.timeout,
            "cpu_cap_hours": args.cpu_cap_hours,
            "cap_rule": (
                "a run starts only if the recorded CPU, the worst case of every run still "
                "going and its own stay within the cap; each run's worst case is its "
                "timeout, held by RLIMIT_CPU and the wall timer"
            ),
        },
        "comparison": (
            "each certificate byte for byte with the archive's n-N.gradec.json; each log, "
            "with the input path written n-N and every '(... s)' time as T, line for line "
            "with the archive's n-N.log (n-N.dropzero.log at 230 and 261)"
        ),
    }
    receipt = summarize(runs, records, header, attempts)
    write_receipt(args.out, receipt)
    summary = receipt["summary"]
    print(json.dumps(summary))
    return 0 if summary["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
