"""Child pytest receipts retain worker, source and partial-interruption evidence."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from contextlib import suppress
from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal, cast

import pytest

from devtools import reachable_progress, reachable_tests
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
            assert row["schema"] == "reachable-progress-v1"
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
    assert not list(tmp_path.glob("child.failures-*.jsonl"))
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


def _writer(stem: Path, *, worker_id: str = "main") -> reachable_progress.ProgressWriter:
    return reachable_progress.ProgressWriter(
        stem, worker_id=worker_id, run_id="focused-run", source_commit=SOURCE, workers=2
    )


def _report(
    phase: Literal["setup", "call", "teardown"],
    *,
    outcome: Literal["passed", "failed", "skipped"] = "failed",
) -> pytest.TestReport:
    return pytest.TestReport(
        nodeid="test_probe.py::test_bad",
        location=("test_probe.py", 0, "test_bad"),
        keywords={},
        outcome=outcome,
        longrepr=f"Full {phase} traceback\nλ: exact diagnostic\n",
        when=phase,
        sections=[
            (f"Captured stdout {phase}", "first\nsecond\n"),
            (f"Captured stderr {phase}", "stderr λ\n"),
            (f"Captured stdout {phase}", "repeated heading retained\n"),
        ],
        duration=0.01,
    )


def test_each_failed_phase_retains_full_diagnostic_and_provenance(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("PACK_JOBS", "3")
    stem = tmp_path / "phases"
    writer = _writer(stem)
    path = Path(f"{stem}.failures-main.jsonl")
    assert not path.exists()
    writer.pytest_runtest_logstart("test_probe.py::test_bad", ("test_probe.py", 0, "test_bad"))
    phases: tuple[Literal["setup", "call", "teardown"], ...] = ("setup", "call", "teardown")
    try:
        for count, phase in enumerate(phases, start=1):
            report = _report(phase)
            writer.pytest_runtest_logreport(report)
            assert path.read_bytes().endswith(b"\n")
            rows = _rows(path)
            assert len(rows) == count
            row = rows[-1]
            assert row["schema"] == "reachable-failure-v1"
            assert row["event"] == "failure"
            assert row["outcome"] == "failed"
            assert row["run_id"] == "focused-run"
            assert row["command_id"] == "phases"
            assert row["source_commit"] == SOURCE
            assert row["worker_id"] == "main"
            assert row["nodeid"] == report.nodeid
            assert row["phase"] == phase
            assert row["pack_jobs"] == "3"
            assert row["xdist_workers"] == 2
            assert isinstance(row["monotonic_ns"], int)
            assert datetime.fromisoformat(str(row["timestamp_utc"])).utcoffset() == timedelta(0)
            assert row["longreprtext"] == report.longreprtext
            assert row["sections"] == [list(section) for section in report.sections]
            progress = _rows(Path(f"{stem}.progress-main.jsonl"))
            assert sum(item["event"] == "finish" for item in progress) == (phase == "teardown")
    finally:
        writer.pytest_sessionfinish(1)
    assert len({row["nodeid"] for row in _rows(path)}) == 1
    assert writer.stream.closed
    assert writer.failure_stream is not None
    assert writer.failure_stream.closed


def test_failure_workers_own_separate_files(tmp_path: Path) -> None:
    stem = tmp_path / "workers"
    writers = [_writer(stem, worker_id=worker) for worker in ("gw0", "gw1")]
    try:
        for writer in writers:
            writer.pytest_runtest_logreport(_report("call"))
        for worker in ("gw0", "gw1"):
            rows = _rows(Path(f"{stem}.failures-{worker}.jsonl"))
            assert len(rows) == 1
            assert rows[0]["worker_id"] == worker
        assert not Path(f"{stem}.failures-main.jsonl").exists()
    finally:
        for writer in writers:
            writer.pytest_sessionfinish(1)


def test_failed_xdist_reports_have_no_controller_duplicates(tmp_path: Path) -> None:
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "def test_a(): assert False\ndef test_b(): assert False\n"
        "def test_c(): assert False\ndef test_d(): assert False\n",
        encoding="utf-8",
    )
    stem = tmp_path / "failed-workers"
    result = subprocess.run(
        _probe(stem, test_file, workers=2),
        cwd=PACKING,
        env=_environment(stem, workers=2),
        capture_output=True,
        text=True,
        check=False,
        timeout=30,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    files = sorted(tmp_path.glob("failed-workers.failures-*.jsonl"))
    assert {path.name for path in files} == {
        "failed-workers.failures-gw0.jsonl",
        "failed-workers.failures-gw1.jsonl",
    }
    reports = [row for path in files for row in _rows(path)]
    assert len(reports) == 4
    assert {row["nodeid"] for row in reports} == {
        f"test_probe.py::test_{name}" for name in ("a", "b", "c", "d")
    }
    assert {row["phase"] for row in reports} == {"call"}
    assert {row["worker_id"] for row in reports} == {"gw0", "gw1"}


def test_existing_failure_file_is_refused_without_losing_failed_outcome(tmp_path: Path) -> None:
    stem = tmp_path / "existing"
    path = Path(f"{stem}.failures-main.jsonl")
    original = "existing complete diagnostic\n"
    path.write_text(original, encoding="utf-8")
    writer = _writer(stem)
    try:
        with pytest.raises(FileExistsError):
            writer.pytest_runtest_logreport(_report("call"))
        assert path.read_text(encoding="utf-8") == original
        assert writer.failure_stream is None
        writer.pytest_runtest_logreport(_report("teardown", outcome="passed"))
        progress = _rows(Path(f"{stem}.progress-main.jsonl"))
        assert [row["outcome"] for row in progress if row["event"] == "finish"] == ["failed"]
    finally:
        writer.pytest_sessionfinish(1)
    with pytest.raises(FileExistsError):
        _writer(stem)
    assert path.read_text(encoding="utf-8") == original


def test_session_finish_closes_both_streams_when_progress_write_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    writer = _writer(tmp_path / "close")
    writer.pytest_runtest_logreport(_report("call"))

    def fail_emit(*_args: object, **_kwargs: object) -> None:
        raise OSError("progress write refused")

    monkeypatch.setattr(writer, "_emit", fail_emit)
    with pytest.raises(OSError, match="progress write refused"):
        writer.pytest_sessionfinish(1)
    assert writer.stream.closed
    assert writer.failure_stream is not None
    assert writer.failure_stream.closed


def test_pass_skip_and_xfail_children_do_not_create_failure_files(tmp_path: Path) -> None:
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "import pytest\n"
        "def test_pass(): pass\n"
        "@pytest.mark.skip(reason='control')\n"
        "def test_skip(): assert False\n"
        "@pytest.mark.xfail(strict=True, reason='control')\n"
        "def test_xfail(): assert False\n",
        encoding="utf-8",
    )
    stem = tmp_path / "no-failure"
    result = subprocess.run(
        _probe(stem, test_file, workers=1),
        cwd=PACKING,
        env=_environment(stem, workers=1),
        capture_output=True,
        text=True,
        check=False,
        timeout=20,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1 passed, 1 skipped, 1 xfailed" in result.stdout
    assert not list(tmp_path.glob("no-failure.failures-*.jsonl"))


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX process groups are required")
@pytest.mark.parametrize("phase", ["setup", "call"])
def test_failed_phase_is_readable_while_child_blocks_before_teardown_finishes(
    tmp_path: Path, phase: str
) -> None:
    test_file = tmp_path / "test_probe.py"
    test_file.write_text(
        "import os, time\n"
        "from pathlib import Path\n"
        "import pytest\n"
        "@pytest.fixture\n"
        "def failing(request):\n"
        "    def block():\n"
        "        Path(os.environ['PROBE_TEARDOWN_MARKER']).write_text('entered')\n"
        "        time.sleep(30)\n"
        "    request.addfinalizer(block)\n"
        "    if os.environ['PROBE_FAILURE_PHASE'] == 'setup':\n"
        "        print('setup captured stdout')\n"
        "        raise AssertionError('setup original failure')\n"
        "def test_bad(failing):\n"
        "    print('call captured stdout')\n"
        "    raise AssertionError('call original failure')\n",
        encoding="utf-8",
    )
    stem = tmp_path / "live-failure"
    path = Path(f"{stem}.failures-main.jsonl")
    marker = tmp_path / "teardown-entered"
    environment = {
        **_environment(stem, workers=1),
        "PROBE_TEARDOWN_MARKER": str(marker),
        "PROBE_FAILURE_PHASE": phase,
    }
    process = subprocess.Popen(
        _probe(stem, test_file, workers=1),
        cwd=PACKING,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    try:
        deadline = time.monotonic() + 10
        while time.monotonic() < deadline:
            if path.exists() and path.read_bytes().endswith(b"\n") and marker.exists():
                break
            if process.poll() is not None:
                pytest.fail(f"probe exited early with {process.returncode}")
            time.sleep(0.05)
        else:
            pytest.fail("probe never flushed a failure before its blocking teardown")
        assert process.poll() is None
        rows = _rows(path)
        assert len(rows) == 1
        row = rows[0]
        assert row["phase"] == phase
        assert row["nodeid"] == "test_probe.py::test_bad"
        assert f"{phase} original failure" in str(row["longreprtext"])
        assert [f"Captured stdout {phase}", f"{phase} captured stdout\n"] in cast(
            "list[list[str]]", row["sections"]
        )
        progress = _rows(Path(f"{stem}.progress-main.jsonl"))
        assert not any(row["event"] in {"finish", "session_finish"} for row in progress)
    finally:
        if process.poll() is None:
            with suppress(ProcessLookupError):
                os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=5)
    assert process.returncode == -signal.SIGTERM
    assert _rows(path) == rows


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
