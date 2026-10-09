"""A job the hosted pool never served reads as infrastructure, and is re-run once.

On 2026-10-05 from about 19:17 UTC, GitHub cancelled 96 queued jobs after 15 to 35
minutes with "The job was not acquired by Runner of type hosted even after multiple
attempts". Run 37362926042 is the recorded case: seven of `packing-required`'s ten
prerequisites passed, `frontend`, `suite-a` and `suite-b` never acquired a runner, and
the aggregator failed with no test failed. Three things answer it, and each is held here:

* both aggregators name the class (`FAILURE CLASS: infrastructure`) after their verdict
  step fails, without changing the verdict;
* `pages-required` no longer queues against a superseded run (`!cancelled()`, as
  `packing-required` has had since D-380);
* `rerun-starved.yml` re-runs the failed jobs once, when `devtools.rerun_starved` finds
  every condition for it.

The recorded run and jobs are the wall checker's fixture, which keeps `runner_name`.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any

import pytest

from devtools import rerun_starved
from devtools.rerun_starved import EVENTS, WORKFLOWS, decide, newer_runs
from sqpack.yamlio import safe_load

REPO = Path(__file__).resolve().parents[2]
WORKFLOWS_DIR = REPO / ".github" / "workflows"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "pr-wall" / "run-37362926042.json"
STARVED_JOBS = ("frontend", "suite-a", "suite-b")
#: The other runs of the workflow on that branch, as the API reported them: the duplicate
#: `pull_request` run GitHub created a second earlier and cancelled at once, the previous
#: push, and the 20:05 push that superseded it.
DUPLICATE = {
    "id": 37362925550,
    "name": "Packing validation",
    "path": ".github/workflows/packing-validation.yml",
    "event": "pull_request",
    "status": "completed",
    "conclusion": "cancelled",
    "run_attempt": 1,
    "created_at": "2026-10-05T19:22:21Z",
    "head_branch": "claude/n17-enhanced-row-support",
    "head_sha": "b13ffe7674cf314bed9b380a8abe14fc3c8880e5",
}
PREVIOUS = {
    **DUPLICATE,
    "id": 37305130479,
    "conclusion": "failure",
    "created_at": "2026-10-05T11:46:46Z",
    "head_sha": "c3cc143ae",
}
NEXT_PUSH = {
    **DUPLICATE,
    "id": 37367573008,
    "created_at": "2026-10-05T20:05:29Z",
    "head_sha": "b00eed752e35165107c5cb4659b08f6231e4fc91",
}
INFRASTRUCTURE_STEP = "Name every prerequisite that never acquired a runner"
AGGREGATORS = (
    ("packing-validation.yml", "packing-required", "Require every pull-request prerequisite"),
    ("pages.yml", "pages-required", "Require every page this run builds to pass"),
)


def recorded() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    document = json.loads(FIXTURE.read_text(encoding="utf-8"))
    return document["run"], document["jobs"]


def failing(decision: rerun_starved.Decision) -> list[str]:
    return [condition.rule for condition in decision.conditions if not condition.holds]


def workflow(name: str) -> dict[str, Any]:
    return safe_load((WORKFLOWS_DIR / name).read_text(encoding="utf-8"))


def test_the_recorded_starved_run_is_re_run_once() -> None:
    """Run 37362926042 when its first attempt completed at 19:48: every condition held."""
    run, jobs = recorded()
    decision = decide(run, jobs, [DUPLICATE, PREVIOUS, run])
    assert decision.rerun
    assert decision.starved == STARVED_JOBS
    assert failing(decision) == []
    lines = rerun_starved.render(decision)
    assert lines[0] == "run 37362926042: re-run its failed jobs once"
    assert all(line.startswith("  holds: ") for line in lines[1:])
    summary = rerun_starved.summary_markdown(decision)
    assert summary.startswith("### Starved run 37362926042: re-running the failed jobs once\n")
    assert (
        "| a job was cancelled without ever acquiring a runner | yes | `frontend`, " in summary
    )


def _served(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """The same jobs, as if a runner had taken each starved one before it was cancelled."""
    return [
        {**job, "runner_name": "GitHub Actions 1000106700"}
        if job["name"] in STARVED_JOBS
        else job
        for job in jobs
    ]


@pytest.mark.parametrize(
    ("change", "rule"),
    [
        ({"name": "Deep gate"}, "the run belongs to a workflow this listener re-runs"),
        ({"event": "workflow_dispatch"}, "the run was triggered by a pull request or a push"),
        ({"event": "schedule"}, "the run was triggered by a pull request or a push"),
        ({"conclusion": "success"}, "the run completed and failed"),
        ({"conclusion": "cancelled"}, "the run completed and failed"),
        ({"status": "in_progress", "conclusion": None}, "the run completed and failed"),
        ({"run_attempt": 2}, "this is the run's first attempt"),
    ],
)
def test_each_run_condition_alone_prevents_the_re_run(
    change: dict[str, Any], rule: str
) -> None:
    run, jobs = recorded()
    decision = decide({**run, **change}, jobs, [DUPLICATE])
    assert not decision.rerun
    assert failing(decision) == [rule]


def test_a_cancelled_job_that_had_a_runner_is_not_starved() -> None:
    """A job cancelled after it started ran on a runner; that is not the pool's refusal."""
    run, jobs = recorded()
    decision = decide(run, _served(jobs), [DUPLICATE])
    assert not decision.rerun
    assert decision.starved == ()
    assert failing(decision) == ["a job was cancelled without ever acquiring a runner"]
    # The API reports a never-acquired job's runner as `""` or as null; both are no runner.
    assert rerun_starved.never_acquired_a_runner({"conclusion": "cancelled", "runner_name": ""})
    assert rerun_starved.never_acquired_a_runner(
        {"conclusion": "cancelled", "runner_name": None}
    )
    assert not rerun_starved.never_acquired_a_runner(
        {"conclusion": "skipped", "runner_name": None}
    )


@pytest.mark.parametrize(
    "newer",
    [
        # GitHub created a second `pull_request` run for one head twice on 2026-10-05.
        {**DUPLICATE, "id": 37362926099, "created_at": "2026-10-05T19:22:24Z"},
        # The same second, a larger id: the tie is broken by creation order.
        {**DUPLICATE, "id": 37362926099, "created_at": "2026-10-05T19:22:22Z"},
        # The next push to the pull request: a re-run would cancel it in the group.
        NEXT_PUSH,
    ],
)
def test_a_newer_run_for_the_commit_or_the_branch_prevents_the_re_run(
    newer: dict[str, Any],
) -> None:
    run, jobs = recorded()
    decision = decide(run, jobs, [DUPLICATE, newer])
    assert not decision.rerun
    assert failing(decision) == [
        "no newer run of this workflow exists for this commit or this branch"
    ]
    assert newer_runs(run, [newer]) == (newer["id"],)


@pytest.mark.parametrize(
    "unrelated",
    [
        {**NEXT_PUSH, "path": ".github/workflows/pages.yml", "name": "Certificate page"},
        {**NEXT_PUSH, "head_branch": "claude/another-branch"},
        {**NEXT_PUSH, "event": "push"},
        {**DUPLICATE, "id": 37362925000, "created_at": "2026-10-05T19:22:22Z"},
    ],
)
def test_runs_of_another_workflow_branch_event_or_age_do_not_count(
    unrelated: dict[str, Any],
) -> None:
    run, jobs = recorded()
    assert newer_runs(run, [unrelated]) == ()
    assert decide(run, jobs, [unrelated]).rerun


def test_the_command_writes_its_output_and_summary_and_refuses_bad_input(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    run, jobs = recorded()
    (tmp_path / "run.json").write_text(json.dumps(run), encoding="utf-8")
    (tmp_path / "jobs.jsonl").write_text(
        "".join(json.dumps(job) + "\n" for job in jobs), encoding="utf-8"
    )
    (tmp_path / "runs.jsonl").write_text(
        f"{json.dumps(DUPLICATE)}\n\n{json.dumps(NEXT_PUSH)}\n", encoding="utf-8"
    )
    output, summary = tmp_path / "output", tmp_path / "summary.md"
    monkeypatch.setenv("GITHUB_OUTPUT", str(output))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(summary))
    arguments = [
        "--run",
        str(tmp_path / "run.json"),
        "--jobs",
        str(tmp_path / "jobs.jsonl"),
        "--runs",
        str(tmp_path / "runs.jsonl"),
    ]
    assert rerun_starved.main(arguments) == 0
    assert output.read_text(encoding="utf-8") == "rerun=false\n"
    assert summary.read_text(encoding="utf-8").startswith(
        "### Starved run 37362926042: not re-running\n"
    )
    printed = capsys.readouterr().out.splitlines()
    assert printed[0] == "run 37362926042: no re-run"
    assert any(
        line.startswith("  FAILS: no newer run") and "37367573008" in line for line in printed
    )

    (tmp_path / "runs.jsonl").write_text(json.dumps(DUPLICATE) + "\n", encoding="utf-8")
    output.unlink()
    assert rerun_starved.main(arguments) == 0
    assert output.read_text(encoding="utf-8") == "rerun=true\n"

    (tmp_path / "jobs.jsonl").write_text("[1, 2]\n", encoding="utf-8")
    assert rerun_starved.main(arguments) == 2
    (tmp_path / "run.json").write_text(
        json.dumps({**run, "run_attempt": "1"}), encoding="utf-8"
    )
    (tmp_path / "jobs.jsonl").write_text("", encoding="utf-8")
    assert rerun_starved.main(arguments) == 2
    assert "run_attempt" in capsys.readouterr().err


def test_the_listener_is_subscribed_to_the_gating_workflows_and_nothing_wider() -> None:
    """Names, permissions, pins and the payload filter of `rerun-starved.yml`."""
    listener = workflow("rerun-starved.yml")
    trigger = listener["on"]
    assert set(trigger) == {"workflow_run"}
    assert trigger["workflow_run"]["types"] == ["completed"]
    assert tuple(trigger["workflow_run"]["workflows"]) == WORKFLOWS
    assert {workflow(name)["name"] for name in ("packing-validation.yml", "pages.yml")} == set(
        WORKFLOWS
    )
    assert listener["permissions"] == {"actions": "write", "contents": "read"}
    (name, job), *others = listener["jobs"].items()
    assert name == "rerun-starved"
    assert others == []
    assert "permissions" not in job
    condition = " ".join(job["if"].split())
    assert "github.event.workflow_run.conclusion == 'failure'" in condition
    assert "github.event.workflow_run.run_attempt == 1" in condition
    for event in EVENTS:
        assert f"github.event.workflow_run.event == '{event}'" in condition
    steps = job["steps"]
    for step in steps:
        if "uses" in step:
            assert re.fullmatch(r"[\w.-]+/[\w.-]+@[0-9a-f]{40}", step["uses"]), step["uses"]
        # Every value from the payload reaches the shell through `env`.
        assert "${{" not in step.get("run", ""), step["name"]
    checkout = next(
        step for step in steps if step.get("uses", "").startswith("actions/checkout@")
    )
    assert "ref" not in checkout["with"]
    assert checkout["with"]["persist-credentials"] is False
    assert checkout["with"]["sparse-checkout"].split() == ["packing/devtools/rerun_starved.py"]
    decision = next(step for step in steps if step.get("id") == "decide")
    assert decision["run"].startswith(
        "uv run --no-project --python 3.14.7 python packing/devtools/rerun_starved.py "
    )
    rerun = steps[-1]
    assert rerun["if"] == "steps.decide.outputs.rerun == 'true'"
    assert rerun["run"] == 'gh run rerun "$RUN_ID" --failed --repo "$GITHUB_REPOSITORY"'
    assert sum("gh run rerun" in step.get("run", "") for step in steps) == 1


def _infrastructure_steps() -> list[dict[str, Any]]:
    found = []
    for file, aggregator, verdict in AGGREGATORS:
        steps = workflow(file)["jobs"][aggregator]["steps"]
        names = [step.get("name") for step in steps]
        # Right after the verdict, so it can only follow it and never replace it.
        assert names.index(INFRASTRUCTURE_STEP) == names.index(verdict) + 1, file
        found.append(steps[names.index(INFRASTRUCTURE_STEP)])
    return found


def test_both_aggregators_name_a_starved_prerequisite_after_their_verdict() -> None:
    """The same step in both, after the verdict, only on its failure, never deciding."""
    packing, pages = _infrastructure_steps()
    assert packing == pages
    assert packing["if"] == "failure()"
    assert packing["env"] == {"NEEDS": "${{ toJSON(needs) }}"}
    assert "continue-on-error" not in packing
    assert workflow("packing-validation.yml")["jobs"]["packing-required"]["if"] == (
        "!cancelled() && github.event_name == 'pull_request'"
    )
    # A dispatch that asks only for the font diagnostic qualifies nothing, so it skips
    # the aggregate too (`test_pages_workflow`'s font-diagnostic tests).
    assert workflow("pages.yml")["jobs"]["pages-required"]["if"] == (
        "!cancelled() && !inputs.font_diagnostic"
    )


@pytest.mark.skipif(shutil.which("jq") is None, reason="the aggregator's jq is not installed")
@pytest.mark.parametrize(
    ("results", "expected"),
    [
        (
            dict.fromkeys(STARVED_JOBS, "cancelled"),
            [
                *(
                    f"::error title=Infrastructure::{name} never acquired a runner "
                    "(cancelled before start)"
                    for name in STARVED_JOBS
                ),
                (
                    "FAILURE CLASS: infrastructure (3 of 10 prerequisites never acquired "
                    "a runner: frontend, suite-a, suite-b)"
                ),
            ],
        ),
        ({"suite-a": "failure"}, []),
        ({}, []),
    ],
)
def test_the_infrastructure_step_names_each_starved_prerequisite_and_the_class(
    tmp_path: Path, results: dict[str, str], expected: list[str]
) -> None:
    """Run 37362926042's `needs`, through the step's own script under the runner's bash."""
    step = _infrastructure_steps()[0]
    needs = {
        name: {"result": results.get(name, "success"), "outputs": {}}
        for name in workflow("packing-validation.yml")["jobs"]["packing-required"]["needs"]
    }
    summary = tmp_path / "summary.md"
    summary.write_text("", encoding="utf-8")
    bash = shutil.which("bash")
    assert bash is not None
    completed = subprocess.run(
        (bash, "--noprofile", "--norc", "-eo", "pipefail", "-c", step["run"]),
        env={
            "NEEDS": json.dumps(needs),
            "RUNNER_TEMP": str(tmp_path),
            "GITHUB_STEP_SUMMARY": str(summary),
            "PATH": str(Path(shutil.which("jq") or "jq").parent) + ":/usr/bin:/bin",
        },
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.splitlines() == expected
    assert summary.read_text(encoding="utf-8").splitlines() == expected[-1:]
