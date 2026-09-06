"""Per-test CPU-time measurement, as a pytest plugin.

The two-sided per-test discipline in `sqpack.cli.validate` -- a ceiling that pushes an
expensive test off the pull-request surface and a floor that pulls a cheap one back onto
it -- reads pytest's own `--durations` section, which is wall clock.
Wall clock on a shared runner measures the runner as much as the test.
The evidence is in the docstring on `QUICK_TEST_CEILING_SECONDS`: four consecutive runs
of one surface at one commit reported 19, then 5, then 1, then 3 tests over the ceiling,
a different cast each time and every one of them 1.5s to 3s on a quiet box.
The constant absorbed that by rising to 12.0, six times the 2s threshold it is supposed
to enforce, which is a guard that no longer guards.

CPU time is the contention-independent measurement that fixes the threshold rather than
the constant.
A test's wall time grows when a neighbour takes the core away from it; the cpu-seconds it
charges for its own work do not move, because the scheduler is dividing the same work
into the same instructions either way.

This plugin measures each `setup`, `call` and `teardown` phase with `resource.getrusage`,
attaches the result to the phase's report as a user property, and prints a
`slowest cpu durations` section shaped like pytest's own so the gate can parse it the same
way. The section is deliberately *not* byte-compatible with pytest's: the `cpu` token
after the seconds keeps `sqpack.cli.validate._DURATION_LINE` from reading both sections as
one list when both are printed.

Two design decisions are load bearing.

**Children are counted.** `_cpu_seconds` sums `RUSAGE_SELF` and `RUSAGE_CHILDREN`, so a
test whose work happens in a subprocess is charged for it.
Excluding children would be the more literal reading of "this test's cpu time" and it
would put a hole in the middle of the guard: this suite shells out to cargo, to
standalone verifiers and to `sqpack` console scripts, and every one of those tests would
measure near zero cpu and pass a ceiling it should fail.
`RUSAGE_CHILDREN` accrues only on reaping, which `subprocess.run` and friends do before
returning, so the cost lands inside the phase that paid it.
Two consequences are worth stating rather than discovering: a child that a phase spawns
and does not wait for is billed to whichever later phase reaps it, exactly as its wall
time is today; and a child that is itself parallel -- `cargo build -j 4` -- charges the
cpu of all its cores, so it can read *above* its own wall time.
That is the right direction for a ceiling whose subject is what the runner pays.

**Measurement is per process, which is what makes xdist tractable.** Each xdist worker is
its own process, so `RUSAGE_SELF` there is that worker's tests and nobody else's, and the
neighbouring workers -- the contention this exists to reject -- are invisible to it by
construction. The controller aggregates through `user_properties`, which pytest already
serialises across the worker boundary.
"""

from __future__ import annotations

import resource
from typing import TYPE_CHECKING, Final

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator

    from _pytest.terminal import TerminalReporter

#: The user-property name each phase's cpu measurement travels under, from the worker
#: that ran the test to the controller that prints the section.
CPU_PROPERTY: Final = "cpu_seconds"

#: The section header, chosen to contain pytest's own "slowest durations" nowhere: the
#: gate requires that string to prove pytest printed wall durations at all, and a header
#: that also matched would let a run with no wall section look like one that had it.
CPU_DURATIONS_HEADER: Final = "slowest cpu durations"

#: Phase measurements for one item, keyed by phase name. Lives on the item rather than in
#: a module global so nothing has to be cleaned up between tests.
_CPU_STASH: Final = pytest.StashKey[dict[str, float]]()

#: pytest's own default for `--durations-min`, matched so the two sections hide the same
#: uninteresting tail.
_DEFAULT_MIN_SECONDS: Final = 0.005


def _cpu_seconds() -> float:
    """User plus system cpu charged to this process and to every child it has reaped.

    Both halves are needed. `RUSAGE_SELF` alone misses the subprocess work that several
    of this suite's most expensive tests consist entirely of; `RUSAGE_CHILDREN` alone
    misses everything that runs in-process, which is most of it.
    Both counters are monotone within a process, so a difference of two readings is never
    negative and never has to be clamped.
    """
    total = 0.0
    for who in (resource.RUSAGE_SELF, resource.RUSAGE_CHILDREN):
        usage = resource.getrusage(who)
        total += usage.ru_utime + usage.ru_stime
    return total


def _record(item: pytest.Item, phase: str, seconds: float) -> None:
    measured = item.stash.get(_CPU_STASH, None)
    if measured is None:
        measured = {}
        item.stash[_CPU_STASH] = measured
    measured[phase] = seconds


def _timed(item: pytest.Item, phase: str) -> Generator[None]:
    """Charge one runtest phase, whether it returns, raises, or is torn down early."""
    start = _cpu_seconds()
    try:
        return (yield)
    finally:
        _record(item, phase, _cpu_seconds() - start)


def pytest_addoption(parser: pytest.Parser) -> None:
    group = parser.getgroup("terminal reporting")
    _ = group.addoption(
        "--cpu-durations",
        action="store",
        type=int,
        default=0,
        metavar="N",
        help="show the N slowest test phases by cpu time (0 for all)",
    )
    _ = group.addoption(
        "--cpu-durations-min",
        action="store",
        type=float,
        default=_DEFAULT_MIN_SECONDS,
        metavar="N",
        help="minimum cpu seconds for a phase to be listed by --cpu-durations",
    )


@pytest.hookimpl(wrapper=True)
def pytest_runtest_setup(item: pytest.Item) -> Generator[None]:
    return (yield from _timed(item, "setup"))


@pytest.hookimpl(wrapper=True)
def pytest_runtest_call(item: pytest.Item) -> Generator[None]:
    return (yield from _timed(item, "call"))


@pytest.hookimpl(wrapper=True)
def pytest_runtest_teardown(item: pytest.Item) -> Generator[None]:
    return (yield from _timed(item, "teardown"))


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    """Attach the phase's cpu measurement to the report that carries it to the controller.

    A user property is the one channel pytest already serialises across the xdist worker
    boundary, so the same code path serves `-n 0` and `-n 8`.
    """
    report = yield
    measured = item.stash.get(_CPU_STASH, None)
    if measured is not None and (seconds := measured.get(call.when)) is not None:
        report.user_properties.append((CPU_PROPERTY, seconds))
    return report


class CpuDurations:
    """Collects each phase's cpu measurement on the controller and prints the section."""

    def __init__(self) -> None:
        self.entries: list[tuple[float, str, str]] = []

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None:
        for name, value in report.user_properties:
            if name == CPU_PROPERTY and isinstance(value, float | int):
                self.entries.append((float(value), report.when or "call", report.nodeid))

    def pytest_terminal_summary(
        self, terminalreporter: TerminalReporter, config: pytest.Config
    ) -> None:
        """Always print the header, even with nothing to list.

        The gate's `_require_durations` fails closed on a missing header: a run whose
        section vanished has to look different from a run whose section was empty, or a
        renamed section would silently retire the ceiling.
        """
        # `getoption` is typed `Any`, and returns `None` for an option some other
        # invocation of this plugin did not register; the defaults are restated rather
        # than trusted.
        limit_option = config.getoption("--cpu-durations", default=None)
        minimum_option = config.getoption("--cpu-durations-min", default=None)
        limit = 0 if limit_option is None else int(limit_option)
        minimum = _DEFAULT_MIN_SECONDS if minimum_option is None else float(minimum_option)
        listed = sorted(self.entries, reverse=True)
        shown = [entry for entry in listed if entry[0] >= minimum]
        if limit > 0:
            shown = shown[:limit]
        terminalreporter.write_sep("=", CPU_DURATIONS_HEADER)
        hidden = len(listed) - len(shown)
        if hidden > 0:
            terminalreporter.write_line(
                f"({hidden} cpu durations < {minimum:g}s or beyond --cpu-durations hidden.)"
            )
        for seconds, when, nodeid in shown:
            terminalreporter.write_line(f"{seconds:02.2f}s cpu {when:<8} {nodeid}")


def pytest_configure(config: pytest.Config) -> None:
    """Register the collecting half only where reports are aggregated.

    Under xdist the hooks above run in every worker and this object exists in every
    process, but only the controller's `pytest_runtest_logreport` sees the whole run, and
    only the controller writes a terminal summary. Registering it everywhere is harmless
    and keeps the plugin symmetric.
    """
    config.pluginmanager.register(CpuDurations(), "cpu-durations-collector")
