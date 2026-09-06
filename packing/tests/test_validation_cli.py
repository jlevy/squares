"""Behavioral tests for the self-documenting packing validation command."""

# These contracts deliberately exercise the CLI module's internal functional seams.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import io
import os
import shlex
import signal
import subprocess
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pytest

from sqpack import gate_budgets
from sqpack.cli import validate
from sqpack.cli.validate import main
from sqpack.yamlio import safe_load

WORKFLOW = Path(__file__).resolve().parents[2] / ".github/workflows/packing-validation.yml"
"""The gate's own workflow, read by the test that keeps its two post-merge jobs a
partition of `STEPS`. Repository-relative from `packing/tests/`, so two levels up."""


def _invoke(*arguments: str) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        status = main(list(arguments))
    return status, stdout.getvalue(), stderr.getvalue()


def _process_is_running(pid: int) -> bool:
    if os.name == "nt":
        result = subprocess.run(
            ("tasklist", "/FI", f"PID eq {pid}", "/FO", "CSV", "/NH"),
            capture_output=True,
            text=True,
            check=False,
        )
        return f'"{pid}"' in result.stdout
    result = subprocess.run(
        ("ps", "-o", "stat=", "-p", str(pid)),
        capture_output=True,
        text=True,
        check=False,
    )
    state = result.stdout.strip()
    return result.returncode == 0 and bool(state) and not state.startswith("Z")


@pytest.mark.slow
@pytest.mark.skipif(os.name == "nt", reason="bounded tree mode fails closed on Windows")
def test_run_timeout_terminates_child_and_reports_captured_output(tmp_path: Path) -> None:
    child_pid_path = tmp_path / "child.pid"
    child_ready_path = tmp_path / "child.ready"
    leaked_path = tmp_path / "child-leaked"
    child_script = "\n".join(
        (
            "import os",
            "import signal",
            "import time",
            "from pathlib import Path",
            "signal.signal(signal.SIGTERM, signal.SIG_IGN)",
            f"Path({str(child_pid_path)!r}).write_text(str(os.getpid()), encoding='utf-8')",
            f"Path({str(child_ready_path)!r}).write_text('ready', encoding='utf-8')",
            "time.sleep(2)",
            f"Path({str(leaked_path)!r}).write_text('leaked', encoding='utf-8')",
            "time.sleep(30)",
        )
    )
    parent_script = "\n".join(
        (
            "import subprocess",
            "import sys",
            "import time",
            f"child_script = {child_script!r}",
            "child = subprocess.Popen(",
            "    [sys.executable, '-c', child_script],",
            "    stdout=subprocess.DEVNULL,",
            "    stderr=subprocess.DEVNULL,",
            ")",
            f"ready_path = __import__('pathlib').Path({str(child_ready_path)!r})",
            "while not ready_path.exists():",
            "    time.sleep(0.01)",
            "print('parent captured output', flush=True)",
            "time.sleep(30)",
        )
    )
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
    )

    started = time.monotonic()
    with pytest.raises(validate.StepFailureError) as captured:
        validate._run(
            context,
            (sys.executable, "-c", parent_script),
            cwd=tmp_path,
            timeout_seconds=0.25,
        )
    elapsed = time.monotonic() - started

    assert 1 <= elapsed < 3
    assert "command timed out after 0.25 seconds" in str(captured.value)
    assert "parent captured output" in str(captured.value)
    child_pid = int(child_pid_path.read_text(encoding="utf-8"))
    deadline = time.monotonic() + 1
    while _process_is_running(child_pid) and time.monotonic() < deadline:
        time.sleep(0.01)
    assert not _process_is_running(child_pid)
    time.sleep(1)
    assert not leaked_path.exists()


@pytest.mark.skipif(os.name == "nt", reason="bounded tree mode fails closed on Windows")
def test_run_ordinary_action_inherits_context_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")
    engine = tmp_path / "slow-engine"
    engine.write_text(
        f"#!{sys.executable}\nimport time\ntime.sleep(1)\n",
        encoding="utf-8",
    )
    engine.chmod(0o755)
    monkeypatch.setattr(validate, "ENGINE", engine)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
        timeout_seconds=0.05,
    )
    production_step = next(
        step for step in validate.STEPS if step.name == "search engine (sqsearch)"
    )
    step = validate.Step(production_step.name, production_step.action)
    summary = validate._run_selected([step], context, [])
    assert summary.results[0].status == "failed"
    assert "timed out after 0.05 seconds" in summary.results[0].reason


@pytest.mark.slow
@pytest.mark.skipif(os.name == "nt", reason="bounded tree mode fails closed on Windows")
def test_run_selected_interrupt_stops_detached_production_process(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")
    pid_path = tmp_path / "engine.pid"
    leaked_path = tmp_path / "engine-leaked"
    engine = tmp_path / "interrupt-engine"
    engine.write_text(
        "\n".join(
            (
                f"#!{sys.executable}",
                "import os",
                "import signal",
                "import time",
                "from pathlib import Path",
                "signal.signal(signal.SIGTERM, signal.SIG_IGN)",
                f"Path({str(pid_path)!r}).write_text(str(os.getpid()), encoding='utf-8')",
                "os.kill(os.getppid(), signal.SIGINT)",
                "time.sleep(2)",
                f"Path({str(leaked_path)!r}).write_text('leaked', encoding='utf-8')",
                "time.sleep(30)",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    engine.chmod(0o755)
    monkeypatch.setattr(validate, "ENGINE", engine)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
        timeout_seconds=10,
    )
    production_step = next(
        step for step in validate.STEPS if step.name == "search engine (sqsearch)"
    )
    step = validate.Step(production_step.name, production_step.action)

    started = time.monotonic()
    with pytest.raises(KeyboardInterrupt):
        validate._run_selected([step], context, [])
    elapsed = time.monotonic() - started

    assert 1 <= elapsed < 5
    assert pid_path.exists()
    pid = int(pid_path.read_text(encoding="utf-8"))
    deadline = time.monotonic() + 1
    while _process_is_running(pid) and time.monotonic() < deadline:
        time.sleep(0.01)
    assert not _process_is_running(pid)
    time.sleep(1)
    assert not leaked_path.exists()


@pytest.mark.skipif(os.name == "nt", reason="bounded tree mode fails closed on Windows")
def test_process_registry_rejects_registration_after_stop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    signals: list[tuple[int, int]] = []
    monkeypatch.setattr(validate, "PROCESS_TERMINATION_GRACE_SECONDS", 0)
    monkeypatch.setattr(
        validate.os,
        "killpg",
        lambda pid, sent_signal: signals.append((pid, sent_signal)),
    )
    registry = validate._ProcessRegistry()
    registry.stop()

    with pytest.raises(validate.StepFailureError, match="rejected new subprocess"):
        registry.register(12345)
    assert signals == [(12345, signal.SIGKILL)]


def test_process_registry_stop_returns_without_an_empty_grace_sleep(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr(validate.time, "sleep", sleeps.append)

    validate._ProcessRegistry().stop()

    assert sleeps == []


@pytest.mark.skipif(os.name == "nt", reason="bounded tree mode fails closed on Windows")
def test_run_drains_rejected_process_output(monkeypatch: pytest.MonkeyPatch) -> None:
    class RejectedProcess:
        pid = 12345
        stdout = io.StringIO()
        returncode = -signal.SIGKILL
        communicated = False

        def communicate(self, *, timeout: float) -> tuple[str, None]:
            assert timeout == validate.PROCESS_TERMINATION_GRACE_SECONDS
            self.communicated = True
            return "", None

    process = RejectedProcess()
    monkeypatch.setattr(validate.subprocess, "Popen", lambda *_args, **_kwargs: process)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
    )
    context.processes.stop()

    with pytest.raises(validate.StepFailureError, match="rejected new subprocess"):
        validate._run(context, (sys.executable, "-c", "pass"))

    assert process.communicated


@pytest.mark.skipif(os.name == "nt", reason="bounded tree mode fails closed on Windows")
def test_run_explicit_smaller_timeout_wins() -> None:
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
        timeout_seconds=1,
    )
    with pytest.raises(validate.StepFailureError, match=r"timed out after 0\.05 seconds"):
        validate._run(
            context,
            (sys.executable, "-c", "import time; time.sleep(1)"),
            timeout_seconds=0.05,
        )


def test_timeout_override_requires_positive_finite_seconds() -> None:
    for value in ("", "0", "-1", "nan", "inf", "not-a-number"):
        status, _, stderr = _invoke("--timeout-seconds", value, "--list")
        assert status == 2
        assert "--timeout-seconds" in stderr
        assert "positive number of seconds" in stderr


def test_list_is_read_only_and_exposes_fast_and_full_check_groups() -> None:
    status, stdout, stderr = _invoke("--list")

    assert status == 0
    assert stderr == ""
    assert "fast behavioral tests [fast, suite]" in stdout
    assert "exhaustive exact behavioral tests [full]" in stdout
    assert "soundness perimeter [fast, checks, engine]" in stdout


def test_list_applies_the_same_fast_and_name_filters_as_execution() -> None:
    status, stdout, stderr = _invoke("--list", "--fast")

    assert status == 0
    assert stderr == ""
    assert "fast behavioral tests [fast, suite]" in stdout
    assert "exhaustive exact behavioral tests" not in stdout
    assert "negative controls" not in stdout

    status, stdout, stderr = _invoke("--list", "--only", "negative control")

    assert status == 0
    assert stderr == ""
    assert stdout.splitlines() == ["negative controls [full]"]


def test_skip_is_only_read_the_other_way_round() -> None:
    """`--skip` selects a tier and removes named steps, leaving the rest untouched.

    The flag exists because two CI jobs cannot divide the gate with `--only` alone: the
    job that keeps everything but one step would have to name the other sixty, and the
    step that got left out of that list is a step nobody runs.
    """
    status, stdout, stderr = _invoke("--list", "--skip", "exhaustive exact behavioral tests")

    assert status == 0
    assert stderr == ""
    listed = stdout.splitlines()
    assert len(listed) == len(validate.STEPS) - 1
    assert not any("exhaustive exact" in line for line in listed)
    assert "fast behavioral tests [fast, suite]" in stdout


def test_a_skip_naming_no_step_is_refused_rather_than_ignored() -> None:
    """The asymmetry with `--only` is the point.

    An `--only` that matches nothing empties the selection and announces itself. A
    `--skip` that matches nothing leaves the selection whole, so the run merely does more
    than it meant to -- safe for the verdict and silent about the fact that the name it
    was written against has moved. The workflow's post-merge split depends on one such
    name, so a rename has to fail the job that carries it rather than quietly cost that
    job half an hour.
    """
    status, _, stderr = _invoke("--list", "--skip", "not-a-real-step")

    assert status == 2
    assert "matched no validation step" in stderr
    assert "packing-validate --list" in stderr


def test_a_skip_outside_the_selected_tier_is_a_no_op_not_an_error() -> None:
    """Patterns are matched against every declared step, not against this tier.

    Whether a real step is in the tier someone asked for is the tier's business. Refusing
    `--fast --skip "negative controls"` would make the flag depend on which tier it was
    combined with, which is a worse contract than one that removes nothing.
    """
    status, stdout, stderr = _invoke("--list", "--fast", "--skip", "negative controls")

    assert status == 0
    assert stderr == ""
    assert len(stdout.splitlines()) == len([step for step in validate.STEPS if step.fast])


def test_a_skip_that_empties_an_only_selection_names_the_skip() -> None:
    """The refusal has to name the narrowing that caused it, not the other one."""
    status, _, stderr = _invoke("--only", "negative controls", "--skip", "negative controls")

    assert status == 2
    assert "--skip 'negative controls' left no validation step to run" in stderr


def test_fast_behavioral_step_excludes_exhaustive_exact_tests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: tuple[str, ...] | None = None

    def capture(context: validate.Context, command: tuple[str, ...], **_kwargs: object) -> str:
        del context
        nonlocal observed
        observed = command
        return "==== slowest durations ====\n(1904 durations < 5.00s hidden.)"

    monkeypatch.setattr(validate, "_run", capture)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
    )

    monkeypatch.setattr(validate, "_pytest_workers", lambda _jobs: 4)

    validate._fast_tests(context)

    assert observed == (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests",
        "-m",
        "not exhaustive_exact and not slow",
        "-n",
        "4",
        "--durations=0",
        f"--durations-min={validate.QUICK_TEST_CEILING_SECONDS:g}",
    )


def test_the_quick_lane_asks_for_no_xdist_worker_on_a_single_core_machine(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`-n 1` is a subprocess and a protocol for no concurrency, so it is worse than none.

    The lane sizes itself to what the box has left rather than to what it has, so one
    worker is reached whenever the other steps have claimed everything -- and on a machine
    with one core there is nothing to divide anyway. Either way, asking xdist for a single
    worker would pay the fork and the marshalling for no concurrency.
    """
    monkeypatch.setattr(validate, "_pytest_workers", lambda _jobs: 1)

    command = validate._quick_lane_command(1)

    assert "-n" not in command
    assert command[-2:] == (
        "--durations=0",
        f"--durations-min={validate.QUICK_TEST_CEILING_SECONDS:g}",
    )


def test_the_quick_lane_worker_count_follows_the_machine_and_is_never_zero(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """It is what the box has left -- `cpus - jobs + 1`, this step being one of the jobs.

    Asking for every cpu was right while `--jobs 2` hid every other step under this one.
    At `--jobs 3` it oversubscribes, and the cost lands on the per-test ceiling: the run
    that forced this change reported 19 tests between 5.4s and 8.3s against a 5s ceiling,
    none of them slow tests, all of them merely contended. A ceiling measured under
    oversubscription sends tests to the deep surface for having noisy neighbours.
    """
    monkeypatch.setattr(os, "process_cpu_count", lambda: 8)
    assert validate._pytest_workers(1) == 8
    assert validate._pytest_workers(3) == 6
    assert validate._pytest_workers(8) == 1
    # More jobs than cpus is still one worker, never zero and never negative.
    assert validate._pytest_workers(99) == 1

    monkeypatch.setattr(os, "process_cpu_count", lambda: None)
    assert validate._pytest_workers(1) == validate.DEFAULT_CPU_COUNT


def test_slow_behavioral_step_selects_exactly_what_the_quick_lane_defers(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: tuple[str, ...] | None = None

    def capture(context: validate.Context, command: tuple[str, ...], **_kwargs: object) -> str:
        del context
        nonlocal observed
        observed = command
        return "==== slowest durations ====\n(0 durations < 0.005s hidden.)"

    monkeypatch.setattr(validate, "_run", capture)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
    )

    validate._slow_tests(context)

    assert observed == (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests",
        "-m",
        "slow and not exhaustive_exact",
        "--durations=0",
        "--durations-min=0",
    )


def test_an_empty_slow_lane_passes_and_a_real_failure_does_not(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The lane's membership is decided by a ceiling, so it may legitimately be empty.

    pytest exits 5 when every test is deselected. Failing the deep surface on that would
    make "keep one slow test around" the cheapest fix, which is a worse gate than the one
    the failure was meant to protect. Every other non-zero exit still fails.
    """

    def deselected(*_args: object, **_kwargs: object) -> str:
        raise validate.StepFailureError("command exited 5: pytest\n2153 deselected in 5.32s")

    def broken(*_args: object, **_kwargs: object) -> str:
        raise validate.StepFailureError("command exited 1: pytest\n1 failed, 3 passed")

    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )

    monkeypatch.setattr(validate, "_run", deselected)
    assert "no test is deferred" in validate._slow_tests(context)

    monkeypatch.setattr(validate, "_run", broken)
    with pytest.raises(validate.StepFailureError):
        validate._slow_tests(context)


#: Node ids taken verbatim from this project's own pytest, not invented: a parametrized
#: id is `ascii_escaped`, so a parameter carrying `[`, `]` or `::` lands in the id
#: unchanged. Each one breaks a plausible shortcut -- cutting at the first `[`, cutting at
#: the last `[`, splitting on the last `::` -- which is why they are pinned here.
_REAL_NODE_IDS = {
    "tests/test_probe.py::test_plain": "tests/test_probe.py::test_plain",
    "tests/test_probe.py::test_param[plain]": "tests/test_probe.py::test_param",
    "tests/test_probe.py::test_param[a-b]": "tests/test_probe.py::test_param",
    "tests/test_probe.py::test_param[x::y]": "tests/test_probe.py::test_param",
    "tests/test_probe.py::test_param[with[brackets]]": "tests/test_probe.py::test_param",
    "tests/test_probe.py::test_multi[q-1]": "tests/test_probe.py::test_multi",
    "tests/test_probe.py::TestClass::test_method[z[1]]": (
        "tests/test_probe.py::TestClass::test_method"
    ),
}


def test_a_node_id_is_split_from_its_parametrization_however_it_is_spelled() -> None:
    """The marker floor groups by function, so the grammar of a node id is load-bearing.

    An id that grouped wrongly would either split one function into several -- and then
    report a case that is not the slowest -- or merge two functions and hide one. Both
    turn the floor into a coin toss, so the ids are pinned rather than assumed.
    """
    for node, function in _REAL_NODE_IDS.items():
        assert validate._test_function(node) == function

    # An id the grammar does not recognise is its own group rather than a crash or a
    # silent drop, so an unfamiliar shape makes the floor stricter, never blind.
    assert validate._test_function("not-a-node-id") == "not-a-node-id"


def test_the_marker_floor_is_measured_per_function_and_not_per_parametrization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A `slow` marker costs what its slowest case costs, because it defers all of them.

    The marker is a decorator on a `def`. A parametrized function therefore leaves the
    pull-request surface whole, which is why the registry in
    `test_the_slow_marker_is_declared_only_by_measured_nodes` counts 62 functions and 92
    collected tests. A floor applied per node asks a question the marker cannot answer:
    it reports the cheap case of an expensive function as a marker to delete, and
    deleting it would drag the expensive case back onto the pull-request surface.

    So this is two-sided, and both sides are needed. `test_two_sided` and `test_method`
    each have a cheap case under the floor and an expensive one far above it, and neither
    may be reported -- the per-node rule reports both. `test_retired` has no case above
    the floor and must still be reported -- a rule that simply stopped looking would pass
    this half of the test while losing the check entirely. Its 2.90s *setup* is over the
    floor and is ignored, because the floor is a `call`-phase rule.
    """
    durations = """
        ======================== slowest durations ========================
        12.40s call     tests/test_a.py::test_two_sided[expensive]
        4.10s call      tests/test_a.py::TestGroup::test_method[z[1]]
        2.90s setup     tests/test_b.py::test_retired[x::y]
        0.31s call      tests/test_a.py::test_two_sided[cheap]
        0.22s call      tests/test_a.py::TestGroup::test_method[z[2]]
        0.18s call      tests/test_b.py::test_retired[x::y]
        0.05s call      tests/test_b.py::test_retired[with[brackets]]
    """
    monkeypatch.setattr(validate, "_run", lambda *_args, **_kwargs: durations)
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )

    with pytest.raises(validate.StepFailureError) as raised:
        validate._slow_tests(context)
    reported = str(raised.value)

    # The function that is still slow is not reported, though one of its cases is cheap.
    assert "test_two_sided" not in reported
    assert "test_method" not in reported
    # The function that is no longer slow still is, at its slowest case and not its
    # cheapest, and counted once rather than once per parametrization.
    assert "1 deferred test(s)" in reported
    assert "tests/test_b.py::test_retired[x::y]" in reported
    assert "0.18s" in reported
    assert "0.05s" not in reported


def test_the_behavioral_lanes_partition_every_test() -> None:
    """No test runs in two lanes, and none runs in none.

    This is the property the pull-request/deep split rests on (`BC-214`). The three lanes
    are pytest marker expressions over two markers, so the whole question is four cases,
    and each must be claimed exactly once. The expressions themselves are read, not
    paraphrased: a second copy of the lane definitions written out here could disagree
    with the ones the gate passes to pytest, and would then agree with itself forever.
    """

    def claims(expression: str, markers: dict[str, bool]) -> bool:
        return all(
            markers[term.removeprefix("not ")] is not term.startswith("not ")
            for term in expression.split(" and ")
        )

    lanes = (validate.QUICK_TESTS, validate.SLOW_TESTS, validate.EXHAUSTIVE_TESTS)
    for exhaustive_exact in (False, True):
        for slow in (False, True):
            markers = {"exhaustive_exact": exhaustive_exact, "slow": slow}
            claimed = [lane for lane in lanes if claims(lane, markers)]
            assert len(claimed) == 1, f"{markers} is claimed by {claimed}"


def test_a_test_over_the_per_test_ceiling_fails_the_pull_request_surface(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The boundary between the lanes is a rule the gate applies, not a list it trusts.

    A hand-kept list of slow tests rots the way `--fast`'s 499s docstring rotted. This is
    the negative control for the thing that stops it: a retained test measured at or above
    the ceiling fails, and the failure names the test rather than the tier.
    """
    ceiling = validate.QUICK_TEST_CEILING_SECONDS
    output = (
        "============================= slowest durations ==========================\n"
        f"{ceiling + 7.0:.2f}s call     tests/test_probe.py::test_that_grew\n"
        f"{ceiling + 1.0:.2f}s setup    tests/test_probe.py::test_with_a_costly_fixture\n"
        "(1904 durations < 5.00s hidden.  Use -vv to show these durations.)\n"
        "1904 passed in 61.00s"
    )
    monkeypatch.setattr(validate, "_run", lambda *_a, **_k: output)
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )

    with pytest.raises(validate.StepFailureError) as failure:
        validate._fast_tests(context)

    message = str(failure.value)
    assert "test_that_grew" in message
    assert "mark it `slow`" in message
    # Setup, not call: a module-scoped fixture bills its whole cost to whichever test
    # happens to trigger it first, so marking that test moves the cost instead of
    # removing it. The ceiling is a claim about a test, not about a fixture.
    assert "test_with_a_costly_fixture" not in message


def test_a_quick_lane_under_the_ceiling_passes_and_still_reads_the_durations() -> None:
    """A durations section reporting nothing is read, not mistaken for an unread one.

    Both lanes fail closed on a missing section, so the empty-but-present case has to be
    distinguishable from it: pytest prints the header and a "hidden" line whenever every
    test is under `--durations-min`, and that is a passing lane rather than a broken one.
    """
    header = "============================= slowest durations ====================="
    assert validate._call_durations(f"{header}\n(9 durations < 5.00s hidden.)") == []
    assert validate._call_durations(
        f"{header}\n99.00s call     tests/test_probe.py::test_slow"
    ) == [(99.0, "tests/test_probe.py::test_slow")]


def test_the_ceiling_check_refuses_output_it_cannot_read(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(validate, "_run", lambda *_a, **_k: "1904 passed in 61.00s")
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )

    with pytest.raises(validate.StepFailureError) as failure:
        validate._fast_tests(context)

    assert "went unchecked" in str(failure.value)


def test_full_exhaustive_behavioral_step_selects_only_exhaustive_exact_tests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: tuple[str, ...] | None = None

    def capture(context: validate.Context, command: tuple[str, ...], **_kwargs: object) -> str:
        del context
        nonlocal observed
        observed = command
        return ""

    monkeypatch.setattr(validate, "_run", capture)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
    )

    validate._exhaustive_exact_tests(context)

    assert observed == (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests",
        "-m",
        "exhaustive_exact",
    )


@pytest.mark.parametrize((("inner_jobs", "expected_workers")), [(1, "1"), (4, "2")])
def test_full_negative_controls_respect_the_cap_and_measured_worker_count(
    monkeypatch: pytest.MonkeyPatch,
    inner_jobs: int,
    expected_workers: str,
) -> None:
    observed: tuple[str, ...] | None = None

    def capture(_context: validate.Context, module: str, *arguments: str) -> str:
        nonlocal observed
        observed = (module, *arguments)
        return "controls passed"

    monkeypatch.setattr(validate, "_module", capture)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=inner_jobs,
        environment=os.environ.copy(),
    )

    assert validate._negative_controls(context) == "controls passed"
    assert observed == (
        "devtools.run_negative_controls",
        "devtools/controls.yaml",
        "-j",
        expected_workers,
    )


def test_invalid_worker_count_and_unmatched_selection_are_actionable() -> None:
    status, _, stderr = _invoke("--jobs", "0", "--list")
    assert status == 2
    assert "--jobs must be a positive integer" in stderr

    status, _, stderr = _invoke("--only", "not-a-real-step")
    assert status == 2
    assert "matched no validation step" in stderr
    assert "packing-validate --list" in stderr


@pytest.mark.parametrize(
    "narrowing",
    [
        ("--only", "fast behavioral tests"),
        ("--skip", "negative controls"),
        ("--fast",),
        ("--records",),
        ("--edit",),
        ("--checks",),
        ("--suite",),
        ("--sweeps",),
        ("--since", "HEAD"),
    ],
)
def test_strict_mode_refuses_a_partial_validation_surface(narrowing: tuple[str, ...]) -> None:
    """Every narrowing flag must be refused under --strict, including new ones.

    Each is parametrized rather than tested separately because the risk with a new flag is
    that it is added to the selector and forgotten in the refusal, which would let
    `--strict` quietly report a partial surface as a complete one.

    What is asserted is that the refusal **names the flag that was passed**, not that the
    sentence reads a particular way. The verbatim sentence was pinned here until
    2026-08-30, when adding `--since` broke this test four times over for no defect: the
    refusal was correct and more complete than the pin. A pin that fails whenever the
    behaviour it guards is extended correctly trains people to edit the assertion, which
    is how a guard stops guarding. Per-flag, it is also the stronger check -- it now
    verifies the refusal mentions *this* flag rather than any fixed list.
    """
    status, _, stderr = _invoke("--strict", *narrowing)

    assert status == 2
    assert "--strict cannot be combined with" in stderr
    assert narrowing[0] in stderr


def test_the_records_tier_selects_every_record_check_and_no_test() -> None:
    selected = validate._select_steps(only=[], fast=False, records=True)

    assert [step.name for step in selected] == [
        step.name for step in validate.STEPS if step.records
    ]
    # The tier exists because record drift is what breaks CI and the test step is what
    # makes the fast tier too expensive to run before every push (D-369). A test step
    # tagged into it would put the cost straight back.
    assert "fast behavioral tests" not in {step.name for step in selected}
    assert all(step.fast for step in selected)


def test_strict_mode_enables_deep_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    observed: validate.Context | None = None

    # The narrowing patterns are collected with `*` and discarded on purpose. This stub
    # exists to read the `Context`, and a stub that also pins how many pattern lists the
    # caller passes is a test that fails when the flag surface is extended correctly --
    # which it was, twice: `--only`, then `--skip` on 2026-09-05. Same reason
    # `test_strict_mode_refuses_a_partial_validation_surface` stopped pinning the
    # refusal's exact sentence.
    def capture_context(
        selected: list[validate.Step],
        context: validate.Context,
        *_narrowing: object,
    ) -> validate.RunSummary:
        nonlocal observed
        observed = context
        return validate.RunSummary(
            results=[],
            wall_seconds=0,
            selected_count=len(selected),
            total_count=len(validate.STEPS),
        )

    monkeypatch.setattr(validate, "_run_selected", capture_context)

    status, _, stderr = _invoke("--strict")

    assert status == 0
    assert stderr == ""
    assert observed is not None
    if not observed.deep:
        pytest.fail("strict mode did not enable deep validation")


def test_existing_activity_marker_explains_safe_recovery(tmp_path: Path) -> None:
    marker = tmp_path / ".gate-running"
    marker.mkdir()

    with (
        pytest.raises(validate.StepFailureError, match="Wait for it, or delete"),
        validate._validation_activity(marker),
    ):
        pytest.fail("an existing marker must prevent validation")


def test_missing_provenance_object_is_not_called_an_orphan() -> None:
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
    )
    assert validate._commit_state(context, "0" * 40) == "missing"


def test_commit_state_routes_git_probes_through_bounded_seam(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
    )
    commands: list[tuple[str, ...]] = []
    returncodes = iter((0, 0))

    def capture(_context: validate.Context, command: tuple[str, ...]) -> int:
        commands.append(command)
        return next(returncodes)

    monkeypatch.setattr(validate, "_run_returncode", capture)
    assert validate._commit_state(context, "deadbee") == "reachable"
    assert commands == [
        ("git", "cat-file", "-e", "deadbee^{commit}"),
        ("git", "merge-base", "--is-ancestor", "deadbee", "HEAD"),
    ]


def test_quiet_returncode_path_fails_closed_without_windows_tree_cleanup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
    )
    monkeypatch.setattr(validate.os, "name", "nt")
    with pytest.raises(validate.StepFailureError, match="Windows support"):
        validate._run_returncode(context, ("git", "--version"))


def test_timeout_cli_override_wins_over_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PACKING_VALIDATE_TIMEOUT_SECONDS", "120")
    observed: validate.Context | None = None

    def capture(
        selected: list[validate.Step], context: validate.Context, *_narrowing: object
    ) -> validate.RunSummary:
        del selected
        nonlocal observed
        observed = context
        return validate.RunSummary([], 0, selected_count=0, total_count=0)

    monkeypatch.setattr(validate, "_run_selected", capture)
    assert _invoke("--timeout-seconds", "7")[0] == 0
    assert observed is not None
    assert observed.timeout_seconds == 7


def test_default_timeout_covers_the_measured_full_census(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("PACKING_VALIDATE_TIMEOUT_SECONDS", raising=False)
    observed: validate.Context | None = None

    def capture(
        selected: list[validate.Step], context: validate.Context, *_narrowing: object
    ) -> validate.RunSummary:
        del selected
        nonlocal observed
        observed = context
        return validate.RunSummary([], 0, selected_count=0, total_count=0)

    monkeypatch.setattr(validate, "_run_selected", capture)
    assert _invoke()[0] == 0
    assert observed is not None
    assert observed.timeout_seconds == 900


def test_invalid_timeout_environment_names_environment_variable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PACKING_VALIDATE_TIMEOUT_SECONDS", "0")
    status, _, stderr = _invoke("--list")
    assert status == 2
    assert "PACKING_VALIDATE_TIMEOUT_SECONDS" in stderr


def test_annotated_lost_provenance_object_is_reported_unavailable() -> None:
    line = validate._provenance_line(
        "exp-001.md",
        "d6a1057",
        "## Annotation\n`engine_commit: d6a1057` is unreachable after a rebase.",
        "missing",
    )

    assert "UNAVAILABLE" in line
    assert "ORPHANED" not in line

    with pytest.raises(validate.StepFailureError, match="fetch complete history"):
        validate._provenance_line("unannotated.md", "deadbee", "", "missing")


def test_basin_event_archives_are_discovered_from_their_contract(tmp_path: Path) -> None:
    (tmp_path / "baseline.jsonl").write_text('{"kind": "result"}\n', encoding="utf-8")
    (tmp_path / "events-v2.jsonl").write_text(
        '{"contract": "packing.squares:BasinEvent/v2"}\n', encoding="utf-8"
    )
    (tmp_path / "events-v3.jsonl").write_text(
        '{"contract": "packing.squares:BasinEvent/v3"}\n', encoding="utf-8"
    )

    assert [path.name for path in validate._basin_event_archives(tmp_path)] == [
        "events-v2.jsonl",
        "events-v3.jsonl",
    ]


def test_failure_summary_uses_singular_step_for_one_failure() -> None:
    summary = validate.RunSummary(
        results=[validate.StepResult("broken", "failed", 0.1, reason="because")],
        wall_seconds=0.1,
        selected_count=1,
        total_count=1,
    )
    stdout = io.StringIO()
    stderr = io.StringIO()

    with redirect_stdout(stdout), redirect_stderr(stderr):
        status = validate._render_text(summary, strict=False)

    assert status == 1
    assert "1 STEP FAILED:" in stdout.getvalue()


def test_lint_floor_reaches_the_handwritten_skill_assets(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """The one Python file outside `packing/` is linted, and the list of hand-written
    skills is the Makefile's rather than a second copy that could drift from it."""
    directories = validate._handwritten_skill_directories()
    assert directories
    assert all(path.is_dir() for path in directories)
    assert any(path.rglob("*.py") for path in directories)
    assert all(
        path.parent == validate.REPOSITORY_ROOT / ".agents" / "skills" for path in directories
    )

    monkeypatch.setattr(validate, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "Makefile").write_text("check: skills-check\n")
    with pytest.raises(validate.StepFailureError, match="HANDWRITTEN_SKILLS"):
        validate._handwritten_skill_directories()
    (tmp_path / "Makefile").write_text("HANDWRITTEN_SKILLS := absent-skill\n")
    with pytest.raises(validate.StepFailureError, match="absent-skill"):
        validate._handwritten_skill_directories()


def test_multi_command_step_stops_at_first_failure_without_printing_success(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    marker = tmp_path / "later-command-ran"
    commands = (
        (sys.executable, "-c", "raise SystemExit(17)"),
        (
            sys.executable,
            "-c",
            f"from pathlib import Path; Path({str(marker)!r}).touch()",
        ),
    )
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")
    monkeypatch.setattr(
        validate,
        "STEPS",
        (
            validate.Step(
                "multi-command mutation",
                lambda context: validate._commands(context, commands),
            ),
        ),
    )

    status, stdout, stderr = _invoke("--jobs", "1")

    assert status == 1
    assert "command exited 17" in stderr
    assert "1 STEP FAILED:" in stdout
    assert "ALL CHECKS PASSED" not in stdout
    assert not marker.exists()


def test_frontier_contract_accepts_the_declared_schema_metadata(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    # The full gate runs pytest while its real activity marker is present. Give this
    # deliberately nested CLI contract an isolated marker without weakening the
    # production exclusion between validation and campaign execution.
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")
    status, stdout, stderr = _invoke("--only", "frontier corpus", "--jobs", "1")

    assert status == 0
    assert stderr == ""
    assert "100 artifacts, n = 1..100; formal lane: 35 proved, 65 open" in stdout
    assert "reported lane: 35 proved, 65 open" in stdout


def _budget_context(*, timeout_seconds: float, explicit: bool) -> validate.Context:
    return validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
        timeout_seconds=timeout_seconds,
        timeout_is_explicit=explicit,
    )


def _sleeping_step(name: str, seconds: float, budget: float | None) -> validate.Step:
    def action(context: validate.Context) -> str:
        return validate._run(
            context, (sys.executable, "-c", f"import time; time.sleep({seconds})")
        )

    return validate.Step(name, action, budget_seconds=budget)


def test_step_budget_raises_the_default_cap_for_that_step_only(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """`D-366`: the control suite outgrew the shared cap and nothing was wrong with it.

    A budget lets one step declare a higher ceiling without touching the ceiling every
    other step runs under, which is the trade that made raising the shared cap the wrong
    fix.
    """
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")
    context = _budget_context(timeout_seconds=0.05, explicit=False)
    budgeted = _sleeping_step("budgeted", 0.4, 5)
    unbudgeted = _sleeping_step("unbudgeted", 0.4, None)

    summary = validate._run_selected([budgeted, unbudgeted], context, [])
    by_name = {result.name: result for result in summary.results}
    assert by_name["budgeted"].status == "passed"
    assert by_name["unbudgeted"].status == "failed"
    assert "timed out after 0.05 seconds" in by_name["unbudgeted"].reason


def test_an_explicit_operator_timeout_beats_a_step_budget(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Tightening the cap by hand must bound the run, budgets included.

    A budget exists to correct a project-wide default that one step is known to exceed.
    Someone typing `--timeout-seconds` is bounding *this* run deliberately, and a step
    opting out of that would make the flag advisory.
    """
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")
    context = _budget_context(timeout_seconds=0.05, explicit=True)
    summary = validate._run_selected([_sleeping_step("budgeted", 0.4, 5)], context, [])
    assert summary.results[0].status == "failed"
    assert "timed out after 0.05 seconds" in summary.results[0].reason


def test_a_step_that_exceeds_its_own_budget_still_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A budget is a declaration, not a waiver.

    Without this, a budget would be indistinguishable from switching the cap off for the
    step that claims one, and a hung control suite would hang the run instead of
    reporting.
    """
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")
    context = _budget_context(timeout_seconds=0.05, explicit=False)
    summary = validate._run_selected([_sleeping_step("budgeted", 2, 0.2)], context, [])
    assert summary.results[0].status == "failed"
    assert "timed out after 0.2 seconds" in summary.results[0].reason


def test_only_the_whole_suite_steps_carry_budgets() -> None:
    """A budget is an exception, so the set of them is worth watching.

    If a second step acquires one, that is a signal the shared cap is wrong rather than
    that another step is special, and this test is where that conversation starts.

    It started on 2026-09-03, when `fast behavioral tests` became the second. The
    conversation did not end in raising the shared cap, and the reason is that the two
    budgeted steps are the only two that run a whole suite: the control harness clones
    the tree per worker, and the behavioural step walks every test. The other fifty-seven
    steps check one record or one certificate and finish in seconds, so a cap wide
    enough for these two would stop being a guard for them at all -- which is the trade
    `budget_seconds` exists to refuse, and it does not get better for being made twice.

    The exhaustive exact tier became the third on 2026-09-05, and it is the same class:
    a whole suite, of complete finite certificate decisions, that measured 892 s on CI's
    runner against the 900 s cap it had been inheriting -- eight seconds from failing on
    every merge to main. A fourth budgeted step would mean the cap is wrong rather than
    that another suite is heavy, and should raise the cap instead of extending this set.
    The step `--push` builds outside this tuple is not a fourth: when its selector
    expands to the whole suite it runs the quick and slow lanes together, so it takes the
    constant that bounds both (D-432), which the next test holds.

    The set changed size twice on 2026-09-05 and stayed at three. `BC-214` split the
    behavioural suite by measured cost, and the two halves did not both keep the budget:
    `slow behavioral tests` inherited it, because it is the half that carries the wall,
    and `fast behavioral tests` gave it up, because a lane whose slowest test is capped
    at `QUICK_TEST_CEILING_SECONDS` is no longer a step the shared cap is wrong for. An
    exception that is no longer needed is not harmless -- it is a guard switched off.

    Recorded honestly: the second budget was added by the coordinator during an
    unattended run and has not been independently reviewed.
    """
    budgeted = {
        step.name: step.budget_seconds for step in validate.STEPS if step.budget_seconds
    }
    assert budgeted == {
        "negative controls": 1800,
        "slow behavioral tests": 1800,
        "exhaustive exact behavioral tests": 3600,
    }


@pytest.mark.parametrize(
    ("summary", "expected_scope", "expected_budget"),
    [("everything", "whole", validate.FAST_SUITE_BUDGET_SECONDS), ("narrow 7", "subset", None)],
)
def test_push_tests_take_the_whole_suite_budget_only_when_the_selector_expands(
    monkeypatch: pytest.MonkeyPatch,
    summary: str,
    expected_scope: str,
    expected_budget: float | None,
) -> None:
    """The entry point must not decide the suite's ceiling; the suite does.

    D-432: a change set touching a suite-configuring file made `--push` select the whole
    suite, and the step it built lost the budget declared for that same suite, so the run
    died at the shared 900-second cap without naming the failing test it had reached. The
    budget is one constant both steps read. A selected subset stays on the shared cap,
    which is the guard against a hung test.

    Since `BC-214` the step that reads the same constant is `slow behavioral tests`. The
    whole-suite fallback runs `-m "not exhaustive_exact"`, which is the quick lane and the
    slow lane together, and the slow lane is the half that costs the wall -- so the
    constant that bounds `--push` is the one the slow lane declares, not the quick one's
    absent budget.
    """

    def probe(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        del args, kwargs
        return subprocess.CompletedProcess(
            args=("reachable-tests",), returncode=0, stdout=f"{summary}\n", stderr=""
        )

    monkeypatch.setattr(validate.subprocess, "run", probe)
    step = validate._push_test_step("origin/main")

    assert step.broad is (expected_scope == "whole")
    assert step.budget_seconds == expected_budget
    assert (
        validate.STEPS[
            [s.name for s in validate.STEPS].index("slow behavioral tests")
        ].budget_seconds
        == validate.FAST_SUITE_BUDGET_SECONDS
    )


def test_the_edit_tier_cannot_under_run() -> None:
    """Tiers must nest, or a narrower tier could contain a step a wider one lacks.

    This is the property that makes retiering safe to do at all. `BC-079` split `--edit`
    out of `--fast` because one step was 451 seconds more than the other seventeen
    combined, and the risk in any such split is that a step ends up reachable from the
    cheap tier and not the expensive one, or from neither.

    Containment is checked as sets rather than counts, so a swap of two steps between
    tiers cannot pass by keeping the totals equal.
    """
    names = lambda **kw: {  # noqa: E731
        step.name for step in validate._select_steps(only=[], **kw)
    }
    everything = names(fast=False)
    fast = names(fast=True)
    edit = names(fast=False, edit=True)
    records = names(fast=True, records=True)
    checks = names(fast=False, checks=True)
    sweeps = names(fast=False, sweeps=True)
    suite = names(fast=False, suite=True)

    assert records <= edit <= fast <= everything
    assert fast - edit == {step.name for step in validate.STEPS if step.broad}, (
        "the only steps --fast adds over --edit are the ones marked broad"
    )
    # The pull request's three jobs are a partition of `--fast` and not three filters,
    # which is what makes it safe to run them on separate runners: no step can be in two
    # and none in none. `--edit` lands wholly inside `--checks` because every sweep and
    # the behavioural lane are all `broad`, so the edit loop is never waiting on the
    # runners that carry them.
    assert checks | suite | sweeps == fast
    assert not checks & sweeps
    assert not checks & suite
    assert not suite & sweeps
    assert edit <= checks


def test_every_step_is_reachable_from_some_tier() -> None:
    """A step in no tier is a check nobody runs, which is worse than not having it.

    The full run is the backstop: every declared step must appear there, so a step can
    only ever be *deferred* to a wider tier and never dropped out of all of them.
    """
    reachable = {step.name for step in validate._select_steps(only=[], fast=False)}
    assert reachable == {step.name for step in validate.STEPS}


def test_the_pull_request_surface_defers_only_what_was_measured() -> None:
    """A step no pull-request job selects is a step no pull request runs, so the set is
    pinned -- and read from the workflow rather than from a flag.

    This is the guard think-k4fb asked for, and it exists because `fast` defaults to
    False. Twenty-four of sixty-one steps had accumulated outside the tier, nobody had
    decided that for most of them, and on 2026-09-05 two defects reached main through the
    gap and stayed red for nine hours (D-455, D-456). Twenty-one were promoted; a
    twenty-fifth step added tomorrow would rebuild the gap silently unless adding it to
    this set is a thing someone has to type.

    It reads the workflow because since 2026-09-06 the surface is several jobs, and a
    flag can no longer answer the question on its own. `Step.fast` says a step is meant to
    run on a pull request; only the workflow says one does. The old assertion would have
    gone on passing if a job stopped being invoked, if `--only` narrowed one of them, or
    if a new step landed in a `sweep` or `suite` set no job selected -- three ways to
    lose a check that all look identical from inside `STEPS`. So the deferred set is
    computed as
    everything the pull-request jobs do not select, and the flag is checked against it
    afterwards rather than trusted as the answer.

    Each remaining name is deferred on a measurement, and the measurements are on CI's
    two-core runner in the complete surface of run 33987628341:

    - `exhaustive exact behavioral tests` at 1943.05s has its own workflow job, which is
      what a step that size needs rather than a larger share of someone else's;
    - `negative controls` at 543.67s clones the tree per worker for 148 declared
      mutations, and would become the thing a pull request waits for -- about five
      minutes longer than the suite it would displace;
    - `n=40 rigidity bracket still reproduces` at 221.36s is the one that would have fit,
      and only just: it is about the whole remaining margin. It also re-derives
      mathematics rather than checking a record, no pull request changes its answer
      without editing the assessor, and `--since` selects it for exactly those changes.

    Deferring a fourth means arguing here that the tier's wall time -- now `max(the
    checks job, the suite job, the sweeps job)` rather than one job's queue -- has moved.
    There is a fourth, and this is that argument.

    Nothing was deferred on 2026-09-06, and that is the point of recording it here. The
    tier had reached 501.97s and the obvious 468.11s of it to drop were the two atlas
    sweeps main had just promoted; the measurement refused that too. Those two are the
    class `D-369` counted -- a registry or generated view going stale is what actually
    fails CI here -- and a change that retains a witness or edits a source map is exactly
    what breaks them, so deferring them would have re-opened the gap `D-455` came through
    with the cheapest half of the evidence. The cost was bought from concurrency instead:
    a second runner, and then a third for the behavioural lane, both argued in
    `test_the_pull_request_runs_its_sweeps_and_its_suite_apart`, which changes when a
    check runs but not whether. This set has held at four across both changes.

    `slow behavioral tests` is `BC-214`. It is not a step that was never decided: it is
    the half of the behavioural suite that carries the wall, split out by measurement
    rather than by name. Of 2,251 collected tests, 92 are marked `slow` and 2,106 remain
    on the pull-request surface, and those 92 carried 890s of a 1,038s suite -- 86 per
    cent of the cost in 4 per cent of the tests. Removing them took the tier from
    1369.60s to 177.02s.

    It is the one deferral whose membership is *enforced* rather than listed, which is
    what makes it safe to have at all. `QUICK_TESTS` and `SLOW_TESTS` are complements, so
    a test cannot fall out of both; `fast behavioral tests` fails when a test it ran
    reports a `call` phase at or above `QUICK_TEST_CEILING_SECONDS`, so a test that grows
    is caught in the week it grows; and `slow behavioral tests` fails when a deferred test
    reports below the marker floor, so one that stops being slow has to come back. The
    other three deferrals are a typed list. This one is a rule.

    And it defers cost without deferring detection, which is the distinction `OR-13`
    turns on: all eight failures CI caught on the `T-021` branch were sub-0.15s record
    comparisons, 0.46s of call time between them. The wall was never where the catching
    was.
    """
    deferred = {step.name for step in validate.STEPS} - set().union(
        *_workflow_selections(pull_request=True).values()
    )

    assert deferred == {
        "exhaustive exact behavioral tests",
        "negative controls",
        "n=40 rigidity bracket still reproduces",
        "slow behavioral tests",
    }
    # And the same four are what `--fast` leaves out, so the flag and the workflow cannot
    # drift apart: a step marked `fast` that no pull-request job invokes is deferred in
    # fact and promoted on paper, which is the state think-k4fb found and this pins shut.
    assert deferred == {step.name for step in validate.STEPS if not step.fast}


def test_the_pull_request_runs_its_sweeps_and_its_suite_apart() -> None:
    """Which steps leave the `checks` job for a runner of their own, and why each did.

    `sweep` and `suite` decide which of the pull request's three jobs runs a step, and
    both default to False, so the failure mode of forgetting one is a slower `checks` job
    rather than a step nobody runs -- the safe direction, as with `broad` and `touches`.
    What needs a guard is the other direction: a step moved out to make the `checks` job
    look fast. Adding a name below means typing a number next to it.

    The measurements are CI's, run 34010470187 on a four-cpu runner: `--checks --jobs 3
    --inner-jobs 1` at 221.70s of wall over 58 steps, and `--sweeps --jobs 4
    --inner-jobs 1` at 110.66s over four.

    The sweeps, 313.95s of step time between them:

    - `single-square translation escape screen`, 110.66s. The longest single unit
      anywhere on the pull-request surface, this job's wall, and therefore the floor
      under the whole surface.
    - `known-best chunk census`, 90.38s.
    - `known-best n=1..100 atlas`, 75.88s -- the eight subcommands left after the census
      was split out of it.
    - `prospective n=101..324 safe seed`, 37.03s.

    They are one kind of work: each re-derives a retained atlas from the hundred-odd
    witnesses under it and compares it byte for byte. That matters more than the ranking,
    because a rule keyed on kind survives a step getting faster, and a rule keyed on
    today's top four does not -- as this list has already shown, the prospective seed
    having gone from the longest of the four to the shortest.

    The suite is one step and its rule is arithmetic rather than kind:

    - `fast behavioral tests`, 142.43s of the 221.70s `checks` job, which is 64 per cent
      of a job it shares with 57 others. A job cannot be shorter than its longest step,
      so while this ran in `checks` no `--jobs` setting could take that job under 142s.
      Alone it also stops being throttled: `_pytest_workers` gives it `cpus - jobs + 1`
      xdist workers, which was two beside 57 steps at `--jobs 3` and is four at
      `--jobs 1` on a runner of its own.

    What this buys is three numbers instead of one queue, and no coverage change at all:
    every one of these steps runs on every pull request exactly as it did before, which
    is what `test_the_pull_request_surface_defers_only_what_was_measured` re-checks from
    the workflow rather than from these flags.
    """
    assert {step.name for step in validate.STEPS if step.sweep} == {
        "prospective n=101..324 safe seed",
        "known-best chunk census",
        "single-square translation escape screen",
        "known-best n=1..100 atlas",
    }
    assert {step.name for step in validate.STEPS if step.suite} == {
        "fast behavioral tests",
    }
    # A sweep or a suite step outside `--fast` would be a step the pull request does not
    # run at all, which is a deferral and belongs in the test above rather than in this
    # one. Being both would put one step in two jobs, which is a bill paid twice.
    assert all(step.fast for step in validate.STEPS if step.sweep or step.suite)
    assert not any(step.sweep and step.suite for step in validate.STEPS)


def _workflow_selections(*, pull_request: bool) -> dict[str, set[str]]:
    """What each Linux gate job actually selects on this event, by job name.

    Read from the workflow, parsed with the CLI's own parser and resolved through its own
    selector, because every part of the split is a string typed into a YAML file and a
    guard that reimplemented the selector would drift from the thing it guards.

    `macos-portability` is excluded by name rather than by rule. It runs four steps a
    second architecture could disagree about, deliberately duplicating work the Linux
    jobs also do, so it is not part of either partition -- and the tests that call this
    assert which jobs exist, so a new one cannot join either surface unnoticed.
    """
    condition = "github.event_name == 'pull_request'"
    negation = "github.event_name != 'pull_request'"
    excluded = negation if pull_request else condition
    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    selections: dict[str, set[str]] = {}
    for job_name, job in document["jobs"].items():
        if job_name == "macos-portability" or excluded in str(job.get("if", "")):
            continue
        for step in job.get("steps", []):
            command = str(step.get("run", ""))
            if "packing-validate" not in command or excluded in str(step.get("if", "")):
                continue
            tokens = shlex.split(command)
            arguments = tokens[tokens.index("packing-validate") + 1 :]
            namespace = validate._parser().parse_args(arguments)
            selections[job_name] = {
                selected.name
                for selected in validate._select_steps(
                    only=namespace.only,
                    skip=namespace.skip,
                    fast=namespace.fast,
                    records=namespace.records,
                    edit=namespace.edit,
                    checks=namespace.checks,
                    sweeps=namespace.sweeps,
                    suite=namespace.suite,
                )
            }
    return selections


def test_the_pull_request_jobs_partition_the_surface() -> None:
    """The jobs a pull request runs must divide `--fast`, and pay for nothing twice.

    The surface was one job until 2026-09-06 and one job could not hold it: 1,100s of
    step time on a four-cpu runner has a 275s floor however it is scheduled, and it was
    finishing in 501.97s. It was two jobs for one day, and two could not balance it:
    `checks` 221.70s against `sweeps` 110.66s on run 34010470187, with 142.43s of the
    longer half in a single indivisible step. Three runners is twelve cpus and puts that
    step on its own. What a split like this risks is the gap `D-455` came through in the
    other direction -- a step in no selection, run by nobody, reported by nothing -- so
    the three commands are read from the workflow and checked to be a partition rather
    than trusted to be.

    `--checks`, `--suite` and `--sweeps` are a partition in `_select_steps` by
    construction, so this is really a check on the YAML: that the workflow invokes all
    three, on a pull request, and narrows none of them with `--only` or `--skip`.

    Pairwise disjointness is asserted rather than inferred from the union. Two jobs make
    those the same statement; three do not, and the case they differ on -- one step in
    two jobs and another in none -- is a bill paid twice hiding a check nobody runs.
    """
    selections = _workflow_selections(pull_request=True)

    assert set(selections) == {"validate", "suite", "sweeps"}
    assert not selections["validate"] & selections["sweeps"]
    assert not selections["validate"] & selections["suite"]
    assert not selections["suite"] & selections["sweeps"]
    assert selections["validate"] | selections["suite"] | selections["sweeps"] == {
        step.name for step in validate.STEPS if step.fast
    }
    assert selections["sweeps"] == {step.name for step in validate.STEPS if step.sweep}
    assert selections["suite"] == {step.name for step in validate.STEPS if step.suite}


def test_every_tier_band_is_declared_for_the_shape_ci_runs() -> None:
    """A `reference` that names no invocation CI makes is a band nothing ever enforces.

    `gate_budgets.judge` applies the drift and stale rules only to a run whose `--jobs`,
    `--inner-jobs` and cpu count match the tier's `reference`, and reports without
    failing on every other run. That is the right rule -- wall time is not comparable
    across machines -- and it has one failure mode: a reference nobody hits. Then every
    CI run prints "not the reference shape", nothing is ever judged, and the register
    reads as though it were guarding a tier it has never once bounded. The `fast` entry
    already carries that warning in prose ("leaving the old one here is how a band stays
    permanently unenforced"); this is the same statement as a check.

    It is written against the pull-request jobs because those are the ones that run a
    whole tier on a known runner. `--jobs` and `--inner-jobs` come from the command in
    the YAML; the cpu count does not, so it is not asserted here -- GitHub's runner
    reports four and the register records four, and a runner that changed size would
    show up as an unenforced band rather than as a wrong one.

    The post-merge commands are out of scope rather than exempt. Both are narrowed --
    `--skip` on one, `--only` on the other -- so neither is a clean reading of a whole
    tier, which is the same reason the `full` entry says only its ceiling applies.
    """
    register = gate_budgets.load()
    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    negation = "github.event_name != 'pull_request'"
    checked: set[str] = set()
    for job in document["jobs"].values():
        if negation in str(job.get("if", "")):
            continue
        for step in job.get("steps", []):
            command = str(step.get("run", ""))
            if "packing-validate" not in command or negation in str(step.get("if", "")):
                continue
            tokens = shlex.split(command)
            namespace = validate._parser().parse_args(
                tokens[tokens.index("packing-validate") + 1 :]
            )
            tier_id = validate._tier_id(namespace)
            if tier_id is None:
                continue
            tier = register.tier(tier_id)
            assert tier is not None, f"{tier_id} runs on a pull request with no ceiling"
            assert tier.reference.jobs == int(namespace.jobs), tier_id
            assert tier.reference.inner_jobs == int(namespace.inner_jobs), tier_id
            checked.add(tier_id)
    assert checked == {"checks", "suite", "sweeps"}


def test_the_post_merge_jobs_partition_the_gate() -> None:
    """The two jobs a merge runs must together select every step, and none twice.

    think-tr2z split the exhaustive tier onto its own runner so that it reports its own
    verdict against its own budget; `--skip` on the other job is what stops it being paid
    for twice. Both halves of that are a name typed into a YAML file, so this reads the
    workflow, parses each command with the CLI's own parser, and resolves it through the
    CLI's own selector: a step added to `STEPS` lands in one job or the other, and a
    rename that breaks the split fails here rather than after a merge.

    A merge still runs the gate as one job plus the exhaustive tier, not as the pull
    request's three parts. The `suite` and `sweeps` jobs are pull-request only, and the
    complete integration surface here already contains every step they would have run.
    """
    selections = _workflow_selections(pull_request=False)

    assert set(selections) == {"validate", "exhaustive"}
    assert selections["exhaustive"] == {"exhaustive exact behavioral tests"}
    assert not selections["validate"] & selections["exhaustive"]
    assert selections["validate"] | selections["exhaustive"] == {
        step.name for step in validate.STEPS
    }


def test_the_longest_steps_are_submitted_first() -> None:
    """A long step submitted late finishes late, and the run ends when it does.

    The pool takes steps in submission order, and the behavioural suite is declared
    fifteenth. That cost nothing while the fourteen ahead of it were seconds of record
    checks; the 2026-09-05 promotion put eleven steps and 476s there, which greedy
    submission would have spent delaying the suite's start rather than running beside it.

    Ordering by declared budget rather than by a guessed duration keeps the file the only
    place a step's cost is asserted.

    `fast behavioral tests` is no longer in this list, and its absence is the point rather
    than an omission. It carried an 1800s exception to the shared cap for as long as it
    ran every non-exhaustive test; `BC-214` moved the slow half to `slow behavioral tests`,
    so the quick lane is ordinary enough to live under the shared cap and a step that no
    longer needs an exception should not keep one. What it is allowed to *cost*, as
    against how long one hung subprocess may hang, is `devtools/gate-budgets.yaml`.
    """
    order = [step.name for step in validate._submission_order(validate.STEPS)]

    assert order[:3] == [
        "exhaustive exact behavioral tests",  # 3600s
        "negative controls",  # 1800s, and declared before the suite
        "slow behavioral tests",  # 1800s, the non-exhaustive suite's own bound
    ]
    assert order[3:] == [step.name for step in validate.STEPS if step.budget_seconds is None]


def test_submission_order_does_not_change_the_reported_order(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Output is replayed in declared order, which is what keeps two runs comparable."""
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")
    context = _budget_context(timeout_seconds=5, explicit=False)
    first = _sleeping_step("declared first", 0.05, None)
    second = _sleeping_step("declared second", 0.05, 4)

    summary = validate._run_selected([first, second], context, [])

    assert [result.name for result in summary.results] == ["declared first", "declared second"]
    assert [step.name for step in validate._submission_order([first, second])] == [
        "declared second",
        "declared first",
    ]


def test_broad_is_opt_out_so_a_new_step_joins_the_edit_tier() -> None:
    """Forgetting the marker must make the tier slower, never blinder.

    A `broad` default of True would mean a new fast step silently sat outside the edit
    loop until someone noticed. The default is False, so the failure mode of forgetting
    is a tier that costs more than it needs to -- which shows up in the timings rather
    than in a missed regression.
    """
    assert validate.Step("probe", lambda _context: "", fast=True).broad is False
    assert {step.name for step in validate.STEPS if step.broad} == {
        "fast behavioral tests",
        # Measured 2026-08-30: 31.6s in CI against a 43s edit tier, so carrying it there
        # would nearly double the tier for a record that changes when a witness is
        # retained -- which is to say rarely, and never from an edit. It still runs in
        # `--fast` and above, and CI runs the full gate on every push.
        "the decimal route still cannot price an exact pose",
        # The rest arrived together on 2026-09-05, when twenty-one steps that had run
        # only after a merge joined the pull-request tier (think-k4fb). Being in that
        # tier is what makes `broad` load-bearing for them: without it each would also
        # have joined a 40s edit loop, and these fifteen measure 529s between them.
        # The rule applied was a cost one -- above about five seconds locally, or
        # needing a toolchain the edit loop should not be starting -- and the six
        # promoted steps that fell under it are in `--edit` rather than here.
        "soundness perimeter",  # 47.14s, and selecting it builds sqsearch
        "search engine (sqsearch)",  # 2.19s, but needs that same build
        "differential: search energy vs validity oracle",  # 0.34s, likewise
        "lint floor (rust)",  # 14.94s of cargo clippy and rustfmt
        # The four record sweeps, split at their measured seams on 2026-09-06 so the pull
        # request's second runner can schedule them. The figures beside them are the
        # 148.50s and 102.56s above, divided by the same measurement that split them:
        # locally, at `PACK_JOBS=1` and one subcommand at a time, the census was 94.85s of
        # the undivided known-best step's 133.22s and the seed 88.37s of the prospective
        # step's 88.76s.
        "known-best n=1..100 atlas",  # 148.50s undivided, about 43s without the census
        "known-best chunk census",  # about 106s of that 148.50s
        "prospective n=101..324 safe seed",  # 102.10s of the 102.56s
        "single-square translation escape screen",  # 73.07s
        "historical regressions",  # 29.35s
        "deterministic SVG rendering",  # 26.39s
        "D-034's n=5 identity pair still reproduces",  # 23.54s
        "small-n exact models and local geometry",  # 19.80s
        "Trump exact branchwise linearized cones",  # 13.82s
        "fixed-angle cell is an LP, rebuilt independently",  # 9.76s
        "basin atlas",  # 9.63s
        "basin event record and replay",  # 7.89s
    }


def test_edit_and_fast_are_not_silently_combinable() -> None:
    """Passing both should say which is wider rather than quietly picking one."""
    status, _stdout, stderr = _invoke("--edit", "--fast", "--list")
    assert status == 2
    assert "different tiers" in stderr


def test_a_vanished_activity_marker_does_not_discard_the_run(tmp_path: Path) -> None:
    """Releasing a lock that is already released is not a failure (D-383).

    A bare `rmdir` in the `finally` raised out of the teardown and replaced the summary of
    a completed 25-minute `--fast` run with a traceback. The marker stops two gates running
    at once; by the time it is released this gate is over, so its absence is nothing to
    report.
    """
    marker = tmp_path / ".gate-running"

    with validate._validation_activity(marker):
        assert marker.is_dir()
        marker.rmdir()  # what an operator clearing a "stale" marker does

    assert not marker.exists()


def test_the_activity_marker_still_refuses_a_second_gate(tmp_path: Path) -> None:
    """The half that must not be weakened by the fix above."""
    marker = tmp_path / ".gate-running"
    marker.mkdir()

    with (
        pytest.raises(validate.StepFailureError, match="another gate may be running"),
        validate._validation_activity(marker),
    ):
        pass  # pragma: no cover - the context manager refuses to enter
