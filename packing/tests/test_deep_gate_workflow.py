"""The deep gate's properties, which are otherwise only a comment nobody re-reads.

`packing-validation.yml` defers expensive steps from the pull-request surface, and its
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
  avoids it -- one aggregate, `!cancelled()`, label-gated jobs -- is pinned, and so is the
  script inside that aggregate, because a prerequisite whose result it never tests is an
  advisory check wearing a required one's name;
- and a conflict check moved onto a `pull_request` trigger would be silent in exactly the
  case it exists to name, because that is the defect: GitHub creates no run.

The selections are read from the workflow rather than from a flag for the reason
`test_the_pull_request_surface_defers_only_what_was_measured` gives: `Step.fast` says a
step is *meant* to be deferred, and only a workflow says one is *run*.
"""

from __future__ import annotations

import io
import json
import re
import shlex
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any

from sqpack.cli import validate
from sqpack.gate_budgets import BUDGETS, ci_declaration_problems, load
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

    This is the property the whole file exists for. A deep gate that covers all but one
    of the deferrals looks identical to one that covers every one -- green -- and the one
    it does not cover is the one that takes `main` red. So the names typed into
    `deep-gate.yml` are resolved through the CLI and compared against every step no pull
    request runs. The next deferral argued into
    `test_the_pull_request_surface_defers_only_what_was_measured` fails here until it is
    also argued into the deep gate, which is how the set reached seven on 2026-09-07
    without anyone maintaining a count.

    The jobs are disjoint for the reason the post-merge jobs are: nothing is paid for
    twice. Three steps have their own jobs. The exhaustive tier is
    `D-456` -- when it outgrew its budget the gate killed it with its output in an
    unflushed pipe, and three merges went red saying nothing about the sixty other steps.
    A deep gate that cannot say *which* deferral broke is most of the way back to the
    daily backstop. The escape screen is `D-484`, and its reason is workers rather than
    verdicts: it is a process pool sized by `PACK_JOBS`, so beside the other five
    deferrals it gets two of the runner's four. Run 34177317419 killed it here at the
    shared 900s cap on commit `831697c0`, an hour after post-merge run 34176106076 had
    finished the same step at 858.62s on the same commit.

    Disjointness is asserted pairwise over whatever jobs exist rather than over a named
    pair. The slow lane's separate runner is included in the same partition. A new job
    still fails this test loudly
    the day it arrives -- the job-set assertion below fires first and has to be taught the
    new name -- and once it has been, the pairwise loop covers it without further edits.
    """
    selections = {
        job_name: _selected_steps(command)
        for job_name, command in _gate_commands(DEEP_GATE).items()
    }

    assert set(selections) == {
        "deferred-threshold-1440",
        "deferred-atlas-grid",
        "deferred-controls-finer",
        "deferred-threshold-720-rigidity",
        "deferred-slow-lane",
        "exhaustive-1",
        "exhaustive-2",
        "exhaustive-3",
        "screen",
        "regularized-views",
    }
    assert selections["deferred-slow-lane"] == {"slow behavioral tests"}
    exhaustive_jobs = {f"exhaustive-{index}" for index in range(1, 4)}
    for job in exhaustive_jobs:
        assert selections[job] == {"exhaustive exact behavioral tests"}
    assert selections["screen"] == {"single-square translation escape screen"}
    assert selections["regularized-views"] == {"regularized atlas views re-derive exactly"}
    ownership: dict[str, set[str]] = {}
    for job, selected in selections.items():
        for step in selected:
            ownership.setdefault(step, set()).add(job)
    assert ownership["exhaustive exact behavioral tests"] == exhaustive_jobs
    assert all(
        len(jobs) == 1
        for step, jobs in ownership.items()
        if step != "exhaustive exact behavioral tests"
    )

    commands = _gate_commands(DEEP_GATE)
    for index in range(1, 4):
        job = f"exhaustive-{index}"
        tokens = shlex.split(commands[job])
        shard_positions = [
            position for position, token in enumerate(tokens) if token == "--exhaustive-shard"
        ]
        assert len(shard_positions) == 1, job
        assert tokens[shard_positions[0] + 1] == f"{index}/3", job

    covered = set(ownership)
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
    request all four skip together and none of them hangs.
    """
    jobs = _workflow(DEEP_GATE)["jobs"]
    aggregate = jobs[AGGREGATE_JOB]

    assert set(aggregate["needs"]) == set(jobs) - {AGGREGATE_JOB}
    for name, job in jobs.items():
        if name == "resolve-tree":
            assert not job.get("needs")
        elif name == AGGREGATE_JOB:
            assert set(job["needs"]) == set(jobs) - {AGGREGATE_JOB}
        else:
            assert job.get("needs") == "resolve-tree", name
    # `!cancelled()` rather than `always()`: `cancel-in-progress` is on for pull requests,
    # so supersession is routine and must leave this unreported rather than failing hard.
    assert str(aggregate["if"]).lstrip().startswith("!cancelled()")
    assert "always()" not in str(aggregate["if"])


def test_every_deep_worker_and_receipt_are_bound_to_one_immutable_tree() -> None:
    """A moving dispatch ref is resolved once and never re-read by a worker."""
    jobs = _workflow(DEEP_GATE)["jobs"]
    resolver = jobs["resolve-tree"]
    assert resolver["outputs"] == {"sha": "${{ steps.tree.outputs.sha }}"}
    resolver_checkout = next(
        step
        for step in resolver["steps"]
        if str(step.get("uses", "")).startswith("actions/checkout@")
    )
    resolver_ref = str(resolver_checkout["with"]["ref"])
    assert "github.sha" in resolver_ref
    assert "refs/pull/{0}/merge" in resolver_ref

    for job_name, job in jobs.items():
        if job_name == "resolve-tree":
            continue
        checkouts = [
            step
            for step in job["steps"]
            if str(step.get("uses", "")).startswith("actions/checkout@")
        ]
        assert checkouts
        assert all(
            checkout["with"]["ref"] == "${{ needs.resolve-tree.outputs.sha }}"
            for checkout in checkouts
        ), job_name
        if job_name == AGGREGATE_JOB:
            continue
        receipts = [
            step
            for step in job["steps"]
            if step.get("name") == "Bind the receipt to the immutable tree"
        ]
        assert len(receipts) == 1, job_name
        receipt = receipts[0]
        assert receipt["env"] == {"VALIDATED_SHA": "${{ needs.resolve-tree.outputs.sha }}"}
        command = str(receipt["run"])
        assert 'test "$(git rev-parse HEAD)" = "$VALIDATED_SHA"' in command
        assert '"$PACKING_VALIDATION_ARTIFACT_DIR/tree-sha.txt"' in command
        validate_indexes = [
            index
            for index, step in enumerate(job["steps"])
            if "packing-validate" in str(step.get("run", ""))
        ]
        assert len(validate_indexes) == 1, job_name
        assert job["steps"].index(receipt) < validate_indexes[0], job_name


def test_every_deep_worker_publishes_one_uniquely_named_receipt() -> None:
    jobs = _workflow(DEEP_GATE)["jobs"]
    expected_name = "validation-timings-${{ github.job }}-${{ github.run_attempt }}"

    for job_name, job in jobs.items():
        if job_name in {"resolve-tree", AGGREGATE_JOB}:
            continue
        uploads = [
            step
            for step in job["steps"]
            if str(step.get("uses", "")).startswith("actions/upload-artifact@")
        ]
        assert len(uploads) == 1, job_name
        assert uploads[0]["if"] == "always()", job_name
        assert uploads[0]["with"]["name"] == expected_name, job_name
        assert uploads[0]["with"]["path"] == ("${{ env.PACKING_VALIDATION_ARTIFACT_DIR }}"), (
            job_name
        )


def test_every_deep_gate_prerequisite_decides_the_aggregate_verdict() -> None:
    """`needs` does not make a deep job's failure fatal here; the script does (`D-380`).

    The aggregate runs under `!cancelled()`, which is the `D-380` fix -- a superseded run
    must report nothing rather than a hard failure. What that buys is also what it costs:
    the job is *reached* when a prerequisite has failed, so the `run:` script is what
    decides the verdict, one `test` per result. A fourth deep job added with only `needs`
    updated would satisfy every other assertion in this file and still be advisory --
    green aggregate, red job, nothing on the pull request to say so. That is the `D-380`
    shape one level along: a check that reports the wrong thing quietly.

    So the pairing is derived rather than transcribed. Every job the aggregate needs must
    have its `result` bound to an environment variable, and every one of those variables
    must be tested for `success` in the script.
    `test_ci_jobs_fetch_provenance_history_and_key_the_uv_cache_from_the_lock` in
    `test_module_boundaries.py` holds the same property for `packing-required`, by pinning
    that job's exact command; this one is read from `needs`, so it also covers the deep
    job that does not exist yet.
    """
    aggregate = _workflow(DEEP_GATE)["jobs"][AGGREGATE_JOB]
    steps = [step for step in aggregate["steps"] if isinstance(step.get("run"), str)]
    assert steps, f"{AGGREGATE_JOB} must decide the verdict in a script"

    script = " ".join(" ".join(str(step["run"]).split()) for step in steps)
    environment: dict[str, str] = {
        str(name): str(value)
        for step in steps
        for name, value in (step.get("env") or {}).items()
    }

    for job_name in aggregate["needs"]:
        result = "${{ needs." + str(job_name) + ".result }}"
        bound = sorted(name for name, value in environment.items() if value == result)
        assert bound, f"{job_name} is a prerequisite whose result the aggregate never reads"
        for name in bound:
            assert f'test "${name}" = "success"' in script, (
                f"{job_name} is needed but its result is never tested: it would be "
                f"advisory, failing while {AGGREGATE_JOB} reports success"
            )


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


def test_every_deep_gate_job_is_clocked_against_a_declared_wall() -> None:
    """`OR-17`: a hosted job with no ceiling is a job that can double unremarked.

    Not hypothetical here, and the numbers are the ones this file already carries.
    `deep-gate.yml` prices the exhaustive tier at 1943.05s of step time, and the job that
    runs it cost 2674s on two complete runs on 2026-09-21 -- 1.38x, under the 1.5x that
    fails a local tier, and read by no rule at all, because `gate-budgets.yaml` clocked
    `packing-validate`'s own wall and nothing clocked a workflow job's.

    So the tiers' own rule, asked of every worker: every job the gate runs has an
    entry and a concrete ceiling. Existing job shapes carry hosted measurements. New
    worker shapes carry an explicit pending-measurement bead and predecessor-derived
    ceiling until their first candidate run; they cannot be mistaken for observed
    walls. The same shape `test_every_page_job_a_pull_request_runs_is_budgeted` holds
    over `pages`.

    Enforcement against a live run belongs to `devtools.check_ci_gate_walls`; this is the
    declaration check, and like `check_gate_budgets` it needs no clock.
    """
    register = load(BUDGETS)
    gate = register.ci_gate("deep-gate")
    assert gate is not None, "the deep gate has no entry in gate-budgets.yaml"
    jobs = _workflow(DEEP_GATE)["jobs"]

    assert gate.file == str(DEEP_GATE.relative_to(REPOSITORY_ROOT))
    assert gate.aggregate == AGGREGATE_JOB
    # Driven from the workflow, so a fifth deep job fails here the day it arrives rather
    # than running unclocked -- which is the property the 1943.05s figure never had.
    assert set(gate.ids) == set(jobs) - {AGGREGATE_JOB}
    assert ci_declaration_problems(register) == []

    headroom = register.policy.max_headroom
    for budget in (*gate.jobs, gate.wall):
        where = budget.id
        assert budget.argument.strip(), where
        if budget.measured_seconds is None:
            assert budget.measured_seconds is None, where
            assert budget.measured_on is None, where
            assert budget.measured_where is None, where
            assert budget.spread is None, where
            assert re.fullmatch(r"think-[a-z0-9]{4}", budget.pending_measurement or ""), where
        else:
            assert budget.pending_measurement is None, where
            assert budget.measured_seconds is not None, where
            assert budget.measured_on, where
            assert budget.measured_where is not None, where
            assert re.search(r"run \d{8,}", budget.measured_where), where
            assert budget.ceiling_seconds >= budget.measured_seconds, where
            assert budget.ceiling_seconds <= headroom * budget.measured_seconds, where
            # A hosted band has to be argued against the runner's own variance, so the
            # spread the readings showed is recorded beside the mean of them.
            assert budget.spread is not None, where
            assert budget.spread >= 1.0, where

    # The gate declares its own band rather than inheriting the policy's, because the
    # policy's 1.5x was measured against local tiers. It may be tighter, never looser.
    assert 1.0 < gate.drift_ratio <= register.policy.drift_ratio
    # A relaxation with no bead behind it is a permanent one.
    assert gate.reports_only
    assert gate.tracking_bead
    assert gate.wall.history[-1].seconds == 2540.6


def test_the_deep_gate_aggregate_reads_the_walls_it_is_budgeted_against() -> None:
    """A price nothing reads is not a budget, which is `OR-17`'s third obligation.

    The register above is only a declaration until something compares a finished run
    against it. `packing-required` runs `check_pr_wall` for exactly this reason and
    `check_gate_budgets` refuses a pull-request wall whose aggregator never runs it; this
    is that rule for the deep surface.

    The step is `continue-on-error` and the gate is declared `enforcement: reporting`,
    which are two different relaxations and both are deliberate. The gate reports because
    a band built on one hosted reading cannot separate a 1.5x regression from a slow
    runner draw. The step continues on error because a 45-minute pre-merge gate must not
    go red for a measurement tool, and an unreachable API is not a regression. Both are
    `think-haam`'s to remove.
    """
    aggregate = _workflow(DEEP_GATE)["jobs"][AGGREGATE_JOB]
    all_steps = list(aggregate["steps"])
    steps = [step for step in all_steps if isinstance(step.get("run"), str)]
    reporting = [step for step in steps if "devtools.check_ci_gate_walls" in str(step["run"])]

    assert len(reporting) == 1, "the aggregate must read its own walls exactly once"
    # Nothing added to this job may decide its verdict except the prerequisite script,
    # so every other step -- the checkout and the toolchain included -- continues on
    # error. A measurement tool that can redden a 45-minute pre-merge gate is worse than
    # no measurement tool.
    verdict = all_steps[0]
    for index in range(1, 4):
        assert "needs." in str(verdict.get("env", {}).get(f"EXHAUSTIVE_{index}_RESULT", ""))
    for step in all_steps[1:]:
        assert step.get("continue-on-error") is True, step.get("name")
    (step,) = reporting
    command = " ".join(str(step["run"]).split())
    assert "--gate deep-gate" in command
    # No `--enforce`: the register's `enforcement` field is the one authority for that,
    # and a flag in the workflow would be a second one that could disagree with it.
    assert "--enforce" not in command
    assert step.get("continue-on-error") is True
    # It must run when a prerequisite failed too: a deep job that died slowly is exactly
    # the run whose walls are worth reading.
    assert str(step.get("if", "")).startswith("always()")
    assert aggregate["permissions"] == {"contents": "read", "actions": "read"}
