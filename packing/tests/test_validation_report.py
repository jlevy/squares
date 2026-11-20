"""Guard the exploratory report against accepting invalid or incomparable evidence."""

import json
import os
import re
import shutil
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import pytest

from benchmarks import validation_report
from benchmarks.validation_report import (
    DEFAULT_ROOT,
    completed_runs,
    render,
    screen,
    validate_evidence,
)


def _phase_write_receipt(directory: Path, result: dict[str, Any]) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    end_only = {
        "status",
        "returncode",
        "wall_seconds",
        "allocated_worker_seconds",
        "error",
        "phase_journals",
    }
    start = {key: value for key, value in result.items() if key not in end_only}
    (directory / "receipts.jsonl").write_text(
        json.dumps({**start, "event": "start"})
        + "\n"
        + json.dumps({**result, "event": "end"})
        + "\n"
    )


@pytest.fixture
def phase_evidence(tmp_path: Path) -> Path:
    """Complete synthetic v2 records; their original source/interpreter do not exist."""
    root = tmp_path / "evidence"
    root.mkdir()
    protocol = {
        "protocol": "phase-overhead-v2",
        "order": list(validation_report.PHASE_ORDER),
        "output_root": str(root),
        "null_config": os.devnull,
        "source": {
            "root": "/historical/packing",
            "commit": "a" * 40,
            "interpreter": "/historical/python",
            "python": "3.14.7",
            "git_status": "",
            "platform": "historical platform",
            "available_cpus": 2,
        },
    }
    (root / "protocol.json").write_text(json.dumps(protocol))
    (root / "completion.json").write_text(json.dumps({"complete": True}))
    (root / "fixture").mkdir()
    (root / "fixture/test_phase_timing_work.py").write_text(validation_report.PHASE_FIXTURE)
    outer_events = []
    for index, arm in enumerate(validation_report.PHASE_ORDER):
        identifier, outer_id = f"{index + 1:032x}", f"{index + 100:032x}"
        directory = root / f"observations/{index}-{arm}/runs"
        stem = directory / identifier
        command = validation_report.phase_command(protocol, index, arm)
        targets = command[command.index("--") + 1 :]
        pytest_command = [
            "/historical/python",
            "-m",
            "pytest",
            "-q",
            *targets,
            "--durations=0",
            "--durations-min=0",
            f"--junitxml={stem}.junit.xml",
            "-n",
            "2",
        ]
        environment: dict[str, str] = dict.fromkeys(
            (
                "OPENBLAS_NUM_THREADS",
                "OMP_NUM_THREADS",
                "MKL_NUM_THREADS",
                "VECLIB_MAXIMUM_THREADS",
                "NUMEXPR_NUM_THREADS",
                "BLIS_NUM_THREADS",
                "PACK_JOBS",
                "UV_NO_SYNC",
            ),
            "1",
        )
        environment["PYTHONPATH"] = os.pathsep.join(
            ("/historical/packing/src", "/historical/packing")
        )
        run = {
            "run_id": identifier,
            "label": arm,
            "repeat": 1,
            "root": "/historical/packing",
            "commit": "a" * 40,
            "git_status": "",
            "timeout_seconds": 30,
            "pytest_workers": 2,
            "inner_workers": 1,
            "native_threads": 1,
            "allocated_workers": 2,
            "interpreter": "/historical/python",
            "environment": environment,
            "python": "3.14.7",
            "platform": "historical platform",
            "available_cpus": 2,
            "pytest_configuration": {
                "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
                "PYTHONUNBUFFERED": "1",
                "PYTHONPYCACHEPREFIX": str(root / "python-cache"),
            },
            "stdout_path": f"{stem}.stdout.log",
            "stderr_path": f"{stem}.stderr.log",
            "junit_path": f"{stem}.junit.xml",
            "status": "passed",
            "returncode": 0,
            "wall_seconds": 1.0,
            "allocated_worker_seconds": 2.0,
            "error": "",
        }
        if arm == "on":
            pytest_command += [
                "-p",
                "devtools.reachable_progress",
                "--reachable-phase-timings=pytest-report-duration-v1",
            ]
            run["phase_timings"] = {
                "capability": "pytest-report-duration-v1",
                "stem": str(stem),
            }
            run["phase_journals"] = [f"{stem}.progress-gw{worker}.jsonl" for worker in range(2)]
        run["command"] = pytest_command
        _phase_write_receipt(directory, run)
        Path(run["stdout_path"]).write_text("raw output")
        Path(run["stderr_path"]).write_text("")
        suite = ET.Element("testsuite", tests="1000", failures="0", errors="0", skipped="0")
        for number in range(1000):
            ET.SubElement(
                suite,
                "testcase",
                classname="test_phase_timing_work",
                name=f"test_case[case::{number:04d}]",
                time="0.003",
            )
        ET.ElementTree(suite).write(run["junit_path"], encoding="unicode")
        if arm == "on":
            for worker in range(2):
                identity = {
                    "schema": "reachable-progress-v1",
                    "run_id": identifier,
                    "command_id": identifier,
                    "source_commit": "a" * 40,
                    "worker_id": f"gw{worker}",
                    "xdist_workers": 2,
                    "pack_jobs": "1",
                    "lane": "validation-timing",
                    "marker": "",
                    "exclusions": "explicit timing selection",
                }
                rows = [
                    {
                        **identity,
                        "event": "session_start",
                        "nodeid": "",
                        "phase_timing_capability": "pytest-report-duration-v1",
                        "phase_plugin_path": (
                            "/historical/packing/devtools/reachable_progress.py"
                        ),
                    }
                ]
                for number in range(worker, 1000, 2):
                    node = f"test_phase_timing_work.py::test_case[case::{number:04d}]"
                    rows.append({**identity, "event": "start", "nodeid": node})
                    rows.extend(
                        {
                            **identity,
                            "event": "phase_finish",
                            "nodeid": node,
                            "phase": phase,
                            "outcome": "passed",
                            "duration_seconds": 0.001,
                        }
                        for phase in ("setup", "call", "teardown")
                    )
                    rows.append(
                        {**identity, "event": "finish", "nodeid": node, "outcome": "passed"}
                    )
                rows.append(
                    {**identity, "event": "session_finish", "nodeid": "", "exit_status": 0}
                )
                Path(run["phase_journals"][worker]).write_text(
                    "".join(json.dumps(row) + "\n" for row in rows)
                )
        outer_stem = root / "outer" / outer_id
        wall = 10.1 if arm == "on" else 10.0
        result = {
            "run_id": outer_id,
            "label": arm,
            "observation": index,
            "command": command,
            "root": "/historical/packing",
            "allocated_workers": 2,
            "timeout_seconds": 45,
            "stdout_path": f"{outer_stem}.stdout.log",
            "stderr_path": f"{outer_stem}.stderr.log",
            "status": "passed",
            "returncode": 0,
            "wall_seconds": wall,
            "allocated_worker_seconds": wall * 2,
            "error": "",
        }
        _phase_write_receipt(root / "outer", result)
        outer_events.extend((root / "outer/receipts.jsonl").read_text().splitlines())
        Path(result["stdout_path"]).write_text("recorded CLI output")
        Path(result["stderr_path"]).write_text("")
    (root / "outer/receipts.jsonl").write_text("\n".join(outer_events) + "\n")
    return root


def test_phase_overhead_accepts_complete_equal_work_with_bounded_cost(
    phase_evidence: Path,
) -> None:
    result = validation_report.phase_overhead(phase_evidence)
    assert result["accepted"]
    assert result["median_ratio"] == pytest.approx(1.01)
    assert result["phase_rows"] == [0, 3000, 3000, 0, 0, 3000]


def _set_first_phase_case_time(root: Path, arm: str, value: str | None) -> None:
    observation = "0-off" if arm == "off" else "1-on"
    directory = root / f"observations/{observation}/runs"
    junit = next(directory.glob("*.junit.xml"))
    tree = ET.parse(junit)
    case = tree.findall(".//testcase")[0]
    if value is None:
        case.attrib.pop("time")
    else:
        case.set("time", value)
    tree.write(junit, encoding="unicode")
    if arm == "on":
        journal = next(directory.glob("*.progress-gw0.jsonl"))
        rows = [json.loads(line) for line in journal.read_text().splitlines()]
        measured = [
            row
            for row in rows
            if row["event"] == "phase_finish"
            and row["nodeid"] == f"test_phase_timing_work.py::{case.get('name')}"
        ]
        assert len(measured) == 3
        for row in measured:
            row["duration_seconds"] = 0.0
        journal.write_text("".join(json.dumps(row) + "\n" for row in rows))


@pytest.mark.parametrize(
    ("arm", "value"),
    [("off", "NaN"), ("off", "-0.0001"), ("off", None), ("on", "-0.0001")],
)
def test_phase_reader_requires_finite_nonnegative_junit_time_in_both_arms(
    phase_evidence: Path, arm: str, value: str | None
) -> None:
    # The on-arm phases sum to zero, so -0.0001 would fit the rounding tolerance.
    _set_first_phase_case_time(phase_evidence, arm, value)
    with pytest.raises(ValueError, match="JUnit testcase time"):
        validation_report.phase_overhead(phase_evidence)


@pytest.mark.parametrize("arm", ["off", "on"])
def test_phase_reader_accepts_completed_zero_time(phase_evidence: Path, arm: str) -> None:
    _set_first_phase_case_time(phase_evidence, arm, "0")
    assert validation_report.phase_overhead(phase_evidence)["accepted"]


@pytest.mark.parametrize(
    "mutation",
    [
        "missing",
        "duplicate",
        "nan",
        "negative",
        "worker",
        "node",
        "junit",
        "junit_identity",
        "duration_none",
        "duration_bool",
        "phase_none",
        "phase_number",
    ],
)
def test_phase_census_and_same_run_totals_refuse_bad_evidence(
    phase_evidence: Path, mutation: str
) -> None:
    journal = next((phase_evidence / "observations/1-on/runs").glob("*.progress-gw0.jsonl"))
    rows = [json.loads(line) for line in journal.read_text().splitlines()]
    if mutation == "missing":
        rows.pop(2)
    elif mutation == "duplicate":
        rows.insert(3, dict(rows[2]))
    elif mutation in {"nan", "negative"}:
        rows[2]["duration_seconds"] = float("nan") if mutation == "nan" else -1
    elif mutation in {"duration_none", "duration_bool"}:
        rows[2]["duration_seconds"] = None if mutation == "duration_none" else True
    elif mutation in {"phase_none", "phase_number"}:
        rows[2]["phase"] = None if mutation == "phase_none" else 1
    elif mutation == "worker":
        rows[2]["worker_id"] = "gw1"
    elif mutation == "node":
        rows[2]["nodeid"] = "test_phase_timing_work.py::test_case[substituted]"
    elif mutation == "junit":
        junit = next(journal.parent.glob("*.junit.xml"))
        junit.write_text(junit.read_text().replace('time="0.003"', 'time="1.003"', 1))
    else:
        junit = next(journal.parent.glob("*.junit.xml"))
        junit.write_text(
            junit.read_text().replace(
                'name="test_case[case::0000]"', 'name="test_case[substituted]"', 1
            )
        )
    journal.write_text("".join(json.dumps(row) + "\n" for row in rows))
    errors = {
        "missing": "node finish precedes its completed phases",
        "duplicate": "invalid or duplicate quantitative phase",
        "nan": "invalid or duplicate quantitative phase",
        "negative": "invalid or duplicate quantitative phase",
        "duration_none": "invalid or duplicate quantitative phase",
        "duration_bool": "invalid or duplicate quantitative phase",
        "phase_none": "invalid or duplicate quantitative phase",
        "phase_number": "invalid or duplicate quantitative phase",
        "worker": "worker journal identity differs",
        "node": "node report belongs to another worker",
        "junit": "same-run JUnit and phase totals differ",
        "junit_identity": "selected JUnit identities differ",
    }
    with pytest.raises(ValueError, match=rf"^{re.escape(errors[mutation])}$"):
        validation_report.phase_overhead(phase_evidence)


@pytest.mark.parametrize(
    "mutation",
    ["junit_uuid", "command", "incomplete", "configuration", "completion", "outer_incomplete"],
)
def test_phase_record_bindings_refuse_substituted_runs(
    phase_evidence: Path, mutation: str
) -> None:
    receipt = phase_evidence / "observations/1-on/runs/receipts.jsonl"
    events = [json.loads(line) for line in receipt.read_text().splitlines()]
    if mutation == "incomplete":
        events.pop()
    elif mutation == "outer_incomplete":
        path = phase_evidence / "outer/receipts.jsonl"
        path.write_text("\n".join(path.read_text().splitlines()[:-1]) + "\n")
    elif mutation == "completion":
        (phase_evidence / "completion.json").write_text('{"complete": false}')
    else:
        for event in events:
            if mutation == "junit_uuid":
                event["junit_path"] = event["junit_path"].replace(
                    "00000000000000000000000000000002", "00000000000000000000000000000003"
                )
            elif mutation == "command":
                event["command"][event["command"].index("-n") + 1] = "1"
            else:
                event["pytest_configuration"]["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = ""
    receipt.write_text("".join(json.dumps(event) + "\n" for event in events))
    errors = {
        "junit_uuid": "inner artifact is not bound to its UUID",
        "command": "inner selection or execution regime differs",
        "incomplete": "observation needs exactly one successful inner receipt",
        "configuration": "pytest configuration differs",
        "completion": "comparison has no completed capture",
        "outer_incomplete": "whole-CLI observation contradicts the declared command",
    }
    with pytest.raises(ValueError, match=rf"^{re.escape(errors[mutation])}$"):
        validation_report.phase_overhead(phase_evidence)


def test_phase_reader_refuses_a_symlinked_observation_subtree(phase_evidence: Path) -> None:
    directory = phase_evidence / "observations/1-on/runs"
    retained = directory.with_name("retained-runs")
    directory.rename(retained)
    directory.symlink_to(retained, target_is_directory=True)
    with pytest.raises(ValueError, match=r"subtree|symlink"):
        validation_report.phase_overhead(phase_evidence)


def test_phase_reader_keeps_a_failed_cap_and_all_samples(phase_evidence: Path) -> None:
    path = phase_evidence / "outer/receipts.jsonl"
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    for row in rows:
        if row["event"] == "end" and row["label"] == "on":
            row["wall_seconds"], row["allocated_worker_seconds"] = 14.0, 28.0
    path.write_text("".join(json.dumps(row) + "\n" for row in rows))
    result = validation_report.phase_overhead(phase_evidence)
    assert not result["accepted"]
    assert result["wall_seconds"] == [[10.0] * 3, [14.0] * 3]


def test_compatible_current_reader_and_moved_data_replay_without_old_source(
    phase_evidence: Path, tmp_path: Path
) -> None:
    moved = tmp_path / "moved"
    shutil.copytree(phase_evidence, moved)
    reader = tmp_path / "maintained_reader.py"
    reader.write_text(
        Path(validation_report.__file__).read_text() + "\n# Compatible reader maintenance.\n"
    )
    packing = Path(validation_report.__file__).parents[1]
    result = subprocess.run(
        [sys.executable, str(reader), "phase-overhead", "--root", str(moved)],
        env={**os.environ, "PYTHONPATH": os.pathsep.join((str(packing / "src"), str(packing)))},
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["accepted"]


EXPERIMENT = {
    "control_label": "control",
    "candidate_label": "candidate",
    "target": "tests/test_target.py",
    "minimum_samples": 3,
    "minimum_improvement": 0.15,
    "maximum_allocation_ratio": 1.25,
}


def observations() -> list[dict[str, Any]]:
    return [
        {
            "run_id": f"{label}-{index}",
            "label": label,
            "status": "passed",
            "wall_seconds": wall,
            "allocated_worker_seconds": wall,
            "allocated_workers": 1,
            "inner_workers": 1,
            "pytest_workers": 0,
            "native_threads": 1,
            "platform": "host",
            "python": "3.14",
            "interpreter": "/python",
            "available_cpus": 4,
            "commit": "base",
            "dirty_diff_sha256": label,
            "source_hashes": {"target": label},
            "root": label,
            "environment": {},
            "timeout_seconds": 60,
            "command": ["/python", "-m", "pytest", "tests/test_target.py"],
            "test_cases": [("test_target", "test_contract")],
        }
        for label, walls in (("control", (10, 11, 12)), ("candidate", (5, 6, 7)))
        for index, wall in enumerate(walls)
    ]


def test_clean_comparison_passes_only_the_arithmetic_screen() -> None:
    assert screen(EXPERIMENT, observations())[2] == (
        "Screen passes (45.5% median reduction); correctness and complexity review required"
    )


@pytest.mark.parametrize("status", ["failed", "timeout", "interrupted", "incomplete"])
def test_unsuccessful_observation_is_not_dropped(status: str) -> None:
    runs = observations()
    runs.append({"label": "candidate", "status": status})
    assert "no acceptance" in screen(EXPERIMENT, runs)[2]


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("test_cases", [("test_target", "different_test")]),
        ("command", ["pytest", "tests/other.py"]),
        ("source_hashes", {"target": "changed-mid-arm"}),
        ("inner_workers", 2),
        ("environment", {"OMP_NUM_THREADS": "8"}),
        ("platform", "other-host"),
    ],
)
def test_selection_and_regime_drift_prevent_comparison(field: str, value: Any) -> None:
    runs = observations()
    runs[-1][field] = value
    assert "Incomparable" in screen(EXPERIMENT, runs)[2]


def test_overlap_and_allocation_guard_are_independent() -> None:
    runs = observations()
    runs[-1]["wall_seconds"] = 10
    assert "ranges overlap" in screen(EXPERIMENT, runs)[2]
    runs = observations()
    for run in runs[3:]:
        run["allocated_worker_seconds"] *= 3
        run["allocated_workers"] = 3
    assert "allocated-work guard" in screen(EXPERIMENT, runs)[2]


def test_incomplete_receipt_survives_and_contradictory_end_is_rejected() -> None:
    start = {**observations()[0], "event": "start"}
    start.pop("status")
    assert completed_runs([start])[0]["status"] == "incomplete"
    end = {**start, "event": "end", "status": "passed", "returncode": 0}
    assert completed_runs([start, end])[0]["status"] == "passed"
    for change in ({"command": []}, {"returncode": 1}, {"allocated_workers": 2}):
        with pytest.raises(ValueError, match=r"receipt changed|nonzero pass"):
            completed_runs([start, {**end, **change}])
    with pytest.raises(ValueError, match="duplicate start"):
        completed_runs([start, start])
    with pytest.raises(ValueError, match="duplicate end"):
        completed_runs([start, end, end])


@pytest.mark.parametrize(
    "xml",
    [
        '<testsuite tests="0"/>',
        "<testsuite><testcase><failure/></testcase></testsuite>",
        "<testsuite><testcase><error/></testcase></testsuite>",
        "<testsuite><testcase><skipped/></testcase></testsuite>",
        '<testsuite failures="1"><testcase/></testsuite>',
        '<testsuite tests="0"><testcase/></testsuite>',
    ],
)
def test_passing_receipt_cannot_mask_unsuccessful_junit(tmp_path: Path, xml: str) -> None:
    (tmp_path / "runs").mkdir()
    (tmp_path / "runs/result.xml").write_text(xml)
    run = {**observations()[0], "junit_path": "/original/result.xml"}
    with pytest.raises(ValueError, match="JUnit"):
        validate_evidence(tmp_path, [run])


def test_junit_guard_requires_file_and_retains_case_identities(tmp_path: Path) -> None:
    run = {**observations()[0], "junit_path": "result.xml"}
    with pytest.raises(ValueError, match="no JUnit"):
        validate_evidence(tmp_path, [run])
    (tmp_path / "runs").mkdir()
    (tmp_path / "runs/result.xml").write_text(
        '<testsuites><testsuite tests="1" failures="0" errors="0" skipped="0">'
        '<testcase classname="test_target" name="test_contract"/>'
        "</testsuite></testsuites>"
    )
    validated = deepcopy(run)
    validate_evidence(tmp_path, [validated])
    assert validated["test_cases"] == [("test_target", "test_contract")]


def test_missing_samples_and_zero_denominator_cannot_pass() -> None:
    assert screen(EXPERIMENT, observations()[:-1])[2] == "Pending samples"
    runs = observations()
    for run in runs[:3]:
        run["wall_seconds"] = 0
        run["allocated_worker_seconds"] = 0
    assert "no acceptance" in screen(EXPERIMENT, runs)[2]


def test_end_cannot_understate_declared_worker_allocation() -> None:
    start = {"event": "start", "run_id": "one", "allocated_workers": 2}
    end = {
        **start,
        "event": "end",
        "status": "passed",
        "returncode": 0,
        "wall_seconds": 10,
        "allocated_worker_seconds": 10,
    }
    with pytest.raises(ValueError, match="contradictory worker allocation"):
        completed_runs([start, end])


def test_render_rejects_an_experiment_without_yaml_frontmatter(tmp_path: Path) -> None:
    shutil.copy(DEFAULT_ROOT / "experiment.schema.yaml", tmp_path / "experiment.schema.yaml")
    (tmp_path / "experiments").mkdir()
    (tmp_path / "experiments" / "bad-experiment.md").write_text(
        "# No Frontmatter\n\nThis file has no YAML frontmatter.\n"
    )
    (tmp_path / "runs").mkdir()
    with pytest.raises(ValueError, match=r"lacks YAML frontmatter.*bad-experiment\.md"):
        render(tmp_path)


def test_retained_report_matches_the_actual_experiment_corpus() -> None:
    assert render(DEFAULT_ROOT) == (DEFAULT_ROOT / "report.md").read_text()


def test_whole_tree_diff_variation_requires_explicit_affected_source_audit() -> None:
    runs = observations()
    runs[-1]["dirty_diff_sha256"] = "unrelated-docs-edit"
    verdict = screen(EXPERIMENT, runs)[2]
    assert verdict.startswith("Screen passes")
    assert "correctness and complexity review required" in verdict
    assert "affected-source audit required" in verdict
    assert "whole-tree equivalence is not established" in verdict
    runs[-1]["source_hashes"] = {"target": "changed-target"}
    assert "Incomparable" in screen(EXPERIMENT, runs)[2]
