"""The pull-request wall budget, on recorded runs of the surface it is meant to bound.

`OR-14` names one number -- two to two and a half minutes, three at the outer edge -- and
until 2026-09-15 nothing measured it. Every tier stayed inside its own ceiling while the
required wall went from a 154 s median on 2026-09-06 to 288 s on 2026-09-15, because the
wall is the longest job with its queue, checkout and toolchain and no tier sees that.

So the fixtures here are four real runs of that spiral, recorded from the GitHub API with
`check_pr_wall --dump`:

* `34023121156`, 2026-09-06, the day the jobs split and the surface was in band;
* `34921505934`, 2026-09-15, the same workflow at 295 s;
* `34993754160`, the certificate page at 543 s, from before its `pr-wall` job existed;
* `34996541230`, a run superseded by the next push, which is the case a wall check must
  refuse to judge rather than pass.

The budgets a test needs to bind are fabricated in `tmp_path`, so a test never pins a
figure the live register is free to re-measure. The two things read from the live register
are its own shape and its own rules, which is what `check_gate_budgets` enforces.
"""

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

from devtools import check_pr_wall
from devtools.check_pr_wall import (
    WallError,
    WorkflowWall,
    judge,
    kind_of,
    load_walls,
    measure,
    render,
    summary_markdown,
)

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "pr-wall"
IN_BAND = 34023121156
OVER_BUDGET = 34921505934
PAGES = 34993754160
SUPERSEDED = 34996541230


def recorded(run_id: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    document = json.loads((FIXTURES / f"run-{run_id}.json").read_text(encoding="utf-8"))
    return document["run"], document["jobs"]


def register(
    tmp_path: Path,
    *,
    budget: float = 180.0,
    median: float | None = None,
    samples: int = 15,
    ratio: float = 1.2,
    minimum: int = 15,
) -> Path:
    """A whole wall register in `tmp_path`, so a test can declare what it needs to fail."""
    kinds = ""
    if median is not None:
        rows = "\n".join(
            f"      - {{run: {index + 1}, seconds: {median}}}" for index in range(samples)
        )
        kinds = f"""    kinds:
    - kind: main
      median_seconds: {median}
      measured_on: '2026-09-15'
      samples:
{rows}
"""
    path = tmp_path / "gate-budgets.yaml"
    path.write_text(
        "pull_request_walls:\n"
        "  policy:\n"
        f"    regression_ratio: {ratio}\n"
        f"    min_samples: {minimum}\n"
        "    main_branch: main\n"
        "    setup_steps: ['^(Set up job|Complete job)$', '^Post ', '^Check out ', "
        "'^Install ', '^Synchroni[sz]e ', '^Cache ', '^(Preserve|Retain|Upload) ', "
        "'^(Use|Share) the prepared ']\n"
        "  workflows:\n"
        "  - id: packing-validation\n"
        "    file: .github/workflows/packing-validation.yml\n"
        "    aggregator: packing-required\n"
        "    not_gating: [macos-portability]\n"
        f"    budget_seconds: {budget}\n"
        "    argument: a fabricated register\n" + kinds,
        encoding="utf-8",
    )
    return path


def verdict_of(
    path: Path, run_id: int, *, workflow: str = "packing-validation", kind: str | None = "main"
):
    walls = load_walls(path)
    entry = walls.workflow(workflow)
    run, jobs = recorded(run_id)
    measurement = measure(run, jobs, entry, walls.policy, kind=kind)
    return measurement, judge(measurement, entry, walls.policy)


def test_a_run_inside_the_budget_passes_and_names_no_failure(tmp_path: Path) -> None:
    """2026-09-06, the shape the split was measured at: four jobs, and in band."""
    measurement, verdict = verdict_of(register(tmp_path), IN_BAND)
    assert verdict.status == "passed"
    assert verdict.failures == ()
    assert measurement.wall_seconds is not None
    assert measurement.wall_seconds < 180.0
    assert {job.name for job in measurement.jobs} == {"validate", "geometry", "suite", "sweeps"}


def test_a_run_over_the_budget_fails_and_names_the_job_that_set_the_wall(
    tmp_path: Path,
) -> None:
    """The failure has to be actionable, which means naming the job and its split.

    "CI is slow" is not actionable; "`suite` finished last, setup 35s, work 250s" is, and
    it is the sentence that would have started the conversation on 2026-09-08 rather than
    on 2026-09-15.
    """
    measurement, verdict = verdict_of(register(tmp_path), OVER_BUDGET)
    assert verdict.status == "failed"
    assert measurement.critical_job == "suite"
    assert any("suite" in failure and "180s budget" in failure for failure in verdict.failures)
    assert any("work" in failure for failure in verdict.failures)


def test_a_run_inside_the_budget_still_fails_a_regression_against_the_record(
    tmp_path: Path,
) -> None:
    """The budget is `OR-14`'s edge; this is the rule around what was measured.

    The drift that was missed was about ten per cent a day for eight days, every day of it
    inside whatever the ceiling was. A ratio against the recorded median fails the second
    day of that, long before the absolute budget does.
    """
    path = register(tmp_path, budget=180.0, median=110.0)
    measurement, verdict = verdict_of(path, IN_BAND)
    assert measurement.wall_seconds is not None
    assert measurement.wall_seconds <= 180.0
    assert verdict.status == "failed"
    assert any("110s median" in failure for failure in verdict.failures)


def test_a_cancelled_run_is_not_judged_and_says_so(tmp_path: Path) -> None:
    """A superseded push is routine here, and its wall is not the surface's wall.

    Passing it silently would be worse than not checking: the run that replaced it is the
    one with something to say, and a check that reports green on a cancelled run teaches a
    reader that green means nothing.
    """
    _, verdict = verdict_of(register(tmp_path, median=110.0), SUPERSEDED)
    assert verdict.status == "unmeasurable"
    assert verdict.failures == ()
    assert any("cancelled" in note for note in verdict.unjudged)
    assert any(
        "neither the budget nor the regression rule" in note for note in verdict.unjudged
    )


def test_too_few_recorded_runs_leaves_the_regression_rule_unapplied(tmp_path: Path) -> None:
    """Runner speed here is bimodal, so a median over a handful of runs is not a median.

    About seventy per cent of `suite` jobs land on the slow class, so a small sample can
    put the record in the fast mode and fail every ordinary run afterwards. Below
    `min_samples` the rule reports that it did not run, which is the honest answer.
    """
    path = register(tmp_path, median=110.0, samples=3)
    _, verdict = verdict_of(path, IN_BAND)
    assert verdict.status == "passed"
    assert any("3 run(s)" in note and "not applied" in note for note in verdict.unjudged)


def test_a_kind_with_no_record_is_reported_rather_than_skipped(tmp_path: Path) -> None:
    _, verdict = verdict_of(register(tmp_path), IN_BAND, kind="stacked")
    assert any("`stacked`" in note for note in verdict.unjudged)
    _, unknown = verdict_of(register(tmp_path), IN_BAND, kind=None)
    assert any("base branch is unknown" in note for note in unknown.unjudged)


def test_the_wall_ends_where_the_aggregating_job_starts(tmp_path: Path) -> None:
    """A job cannot see its own completion, so this is where the measurement stops.

    The same rule applies afterwards, so a run measured live and the same run measured a
    day later agree. A run whose workflow had no aggregator yet -- every certificate-page
    run before 2026-09-15 -- ends at its last job instead and says which it used.
    """
    walls = load_walls(register(tmp_path))
    entry = walls.workflow("packing-validation")
    run, jobs = recorded(IN_BAND)
    aggregator = next(job for job in jobs if job["name"] == "packing-required")
    live = deepcopy(jobs)
    for job in live:
        if job["name"] == "packing-required":
            job["status"], job["conclusion"], job["completed_at"] = "in_progress", None, None
    measured_live = measure(run, live, entry, walls.policy, kind="main")
    measured_after = measure(run, jobs, entry, walls.policy, kind="main")
    assert measured_live.wall_seconds == measured_after.wall_seconds
    assert measured_after.ends_at == "the start of `packing-required`"
    assert aggregator["started_at"] > max(
        str(job["completed_at"]) for job in jobs if job["name"] != "packing-required"
    )


def test_a_prerequisite_still_running_is_unmeasurable(tmp_path: Path) -> None:
    """The API can lag the `needs` graph, and a wall taken then would be a wall of less."""
    walls = load_walls(register(tmp_path))
    entry = walls.workflow("packing-validation")
    run, jobs = recorded(IN_BAND)
    pending = deepcopy(jobs)
    for job in pending:
        if job["name"] == "suite":
            job["status"], job["conclusion"], job["completed_at"] = "in_progress", None, None
    verdict = judge(
        measure(run, pending, entry, walls.policy, kind="main"), entry, walls.policy
    )
    assert verdict.status == "unmeasurable"
    assert any("`suite` has not completed" in note for note in verdict.unjudged)


def test_the_macos_job_is_declared_aside_and_not_waited_on(tmp_path: Path) -> None:
    """`packing-required` does not wait on it, so it must not be part of the wall."""
    measurement, _ = verdict_of(register(tmp_path), OVER_BUDGET)
    assert "macos-portability" not in {job.name for job in measurement.jobs}
    _, jobs = recorded(OVER_BUDGET)
    assert "macos-portability" in {str(job["name"]) for job in jobs}


def test_every_job_of_the_run_is_measured_rather_than_a_list_of_names(tmp_path: Path) -> None:
    """The jobs come from the run, so a job added to the surface is waited on at once.

    The surface has been four jobs, then five; the certificate page's is being split as
    this lands. A hard-coded list would have to be edited by whoever changes the graph,
    which is exactly the step that was skipped every time the wall grew.
    """
    walls = load_walls(register(tmp_path))
    entry = walls.workflow("packing-validation")
    run, jobs = recorded(OVER_BUDGET)
    invented = [
        *deepcopy(jobs),
        {
            "name": "a job nobody told the register about",
            "status": "completed",
            "conclusion": "success",
            "created_at": run["run_started_at"],
            "started_at": run["run_started_at"],
            "completed_at": "2026-09-15T02:40:00Z",
            "steps": [],
        },
    ]
    measurement = measure(run, invented, entry, walls.policy, kind="main")
    assert measurement.critical_job == "a job nobody told the register about"
    still_running = deepcopy(invented)
    still_running[-1]["status"], still_running[-1]["completed_at"] = "in_progress", None
    waiting = judge(
        measure(run, still_running, entry, walls.policy, kind="main"), entry, walls.policy
    )
    assert waiting.status == "unmeasurable"
    assert any("nobody told the register about" in note for note in waiting.unjudged)


def test_a_matrix_job_is_measured_and_a_pages_run_reports_its_own_end(tmp_path: Path) -> None:
    """The certificate page's two `font-loading` jobs are one matrix, reported as two."""
    walls = load_walls(register(tmp_path))
    entry = WorkflowWall(
        id="certificate-page",
        file=".github/workflows/pages.yml",
        aggregator="pr-wall",
        not_gating=(),
        budget_seconds=180.0,
        kinds=(),
    )
    run, jobs = recorded(PAGES)
    measurement = measure(run, jobs, entry, walls.policy, kind="stacked")
    verdict = judge(measurement, entry, walls.policy)
    assert {job.name for job in measurement.jobs} == {
        "prepare",
        "build",
        "font-loading (webkit)",
        "font-loading (firefox)",
    }
    assert measurement.ends_at.endswith("(this run has no `pr-wall`)")
    assert verdict.status == "failed"


def test_each_job_is_split_into_queue_setup_and_work(tmp_path: Path) -> None:
    """`OR-14` asks for queue, setup and execution apart, and the split is where it went.

    Setup was 180 of 874 Linux job-seconds on a stack run of 2026-09-15 and no budget
    covered any of it, which is how checkout doubling from 8 s to 16 s went unremarked.
    """
    measurement, _ = verdict_of(register(tmp_path), OVER_BUDGET)
    suite = next(job for job in measurement.jobs if job.name == "suite")
    assert suite.wall_seconds is not None
    assert suite.queue_seconds is not None
    assert suite.setup_seconds > 0
    assert suite.work_seconds > suite.setup_seconds
    assert suite.setup_seconds + suite.work_seconds <= suite.wall_seconds + 1


def test_the_verdict_renders_the_table_and_the_step_summary(tmp_path: Path) -> None:
    measurement, verdict = verdict_of(register(tmp_path), OVER_BUDGET)
    lines = render(measurement, verdict)
    assert any("suite" in line for line in lines)
    assert lines[-1] == "  verdict: failed"
    summary = summary_markdown(measurement, verdict)
    assert "| Job | Queue | Setup | Work | Wall |" in summary
    assert "**Fail:**" in summary


def test_the_kind_of_a_pull_request_is_its_base() -> None:
    assert kind_of("main", "main") == "main"
    assert kind_of("claude/no-js-spike-tools", "main") == "stacked"
    assert kind_of(None, "main") is None


def test_a_median_that_disagrees_with_its_own_samples_is_refused(tmp_path: Path) -> None:
    """The figure is read from the runs it names, not typed beside them."""
    path = register(tmp_path, median=110.0)
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "median_seconds: 110.0", "median_seconds: 90.0"
        ),
        encoding="utf-8",
    )
    with pytest.raises(WallError, match="median"):
        load_walls(path)


def test_the_live_register_declares_a_wall_for_both_workflows() -> None:
    """Read from the register rather than asserted here, because both are measurements.

    What is pinned is that they exist, that each names a workflow file that exists, and
    that no budget is looser than `OR-14`'s outer edge -- the rule
    `devtools.check_gate_budgets` enforces and this repeats as a live check.
    """
    walls = load_walls(check_pr_wall.REGISTER)
    assert {workflow.id for workflow in walls.workflows} == {
        "packing-validation",
        "certificate-page",
    }
    repository = Path(__file__).resolve().parents[2]
    for workflow in walls.workflows:
        assert (repository / workflow.file).is_file()
        assert workflow.budget_seconds <= 180.0
        for record in workflow.kinds:
            assert len(record.samples) >= 1
            assert record.median_seconds > 0
