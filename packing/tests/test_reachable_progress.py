"""Child pytest receipts retain worker, source and partial-interruption evidence."""

from __future__ import annotations

import json
import math
import os
import signal
import subprocess
import sys
import time
from collections.abc import Sequence
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from datetime import datetime
from pathlib import Path
from typing import Literal, cast
from unittest.mock import Mock
from xml.etree import ElementTree as ET

import pytest

from devtools import reachable_progress, reachable_tests
from sqpack.cli import validate

PACKING = Path(__file__).resolve().parents[1]
SOURCE = "a" * 40

# These seams exercise the validator without launching its full behavioral lanes.
_run_native = validate._run  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
_slow_lane = validate._slow_tests  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
_quick_lane_command = validate._quick_lane_command  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]


def _environment(stem: Path, *, workers: int) -> dict[str, str]:
    return {
        **os.environ,
        "PYTHONPATH": os.pathsep.join((str(PACKING), os.environ.get("PYTHONPATH", ""))),
        "PACKING_REACHABLE_TEST_ARTIFACT_STEM": str(stem),
        "PACKING_REACHABLE_TEST_RUN_ID": "focused-run",
        "PACKING_REACHABLE_TEST_SOURCE_COMMIT": SOURCE,
        "PACKING_REACHABLE_TEST_WORKERS": str(workers),
        "PACK_JOBS": "1",
        "PACKING_REACHABLE_TEST_LANE": "quick",
        "PACKING_REACHABLE_TEST_MARKER": validate.QUICK_TESTS,
        "PACKING_REACHABLE_TEST_EXCLUSIONS": "slow, exhaustive_exact",
    }


def _probe(
    stem: Path, test_file: Path, *, workers: int, extra: tuple[str, ...] = ()
) -> tuple[str, ...]:
    # xdist allocates a basetemp even without tmp_path. An inherited shared root can
    # make this short probe clean up unrelated prior sessions before it exits.
    return (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-c",
        os.devnull,
        "--rootdir",
        str(test_file.parent),
        "--basetemp",
        f"{stem}.pytest-tmp",
        "-p",
        "devtools.reachable_progress",
        str(test_file),
        *(("-n", str(workers)) if workers > 1 else ()),
        "--durations=0",
        "--durations-min=0",
        f"--junitxml={stem}.junit.xml",
        *extra,
    )


def _rows(path: Path) -> list[dict[str, object]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_two_workers_write_separate_complete_progress_and_junit(tmp_path: Path) -> None:
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "def test_a(): pass\ndef test_b(): pass\ndef test_c(): pass\ndef test_d(): pass\n",
        encoding="utf-8",
    )
    stem = tmp_path / "child"
    inherited_temproot = tmp_path / "inherited-temproot"
    inherited_temproot.write_text("not a directory", encoding="utf-8")
    environment = _environment(stem, workers=2)
    environment["PYTEST_DEBUG_TEMPROOT"] = str(inherited_temproot)
    result = subprocess.run(
        _probe(stem, test_file, workers=2),
        cwd=PACKING,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    files = sorted(tmp_path.glob("child.progress-*.jsonl"))
    assert {path.name for path in files} == {
        "child.progress-gw0.jsonl",
        "child.progress-gw1.jsonl",
    }
    starts: set[str] = set()
    for path in files:
        rows = _rows(path)
        assert rows[0]["event"] == "session_start"
        assert rows[-1]["event"] == "session_finish"
        assert rows[-1]["exit_status"] == 0
        assert {row["event"] for row in rows} == {
            "session_start",
            "start",
            "finish",
            "session_finish",
        }
        worker = path.stem.removeprefix("child.progress-")
        started = {str(row["nodeid"]) for row in rows if row["event"] == "start"}
        finished = {str(row["nodeid"]) for row in rows if row["event"] == "finish"}
        assert started == finished
        starts |= started
        for row in rows:
            assert row["run_id"] == "focused-run"
            assert row["source_commit"] == SOURCE
            assert row["command_id"] == "child"
            assert row["worker_id"] == worker
            assert row["pack_jobs"] == "1"
            assert row["lane"] == "quick"
            assert row["marker"] == validate.QUICK_TESTS
            assert row["exclusions"] == "slow, exhaustive_exact"
            assert row["xdist_workers"] == 2
            assert isinstance(row["monotonic_ns"], int)
            assert datetime.fromisoformat(str(row["timestamp_utc"])).tzinfo is not None
    assert {node.rsplit("::", 1)[-1] for node in starts} == {
        "test_a",
        "test_b",
        "test_c",
        "test_d",
    }
    assert Path(f"{stem}.junit.xml").is_file()
    assert "slowest durations" in result.stdout


def test_failed_and_empty_children_leave_finished_session_receipts(tmp_path: Path) -> None:
    test_file = tmp_path / "test_probe.py"
    test_file.write_text("def test_bad(): assert False\n", encoding="utf-8")
    for label, extra, status in (("failed", (), 1), ("empty", ("-k", "absent"), 5)):
        stem = tmp_path / label
        result = subprocess.run(
            _probe(stem, test_file, workers=1, extra=extra),
            cwd=PACKING,
            env=_environment(stem, workers=1),
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )
        assert result.returncode == status, result.stdout + result.stderr
        rows = _rows(Path(f"{stem}.progress-main.jsonl"))
        assert rows[0]["event"] == "session_start"
        assert rows[-1]["event"] == "session_finish"
        assert rows[-1]["exit_status"] == status
        if label == "failed":
            assert [row["outcome"] for row in rows if row["event"] == "finish"] == ["failed"]
        else:
            assert not any(row["event"] == "start" for row in rows)


def test_terminated_child_keeps_a_flushed_unfinished_start(tmp_path: Path) -> None:
    test_file = tmp_path / "test_probe.py"
    test_file.write_text("import time\ndef test_wait(): time.sleep(30)\n", encoding="utf-8")
    stem = tmp_path / "interrupted"
    process = subprocess.Popen(
        _probe(stem, test_file, workers=1),
        cwd=PACKING,
        env=_environment(stem, workers=1),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    path = Path(f"{stem}.progress-main.jsonl")
    try:
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if path.exists() and any(row["event"] == "start" for row in _rows(path)):
                break
            if process.poll() is not None:
                pytest.fail(f"probe exited early with {process.returncode}")
            time.sleep(0.05)
        else:
            pytest.fail("probe never flushed a test start")
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
    rows = _rows(path)
    assert any(row["event"] == "session_start" for row in rows)
    assert any(row["event"] == "start" for row in rows)
    assert not any(row["event"] == "finish" for row in rows)


def test_wrapper_binds_child_receipts_to_parent_run_and_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent_stem = tmp_path / "command-probe"
    monkeypatch.setenv("PACKING_REACHABLE_TEST_ARTIFACT_STEM", str(parent_stem))
    monkeypatch.setenv("PACKING_REACHABLE_TEST_RUN_ID", "parent-run")
    monkeypatch.setenv("GIT_DIR", "/untrusted/git")
    monkeypatch.setattr(reachable_tests, "changed_paths", lambda _since: ["known"])
    monkeypatch.setattr(
        reachable_tests,
        "select_tests",
        lambda _changed: reachable_tests.TestSelection(
            everything=False, reason="fixture", tests=("packing/tests/test_reachable_tests.py",)
        ),
    )
    commands: list[tuple[str, ...]] = []
    child_environments: list[dict[str, str]] = []

    def run(command: tuple[str, ...], **kwargs: object) -> subprocess.CompletedProcess[str]:
        environment = cast("dict[str, str]", kwargs["env"])
        if command[:2] == ("git", "rev-parse"):
            assert "GIT_DIR" not in environment
            return subprocess.CompletedProcess(command, 0, stdout=SOURCE + "\n")
        commands.append(command)
        child_environments.append(environment)
        return subprocess.CompletedProcess(command, 7)

    monkeypatch.setattr(reachable_tests.subprocess, "run", run)
    assert reachable_tests.main(["--run", "-n", "2"]) == 7
    assert len(commands) == 1
    command = commands[0]
    assert command[command.index("-m", 2) :][:2] == ("-m", validate.QUICK_TESTS)
    assert command[command.index("-n") :][:2] == ("-n", "2")
    assert "--durations=0" in command
    assert "-p" in command
    assert "devtools.reachable_progress" in command
    assert f"--junitxml={parent_stem}.pytest-all.junit.xml" in command
    child = child_environments[0]
    assert child["PACKING_REACHABLE_TEST_ARTIFACT_STEM"] == f"{parent_stem}.pytest-all"
    assert child["PACKING_REACHABLE_TEST_RUN_ID"] == "parent-run"
    assert child["PACKING_REACHABLE_TEST_SOURCE_COMMIT"] == SOURCE
    assert child["PACKING_REACHABLE_TEST_WORKERS"] == "2"
    assert child["PACKING_REACHABLE_TEST_LANE"] == "quick"
    assert child["PACKING_REACHABLE_TEST_MARKER"] == validate.QUICK_TESTS
    assert child["PACKING_REACHABLE_TEST_EXCLUSIONS"] == "slow, exhaustive_exact"


def test_wrapper_refuses_receipts_inside_the_source_checkout(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PACKING_REACHABLE_TEST_ARTIFACT_STEM", str(PACKING / "inside-source"))
    monkeypatch.setattr(reachable_tests, "changed_paths", lambda _since: ["known"])
    monkeypatch.setattr(
        reachable_tests,
        "select_tests",
        lambda _changed: reachable_tests.TestSelection(
            everything=False, reason="fixture", tests=("packing/tests/test_reachable_tests.py",)
        ),
    )
    with pytest.raises(SystemExit) as error:
        reachable_tests.main(["--run"])
    assert error.value.code == 2


def test_parent_artifact_runner_gives_wrapper_its_own_command_stem(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    artifacts = tmp_path / "artifacts"
    seen: list[dict[str, str]] = []

    def capture(context: validate.Context, _command: object, **_kwargs: object) -> str:
        seen.append(context.environment)
        return "child completed"

    monkeypatch.setattr(validate, "_run_command", capture)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={"PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts)},
    )
    command_runner = validate._run  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert (
        command_runner(context, (sys.executable, "-m", "devtools.reachable_tests", "--run"))
        == "child completed"
    )
    assert len(seen) == 1
    child = seen[0]
    assert "PACKING_VALIDATION_ARTIFACT_DIR" not in child
    assert child["PACKING_REACHABLE_TEST_RUN_ID"] == context.artifact_run_id
    assert Path(child["PACKING_REACHABLE_TEST_ARTIFACT_STEM"]).parent == artifacts
    assert len(list(artifacts.glob("command-*.start.json"))) == 1


@pytest.mark.parametrize("lane", ["quick", "slow"])
def test_native_lanes_bind_progress_to_their_run_source_and_workers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, lane: str
) -> None:
    artifacts = tmp_path / "artifacts"
    children: list[tuple[validate.Context, tuple[str, ...]]] = []

    def git(command: tuple[str, ...], **options: object) -> subprocess.CompletedProcess[str]:
        assert command == ("git", "rev-parse", "HEAD")
        assert options["cwd"] == validate.REPOSITORY_ROOT
        assert "GIT_DIR" not in cast("dict[str, str]", options["env"])
        return subprocess.CompletedProcess(command, 0, stdout=SOURCE + "\n")

    def capture(context: validate.Context, command: Sequence[str], **_options: object) -> str:
        children.append((context, tuple(command)))
        return "==== slowest durations ====\n(0 durations < 0.005s hidden.)"

    monkeypatch.setattr(validate.subprocess, "run", git)
    monkeypatch.setattr(validate, "_run_command", capture)
    for workers in (4, 1):
        monkeypatch.setattr(validate, "_pytest_workers", lambda _jobs, count=workers: count)
        context = validate.Context(
            deep=False,
            strict=False,
            jobs=1,
            inner_jobs=2,
            timeout_seconds=1800,
            environment={
                "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts),
                "GIT_DIR": "/untrusted/git",
                "PACK_JOBS": "2",
                "PACKING_REACHABLE_TEST_SOURCE_COMMIT": "stale",
                "PACKING_REACHABLE_TEST_WORKERS": "99",
            },
        )
        if lane == "slow":
            _slow_lane(context)
        else:
            _run_native(context, _quick_lane_command(1, 3))
        child, command = children[-1]
        environment = child.environment
        assert "PACKING_VALIDATION_ARTIFACT_DIR" not in environment
        assert environment["PACKING_REACHABLE_TEST_RUN_ID"] == context.artifact_run_id
        assert environment["PACKING_REACHABLE_TEST_SOURCE_COMMIT"] == SOURCE
        assert environment["PACKING_REACHABLE_TEST_WORKERS"] == str(workers)
        assert environment["PACKING_REACHABLE_TEST_LANE"] == lane
        assert environment["PACKING_REACHABLE_TEST_MARKER"] == (
            validate.SLOW_TESTS if lane == "slow" else validate.QUICK_TESTS
        )
        assert environment["PACKING_REACHABLE_TEST_EXCLUSIONS"] == (
            "quick, exhaustive_exact" if lane == "slow" else "slow, exhaustive_exact"
        )
        assert environment["PACKING_REACHABLE_TEST_PHASES"] == "1"
        assert environment["PACK_JOBS"] == "2"
        stem = environment["PACKING_REACHABLE_TEST_ARTIFACT_STEM"]
        assert Path(stem).parent == artifacts
        if lane == "slow":
            expected = (
                sys.executable,
                "-m",
                "pytest",
                "-q",
                *validate.BEHAVIORAL_TEST_ROOTS,
                "-m",
                "slow and not exhaustive_exact",
                *(("-n", "4") if workers == 4 else ()),
                "--durations=0",
                "--durations-min=0",
                "-p",
                "devtools.reachable_progress",
                f"--junitxml={stem}.junit.xml",
            )
        else:
            expected = (
                *_quick_lane_command(1, 3),
                f"--test-file-costs={stem}.test-files.json",
                "-p",
                "devtools.reachable_progress",
                f"--junitxml={stem}.junit.xml",
            )
        assert command == expected
        end = json.loads(Path(f"{stem}.end.json").read_text())
        assert end["status"] == "passed"
        assert end["timeout_seconds"] == 1800
        assert end["inner_jobs"] == 2
    assert len(list(artifacts.glob("command-*.start.json"))) == 2
    assert (
        len(
            {child.environment["PACKING_REACHABLE_TEST_ARTIFACT_STEM"] for child, _ in children}
        )
        == 2
    )


def test_native_progress_refuses_unidentified_source_and_checkout_artifacts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={"PACKING_VALIDATION_ARTIFACT_DIR": str(tmp_path / "artifacts")},
    )
    command = (sys.executable, "-m", "pytest", "-m", validate.SLOW_TESTS)
    for output, status in (("unidentified", 0), (SOURCE, 1)):
        monkeypatch.setattr(
            validate.subprocess,
            "run",
            lambda *_args, source_status=status, source_stdout=output, **_kwargs: (
                subprocess.CompletedProcess(command, source_status, stdout=source_stdout)
            ),
        )
        with pytest.raises(validate.StepFailureError, match="source commit"):
            _run_native(context, command)
    monkeypatch.setattr(validate, "REPOSITORY_ROOT", tmp_path)
    with pytest.raises(validate.StepFailureError, match="outside the source checkout"):
        _run_native(context, command)
    assert not list((tmp_path / "artifacts").iterdir())


def test_native_lanes_without_artifacts_keep_their_command_and_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    context = validate.Context(
        deep=False, strict=False, jobs=1, inner_jobs=2, environment={"PACK_JOBS": "2"}
    )
    commands = (
        _quick_lane_command(1, 3),
        (sys.executable, "-m", "pytest", "-m", validate.SLOW_TESTS),
    )
    seen: list[Sequence[str]] = []

    def capture(child: validate.Context, command: Sequence[str], **_options: object) -> str:
        assert child is context
        seen.append(command)
        return "unchanged"

    monkeypatch.setattr(validate, "_run_command", capture)
    for command in commands:
        assert _run_native(context, command) == "unchanged"
    assert seen == list(commands)


def _native_probe(test_file: Path) -> tuple[str, ...]:
    return (
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-c",
        os.devnull,
        "--rootdir",
        str(test_file.parent),
        "--basetemp",
        str(test_file.parent / "child-tmp"),
        str(test_file),
        "-m",
        validate.SLOW_TESTS,
    )


def test_native_lane_completes_with_phase_progress_and_junit(tmp_path: Path) -> None:
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "import pytest\n@pytest.mark.slow\ndef test_complete(): pass\n", encoding="utf-8"
    )
    artifacts = tmp_path / "artifacts"
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=2,
        environment={**os.environ, "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts)},
        timeout_seconds=15,
    )
    _run_native(context, _native_probe(test_file))
    rows = _rows(next(artifacts.glob("*.progress-main.jsonl")))
    assert [row["event"] for row in rows] == [
        "session_start",
        "start",
        "phase_finish",
        "phase_finish",
        "phase_finish",
        "finish",
        "session_finish",
    ]
    assert [row["phase"] for row in rows if row["event"] == "phase_finish"] == [
        "setup",
        "call",
        "teardown",
    ]
    assert all(row["outcome"] == "passed" for row in rows if "outcome" in row)
    assert rows[-1]["exit_status"] == 0
    assert {row["run_id"] for row in rows} == {context.artifact_run_id}
    assert len(list(artifacts.glob("*.junit.xml"))) == 1


def test_native_progress_uses_effective_workers_from_pytest_addopts(tmp_path: Path) -> None:
    for label, addopts, worker_ids, count in (
        ("distributed", "-n 2", {"gw0", "gw1"}, 2),
        ("serial", "", {"main"}, 1),
    ):
        root = tmp_path / label
        root.mkdir()
        test_file = root / "test_probe.py"
        test_file.write_text(
            "import pytest\n@pytest.mark.slow\ndef test_complete(): pass\n",
            encoding="utf-8",
        )
        artifacts = root / "artifacts"
        context = validate.Context(
            deep=False,
            strict=False,
            jobs=1,
            inner_jobs=2,
            environment={
                **os.environ,
                "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts),
                "PYTEST_ADDOPTS": (
                    "-o tmp_path_retention_policy=failed -o tmp_path_retention_count=1 "
                    f"{addopts}"
                ),
            },
            timeout_seconds=15,
        )
        _run_native(context, _native_probe(test_file))
        paths = list(artifacts.glob("*.progress-*.jsonl"))
        assert len(paths) == count
        rows = [row for path in paths for row in _rows(path)]
        assert {row["worker_id"] for row in rows} == worker_ids
        assert {row["xdist_workers"] for row in rows} == {count}
        assert {row["run_id"] for row in rows} == {context.artifact_run_id}
        assert sum(row["event"] == "finish" for row in rows) == 1
        assert sum(row["event"] == "session_finish" for row in rows) == count


def test_native_lane_cancellation_keeps_its_last_completed_phase(tmp_path: Path) -> None:
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "import time, pytest\n@pytest.mark.slow\ndef test_wait(): time.sleep(30)\n",
        encoding="utf-8",
    )
    artifacts = tmp_path / "artifacts"
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=2,
        environment={**os.environ, "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts)},
        timeout_seconds=15,
    )
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(_run_native, context, _native_probe(test_file))
        try:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                paths = list(artifacts.glob("*.progress-main.jsonl"))
                if paths and any(row.get("phase") == "setup" for row in _rows(paths[0])):
                    break
                if future.done():
                    future.result()
                    pytest.fail("native probe finished before its blocked call")
                time.sleep(0.05)
            else:
                pytest.fail("native probe never flushed setup completion")
        finally:
            context.processes.stop()
        with pytest.raises(validate.StepCancelledError):
            future.result(timeout=5)
    rows = _rows(next(artifacts.glob("*.progress-main.jsonl")))
    assert [row["event"] for row in rows] == ["session_start", "start", "phase_finish"]
    assert rows[-1]["phase"] == "setup"
    assert rows[-1]["outcome"] == "passed"
    assert str(rows[-1]["nodeid"]).endswith("::test_wait")
    assert not list(artifacts.glob("*.junit.xml"))
    end = json.loads(next(artifacts.glob("*.end.json")).read_text())
    assert end["status"] == "cancelled"


def test_browser_owner_keeps_progress_without_a_marker_expression(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    children: list[tuple[validate.Context, Sequence[str]]] = []

    def capture(context: validate.Context, command: Sequence[str], **_options: object) -> str:
        children.append((context, command))
        return "passed"

    monkeypatch.setattr(validate, "_run_command", capture)
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=2,
        inner_jobs=1,
        environment={
            **os.environ,
            "PACKING_VALIDATION_ARTIFACT_DIR": str(tmp_path / "artifacts"),
        },
    )
    validate._site_layout_tests(context)  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    assert len(children) == 3
    for child, command in children:
        assert "devtools.reachable_progress" in command
        assert child.environment["PACKING_REACHABLE_TEST_MARKER"] == ""
        assert child.environment["PACKING_REACHABLE_TEST_PHASES"] == "1"
        assert child.environment["PACKING_REACHABLE_TEST_SOURCE_COMMIT"]
    assert [child.environment["PACKING_REACHABLE_TEST_LANE"] for child, _ in children] == [
        "browser-functional",
        "browser-forwarders",
        "browser-load",
    ]
    assert [
        child.environment["PACKING_REACHABLE_TEST_EXCLUSIONS"] for child, _ in children
    ] == [
        f"tests/test_site_forwarders.py, {validate.SITE_LOAD_BUDGET_TEST}",
        "all other browser cases",
        "all other browser cases",
    ]


def test_explicit_pytest_progress_refuses_other_commands_before_writing(tmp_path: Path) -> None:
    artifacts = tmp_path / "artifacts"
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={"PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts)},
    )
    with pytest.raises(validate.StepFailureError, match="native pytest command"):
        _run_native(
            context,
            (sys.executable, "-c", "raise AssertionError('must not execute')"),
            pytest_progress=("browser", "none"),
        )
    assert not artifacts.exists()


def test_failed_phase_is_flushed_before_a_later_call_is_cancelled(tmp_path: Path) -> None:
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "import time, pytest\n"
        "@pytest.mark.slow\ndef test_bad(): assert False, 'retained assertion detail'\n"
        "@pytest.mark.slow\ndef test_wait(): time.sleep(30)\n",
        encoding="utf-8",
    )
    artifacts = tmp_path / "artifacts"
    context = validate.Context(
        deep=False,
        strict=False,
        jobs=1,
        inner_jobs=1,
        environment={**os.environ, "PACKING_VALIDATION_ARTIFACT_DIR": str(artifacts)},
        timeout_seconds=15,
    )
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(_run_native, context, _native_probe(test_file))
        try:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                paths = list(artifacts.glob("*.progress-main.jsonl"))
                if paths and any(
                    str(row["nodeid"]).endswith("::test_wait") and row.get("phase") == "setup"
                    for row in _rows(paths[0])
                ):
                    break
                if future.done():
                    future.result()
                    pytest.fail("probe exited before the blocked call")
                time.sleep(0.05)
            else:
                pytest.fail("probe never reached the blocked call")
        finally:
            context.processes.stop()
        with pytest.raises(validate.StepCancelledError):
            future.result(timeout=5)
    rows = _rows(next(artifacts.glob("*.progress-main.jsonl")))
    (failure,) = [row for row in rows if row["event"] == "failure"]
    assert str(failure["nodeid"]).endswith("::test_bad")
    assert failure["phase"] == "call"
    assert "retained assertion detail" in str(failure["longrepr"])
    assert not list(artifacts.glob("*.junit.xml"))


def test_pool_phases_have_distinct_receipts_and_effective_resource_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    parent_stem = tmp_path / "command-pool"
    monkeypatch.setenv("PACKING_REACHABLE_TEST_ARTIFACT_STEM", str(parent_stem))
    monkeypatch.setenv("PACKING_REACHABLE_TEST_RUN_ID", "parent-pool-run")
    monkeypatch.setattr(reachable_tests, "changed_paths", lambda _since: ["known"])
    monkeypatch.setattr(
        reachable_tests,
        "select_tests",
        lambda _changed: reachable_tests.TestSelection(
            everything=False, reason="fixture", tests=("packing/tests/test_reachable_tests.py",)
        ),
    )
    children: list[tuple[tuple[str, ...], dict[str, str]]] = []
    git_calls = 0

    def run(command: tuple[str, ...], **kwargs: object) -> subprocess.CompletedProcess[str]:
        nonlocal git_calls
        if command[:2] == ("git", "rev-parse"):
            git_calls += 1
            return subprocess.CompletedProcess(command, 0, stdout=SOURCE + "\n")
        children.append((command, cast("dict[str, str]", kwargs["env"])))
        return subprocess.CompletedProcess(command, 0)

    monkeypatch.setattr(reachable_tests.subprocess, "run", run)
    assert reachable_tests.main(["--run", "-n", "3", "--pool-workers", "3"]) == 0
    assert git_calls == 1
    assert len(children) == 2
    for (command, environment), name, workers, pack_jobs in zip(
        children, ("normal", "pool"), ("3", "1"), ("1", "3"), strict=True
    ):
        stem = f"{parent_stem}.pytest-{name}"
        assert f"--junitxml={stem}.junit.xml" in command
        assert environment["PACKING_REACHABLE_TEST_ARTIFACT_STEM"] == stem
        assert environment["PACKING_REACHABLE_TEST_RUN_ID"] == "parent-pool-run"
        assert environment["PACKING_REACHABLE_TEST_SOURCE_COMMIT"] == SOURCE
        assert environment["PACKING_REACHABLE_TEST_WORKERS"] == workers
        assert environment["PACK_JOBS"] == pack_jobs
        assert environment["PACKING_REACHABLE_TEST_LANE"] == "quick"
        assert environment["PACKING_REACHABLE_TEST_EXCLUSIONS"] == "slow, exhaustive_exact"
        assert (
            environment["PACKING_REACHABLE_TEST_MARKER"] == command[command.index("-m", 2) + 1]
        )


def _timed_environment(stem: Path, *, workers: int) -> dict[str, str]:
    environment = _environment(stem, workers=workers)
    plugin = Path(reachable_progress.__file__).resolve()
    environment.update(
        {
            "PACKING_REACHABLE_TEST_PHASES": "1",
            reachable_progress.PHASE_PLUGIN_PATH: str(plugin),
        }
    )
    environment.pop("PYTEST_ADDOPTS", None)
    return environment


@pytest.mark.parametrize(
    ("outcome", "seconds"), [("passed", 0.0), ("failed", 0.125), ("skipped", 0.375)]
)
@pytest.mark.parametrize("phase", ["setup", "call", "teardown"])
def test_phase_row_uses_actual_report_duration_once(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    outcome: Literal["passed", "failed", "skipped"],
    seconds: float,
    phase: Literal["setup", "call", "teardown"],
) -> None:
    monkeypatch.setenv("PACKING_REACHABLE_TEST_PHASES", "1")
    stem = tmp_path / "measured"
    writer = reachable_progress.ProgressWriter(
        stem, worker_id="main", run_id="actual-duration", source_commit=SOURCE, workers=1
    )
    nodeid = "test_probe.py::test_actual"
    writer.pytest_runtest_logstart(nodeid, ("test_probe.py", 1, "test_actual"))
    report = pytest.TestReport(
        nodeid=nodeid,
        location=("test_probe.py", 1, "test_actual"),
        keywords={},
        outcome=outcome,
        longrepr="retained failure" if outcome == "failed" else None,
        when=phase,
        sections=[],
        duration=seconds,
        start=10.0,
        stop=99.0,
    )
    writer.pytest_runtest_logreport(report)
    writer.pytest_sessionfinish(0)
    rows = _rows(Path(f"{stem}.progress-main.jsonl"))
    measured = [row for row in rows if "duration_seconds" in row]
    assert len(measured) == 1
    assert measured[0]["event"] == "phase_finish"
    assert measured[0]["duration_seconds"] == seconds
    assert measured[0]["outcome"] == outcome
    assert measured[0]["phase"] == phase
    assert rows[0]["phase_timing_capability"] == reachable_progress.PHASE_CAPABILITY


@pytest.mark.parametrize("workers", [1, 2])
def test_quantitative_phases_match_the_same_run_junit(tmp_path: Path, workers: int) -> None:
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "import pytest\n"
        "@pytest.fixture\n"
        "def prepared():\n"
        "    assert sum(range(100)) == 4950\n"
        "    yield\n"
        "    assert sum(range(100)) == 4950\n"
        "class TestPhases:\n"
        "    @pytest.mark.parametrize('value', [0, 1], ids=['has::separator', 'ordinary'])\n"
        "    def test_actual(self, prepared, value):\n"
        "        assert value in (0, 1)\n",
        encoding="utf-8",
    )
    stem = tmp_path / "timed"
    result = subprocess.run(
        _probe(
            stem,
            test_file,
            workers=workers,
            extra=(
                f"--reachable-phase-timings={reachable_progress.PHASE_CAPABILITY}",
                "-o",
                "junit_duration_report=total",
            ),
        ),
        cwd=PACKING,
        env=_timed_environment(stem, workers=workers),
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    paths = sorted(tmp_path.glob("timed.progress-*.jsonl"))
    assert len(paths) == workers
    durations: dict[tuple[str, str], list[float]] = {}
    for path in paths:
        rows = _rows(path)
        assert rows[0]["phase_plugin_path"] == str(Path(reachable_progress.__file__).resolve())
        assert rows[0]["phase_timing_capability"] == reachable_progress.PHASE_CAPABILITY
        assert rows[-1]["event"] == "session_finish"
        for row in rows:
            if row["event"] != "phase_finish":
                assert "duration_seconds" not in row
                continue
            seconds = row["duration_seconds"]
            assert isinstance(seconds, (int, float))
            assert not isinstance(seconds, bool)
            assert math.isfinite(seconds)
            assert seconds >= 0
            # This controlled class has a single class separator; parameter :: stays intact.
            _, class_name, name = str(row["nodeid"]).split("::", 2)
            durations.setdefault((class_name, name), []).append(float(seconds))
    cases = ET.parse(Path(f"{stem}.junit.xml")).findall(".//testcase")
    assert len(cases) == 2
    assert set(durations) == {
        ("TestPhases", "test_actual[has::separator]"),
        ("TestPhases", "test_actual[ordinary]"),
    }
    for case in cases:
        key = (case.get("classname", "").rsplit(".", 1)[-1], case.get("name", ""))
        assert len(durations[key]) == 3
        assert float(case.get("time", "")) == pytest.approx(sum(durations[key]), abs=0.001)


@pytest.mark.parametrize("explicit", [True, False])
def test_actual_worker_only_identity_mismatch_refuses_before_collection(
    tmp_path: Path, *, explicit: bool
) -> None:
    markers = tmp_path / "admission-markers"
    markers.mkdir()
    probe_plugin = tmp_path / "worker_admission_probe.py"
    setting = reachable_progress.PHASE_PLUGIN_PATH
    mismatch = str(tmp_path / "other-plugin.py")
    injected = (
        f"        os.environ[{setting!r}] = {mismatch!r}\n"
        if explicit
        else "        raise pytest.UsageError('controlled worker startup failure')\n"
    )
    probe_plugin.write_text(
        "import os\nfrom pathlib import Path\nimport pytest\n"
        "@pytest.hookimpl(tryfirst=True)\n"
        "def pytest_configure(config):\n"
        "    worker = getattr(config, 'workerinput', {}).get('workerid', 'controller')\n"
        f"    markers = Path({str(markers)!r})\n"
        "    if worker == 'gw1':\n"
        "        (markers / 'gw1-mismatch').write_text('injected before admission')\n"
        + injected
        + "@pytest.hookimpl(tryfirst=True)\n"
        "def pytest_sessionstart(session):\n"
        "    if not hasattr(session.config, 'workerinput'):\n"
        f"        (Path({str(markers)!r}) / 'controller-admitted')"
        ".write_text('configure completed')\n",
        encoding="utf-8",
    )
    test_file = tmp_path / "test_worker_sentinel.py"
    test_file.write_text(
        "import os\nfrom pathlib import Path\n"
        "worker = os.environ.get('PYTEST_XDIST_WORKER', 'controller')\n"
        f"markers = Path({str(markers)!r})\n"
        "(markers / f'collected-{worker}').write_text('collected')\n"
        "def test_sentinel():\n"
        "    (markers / f'executed-{worker}').write_text('executed')\n",
        encoding="utf-8",
    )
    stem = tmp_path / "worker-refusal"
    environment = _timed_environment(stem, workers=2)
    environment["PYTHONPATH"] = os.pathsep.join((str(tmp_path), environment["PYTHONPATH"]))
    process = subprocess.Popen(
        _probe(
            stem,
            test_file,
            workers=2,
            extra=(
                "-p",
                "worker_admission_probe",
                *(
                    (f"--reachable-phase-timings={reachable_progress.PHASE_CAPABILITY}",)
                    if explicit
                    else ()
                ),
                "--max-worker-restart=0",
            ),
        ),
        cwd=PACKING,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=30)
    finally:
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=5)
    assert process.returncode != 0, stdout + stderr
    expected_error = (
        "actual phase timing plugin path or settings differ"
        if explicit
        else "controlled worker startup failure"
    )
    assert expected_error in stdout + stderr
    assert (markers / "controller-admitted").is_file()
    assert (markers / "gw1-mismatch").is_file()
    assert not (markers / "collected-gw1").exists()
    assert not (markers / "executed-gw1").exists()
    assert not Path(f"{stem}.progress-gw1.jsonl").exists()
    # A healthy worker may have started before controller abort; retain its raw evidence.
    for path in tmp_path.glob("worker-refusal.progress-*.jsonl"):
        assert path.name == "worker-refusal.progress-gw0.jsonl"
    assert all(row["worker_id"] == "gw0" for row in _flushed_progress(stem))


def _flushed_progress(stem: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted(stem.parent.glob(f"{stem.name}.progress-*.jsonl")):
        # Poll only complete rows while a worker may be writing its final line.
        rows.extend(
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines(keepends=True)
            if line.endswith("\n")
        )
    return rows


def test_actual_worker_death_preserves_other_workers_measured_phases(tmp_path: Path) -> None:
    release = tmp_path / "release"
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "import os, time\nfrom pathlib import Path\n"
        "def test_a_healthy(): pass\n"
        "def test_b_healthy(): pass\n"
        "def test_c_crash():\n"
        f"    release = Path({str(release)!r})\n"
        "    deadline = time.monotonic() + 15\n"
        "    while not release.exists():\n"
        "        assert time.monotonic() < deadline\n"
        "        time.sleep(0.01)\n"
        "    os._exit(23)\n"
        "def test_d_after(): pass\n",
        encoding="utf-8",
    )
    stem = tmp_path / "worker-death"
    process = subprocess.Popen(
        _probe(
            stem,
            test_file,
            workers=2,
            extra=(
                f"--reachable-phase-timings={reachable_progress.PHASE_CAPABILITY}",
                "--max-worker-restart=0",
            ),
        ),
        cwd=PACKING,
        env=_timed_environment(stem, workers=2),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            rows = _flushed_progress(stem)
            healthy = any(
                row["event"] == "finish" and str(row["nodeid"]).endswith("::test_a_healthy")
                for row in rows
            )
            crash_setup = any(
                row["event"] == "phase_finish"
                and row["phase"] == "setup"
                and str(row["nodeid"]).endswith("::test_c_crash")
                for row in rows
            )
            if healthy and crash_setup:
                break
            if process.poll() is not None:
                pytest.fail(f"worker-death probe exited early: {process.returncode}")
            time.sleep(0.02)
        else:
            pytest.fail("worker-death probe never reached both observed phases")
        release.write_bytes(b"release")
        assert process.wait(timeout=15) != 0
    finally:
        with suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
        process.wait(timeout=5)
    paths = list(tmp_path.glob("worker-death.progress-*.jsonl"))
    assert len(paths) == 2
    rows = _flushed_progress(stem)
    healthy_rows = [row for row in rows if str(row["nodeid"]).endswith("::test_a_healthy")]
    crash_rows = [row for row in rows if str(row["nodeid"]).endswith("::test_c_crash")]
    assert {row["phase"] for row in healthy_rows if row["event"] == "phase_finish"} == {
        "setup",
        "call",
        "teardown",
    }
    assert all(
        "duration_seconds" in row for row in healthy_rows if row["event"] == "phase_finish"
    )
    assert any(row["phase"] == "setup" for row in crash_rows if row["event"] == "phase_finish")
    assert not any(
        row["event"] == "finish" or row.get("phase") in {"call", "teardown"}
        for row in crash_rows
    )
    assert {row["worker_id"] for row in healthy_rows}.isdisjoint(
        {row["worker_id"] for row in crash_rows}
    )


def test_unsupported_phase_capability_refuses_before_collection(tmp_path: Path) -> None:
    sentinel = tmp_path / "collected"
    source = tmp_path / "test_probe.py"
    source.write_text(
        f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('collected')\n"
        "def test_complete(): pass\n",
        encoding="utf-8",
    )
    stem = tmp_path / "unsupported"
    result = subprocess.run(
        _probe(stem, source, workers=1, extra=("--reachable-phase-timings=unsupported",)),
        cwd=PACKING,
        env=_timed_environment(stem, workers=1),
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )
    assert result.returncode != 0
    assert not sentinel.exists()
    assert not list(tmp_path.glob("unsupported.progress-*.jsonl"))


def test_worker_journal_exclusive_create_preserves_existing_evidence(tmp_path: Path) -> None:
    stem = tmp_path / "exclusive"
    writer = reachable_progress.ProgressWriter(
        stem, worker_id="main", run_id="exclusive", source_commit=SOURCE, workers=1
    )
    writer.pytest_sessionfinish(0)
    path = Path(f"{stem}.progress-main.jsonl")
    before = path.read_bytes()
    with pytest.raises(FileExistsError):
        reachable_progress.ProgressWriter(
            stem, worker_id="main", run_id="other-run", source_commit=SOURCE, workers=1
        )
    assert path.read_bytes() == before


@pytest.mark.parametrize(
    ("requested", "error", "incoming", "current", "expected"),
    [
        (False, "startup error", 0, 0, 0),
        (True, None, 0, 0, 0),
        (True, "startup error", 0, 0, 3),
        (True, "startup error", 1, 1, 1),
        (True, "startup error", 0, 1, 1),
        (True, "startup error", 3, 3, 3),
    ],
)
def test_opted_in_worker_failure_preserves_nonzero_exit_status(
    *,
    requested: bool,
    error: str | None,
    incoming: int,
    current: int,
    expected: int,
) -> None:
    config = Mock(spec=pytest.Config)
    config.stash = pytest.Stash()
    config.stash[reachable_progress._PHASE_REQUESTED] = requested  # noqa: SLF001  # pyright: ignore[reportPrivateUsage]
    node = Mock()
    node.config = config
    session = Mock(spec=pytest.Session)
    session.config = config
    session.exitstatus = current
    reachable_progress.pytest_testnodedown(node, error)
    reachable_progress.pytest_sessionfinish(session, incoming)
    assert session.exitstatus == expected


@pytest.mark.parametrize("duration", [float("nan"), float("inf"), -0.1])
def test_writer_refuses_invalid_quantitative_phase(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, duration: float
) -> None:
    monkeypatch.setenv("PACKING_REACHABLE_TEST_PHASES", "1")
    writer = reachable_progress.ProgressWriter(
        tmp_path / "invalid",
        worker_id="main",
        run_id="invalid",
        source_commit=SOURCE,
        workers=1,
    )
    try:
        with pytest.raises(ValueError, match="finite and nonnegative"):
            writer.pytest_runtest_logreport(
                pytest.TestReport(
                    nodeid="test_invalid.py::test_value",
                    location=("test_invalid.py", 1, "test_value"),
                    keywords={},
                    outcome="passed",
                    longrepr=None,
                    when="call",
                    duration=duration,
                )
            )
    finally:
        writer.pytest_sessionfinish(3)


def test_actual_failed_and_skipped_phases_keep_only_reported_durations(tmp_path: Path) -> None:
    source = tmp_path / "test_failures.py"
    source.write_text(
        "import pytest\n"
        "@pytest.fixture\ndef bad_setup(): assert False\n"
        "@pytest.fixture\ndef bad_teardown():\n    yield\n    assert False\n"
        "def test_setup(bad_setup): pass\n"
        "def test_teardown(bad_teardown): pass\n"
        "def test_call(): assert False\n"
        "def test_skip(): pytest.skip('controlled skip')\n"
    )
    stem = tmp_path / "failed-phases"
    result = subprocess.run(
        _probe(stem, source, workers=1),
        cwd=PACKING,
        env=_timed_environment(stem, workers=1),
        capture_output=True,
        text=True,
        check=False,
        timeout=20,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    rows = _rows(Path(f"{stem}.progress-main.jsonl"))
    phases = [row for row in rows if row["event"] == "phase_finish"]
    setup = [row for row in phases if str(row["nodeid"]).endswith("::test_setup")]
    assert [(row["phase"], row["outcome"]) for row in setup] == [
        ("setup", "failed"),
        ("teardown", "passed"),
    ]
    assert any(row["phase"] == "teardown" and row["outcome"] == "failed" for row in phases)
    assert any(row["phase"] == "call" and row["outcome"] == "skipped" for row in phases)
    assert all(
        isinstance(row["duration_seconds"], float) and row["duration_seconds"] >= 0
        for row in phases
    )
