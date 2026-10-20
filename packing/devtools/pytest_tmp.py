"""Bound what pytest leaves in the temporary directory, and measure what tests write there.

`pyproject.toml` loads this plugin into every session through `addopts` and sets
`tmp_path_retention_policy = "failed"`: a passing test's `tmp_path` is removed when the
test ends, and a session in which every test passed removes its whole numbered directory
at exit, so only failures stay behind to inspect. The plugin covers the one case that
policy cannot reach, and measures the rest.

**Killed sessions.** pytest names each session's directory `pytest-of-<user>/pytest-N`
and writes the session's PID to a `.lock` file inside it, removing the lock at exit.
Every later session prunes the numbered directories beyond the newest
`tmp_path_retention_count`, but skips any whose lock is younger than three days. A
session that never reaches its exit -- SIGTERM from a validation deadline or a cancelled
gate, SIGKILL, an agent's command timeout -- leaves its lock behind, so its whole tree
outlived every later session for three days. On 2026-10-16 that left about 11 GB in
`/tmp/pytest-of-root` across 19 numbered directories, with `pytest-3` still present
beside `pytest-132`. pytest's `cleanup_numbered_dir` also removes `garbage-*`
directories, the trees a session was deleting when it died, under the same lock rule.

At the start of each session that uses the shared numbered root (not an xdist worker,
not one given `--basetemp`), `release_dead_locks` removes the lock of every `pytest-N`
and `garbage-*` directory whose recorded process no longer exists. pytest's own
retention at that session's exit then treats them as finished sessions: those beyond the
newest `tmp_path_retention_count` are deleted, the rest are kept. A lock whose process
still exists, whose PID is unreadable, or that is half-written is left alone. A PID is
only meaningful in the PID namespace that wrote it, so this assumes the processes that
share one temporary root also share one PID namespace -- true of one machine or one
container, and not of containers that bind-mount the same `/tmp`. A reused PID errs the
safe way: the directory waits for pytest's three days.

**Measurement.** `--tmp-usage PATH` appends JSON lines to `PATH`: one per test that used
`tmp_path` (its allocated bytes and file count just before teardown removes it), one per
directory left in the session's base directory at session finish that no test's
`tmp_path` accounts for (session- and module-scoped `tmp_path_factory` directories, which
pytest keeps until the session ends, once per xdist worker), and from the controller the
peak allocated size of the session's base temporary directory, sampled every
`--tmp-usage-interval` seconds. To include what tools write through `tempfile` outside
it, point `TMPDIR` at a fresh directory and pass the same directory as
`--tmp-usage-root`. Summarize a report with

    uv run --frozen --all-extras --group dev python -m devtools.pytest_tmp summarize PATH

Sizes are allocated blocks of distinct inodes, which is what a full disk runs out of.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import threading
import time
from collections import defaultdict
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager, suppress
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

SCHEMA = "pytest-tmp-usage-v1"
NUMBERED_PREFIX = "pytest-"
GARBAGE_PREFIX = "garbage-"
LOCK_NAME = ".lock"
DEFAULT_INTERVAL_SECONDS = 2.0
PEAK_OWNERS = 20
BUDGET_OPTION = "tmp_path_budget_mib"


# -- killed sessions -------------------------------------------------------------------


def numbered_root() -> Path:
    """The directory pytest numbers its session directories in, as it computes it."""
    temproot = Path(os.environ.get("PYTEST_DEBUG_TEMPROOT") or tempfile.gettempdir())
    try:
        user = getpass.getuser()
    except OSError, KeyError:
        user = "unknown"
    return temproot.resolve() / f"pytest-of-{user}"


def process_exists(pid: int) -> bool:
    """Whether `pid` names a live process; any doubt answers yes."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except OSError:
        return True  # EPERM: alive and someone else's
    return True


def release_dead_locks(root: Path) -> list[Path]:
    """Remove the lock of every numbered or garbage directory whose owner has exited.

    Returns the directories released. pytest's own retention deletes them later.
    """
    if os.name != "posix":
        return []  # os.kill(pid, 0) terminates the process on Windows
    try:
        entries = sorted(root.iterdir())
    except OSError:
        return []
    released: list[Path] = []
    for entry in entries:
        if not entry.name.startswith((NUMBERED_PREFIX, GARBAGE_PREFIX)):
            continue
        if entry.is_symlink() or not entry.is_dir():
            continue  # `pytest-current` is a symlink to the newest session
        lock = entry / LOCK_NAME
        try:
            text = lock.read_text(encoding="ascii")
        except OSError, UnicodeDecodeError:
            continue
        if not text.isdecimal():
            continue  # absent or half-written: its owner may be creating it now
        pid = int(text)
        if pid <= 0 or pid == os.getpid() or process_exists(pid):
            continue
        with suppress(OSError):
            lock.unlink()
            released.append(entry)
    return released


# -- measurement -----------------------------------------------------------------------


# The measurement runs inside other tests' lifetimes: its teardown hook before their
# monkeypatches are undone, its sampler thread beside them. Tests here inject failures
# into `os.write`, guard `os.scandir` and drive `time.monotonic`, so it holds the
# originals rather than looking them up when it runs.
_scandir = os.scandir
_open = os.open
_write = os.write
_close = os.close
_monotonic = time.monotonic
_dumps = json.dumps


@dataclass(frozen=True)
class Usage:
    """Allocated bytes and regular-file count of one tree, and which directories hold them.

    `owners` maps each owning directory to its bytes: the first path component below
    pytest's own nesting (`pytest-of-*`, `pytest-N`, `popen-gwN`), so a test's `tmp_path`,
    a `tmp_path_factory` directory and a tool's `tempfile` directory each count apart.
    """

    bytes: int
    files: int
    owners: dict[str, int] = field(default_factory=dict[str, int])


_NESTING = re.compile(r"pytest-of-.+|pytest-\d+|popen-gw\d+")


def tree_usage(root: str | Path) -> Usage:
    """Allocated size of the distinct inodes under `root`, not following symlinks.

    A missing root measures zero, and entries that vanish while the walk runs are
    skipped: another process may be deleting them.
    """
    seen: set[tuple[int, int]] = set()
    owners: dict[str, int] = defaultdict(int)
    total = 0
    files = 0
    pending: list[tuple[str, str | None]] = [(str(root), None)]
    while pending:
        directory, owner = pending.pop()
        try:
            iterator = _scandir(directory)
        except OSError:
            continue
        with iterator:
            for entry in iterator:
                try:
                    status = entry.stat(follow_symlinks=False)
                except OSError:
                    continue
                name = owner
                if name is None:
                    name = os.path.relpath(entry.path, root)
                    nesting = stat.S_ISDIR(status.st_mode) and _NESTING.fullmatch(entry.name)
                    if nesting:
                        pending.append((entry.path, None))
                        continue
                if stat.S_ISDIR(status.st_mode):
                    pending.append((entry.path, name))
                key = (status.st_dev, status.st_ino)
                if key in seen:
                    continue
                seen.add(key)
                size = _allocated(status)
                total += size
                owners[name] += size
                if stat.S_ISREG(status.st_mode):
                    files += 1
    return Usage(total, files, dict(owners))


def _allocated(status: os.stat_result) -> int:
    blocks = getattr(status, "st_blocks", None)
    return status.st_size if blocks is None else int(blocks) * 512


def _session_basetemp(config: pytest.Config) -> Path | None:
    """This process's base temporary directory, or None before any test has asked for one.

    pytest exposes no public way to read it without creating it.
    """
    factory = getattr(config, "_tmp_path_factory", None)
    basetemp: Path | None = getattr(factory, "_basetemp", None)
    return basetemp


class _Sampler:
    """Track the largest size a directory reaches, from a daemon thread."""

    def __init__(self, locate: Callable[[], Path | None], label: str, interval: float) -> None:
        self.locate = locate
        self.label = label
        self.interval = interval
        self.peak = Usage(0, 0)
        self.peak_at = 0.0
        self.samples = 0
        self._started = _monotonic()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, name="tmp-usage", daemon=True)
        self._thread.start()

    def _sample(self) -> None:
        root = self.locate()
        usage = Usage(0, 0) if root is None else tree_usage(root)
        self.samples += 1
        if usage.bytes > self.peak.bytes:
            self.peak = usage
            self.peak_at = _monotonic() - self._started

    def _run(self) -> None:
        self._sample()
        while not self._stop.wait(self.interval):
            self._sample()

    def finish(self) -> None:
        self._stop.set()
        self._thread.join()
        self._sample()


class UsageRecorder:
    """One serial runner, xdist worker or xdist controller, appending rows to one report."""

    def __init__(
        self, config: pytest.Config, report: Path, root: Path | None, interval: float
    ) -> None:
        self.config = config
        worker_input: dict[str, Any] | None = getattr(config, "workerinput", None)
        self.worker = "main" if worker_input is None else str(worker_input["workerid"])
        self.measured: set[str] = set()
        # One descriptor for the session; O_APPEND keeps workers' rows whole.
        self.descriptor = _open(report, os.O_WRONLY | os.O_APPEND | os.O_CREAT, 0o644)
        self.sampler: _Sampler | None = None
        if worker_input is None:
            self.sampler = (
                _Sampler(lambda: _session_basetemp(config), "the session basetemp", interval)
                if root is None
                else _Sampler(lambda: root, str(root), interval)
            )

    def _emit(self, row: dict[str, object]) -> None:
        line = _dumps({"schema": SCHEMA, "worker": self.worker, **row}, sort_keys=True)
        _write(self.descriptor, (line + "\n").encode())

    def record_test(self, nodeid: str, path: Path, usage: Usage) -> None:
        self.measured.add(str(path))
        self._emit(
            {"event": "test", "nodeid": nodeid, "bytes": usage.bytes, "files": usage.files}
        )

    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionfinish(self, exitstatus: int | pytest.ExitCode) -> None:
        # tryfirst: pytest's own session finish removes a passing session's directory.
        basetemp = _session_basetemp(self.config)
        entries: list[os.DirEntry[str]] = []
        if basetemp is not None:
            with suppress(OSError), _scandir(basetemp) as iterator:
                entries = sorted(iterator, key=lambda entry: entry.name)
        for entry in entries:
            if not entry.is_dir(follow_symlinks=False):
                continue
            if entry.name.startswith("popen-gw") or entry.path in self.measured:
                continue  # a worker's own directory, or a test already counted
            usage = tree_usage(entry.path)
            self._emit(
                {
                    "event": "residue",
                    "name": entry.name,
                    "bytes": usage.bytes,
                    "files": usage.files,
                }
            )
        row: dict[str, object] = {"event": "session", "exitstatus": int(exitstatus)}
        if self.sampler is not None:
            self.sampler.finish()
            owners = sorted(
                ((owner, size) for owner, size in self.sampler.peak.owners.items() if size),
                key=lambda item: -item[1],
            )
            row |= {
                "root": self.sampler.label,
                "peak_bytes": self.sampler.peak.bytes,
                "peak_files": self.sampler.peak.files,
                "peak_owners": [list(item) for item in owners[:PEAK_OWNERS]],
                "peak_at_seconds": round(self.sampler.peak_at, 1),
                "samples": self.sampler.samples,
            }
        self._emit(row)
        _close(self.descriptor)


class TmpPathMonitor:
    """Measure each test's `tmp_path` once, for the budget and for the report."""

    def __init__(self, budget_bytes: int, recorder: UsageRecorder | None) -> None:
        self.budget_bytes = budget_bytes
        self.recorder = recorder

    @pytest.hookimpl(wrapper=True)
    def pytest_runtest_teardown(
        self, item: pytest.Item, nextitem: pytest.Item | None
    ) -> Iterator[None]:
        # Measured before the fixtures' own teardown, which removes a passing test's
        # tmp_path; judged after it, so a refusal never skips a finalizer.
        del nextitem
        funcargs: dict[str, object] = getattr(item, "funcargs", {})
        path = funcargs.get("tmp_path")
        usage = tree_usage(path) if isinstance(path, Path) else None
        if self.recorder is not None and isinstance(path, Path) and usage is not None:
            self.recorder.record_test(item.nodeid, path, usage)
        result = yield
        if usage is not None and 0 < self.budget_bytes < usage.bytes:
            pytest.fail(
                f"tmp_path held {_mib(usage.bytes)} in {usage.files:,} files at teardown, "
                f"over the {_mib(self.budget_bytes)} `{BUDGET_OPTION}`: share a read-only "
                "fixture, copy or check out only what the test reads, or write less "
                "(development.md, Temporary test directories)",
                pytrace=False,
            )
        return result


# -- scoped directories ----------------------------------------------------------------


@contextmanager
def scoped_tmp_path(
    request: pytest.FixtureRequest, factory: pytest.TempPathFactory, basename: str
) -> Iterator[Path]:
    """A `tmp_path_factory` directory that a module- or class-scoped fixture gives back.

    pytest removes a `tmp_path_factory` directory only when the whole session ends, so a
    module-scoped fixture's tree occupies the disk for the rest of the session and, if
    any test anywhere fails, survives it. Yield from this in the fixture instead: the
    directory goes when the fixture's scope ends, unless a test failed while it was open
    or the retention policy is `all`, mirroring what pytest does with a test's `tmp_path`.
    """
    failures = request.session.testsfailed
    directory = factory.mktemp(basename)
    yield directory
    keep = request.config.getini("tmp_path_retention_policy") == "all"
    if not keep and request.session.testsfailed == failures:
        shutil.rmtree(directory, ignore_errors=True)


# -- pytest hooks ----------------------------------------------------------------------


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addini(
        BUDGET_OPTION,
        "fail a test whose tmp_path holds more than this many MiB at teardown; 0 disables",
        default="0",
    )
    group = parser.getgroup("tmp-usage", "temporary directory usage (devtools.pytest_tmp)")
    group.addoption(
        "--tmp-usage",
        metavar="PATH",
        default=None,
        help="append each test's tmp_path size, the session residue and the peak "
        "temporary-root size to this JSON-lines file",
    )
    group.addoption(
        "--tmp-usage-interval",
        metavar="SECONDS",
        type=float,
        default=DEFAULT_INTERVAL_SECONDS,
        help="how often the controller samples the size of the sampled root",
    )
    group.addoption(
        "--tmp-usage-root",
        metavar="DIR",
        default=None,
        help="sample this directory's peak size instead of the session's base temporary "
        "directory: a fresh TMPDIR, to include the tools' own tempfile use",
    )


def pytest_configure(config: pytest.Config) -> None:
    worker = hasattr(config, "workerinput")
    if not worker and config.getoption("basetemp") is None:
        release_dead_locks(numbered_root())
    try:
        budget = float(str(config.getini(BUDGET_OPTION)))
    except ValueError as error:
        raise pytest.UsageError(f"{BUDGET_OPTION} must be a number of MiB") from error
    if budget < 0:
        raise pytest.UsageError(f"{BUDGET_OPTION} must not be negative")
    recorder: UsageRecorder | None = None
    report = config.getoption("tmp_usage")
    if report is not None:
        interval = config.getoption("tmp_usage_interval")
        if not isinstance(interval, float) or interval <= 0:
            raise pytest.UsageError("--tmp-usage-interval must be positive")
        root = config.getoption("tmp_usage_root")
        recorder = UsageRecorder(
            config,
            Path(report).resolve(),
            None if root is None else Path(root).resolve(),
            interval,
        )
        config.pluginmanager.register(recorder, "tmp-usage-recorder")
    if budget or recorder is not None:
        monitor = TmpPathMonitor(int(budget * 2**20), recorder)
        config.pluginmanager.register(monitor, "tmp-path-monitor")


# -- report ----------------------------------------------------------------------------


def _mib(value: int) -> str:
    return f"{value / 2**20:,.1f} MiB"


def _module(nodeid: str) -> str:
    return nodeid.split("::", 1)[0]


def summarize(rows: Sequence[dict[str, Any]], top: int) -> str:
    """A plain-text account of one report: totals, then the largest writers."""
    tests = [row for row in rows if row.get("event") == "test"]
    residue = [row for row in rows if row.get("event") == "residue"]
    sessions = [row for row in rows if row.get("event") == "session" and "peak_bytes" in row]
    by_module: dict[str, int] = defaultdict(int)
    for row in tests:
        by_module[_module(str(row["nodeid"]))] += int(row["bytes"])
    by_residue: dict[str, int] = defaultdict(int)
    for row in residue:
        by_residue[str(row["name"])] += int(row["bytes"])
    written = sum(int(row["bytes"]) for row in tests)
    kept = sum(int(row["bytes"]) for row in residue)
    lines = [
        (
            f"tests with tmp_path: {len(tests)}, holding {_mib(written)} "
            f"in {sum(int(row['files']) for row in tests):,} files at teardown"
        ),
        f"session-scoped directories at session finish: {len(residue)}, {_mib(kept)}",
        f"tmp_path bytes a retain-everything policy keeps: {_mib(written + kept)}",
    ]
    for row in sessions:
        lines.append(
            f"peak of {row['root']}: {_mib(int(row['peak_bytes']))} "
            f"at {row['peak_at_seconds']} s over {row['samples']} samples, held by"
        )
        lines.extend(
            f"  {_mib(int(size)):>14}  {owner}"
            for owner, size in row.get("peak_owners", [])[:top]
        )
    lines.append(f"\nlargest {top} tests:")
    lines.extend(
        f"  {_mib(int(row['bytes'])):>14}  {int(row['files']):>7,} files  {row['nodeid']}"
        for row in sorted(tests, key=lambda row: -int(row["bytes"]))[:top]
    )
    lines.append(f"\nlargest {top} test modules:")
    lines.extend(
        f"  {_mib(size):>14}  {module}"
        for module, size in sorted(by_module.items(), key=lambda item: -item[1])[:top]
    )
    if by_residue:
        lines.append(f"\nlargest {top} session-scoped directories, summed over workers:")
        lines.extend(
            f"  {_mib(size):>14}  {name}"
            for name, size in sorted(by_residue.items(), key=lambda item: -item[1])[:top]
        )
    return "\n".join(lines)


def read_report(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        row = json.loads(line)
        if not isinstance(row, dict) or row.get("schema") != SCHEMA:
            raise ValueError(f"{path}:{number}: not a {SCHEMA} row")
        rows.append(row)
    return rows


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m devtools.pytest_tmp", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("summarize", help="summarize a --tmp-usage report")
    report.add_argument("report", type=Path)
    report.add_argument("--top", type=int, default=20)
    arguments = parser.parse_args(argv)
    print(summarize(read_report(arguments.report), arguments.top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
