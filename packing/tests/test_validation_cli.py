"""Behavioral tests for the self-documenting packing validation command."""

# These contracts deliberately exercise the CLI module's internal functional seams.
# pyright: reportPrivateUsage=false

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import shlex
import signal
import subprocess
import sys
import time
from collections.abc import Callable, Mapping, Sequence
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from textwrap import dedent
from threading import Barrier, Lock
from typing import Any

import pytest

from sqpack import gate_budgets
from sqpack.cli import validate
from sqpack.cli.validate import main
from sqpack.yamlio import safe_load
from tests import site_browser

#: (proved, open) at each corpus the frontier-corpus step has summarized. 2026-10-02: the
#: replayed zmx2 sweeps of the s(60) and s(59) mixed covers (T-062, T-063, T-066) proved
#: n = 59, 60 and 61 in the formal lane, three more in every corpus; later that day the
#: completed sweeps of the s(77) cover (T-067) proved n = 77 and 78, two more. 2026-10-03:
#: the full Valid7 replay and the built Lean reduction (T-064) proved n = 97, 118, 141,
#: 166, 193, 222, 253, 286 and 321, which meets the reported lane at every corpus.
FRONTIER_LANE_SPLIT: dict[str, tuple[int, int]] = {
    "n=1..100": (45, 55),
    "n=1..200": (61, 139),
    "n=1..324": (77, 247),
}

# Source-reported closures from T-062 to T-064, and T-066 and T-067 at n = 59 and 77,
# change this lane alone; the verified/formal lane above remains open until
# certificate replay. 2026-10-03: Daniel's reported s(k^2 - 4) = k (T-081) closes
# n = 96, 117, 140, 165, 192, 221, 252, 285 and 320 in this lane only.
REPORTED_LANE_SPLIT: dict[str, tuple[int, int]] = {
    "n=1..100": (46, 54),
    "n=1..200": (66, 134),
    "n=1..324": (86, 238),
}

WORKFLOW = Path(__file__).resolve().parents[2] / ".github/workflows/packing-validation.yml"
"""The gate's own workflow, read by the test that keeps its post-merge jobs a
partition of `STEPS`. Repository-relative from `packing/tests/`, so two levels up."""


def test_artifacts_keep_partial_subprocess_output_after_timeout(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    artifacts = tmp_path / "artifacts"
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={**os.environ, "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts)},
    )

    def time_out_after_partial_output(
        _context: validate.Context, _command: list[str], **options: object
    ) -> str:
        stream = options["output_stream"]
        assert isinstance(stream, io.TextIOBase)
        stream.write("partial\n")
        stream.flush()
        raise validate.StepTimeoutError("command timed out after partial output")

    monkeypatch.setattr(validate, "_run_command", time_out_after_partial_output)
    with pytest.raises(validate.StepFailureError, match="timed out"):
        validate._run(context, [sys.executable, "-c", "pass"])
    assert "partial" in next(artifacts.glob("*.log")).read_text()
    end = json.loads(next(artifacts.glob("*.end.json")).read_text())
    assert end["status"] == "timed_out"
    assert end["run_id"] == context.artifact_run_id
    assert end["wall_seconds"] > 0
    assert next(artifacts.glob("*.start.json")).is_file()


@pytest.mark.parametrize("error_type", [KeyboardInterrupt, validate.StepCancelledError])
def test_artifacts_distinguish_cancelled_commands(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    error_type: type[BaseException],
) -> None:
    artifacts = tmp_path / "artifacts"
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={**os.environ, "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts)},
    )

    def cancelled(*_args: object, **_kwargs: object) -> str:
        raise error_type("operator cancelled")

    monkeypatch.setattr(validate, "_run_command", cancelled)
    with pytest.raises(error_type):
        validate._run(context, [sys.executable, "-c", "pass"])
    end = json.loads(next(artifacts.glob("*.end.json")).read_text())
    assert end["status"] == "cancelled"
    assert end["reason"] == "operator cancelled"


def test_artifacts_give_pytest_unique_junit_and_all_phase_timings(tmp_path: Path) -> None:
    source = tmp_path / "test_probe.py"
    source.write_text("def test_probe():\n    assert True\n")
    artifacts = tmp_path / "artifacts"
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={**os.environ, "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts)},
    )
    output = validate._run(
        context, [sys.executable, "-m", "pytest", "-q", str(source)], cwd=tmp_path
    )
    assert "slowest durations" in output
    assert next(artifacts.glob("*.junit.xml")).is_file()
    end = json.loads(next(artifacts.glob("*.end.json")).read_text())
    assert end["status"] == "passed"


def test_artifacts_keep_a_steps_own_durations_filter(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The quick lane's `--durations-min` is its ceiling; capture must not override it."""
    artifacts = tmp_path / "artifacts"
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={**os.environ, "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts)},
    )
    commands: list[list[str]] = []

    def record(_context: validate.Context, command: list[str], **_options: object) -> str:
        commands.append(list(command))
        return ""

    monkeypatch.setattr(validate, "_run_command", record)
    validate._run(context, validate._quick_lane_command(1, 0))
    validate._run(context, [sys.executable, "-m", "pytest", "-q", "tests"])
    quick, bare = commands
    assert [argument for argument in quick if argument.startswith("--durations-min")] == [
        f"--durations-min={validate.QUICK_TEST_WALL_BACKSTOP_SECONDS:g}"
    ]
    assert quick.count("--durations=0") == 1
    assert bare[-3:-1] == ["--durations=0", "--durations-min=0"]
    assert all(command[-1].startswith("--junitxml=") for command in commands)
    # The quick lane also writes its per-file cost report into the same artifact, under the
    # junit file's stem, and a pytest command without the plugin is not asked for one.
    # `devtools.suite_files record` rebuilds the shard partition from those reports, so
    # losing the argument would leave the next recalibration with nothing to read.
    [costs] = [argument for argument in quick if argument.startswith("--test-file-costs=")]
    stem = quick[-1].removeprefix("--junitxml=").removesuffix(".junit.xml")
    assert costs == f"--test-file-costs={stem}.test-files.json"
    assert not any(argument.startswith("--test-file-costs=") for argument in bare)


def test_artifact_provenance_reports_a_git_failure_as_a_step_failure(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    artifacts = tmp_path / "artifacts"
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={**os.environ, "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts)},
    )
    monkeypatch.setattr(validate, "REPOSITORY_ROOT", tmp_path / "not-a-repository")
    with pytest.raises(validate.StepFailureError, match="artifact provenance: git ls-files"):
        validate._begin_artifacts(context, [])
    assert not list(artifacts.glob("run-*.json"))


def test_artifact_provenance_includes_untracked_source(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(
        [
            "git",
            "-C",
            str(repo),
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.com",
            "commit",
            "-q",
            "--allow-empty",
            "-m",
            "baseline",
        ],
        check=True,
    )
    source = repo / "untracked.py"
    source.write_text("VALUE = 3\n")
    artifacts = tmp_path / "artifacts"
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={
            **os.environ,
            "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts),
            "DYLD_FALLBACK_LIBRARY_PATH": "/opt/homebrew/lib",
        },
    )
    monkeypatch.setattr(validate, "REPOSITORY_ROOT", repo)
    validate._begin_artifacts(context, [])
    receipt = json.loads(next(artifacts.glob("run-*.json")).read_text())
    assert receipt["commit"]
    assert receipt["run_id"] == context.artifact_run_id
    assert receipt["untracked_hashes"] == {
        "untracked.py": hashlib.sha256(source.read_bytes()).hexdigest(),
    }
    assert receipt["environment"]["DYLD_FALLBACK_LIBRARY_PATH"] == "/opt/homebrew/lib"
    assert "untracked.py" in receipt["git_status"]


def test_ci_keeps_each_gate_jobs_timing_artifacts_even_on_failure() -> None:
    for workflow in (WORKFLOW, WORKFLOW.parent / "deep-gate.yml"):
        document = safe_load(workflow.read_text())
        assert isinstance(document, dict)
        assert "PACKING_VALIDATION_ARTIFACT_DIR" in document["env"]
        workspace = "/home/runner/work/squares/squares"
        artifact_pattern = document["env"]["PACKING_VALIDATION_ARTIFACT_DIR"].replace(
            "${{ github.workspace }}", workspace
        )
        # upload-artifact rejects these segments even in an absolute path.
        assert not {".", ".."}.intersection(artifact_pattern.split("/")), workflow
        assert Path(artifact_pattern).is_absolute(), workflow
        assert not Path(artifact_pattern).is_relative_to(workspace), workflow
        for name, job in document["jobs"].items():
            steps = job.get("steps", [])
            if not any("packing-validate" in str(step.get("run", "")) for step in steps):
                continue
            upload = [
                step
                for step in steps
                if str(step.get("uses", "")).startswith("actions/upload-artifact@")
                and step.get("with", {}).get("path")
                == "${{ env.PACKING_VALIDATION_ARTIFACT_DIR }}"
            ]
            assert len(upload) == 1, name
            assert upload[0]["if"] == "always()", name
            assert upload[0]["with"]["path"] == "${{ env.PACKING_VALIDATION_ARTIFACT_DIR }}"


def test_isolated_jobs_use_the_host_without_multiplying_concurrent_pools() -> None:
    """Each isolated selection retains its declared worker allocation.

    The screen and exhaustive tier use four inner workers. The slow lane has xdist
    workers of its own and retains the two-worker inner cap from PR #120. The other
    numeric checks run serially with two inner workers, preserving that PR's response
    to the simultaneous corpus-pool timeout. These flags do not establish a speedup
    or a total process bound when tests create their own pools.

    `D-484` is why this is a rule over selections instead of a list of exhaustive jobs.
    The escape screen became the second step to own a runner, and under the old matching
    -- which tested for the exhaustive tier by name -- it would have been skipped
    silently, along with the integration surface whose `--skip` list it lengthened.

    `macos-portability` is excluded by name, as it is in `_workflow_selections` and for
    the same reason: it is a second architecture deliberately duplicating four steps the
    Linux jobs also run, on a different host class, so the cpu arithmetic here is not the
    arithmetic it is sized against.
    """
    checked: set[tuple[str, str]] = set()
    for workflow in (WORKFLOW, WORKFLOW.parent / "deep-gate.yml"):
        document = safe_load(workflow.read_text())
        for name, job in document["jobs"].items():
            if name == "macos-portability":
                continue
            for step in job.get("steps", []):
                tokens = shlex.split(str(step.get("run", "")))
                if "packing-validate" not in tokens:
                    continue
                namespace = validate._parser().parse_args(
                    tokens[tokens.index("packing-validate") + 1 :]
                )
                only = namespace.only or []
                if name.startswith("deferred-") or only == ["slow behavioral tests"]:
                    assert (namespace.jobs, namespace.inner_jobs) == ("1", "2")
                elif len(only) == 1:
                    assert (namespace.jobs, namespace.inner_jobs) == ("1", "4")
                elif namespace.skip or len(only) > 1:
                    assert (namespace.jobs, namespace.inner_jobs) == ("1", "2")
                else:
                    continue
                checked.add((workflow.name, name))
    assert checked == {
        ("packing-validation.yml", "exhaustive-1"),
        ("packing-validation.yml", "exhaustive-2"),
        ("packing-validation.yml", "exhaustive-3"),
        ("packing-validation.yml", "screen"),
        ("packing-validation.yml", "slow-lane"),
        ("packing-validation.yml", "validate"),
        ("packing-validation.yml", "deferred-threshold-1440"),
        ("packing-validation.yml", "deferred-atlas-grid"),
        ("packing-validation.yml", "deferred-controls-finer"),
        ("packing-validation.yml", "deferred-threshold-720-rigidity"),
        ("packing-validation.yml", "regularized-views"),
        ("deep-gate.yml", "exhaustive-1"),
        ("deep-gate.yml", "exhaustive-2"),
        ("deep-gate.yml", "exhaustive-3"),
        ("deep-gate.yml", "deferred-threshold-1440"),
        ("deep-gate.yml", "deferred-atlas-grid"),
        ("deep-gate.yml", "deferred-controls-finer"),
        ("deep-gate.yml", "deferred-threshold-720-rigidity"),
        ("deep-gate.yml", "screen"),
        ("deep-gate.yml", "deferred-slow-lane"),
        ("deep-gate.yml", "regularized-views"),
    }


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

    with pytest.raises(validate.StepCancelledError, match="rejected new subprocess"):
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
    signals: list[tuple[int, int]] = []
    monkeypatch.setattr(
        validate.os, "killpg", lambda pid, signum: signals.append((pid, signum))
    )
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
    assert signals == [(process.pid, signal.SIGKILL)]


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
    assert "fast behavioral tests, shard A [fast, suite-a]" in stdout
    assert "fast behavioral tests, shard B [fast, suite-b]" in stdout
    assert "fast behavioral tests, shard C [fast, suite-c]" in stdout
    assert "fast behavioral tests, shard D [fast, suite-d]" in stdout
    assert "exhaustive exact behavioral tests [full]" in stdout
    assert "soundness perimeter [fast, checks, engine]" in stdout


def test_list_applies_the_same_fast_and_name_filters_as_execution() -> None:
    status, stdout, stderr = _invoke("--list", "--fast")

    assert status == 0
    assert stderr == ""
    assert "fast behavioral tests, shard A [fast, suite-a]" in stdout
    assert "fast behavioral tests, shard B [fast, suite-b]" in stdout
    assert "fast behavioral tests, shard C [fast, suite-c]" in stdout
    assert "fast behavioral tests, shard D [fast, suite-d]" in stdout
    assert "exhaustive exact behavioral tests" not in stdout
    assert "negative controls" not in stdout

    status, stdout, stderr = _invoke("--list", "--only", "negative control")

    assert status == 0
    assert stderr == ""
    assert stdout.splitlines() == ["negative controls [full]"]


def test_exhaustive_shard_is_confined_to_the_exact_exhaustive_selection() -> None:
    status, stdout, stderr = _invoke(
        "--list",
        "--only",
        "exhaustive exact behavioral tests",
        "--exhaustive-shard",
        "2/3",
    )
    assert status == 0
    assert stderr == ""
    assert stdout.splitlines() == ["exhaustive exact behavioral tests [full]"]

    invalid = (
        ("--list", "--exhaustive-shard", "1/3"),
        ("--list", "--fast", "--exhaustive-shard", "1/3"),
        (
            "--list",
            "--only",
            "exhaustive exact behavioral tests",
            "--exhaustive-shard",
            "1/2",
        ),
        (
            "--list",
            "--only",
            "exhaustive exact behavioral tests",
            "--exhaustive-shard",
            "4/3",
        ),
        (
            "--list",
            "--only",
            "exhaustive exact behavioral tests",
            "--exhaustive-shard",
            "one/3",
        ),
    )
    for arguments in invalid:
        status, _, stderr = _invoke(*arguments)
        assert status == 2
        assert "--exhaustive-shard" in stderr


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
    assert "fast behavioral tests, shard A [fast, suite-a]" in stdout
    assert "fast behavioral tests, shard B [fast, suite-b]" in stdout
    assert "fast behavioral tests, shard C [fast, suite-c]" in stdout
    assert "fast behavioral tests, shard D [fast, suite-d]" in stdout


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
        return (
            "==== slowest durations ====\n(1904 durations < 12s hidden.)\n"
            "==== slowest observed cpu durations (lower bounds) ====\n"
            "Incomplete descendant accounting; do not use for total CPU thresholds.\n"
            "(1904 CPU lower bounds < 6s hidden.)"
        )

    monkeypatch.setattr(validate, "_run", capture)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
    )

    monkeypatch.setattr(validate, "_pytest_workers", lambda _jobs: 4)

    validate._fast_tests(context, 1)

    assert observed == (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        *validate.BEHAVIORAL_TEST_ROOTS,
        f"--ignore={validate.BROWSER_FLOOR_LIVENESS_TESTS}",
        # The two files that pin the tables' pixels run where Chromium is installed, in
        # `site table layout in Chromium`; a shard has no browser for them (D-513).
        "--ignore=tests/test_site_result_columns.py",
        "--ignore=tests/test_site_frontier_table.py",
        "-m",
        "not exhaustive_exact and not slow",
        "-n",
        "4",
        "--dist=loadfile",
        "-p",
        "devtools.suite_files",
        "--suite-shard=1/4",
        # The plugin that prints the cpu section, loaded by name across the subprocess
        # boundary because `sqpack.cli` may not import `devtools`.
        "-p",
        "devtools.cpu_durations",
        # Wall time enforces the ceiling; the CPU threshold only filters diagnostics.
        "--durations=0",
        f"--durations-min={validate.QUICK_TEST_WALL_BACKSTOP_SECONDS:g}",
        "--cpu-durations=0",
        f"--cpu-durations-min={validate.QUICK_TEST_CPU_REPORT_SECONDS:g}",
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

    command = validate._quick_lane_command(1, 1)

    assert "-n" not in command
    assert "--dist=loadfile" not in command
    assert command[-4:] == (
        "--durations=0",
        f"--durations-min={validate.QUICK_TEST_WALL_BACKSTOP_SECONDS:g}",
        "--cpu-durations=0",
        f"--cpu-durations-min={validate.QUICK_TEST_CPU_REPORT_SECONDS:g}",
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
    """The slow lane asks for the workers `_pytest_workers` sizes from this run's `--jobs`.

    Asserted as the literal `-n 4` with `_pytest_workers` pinned to four, exactly as
    `test_fast_behavioral_step_excludes_exhaustive_exact_tests` pins it for the quick lane,
    because the pin is what makes the assertion mean anything. This test used to build its
    expected tuple from `*validate._xdist_distribution(1)` -- the helper the code under
    test calls -- and so asserted nothing on any host where that helper answers `()`: one
    cpu, or every cpu already claimed by `--jobs`. A `_slow_tests` with its workers deleted
    passed it on a one-cpu view of this box, and that is `D-484` exactly: the two lanes
    split, and only one of them given workers.

    The call is recorded too, because the count has to be sized from this run's `--jobs`
    and not from a constant: the lane is one of the `jobs`, and `cpus - jobs + 1` is what
    it is owed beside whatever else the runner is doing.
    """
    observed: tuple[str, ...] | None = None
    sized_for: list[int] = []

    def capture(context: validate.Context, command: tuple[str, ...], **_kwargs: object) -> str:
        del context
        nonlocal observed
        observed = command
        return "==== slowest durations ====\n(0 durations < 0.005s hidden.)"

    def four_workers(jobs: int) -> int:
        sized_for.append(jobs)
        return 4

    monkeypatch.setattr(validate, "_run", capture)
    monkeypatch.setattr(validate, "_pytest_workers", four_workers)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=2,
        inner_jobs=1,
        environment=os.environ.copy(),
    )

    validate._slow_tests(context)

    assert sized_for == [2]
    assert observed == (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        *validate.BEHAVIORAL_TEST_ROOTS,
        "-m",
        "slow and not exhaustive_exact",
        "-n",
        "4",
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

    def broken_collection(_context: validate.Context, command: tuple[str, ...]) -> str:
        if "--collect-only" in command:
            raise validate.StepFailureError("command exited 2: pytest\ncollection failed")
        return deselected()

    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )

    monkeypatch.setattr(validate, "_run", deselected)
    assert "no test is deferred" in validate._slow_tests(context)

    monkeypatch.setattr(validate, "_run", broken)
    with pytest.raises(validate.StepFailureError):
        validate._slow_tests(context)

    monkeypatch.setattr(validate, "_run", broken_collection)
    with pytest.raises(validate.StepFailureError, match="command exited 2"):
        validate._slow_tests(context)


@pytest.mark.parametrize("worker_failure", [False, True], ids=["empty", "worker-failure"])
def test_slow_lane_distinguishes_worker_collection_failure_from_empty_selection(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, *, worker_failure: bool
) -> None:
    """xdist can return exit 5 after all workers fail before collecting any tests."""
    tests = tmp_path / "tests"
    tests.mkdir()
    (tmp_path / "pytest.ini").write_text("[pytest]\nmarkers = slow: deferred tests\n")
    if worker_failure:
        (tmp_path / "conftest.py").write_text(
            dedent("""
                import pytest

                def pytest_configure(config):
                    if hasattr(config, "workerinput"):
                        raise pytest.UsageError("worker cannot collect the slow lane")
                """)
        )
    (tests / "test_slow.py").write_text(
        "import pytest\n"
        + ("@pytest.mark.slow\n" if worker_failure else "")
        + "def test_selected():\n    pass\n"
    )
    commands: list[tuple[str, ...]] = []
    run = validate._run

    def run_here(context: validate.Context, command: tuple[str, ...]) -> str:
        commands.append(command)
        return run(context, command, cwd=tmp_path)

    monkeypatch.setattr(validate, "_run", run_here)
    monkeypatch.setattr(validate, "_pytest_workers", lambda _jobs: 2)
    monkeypatch.setattr(validate, "BEHAVIORAL_TEST_ROOTS", ("tests",))
    environment = os.environ.copy()
    for name in ("PYTEST_ADDOPTS", "PYTEST_XDIST_WORKER", "PACKING_VALIDATION_ARTIFACT_DIR"):
        environment.pop(name, None)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=environment,
        timeout_seconds=30,
    )
    if worker_failure:
        with pytest.raises(validate.StepFailureError, match="command exited 5") as raised:
            validate._slow_tests(context)
        assert "worker cannot collect the slow lane" in str(raised.value)
    else:
        assert "no test is deferred" in validate._slow_tests(context)
    assert len(commands) == 2
    assert "-n" in commands[0]
    assert "--collect-only" in commands[1]
    assert "-n" not in commands[1]


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
    `test_the_slow_marker_is_declared_only_by_measured_nodes` counts 66 functions and 96
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


def _cpu_duration_line(seconds: float, phase: str, node: str) -> str:
    """One line in the shape `devtools/cpu_durations.py` actually prints.

    Transcribed from that module's own f-string rather than approximated, and the padding
    is the reason it is worth a helper: pytest pads the phase name to eight columns, so a
    fixture that wrote a single space would be read by a pattern that also expected one
    and would prove nothing about the output the gate really meets.
    """
    return f"{seconds:02.2f}s cpu-lower-bound {phase:<8} {node}"


def test_cpu_observations_above_the_report_filter_do_not_fail_the_surface(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """CPU counters include work performed outside the reported test call."""
    ceiling = validate.QUICK_TEST_CPU_REPORT_SECONDS
    output = (
        "============================= slowest durations ==========================\n"
        f"{ceiling + 1.0:.2f}s call     tests/test_probe.py::test_that_grew\n"
        "(1904 durations < 12.00s hidden.  Use -vv to show these durations.)\n"
        "=============== slowest observed cpu durations (lower bounds) ============\n"
        "Incomplete descendant accounting; do not use for total CPU thresholds.\n"
        + _cpu_duration_line(ceiling + 7.0, "call", "tests/test_probe.py::test_that_grew")
        + "\n"
        + _cpu_duration_line(
            ceiling + 1.0, "setup", "tests/test_probe.py::test_with_a_costly_fixture"
        )
        + "\n"
        "1904 passed in 61.00s"
    )
    monkeypatch.setattr(validate, "_run", lambda *_a, **_k: output)
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )

    assert validate._fast_tests(context, 0) == output


def test_the_cpu_diagnostics_parser_reads_the_section_the_plugin_really_prints() -> None:
    """The one failure mode of this wiring that fails silently rather than loudly.

    pytest pads the phase name to eight columns. A pattern written with a single space
    matches no line at all, so the whole cpu section parses as an empty list -- and an
    empty list would conceal observations above the diagnostic display threshold.
    The header check cannot catch it, because the header is still printed. So the parser
    is checked against a line built the way the plugin builds it, with the padding in.
    """
    line = _cpu_duration_line(4.85, "call", "tests/test_probe.py::test_expensive")
    assert "call     " in line, "the fixture must carry the padding it exists to check"

    parsed = validate._call_durations(line, validate._CPU_DURATION_LINE)

    assert parsed == [(4.85, "tests/test_probe.py::test_expensive")]


def test_neither_durations_section_is_read_as_the_other() -> None:
    """Two measurements share one stream, so each parser must ignore the other's lines.

    `devtools/cpu_durations.py` holds this from its side; this is the same claim checked
    against the constants the gate itself uses. Reading one section as the other would be
    a ceiling comparing cpu seconds to wall readings, in whichever direction, and it would
    not announce itself.
    """
    wall = "13.69s call     tests/test_probe.py::test_contended"
    cpu = _cpu_duration_line(4.85, "call", "tests/test_probe.py::test_expensive")

    assert validate._call_durations(cpu) == []
    assert validate._call_durations(wall, validate._CPU_DURATION_LINE) == []
    assert validate._call_durations(wall) == [(13.69, "tests/test_probe.py::test_contended")]
    assert validate._call_durations(cpu, validate._CPU_DURATION_LINE) == [
        (4.85, "tests/test_probe.py::test_expensive")
    ]
    # The two headers must not match each other either: the wall check proves pytest
    # printed its section by looking for its header as a substring, and a cpu header
    # containing it would let a run that lost the wall section look like one that had it.
    assert validate._DURATION_HEADER not in validate._CPU_DURATION_HEADER


def _one_slow_call(seconds: float) -> str:
    """Quick-lane output with one test call of `seconds` wall and negligible CPU."""
    return (
        "============================= slowest durations ==========================\n"
        f"{seconds:.2f}s call     tests/test_probe.py::test_that_waits\n"
        "=============== slowest observed cpu durations (lower bounds) ============\n"
        "Incomplete descendant accounting; do not use for total CPU thresholds.\n"
        + _cpu_duration_line(0.02, "call", "tests/test_probe.py::test_that_waits")
        + "\n"
        "1904 passed in 61.00s"
    )


def test_a_slow_call_on_a_hosted_pull_request_is_reported_below_the_hang_limit(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Under `policy.pull_request_ceiling` (think-6erz) a 16 s call on a pull request is
    reported with a Cost warning and does not fail the shard."""
    relaxed = validate._pull_request_ceiling()
    assert relaxed is not None, "the live register no longer relaxes the per-test rule"
    output = _one_slow_call(validate.QUICK_TEST_WALL_BACKSTOP_SECONDS + 4.0)
    monkeypatch.setattr(validate, "_run", lambda *_a, **_k: output)
    monkeypatch.setattr(validate, "_hosted_pull_request", lambda *_a, **_k: True)
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )

    assert validate._fast_tests(context, 0) == output
    printed = capsys.readouterr().out
    assert "reported and not failed" in printed
    assert "::warning title=Cost::tests/test_probe.py::test_that_waits" in printed
    assert relaxed.advisory.tracking_bead in printed


def test_a_hung_call_on_a_hosted_pull_request_still_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The relaxation keeps the hang detector: a call at the per-test hang limit fails."""
    relaxed = validate._pull_request_ceiling()
    assert relaxed is not None
    output = _one_slow_call(relaxed.per_test_hang_seconds + 1.0)
    monkeypatch.setattr(validate, "_run", lambda *_a, **_k: output)
    monkeypatch.setattr(validate, "_hosted_pull_request", lambda *_a, **_k: True)
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )

    with pytest.raises(validate.StepFailureError, match="test_that_waits"):
        validate._fast_tests(context, 0)


def test_a_test_expensive_by_waiting_is_caught_by_the_wall_backstop(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Long call wall time fails even when observed CPU is negligible, on any run that is
    not a hosted pull request (the only run the register's relaxation reaches)."""
    output = _one_slow_call(validate.QUICK_TEST_WALL_BACKSTOP_SECONDS + 4.0)
    monkeypatch.setattr(validate, "_run", lambda *_a, **_k: output)
    monkeypatch.setattr(validate, "_hosted_pull_request", lambda *_a, **_k: False)
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )

    with pytest.raises(validate.StepFailureError) as failure:
        validate._fast_tests(context, 0)

    message = str(failure.value)
    assert "test_that_waits" in message
    assert "call wall time" in message


def test_a_quick_lane_under_the_ceiling_passes_and_still_reads_the_durations() -> None:
    """A durations section reporting nothing is read, not mistaken for an unread one.

    Both lanes fail closed on a missing section, so the empty-but-present case has to be
    distinguishable from it: pytest prints the header and a "hidden" line whenever every
    test is under `--durations-min`, and that is a passing lane rather than a broken one.
    The CPU diagnostic section may also be empty when no observations exceed its
    display filter; its header must still be present.
    """
    header = "============================= slowest durations ====================="
    assert validate._call_durations(f"{header}\n(9 durations < 12.00s hidden.)") == []
    assert validate._call_durations(
        f"{header}\n99.00s call     tests/test_probe.py::test_slow"
    ) == [(99.0, "tests/test_probe.py::test_slow")]

    cpu_header = f"====== {validate._CPU_DURATION_HEADER} ======"
    empty_cpu = (
        f"{cpu_header}\n"
        "Incomplete descendant accounting; do not use for total CPU thresholds.\n"
        "(9 CPU lower bounds < 6s or beyond --cpu-durations hidden.)"
    )
    assert validate._call_durations(empty_cpu, validate._CPU_DURATION_LINE) == []
    assert validate._CPU_DURATION_HEADER in empty_cpu


@pytest.mark.parametrize(
    ("output", "missing"),
    [
        pytest.param("1904 passed in 61.00s", "cpu", id="neither-section"),
        pytest.param(
            "==== slowest durations ====\n(9 durations < 12.00s hidden.)\n"
            "1904 passed in 61.00s",
            "cpu",
            id="wall-only",
        ),
        pytest.param(
            f"==== {validate._CPU_DURATION_HEADER} ====\n"
            "Incomplete descendant accounting; do not use for total CPU thresholds.\n"
            "1904 passed in 61.00s",
            "wall",
            id="cpu-only",
        ),
    ],
)
def test_the_ceiling_check_refuses_output_it_cannot_read(
    monkeypatch: pytest.MonkeyPatch, output: str, missing: str
) -> None:
    """Fail closed on either section, because a silent pass is the failure mode here.

    A threshold that reads an empty list finds no violations forever and says nothing
    about it. Each section is therefore proved present by its header before it is read,
    and one section arriving is not evidence about the other: the plugin's header and
    pytest's are separately renameable, and the `wall-only` case is what a lost `-p
    devtools.cpu_durations` looks like from here.
    """
    monkeypatch.setattr(validate, "_run", lambda *_a, **_k: output)
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )

    with pytest.raises(validate.StepFailureError) as failure:
        validate._fast_tests(context, 0)

    message = str(failure.value)
    assert "went unchecked" in message
    expected = validate._CPU_DURATION_HEADER if missing == "cpu" else validate._DURATION_HEADER
    assert repr(expected) in message


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
        *validate.BEHAVIORAL_TEST_ROOTS,
        "-m",
        "exhaustive_exact",
        "--durations=0",
        "--durations-min=0",
    )


def test_exhaustive_shard_uses_the_recorded_whole_file_partition(
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
        inner_jobs=4,
        environment=os.environ.copy(),
        exhaustive_shard="2/3",
    )

    validate._exhaustive_exact_tests(context)

    assert observed == (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        *validate.BEHAVIORAL_TEST_ROOTS,
        "-m",
        "exhaustive_exact",
        "-p",
        "devtools.suite_files",
        "--suite-shard=2/3",
        "--suite-file-costs=devtools/exhaustive-file-costs.json",
        "--suite-unrecorded-share=1",
        "--durations=0",
        "--durations-min=0",
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
        ("--frontend",),
        ("--geometry",),
        ("--suite-a",),
        ("--suite-b",),
        ("--suite-c",),
        ("--suite-d",),
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
    assert not any(step.name.startswith("fast behavioral tests") for step in selected)
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


@pytest.mark.parametrize(
    ("host_system", "library_name"),
    [("Linux", "libcairo.2.dylib"), ("Darwin", None)],
    ids=["non-macos", "missing-library"],
)
def test_validation_environment_changes_only_a_macos_host_with_homebrew_cairo(
    tmp_path: Path, host_system: str, library_name: str | None
) -> None:
    library_directory = tmp_path / "lib"
    library_directory.mkdir()
    if library_name is not None:
        (library_directory / library_name).touch()

    environment = validate._validation_environment(
        {"PATH": "/usr/bin"},
        host_system=host_system,
        cairo_library_directories=(library_directory,),
    )

    assert environment == {"PATH": "/usr/bin"}


def test_validation_environment_adds_discovered_homebrew_cairo(tmp_path: Path) -> None:
    library_directory = tmp_path / "lib"
    library_directory.mkdir()
    (library_directory / "libcairo.2.dylib").touch()

    environment = validate._validation_environment(
        {"PATH": "/usr/bin"},
        host_system="Darwin",
        cairo_library_directories=(library_directory,),
    )

    assert environment["DYLD_FALLBACK_LIBRARY_PATH"] == str(library_directory)


def test_validation_environment_preserves_an_explicit_cairo_loader_path(
    tmp_path: Path,
) -> None:
    library_directory = tmp_path / "lib"
    library_directory.mkdir()
    (library_directory / "libcairo.2.dylib").touch()

    environment = validate._validation_environment(
        {"DYLD_FALLBACK_LIBRARY_PATH": ""},
        host_system="Darwin",
        cairo_library_directories=(library_directory,),
    )

    assert environment["DYLD_FALLBACK_LIBRARY_PATH"] == ""


def test_main_passes_the_discovered_cairo_path_to_validation_children(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    library_directory = tmp_path / "lib"
    library_directory.mkdir()
    (library_directory / "libcairo.2.dylib").touch()
    monkeypatch.delenv("DYLD_FALLBACK_LIBRARY_PATH", raising=False)
    monkeypatch.setattr(validate.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(validate, "MACOS_CAIRO_LIBRARY_DIRECTORIES", (library_directory,))
    observed: validate.Context | None = None

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

    status, _, stderr = _invoke("--edit")

    assert status == 0
    assert stderr == ""
    assert observed is not None
    assert observed.environment["DYLD_FALLBACK_LIBRARY_PATH"] == str(library_directory)


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


@pytest.mark.parametrize(("tier", "expected_status"), [("typecheck", 1), (None, 0)])
def test_an_unknown_budget_fails_only_a_whole_tier(
    tier: str | None, expected_status: int
) -> None:
    summary = validate.RunSummary(
        results=[],
        wall_seconds=0.1,
        selected_count=1,
        total_count=1,
        budget=gate_budgets.Verdict(
            tier=tier,
            wall_seconds=0.1,
            status="unknown",
            notes=("the tier register could not be read",),
        ),
    )
    stdout = io.StringIO()

    with redirect_stdout(stdout):
        status = validate._render_text(summary, strict=False)

    assert status == expected_status
    if tier is not None:
        assert "DECLARED COST COULD NOT BE JUDGED" in stdout.getvalue()


def test_a_budget_only_failure_prints_a_machine_readable_pass_count() -> None:
    summary = validate.RunSummary(
        results=[],
        wall_seconds=10.0,
        selected_count=49,
        total_count=80,
        budget=gate_budgets.Verdict(
            tier="checks",
            wall_seconds=10.0,
            status="failed",
            failures=("the recorded cost is stale",),
        ),
    )
    stdout = io.StringIO()

    with redirect_stdout(stdout):
        status = validate._render_text(summary, strict=False)

    assert status == 1
    assert "49 of 80 STEPS PASSED (the budget verdict alone failed)" in stdout.getvalue()


def _hosted(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, hosted: bool) -> Path:
    """A GitHub step's own environment, or none of it; returns the summary file's path."""
    summary = tmp_path / "step-summary.md"
    if hosted:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
        monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    else:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
        monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    return summary


def _render(summary: validate.RunSummary, *, strict: bool = False) -> tuple[int, list[str]]:
    stdout = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(io.StringIO()):
        status = validate._render_text(summary, strict=strict)
    return status, stdout.getvalue().splitlines()


def _suite_a_verdict(
    wall: float, *, failures: tuple[str, ...] = ("the suite_a tier ran over",)
) -> gate_budgets.Verdict:
    return gate_budgets.Verdict(
        tier="suite_a",
        wall_seconds=wall,
        status="failed" if failures else "passed",
        enforced=True,
        ceiling_seconds=131.0,
        measured_seconds=114.58,
        failures=failures,
    )


def test_a_failed_test_is_named_by_the_closing_failure_class(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Real pytest output, so a change in pytest's short summary fails here, not in CI."""
    _ = _hosted(monkeypatch, tmp_path, hosted=False)
    (tmp_path / "test_demo.py").write_text(
        dedent(
            """
            import pytest

            def test_ok():
                pass

            def test_bad():
                assert 1 == 2, "one is not two"

            @pytest.fixture
            def broken():
                raise RuntimeError("fixture boom")

            def test_err(broken):
                pass

            @pytest.mark.parametrize("x", ["a b", "c"])
            def test_param(x):
                assert x == "c"
            """
        ),
        encoding="utf-8",
    )
    command = (sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "test_demo.py")
    completed = subprocess.run(
        command, cwd=tmp_path, capture_output=True, text=True, check=False
    )
    assert completed.returncode == 1
    reason = f"command exited 1: {' '.join(command)}\n{completed.stdout}"
    summary = validate.RunSummary(
        results=[
            validate.StepResult("lint floor", "passed", 1.0),
            validate.StepResult("fast behavioral tests, shard A", "failed", 9.0, reason=reason),
        ],
        wall_seconds=10.0,
        selected_count=2,
        total_count=98,
        budget=_suite_a_verdict(10.0, failures=()),
    )

    status, lines = _render(summary)

    assert status == 1
    assert "1 STEP FAILED:" in lines
    assert lines[-1] == (
        "FAILURE CLASS: tests failed (3 failures: test_demo.py::test_bad, "
        "test_demo.py::test_param[a b], test_demo.py::test_err)"
    )
    assert not any(line.startswith("::") for line in lines)


@pytest.mark.parametrize("rule", ["ceiling", "floor"])
def test_a_per_test_wall_failure_is_its_own_class(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, rule: str
) -> None:
    """Driven through the raising lanes, so the class follows their own headline."""
    _ = _hosted(monkeypatch, tmp_path, hosted=False)
    seconds = "13.40" if rule == "ceiling" else "0.40"
    output = (
        "==== slowest durations ====\n"
        f"{seconds}s call     tests/test_x.py::test_slow\n"
        "==== slowest observed cpu durations (lower bounds) ====\n"
    )
    monkeypatch.setattr(validate, "_run", lambda *_args, **_kwargs: output)
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=1, environment=os.environ.copy()
    )
    lane = (
        (lambda: validate._fast_tests(context, 1))
        if rule == "ceiling"
        else (lambda: validate._slow_tests(context))
    )
    with pytest.raises(validate.StepFailureError) as raised:
        lane()
    summary = validate.RunSummary(
        results=[validate.StepResult("a lane", "failed", 20.0, reason=str(raised.value))],
        wall_seconds=20.0,
        selected_count=1,
        total_count=98,
    )

    status, lines = _render(summary)

    expected = (
        "per-test wall ceiling failed (1 test at or above 12 s: "
        "tests/test_x.py::test_slow 13.40 s)"
        if rule == "ceiling"
        else "per-test wall floor failed (1 slow-marked test under 1 s: "
        "tests/test_x.py::test_slow 0.40 s)"
    )
    assert status == 1
    assert lines[-1] == f"FAILURE CLASS: {expected}"


@pytest.mark.parametrize("hosted", [True, False])
def test_a_budget_only_failure_names_the_tier_its_wall_and_its_ceiling(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, hosted: bool
) -> None:
    """Every step green and the wall over: the class and both numbers, without the log.

    On a hosted step the same line is a warning annotation on the checks page and a block
    in the job's step summary. The exit status is the one this class always had.
    """
    target = _hosted(monkeypatch, tmp_path, hosted=hosted)
    summary = validate.RunSummary(
        results=[validate.StepResult("fast behavioral tests, shard A", "passed", 134.0)],
        wall_seconds=134.2,
        selected_count=1,
        total_count=98,
        budget=_suite_a_verdict(134.2),
    )

    status, lines = _render(summary)

    verdict = "budget verdict alone failed (tier suite_a: 134.2 s vs ceiling 131 s)"
    assert status == 1
    assert "1 of 98 STEPS PASSED (the budget verdict alone failed)" in lines
    assert lines[-1] == f"FAILURE CLASS: {verdict}"
    annotation = f"::warning title=budget::{verdict}; every selected step passed"
    assert (annotation in lines) is hosted
    assert not any(line.startswith("::error") for line in lines)
    if hosted:
        written = target.read_text(encoding="utf-8")
        assert "### packing-validate failed: tier `suite_a`" in written
        assert f"**Failure class:** {verdict}" in written
        assert "  134.20s  wall of a 131s ceiling (102%), recorded 114.58s" in written
    else:
        assert not target.exists()


def test_a_record_relative_budget_failure_names_the_rule_that_fired(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    _ = _hosted(monkeypatch, tmp_path, hosted=False)
    summary = validate.RunSummary(
        results=[],
        wall_seconds=40.0,
        selected_count=1,
        total_count=98,
        budget=_suite_a_verdict(40.0),
    )

    _, lines = _render(summary)

    assert lines[-1] == (
        "FAILURE CLASS: budget verdict alone failed (tier suite_a: 40.0 s vs ceiling 131 s; "
        "the stale rule against the recorded 114.58 s)"
    )


def test_failing_tests_beside_a_failed_budget_name_both_classes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    target = _hosted(monkeypatch, tmp_path, hosted=True)
    reason = (
        "command exited 1: python -m pytest -q tests\n"
        "=========================== short test summary info ============================\n"
        "FAILED tests/test_x.py::test_a - AssertionError: 100% wrong\n"
        "1 failed, 2000 passed in 133.00s (0:02:13)"
    )
    summary = validate.RunSummary(
        results=[
            validate.StepResult(
                "fast behavioral tests, shard A", "failed", 134.0, reason=reason
            ),
            validate.StepResult(
                "lint floor",
                "failed",
                900.0,
                reason="command timed out after 900 seconds: ruff",
            ),
        ],
        wall_seconds=134.2,
        selected_count=2,
        total_count=98,
        budget=_suite_a_verdict(134.2),
    )

    status, lines = _render(summary)

    assert status == 1
    assert lines[-1] == (
        "FAILURE CLASS: tests failed (1 failure: tests/test_x.py::test_a); "
        "1 step failed (lint floor [timed out after 900 s]); "
        "budget verdict also failed (tier suite_a: 134.2 s vs ceiling 131 s)"
    )
    # Titles escape `:` and `,`; messages escape `%`, the way GitHub's commands require.
    assert (
        "::error title=Tests failed%3A 1 failure in fast behavioral tests%2C shard A::"
        "tests/test_x.py::test_a - AssertionError: 100%25 wrong"
    ) in lines
    assert "::error title=Validation step failed%3A lint floor::timed out after 900 s" in lines
    assert (
        "::warning title=budget::budget verdict also failed "
        "(tier suite_a: 134.2 s vs ceiling 131 s)"
    ) in lines
    written = target.read_text(encoding="utf-8")
    assert "- **Tests failed** in fast behavioral tests, shard A: 1" in written
    assert "  - `tests/test_x.py::test_a`: AssertionError: 100% wrong" in written
    assert "- **Step failed:** lint floor (timed out after 900 s)" in written


def test_a_passing_run_reports_no_failure_class(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    target = _hosted(monkeypatch, tmp_path, hosted=True)
    summary = validate.RunSummary(
        results=[validate.StepResult("lint floor", "passed", 1.0)],
        wall_seconds=1.0,
        selected_count=1,
        total_count=1,
        budget=_suite_a_verdict(1.0, failures=()),
    )

    status, lines = _render(summary)

    assert status == 0
    assert not any(line.startswith(("FAILURE CLASS", "::")) for line in lines)
    assert not target.exists()


def test_the_gate_keeps_the_step_summary_from_its_steps(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """A shard's tests render failing summaries on purpose; none may reach the job's."""
    target = _hosted(monkeypatch, tmp_path, hosted=True)
    observed: validate.Context | None = None

    def capture_context(
        selected: list[validate.Step], context: validate.Context, *_narrowing: object
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

    status, _, _ = _invoke("--records")

    assert status == 0
    assert observed is not None
    assert "GITHUB_STEP_SUMMARY" not in observed.environment
    assert os.environ["GITHUB_STEP_SUMMARY"] == str(target)
    assert not target.exists()


@pytest.mark.parametrize("hosted", [True, False])
def test_an_advisory_budget_verdict_prints_its_findings_and_passes(
    monkeypatch: pytest.MonkeyPatch, *, hosted: bool
) -> None:
    """A finding the register has declared advisory is printed in full, annotated on a
    hosted run so the pull request shows it, and does not fail the command."""
    if hosted:
        monkeypatch.setenv("GITHUB_ACTIONS", "true")
    else:
        monkeypatch.delenv("GITHUB_ACTIONS", raising=False)
    finding = "the checks tier ran 62.3s against a recorded 114.34s, which is 0.54x"
    summary = validate.RunSummary(
        results=[],
        wall_seconds=62.3,
        selected_count=54,
        total_count=85,
        budget=gate_budgets.Verdict(
            tier="checks",
            wall_seconds=62.3,
            status="advisory",
            enforced=True,
            ceiling_seconds=140.0,
            measured_seconds=114.34,
            advisory_failures=(finding,),
            advisory=gate_budgets.Advisory("think-aaaa", "a fabricated owner decision"),
        ),
    )
    stdout = io.StringIO()

    with redirect_stdout(stdout):
        status = validate._render_text(summary, strict=False)

    printed = stdout.getvalue()
    assert status == 0
    assert "FAIL (advisory, not enforced): " + finding in printed
    assert (
        "THE TIER IS OUTSIDE ITS RECORDED BAND (advisory, not enforced under think-aaaa):"
        in printed
    )
    assert f"  - {finding}" in printed
    assert "54 of 85 STEPS PASSED (a named tier; this is not the full gate)" in printed
    annotation = f"::warning title=Tier cost band (advisory under think-aaaa)::{finding}"
    assert (annotation in printed) is hosted
    # `read_tier_walls` must still count this log as a reading at the reference shape.
    assert "reported and not enforced" not in printed
    assert "THE TIER IS OUTSIDE ITS DECLARED COST BAND:" not in printed


def test_a_hosted_pull_request_is_read_from_the_runner_s_own_variables() -> None:
    """Only a GitHub Actions job on a `pull_request` event is one; nothing run by hand."""
    assert validate._hosted_pull_request(
        {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "pull_request"}
    )
    assert not validate._hosted_pull_request(
        {"GITHUB_ACTIONS": "true", "GITHUB_EVENT_NAME": "push"}
    )
    assert not validate._hosted_pull_request({"GITHUB_EVENT_NAME": "pull_request"})
    assert not validate._hosted_pull_request({})


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


def test_concurrent_commands_join_in_declared_order_and_report_the_first_declared_failure(
    tmp_path: Path,
) -> None:
    """`exact verification`'s seventeen subprocesses run at once and must read as serial.

    The step checks its joined output for substrings, so the join is in declared order
    whichever command finishes first; and a failure reports the earliest declared command
    that failed -- the one the serial loop would have stopped on -- so which error a run
    names does not depend on scheduling.
    """
    context = _budget_context(timeout_seconds=30, explicit=False)
    slow_first = (
        (sys.executable, "-c", "import time; time.sleep(0.4); print('first')"),
        (sys.executable, "-c", "print('second')"),
        (sys.executable, "-c", "print('third')"),
    )
    started = time.perf_counter()
    output = validate._concurrent_commands(context, slow_first, workers=3)
    assert output.splitlines() == ["first", "second", "third"]
    assert time.perf_counter() - started < 2.0

    marker = tmp_path / "never-started"
    failing = (
        (sys.executable, "-c", "import time; time.sleep(0.4); raise SystemExit(11)"),
        (sys.executable, "-c", "raise SystemExit(12)"),
        (sys.executable, "-c", "import time; time.sleep(1.5)"),
        (sys.executable, "-c", f"from pathlib import Path; Path({str(marker)!r}).touch()"),
    )
    with pytest.raises(validate.StepFailureError, match="command exited 11"):
        validate._concurrent_commands(context, failing, workers=2)
    # The 1.5s command held a worker, so the fourth was still queued when the first
    # failure arrived and was cancelled rather than started.
    assert not marker.exists()
    # A failure inside the step is the step's own: it does not stop the validation run, so
    # the gate's other steps can still start subprocesses.
    assert not context.processes.stopping


def test_exact_verification_takes_the_cpus_its_neighbours_leave(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Two of four cpus at the pull request's `--checks --jobs 3`, serial where `--jobs`
    already fills the machine -- the same `cpus - jobs + 1` the quick lane sizes by.

    And the step asks for that bound rather than running its list serially: the pool was
    dropped once without a recorded decision (`think-5hfr`), and nothing failed.
    """
    monkeypatch.setattr(os, "process_cpu_count", lambda: 4)
    assert validate._command_workers(3) == 2
    assert validate._command_workers(4) == 1
    assert validate._command_workers(1) == 4

    requested: list[tuple[int, int]] = []

    def record(
        _context: validate.Context,
        commands: tuple[tuple[str, ...], ...],
        *,
        workers: int,
        **_options: object,
    ) -> str:
        requested.append((len(commands), workers))
        raise validate.StepFailureError("recorded")

    def serial(*_arguments: object, **_options: object) -> str:
        message = "exact verification ran its members serially"
        raise AssertionError(message)

    monkeypatch.setattr(validate, "_concurrent_commands", record)
    monkeypatch.setattr(validate, "_commands", serial)
    context = validate.Context(deep=False, strict=False, jobs=3, inner_jobs=1, environment={})
    with pytest.raises(validate.StepFailureError, match="recorded"):
        validate._exact_verification(context)
    [(count, workers)] = requested
    assert count > 1
    assert workers == 2


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


def test_independent_command_groups_overlap_but_keep_serial_order_within_each(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    entered: set[str] = set()
    finished: list[str] = []

    def run(_context: validate.Context, command: tuple[str, ...], **_options: object) -> str:
        name = command[0]
        entered.add(name)
        if name in {"a1", "b1"}:
            deadline = time.monotonic() + 1
            while len(entered & {"a1", "b1"}) < 2 and time.monotonic() < deadline:
                time.sleep(0.001)
            assert entered & {"a1", "b1"} == {"a1", "b1"}
        finished.append(name)
        return name

    monkeypatch.setattr(validate, "_run", run)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={},
    )
    output = validate._command_groups(
        context,
        (
            (("a1",), ("a2",)),
            (("b1",), ("b2",)),
        ),
    )
    assert finished.index("a1") < finished.index("a2")
    assert finished.index("b1") < finished.index("b2")
    assert output.splitlines() == ["a1", "a2", "b1", "b2"]


def _python(source: str) -> tuple[str, ...]:
    return (sys.executable, "-c", source)


def _isolated_context(jobs: int) -> validate.Context:
    """A context whose subprocesses write no gate artifacts, whatever runs this test."""
    environment = os.environ.copy()
    environment.pop("PACKING_VALIDATION_ARTIFACT_DIR", None)
    return validate.Context(
        deep=False, strict=False, jobs=jobs, inner_jobs=1, environment=environment
    )


def _failing_groups_step() -> validate.Step:
    """A step whose command groups fail with an ordinary nonzero exit (`think-63ra`)."""

    def action(context: validate.Context) -> str:
        return validate._command_groups(
            context,
            (
                (_python("import time; time.sleep(0.3); raise SystemExit(3)"),),
                (_python("print('sibling group')"),),
            ),
        )

    return validate.Step("command groups that fail", action, fast=True)


def test_a_failing_command_group_finishes_its_siblings_and_names_the_first_declared(
    tmp_path: Path,
) -> None:
    """Running groups finish, and the error is the earliest declared group's, whichever
    group failed first -- so the failure a run reports does not depend on scheduling."""
    marker = tmp_path / "sibling-finished"
    context = _isolated_context(jobs=1)
    with pytest.raises(validate.StepFailureError, match="command exited 3"):
        validate._command_groups(
            context,
            (
                (_python("import time; time.sleep(0.6); raise SystemExit(3)"),),
                (_python("raise SystemExit(4)"),),
                (
                    _python(
                        "import time; from pathlib import Path; time.sleep(1.2); "
                        f"Path({str(marker)!r}).touch()"
                    ),
                ),
            ),
        )
    assert marker.exists()
    assert not context.processes.stopping


def test_a_failing_command_group_does_not_kill_a_concurrent_step(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """At `--jobs 2`, a group's nonzero exit fails its own step and nothing beside it.

    Before `think-63ra` the failure stopped the run-wide process registry, and the
    unrelated step running beside it reported `command exited -15`.
    """
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")

    def neighbour(context: validate.Context) -> str:
        return validate._run(context, _python("import time; time.sleep(2); print('ok')"))

    steps = [
        _failing_groups_step(),
        validate.Step("an unrelated concurrent step", neighbour, fast=True),
    ]
    summary = validate._run_selected(steps, _isolated_context(jobs=2), [])
    failing, unrelated = summary.results
    assert failing.status == "failed"
    assert "command exited 3" in failing.reason
    assert (unrelated.status, unrelated.reason) == ("passed", "")


def test_a_failing_command_group_does_not_refuse_later_steps(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """At `--jobs 1`, a step that starts after a group's failure still runs its commands.

    Before `think-63ra` the registry stayed stopping for the rest of the run, so every
    later step reported `validation is stopping; rejected new subprocess`.
    """
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")

    def later(context: validate.Context) -> str:
        return validate._run(context, _python("print('later step ran')"))

    steps = [_failing_groups_step(), validate.Step("a later step", later, fast=True)]
    summary = validate._run_selected(steps, _isolated_context(jobs=1), [])
    failing, following = summary.results
    assert failing.status == "failed"
    assert (following.status, following.output) == ("passed", "later step ran")


class _Interrupt(KeyboardInterrupt):
    """A `KeyboardInterrupt`-class exception raised from inside one group or command."""


def _groups_pool(
    context: validate.Context, first: tuple[str, ...], second: tuple[str, ...]
) -> str:
    return validate._command_groups(context, ((first,), (second,)))


def _bounded_pool(
    context: validate.Context, first: tuple[str, ...], second: tuple[str, ...]
) -> str:
    return validate._concurrent_commands(context, (first, second), workers=2)


@pytest.mark.parametrize("pool", [_groups_pool, _bounded_pool], ids=["groups", "bounded"])
def test_an_interrupt_inside_a_command_pool_still_stops_the_whole_run(
    pool: Callable[[validate.Context, tuple[str, ...], tuple[str, ...]], str],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Only an exception that is not an `Exception` stops every subprocess the run owns.

    The other half of `think-63ra`: keeping ordinary failures inside the step must not
    also keep an interrupt there. A 30-second sibling is killed rather than awaited, and
    the registry refuses anything started afterwards.
    """
    run = validate._run

    def interrupting(
        context: validate.Context,
        command: tuple[str, ...],
        *,
        cwd: Path = validate.PROJECT_ROOT,
    ) -> str:
        if command == ("interrupt",):
            deadline = time.monotonic() + 5
            while not context.processes._pids and time.monotonic() < deadline:
                time.sleep(0.01)
            raise _Interrupt
        return run(context, command, cwd=cwd)

    monkeypatch.setattr(validate, "_run", interrupting)
    context = _isolated_context(jobs=1)
    sleeper = _python("import time; time.sleep(30)")
    started = time.monotonic()
    with pytest.raises(_Interrupt):
        pool(context, sleeper, ("interrupt",))
    assert time.monotonic() - started < 15
    assert context.processes.stopping


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
    # The corpus summary is a corpus fact and follows KNOWN_BEST_CORPUS; the split is
    # pinned per corpus so a record silently changing status still fails (think-93on).
    proved, open_cases = FRONTIER_LANE_SPLIT[validate.KNOWN_BEST_CORPUS.label]
    corpus = validate.KNOWN_BEST_CORPUS
    assert (
        f"{corpus.count} artifacts, n = {corpus.label[2:]}; formal lane: "
        f"{proved} proved, {open_cases} open"
    ) in stdout
    # T-062 to T-064, T-066 and T-067 close fourteen cases in the reported lane; three of
    # them, n = 59, 60 and 61, are also closed in the formal lane since 2026-10-02.
    # Keep this expectation independent of the production count tuple.
    reported_proved, reported_open = REPORTED_LANE_SPLIT[corpus.label]
    assert f"reported lane: {reported_proved} proved, {reported_open} open" in stdout


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


def test_only_whole_suite_and_solo_steps_carry_budgets() -> None:
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
    every merge to main. The rule proposed then was that a fourth budgeted step would
    mean the shared cap needed revisiting instead of extending this set.
    The step `--push` builds outside this tuple is not a fourth: when its selector
    expands to the whole suite it runs the quick and slow lanes together, so it takes the
    constant that bounds both (D-432), which the next test holds.

    The set changed size twice on 2026-09-05 and stayed at three. `BC-214` split the
    behavioural suite by measured cost, and the two halves did not both keep the budget:
    `slow behavioral tests` inherited it, because it is the half that carries the wall,
    and `fast behavioral tests` gave it up, because a lane whose slowest test is capped
    at `QUICK_TEST_WALL_BACKSTOP_SECONDS` is no longer a step the shared cap is wrong for. An
    exception that is no longer needed is not harmless -- it is a guard switched off.

    The fourth arrived on 2026-09-08 with `D-484`, and the paragraph above said a fourth
    would mean the shared cap is wrong. That warning was written when every budgeted step
    shared a runner with fifty-seven short ones, and it is right about that case. The
    escape screen earned its budget elsewhere: `--only` puts it alone on its own
    post-merge job, where a single-step selection reports no tier and has no
    `gate-budgets.yaml` ceiling behind it, so on that job this number is the whole guard.
    But a budget is a property of the step and not of the job. `_execute_step_result`
    raises the cap for this step in every run whose cap nobody set by hand, through
    `--timeout-seconds` or its environment variable -- and that includes the full gate,
    `packing-validate` with no flags, 69 steps, the one AGENTS.md sends every agent
    through at a merge checkpoint. There the screen sits beside 68 short steps, and a hung
    screen takes 1800s to die instead of 900s, under the `full` tier's 3600s ceiling. That
    is what the fourth budget costs, and it is not nothing: a hang detector loosened by
    900s in the run with the most steps in it. It is paid only when the screen hangs, and
    it moves no other step's cap.

    So the set is two rules rather than one, and the exhaustive tier belongs to the
    second as much as the screen does. A step in the shared job earns a budget by running
    a whole suite, where a cap wide enough for it would stop guarding the short steps
    beside it. A step that owns a job carries one because nothing else bounds that job --
    and carries it into every other run too, which is the cost priced above. Raising the
    shared cap would answer neither: it would loosen the guard in the shared job, which is
    the trade this test exists to refuse, and it would not bound the solo jobs at all.

    Recorded honestly: the second budget was added by the coordinator during an
    unattended run and has not been independently reviewed.

    The fourth is a corpus sweep, rather than a suite: the whole translation escape
    screen at `n=1..324` timed out after 900s in hosted run 34196436989. It now carries
    the independent 1800s budget used by PR #116. The shared cap remains 900s for
    ordinary checks, including the sampled screen; a larger corpus does not justify
    extending every subprocess's deadline.
    """
    budgeted = {
        step.name: step.budget_seconds for step in validate.STEPS if step.budget_seconds
    }
    assert budgeted == {
        # Whole suites in the shared job.
        "negative controls": 1800,
        "slow behavioral tests": 1800,
        # Each alone on a post-merge job, where this number is the whole guard -- and
        # the step's wherever else it runs, the full gate included.
        "exhaustive exact behavioral tests": 3600,
        "single-square translation escape screen": 1800,
    }


@pytest.mark.parametrize(
    ("timeout_seconds", "explicit", "expected_timeout"),
    [(900.0, False, 1800.0), (7.0, True, 7.0), (2400.0, True, 2400.0)],
)
def test_whole_escape_screen_uses_its_budget_unless_the_operator_sets_a_cap(
    monkeypatch: pytest.MonkeyPatch,
    *,
    timeout_seconds: float,
    explicit: bool,
    expected_timeout: float,
) -> None:
    observed: list[float] = []

    def probe(context: validate.Context, module: str, *arguments: str) -> str:
        assert module == "devtools.screen_translation_escape"
        assert arguments == ("--check",)
        observed.append(context.timeout_seconds)
        return f"translation escape screen check passed: {validate._screen_findings()}"

    monkeypatch.setattr(validate, "_module", probe)
    step = next(
        step
        for step in validate.STEPS
        if step.name == "single-square translation escape screen"
    )
    context = _budget_context(timeout_seconds=timeout_seconds, explicit=explicit)
    result = validate._execute_step_result(step, context)

    assert result.status == "passed"
    assert observed == [expected_timeout]
    assert context.timeout_seconds == timeout_seconds


@pytest.mark.parametrize("last_n", [100, 200, 324])
def test_screen_findings_match_the_current_retained_square_motions(last_n: int) -> None:
    document = json.loads(
        (validate.PROJECT_ROOT / "atlas/known-best/translation-escape-screen.json").read_text()
    )["screen"]
    cases = document["cases"]
    assert [case["n"] for case in cases] == list(range(1, 325))
    assert document["excluded"] == []
    cases = [case for case in cases if case["n"] <= last_n]
    separating = [
        sum(square["witness_kind"] == "strict-separating" for square in case["movable_squares"])
        for case in cases
    ]
    moving = [len(case["movable_squares"]) for case in cases]
    assert separating == [case["separating_square_count"] for case in cases]
    assert moving == [case["movable_square_count"] for case in cases]
    assert validate.SCREEN_FINDINGS[f"n=1..{last_n}"] == (
        sum(count > 0 for count in separating),
        sum(separating),
        sum(count > 0 for count in moving),
        sum(moving),
    )


@pytest.mark.parametrize("sample", [False, True])
@pytest.mark.parametrize("stale", [False, True])
def test_screen_output_guards_accept_current_and_refuse_previous_pose_findings(
    monkeypatch: pytest.MonkeyPatch, *, sample: bool, stale: bool
) -> None:
    findings = validate._screen_findings()
    if stale:
        findings = (
            "324 records screened, 120 with a square that separates (1867 squares), "
            "302 with a square that translates at all (4511 squares), excluded: none"
        )
    output = (
        "translation escape screen sample check passed: 12 of 324 records replayed "
        f"(every 27th from n=1); retained screen: {findings}"
        if sample
        else f"translation escape screen check passed: {findings}"
    )
    monkeypatch.setattr(validate, "_module", lambda *_args: output)
    action = (
        validate._translation_escape_sample if sample else validate._translation_escape_screen
    )
    context = _budget_context(timeout_seconds=900.0, explicit=False)
    if stale:
        with pytest.raises(validate.StepFailureError, match="output omitted required text"):
            action(context)
    else:
        assert action(context) == output


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
    assert step.reachable_test_files == (None if expected_scope == "whole" else 7)
    assert step.budget_seconds == expected_budget
    assert (
        validate.STEPS[
            [s.name for s in validate.STEPS].index("slow behavioral tests")
        ].budget_seconds
        == validate.FAST_SUITE_BUDGET_SECONDS
    )


@pytest.mark.parametrize(
    "summary", ["", "narrow", "narrow 0", "narrow nope", "other", "noise\nnarrow 7"]
)
def test_push_refuses_a_missing_or_malformed_selector_summary(
    monkeypatch: pytest.MonkeyPatch, summary: str
) -> None:
    monkeypatch.setattr(
        validate.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess(
            args=("reachable-tests",), returncode=0, stdout=f"{summary}\n", stderr=""
        ),
    )
    with pytest.raises(validate.UsageError, match="no valid summary"):
        validate._push_test_step("origin/main")


@pytest.mark.parametrize("summary", ["everything", "narrow 7"])
def test_push_tests_forward_the_shared_worker_allocation(
    monkeypatch: pytest.MonkeyPatch, summary: str
) -> None:
    """The reachable runner must not become a serial copy of the quick and slow lanes."""

    def probe(*args: object, **kwargs: object) -> subprocess.CompletedProcess[str]:
        del args, kwargs
        return subprocess.CompletedProcess(
            args=("reachable-tests",), returncode=0, stdout=f"{summary}\n", stderr=""
        )

    commands: list[tuple[str, ...]] = []
    sized_for: list[int] = []

    def capture(context: validate.Context, command: tuple[str, ...]) -> str:
        del context
        commands.append(command)
        return "selected tests passed"

    def four_workers(jobs: int) -> int:
        sized_for.append(jobs)
        return 4

    monkeypatch.setattr(validate.subprocess, "run", probe)
    monkeypatch.setattr(validate, "_run", capture)
    monkeypatch.setattr(validate, "_pytest_workers", four_workers)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=2,
        inner_jobs=1,
        environment=os.environ.copy(),
    )

    assert validate._push_test_step("origin/main").action(context) == "selected tests passed"
    assert sized_for == [2]
    assert commands == [
        (
            sys.executable,
            "-m",
            "devtools.reachable_tests",
            "--run",
            "--since",
            "origin/main",
            "-n",
            "4",
        )
    ]


def test_exclusive_push_forwards_pytest_and_pool_worker_allocations(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(validate.os, "process_cpu_count", lambda: 10)
    monkeypatch.setattr(
        validate.subprocess,
        "run",
        lambda *_args, **_kwargs: subprocess.CompletedProcess(
            args=("reachable-tests",), returncode=0, stdout="narrow 114\n", stderr=""
        ),
    )
    commands: list[tuple[str, ...]] = []

    def capture(_context: validate.Context, command: tuple[str, ...]) -> str:
        commands.append(command)
        return "selected tests passed"

    monkeypatch.setattr(validate, "_run", capture)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
        pool_workers=10,
    )

    assert validate._push_test_step("origin/main").action(context) == "selected tests passed"
    assert commands[0][-4:] == ("-n", "10", "--pool-workers", "10")


@pytest.mark.parametrize(
    (
        "cpus",
        "broad",
        "selected_files",
        "arguments",
        "environment_jobs",
        "expected_jobs",
        "expected_inner_jobs",
        "exclusive",
    ),
    [
        (8, True, None, (), None, 8, 2, True),
        (8, False, 7, (), None, 8, 2, False),
        (8, False, 8, (), None, 8, 2, True),
        (8, False, 114, (), None, 8, 2, True),
        (1, False, 114, (), None, 1, 1, False),
        (8, True, None, ("--jobs", "3"), None, 3, 1, False),
        (8, True, None, (), "3", 3, 1, False),
        (8, True, None, ("--inner-jobs", "7"), None, 1, 7, False),
    ],
)
def test_implicit_large_push_reserves_an_exclusive_test_phase(
    monkeypatch: pytest.MonkeyPatch,
    *,
    cpus: int,
    broad: bool,
    selected_files: int | None,
    arguments: tuple[str, ...],
    environment_jobs: str | None,
    expected_jobs: int,
    expected_inner_jobs: int,
    exclusive: bool,
) -> None:
    """Large implicit selections reserve pytest; explicit resource choices still win."""
    if environment_jobs is None:
        monkeypatch.delenv("PACKING_VALIDATE_JOBS", raising=False)
    else:
        monkeypatch.setenv("PACKING_VALIDATE_JOBS", environment_jobs)
    monkeypatch.delenv("PACKING_VALIDATE_INNER_JOBS", raising=False)
    monkeypatch.setattr(validate.os, "process_cpu_count", lambda: cpus)
    monkeypatch.setattr(
        validate,
        "_push_test_step",
        lambda _base: validate.Step(
            name="reachable behavioral tests",
            action=lambda _context: "",
            fast=True,
            broad=broad,
            reachable_test_files=selected_files,
        ),
    )
    monkeypatch.setattr(validate, "_begin_artifacts", lambda _context, _selected: None)
    observed: list[validate.Context] = []

    def capture(
        selected: list[validate.Step],
        context: validate.Context,
        *_narrowing: object,
    ) -> validate.RunSummary:
        observed.append(context)
        return validate.RunSummary(
            results=[],
            wall_seconds=0,
            selected_count=len(selected),
            total_count=len(validate.STEPS),
        )

    monkeypatch.setattr(validate, "_run_selected", capture)

    status, _stdout, stderr = _invoke("--push", *arguments)

    assert status == 0
    assert stderr == ""
    assert len(observed) == 1
    assert observed[0].jobs == expected_jobs
    assert observed[0].inner_jobs == expected_inner_jobs
    assert observed[0].exclusive_step_name == (
        "reachable behavioral tests" if exclusive else ""
    )


def test_exclusive_push_phase_waits_for_parallel_edits_and_keeps_one_report_order(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The edit pool drains before pytest gets the host, with one final verdict."""
    monkeypatch.setattr(validate.os, "process_cpu_count", lambda: 10)
    marker = tmp_path / ".gate-running"
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", marker)
    rendezvous = Barrier(2, timeout=10)
    lock = Lock()
    active = 0
    completed: set[str] = set()

    def edit(name: str) -> validate.Step:
        def action(_context: validate.Context) -> str:
            nonlocal active
            with lock:
                active += 1
            try:
                rendezvous.wait()
                with lock:
                    completed.add(name)
                return name
            finally:
                with lock:
                    active -= 1

        return validate.Step(name, action, fast=True)

    def tests(context: validate.Context) -> str:
        assert marker.is_dir()
        with lock:
            assert active == 0
            assert completed == {"first edit", "second edit"}
        assert (context.jobs, context.inner_jobs) == (1, 1)
        assert context.environment["PACK_JOBS"] == "1"
        assert validate._pytest_workers(context.jobs) == 10
        assert context.pool_workers == 10
        return "reachable tests ran"

    steps = [
        edit("first edit"),
        validate.Step("reachable behavioral tests", tests, fast=True),
        edit("second edit"),
    ]
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=10,
        inner_jobs=3,
        environment={"PACK_JOBS": "3"},
        exclusive_step_name="reachable behavioral tests",
    )

    summary = validate._run_selected(steps, context, [])

    assert [result.name for result in summary.results] == [step.name for step in steps]
    assert [result.status for result in summary.results] == ["passed"] * 3
    assert context.environment["PACK_JOBS"] == "3"
    assert not marker.exists()


def test_exclusive_push_phase_keeps_edit_failures_and_runs_the_remaining_check(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")

    def failed(_context: validate.Context) -> str:
        raise validate.StepFailureError("edit check refused")

    def selected(_context: validate.Context) -> str:
        return "selected tests passed"

    steps = [
        validate.Step("edit check", failed, fast=True),
        validate.Step("reachable behavioral tests", selected, fast=True),
    ]
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=2,
        inner_jobs=1,
        environment={"PACK_JOBS": "1"},
        exclusive_step_name="reachable behavioral tests",
    )

    summary = validate._run_selected(steps, context, [])

    assert [(result.name, result.status) for result in summary.results] == [
        ("edit check", "failed"),
        ("reachable behavioral tests", "passed"),
    ]
    assert "edit check refused" in summary.results[0].reason


def test_large_narrow_push_keeps_its_floor_when_a_full_gate_holds_the_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    marker = tmp_path / ".gate-running"
    marker.mkdir()
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", marker)
    observed: list[tuple[int, int, str, int | None]] = []

    def selected(context: validate.Context) -> str:
        observed.append(
            (
                context.jobs,
                context.inner_jobs,
                context.environment["PACK_JOBS"],
                context.pool_workers,
            )
        )
        return "selected tests passed"

    step = validate.Step("reachable behavioral tests", selected, fast=True)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=10,
        inner_jobs=3,
        environment={"PACK_JOBS": "3"},
        exclusive_step_name=step.name,
    )

    summary = validate._run_selected([step], context, [])

    assert summary.results[0].status == "passed"
    assert observed == [(10, 3, "3", None)]
    assert marker.is_dir()


def test_exclusive_push_command_receipt_records_its_effective_worker_allocation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", tmp_path / ".gate-running")
    artifacts = tmp_path / "artifacts"

    def selected(context: validate.Context) -> str:
        return validate._run(context, (sys.executable, "-c", "print('selected')"))

    step = validate.Step("reachable behavioral tests", selected, fast=True)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=10,
        inner_jobs=3,
        environment={
            **os.environ,
            "PACK_JOBS": "3",
            "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts),
        },
        exclusive_step_name=step.name,
    )

    summary = validate._run_selected([step], context, [])

    assert [(result.status, result.output) for result in summary.results] == [
        ("passed", "selected")
    ]
    start = json.loads(next(artifacts.glob("command-*.start.json")).read_text())
    assert (start["jobs"], start["inner_jobs"], start["step_name"]) == (
        1,
        1,
        step.name,
    )
    assert start["run_id"] == context.artifact_run_id


def test_exclusive_push_interrupt_stops_run_and_releases_marker(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    marker = tmp_path / ".gate-running"
    monkeypatch.setattr(validate, "ACTIVITY_MARKER", marker)

    def interrupt(_context: validate.Context) -> str:
        raise KeyboardInterrupt

    step = validate.Step("reachable behavioral tests", interrupt, fast=True)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=2,
        inner_jobs=1,
        environment={"PACK_JOBS": "1"},
        exclusive_step_name=step.name,
    )

    with pytest.raises(KeyboardInterrupt):
        validate._run_selected([step], context, [])
    assert context.processes.stopping
    assert not marker.exists()


def test_exclusive_push_refuses_an_absent_selected_step() -> None:
    step = validate.Step("edit check", lambda _context: "passed", fast=True)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=2,
        inner_jobs=1,
        environment={},
        exclusive_step_name="reachable behavioral tests",
    )

    with pytest.raises(validate.StepFailureError, match="absent from the selection"):
        validate._run_selected([step], context, [])


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
    frontend = names(fast=False, frontend=True)
    sweeps = names(fast=False, sweeps=True)
    suite_a = names(fast=False, suite_a=True)
    suite_b = names(fast=False, suite_b=True)
    suite_c = names(fast=False, suite_c=True)
    suite_d = names(fast=False, suite_d=True)
    geometry = names(fast=False, geometry=True)
    typecheck = names(fast=False, typecheck=True)
    measure_verifier = names(fast=False, measure_verifier=True)

    assert records <= edit <= fast <= everything
    assert fast - edit == {step.name for step in validate.STEPS if step.broad}, (
        "the only steps --fast adds over --edit are the ones marked broad"
    )
    # The pull request's jobs are a partition of `--fast` rather than independent filters,
    # which is what makes it safe to run them on separate runners: no step can be in two
    # and none in none.
    parts = [
        checks,
        frontend,
        typecheck,
        geometry,
        suite_a,
        suite_b,
        suite_c,
        suite_d,
        sweeps,
        measure_verifier,
    ]
    assert set().union(*parts) == fast
    for index, part in enumerate(parts):
        for other in parts[index + 1 :]:
            assert not part & other
    # The cheap frontend source floor remains in `--edit`; the full-page browser contract
    # is broad. The other partition lanes remain wholly broad.
    assert edit <= checks | frontend | typecheck
    assert {step.name for step in validate.STEPS if step.frontend and not step.broad} == {
        "browser floor (biome, eslint, tsc, node:test)",
    }
    assert {step.name for step in validate.STEPS if step.typecheck} == {
        "type floor (basedpyright)",
    }
    assert all(step.broad for step in validate.STEPS if step.geometry), (
        "a non-broad step in --geometry would put part of --edit on a second runner"
    )
    assert not any(step.needs_engine for step in validate.STEPS if step.geometry), (
        "an engine step in --geometry would make both halves compile Rust"
    )


@pytest.mark.parametrize(
    "path",
    [
        "packing/devtools/dilation_corollary.py",
        "packing/devtools/decide_certificate.py",
    ],
)
def test_limit_record_tools_select_the_complete_exact_replay(path: str) -> None:
    for universe in (validate.STEPS, tuple(step for step in validate.STEPS if step.fast)):
        selection = validate.select_for_paths([path], universe)
        assert not selection.unattributed_paths
        assert "exact verification" in {step.name for step in selection.steps}


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
    if a new step landed in a `sweep`, `suite_a`, or `suite_b` set no job selected --
    three ways to lose a check that all look identical from inside `STEPS`. So the
    deferred set is computed as everything the pull-request jobs do not select, and the
    flag is checked against it afterwards rather than trusted as the answer.

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

    At that 2026-09-06 checkpoint, deferring a fourth meant arguing that the tier's wall
    time -- then `max(the checks job, the suite job, the sweeps job)` rather than one
    job's queue -- had moved. There is a fourth, and this is that historical argument.

    **A fifth and a sixth arrived on 2026-09-07, and what moved was the corpus rather
    than the gate.** The known-best atlas went from `n=1..100` to `n=1..324` -- 324 cases
    and 52,650 squares against 100 and 5,050 -- and two sweeps grew with it. Measured on
    an idle ten-cpu box at the sweeps job's own shape (`--jobs 4 --inner-jobs 2`), on
    commit `2841eec9`, with every reading retained under
    `benchmarks/gate-cost-at-324/runs/`:

    - `single-square translation escape screen` at **766.26s**, against 110.66s at
      `n=1..100`. It is already pooled and the pool is already sized by the tier's
      `--inner-jobs`, so this is what the lever buys, not what it costs unpulled. It is
      also within 134s of the gate's own 900s per-step subprocess timeout on a box faster
      than CI's, which is a step that has stopped fitting rather than one that is merely
      dear.
    - `known-best n=1..324 atlas rebuild` at **691.19s** of that step's 703.28s, against
      75.88s for the whole step at `n=1..100`. The seam is measured, not guessed: the
      seven other subcommands in the step cost 12.09s between them, and five of them are
      pinned at `CALIBRATION_CORPUS` by `D4` and cannot grow with the corpus at all.

    Both were made faster before either was deferred, which is the order `OR-13` asks
    for. `build_known_best_atlas` was given the process pool `screen_translation_escape`
    already had: 691.19s serial, 348.15s at two workers, 184.34s at four, over 677.66s
    and 688.74s of cpu against the serial run's 691.19s -- the pool divides the work
    rather than adding any, and `--check` passes at every count, which is what makes the
    parallel build byte-identical rather than merely quick. 184.34s is still most of the
    sweeps job's 210s ceiling on a box faster than the runner, so the speedup changes
    where the deferral lands rather than whether it is needed. It does decide the deep
    gate's shape: at that job's `--inner-jobs 2` the rebuild is 348.15s here, comfortably
    inside both the slow lane's 890s and the gate's own 900s per-step timeout.

    Neither is deferred without a stand-in, which is the difference between this and
    dropping a check. `known-best atlas records and sample` and `translation escape
    screen records and sample` are new steps on the sweeps job, and each re-derives the
    whole of its record layer -- the manifest but for its entries, the source index and
    every upstream digest, every frontier link, every composite receipt; the screen's
    aggregate, method block, schema and per-certificate claims -- and then rebuilds a
    fixed, recorded sample of the cases in full. So the drift `D-369` counts still fails
    a pull request in the minute it is introduced, and only per-case geometry waits for
    the deep gate.

    **A seventh arrived the same day, from the same corpus and on a different job.**
    `exact rational grid replay` is `devtools.check_basic_bounds` run whole, and it was
    the corpus-scaling member of `exact verification` on the `checks` job. What that job
    did on CI at commit `2841eec9` is the whole argument: 189.09s against a 195s ceiling
    and a recorded 99.39s, with the gate's own verdict naming `exact verification` as
    133.4s of it -- 70.6 per cent. Measured on an idle ten-cpu box, three readings
    apiece, with everything retained under `benchmarks/gate-cost-at-324/runs/`:

    - the step, 84.56s, 84.11s and 83.95s, spread 0.7 per cent;
    - `check_basic_bounds` inside it, 34.70s, 34.94s and 34.80s -- 41 per cent of the
      step, against 3.58s when `D-370` moved it here at `n=1..100`;
    - the sixteen other subcommands, 49.4s between them, every one a fixed case that
      cannot grow with the corpus.

    The cost is quadratic in the corpus's last `n` -- `verify_grid` buckets its pair
    enumeration, so a case is linear in its own `n` and the corpus is the sum -- which
    the tool's own `--max-n` measures: 2.75s at `n=1..100`, 12.65s at `n=1..200`, 34.81s
    at `n=1..324`. A widening to 400 would put it near 53s without anything else
    changing.

    It was made faster before it was deferred, and the speedup is why the deep gate can
    afford it. The replay is a map over independent cases, so it now asks
    `sqpack.workers.worker_count` for its pool exactly as `screen_translation_escape` and
    `build_known_best_atlas` do: 34.81s serial, 18.58s at two workers, 9.97s at four,
    over 34.8s, 36.6s and 38.5s of cpu, and the whole run's stdout is byte-for-byte
    identical at one worker and at four. What that does not do is help the job it was on:
    every pull-request tier passes `--inner-jobs 1`, so `PACK_JOBS` is 1 and the pooled
    step is the serial step there by design. The pool decides where the deferred copy can
    live, not whether the deferral is needed.

    The stand-in is the complement rather than a sample of the step. Every one of the 324
    cases still has its declared upper, area and Nagamochi bounds compared against their
    closed forms -- that half is 0.14s and never left -- and every ninth grid case is
    still replayed exactly, at 4.15s in place of 34.81s. What waits for the deep gate is
    the other eight ninths of the per-case geometry, on witnesses whose non-overlap is a
    property of the lattice they are built on.

    Nothing was deferred on 2026-09-06, and that is the point of recording it here. The
    tier had reached 501.97s and the obvious 468.11s of it to drop were the two atlas
    sweeps main had just promoted; the measurement refused that too. Those two are the
    class `D-369` counted -- a registry or generated view going stale is what actually
    fails CI here -- and a change that retains a witness or edits a source map is exactly
    what breaks them, so deferring them would have re-opened the gap `D-455` came through
    with the cheapest half of the evidence. The cost was bought from concurrency instead:
    a second runner, and then a third for the behavioural lane, both argued in
    `test_the_pull_request_runs_its_sweeps_and_its_suite_apart`, which changes when a
    check runs but not whether. This set held at four across both changes, and what took
    it to seven a day later was not a decision to carry less but a corpus that tripled:
    the same refusal applies to the record layer of all three, which is why the record
    layer stayed and only the per-case re-derivation left.

    **An eighth and a ninth arrived on 2026-09-09 with `T-024`.** The two `finer-net
    dilation-limit record` steps are `devtools.dilation_corollary --check-limit-record`
    on the two finer-net re-certifications of the retained `n = 11` atoms, and each
    check replays all five source conditions over 721 or 1441 directions before
    re-deriving its endpoint. Measured on the branch that registered the result, on a
    loaded four-cpu host at `PACK_JOBS=1`: 173s for the 720-step record and 352s for
    the 1440-step record, against `T-022`'s 181-direction check that stays on the
    surface. They are two steps so that neither waits on the other and each stays well
    inside the shared cap on the deep gate's serial schedule; neither carries a budget
    of its own. The stand-in is not a sample: on every pull request
    `test_every_case_page_binds_the_certificate_its_own_evidence_names` rehashes each
    record's source bytes and re-derives its supremum from the declared gap and shrink,
    so the promoted endpoint cannot be left looking current by a changed certificate.
    What waits for the deep gate is the five-condition replay behind the record, on a
    certificate whose own bytes the two-route gate decided when it was retained.

    **A tenth and an eleventh arrived the same day with `T-026`.** The two `threshold
    dilation-limit record` steps are the same check over the threshold re-certifications
    of the retained `n = 11` atoms, and each replays six conditions rather than five,
    by the threshold theorem's own exact event-cell sweep. Measured on the branch that
    registered the result, on a four-cpu host at `PACK_JOBS=1`: 618s for the 720-step
    record and 919s for the 1440-step record. They carry the same stand-in as T-024's,
    since `test_every_case_page_binds_the_certificate_its_own_evidence_names` reads the
    `v3` threshold record beside the `v2` point one. The separate standard-library
    reader embedded in the T-025 and T-026 claim documents is also an exhaustive check;
    it does not make either repository replay cheap enough for this tier.

    **A twelfth arrived on 2026-10-02 with `think-bgkz`.** `regularized atlas views
    re-derive exactly` is `devtools.regularize_axis_components --verify-atlas`: every
    record of the derived regularized layer regularized again from its witness, both
    exact verifications over `Q` re-run, and every view required byte-identical. It is
    about 800 cpu-seconds on a four-cpu host: 406.32s at two workers and 223.35s at four
    on 2026-10-02, on a host other sessions were also using. The `sweeps` job would give
    it `--inner-jobs 2`, about twice that job's 200s ceiling on its own, and a runner of
    its own at four workers would be about four minutes of pull-request wall with setup,
    past `OR-14`'s outer edge. The stand-in is the complement:
    `regularized atlas views match their index` runs in the records tier on every pull
    request and compares the index with the manifest, every source witness and every
    retained view by digest in about a tenth of a second, so a changed witness or an
    edited view still fails the pull request in the minute it lands. What waits for the
    deep gate is whether the code that now ships still earns the recorded verdicts.

    `slow behavioral tests` is `BC-214`. It is not a step that was never decided: it is
    the half of the behavioural suite that carries the wall, split out by measurement
    rather than by name. Of 2,251 collected tests, 92 are marked `slow` and 2,106 remain
    on the pull-request surface, and those 92 carried 890s of a 1,038s suite -- 86 per
    cent of the cost in 4 per cent of the tests. Removing them took the tier from
    1369.60s to 177.02s.

    It is the one deferral whose membership is *enforced* rather than listed, which is
    what makes it safe to have at all. `QUICK_TESTS` and `SLOW_TESTS` are complements, so
    a test cannot fall out of both; `fast behavioral tests` fails when a test it ran
    reports a `call` phase at or above `QUICK_TEST_WALL_BACKSTOP_SECONDS` of wall.
    CPU observations remain diagnostic because they cannot attribute earlier child work
    to an isolated call. `slow behavioral tests` fails when a
    deferred test reports below the marker floor, so one that stops being slow has to come
    back. The other three deferrals are a typed list. This one is a rule.

    And it defers cost without deferring detection, which is the distinction `OR-13`
    turns on: all eight failures CI caught on the `T-021` branch were sub-0.15s record
    comparisons, 0.46s of call time between them. The wall was never where the catching
    was.

    **A twelfth arrived on 2026-10-03 with the clean-room measure verifier.**
    `measure verifier full controls (sqverify-fast)` is `devtools.check_sqverify_fast`
    without `--quick`: 72.8s single threaded on an idle four-cpu box, 56.6s of it the
    mixed certificates' exact differentials and near-threshold controls, against about
    22s for the quick set. The quick set runs on every pull request in the
    `measure-verifier` job, and it keeps one of each kind of check: the differential
    against the exact oracle on one rectangle and one mixed certificate, the rectangle
    controls, the mixed `n = 101` packet's retained controls, the admission refusals and
    the fault injection. What waits for the deep gate is the second rectangle and the
    other directions, the mixed `n = 37` packet and the near-threshold controls. It runs
    in `deferred-controls-finer` beside the negative controls, which measured 621s against
    a 965s ceiling.
    """
    deferred = {step.name for step in validate.STEPS} - set().union(
        *_workflow_selections(pull_request=True).values()
    )

    assert deferred == {
        "exhaustive exact behavioral tests",
        "negative controls",
        "n=40 rigidity bracket still reproduces",
        "slow behavioral tests",
        "known-best n=1..324 atlas rebuild",
        "single-square translation escape screen",
        "exact rational grid replay",
        "finer-net dilation-limit record, 720 steps",
        "finer-net dilation-limit record, 1440 steps",
        "threshold dilation-limit record, 720 steps",
        "threshold dilation-limit record, 1440 steps",
        "measure verifier full controls (sqverify-fast)",
        "regularized atlas views re-derive exactly",
    }
    # And the same set is what `--fast` leaves out, so the flag and the workflow cannot
    # drift apart: a step marked `fast` that no pull-request job invokes is deferred in
    # fact and promoted on paper, which is the state think-k4fb found and this pins shut.
    assert deferred == {step.name for step in validate.STEPS if not step.fast}


def test_the_pull_request_runs_its_sweeps_and_its_suite_apart() -> None:
    """Which steps leave the `checks` job for a runner of their own, and why each did.

    `frontend`, `sweep`, `suite_a`, `suite_b`, `suite_c`, `suite_d`, `geometry`, and
    `typecheck` decide which pull-request job runs a step. All eight default to False, so
    forgetting one makes a slower `checks` job rather than a step nobody runs -- the safe
    direction, as with `broad` and `touches`. What needs a guard is the other direction: a
    step moved out to make the `checks` job look fast. Adding a name below means typing a
    number next to it.

    The measurements are CI's, run 34010470187 on a four-cpu runner: `--checks --jobs 3
    --inner-jobs 1` at 221.70s of wall over 58 steps, and `--sweeps --jobs 4
    --inner-jobs 1` at 110.66s over four.

    The sweeps were 313.95s of step time between them while the corpus was a hundred
    cases: the escape screen 110.66s, the chunk census 90.38s, `known-best n=1..100
    atlas` 75.88s, the prospective seed 37.03s.

    Two of those four names are gone, and the corpus is why rather than the gate. At
    `n=1..324` the screen is 766.26s and the atlas step 703.28s on an idle ten-cpu box at
    this job's own shape, against a 210s ceiling, and
    `test_the_pull_request_surface_defers_only_what_was_measured` carries both readings
    and the argument for moving the per-case re-derivation to the deep gate. What runs
    here now:

    - `known-best chunk census`, unchanged. `D4` pins it at `CALIBRATION_CORPUS`, so a
      widening corpus does not reach it, and three readings on 2026-09-07 agreed to
      within 0.07s at 40.03s.
    - `known-best atlas records and sample`, the 12.09s of subcommands that did not grow
      with the corpus plus a sampled rebuild in place of the 691.19s whole one.
    - `translation escape screen records and sample`, the retained screen rebuilt from
      its own records plus a sampled replay.
    - `prospective n=101..324 safe seed`, now about 0.07s. Where a step runs is not what
      makes it cheap, so a step that has become free is left where it is rather than
      moved for tidiness.

    They are one kind of work: each re-derives a retained atlas from the witnesses under
    it and compares it byte for byte. That matters more than the ranking, because a rule
    keyed on kind survives a step getting faster, and a rule keyed on today's top four
    does not -- as this list has already shown, the prospective seed having gone from the
    longest of the four to the shortest and then to nothing at all.

    The suite was one step when it first left `checks`, and its rule was arithmetic
    rather than kind:

    - `fast behavioral tests`, 142.43s of the 221.70s `checks` job, which is 64 per cent
      of a job it shares with 57 others. A job cannot be shorter than its longest step,
      so while this ran in `checks` no `--jobs` setting could take that job under 142s.
      Alone it also stops being throttled: `_pytest_workers` gives it `cpus - jobs + 1`
      xdist workers, which was two beside 57 steps at `--jobs 3` and is four at
      `--jobs 1` on a runner of its own.

    That measurement justified extracting the lane. The current lane has four step
    instances, one for each file shard. The plugin filters before collection
    and assigns every module to exactly one of them. Their separate jobs reduce the lane
    wall without dropping a test or importing the other shard.

    The `geometry` half became the fourth job at that stage, and its rule was neither kind
    nor floor but a queue. What was left in `checks` once the lane moved out was 57 steps
    of pure outer-parallel work with nothing large enough to floor the job, and CI run
    34016999060 priced the obvious response -- spend the freed cpu at `--jobs 4` -- at
    198.22s against the 221.70s three-worker job that still had the 142.43s lane inside
    it. 23.5s, because saturating four cpus inflated every step by thirty to eighty per
    cent: the perimeter 60.62s to 84.41s, exact verification 61.75s to 79.98s, the type
    floor 40.37s to 72.31s, the SVG renderer 41.30s to 65.36s. A queue of that shape is
    shortened by cpus and by nothing else, so the queue was halved and both halves run at
    `--jobs 3`.

    Two rules bound which steps may cross, and both are asserted in
    `test_the_edit_tier_cannot_under_run`: only a `broad` step, so `--edit` stays wholly
    inside `--checks`; and nothing that needs the engine, so only one of the two jobs pays
    the serial `cargo build --release`. Inside those, the boundary is arithmetic. Local,
    2026-09-06, four cpus, `--checks --jobs 4 --inner-jobs 1` over the undivided 57 steps
    at 545.08s of step time, these nine are 275.48s of it:

    - `D-034's n=5 identity pair still reproduces`, 62.62s -- and the step that most wants
      a runner of its own, because `build_n5_identity_pair` asks `ProcessPoolExecutor` for
      the whole machine rather than for `PACK_JOBS` workers.
    - `historical regressions`, 42.35s.
    - `the decimal route still cannot price an exact pose`, 39.43s.
    - `deterministic SVG rendering`, 39.36s -- the step `D-455` was caught by.
    - `small-n exact models and local geometry`, 28.34s.
    - `Trump exact branchwise linearized cones`, 20.94s.
    - `fixed-angle cell is an LP, rebuilt independently`, 15.84s.
    - `basin atlas`, 13.94s.
    - `basin event record and replay`, 12.66s.

    That leaves 269.60s in `checks`, two halves within two per cent of each other. At the
    reference shape on the same box the two walls are 93.27s and 86.20s.

    The current surface exposes nine tier readings instead of one queue, and no coverage
    change at all: every one of these steps runs on every pull request exactly as it did
    before, which is what
    `test_the_pull_request_surface_defers_only_what_was_measured` re-checks from the
    workflow rather than from these flags.
    """
    assert {step.name for step in validate.STEPS if step.sweep} == {
        "prospective n=101..324 safe seed",
        "known-best chunk census",
        "known-best family and contact-shade censuses",
        "translation escape screen records and sample",
        "known-best atlas records and sample",
    }
    assert {step.name for step in validate.STEPS if step.suite_a} == {
        "fast behavioral tests, shard A",
    }
    assert {step.name for step in validate.STEPS if step.suite_b} == {
        "fast behavioral tests, shard B",
    }
    assert {step.name for step in validate.STEPS if step.suite_c} == {
        "fast behavioral tests, shard C",
    }
    assert {step.name for step in validate.STEPS if step.suite_d} == {
        "fast behavioral tests, shard D",
    }
    assert {step.name for step in validate.STEPS if step.frontend} == {
        "browser floor (biome, eslint, tsc, node:test)",
        "browser floor liveness tests",
        "workbench browser behavior in Chromium",
        "site table layout in Chromium",
    }
    assert {step.name for step in validate.STEPS if step.typecheck} == {
        "type floor (basedpyright)",
    }
    assert {step.name for step in validate.STEPS if step.geometry} == {
        "D-034's n=5 identity pair still reproduces",
        "historical regressions",
        "the decimal route still cannot price an exact pose",
        "deterministic SVG rendering",
        "small-n exact models and local geometry",
        "Trump exact branchwise linearized cones",
        "fixed-angle cell is an LP, rebuilt independently",
        "basin atlas",
        "basin event record and replay",
    }
    # A sweep, a suite or a geometry step outside `--fast` would be a step the pull
    # request does not run at all, which is a deferral and belongs in the test above
    # rather than in this one. Carrying two of the flags would put one step in two jobs,
    # which is a bill paid twice.
    marks = [
        {step.name for step in validate.STEPS if step.frontend},
        {step.name for step in validate.STEPS if step.sweep},
        {step.name for step in validate.STEPS if step.suite_a},
        {step.name for step in validate.STEPS if step.suite_b},
        {step.name for step in validate.STEPS if step.suite_c},
        {step.name for step in validate.STEPS if step.suite_d},
        {step.name for step in validate.STEPS if step.geometry},
        {step.name for step in validate.STEPS if step.typecheck},
    ]
    assert all(
        step.fast
        for step in validate.STEPS
        if step.frontend
        or step.sweep
        or step.suite_a
        or step.suite_b
        or step.suite_c
        or step.suite_d
        or step.geometry
        or step.typecheck
    )
    for index, marked in enumerate(marks):
        for other in marks[index + 1 :]:
            assert not marked & other


def _workflow_commands(*, pull_request: bool) -> dict[str, argparse.Namespace]:
    """Each Linux gate job's parsed `packing-validate` command on this event, by job name.

    `macos-portability` is excluded here for the reason `_workflow_selections` gives.
    """
    condition = "github.event_name == 'pull_request'"
    negation = "github.event_name != 'pull_request'"
    excluded = negation if pull_request else condition
    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    commands: dict[str, argparse.Namespace] = {}
    for job_name, job in document["jobs"].items():
        if job_name == "macos-portability" or excluded in str(job.get("if", "")):
            continue
        for step in job.get("steps", []):
            command = str(step.get("run", ""))
            if "packing-validate" not in command or excluded in str(step.get("if", "")):
                continue
            tokens = shlex.split(command)
            arguments = tokens[tokens.index("packing-validate") + 1 :]
            commands[job_name] = validate._parser().parse_args(arguments)
    return commands


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
    return {
        job_name: {
            selected.name
            for selected in validate._select_steps(
                only=namespace.only,
                skip=namespace.skip,
                fast=namespace.fast,
                records=namespace.records,
                edit=namespace.edit,
                checks=namespace.checks,
                frontend=namespace.frontend,
                sweeps=namespace.sweeps,
                suite_a=namespace.suite_a,
                suite_b=namespace.suite_b,
                suite_c=namespace.suite_c,
                suite_d=namespace.suite_d,
                geometry=namespace.geometry,
                typecheck=namespace.typecheck,
                measure_verifier=namespace.measure_verifier,
            )
        }
        for job_name, namespace in _workflow_commands(pull_request=pull_request).items()
    }


def test_the_pull_request_jobs_partition_the_surface() -> None:
    """The jobs a pull request runs must divide `--fast`, and pay for nothing twice.

    The surface was one job until 2026-09-06 and one job could not hold it: 1,100s of
    step time on a four-cpu runner has a 275s floor however it is scheduled, and it was
    finishing in 501.97s. It was two jobs for one day, and two could not balance it:
    `checks` 221.70s against `sweeps` 110.66s on run 34010470187, with 142.43s of the
    longer half in a single indivisible step. Three runners put that step on its own. The
    next cut was the one the arithmetic forced rather than a preference: what was left
    in `checks` was 790 worker-seconds of pure
    outer-parallel work against four cpus, `--jobs 4` on run 34016999060 bought 23.5s
    because it inflated every step by thirty to eighty per cent, and a queue of that
    shape is shortened by cpus and by nothing else.

    What a split like this risks is the gap `D-455` came through in the other direction --
    a step in no selection, run by nobody, reported by nothing -- so the nine commands are
    read from the workflow and checked to be a partition rather than trusted to be.

    `--checks`, `--frontend`, `--geometry`, all four suite shards and `--sweeps` partition
    `_select_steps` by construction, so this is really a check on the YAML: that the
    workflow invokes all nine, on a pull request, and narrows none of them with `--only`
    or `--skip`.

    Pairwise disjointness is asserted rather than inferred from the union. Two jobs make
    those the same statement; more than two do not, and the case they differ on -- one
    step in two jobs and another in none -- is a bill paid twice hiding a check nobody
    runs.
    """
    selections = _workflow_selections(pull_request=True)

    assert set(selections) == {
        "validate",
        "frontend",
        "geometry",
        "suite-a",
        "suite-b",
        "suite-c",
        "suite-d",
        "sweeps",
        "typecheck",
        "measure-verifier",
    }
    names = list(selections)
    for index, job in enumerate(names):
        for other in names[index + 1 :]:
            assert not selections[job] & selections[other], f"{job} and {other} overlap"
    assert set().union(*selections.values()) == {
        step.name for step in validate.STEPS if step.fast
    }
    assert selections["sweeps"] == {step.name for step in validate.STEPS if step.sweep}
    assert selections["suite-a"] == {step.name for step in validate.STEPS if step.suite_a}
    assert selections["suite-b"] == {step.name for step in validate.STEPS if step.suite_b}
    assert selections["suite-c"] == {step.name for step in validate.STEPS if step.suite_c}
    assert selections["suite-d"] == {step.name for step in validate.STEPS if step.suite_d}
    assert selections["geometry"] == {step.name for step in validate.STEPS if step.geometry}
    assert selections["frontend"] == {step.name for step in validate.STEPS if step.frontend}
    assert selections["typecheck"] == {step.name for step in validate.STEPS if step.typecheck}
    assert selections["measure-verifier"] == {
        step.name for step in validate.STEPS if step.measure_verifier
    }


def test_a_verified_merge_repeats_everything_not_positively_tree_reusable() -> None:
    narrowed = validate._after_verified_pull_request(validate.STEPS)
    assert {step.name for step in narrowed if step.fast} == {
        "bead tree",
        "provenance: recorded commits are reachable",
        "campaign record",
        # An advisory wall's tracking bead is read from the bead store, not the tree.
        "tier ceilings are declared and not slack",
        # The new native crate is not yet classified as tree-reusable.
        "n17 kernel verifier (Rust)",
        # New custody checks repeat until their tree reuse is explicitly classified.
        "SQUISH update certification binds complete reviewed inputs",
        "SQUISH second update certification binds complete reviewed inputs",
    }

    # Fail closed: a new fast step is repeated until explicitly classified.
    unclassified = validate.Step("unclassified probe", lambda _context: "", fast=True)
    assert validate._after_verified_pull_request([unclassified]) == [unclassified]

    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    validate_job = document["jobs"]["validate"]
    [finder] = [step for step in validate_job["steps"] if step.get("id") == "verified-tree"]
    assert finder["if"] == "github.event_name == 'push'"
    assert "devtools.verified_merge_tree" in finder["run"]
    [gate] = [
        step
        for step in validate_job["steps"]
        if step.get("name") == "Run the complete integration surface"
    ]
    assert gate["env"] == {
        validate.TREE_VERIFIED_ENVIRONMENT: "${{ steps.verified-tree.outputs.run }}"
    }
    assert validate_job["permissions"] == {"contents": "read", "actions": "read"}


def test_a_tree_proof_narrows_only_the_complete_post_merge_surface(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """The CLI half of the post-merge reuse: where the proof applies, and what it leaves.

    `_after_verified_pull_request` decides which fast steps a proof may leave out. What
    keeps that from narrowing anything else is `_unless_verified`: a tier, `--only`,
    `--since` or `--push` run that inherited the variable refuses rather than quietly
    dropping part of a declared selection, and the complete surface the workflow runs
    after a push lists exactly the narrowed selection.
    """
    monkeypatch.setenv(validate.TREE_VERIFIED_ENVIRONMENT, "12345")
    for arguments in (
        ["--checks"],
        ["--only", "exact verification"],
        ["--since", "HEAD"],
        ["--push"],
    ):
        assert main([*arguments, "--list"]) == 2, arguments
        assert validate.TREE_VERIFIED_ENVIRONMENT in capsys.readouterr().err, arguments

    post_merge = _workflow_commands(pull_request=False)["validate"]
    complete = _workflow_selections(pull_request=False)["validate"]
    narrowed = {
        step.name
        for step in validate._after_verified_pull_request(
            [step for step in validate.STEPS if step.name in complete]
        )
    }
    assert narrowed < complete
    skips = [part for pattern in post_merge.skip for part in ("--skip", pattern)]
    assert main([*skips, "--list", "--format", "json"]) == 0
    captured = capsys.readouterr()
    assert {entry["name"] for entry in json.loads(captured.out)} == narrowed
    # The announcement goes to stderr under `--format json`, never into the document.
    assert "passed this exact tree" in captured.err


def test_exact_verifier_cache_cannot_relabel_an_older_build() -> None:
    """Partial failed builds may be reused only for identical sources and compiler."""
    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = document["jobs"]["validate"]["steps"]
    key = next(step for step in steps if step.get("id") == "exact-key")
    assert key["working-directory"] == "packing/sqverify_exact"
    assert "git rev-parse HEAD:packing/sqverify_exact" in key["run"]
    assert "rustc -vV" in key["run"]
    cache = next(step for step in steps if step.get("id") == "exact-cache")
    assert "restore-keys" not in cache["with"]
    assert cache["with"]["path"] == "packing/sqverify_exact/target"
    assert "steps.exact-key.outputs.rustc" in cache["with"]["key"]
    assert "steps.exact-key.outputs.tree" in cache["with"]["key"]
    repair = next(step for step in steps if "identical cached build" in step.get("name", ""))
    assert repair["if"] == "steps.exact-cache.outputs.cache-hit == 'true'"
    assert "git ls-files -z -- sqverify_exact" in repair["run"]
    save = next(step for step in steps if "Save the exact verifier" in step.get("name", ""))
    assert "always()" in save["if"]
    assert "steps.exact-cache.outcome == 'success'" in save["if"]
    assert save["with"]["key"] == "${{ steps.exact-cache.outputs.cache-primary-key }}"
    assert save["with"]["path"] == cache["with"]["path"]
    gate = next(
        step for step in steps if step.get("name") == "Run the required pull-request checks"
    )
    assert "exact-cache" not in gate.get("if", "")
    assert steps.index(repair) < steps.index(gate) < steps.index(save)


def test_the_engine_cache_backdates_and_saves_only_a_build_for_its_exact_key() -> None:
    """A partial restore or verified-main skip must not bless an old target as current."""
    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = document["jobs"]["validate"]["steps"]

    key_step = next(step for step in steps if step.get("id") == "engine-key")
    assert key_step["working-directory"] == "packing/sqsearch"
    key_program = key_step["run"]
    assert 'rustc_vv="$(rustc -vV)"' in key_program
    assert "git rev-parse HEAD:packing/sqsearch" in key_program
    assert "sha256sum | cut -c1-16" in key_program

    cache_index, cache = next(
        (index, step)
        for index, step in enumerate(steps)
        if step.get("name") == "Cache the Rust build for the engine"
    )
    assert cache["id"] == "engine-cache"
    assert "actions/cache/restore@" in cache["uses"]
    cache_key = cache["with"]["key"]
    assert "${{ runner.os }}-sqsearch-" in cache_key
    assert "${{ steps.engine-key.outputs.rustc }}" in cache_key
    assert cache_key.endswith("${{ steps.engine-key.outputs.tree }}")
    assert cache["with"]["restore-keys"].strip() == (
        "${{ runner.os }}-sqsearch-${{ steps.engine-key.outputs.rustc }}-"
    )

    populate = steps[cache_index + 1]
    assert populate["name"] == "Populate the engine cache for this exact tree"
    assert populate["if"] == "steps.engine-cache.outputs.cache-hit != 'true'"
    assert populate["working-directory"] == "packing/sqsearch"
    assert populate["run"] == "cargo build --locked --release --quiet"

    repair = steps[cache_index + 2]
    assert repair["name"] == "Date the engine sources before the build restored for them"
    assert repair["if"] == "steps.engine-cache.outputs.cache-hit == 'true'"
    assert repair["run"] == ("git ls-files -z -- sqsearch | xargs -0 touch -t 200001010000")

    save = next(
        step
        for step in steps
        if step.get("name") == "Save the Rust build for the exact engine tree"
    )
    assert "actions/cache/save@" in save["uses"]
    assert save["if"] == ("success() && steps.engine-cache.outputs.cache-hit != 'true'")
    assert save["with"] == {
        "path": cache["with"]["path"],
        "key": "${{ steps.engine-cache.outputs.cache-primary-key }}",
    }
    gate_indices = [
        index
        for index, step in enumerate(steps)
        if step.get("name")
        in {"Run the required pull-request checks", "Run the complete integration surface"}
    ]
    assert steps.index(save) > max(gate_indices)
    assert steps.index(save) < next(
        index
        for index, step in enumerate(steps)
        if step.get("name") == "Preserve validation timings and partial logs"
    )

    # This is the formerly unsafe path: a verified main push narrows away every
    # validation-owned engine step. The explicit miss build above still runs first.
    assert any(step.needs_engine for step in validate.STEPS)
    assert not any(
        step.needs_engine for step in validate._after_verified_pull_request(validate.STEPS)
    )


def test_browser_floor_liveness_runs_only_with_the_frontend_node_toolchain() -> None:
    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    selections = _workflow_selections(pull_request=True)
    owners = [
        name
        for name, selected in selections.items()
        if "browser floor liveness tests" in selected
    ]
    assert owners == ["frontend"]
    for job_name in ("suite-a", "suite-b", "suite-c", "suite-d"):
        steps = document["jobs"][job_name]["steps"]
        assert not any("setup-node" in str(step.get("uses", "")) for step in steps)
        assert not any("npm ci" in str(step.get("run", "")) for step in steps)


SITE_LAYOUT_STEP = "site table layout in Chromium"


def _installs_chromium(job: Mapping[str, Any], *, pull_request: bool) -> bool:
    """Whether a workflow job installs the pinned Chromium on this event: a `playwright
    install` step whose own condition does not exclude the event."""
    excluded = (
        "github.event_name != 'pull_request'"
        if pull_request
        else "github.event_name == 'pull_request'"
    )
    return any(
        "playwright install" in str(step.get("run", ""))
        and excluded not in str(step.get("if", ""))
        for step in job.get("steps", [])
    )


def test_the_site_layout_tests_run_only_where_chromium_is_installed() -> None:
    """The site's table-layout tests measure pixels in Chromium, so the step that runs
    them is selected only by jobs that install the pinned browser on the event -- the
    frontend job on a pull request, the validate job after a merge -- and by no
    behavioural shard, which installs none and where the tests could only skip, as they
    did on every pull request until run 36943941580 read them on Linux (D-513)."""
    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    for pull_request, expected in ((True, ["frontend"]), (False, ["validate"])):
        selections = _workflow_selections(pull_request=pull_request)
        owners = sorted(
            name for name, selected in selections.items() if SITE_LAYOUT_STEP in selected
        )
        assert owners == expected, pull_request
        for owner in owners:
            assert _installs_chromium(document["jobs"][owner], pull_request=pull_request), owner
    for job_name in ("suite-a", "suite-b", "suite-c", "suite-d"):
        assert not _installs_chromium(document["jobs"][job_name], pull_request=True), job_name
    assert set(validate.SITE_LAYOUT_TESTS) == {
        "tests/test_site_result_columns.py",
        "tests/test_site_frontier_table.py",
    }
    for path in validate.SITE_LAYOUT_TESTS:
        assert (validate.PROJECT_ROOT / path).is_file(), path


def test_a_frontend_job_without_chromium_is_detected() -> None:
    """The negative control: the site's tests cannot move to a runner with no browser."""
    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert _installs_chromium(document["jobs"]["frontend"], pull_request=True)
    document["jobs"]["frontend"]["steps"] = [
        step
        for step in document["jobs"]["frontend"]["steps"]
        if "playwright install" not in str(step.get("run", ""))
    ]
    assert not _installs_chromium(document["jobs"]["frontend"], pull_request=True)
    # The validate job installs Chromium only after a merge, so on a pull request it
    # counts as a job without one, which is why `--checks` must not select the step.
    assert not _installs_chromium(document["jobs"]["validate"], pull_request=True)
    assert _installs_chromium(document["jobs"]["validate"], pull_request=False)


def test_the_site_layout_step_requires_a_chromium_and_runs_its_two_files(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The step fails rather than skips when no Chromium launches: it sets the name
    `tests.site_browser` reads, for its command alone, and runs exactly the files the
    quick lane ignores, one to a worker as the quick lane runs its own."""
    observed: dict[str, Any] = {}

    def capture(_context: validate.Context, command: Sequence[str], **options: Any) -> str:
        observed["command"] = tuple(command)
        observed["environment"] = options.get("extra_environment")
        return ""

    monkeypatch.setattr(validate, "_run", capture)
    monkeypatch.setattr(validate, "_pytest_workers", lambda _jobs: 2)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment=os.environ.copy(),
    )
    validate._site_layout_tests(context)
    assert observed["command"] == (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-p",
        "no:cacheprovider",
        "-n",
        "2",
        "--dist=loadfile",
        *validate.SITE_LAYOUT_TESTS,
    )
    assert observed["environment"] == {validate.REQUIRE_CHROMIUM: "1"}
    assert validate.REQUIRE_CHROMIUM == site_browser.REQUIRED


def test_a_commands_extra_environment_reaches_only_that_command(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`_run` lays the extra environment over the gate's for the one subprocess, and the
    context the caller holds is unchanged."""
    seen: list[dict[str, str]] = []

    def run_command(context: validate.Context, *_args: Any, **_options: Any) -> str:
        seen.append(dict(context.environment))
        return ""

    monkeypatch.setattr(validate, "_run_command", run_command)
    monkeypatch.setattr(validate, "_artifact_directory", lambda _context: None)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={"KEPT": "1"},
    )
    validate._run(context, ("true",), extra_environment={"ADDED": "2"})
    validate._run(context, ("true",))
    assert seen == [{"KEPT": "1", "ADDED": "2"}, {"KEPT": "1"}]
    assert context.environment == {"KEPT": "1"}


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

    The post-merge commands are out of scope rather than exempt. All are narrowed --
    `--skip` on the broad job, `--only` on the isolated lanes -- so none reads a whole
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
    assert checked == {
        "checks",
        "frontend",
        "geometry",
        "suite_a",
        "suite_b",
        "suite_c",
        "suite_d",
        "sweeps",
        "typecheck",
        "measure_verifier",
    }


def test_the_post_merge_jobs_partition_the_gate() -> None:
    """The complete checkpoint partitions whole Steps; exhaustive shards share one Step."""
    selections = _workflow_selections(pull_request=False)
    deferred = {
        "deferred-threshold-1440",
        "deferred-atlas-grid",
        "deferred-controls-finer",
        "deferred-threshold-720-rigidity",
    }
    shards = {f"exhaustive-{index}" for index in (1, 2, 3)}
    assert set(selections) == {
        "validate",
        "slow-lane",
        "screen",
        "regularized-views",
        *deferred,
        *shards,
    }
    assert selections["slow-lane"] == {"slow behavioral tests"}
    assert selections["screen"] == {"single-square translation escape screen"}
    assert selections["regularized-views"] == {"regularized atlas views re-derive exactly"}
    commands = _workflow_commands(pull_request=False)
    for index in (1, 2, 3):
        job = f"exhaustive-{index}"
        assert selections[job] == {"exhaustive exact behavioral tests"}
        assert commands[job].exhaustive_shard == f"{index}/3"
        assert (commands[job].jobs, commands[job].inner_jobs) == ("1", "4")

    # The three whole-file shards jointly own one Step. Every other Step has one owner.
    logical = {name: selected for name, selected in selections.items() if name not in shards}
    logical["exhaustive"] = selections["exhaustive-1"]
    names = list(logical)
    for index, job in enumerate(names):
        for other in names[index + 1 :]:
            assert not logical[job] & logical[other], f"{job} and {other} overlap"
    assert set().union(*logical.values()) == {step.name for step in validate.STEPS}
    assert sum(map(len, logical.values())) == len(validate.STEPS)


def test_post_merge_workers_bind_one_sha_and_a_separate_complete_aggregate() -> None:
    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    jobs = document["jobs"]
    expected = {
        "validate",
        "deferred-threshold-1440",
        "deferred-atlas-grid",
        "deferred-controls-finer",
        "deferred-threshold-720-rigidity",
        "slow-lane",
        "exhaustive-1",
        "exhaustive-2",
        "exhaustive-3",
        "screen",
        "regularized-views",
    }
    aggregate = jobs["post-merge-required"]
    assert aggregate["if"] == "!cancelled() && github.event_name != 'pull_request'"
    assert set(aggregate["needs"]) == expected
    verdict = aggregate["steps"][0]
    command = verdict["run"]
    for job in expected:
        expression = f"${{{{ needs.{job}.result }}}}"
        matching = [key for key, value in verdict["env"].items() if value == expression]
        assert len(matching) == 1, job
        assert f'test "${matching[0]}" = "success"' in command

    # No deferred job can enter the ten-prerequisite pull-request context.
    assert set(jobs["packing-required"]["needs"]) == {
        "validate",
        "frontend",
        "typecheck",
        "geometry",
        "suite-a",
        "suite-b",
        "suite-c",
        "suite-d",
        "sweeps",
        "measure-verifier",
    }
    for name in expected - {"validate"}:
        job = jobs[name]
        assert job["if"] == "github.event_name != 'pull_request'"
        steps = job["steps"]
        checkouts = [step for step in steps if "actions/checkout@" in step.get("uses", "")]
        assert checkouts
        assert all(step["with"]["ref"] == "${{ github.sha }}" for step in checkouts)
        validators = [
            index
            for index, step in enumerate(steps)
            if "packing-validate" in step.get("run", "")
        ]
        receipts = [
            index
            for index, step in enumerate(steps)
            if step.get("name") == "Bind the receipt to the immutable tree"
        ]
        assert len(validators) == len(receipts) == 1
        assert receipts[0] < validators[0]
        receipt = steps[receipts[0]]
        assert receipt["env"]["VALIDATED_SHA"] == "${{ github.sha }}"
        assert 'test "$(git rev-parse HEAD)" = "$VALIDATED_SHA"' in receipt["run"]
        uploads = [step for step in steps if "actions/upload-artifact@" in step.get("uses", "")]
        assert len(uploads) == 1
        expected_artifact = "validation-timings-${{ github.job }}-${{ github.run_attempt }}"
        assert uploads[0]["with"]["name"] == expected_artifact


def test_the_longest_steps_are_submitted_first() -> None:
    """A long step submitted late finishes late, and the run ends when it does.

    The pool takes steps in submission order, and the behavioural suite is declared
    fifteenth. That cost nothing while the fourteen ahead of it were seconds of record
    checks; the 2026-09-05 promotion put eleven steps and 476s there, which greedy
    submission would have spent delaying the suite's start rather than running beside it.

    Budget precedence remains ahead of early-start hints. Two unbudgeted steps have
    measured late tails, so they start ahead of the remaining declaration-order work:
    Chromium (declared first) and exact verification.

    `fast behavioral tests` is no longer in this list, and its absence is the point rather
    than an omission. It carried an 1800s exception to the shared cap for as long as it
    ran every non-exhaustive test; `BC-214` moved the slow half to `slow behavioral tests`,
    so the quick lane is ordinary enough to live under the shared cap and a step that no
    longer needs an exception should not keep one. What it is allowed to *cost*, as
    against how long one hung subprocess may hang, is `devtools/gate-budgets.yaml`.
    """
    order = [step.name for step in validate._submission_order(validate.STEPS)]

    assert order[:4] == [
        "exhaustive exact behavioral tests",  # 3600s
        # The three 1800s steps, in declaration order, because the sort is stable and a
        # tie is not a ranking. Which of them starts first does not matter to the wall:
        # three of the four have their own post-merge runner and are alone on it.
        "single-square translation escape screen",  # 1800s, `D-484`
        "negative controls",  # 1800s, and declared before the suite
        "slow behavioral tests",  # 1800s, the non-exhaustive suite's own bound
    ]
    budgeted_count = sum(step.budget_seconds is not None for step in validate.STEPS)
    early = (
        "workbench browser behavior in Chromium",
        "exact verification",
    )
    assert order[budgeted_count : budgeted_count + 2] == list(early)
    assert order[budgeted_count + 2 :] == [
        step.name
        for step in validate.STEPS
        if step.budget_seconds is None and step.name not in early
    ]


def test_early_start_preserves_failures_stable_ties_and_report_order(
    capsys: pytest.CaptureFixture[str],
) -> None:
    launched: list[str] = []

    def step(
        name: str,
        exit_code: int = 0,
        *,
        early: bool = False,
        budget: float | None = None,
    ) -> validate.Step:
        def action(context: validate.Context) -> str:
            launched.append(name)
            return validate._run(
                context,
                (sys.executable, "-c", f"import sys; print({name!r}); sys.exit({exit_code})"),
            )

        return validate.Step(name, action, fast=True, budget_seconds=budget, start_early=early)

    steps = [
        step("ordinary"),
        step("early failure", 17, early=True),
        step("also early", early=True),
        step("budgeted", budget=2),
        step("last ordinary"),
    ]
    summary = validate._run_selected(
        steps, _budget_context(timeout_seconds=5, explicit=False), []
    )
    assert launched == ["budgeted", "early failure", "also early", "ordinary", "last ordinary"]
    assert [result.name for result in summary.results] == [step.name for step in steps]
    assert [result.status for result in summary.results] == [
        "passed",
        "failed",
        "passed",
        "passed",
        "passed",
    ]
    assert "exited 17" in summary.results[1].reason
    assert validate._render_text(summary, strict=False) == 1
    output = capsys.readouterr().out
    assert "1 STEP FAILED" in output
    assert "STEPS PASSED" not in output


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


def test_workbench_chromium_starts_ahead_of_the_other_frontend_steps() -> None:
    """`--jobs 2` otherwise starts biome and liveness, and Chromium is the late tail."""
    chromium = next(
        step for step in validate.STEPS if step.name == "workbench browser behavior in Chromium"
    )
    assert chromium.start_early is True
    assert chromium.frontend is True
    frontend = [step for step in validate.STEPS if step.frontend]
    assert next(step.name for step in validate._submission_order(frontend)) == chromium.name
    assert {step.name for step in validate.STEPS if step.start_early} == {
        "exact verification",
        "workbench browser behavior in Chromium",
    }


def test_broad_is_opt_out_so_a_new_step_joins_the_edit_tier() -> None:
    """Forgetting the marker must make the tier slower, never blinder.

    A `broad` default of True would mean a new fast step silently sat outside the edit
    loop until someone noticed. The default is False, so the failure mode of forgetting
    is a tier that costs more than it needs to -- which shows up in the timings rather
    than in a missed regression.
    """
    assert validate.Step("probe", lambda _context: "", fast=True).broad is False
    assert {step.name for step in validate.STEPS if step.broad} == {
        "fast behavioral tests, shard A",
        "fast behavioral tests, shard B",
        "fast behavioral tests, shard C",
        "fast behavioral tests, shard D",
        "browser floor liveness tests",
        "workbench browser behavior in Chromium",
        "site table layout in Chromium",
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
        "exact rectangle Rust geometry",  # exact crate lint/tests and Python oracle
        "measure verifier Rust (sqverify-fast)",  # clean-room crate, oracle, controls
        "n17 branch-and-bound native (Rust)",  # native pilot build and bitwise replay
        "n17 kernel verifier (Rust)",  # standalone ordinary-certificate controls and floor
        # The four record sweeps, split at their measured seams on 2026-09-06 so the pull
        # request's second runner can schedule them. The figures beside them are the
        # 148.50s and 102.56s above, divided by the same measurement that split them:
        # locally, at `PACK_JOBS=1` and one subcommand at a time, the census was 94.85s of
        # the undivided known-best step's 133.22s and the seed 88.37s of the prospective
        # step's 88.76s.
        "known-best atlas records and sample",  # 12.09s of records plus a sampled rebuild
        "known-best chunk census",  # 40.03s, pinned at CALIBRATION_CORPUS by D4
        # X-049's descriptive censuses, 8.8s and 7.6s locally (2026-10-02), on the
        # sweeps runner beside the seed.
        "known-best family and contact-shade censuses",
        "prospective n=101..324 safe seed",  # 102.10s of the 102.56s
        "translation escape screen records and sample",  # the retained screen, plus a replay
        "historical regressions",  # 29.35s
        "deterministic SVG rendering",  # 26.39s
        "D-034's n=5 identity pair still reproduces",  # 23.54s
        "small-n exact models and local geometry",  # 19.80s
        "Trump exact branchwise linearized cones",  # 13.82s
        "fixed-angle cell is an LP, rebuilt independently",  # 9.76s
        "basin atlas",  # 9.63s
        "basin event record and replay",  # 7.89s
    }


def test_exact_rust_geometry_is_fast_and_runs_the_differential_oracle(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    step = next(step for step in validate.STEPS if step.name == "exact rectangle Rust geometry")
    assert step.fast
    assert step.broad
    assert not step.needs_engine
    assert "packing/sqverify_exact/*" in step.touches
    calls: list[tuple[str, ...]] = []

    def commands(
        context: validate.Context,
        commands: tuple[tuple[str, ...], ...],
        *,
        cwd: Path,
    ) -> str:
        assert cwd == validate.EXACT_GEOMETRY_CRATE
        assert context.environment["RUSTDOCFLAGS"] == "old -D warnings"
        calls.extend(commands)
        return "test result: ok. 2 passed; 0 failed"

    def run(context: validate.Context, command: tuple[str, ...], **_: object) -> str:
        assert context.environment["RUSTDOCFLAGS"] == "old -D warnings"
        calls.append(command)
        return "EXACT RUST GEOMETRY DIFFERENTIAL PASSED"

    monkeypatch.setattr(validate.shutil, "which", lambda *_, **__: "cargo")
    monkeypatch.setattr(validate, "_commands", commands)
    monkeypatch.setattr(validate, "_run", run)
    environment = {"RUSTDOCFLAGS": "old", "CARGO_TARGET_DIR": "/scratch/exact-target"}
    context = validate.Context(
        deep=False, strict=True, jobs=1, inner_jobs=1, environment=environment
    )
    assert "DIFFERENTIAL PASSED" in step.action(context)
    assert environment == {"RUSTDOCFLAGS": "old", "CARGO_TARGET_DIR": "/scratch/exact-target"}
    assert any(command[:3] == ("cargo", "clippy", "--locked") for command in calls)
    assert ("cargo", "test", "--locked", "--all-targets", "--quiet") in calls
    assert ("cargo", "build", "--locked", "--release", "--quiet") in calls
    assert calls[-1][-1] == "/scratch/exact-target/release/sqverify-exact"


def test_measure_verifier_is_fast_and_runs_the_oracle_and_controls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    step = next(
        step for step in validate.STEPS if step.name == "measure verifier Rust (sqverify-fast)"
    )
    assert step.fast
    assert step.broad
    assert not step.needs_engine
    assert "packing/sqverify_fast/*" in step.touches
    calls: list[tuple[str, ...]] = []

    def commands(
        context: validate.Context,
        commands: tuple[tuple[str, ...], ...],
        *,
        cwd: Path,
    ) -> str:
        assert cwd == validate.MEASURE_VERIFIER_CRATE
        assert context.environment["RUSTDOCFLAGS"] == "old -D warnings"
        calls.extend(commands)
        return "test result: ok. 8 passed; 0 failed"

    def run(_context: validate.Context, command: tuple[str, ...], **_: object) -> str:
        calls.append(command)
        return "SQVERIFY-FAST CHECKS PASSED"

    monkeypatch.setattr(validate.shutil, "which", lambda *_, **__: "cargo")
    monkeypatch.setattr(validate, "_commands", commands)
    monkeypatch.setattr(validate, "_run", run)
    environment = {"RUSTDOCFLAGS": "old", "CARGO_TARGET_DIR": "/scratch/fast-target"}
    context = validate.Context(
        deep=False, strict=True, jobs=1, inner_jobs=1, environment=environment
    )
    assert "CHECKS PASSED" in step.action(context)
    assert any(command[:3] == ("cargo", "clippy", "--locked") for command in calls)
    assert (
        "cargo",
        "test",
        "--locked",
        "--profile",
        "gate-test",
        "--all-targets",
        "--quiet",
    ) in calls
    assert ("cargo", "build", "--locked", "--release", "--quiet") in calls
    assert calls[-1][-3:] == (
        "--binary",
        "/scratch/fast-target/release/sqverify-fast",
        "--quick",
    )


def test_measure_verifier_refuses_missing_compiler_or_empty_tests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    step = next(
        step for step in validate.STEPS if step.name == "measure verifier Rust (sqverify-fast)"
    )
    context = validate.Context(deep=False, strict=False, jobs=1, inner_jobs=1, environment={})
    monkeypatch.setattr(validate.shutil, "which", lambda *_, **__: None)
    with pytest.raises(validate.StepFailureError, match="requires cargo"):
        step.action(context)
    monkeypatch.setattr(validate.shutil, "which", lambda *_, **__: "cargo")
    monkeypatch.setattr(validate, "_commands", lambda *_, **__: "test result: ok. 0 passed")
    with pytest.raises(validate.StepFailureError, match="no passing Rust tests"):
        step.action(context)


def test_exact_rust_geometry_refuses_missing_compiler_or_empty_tests(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    step = next(step for step in validate.STEPS if step.name == "exact rectangle Rust geometry")
    context = validate.Context(deep=False, strict=False, jobs=1, inner_jobs=1, environment={})
    monkeypatch.setattr(validate.shutil, "which", lambda *_, **__: None)
    with pytest.raises(validate.StepFailureError, match="requires cargo"):
        step.action(context)
    monkeypatch.setattr(validate.shutil, "which", lambda *_, **__: "cargo")
    monkeypatch.setattr(validate, "_commands", lambda *_, **__: "test result: ok. 0 passed")
    with pytest.raises(validate.StepFailureError, match="no passing Rust tests"):
        step.action(context)


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


@pytest.mark.parametrize(
    ("cpus", "jobs", "threads"),
    [(4, 1, ("--threads", "4")), (4, 3, ("--threads", "2")), (4, 4, ())],
)
def test_the_type_floor_threads_across_the_cpus_the_selection_leaves(
    monkeypatch: pytest.MonkeyPatch, cpus: int, jobs: int, threads: tuple[str, ...]
) -> None:
    """Alone on the typecheck job it takes the runner; beside other steps it does not."""
    monkeypatch.setattr(validate.os, "process_cpu_count", lambda: cpus)
    monkeypatch.setattr(validate, "_required_tool", lambda _context, name: name)
    captured: list[tuple[str, ...]] = []

    def commands(_context, commands, **_kwargs):
        captured.extend(commands)
        return "0 errors, 0 warnings, 0 notes"

    monkeypatch.setattr(validate, "_commands", commands)
    context = validate.Context(
        deep=False, strict=False, jobs=jobs, inner_jobs=1, environment={}
    )
    validate._type_floor(context)
    assert captured == [("basedpyright", *threads)]


@pytest.mark.parametrize(("cpus", "jobs", "workers"), [(4, 2, "2"), (2, 2, "1"), (4, 4, "1")])
def test_frontend_browser_workers_fit_outer_topology(
    monkeypatch: pytest.MonkeyPatch, cpus: int, jobs: int, workers: str
) -> None:
    monkeypatch.setattr(validate.os, "process_cpu_count", lambda: cpus)
    captured: list[tuple[str, ...]] = []

    def commands(_context, commands, **_kwargs):
        captured.extend(commands)
        return "passed"

    monkeypatch.setattr(validate, "_commands", commands)
    context = validate.Context(
        deep=False, strict=False, jobs=jobs, inner_jobs=1, environment={}
    )
    validate._workbench_frontend(context)
    assert (
        sys.executable,
        "-m",
        "workbench_tools.check_frontend",
        "--workers",
        workers,
    ) in captured
    assert any("devtools.check_probes" in command for command in captured)
    assert any("devtools.check_motion_lab_pages" in command for command in captured)
