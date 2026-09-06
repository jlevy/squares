"""The deep gate's properties, which are otherwise only a comment nobody re-reads.

`packing-validation.yml` keeps four steps off the pull-request surface on cost, and its
own header states the consequence: "a pull request can be green while a deferred test is
broken." On 2026-09-05 that happened twice.
`test_the_retained_n20_certificate_is_accepted_on_the_full_doubled_net` asserted a
certificate rung a later commit displaced; it is marked `exhaustive_exact`, so no pull
request ran it; run 34009814108 failed on the merge commit `6bd136b0` and `main` stayed
red across three merges until `c743d7bb`.

`.github/workflows/deep-gate.yml` runs that deferred surface against a pull request
before the merge, and `.github/workflows/branch-mergeability.yml` reports the branch that
cannot be merge-built at all (`D-459`). Every property below is one those two files would
lose silently rather than loudly:

- a deep gate that has stopped covering the whole deferred set still passes, and reports
  green on the merge that breaks `main` -- so the selection is resolved through the CLI's
  own `--list`, from the commands in the YAML, and compared against `STEPS`;
- a deep gate that has quietly started running on every push is a 32-minute tax nobody
  asked for, so the triggers are pinned;
- a second always-present required context is the `D-380` failure mode, so the shape that
  avoids it -- one aggregate, `!cancelled()`, label-gated jobs -- is pinned;
- and a conflict check moved onto a `pull_request` trigger would be silent in exactly the
  case it exists to name, because that is the defect: GitHub creates no run.

The selections are read from the workflow rather than from a flag for the reason
`test_the_pull_request_surface_defers_only_what_was_measured` gives: `Step.fast` says a
step is *meant* to be deferred, and only a workflow says one is *run*.
"""

from __future__ import annotations

import io
import json
import shlex
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

from sqpack.cli import validate
from sqpack.yamlio import safe_load

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = PROJECT_ROOT.parent
WORKFLOWS = REPOSITORY_ROOT / ".github" / "workflows"

DEEP_GATE = WORKFLOWS / "deep-gate.yml"
MERGEABILITY = WORKFLOWS / "branch-mergeability.yml"
VALIDATION = WORKFLOWS / "packing-validation.yml"

#: The pull-request label that opts a branch into the deep surface. It is a string in a
#: YAML condition and a string a reviewer types into the GitHub UI, and nothing else
#: connects the two, so every job condition is checked to contain this exact test.
LABEL_TEST = "contains(github.event.pull_request.labels.*.name, 'deep-gate')"

#: The one context the deep gate reports, as `packing-required` is the one context the
#: pull-request surface reports (`D-380`, and `BC-218`'s condition on any job split).
AGGREGATE_JOB = "deep-gate-required"


def _workflow(path: Path) -> dict[str, Any]:
    """One workflow, parsed.

    The `"on"` key is asserted as a string because YAML 1.1 -- which is what PyYAML
    speaks -- reads an unquoted `on:` as the boolean `True`. Every reader of these files
    in this repository looks up `"on"`, so the quoting in the file is load-bearing and
    this is where it is held.
    """
    document = safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(document, dict)
    assert "on" in document, f"{path.name} must quote its `on:` key for YAML 1.1 readers"
    return document


def _gate_commands(path: Path) -> dict[str, str]:
    """Every `packing-validate` invocation in the workflow, by the job that runs it."""
    commands: dict[str, str] = {}
    for job_name, job in _workflow(path)["jobs"].items():
        for step in job.get("steps") or []:
            command = str(step.get("run", ""))
            if "packing-validate" not in command:
                continue
            assert job_name not in commands, f"{job_name} runs the gate twice"
            commands[job_name] = command
    return commands


def _selected_steps(command: str) -> set[str]:
    """What the CLI itself says this command selects.

    Through `--list --format json` rather than a reimplementation of the selector: the
    guard has to move when the thing it guards moves, and a private copy of the selection
    rules would drift from them. Same argument as
    `test_the_pull_request_jobs_partition_the_surface`, one public interface further out.
    """
    tokens = shlex.split(command)
    arguments = tokens[tokens.index("packing-validate") + 1 :]
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        status = validate.main(["--list", "--format", "json", *arguments])
    assert status == 0, f"the CLI refused the workflow's own command: {command}"
    return {str(entry["name"]) for entry in json.loads(stdout.getvalue())}


def _uses(path: Path) -> set[str]:
    return {
        str(step["uses"])
        for job in _workflow(path)["jobs"].values()
        for step in job.get("steps") or []
        if step.get("uses")
    }


def _concurrency_prefix(group: str) -> str:
    """The literal head of a concurrency group, before its first expression.

    Concurrency groups are repository-wide strings. Two workflows whose groups share a
    literal prefix and an expression tail can render to the same string, and one of them
    carries `cancel-in-progress` -- which is how a thirty-second check would come to
    cancel a thirty-minute gate run.
    """
    return group.split("${{", 1)[0]


def test_the_deep_gate_runs_exactly_what_the_pull_request_surface_defers() -> None:
    """The deep gate is the complement of the pull-request surface, not a sample of it.

    This is the property the whole file exists for. A deep gate that covers three of the
    four deferrals looks identical to one that covers all four -- green -- and the one it
    does not cover is the one that takes `main` red. So the four names typed into
    `deep-gate.yml` are resolved through the CLI and compared against every step no pull
    request runs. A fifth deferral argued into
    `test_the_pull_request_surface_defers_only_what_was_measured` fails here until it is
    also argued into the deep gate.

    The two jobs are disjoint for the reason the post-merge jobs are: nothing is paid for
    twice. And the exhaustive tier is alone in its job because of `D-456` -- when it
    outgrew its budget the gate killed it with its output in an unflushed pipe, and three
    merges went red saying nothing about the sixty other steps. A deep gate that cannot
    say *which* deferral broke is most of the way back to the daily backstop.
    """
    selections = {
        job_name: _selected_steps(command)
        for job_name, command in _gate_commands(DEEP_GATE).items()
    }

    assert set(selections) == {"deferred-steps", "exhaustive-tier"}
    assert selections["exhaustive-tier"] == {"exhaustive exact behavioral tests"}
    assert not selections["deferred-steps"] & selections["exhaustive-tier"]

    covered: set[str] = set().union(*selections.values())
    assert covered == {step.name for step in validate.STEPS if not step.fast}


def test_the_deep_gate_does_not_run_on_every_build() -> None:
    """The advisory deep run starts only when a reviewer requests it.

    The selection above is 1943.05s in one step against a `--fast` band of 700s, so a
    deep gate on every push is the tax `test_the_pull_request_surface_defers_only_what_
    was_measured` refused four times over. What makes it conditional is a label tested in
    every job's `if`, not a filter on the trigger -- and that choice is what keeps the
    workflow from leaving a check pending, so it is pinned in the test below too.

    No `push` and no `schedule`: a push-triggered deep gate is the post-merge surface
    that already exists in `packing-validation.yml`, and a scheduled one is the daily
    backstop whose lateness is the reason this file was written.
    """
    triggers = _workflow(DEEP_GATE)["on"]

    assert set(triggers) == {"pull_request", "workflow_dispatch"}
    assert set(triggers["pull_request"]) == {"types"}
    # `synchronize` is not decoration. Without it the label attests to a commit that is
    # no longer the head, which is the same stale evidence the daily backstop provides.
    assert "labeled" in triggers["pull_request"]["types"]
    assert "synchronize" in triggers["pull_request"]["types"]

    for job_name, job in _workflow(DEEP_GATE)["jobs"].items():
        assert LABEL_TEST in str(job.get("if", "")), f"{job_name} runs without the label"


def test_an_unlabelled_opened_pull_request_reports_skipped_deep_jobs() -> None:
    """Opening a PR must create a run, but must not start expensive deep work.

    GitHub cannot report skipped jobs if the event never creates a workflow run.
    Pin both the opening event and the complete conditions: an accidental unconditional
    opening-event clause would preserve the trigger while starting the deep suite.
    """
    document = _workflow(DEEP_GATE)
    assert "opened" in document["on"]["pull_request"]["types"]
    requested = f"github.event_name == 'workflow_dispatch' || {LABEL_TEST}"
    for job_name, job in document["jobs"].items():
        condition = " ".join(str(job["if"]).split())
        expected = f"!cancelled() && ({requested})" if job_name == AGGREGATE_JOB else requested
        assert condition == expected, job_name


def test_the_deep_gate_reports_one_context_and_never_leaves_it_pending() -> None:
    """`D-380` twice over: no fan-out of required checks, and nothing stuck pending.

    `D-380` is a superseded run reporting the required check as a hard failure, twice in
    ten minutes, each time waking a session to diagnose a run that had already been
    replaced. `BC-218` made "the aggregate stays the single required context" the
    condition for allowing the pull-request surface to become two jobs; this workflow is
    also a job split, so it inherits the condition and reports one context.

    The pending half is the other risk a new workflow adds. A required check that never
    runs sits pending forever -- which is why `packing-validation.yml` refuses a path
    filter -- while a job skipped by its own `if` reports a conclusion. So the label is
    tested in the job conditions (above) rather than in the trigger's filters, and the
    aggregate is gated the same way as the jobs it waits on: on an unlabelled pull
    request all three skip together and none of them hangs.
    """
    jobs = _workflow(DEEP_GATE)["jobs"]
    aggregate = jobs[AGGREGATE_JOB]

    assert set(aggregate["needs"]) == set(jobs) - {AGGREGATE_JOB}
    assert [name for name, job in jobs.items() if job.get("needs")] == [AGGREGATE_JOB]
    # `!cancelled()` rather than `always()`: `cancel-in-progress` is on for pull requests,
    # so supersession is routine and must leave this unreported rather than failing hard.
    assert str(aggregate["if"]).lstrip().startswith("!cancelled()")
    assert "always()" not in str(aggregate["if"])


def test_the_deep_gate_is_not_cancelled_by_the_pull_request_gate() -> None:
    """A shared concurrency group would let an ordinary push kill a 32-minute deep run.

    `packing-validation.yml` cancels in progress on pull requests, deliberately: dropping
    a superseded pull-request run is what makes "push, then keep working" cheap. Groups
    are repository-wide strings, so a deep gate that reused that group would inherit that
    cancellation and the label would end up attesting to a run that never finished.
    """
    groups = {
        path.name: str(_workflow(path)["concurrency"]["group"])
        for path in (DEEP_GATE, MERGEABILITY, VALIDATION)
    }
    prefixes = [_concurrency_prefix(group) for group in groups.values()]

    assert len(set(prefixes)) == len(prefixes), groups


def test_the_conflict_check_runs_on_an_event_that_fires_for_an_unmergeable_branch() -> None:
    """`D-459`: the branch that produces no CI at all, and why `push` is the only placement.

    When a branch conflicts with its base, GitHub cannot build `refs/pull/N/merge`, so no
    `pull_request` workflow run is created -- not a failing one, none. The checks sit
    pending and the pull request looks like it is waiting rather than broken. Measured on
    2026-09-05: five pushes over twenty-five minutes produced no run and no check on
    PR 83 while every other branch ran normally.

    So a `pull_request`-triggered check cannot report this: it has the same blind spot as
    the runs it would be reporting on. A `push` event fires off the branch tip, which
    exists whatever the base is doing, and its check run is keyed to the head commit SHA
    so it still appears on the pull request. That is the placement, and this test is what
    stops it being "tidied" onto `pull_request` later.

    It also has to fail rather than warn. An absent check already reads as pending; a
    check that reports the conflict as a notice reproduces the defect one level up.
    """
    document = _workflow(MERGEABILITY)
    triggers = document["on"]

    assert "push" in triggers
    assert "pull_request" not in triggers
    assert "merge_group" not in triggers
    # No path filter: a conflict is a property of the branch, not of the files in it.
    assert set(triggers["push"]) == {"branches-ignore"}
    assert "main" in triggers["push"]["branches-ignore"]

    steps = [step for job in document["jobs"].values() for step in job["steps"]]
    commands = "\n".join(str(step.get("run", "")) for step in steps)
    # A missing `-e` lets a failed fetch fall through to a stale origin/main and can
    # turn an unknown answer into a false green. The workflow must fail closed before
    # asking merge-tree anything.
    assert "set -euo pipefail" in commands
    assert "git merge-tree --write-tree HEAD origin/main" in commands
    assert "exit 1" in commands

    for job in document["jobs"].values():
        assert not job.get("continue-on-error")
    for step in steps:
        assert not step.get("continue-on-error")


def test_the_new_workflows_pin_the_actions_the_gate_already_pins() -> None:
    """One SHA per action across the repository, or the pin is not a pin.

    Both new files check out and install with the same two actions `packing-validation.yml`
    uses. Pinning them to a *different* SHA would mean a bump had to be found in three
    places by memory, and the one that was missed would be the one running the deep
    surface. Subset rather than equality: the gate uses actions these two do not.
    """
    gate = _uses(VALIDATION)

    assert _uses(DEEP_GATE) <= gate, sorted(_uses(DEEP_GATE) - gate)
    assert _uses(MERGEABILITY) <= gate, sorted(_uses(MERGEABILITY) - gate)


def test_the_deep_gate_runs_the_locked_project_interpreter() -> None:
    """The same environment as the gate, because a deep run in a different one proves
    nothing about the merge it is clearing.

    `--all-extras` on every `uv` command is the same requirement
    `test_ci_jobs_fetch_provenance_history_and_key_the_uv_cache_from_the_lock` places on
    the gate's own jobs, and the Python version is read from `.python-version` rather
    than typed here so that a bump moves one file.
    """
    expected_python = (PROJECT_ROOT / ".python-version").read_text(encoding="utf-8").strip()

    for job_name, job in _workflow(DEEP_GATE)["jobs"].items():
        steps = job["steps"]
        commands = [str(step["run"]) for step in steps if isinstance(step.get("run"), str)]
        if not any("packing-validate" in command for command in commands):
            continue

        setup = next(
            step
            for step in steps
            if str(step.get("uses", "")).startswith("astral-sh/setup-uv@")
        )
        options = setup["with"]
        assert options["python-version"] == expected_python, job_name
        assert options["working-directory"] == "packing", job_name
        assert options["cache-dependency-glob"] == "uv.lock", job_name

        environment = [
            command for command in commands if command.startswith(("uv sync", "uv run"))
        ]
        assert environment, job_name
        assert all("--all-extras" in command for command in environment), job_name
