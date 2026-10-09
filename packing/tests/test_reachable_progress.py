"""Child pytest receipts retain worker, source and partial-interruption evidence."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import cast

import pytest

from devtools import reachable_tests
from sqpack.cli import validate

PACKING = Path(__file__).resolve().parents[1]
SOURCE = "a" * 40


def _environment(stem: Path, *, workers: int) -> dict[str, str]:
    return {
        **os.environ,
        "PYTHONPATH": os.pathsep.join((str(PACKING), os.environ.get("PYTHONPATH", ""))),
        "PACKING_REACHABLE_TEST_ARTIFACT_STEM": str(stem),
        "PACKING_REACHABLE_TEST_RUN_ID": "focused-run",
        "PACKING_REACHABLE_TEST_SOURCE_COMMIT": SOURCE,
        "PACKING_REACHABLE_TEST_WORKERS": str(workers),
        "PACK_JOBS": "1",
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
    assert command[command.index("-m", 2) :][:2] == ("-m", "not exhaustive_exact")
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
