"""Stack dumps for a test phase that runs long, without crashing the process that runs it.

pytest's `faulthandler_timeout` arms `faulthandler.dump_traceback_later`. Its watchdog
is a C thread that walks every Python thread's state without the GIL, and in CPython
3.14 `_Py_DumpTracebackThreads` cannot tell a thread state that is being freed from a
live one in a release build. When a thread ends during the walk, the walk follows a
freed pointer, and the process dies of SIGSEGV. The watchdog thread blocks every
signal, so the kernel kills the process outright and no `Fatal Python error` is
printed. `devtools.preview_site.serve` answers each request on its own thread, so a
browser test that is loading pages is never far from a thread ending. Twice on
2026-11-12 a hosted frontend run lost xdist worker gw0 that way, during
`tests/test_site_atlas_views.py::test_viewport_size_prepaints_without_motion_and_keeps_explicit_choices`.
In both runs the replacement worker re-ran the test and it passed (think-sj00, D-523).

This plugin keeps the diagnostic and removes the crash. A Python thread waits for the
deadline and calls `faulthandler.dump_traceback`, which holds the GIL and stops the
world before reading another thread's state (CPython gh-128400). A thread can unlink
its own state only while it holds the GIL, so the walk never reaches a freed one. The
dump goes to the stderr pytest's faulthandler uses, duplicated before capture can
redirect it, and its header names the test, the phase and the worker.

Setup, call and teardown are timed separately. A module fixture that takes two minutes
to build on a starved runner shows as that test's slow setup rather than being added to
its call, and a hang in any phase still produces a dump once that phase passes the
limit. The dump never ends the process; the step's subprocess deadline does that.

One limit: a thread that holds the GIL and never releases it stops the watchdog too,
as it stops every Python thread. The hangs this is for wait on a browser or a socket,
and those release the GIL.

Enable with `-p devtools.stack_watchdog -o stack_watchdog_timeout=60`.
"""

from __future__ import annotations

import faulthandler
import os
import sys
import threading
import time
from collections.abc import Generator

import pytest

TIMEOUT = "stack_watchdog_timeout"
UNSAFE = "faulthandler_timeout"


class Watchdog:
    """Dump every thread's stack once when an armed phase passes its limit."""

    def __init__(self, seconds: float, fd: int, worker: str) -> None:
        self.seconds = seconds
        self.fd = fd
        self.worker = worker
        self.dumps = 0
        self._condition = threading.Condition()
        self._armed: tuple[str, float] | None = None
        self._closed = False
        self._thread: threading.Thread | None = None

    def arm(self, label: str) -> None:
        """Start timing `label`; the thread starts on first use, so an xdist controller,
        which runs no tests, never starts one."""
        with self._condition:
            if self._thread is None:
                self._thread = threading.Thread(
                    target=self._watch, name="stack-watchdog", daemon=True
                )
                self._thread.start()
            self._armed = (label, time.monotonic())
            self._condition.notify()

    def disarm(self) -> None:
        with self._condition:
            self._armed = None
            self._condition.notify()

    def close(self) -> None:
        with self._condition:
            self._closed = True
            self._armed = None
            self._condition.notify()
            thread = self._thread
        if thread is not None:
            thread.join()

    def _watch(self) -> None:
        while (due := self._next_due()) is not None:
            self._dump(*due)

    def _next_due(self) -> tuple[str, float] | None:
        """Wait until the armed phase passes the limit, and disarm it, so each phase
        dumps at most once; None once closed."""
        with self._condition:
            while not self._closed:
                if self._armed is None:
                    self._condition.wait()
                    continue
                label, started = self._armed
                elapsed = time.monotonic() - started
                if elapsed < self.seconds:
                    self._condition.wait(self.seconds - elapsed)
                    continue
                self._armed = None
                return label, elapsed
            return None

    def _dump(self, label: str, elapsed: float) -> None:
        header = (
            f"\nStack watchdog: {label} has run {elapsed:.1f}s, past {self.seconds:g}s, "
            f"on {self.worker} (pid {os.getpid()}); every thread follows.\n"
        )
        os.write(self.fd, header.encode())
        faulthandler.dump_traceback(file=self.fd, all_threads=True)
        self.dumps += 1


WATCHDOG = pytest.StashKey[Watchdog]()


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addini(
        TIMEOUT,
        "Dump every thread's stack, from a thread that holds the GIL, once a test's "
        "setup, call or teardown has run this many seconds; 0 turns it off",
        default="0",
    )


def _stderr_fileno() -> int:
    """The descriptor pytest's faulthandler plugin writes to: xdist replaces
    `sys.stderr` with an object that has no descriptor, so fall back to the
    original."""
    try:
        fileno = sys.stderr.fileno()
    except AttributeError, ValueError:
        fileno = -1
    if fileno == -1:
        assert sys.__stderr__ is not None
        fileno = sys.__stderr__.fileno()
    return fileno


def pytest_configure(config: pytest.Config) -> None:
    seconds = float(config.getini(TIMEOUT) or 0)
    if seconds <= 0:
        return
    try:
        unsafe = float(config.getini(UNSAFE) or 0)
    except ValueError:  # `-p no:faulthandler` leaves the option unregistered
        unsafe = 0.0
    if unsafe > 0:
        raise pytest.UsageError(
            f"{UNSAFE} arms CPython's C watchdog, which can crash a process whose "
            f"threads come and go (D-523); set {TIMEOUT} alone"
        )
    worker_input = getattr(config, "workerinput", None)
    worker = str(worker_input["workerid"]) if worker_input is not None else "main"
    # Capture is suspended during configure, so this is the real stderr; a duplicate
    # keeps it when per-test capture later points descriptor 2 at a temporary file.
    config.stash[WATCHDOG] = Watchdog(seconds, os.dup(_stderr_fileno()), worker)


def pytest_unconfigure(config: pytest.Config) -> None:
    watchdog = config.stash.get(WATCHDOG, None)
    if watchdog is None:
        return
    watchdog.close()
    os.close(watchdog.fd)
    del config.stash[WATCHDOG]


def _timed(item: pytest.Item, phase: str) -> Generator[None, object, object]:
    watchdog = item.config.stash.get(WATCHDOG, None)
    if watchdog is None:
        return (yield)
    watchdog.arm(f"{item.nodeid} {phase}")
    try:
        return (yield)
    finally:
        watchdog.disarm()


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> Generator[None, object, object]:
    return (yield from _timed(item, "setup"))


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_call(item: pytest.Item) -> Generator[None, object, object]:
    return (yield from _timed(item, "call"))


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_teardown(item: pytest.Item) -> Generator[None, object, object]:
    return (yield from _timed(item, "teardown"))


@pytest.hookimpl(tryfirst=True)
def pytest_enter_pdb(config: pytest.Config) -> None:
    """No dump while someone sits at the debugger prompt, as with pytest's own timer."""
    watchdog = config.stash.get(WATCHDOG, None)
    if watchdog is not None:
        watchdog.disarm()
