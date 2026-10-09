"""Synthetic fresh-process phase execution and preserved failure evidence."""

from __future__ import annotations

import hashlib
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


@pytest.mark.parametrize("number", ["0", "1e999999"])
def test_deep_opaque_metadata_is_validated_without_recursive_walk(
    number: str, tmp_path: Path
) -> None:
    path = tmp_path / "deep.json"
    path.write_text(
        '{"phases":[{"name":"synthetic","argv":["unused"]}],"metadata":'
        + "[" * 1200
        + number
        + "]" * 1200
        + "}"
    )
    if number == "0":
        raw, phases = runner.load_plan(path)
        assert raw == path.read_bytes()
        assert phases == [{"name": "synthetic", "argv": ["unused"]}]
    else:
        with pytest.raises(ValueError, match="nonfinite"):
            runner.load_plan(path)


def test_deep_wrong_plan_retains_normal_cli_refusal(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path, output = tmp_path / "deep.json", tmp_path / "unused.json"
    path.write_text('{"metadata":' + "[" * 1200 + "0" + "]" * 1200 + "}")
    assert runner.main(["--manifest", str(path), "--output", str(output)]) == 2
    assert json.loads(capsys.readouterr().err)["status"] == "refused"
    assert not output.exists()


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


def reconciliation_inputs(tmp_path: Path, *, complete: bool = False) -> tuple[Path, Path, Path]:
    """A completed prefix with one unresolved phase, rather than fictional exits."""
    path = manifest(tmp_path)
    plan = json.loads(path.read_bytes())
    plan["phases"] = [{"name": f"phase-{i}", "argv": ["unused", str(i)]} for i in range(8)]
    path.write_text(json.dumps(plan))
    phases = []
    for index in range(8 if complete else 7):
        done = complete or index < 6
        phases.append(
            {
                **plan["phases"][index],
                "status": "completed" if done else "running",
                "started_at": "2026-10-08T01:00:00Z",
                "returncode": 0 if done else None,
                "wall_seconds": 1.0 if done else None,
                **({"ended_at": "2026-10-08T01:00:01Z"} if done else {}),
            }
        )
    journal = tmp_path / "journal.json"
    journal.write_text(
        json.dumps(
            {
                "schema": runner.SCHEMA,
                "status": "completed" if complete else "running",
                "manifest": str(path),
                "manifest_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "phases": phases,
                "unstarted_phase_names": [] if complete else ["phase-7"],
                "scientific_result_interpreted": False,
            }
        )
    )
    supervision = tmp_path / "supervision.json"
    supervision.write_text(
        json.dumps(
            {
                "schema": "posix-bounded-command-supervision/v1",
                "status": "COMPLETED" if complete else "INCOMPLETE",
                "returncode": 0 if complete else -15,
                "pid": 123,
                "owned_pgid": 123,
                "cleanup_complete": True,
                "argv": [
                    sys.executable,
                    "-m",
                    "devtools.run_registered_phases",
                    "--manifest",
                    str(path),
                    "--output",
                    str(journal),
                ],
            }
        )
    )
    return path, journal, supervision


def test_reconcile_stale_tail_preserves_six_exits_and_unknown_seventh(tmp_path: Path) -> None:
    paths = reconciliation_inputs(tmp_path)
    before = [path.read_bytes() for path in paths]
    result = runner.reconcile(*paths, tmp_path / "derived.json", tmp_path)
    assert result["status"] == "incomplete"
    assert result["original_journal_status"] == "running"
    assert [p["returncode"] for p in result["phases"]] == [0] * 6 + [None]
    assert result["phases"][-1]["status"] == "interrupted_by_supervisor"
    assert result["phases"][-1]["wall_seconds"] is None
    assert result["unstarted_phase_names"] == ["phase-7"]
    assert not result["missing_child_returncodes_inferred"]
    assert not result["scientific_result_interpreted"]
    assert [path.read_bytes() for path in paths] == before
    assert json.loads((tmp_path / "derived.json").read_bytes()) == result


def test_reconcile_completed_preserves_exact_phase_metadata(tmp_path: Path) -> None:
    paths = reconciliation_inputs(tmp_path, complete=True)
    original = json.loads(paths[1].read_bytes())
    result = runner.reconcile(*paths, tmp_path / "derived.json", tmp_path)
    assert result["status"] == "completed"
    assert result["phases"] == original["phases"]
    assert result["unstarted_phase_names"] == []


@pytest.mark.parametrize(
    "tamper",
    [
        "sha",
        "order",
        "argv",
        "unstarted",
        "nonfinal_running",
        "boolean_exit",
        "cleanup",
        "foreign_command",
        "foreign_path",
        "live_supervisor",
        "foreign_group",
    ],
)
def test_reconcile_refuses_unjoined_or_unterminated_evidence(
    tmp_path: Path, tamper: str
) -> None:
    paths = reconciliation_inputs(tmp_path)
    journal = json.loads(paths[1].read_bytes())
    supervisor = json.loads(paths[2].read_bytes())
    if tamper == "sha":
        journal["manifest_sha256"] = "0" * 64
    elif tamper == "order":
        journal["phases"][0], journal["phases"][1] = journal["phases"][1], journal["phases"][0]
    elif tamper == "argv":
        journal["phases"][0]["argv"] = ["different"]
    elif tamper == "unstarted":
        journal["unstarted_phase_names"] = []
    elif tamper == "nonfinal_running":
        journal["phases"][0].update(status="running", returncode=None, wall_seconds=None)
    elif tamper == "boolean_exit":
        journal["phases"][0]["returncode"] = False
    elif tamper == "cleanup":
        supervisor["cleanup_complete"] = False
    elif tamper == "foreign_command":
        supervisor["argv"][2] = "devtools.different"
    elif tamper == "foreign_path":
        supervisor["argv"][-1] = str(tmp_path / "other.json")
    elif tamper == "live_supervisor":
        supervisor["status"] = "running"
    else:
        supervisor["owned_pgid"] = 124
    paths[1].write_text(json.dumps(journal))
    paths[2].write_text(json.dumps(supervisor))
    output = tmp_path / "derived.json"
    with pytest.raises(ValueError, match=r"differs|required|tail|prefix|supervisor"):
        runner.reconcile(*paths, output, tmp_path)
    assert not output.exists()


def test_reconcile_supervisor_interruption_overrides_complete_journal(tmp_path: Path) -> None:
    paths = reconciliation_inputs(tmp_path, complete=True)
    guard = json.loads(paths[2].read_bytes())
    guard.update(status="INCOMPLETE", returncode=-15)
    paths[2].write_text(json.dumps(guard))
    assert (
        runner.reconcile(*paths, tmp_path / "derived.json", tmp_path)["status"] == "incomplete"
    )


def test_reconcile_refuses_successful_supervisor_with_stale_journal(tmp_path: Path) -> None:
    paths = reconciliation_inputs(tmp_path)
    guard = json.loads(paths[2].read_bytes())
    guard.update(status="COMPLETED", returncode=0)
    paths[2].write_text(json.dumps(guard))
    with pytest.raises(ValueError, match="conflicts"):
        runner.reconcile(*paths, tmp_path / "derived.json", tmp_path)


def test_reconcile_existing_output_and_input_alias_preserve_evidence(tmp_path: Path) -> None:
    paths = reconciliation_inputs(tmp_path)
    before = paths[1].read_bytes()
    with pytest.raises(ValueError, match="aliases"):
        runner.reconcile(*paths, paths[1], tmp_path)
    output = tmp_path / "derived.json"
    output.write_bytes(b"prior unique report")
    with pytest.raises(FileExistsError):
        runner.reconcile(*paths, output, tmp_path)
    assert output.read_bytes() == b"prior unique report"
    assert paths[1].read_bytes() == before


def test_reconcile_input_mutation_refuses_before_report(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    paths = reconciliation_inputs(tmp_path)
    original = runner.check_journal

    def mutate(*args: Any) -> Any:
        result = original(*args)
        paths[2].write_bytes(paths[2].read_bytes() + b"\n")
        return result

    monkeypatch.setattr(runner, "check_journal", mutate)
    with pytest.raises(ValueError, match="bytes changed"):
        runner.reconcile(*paths, tmp_path / "derived.json", tmp_path)


def test_reconcile_cli_is_report_only_and_requires_paired_flags(tmp_path: Path) -> None:
    paths = reconciliation_inputs(tmp_path)
    command = [
        sys.executable,
        "-m",
        "devtools.run_registered_phases",
        "--manifest",
        str(paths[0]),
        "--journal",
        str(paths[1]),
        "--supervision",
        str(paths[2]),
        "--execution-root",
        str(tmp_path),
        "--output",
        str(tmp_path / "derived.json"),
    ]
    result = subprocess.run(command, capture_output=True, timeout=10, check=False)
    assert result.returncode == 1, result.stderr
    assert json.loads((tmp_path / "derived.json").read_bytes())["status"] == "incomplete"
    # The manifest's executable is intentionally nonexistent: reporting never runs it.
    assert not (tmp_path / "child-0.json").exists()
    command[command.index("--supervision") : command.index("--supervision") + 2] = []
    unpaired = subprocess.run(command, capture_output=True, timeout=10, check=False)
    assert unpaired.returncode == 2
