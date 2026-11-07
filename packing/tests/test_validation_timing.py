"""Durable receipts survive a failed or interrupted benchmark command."""

from __future__ import annotations

import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from contextlib import suppress
from pathlib import Path
from typing import Any

import pytest

from benchmarks import validation_report, validation_timing
from benchmarks.validation_timing import main, run_sample
from devtools import reachable_progress


def test_failed_sample_retains_output_and_start_end_receipts(tmp_path: Path) -> None:
    result = run_sample(
        [sys.executable, "-c", "import sys; print('observed failure'); sys.exit(7)"],
        root=tmp_path,
        output_dir=tmp_path,
        metadata={"label": "failure", "allocated_workers": 2},
        timeout=5,
    )
    assert result["status"] == "failed"
    assert result["returncode"] == 7
    assert "observed failure" in Path(str(result["stdout_path"])).read_text()
    events = [
        json.loads(line) for line in (tmp_path / "receipts.jsonl").read_text().splitlines()
    ]
    assert [event["event"] for event in events] == ["start", "end"]
    assert events[0]["run_id"] == events[1]["run_id"]
    assert result["allocated_worker_seconds"] == 2 * result["wall_seconds"]


def test_timeout_keeps_partial_output(tmp_path: Path) -> None:
    result = run_sample(
        [sys.executable, "-c", "import time; print('started', flush=True); time.sleep(60)"],
        root=tmp_path,
        output_dir=tmp_path,
        metadata={"label": "timeout", "allocated_workers": 1},
        timeout=0.2,
    )
    assert result["status"] == "timeout"
    assert "started" in Path(str(result["stdout_path"])).read_text()
    assert result["wall_seconds"] < 3


def test_interrupt_reaps_the_command_and_finishes_its_receipt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_wait = subprocess.Popen.wait
    interrupted = False

    def wait(process: subprocess.Popen[bytes], timeout: float | None = None) -> int:
        nonlocal interrupted
        if not interrupted:
            interrupted = True
            raise KeyboardInterrupt
        return original_wait(process, timeout=timeout)

    monkeypatch.setattr(subprocess.Popen, "wait", wait)
    result = run_sample(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        root=tmp_path,
        output_dir=tmp_path,
        metadata={"label": "interrupt", "allocated_workers": 1},
        timeout=5,
    )
    assert result["status"] == "interrupted"
    assert result["returncode"] is not None
    assert result["returncode"] != 0
    assert Path(str(result["stdout_path"])).is_file()
    events = [
        json.loads(line) for line in (tmp_path / "receipts.jsonl").read_text().splitlines()
    ]
    assert [event["event"] for event in events] == ["start", "end"]
    assert events[-1]["status"] == "interrupted"


def test_pytest_run_writes_junit_and_distinct_receipts(tmp_path: Path) -> None:
    source = tmp_path / "test_probe.py"
    source.write_text("def test_probe():\n    assert True\n")
    output = tmp_path / "results"
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "--label",
                "probe",
                "--output-dir",
                str(output),
                "--repeats",
                "2",
                str(source),
            ]
        )
        == 0
    )
    events = [json.loads(line) for line in (output / "receipts.jsonl").read_text().splitlines()]
    ends = [event for event in events if event["event"] == "end"]
    assert len(ends) == 2
    assert len({event["run_id"] for event in ends}) == 2
    for event in ends:
        assert event["status"] == "passed"
        assert Path(event["junit_path"]).is_file()
        assert "slowest durations" in Path(event["stdout_path"]).read_text()
        assert event["source_hashes"][str(source)]
        assert event["environment"]["PACK_JOBS"] == "1"


def test_receipts_hash_exact_diff_and_untracked_imports(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "test_probe.py"
    source.write_text("def test_probe():\n    assert True\n")
    imported = tmp_path / "src/untracked module.py"
    imported.parent.mkdir()
    imported.write_bytes(b"untracked input\n")
    output = tmp_path / "receipts"
    output.mkdir()
    (output / "sample.log").write_bytes(b"not an input")
    raw = b" diff binary \xff\n\n"

    def git_result(command: list[str], **_kwargs: object) -> subprocess.CompletedProcess[bytes]:
        arguments = command[3:]
        if arguments == ["diff", "HEAD", "--binary"]:
            value = raw
        elif arguments == ["rev-parse", "--show-toplevel"]:
            value = str(tmp_path).encode() + b"\n"
        elif arguments == ["ls-files", "--others", "--exclude-standard", "-z"]:
            value = b"src/untracked module.py\0receipts/sample.log\0"
        else:
            value = b"fixture\n"
        return subprocess.CompletedProcess(command, 0, value, b"")

    monkeypatch.setattr(validation_timing.subprocess, "run", git_result)
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "--label",
                "provenance",
                "--output-dir",
                str(output),
                "--repeats",
                "1",
                str(source),
            ]
        )
        == 0
    )
    events = [json.loads(line) for line in (output / "receipts.jsonl").read_text().splitlines()]
    assert [event["event"] for event in events] == ["start", "end"]
    for event in events:
        assert event["dirty_diff_sha256"] == hashlib.sha256(raw).hexdigest()
        assert event["dirty_diff_hash_kind"] == "exact_git_diff_bytes"
        assert event["untracked_sha256"] == {
            "src/untracked module.py": hashlib.sha256(imported.read_bytes()).hexdigest()
        }


@pytest.fixture
def phase_checkout(tmp_path: Path) -> Path:
    repository = tmp_path / "checkout"
    root = repository / "packing"
    package = root / "devtools"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "reachable_progress.py").write_bytes(
        Path(reachable_progress.__file__).read_bytes()
    )
    environment = {
        name: value for name, value in os.environ.items() if not name.startswith("GIT_")
    }
    for command in (
        ["git", "init", "-q", str(repository)],
        ["git", "add", "--all"],
        [
            "git",
            "-c",
            "user.name=Phase control",
            "-c",
            "user.email=phase-control@example.invalid",
            "-c",
            "commit.gpgsign=false",
            "-c",
            "core.hooksPath=/dev/null",
            "commit",
            "-qm",
            "phase timing fixture",
        ],
    ):
        subprocess.run(
            command,
            cwd=repository,
            env=environment,
            capture_output=True,
            check=True,
            timeout=10,
        )
    return root


def _phase_metadata(root: Path) -> dict[str, Any]:
    return {
        "label": "phase-control",
        "allocated_workers": 1,
        "commit": validation_timing._git(root, "rev-parse", "HEAD"),  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    }


def _phase_command(root: Path, source: Path, output: Path) -> list[str]:
    return [
        sys.executable,
        "-m",
        "pytest",
        "-q",
        "-c",
        os.devnull,
        "--rootdir",
        str(root),
        "--basetemp",
        str(output / "pytest-tmp"),
        str(source),
        "--junitxml={junit}",
    ]


def _phase_rows(output: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(output.glob("*.progress-*.jsonl")):
        rows.extend(
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines(keepends=True)
            if line.endswith("\n")
        )
    return rows


def test_phase_timing_cli_has_distinct_stable_journals_and_clears_parent_settings(
    phase_checkout: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = phase_checkout / "test_probe.py"
    source.write_text("def test_complete(): pass\n", encoding="utf-8")
    output = tmp_path / "phase-results"
    inherited = tmp_path / "parent"
    monkeypatch.setenv("PACKING_REACHABLE_TEST_ARTIFACT_STEM", str(inherited))
    monkeypatch.setenv("PACKING_REACHABLE_TEST_RUN_ID", "inherited-run")
    monkeypatch.setenv("PACKING_REACHABLE_TEST_PHASE_PLUGIN_PATH", "wrong")
    assert (
        main(
            [
                "--root",
                str(phase_checkout),
                "--label",
                "phase-on",
                "--output-dir",
                str(output),
                "--repeats",
                "2",
                "--timeout",
                "20",
                "--phase-timings",
                str(source),
            ]
        )
        == 0
    )
    events = [json.loads(line) for line in (output / "receipts.jsonl").read_text().splitlines()]
    assert [event["event"] for event in events] == ["start", "end", "start", "end"]
    for start, end in zip(events[::2], events[1::2], strict=True):
        assert start["phase_timings"] == end["phase_timings"]
        assert start["phase_plugin_path"] == end["phase_plugin_path"]
        assert end["status"] == "passed"
        assert len(end["phase_journals"]) == 1
        rows = [
            json.loads(line) for line in Path(end["phase_journals"][0]).read_text().splitlines()
        ]
        assert rows[0]["phase_plugin_path"] == str(
            (phase_checkout / "devtools/reachable_progress.py").resolve()
        )
        assert {row["run_id"] for row in rows} == {start["run_id"]}
        assert sum(row["event"] == "phase_finish" for row in rows) == 3
        assert all("duration_seconds" in row for row in rows if row["event"] == "phase_finish")
    assert events[0]["phase_timings"]["stem"] != events[2]["phase_timings"]["stem"]
    assert not list(tmp_path.glob("parent.progress-*"))


@pytest.mark.parametrize("plugin", ["old-interface", "missing"])
def test_unavailable_phase_capability_fails_before_test_collection(
    phase_checkout: Path, tmp_path: Path, plugin: str
) -> None:
    plugin_path = phase_checkout / "devtools/reachable_progress.py"
    if plugin == "old-interface":
        plugin_path.write_text(
            'SCHEMA = "reachable-progress-v1"\ndef pytest_configure(config):\n    pass\n',
            encoding="utf-8",
        )
    else:
        plugin_path.rename(plugin_path.with_name("saved_without_plugin.py"))
    sentinel = tmp_path / "collected"
    source = phase_checkout / "test_probe.py"
    source.write_text(
        f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('collected')\n"
        "def test_complete(): pass\n",
        encoding="utf-8",
    )
    output = tmp_path / "refused"
    result = run_sample(
        _phase_command(phase_checkout, source, output),
        root=phase_checkout,
        output_dir=output,
        metadata=_phase_metadata(phase_checkout),
        timeout=20,
        phase_timings=True,
    )
    assert result["status"] == "failed"
    assert not sentinel.exists()
    assert result["phase_journals"] == []
    events = [json.loads(line) for line in (output / "receipts.jsonl").read_text().splitlines()]
    assert [event["event"] for event in events] == ["start", "end"]


def test_actual_import_from_another_checkout_is_refused(
    phase_checkout: Path, tmp_path: Path
) -> None:
    other_package = Path(reachable_progress.__file__).resolve().parent
    (phase_checkout / "devtools/__init__.py").write_text(
        f"__path__ = [{str(other_package)!r}]\n", encoding="utf-8"
    )
    sentinel = tmp_path / "collected"
    source = phase_checkout / "test_probe.py"
    source.write_text(
        f"from pathlib import Path\nPath({str(sentinel)!r}).write_text('collected')\n"
        "def test_complete(): pass\n",
        encoding="utf-8",
    )
    output = tmp_path / "wrong-import"
    result = run_sample(
        _phase_command(phase_checkout, source, output),
        root=phase_checkout,
        output_dir=output,
        metadata=_phase_metadata(phase_checkout),
        timeout=20,
        phase_timings=True,
    )
    assert result["status"] == "failed"
    assert not sentinel.exists()
    assert "actual phase timing plugin" in Path(result["stderr_path"]).read_text()
    assert result["phase_journals"] == []


def test_phase_source_drift_is_not_a_passing_observation(
    phase_checkout: Path, tmp_path: Path
) -> None:
    plugin = phase_checkout / "devtools/reachable_progress.py"
    source = phase_checkout / "test_probe.py"
    source.write_text(
        "from pathlib import Path\n"
        "def test_change_plugin():\n"
        f"    path = Path({str(plugin)!r})\n"
        "    path.write_text(path.read_text() + '\\n# source drift\\n')\n",
        encoding="utf-8",
    )
    output = tmp_path / "drift"
    result = run_sample(
        _phase_command(phase_checkout, source, output),
        root=phase_checkout,
        output_dir=output,
        metadata=_phase_metadata(phase_checkout),
        timeout=20,
        phase_timings=True,
    )
    assert result["returncode"] == 0
    assert result["status"] == "failed"
    assert "plugin changed during this invocation" in result["error"]


@pytest.mark.parametrize("location", ["relative", "inside", "symlink"])
def test_phase_output_must_be_external_and_absolute(
    phase_checkout: Path, tmp_path: Path, location: str
) -> None:
    output = Path("relative-phase-output")
    if location == "inside":
        output = phase_checkout / "phase-output"
    elif location == "symlink":
        alias = tmp_path / "source-alias"
        alias.symlink_to(phase_checkout, target_is_directory=True)
        output = alias / "phase-output"
    with pytest.raises(ValueError, match=r"absolute|outside source"):
        run_sample(
            [sys.executable, "-m", "pytest"],
            root=phase_checkout,
            output_dir=output,
            metadata=_phase_metadata(phase_checkout),
            timeout=5,
            phase_timings=True,
        )


def _blocked_phase_source(
    root: Path, pid_path: Path, *, descendant_path: Path | None = None
) -> Path:
    source = root / "test_blocked.py"
    descendant = ""
    if descendant_path is not None:
        descendant = (
            "    child = subprocess.Popen([sys.executable, '-c', "
            "'import time; time.sleep(60)'])\n"
            f"    Path({str(descendant_path)!r}).write_text(str(child.pid))\n"
        )
    source.write_text(
        "import os, subprocess, sys, time\nfrom pathlib import Path\n"
        "def test_blocked():\n"
        + descendant
        + f"    Path({str(pid_path)!r}).write_text(str(os.getpid()))\n"
        "    time.sleep(60)\n",
        encoding="utf-8",
    )
    return source


def _live_session_processes(session_id: int) -> list[int]:
    # This Linux control owns a private session. Orphan zombies are not executable;
    # the host test cannot waitpid grandchildren after their recorder parent dies.
    proc = Path("/proc")
    assert proc.is_dir(), "Linux /proc is required to confirm private pytest cleanup"
    live: list[int] = []
    for path in proc.glob("[0-9]*/stat"):
        try:
            fields = (
                path.read_text(encoding="utf-8", errors="replace").rsplit(")", 1)[1].split()
            )
        except FileNotFoundError, ProcessLookupError:
            continue
        # /proc/PID/stat fields after comm: state, ppid, pgrp, session, ...
        if int(fields[3]) == session_id and fields[0] not in {"Z", "X", "x"}:
            live.append(int(path.parent.name))
    return sorted(live)


def _assert_no_live_session_processes(session_id: int) -> None:
    deadline = time.monotonic() + 5
    while True:
        live = _live_session_processes(session_id)
        if not live:
            return
        if time.monotonic() >= deadline:
            pytest.fail(f"live pytest session {session_id} survived cleanup: {live}")
        time.sleep(0.02)


def _wait_for_blocked_setup(output: Path, pid_path: Path) -> int:
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        rows = _phase_rows(output)
        if pid_path.exists() and any(
            row["event"] == "phase_finish" and row["phase"] == "setup" for row in rows
        ):
            return int(pid_path.read_text())
        time.sleep(0.02)
    pytest.fail("child never flushed setup and its private pytest PID")


def _assert_only_completed_setup(output: Path) -> None:
    rows = _phase_rows(output)
    phases = [row for row in rows if row["event"] == "phase_finish"]
    assert [row["phase"] for row in phases] == ["setup"]
    assert isinstance(phases[0]["duration_seconds"], float)
    assert phases[0]["duration_seconds"] >= 0
    assert not any(row["event"] in {"finish", "session_finish"} for row in rows)


def test_hard_killed_pytest_retains_duration_and_failed_outer_receipt(
    phase_checkout: Path, tmp_path: Path
) -> None:
    output = tmp_path / "hard-pytest"
    pid_path = tmp_path / "pytest-pid"
    source = _blocked_phase_source(phase_checkout, pid_path)
    pid: int | None = None
    with ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(
            run_sample,
            _phase_command(phase_checkout, source, output),
            root=phase_checkout,
            output_dir=output,
            metadata=_phase_metadata(phase_checkout),
            timeout=25,
            phase_timings=True,
        )
        try:
            pid = _wait_for_blocked_setup(output, pid_path)
            os.killpg(pid, signal.SIGKILL)
            result = future.result(timeout=5)
        finally:
            if pid is not None:
                with suppress(ProcessLookupError):
                    os.killpg(pid, signal.SIGKILL)
    assert result["status"] == "failed"
    assert result["returncode"] == -signal.SIGKILL
    _assert_only_completed_setup(output)
    assert not Path(result["junit_path"]).exists()


@pytest.mark.skipif(
    sys.platform != "linux",
    reason=(
        "Linux /proc is required to confirm no live pytest descendants after recorder SIGKILL"
    ),
)
def test_hard_killed_recorder_keeps_unmatched_start_and_known_phase(
    phase_checkout: Path, tmp_path: Path
) -> None:
    output = tmp_path / "hard-recorder"
    pid_path = tmp_path / "pytest-pid"
    descendant_path = tmp_path / "pytest-descendant-pid"
    source = _blocked_phase_source(phase_checkout, pid_path, descendant_path=descendant_path)
    packing = Path(__file__).resolve().parents[1]
    environment = dict(os.environ)
    environment["PYTHONPATH"] = os.pathsep.join((str(packing / "src"), str(packing)))
    environment.pop("PYTEST_ADDOPTS", None)
    recorder = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "benchmarks.validation_timing",
            "--root",
            str(phase_checkout),
            "--label",
            "hard-recorder",
            "--output-dir",
            str(output),
            "--repeats",
            "1",
            "--timeout",
            "25",
            "--phase-timings",
            str(source),
        ],
        cwd=packing,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    pytest_pid: int | None = None
    try:
        pytest_pid = _wait_for_blocked_setup(output, pid_path)
        assert os.getsid(pytest_pid) == pytest_pid
        assert pytest_pid != os.getsid(0)
        descendant_pid = int(descendant_path.read_text())
        assert os.getsid(descendant_pid) == pytest_pid
        assert {pytest_pid, descendant_pid} <= set(_live_session_processes(pytest_pid))
        recorder.kill()
        assert recorder.wait(timeout=5) == -signal.SIGKILL
        assert {pytest_pid, descendant_pid} <= set(_live_session_processes(pytest_pid))
    finally:
        if pytest_pid is None and recorder.poll() is None:
            # If startup failed before a PID marker, let the bounded wrapper clean its child.
            with suppress(subprocess.TimeoutExpired):
                recorder.wait(timeout=30)
        with suppress(ProcessLookupError):
            os.killpg(recorder.pid, signal.SIGKILL)
        if pytest_pid is None and pid_path.exists():
            pytest_pid = int(pid_path.read_text())
        if pytest_pid is not None:
            with suppress(ProcessLookupError):
                os.killpg(pytest_pid, signal.SIGKILL)
        recorder.wait(timeout=5)
        if pytest_pid is not None:
            _assert_no_live_session_processes(pytest_pid)
    events = [json.loads(line) for line in (output / "receipts.jsonl").read_text().splitlines()]
    assert [event["event"] for event in events] == ["start"]
    _assert_only_completed_setup(output)


def test_phase_opt_in_refuses_unidentified_source_with_a_failed_receipt(
    phase_checkout: Path, tmp_path: Path
) -> None:
    source = phase_checkout / "test_probe.py"
    source.write_text("raise AssertionError('collection must not run')\n", encoding="utf-8")
    output = tmp_path / "unidentified"
    metadata = _phase_metadata(phase_checkout)
    metadata["commit"] = ""
    result = run_sample(
        _phase_command(phase_checkout, source, output),
        root=phase_checkout,
        output_dir=output,
        metadata=metadata,
        timeout=10,
        phase_timings=True,
    )
    assert result["status"] == "failed"
    assert "current source provenance" in result["error"]
    assert result["phase_journals"] == []
    assert (output / "receipts.jsonl").is_file()


def test_phase_opt_in_does_not_execute_generic_commands(
    phase_checkout: Path, tmp_path: Path
) -> None:
    sentinel = tmp_path / "must-not-execute"
    output = tmp_path / "generic-refused"
    result = run_sample(
        [
            sys.executable,
            "-c",
            f"from pathlib import Path; Path({str(sentinel)!r}).write_text('executed')",
        ],
        root=phase_checkout,
        output_dir=output,
        metadata=_phase_metadata(phase_checkout),
        timeout=10,
        phase_timings=True,
    )
    assert result["status"] == "failed"
    assert "maintained pytest command" in result["error"]
    assert not sentinel.exists()


def test_phase_source_change_between_repeats_stops_the_invocation(
    phase_checkout: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = phase_checkout / "test_probe.py"
    source.write_text("def test_complete(): pass\n")
    plugin = phase_checkout / "devtools/reachable_progress.py"
    original = validation_timing.run_sample
    calls = 0

    def changed(*args: Any, **kwargs: Any) -> dict[str, Any]:
        nonlocal calls
        result = original(*args, **kwargs)
        calls += 1
        if calls == 1:
            plugin.write_bytes(plugin.read_bytes() + b"\n# changed between samples\n")
        return result

    monkeypatch.setattr(validation_timing, "run_sample", changed)
    output = tmp_path / "between-repeats"
    assert (
        main(
            [
                "--root",
                str(phase_checkout),
                "--label",
                "drift",
                "--output-dir",
                str(output),
                "--repeats",
                "3",
                "--timeout",
                "15",
                "--phase-timings",
                str(source),
            ]
        )
        == 1
    )
    ends = [
        json.loads(line)
        for line in (output / "receipts.jsonl").read_text().splitlines()
        if json.loads(line)["event"] == "end"
    ]
    assert calls == 2
    assert [row["status"] for row in ends] == ["passed", "failed"]


@pytest.mark.parametrize("failure", ["none", "timeout", "source-drift", "fixture-drift"])
def test_fixed_overhead_executor_uses_six_commands_or_stops_without_retry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    root = tmp_path / "checkout/packing"
    for name in (
        "benchmarks/validation_timing.py",
        "benchmarks/validation_report.py",
        "devtools/reachable_progress.py",
        "pyproject.toml",
        "uv.lock",
        ".python-version",
    ):
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("current input\n")
    monkeypatch.setattr(
        validation_timing, "__file__", str(root / "benchmarks/validation_timing.py")
    )
    monkeypatch.setattr(
        validation_report, "__file__", str(root / "benchmarks/validation_report.py")
    )
    monkeypatch.setattr(
        validation_timing,
        "_git",
        lambda _root, *args, **_kwargs: "a" * 40 if args == ("rev-parse", "HEAD") else "",
    )
    commands: list[list[str]] = []

    def sample(command: list[str], **options: Any) -> dict[str, Any]:
        commands.append(command)
        assert options["timeout"] == 45
        if failure == "source-drift":
            (root / "devtools/reachable_progress.py").write_text("changed current input\n")
        return {"status": "timeout" if failure == "timeout" else "passed"}

    monkeypatch.setattr(validation_timing, "run_sample", sample)

    def observation(
        evidence_root: Path,
        _protocol: dict[str, Any],
        index: int,
        _arm: str,
        _run: dict[str, Any],
    ) -> dict[str, Any]:
        if failure == "fixture-drift" and index == 0:
            fixture = evidence_root / "fixture/test_phase_timing_work.py"
            fixture.write_bytes(fixture.read_bytes() + b"\n# between-observation drift\n")
        return {}

    monkeypatch.setattr(validation_report, "phase_observation", observation)
    monkeypatch.setattr(validation_report, "phase_overhead", lambda _root: {"accepted": True})
    output = tmp_path / "comparison"
    assert validation_timing.phase_overhead_main(
        ["--root", str(root), "--output-dir", str(output)]
    ) == (0 if failure == "none" else 1)
    expected = list(validation_report.PHASE_ORDER) if failure == "none" else ["off"]
    assert [command[command.index("--label") + 1] for command in commands] == expected
    assert all(
        ("--phase-timings" in command) == (arm == "on")
        for command, arm in zip(commands, expected, strict=True)
    )
    completion = json.loads((output / "completion.json").read_text())
    assert completion["complete"] == (failure == "none")
    if failure == "fixture-drift":
        assert completion["error"] == "comparison fixture changed before observation"
    with pytest.raises(FileExistsError):
        validation_timing.phase_overhead_main(
            ["--root", str(root), "--output-dir", str(output)]
        )


def test_overhead_refuses_foreign_current_report_before_capture(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(validation_report, "__file__", str(tmp_path / "foreign_report.py"))
    with pytest.raises(ValueError, match="current report helper"):
        validation_timing.phase_overhead_main(
            ["--root", str(tmp_path), "--output-dir", str(tmp_path / "never-created")]
        )
    assert not (tmp_path / "never-created").exists()


@pytest.mark.parametrize("root_form", ["packing", "repository"])
def test_overhead_refuses_foreign_selected_root_with_active_sibling_pair(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, root_form: str
) -> None:
    active = Path(validation_timing.__file__).resolve().parents[1]
    foreign = tmp_path / "foreign/packing"
    for name in (
        "benchmarks/validation_timing.py",
        "benchmarks/validation_report.py",
        "devtools/reachable_progress.py",
        "pyproject.toml",
        "uv.lock",
        ".python-version",
    ):
        destination = foreign / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes((active / name).read_bytes())

    def unexpected_git(*_args: Any, **_kwargs: Any) -> str:
        pytest.fail("foreign selected root reached Git capture before live-origin admission")

    monkeypatch.setattr(validation_timing, "_git", unexpected_git)
    selected = foreign if root_form == "packing" else foreign.parent
    output = tmp_path / "never-created"
    with pytest.raises(ValueError, match=r"active timing/report modules.*selected root"):
        validation_timing.phase_overhead_main(
            ["--root", str(selected), "--output-dir", str(output)]
        )
    assert not output.exists()
