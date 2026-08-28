"""Behavioral tests for the self-documenting packing validation command."""

# These contracts deliberately exercise the CLI module's internal functional seams.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import io
import os
import signal
import subprocess
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pytest

from sqpack.cli import validate
from sqpack.cli.validate import main


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
    assert "fast behavioral tests [fast]" in stdout
    assert "exhaustive exact behavioral tests [full]" in stdout
    assert "soundness perimeter [full, engine]" in stdout


def test_list_applies_the_same_fast_and_name_filters_as_execution() -> None:
    status, stdout, stderr = _invoke("--list", "--fast")

    assert status == 0
    assert stderr == ""
    assert "fast behavioral tests [fast]" in stdout
    assert "exhaustive exact behavioral tests" not in stdout
    assert "soundness perimeter" not in stdout

    status, stdout, stderr = _invoke("--list", "--only", "negative control")

    assert status == 0
    assert stderr == ""
    assert stdout.splitlines() == ["negative controls [full]"]


def test_fast_behavioral_step_excludes_exhaustive_exact_tests(
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

    validate._fast_tests(context)

    assert observed == (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "tests",
        "-m",
        "not exhaustive_exact",
    )


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


@pytest.mark.parametrize((("inner_jobs", "expected_workers")), ((1, "1"), (4, "2")))
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


def test_strict_mode_refuses_a_partial_validation_surface() -> None:
    status, _, stderr = _invoke("--strict", "--only", "fast behavioral tests")

    assert status == 2
    assert "--strict cannot be combined with --only or --fast" in stderr


def test_strict_mode_enables_deep_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    observed: validate.Context | None = None

    def capture_context(
        selected: list[validate.Step], context: validate.Context, patterns: list[str]
    ) -> validate.RunSummary:
        del patterns
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
        selected: list[validate.Step], context: validate.Context, patterns: list[str]
    ) -> validate.RunSummary:
        del selected, patterns
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
        selected: list[validate.Step], context: validate.Context, patterns: list[str]
    ) -> validate.RunSummary:
        del selected, patterns
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
