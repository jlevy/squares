"""Observed CPU lower bounds for pytest phases, for diagnosis only.

Each setup, call and teardown phase records the increase in `resource.getrusage` for
this process and its reaped children. This separates CPU work from waiting for directly
observed work, but does not measure complete descendant CPU. It must not replace the
wall-clock thresholds in `sqpack.cli.validate`. That module requires the diagnostic
section to be present, but CPU readings never decide whether a test passes or fails:
reaping earlier work can charge an otherwise cheap call.

A waited-for `subprocess.run` child contributes its CPU. A multiprocessing forkserver
worker does not: the persistent server reaps that worker, so the pytest process's
`RUSAGE_CHILDREN` never receives its usage during the phase. Forkserver is Python 3.14's
Linux default. A CPU-heavy process-pool test can therefore report almost zero here even
when the test waits for every result. The plugin leaves process start methods unchanged.

These observations omit descendant work and do not provide complete attribution to
individual tests. A child started by an earlier phase can be charged when a later phase
reaps it, and background threads contribute to process CPU. The lower-bound label
describes incomplete process-tree accounting, not a bound on an isolated test's cost.
Under xdist each worker observes its own process counters; phase report user properties
carry those observations to the controller.

The report property, section heading and per-line token all name the lower-bound
contract. The section always explains the missing descendant accounting, including
when all entries are hidden. Its format is distinct from pytest's wall durations so the
existing gate cannot mistake these incomplete observations for its current measurement.
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
CPU_PROPERTY: Final = "observed_cpu_seconds_lower_bound"

#: The section header, chosen to contain pytest's own "slowest durations" nowhere: the
#: gate requires that string to prove pytest printed wall durations at all, and a header
#: that also matched would let a run with no wall section look like one that had it.
CPU_DURATIONS_HEADER: Final = "slowest observed cpu durations (lower bounds)"

#: Phase measurements for one item, keyed by phase name. Lives on the item rather than in
#: a module global so nothing has to be cleaned up between tests.
_CPU_STASH: Final = pytest.StashKey[dict[str, float]]()

#: pytest's own default for `--durations-min`, matched so the two sections hide the same
#: uninteresting tail.
_DEFAULT_MIN_SECONDS: Final = 0.005


def _cpu_seconds() -> float:
    """User plus system cpu charged to this process and to every child it has reaped.

    This excludes unreaped descendants and forkserver workers: their CPU belongs to
    the persistent server's child counter. It is not total CPU spent by a test.
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
        help="show N largest observed CPU lower bounds (0 for all); not total test CPU",
    )
    _ = group.addoption(
        "--cpu-durations-min",
        action="store",
        type=float,
        default=_DEFAULT_MIN_SECONDS,
        metavar="N",
        help="minimum observed CPU lower bound for a phase to be listed",
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

        The accounting limitation must remain visible even when the display threshold
        hides every entry. These observations cannot establish a test's total CPU cost.

        Printing unconditionally is also what lets `sqpack.cli.validate._require_durations`
        fail closed on this section: a run whose section vanished has to look different
        from a run whose section listed nothing, or a rename here would silently retire
        the ceiling that reads it.
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
        terminalreporter.write_line(
            "Incomplete descendant accounting; do not use for total CPU thresholds."
        )
        hidden = len(listed) - len(shown)
        if hidden > 0:
            terminalreporter.write_line(
                f"({hidden} CPU lower bounds < {minimum:g}s or beyond --cpu-durations hidden.)"
            )
        for seconds, when, nodeid in shown:
            terminalreporter.write_line(f"{seconds:02.2f}s cpu-lower-bound {when:<8} {nodeid}")


def pytest_configure(config: pytest.Config) -> None:
    """Register the collecting half only where reports are aggregated.

    Under xdist the hooks above run in every worker and this object exists in every
    process, but only the controller's `pytest_runtest_logreport` sees the whole run, and
    only the controller writes a terminal summary. Registering it everywhere is harmless
    and keeps the plugin symmetric.
    """
    config.pluginmanager.register(CpuDurations(), "cpu-durations-collector")
