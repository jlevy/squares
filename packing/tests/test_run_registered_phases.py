"""Synthetic fresh-process phase execution and preserved failure evidence."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

from devtools import run_registered_phases as runner


def manifest(tmp_path: Path, *, failure: int | None = None) -> Path:
    phases = []
    for index in range(2):
        marker = tmp_path / f"child-{index}.json"
        code = (
            "import json,os,sys; from pathlib import Path; "
            "Path(sys.argv[1]).write_text(json.dumps({'pid':os.getpid(),'argv':sys.argv})); "
            "raise SystemExit(int(sys.argv[2]))"
        )
        phases.append(
            {
                "name": f"phase-{index}",
                "argv": [
                    sys.executable,
                    "-c",
                    code,
                    str(marker),
                    str(failure if index == 1 and failure else 0),
                ],
            }
        )
    path = tmp_path / "manifest.json"
    path.write_text(
        json.dumps({"phases": phases, "scientific_metadata": {"fixed_budget": 120}})
    )
    return path


def test_two_sequential_fresh_processes_and_exact_argv(tmp_path: Path) -> None:
    path = manifest(tmp_path)
    output = tmp_path / "phase-execution.json"
    result = runner.execute(path, output)
    assert result["status"] == "completed"
    assert result["phases"] == json.loads(output.read_bytes())["phases"]
    assert result["unstarted_phase_names"] == []
    expected = json.loads(path.read_bytes())["phases"]
    for observed, declared in zip(result["phases"], expected, strict=True):
        assert observed["argv"] == declared["argv"]
        assert observed["returncode"] == 0
        assert observed["started_at"] <= observed["ended_at"]
        assert observed["wall_seconds"] >= 0
    children = [json.loads((tmp_path / f"child-{i}.json").read_bytes()) for i in range(2)]
    assert children[0]["pid"] != children[1]["pid"]
    assert not result["scientific_result_interpreted"]


def test_failed_second_retains_first_success_and_returncode(tmp_path: Path) -> None:
    path = manifest(tmp_path, failure=7)
    result = runner.execute(path, tmp_path / "phase-execution.json")
    assert result["status"] == "failed"
    assert [p["returncode"] for p in result["phases"]] == [0, 7]


def test_failure_stops_without_alternative(tmp_path: Path) -> None:
    path = manifest(tmp_path)
    plan = json.loads(path.read_bytes())
    plan["phases"][0]["argv"][-1] = "8"
    path.write_text(json.dumps(plan))
    result = runner.execute(path, tmp_path / "phase-execution.json")
    assert len(result["phases"]) == 1
    assert result["unstarted_phase_names"] == ["phase-1"]
    assert not (tmp_path / "child-1.json").exists()


def test_existing_evidence_refuses_before_any_launch(tmp_path: Path) -> None:
    path = manifest(tmp_path)
    output = tmp_path / "phase-execution.json"
    output.write_bytes(b"preserved prior attempt")
    with pytest.raises(FileExistsError):
        runner.execute(path, output)
    assert output.read_bytes() == b"preserved prior attempt"
    assert not (tmp_path / "child-0.json").exists()


@pytest.mark.parametrize(
    "phases",
    [
        None,
        [],
        [{"name": "x", "argv": "shell command"}],
        [{"name": "x", "argv": []}],
        [{"name": "x", "argv": ["python", 1]}],
        [{"name": "x", "argv": [""]}],
        [{"name": "x", "argv": ["cmd"], "shell": True}],
        [{"name": "x", "argv": ["cmd"]}] * 65,
    ],
)
def test_bad_plan_refuses_without_output(phases: Any, tmp_path: Path) -> None:
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"phases": phases}))
    with pytest.raises(ValueError, match=r"phase|argv|name"):
        runner.execute(path, tmp_path / "phase-execution.json")
    assert not (tmp_path / "phase-execution.json").exists()


@pytest.mark.parametrize("number", ["NaN", "Infinity", "1e999999"])
def test_nonfinite_plan_refused(number: str, tmp_path: Path) -> None:
    path = manifest(tmp_path)
    text = path.read_text()[:-1] + f', "bad": {number}' + "}"
    path.write_text(text)
    with pytest.raises(ValueError, match="nonfinite"):
        runner.execute(path, tmp_path / "phase-execution.json")


def test_partial_receipt_written_before_launch_and_interrupt(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = manifest(tmp_path)
    output = tmp_path / "phase-execution.json"

    def interrupt(_argv: list[str], **_kwargs: Any) -> Any:
        retained = json.loads(output.read_bytes())
        assert retained["status"] == "running"
        assert retained["phases"][0]["status"] == "running"
        assert retained["phases"][0]["started_at"]
        raise KeyboardInterrupt

    monkeypatch.setattr(runner.subprocess, "run", interrupt)
    result = runner.execute(path, output)
    assert result["status"] == "interrupted"
    assert result["phases"][0]["returncode"] is None
    assert result["phases"][0]["wall_seconds"] >= 0
    assert result["unstarted_phase_names"] == ["phase-1"]


def test_launch_error_keeps_started_partial_evidence(tmp_path: Path) -> None:
    path = manifest(tmp_path)
    plan = json.loads(path.read_bytes())
    plan["phases"][0]["argv"][0] = str(tmp_path / "nonexistent")
    path.write_text(json.dumps(plan))
    result = runner.execute(path, tmp_path / "phase-execution.json")
    assert result["status"] == "failed"
    assert result["phases"][0]["status"] == "launch_failed"
    assert result["phases"][0]["returncode"] is None


def test_cli_fresh_process_and_no_overwrite(tmp_path: Path) -> None:
    path = manifest(tmp_path)
    output = tmp_path / "phase-execution.json"
    command = [
        sys.executable,
        "-m",
        "devtools.run_registered_phases",
        "--manifest",
        str(path),
        "--output",
        str(output),
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=10, check=False)
    assert result.returncode == 0, result.stderr
    preserved = output.read_bytes()
    second = subprocess.run(command, capture_output=True, text=True, timeout=10, check=False)
    assert second.returncode == 2
    assert output.read_bytes() == preserved
