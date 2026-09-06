"""Durable receipts survive a failed or interrupted benchmark command."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

from benchmarks import validation_timing
from benchmarks.validation_timing import main, run_sample


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
