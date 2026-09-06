#!/usr/bin/env python3
"""The per-test cpu measurement, checked against the one thing it has to get right.

Three tests are generated and run under the plugin: one that burns cpu in process, one
that burns the same cpu inside a child process, and one that only waits.
The claim the whole measurement rests on is the contrast between the first and the last
-- work is charged, waiting is not -- and the claim that decides whether the measurement
is usable at all is the middle one, because this suite's most expensive tests are
expensive in a subprocess and a measurement that could not see them would leave a hole in
the ceiling exactly where the cost is.

The budget is deliberately small.  These assertions need two decimal places of printed
seconds to separate "did the work" from "did not", not a long run, and this test itself
lives on the pull-request surface under the ceiling it is here to defend.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

from devtools.cpu_durations import CPU_DURATIONS_HEADER

PROJECT_ROOT = Path(__file__).resolve().parents[1]

#: The section the gate reads.
_CPU_LINE = re.compile(
    r"^(?P<seconds>\d+\.\d+)s\s+cpu\s+(?P<phase>setup|call|teardown)\s+(?P<node>\S+)$"
)
#: `sqpack.cli.validate._DURATION_LINE`, transcribed rather than imported.  The two
#: sections are printed into one stream, so the wall parser must not match a cpu line; a
#: copy here fails when either format drifts, where an import would follow one of them
#: silently.
_WALL_LINE = re.compile(
    r"^(?P<seconds>\d+\.\d+)s\s+(?P<phase>setup|call|teardown)\s+(?P<node>\S+)$"
)

#: Seconds of cpu the burning cases spend, and seconds of wall the waiting case spends.
_BUDGET_SECONDS = 0.25
#: The environment variable the generated suite reads its budget from, so the generated
#: source needs no interpolation and stays readable as source.
_BUDGET_VARIABLE = "CPU_DURATIONS_PROBE_BUDGET"

_PROBE_SUITE = """
import os
import subprocess
import sys
import time

BUDGET = float(os.environ["CPU_DURATIONS_PROBE_BUDGET"])
CHILD = (
    "import os, time\\n"
    "end = time.process_time() + float(os.environ['CPU_DURATIONS_PROBE_BUDGET'])\\n"
    "while time.process_time() < end:\\n"
    "    pass\\n"
)


def _burn(seconds):
    end = time.process_time() + seconds
    while time.process_time() < end:
        pass


def test_burns_cpu_in_process():
    _burn(BUDGET)


def test_burns_cpu_in_a_child():
    subprocess.run([sys.executable, "-c", CHILD], check=True)


def test_only_waits():
    time.sleep(BUDGET)
"""

_EMPTY_SUITE = """
def test_costs_nothing():
    assert True
"""


def _run_under_the_plugin(directory: Path, suite: str, *extra: str) -> str:
    (directory / "test_probe.py").write_text(suite, encoding="utf-8")
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            "-p",
            "no:cacheprovider",
            "-p",
            "devtools.cpu_durations",
            str(directory),
            "--durations=0",
            "--durations-min=0",
            *extra,
        ],
        capture_output=True,
        text=True,
        check=False,
        cwd=PROJECT_ROOT,
        env={
            **os.environ,
            "PYTHONPATH": str(PROJECT_ROOT),
            _BUDGET_VARIABLE: repr(_BUDGET_SECONDS),
        },
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr
    return completed.stdout


@pytest.fixture(scope="module")
def probe_output(tmp_path_factory: pytest.TempPathFactory) -> str:
    """One run of the generated suite, shared so the burning is paid for once."""
    directory = tmp_path_factory.mktemp("cpu_durations_probe")
    return _run_under_the_plugin(
        directory, _PROBE_SUITE, "--cpu-durations=0", "--cpu-durations-min=0"
    )


def _call_phases(pattern: re.Pattern[str], output: str) -> dict[str, float]:
    return {
        match["node"].rsplit("::", 1)[-1]: float(match["seconds"])
        for line in output.splitlines()
        if (match := pattern.match(line.strip())) and match["phase"] == "call"
    }


def test_cpu_time_charges_work_and_not_waiting(probe_output: str) -> None:
    """The whole claim: the burner is measured near its cost, the waiter near zero."""
    cpu = _call_phases(_CPU_LINE, probe_output)
    wall = _call_phases(_WALL_LINE, probe_output)
    assert sorted(cpu) == sorted(wall)

    assert cpu["test_burns_cpu_in_process"] >= 0.8 * _BUDGET_SECONDS
    assert cpu["test_only_waits"] <= 0.25 * _BUDGET_SECONDS
    # Without the contrast the first assertion says nothing: the waiting case has to be
    # expensive on the clock and cheap in cpu at the same time, which is the whole
    # difference between the two measurements.
    assert wall["test_only_waits"] >= 0.8 * _BUDGET_SECONDS
    assert wall["test_only_waits"] >= 4 * cpu["test_only_waits"]


def test_cpu_spent_in_a_child_process_is_charged_to_the_test(probe_output: str) -> None:
    """`RUSAGE_CHILDREN` is counted, so shelling out is not a way around the ceiling."""
    cpu = _call_phases(_CPU_LINE, probe_output)
    assert cpu["test_burns_cpu_in_a_child"] >= 0.8 * _BUDGET_SECONDS
    assert cpu["test_burns_cpu_in_a_child"] >= 4 * cpu["test_only_waits"]


def test_the_cpu_section_is_not_read_as_the_wall_section(probe_output: str) -> None:
    """Both sections print into one stream, so the gate must be able to tell them apart."""
    cpu_lines = [
        stripped
        for line in probe_output.splitlines()
        if _CPU_LINE.match(stripped := line.strip())
    ]
    assert cpu_lines != []
    assert [line for line in cpu_lines if _WALL_LINE.match(line)] == []


def test_the_section_is_printed_even_when_it_lists_nothing(tmp_path: Path) -> None:
    """Fail closed: a vanished section has to look different from an empty one.

    `sqpack.cli.validate._require_durations` refuses a lane whose durations section it
    could not find, so a renamed or dropped section reports itself instead of silently
    retiring the ceiling forever.  That only works if an empty section still prints.
    """
    output = _run_under_the_plugin(tmp_path, _EMPTY_SUITE, "--cpu-durations-min=99")
    assert CPU_DURATIONS_HEADER in output
    assert _call_phases(_CPU_LINE, output) == {}
