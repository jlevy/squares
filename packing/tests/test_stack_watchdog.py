"""A test phase that runs long dumps every stack once, from a thread that holds the GIL,
and the process that runs it lives on (think-sj00, `D-523`).

pytest's `faulthandler_timeout` takes the same dump from CPython's C watchdog, which
walks the threads without the GIL and crashed an xdist worker twice on 2026-11-12, when
one of the preview server's request threads ended during the walk. That crash depends
on timing and is not reproduced here. What this file holds instead is the property that
rules it out: `Current thread ... [stack-watchdog]` can only be written by a dump that
the plugin's Python thread takes itself, because the C watchdog has no Python thread
state to call current.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from pathlib import Path
from threading import Thread, current_thread
from typing import override

import pytest

from devtools import stack_watchdog
from devtools.stack_watchdog import Watchdog
from sqpack.cli import validate

PACKING = Path(__file__).resolve().parents[1]
REPO = PACKING.parent

PROBE = """\
import time

import pytest


@pytest.fixture
def slow_fixture():
    time.sleep(1.0)


def test_slow_setup(slow_fixture):
    pass


def test_slow_call():
    time.sleep(1.0)


def test_fast():
    pass


def test_a_patched_clock_keeps_its_readings(monkeypatch):
    readings = iter([1.0, 2.0])
    monkeypatch.setattr(time, "monotonic", lambda: next(readings))
    assert (time.monotonic(), time.monotonic()) == (1.0, 2.0)
"""

UNARMED = """\
from pathlib import Path

import pytest

from devtools import stack_watchdog

EVENTS = Path(__file__).with_name("events.txt")


def _no_clock():
    raise RuntimeError("no clock")


stack_watchdog.monotonic = _no_clock


@pytest.fixture
def resource():
    with EVENTS.open("a", encoding="utf-8") as events:
        events.write("setup\\n")
    yield
    with EVENTS.open("a", encoding="utf-8") as events:
        events.write("teardown\\n")


def test_uses_resource(resource):
    with EVENTS.open("a", encoding="utf-8") as events:
        events.write("call\\n")
"""

HEADER = re.compile(r"^Stack watchdog: (\S+) (setup|call|teardown) has run", re.MULTILINE)
CURRENT = re.compile(r"^Current thread 0x[0-9a-f]+ \[stack-watchdog\]", re.MULTILINE)


def _run_probe(tmp_path: Path, probe: str) -> subprocess.CompletedProcess[str]:
    """Run `probe` as its own pytest session, with the plugin at half a second."""
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(probe, encoding="utf-8")
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("PYTEST_")
    }
    environment["PYTHONPATH"] = os.pathsep.join(
        (str(PACKING), os.environ.get("PYTHONPATH", ""))
    )
    return subprocess.run(
        (
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-c",
            os.devnull,
            "--rootdir",
            str(tmp_path),
            "--basetemp",
            str(tmp_path / "basetemp"),
            "-p",
            "no:cacheprovider",
            *validate.stack_watchdog(0.5),
            str(test_file),
        ),
        capture_output=True,
        text=True,
        env=environment,
        timeout=120,
        check=False,
    )


def test_an_armed_phase_past_its_limit_dumps_once_from_the_watchdog_thread(
    tmp_path: Path,
) -> None:
    path = tmp_path / "dump"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT)
    watchdog = Watchdog(0.05, fd, "unit")
    watchdog.arm("probe.py::test_x call")
    deadline = time.monotonic() + 10
    while watchdog.dumps == 0 and time.monotonic() < deadline:
        time.sleep(0.01)
    time.sleep(0.2)  # a second dump for the same arming would land here
    watchdog.close()
    os.close(fd)
    dump = path.read_text(encoding="utf-8")
    assert HEADER.findall(dump) == [("probe.py::test_x", "call")]
    assert "on unit (pid " in dump
    assert CURRENT.search(dump), dump
    assert watchdog.dumps == 1


def test_a_phase_that_ends_inside_its_limit_dumps_nothing(tmp_path: Path) -> None:
    path = tmp_path / "dump"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT)
    watchdog = Watchdog(30, fd, "unit")
    watchdog.arm("probe.py::test_x setup")
    watchdog.disarm()
    watchdog.close()
    os.close(fd)
    assert path.read_text(encoding="utf-8") == ""
    assert watchdog.dumps == 0


class _EndsOnce(Watchdog):
    """A watchdog whose first thread ends at once, as one an exception had killed would."""

    def __init__(self, seconds: float, fd: int, worker: str) -> None:
        super().__init__(seconds, fd, worker)
        self.threads: list[Thread] = []

    @override
    def _watch(self) -> None:
        self.threads.append(current_thread())
        if len(self.threads) > 1:
            super()._watch()


def test_a_watchdog_thread_that_ended_is_started_again(tmp_path: Path) -> None:
    """A dead thread is replaced at the next arming, so later phases are still timed."""
    path = tmp_path / "dump"
    fd = os.open(path, os.O_WRONLY | os.O_CREAT)
    watchdog = _EndsOnce(0.05, fd, "unit")
    watchdog.arm("probe.py::test_x setup")
    deadline = time.monotonic() + 10
    while not watchdog.threads and time.monotonic() < deadline:
        time.sleep(0.01)
    watchdog.threads[0].join(10)
    assert not watchdog.threads[0].is_alive()
    watchdog.arm("probe.py::test_x call")
    while watchdog.dumps == 0 and time.monotonic() < deadline:
        time.sleep(0.01)
    watchdog.close()
    os.close(fd)
    assert len(watchdog.threads) == 2
    assert HEADER.findall(path.read_text(encoding="utf-8")) == [("probe.py::test_x", "call")]


def test_pytest_dumps_each_slow_phase_by_name_and_the_run_passes(tmp_path: Path) -> None:
    """Setup and call are timed apart, so a slow fixture is named as setup; a fast test
    is not named at all, and the dump reaches the terminal through pytest's capture.

    A test that sets `time.monotonic` to a finite iterator keeps every reading it set:
    `tests/test_site_rendering.py` does, and a watchdog that read the clock through the
    module spent those readings, ended in StopIteration and left 595 errors in the
    frontend job of #968's first push."""
    result = _run_probe(tmp_path, PROBE)
    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    assert "4 passed" in result.stdout
    assert HEADER.findall(output) == [
        ("test_probe.py::test_slow_setup", "setup"),
        ("test_probe.py::test_slow_call", "call"),
    ]
    assert len(CURRENT.findall(output)) == 2
    assert re.search(r'test_probe\.py", line \d+ in test_slow_call$', output, re.MULTILINE)


def test_a_watchdog_that_cannot_arm_warns_and_the_phase_still_runs(tmp_path: Path) -> None:
    """A clock that raises leaves every phase and the fixture's teardown to run, and the
    PytestWarning names each phase that went untimed."""
    result = _run_probe(tmp_path, UNARMED)
    output = result.stdout + result.stderr
    assert result.returncode == 0, output
    assert "1 passed" in result.stdout
    events = (tmp_path / "events.txt").read_text(encoding="utf-8").split()
    assert events == ["setup", "call", "teardown"]
    for phase in ("setup", "call", "teardown"):
        assert (
            "PytestWarning: stack watchdog not armed for "
            f"test_probe.py::test_uses_resource {phase}: RuntimeError('no clock')"
        ) in output, output


class _Config:
    def __init__(self, **ini: str) -> None:
        self.ini = ini
        self.stash = pytest.Stash()

    def getini(self, name: str) -> str:
        return self.ini.get(name, "0")


def test_the_plugin_refuses_to_run_beside_faulthandler_timeout() -> None:
    config = _Config(stack_watchdog_timeout="60", faulthandler_timeout="60")
    with pytest.raises(pytest.UsageError, match="D-523"):
        stack_watchdog.pytest_configure(config)  # pyright: ignore[reportArgumentType]
    assert stack_watchdog.WATCHDOG not in config.stash


def test_no_command_arms_cpython_s_c_watchdog() -> None:
    """The gate's commands, tools and workflows take stack dumps through the plugin."""
    unsafe = re.compile(r"faulthandler_timeout\s*=|dump_traceback_later\(")
    sources = [
        *(PACKING / "src").rglob("*.py"),
        *(PACKING / "devtools").rglob("*.py"),
        PACKING / "pyproject.toml",
        PACKING / "tests" / "conftest.py",
        REPO / "Makefile",
        REPO / "lefthook.yml",
        *(REPO / ".github" / "workflows").glob("*.y*ml"),
    ]
    found = [
        f"{path.relative_to(REPO)}:{number}"
        for path in sources
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1)
        if unsafe.search(line)
    ]
    assert found == []
