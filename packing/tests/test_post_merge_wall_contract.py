"""Post-merge walls are declared, exact and read without changing the verdict."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest

from devtools.check_ci_gate_walls import GateWallError, measure, verdicts
from devtools.check_pr_wall import load_walls
from sqpack.gate_budgets import BUDGETS, ci_declaration_problems, load
from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parents[1]
REPOSITORY = PACKING.parent
WORKFLOW = REPOSITORY / ".github" / "workflows" / "packing-validation.yml"
AGGREGATE = "post-merge-required"
GATE = "post-merge"
RESULT_ENVIRONMENTS = {
    "validate": "VALIDATE_RESULT",
    "deferred-threshold-1440": "THRESHOLD_1440_RESULT",
    "deferred-atlas-grid": "ATLAS_GRID_RESULT",
    "deferred-controls-finer": "CONTROLS_FINER_RESULT",
    "deferred-threshold-720-rigidity": "THRESHOLD_720_RIGIDITY_RESULT",
    "slow-lane": "SLOW_RESULT",
    "exhaustive-1": "EXHAUSTIVE_1_RESULT",
    "exhaustive-2": "EXHAUSTIVE_2_RESULT",
    "exhaustive-3": "EXHAUSTIVE_3_RESULT",
    "screen": "SCREEN_RESULT",
    "regularized-views": "REGULARIZED_VIEWS_RESULT",
}
WORKERS = set(RESULT_ENVIRONMENTS)


def _workflow() -> dict[str, Any]:
    document = safe_load(WORKFLOW.read_text(encoding="utf-8"))
    assert isinstance(document, dict)
    assert "on" in document, "packing-validation.yml must quote its `on:` key"
    return document


def test_post_merge_workers_and_wall_register_are_the_same_exact_set() -> None:
    workflow = _workflow()
    aggregate = workflow["jobs"][AGGREGATE]
    register = load(BUDGETS)
    gate = register.ci_gate(GATE)

    assert gate is not None
    assert gate.file == str(WORKFLOW.relative_to(REPOSITORY))
    assert gate.aggregate == AGGREGATE
    assert set(aggregate["needs"]) == WORKERS
    assert set(gate.ids) == WORKERS
    assert gate.reports_only
    assert gate.tracking_bead == "think-0atx"
    assert ci_declaration_problems(register) == []

    for budget in (*gate.jobs, gate.wall):
        assert budget.measured_seconds is None, budget.id
        assert budget.measured_on is None, budget.id
        assert budget.measured_where is None, budget.id
        assert budget.spread is None, budget.id
        assert budget.pending_measurement == "think-0atx", budget.id
        assert budget.ceiling_seconds > 0, budget.id
        assert re.search(r"derived|estimate|proxy", budget.argument, re.IGNORECASE), budget.id


def test_post_merge_aggregate_reports_walls_without_weakening_its_verdict() -> None:
    aggregate = _workflow()["jobs"][AGGREGATE]
    steps = list(aggregate["steps"])
    verdict = steps[0]
    reporting = [
        step for step in steps if "devtools.check_ci_gate_walls" in str(step.get("run", ""))
    ]

    assert str(aggregate["if"]).endswith("github.event_name != 'pull_request'")
    assert aggregate["permissions"] == {"contents": "read", "actions": "read"}
    for worker, result_name in RESULT_ENVIRONMENTS.items():
        assert f"needs.{worker}.result" in str(verdict["env"][result_name])
    assert len(reporting) == 1
    (report,) = reporting
    command = " ".join(str(report["run"]).split())
    assert "--gate post-merge" in command
    assert "--enforce" not in command
    checkouts = [step for step in steps[1:] if "actions/checkout@" in str(step.get("uses", ""))]
    assert len(checkouts) == 1
    assert checkouts[0]["with"]["ref"] == "${{ github.sha }}"
    assert checkouts[0]["with"]["submodules"] is True
    for step in steps[1:]:
        assert step.get("if") == "always()", step.get("name")
        assert step.get("continue-on-error") is True, step.get("name")


def _job(
    name: str,
    completed_at: str,
    *,
    started_at: str = "2026-09-29T20:00:10+00:00",
) -> dict[str, object]:
    return {
        "name": name,
        "status": "completed",
        "conclusion": "success",
        "created_at": "2026-09-29T20:00:00+00:00",
        "started_at": started_at,
        "completed_at": completed_at,
        "labels": ["ubuntu-latest"],
        "steps": [],
    }


def test_post_merge_wall_ignores_a_later_unrelated_workflow_job() -> None:
    gate = load(BUDGETS).ci_gate(GATE)
    assert gate is not None
    jobs = [_job(name, "2026-09-29T20:02:00+00:00") for name in gate.ids]
    jobs[0] = _job(gate.ids[0], "2026-09-29T20:03:00+00:00")
    jobs[-1] = _job(
        gate.ids[-1],
        "2026-09-29T20:03:10+00:00",
        started_at="2026-09-29T20:02:50+00:00",
    )
    jobs.extend(
        (
            _job("macos-portability", "2026-09-29T20:10:00+00:00"),
            _job(AGGREGATE, "2026-09-29T20:11:00+00:00"),
        )
    )
    run = {
        "id": 7,
        "head_sha": "a" * 40,
        "conclusion": "success",
        "run_started_at": "2026-09-29T20:00:00+00:00",
    }

    measured = measure(run, jobs, gate, load_walls().policy)

    assert measured.wall_seconds == 190
    assert measured.critical_job == gate.ids[-1]
    assert {job.name for job in measured.jobs} == {*gate.ids, AGGREGATE}


@pytest.mark.parametrize("damage", ["missing", "duplicate"])
def test_post_merge_wall_refuses_an_incomplete_or_duplicate_declared_inventory(
    damage: str,
) -> None:
    gate = load(BUDGETS).ci_gate(GATE)
    assert gate is not None
    jobs = [_job(name, "2026-09-29T20:02:00+00:00") for name in gate.ids]
    if damage == "missing":
        jobs.pop()
    else:
        jobs.append(dict(jobs[0]))
    run = {
        "id": 8,
        "head_sha": "b" * 40,
        "conclusion": "success",
        "run_started_at": "2026-09-29T20:00:00+00:00",
    }

    with pytest.raises(GateWallError, match=damage):
        measure(run, jobs, gate, load_walls().policy)


def test_post_merge_wall_reports_unknown_until_every_declared_worker_finishes() -> None:
    register = load(BUDGETS)
    gate = register.ci_gate(GATE)
    assert gate is not None
    jobs = [_job(name, "2026-09-29T20:02:00+00:00") for name in gate.ids]
    jobs[-1]["status"] = "in_progress"
    jobs[-1]["completed_at"] = None
    run = {
        "id": 9,
        "head_sha": "c" * 40,
        "conclusion": None,
        "run_started_at": "2026-09-29T20:00:00+00:00",
    }

    measured = measure(run, jobs, gate, load_walls().policy)
    found = verdicts(register, gate, measured)

    assert measured.wall_seconds is None
    assert measured.critical_job is None
    wall = next(verdict for verdict in found if verdict.tier == "wall")
    assert wall.status == "unknown"
    assert "not measured" in wall.notes[0]
