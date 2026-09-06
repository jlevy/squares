"""Guard the exploratory report against accepting invalid or incomparable evidence."""

import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from benchmarks.validation_report import (
    DEFAULT_ROOT,
    completed_runs,
    render,
    screen,
    validate_evidence,
)

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
