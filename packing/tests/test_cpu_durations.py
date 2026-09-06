#!/usr/bin/env python3
"""Observed CPU diagnostics, including the forkserver accounting limitation.

Small generated workloads distinguish CPU work in this process and a direct child from
waiting. A separate forkserver workload verifies that incomplete observations label
both their display and serialized report property as lower bounds. These diagnostics
are not wired into the validation gate's total-cost thresholds.
"""

# Exercise the CLI gate using real diagnostic output.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from devtools.cpu_durations import CPU_DURATIONS_HEADER
from sqpack.cli import validate

PROJECT_ROOT = Path(__file__).resolve().parents[1]

#: The diagnostic section, distinct from the wall section the gate reads.
_CPU_LINE = re.compile(
    r"^(?P<seconds>\d+\.\d+)s\s+cpu-lower-bound\s+(?P<phase>setup|call|teardown)\s+(?P<node>\S+)$"
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

_FORKSERVER_SUITE = """
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor

def _burn():
    start = time.process_time()
    while time.process_time() - start < float(os.environ["CPU_DURATIONS_PROBE_BUDGET"]):
        pass
    return time.process_time() - start

def test_forkserver_work_runs():
    with ProcessPoolExecutor(
        max_workers=1, mp_context=multiprocessing.get_context("forkserver")
    ) as pool:
        assert pool.submit(_burn).result() >= float(os.environ["CPU_DURATIONS_PROBE_BUDGET"])
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
        timeout=30,
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
    """A direct waited-for child's CPU contributes to the observed lower bound."""
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
    """An empty section must still disclose the diagnostic's incomplete accounting."""
    output = _run_under_the_plugin(tmp_path, _EMPTY_SUITE, "--cpu-durations-min=99")
    assert CPU_DURATIONS_HEADER in output
    assert "Incomplete descendant accounting" in output
    assert _call_phases(_CPU_LINE, output) == {}


def test_forkserver_measurements_are_explicit_lower_bounds(tmp_path: Path) -> None:
    """Forkserver reaps the worker; pytest's child counter cannot see its CPU.

    Verify real worker work, then require the incomplete accounting to identify itself
    in both display and serialized reports. Do not bound controller overhead: a busy
    machine can spend more CPU starting the pool than this short worker spends burning.
    """
    report = tmp_path / "report.xml"
    output = _run_under_the_plugin(
        tmp_path,
        _FORKSERVER_SUITE,
        "--cpu-durations-min=0",
        f"--junitxml={report}",
    )
    assert "1 passed" in output
    assert "slowest observed cpu durations (lower bounds)" in output
    assert "cpu-lower-bound call" in output
    assert "Incomplete descendant accounting; do not use for total CPU thresholds." in output
    names = {element.attrib["name"] for element in ET.parse(report).iter("property")}
    assert "observed_cpu_seconds_lower_bound" in names
    assert "cpu_seconds" not in names


_SETUP_CHILD_SUITE = r"""
import subprocess
import sys

import pytest


@pytest.fixture(scope="module")
def completed_setup_child():
    child = subprocess.Popen(
        [sys.executable, "-c",
         "import os, time\n"
         "budget = float(os.environ['CPU_DURATIONS_PROBE_BUDGET'])\n"
         "start = time.process_time()\n"
         "while time.process_time() - start < budget: pass\n"
         "print('ready', flush=True)"],
        stdout=subprocess.PIPE,
        text=True,
    )
    assert child.stdout.readline() == "ready\n"
    yield child
    child.wait(timeout=10)


def test_only_reaps_setup_work(completed_setup_child):
    assert completed_setup_child.wait(timeout=10) == 0
"""


def test_reaping_setup_cpu_does_not_fail_a_cheap_call(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Synchronize on finished setup work before reaping it in a real test call.

    RUSAGE_CHILDREN increases in call even though the work preceded it. Lower only the
    diagnostic display threshold to keep the regression short; retain the real wall gate.
    """
    output = _run_under_the_plugin(tmp_path, _SETUP_CHILD_SUITE, "--cpu-durations-min=0")
    cpu = _call_phases(_CPU_LINE, output)
    assert cpu["test_only_reaps_setup_work"] >= 0.8 * _BUDGET_SECONDS
    monkeypatch.setattr(validate, "QUICK_TEST_CPU_REPORT_SECONDS", 0.1)
    monkeypatch.setattr(validate, "_run", lambda *_args, **_kwargs: output)
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )
    assert validate._fast_tests(context) == output  # noqa: SLF001 - exercise the real gate
