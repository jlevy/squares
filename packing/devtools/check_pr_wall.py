#!/usr/bin/env python3
"""Hold a pull request's CI wall to `OR-14`'s budget, and to its own recorded median.

`OR-14` names one number for the pull-request surface: two to two and a half minutes,
three at the outer edge. Until 2026-09-15 nothing measured that number. The register in
`devtools/gate-budgets.yaml` times each tier's gate step, and every tier stayed inside
its own ceiling while the required wall went from a 154 s median on 2026-09-06 to 284 s
on 2026-09-15 and the certificate page's pull-request run from 37 s to 464 s. The wall is
the longest job with its checkout, its toolchain and its queue, and no tier sees that.

This reads one workflow run's jobs from the GitHub API and computes:

* **the run's wall**, from the run starting to the start of the job that aggregates it
  (`packing-required`, or Pages' `pr-wall`). A job cannot see its own completion, so the
  aggregator's start is where the measurement ends in CI, and a run measured afterwards
  ends at the same place so that the two agree. A run with no aggregator -- the Pages
  runs from before it existed -- ends at its last gating job's completion, and says so;
* **each job's wall**, with its queue, and its step time split into setup and work.
  A step is setup when its name matches `setup_steps` in the register: provisioning,
  caches, artifact transfer and the post-job teardown. Everything else is work.

It fails when the wall exceeds the workflow's `budget_seconds`, or when it is
`regression_ratio` or more of the median recorded for the workflow and the pull
request's kind (`main` for a pull request into the main branch, `stacked` for one into
another branch). When the regression cannot be judged -- too few recorded runs, no
record for the kind, or a run that was cancelled or failed -- it says so, as a GitHub
warning annotation and in the step summary, and does not pass silently.

It runs on the runner's own `python3` with nothing but PyYAML, so the aggregator pays a
sparse checkout and not an environment sync.

Usage, in CI (the run, repository and aggregator come from the environment):
    python3 packing/devtools/check_pr_wall.py --workflow packing-validation

Afterwards, from `packing/`, on any run:
    uv run --frozen --all-extras --group dev python -m devtools.check_pr_wall \
        --workflow packing-validation --run-id 34921505934

To record a median, measure several runs at once and paste the block it prints:
    ... check_pr_wall --workflow packing-validation --sample --recent 20
    ... check_pr_wall --workflow packing-validation --sample --run-id A --run-id B ...

`--dump` prints the trimmed API payload a verdict was computed from, which is how the
fixtures under `tests/fixtures/pr-wall/` were recorded.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

try:
    import yaml
except ImportError:  # pragma: no cover - only on an interpreter without PyYAML
    print(
        f"check_pr_wall: PyYAML is not importable by {sys.executable}; the register "
        "cannot be read",
        file=sys.stderr,
    )
    raise SystemExit(2) from None

REGISTER = Path(__file__).resolve().parent / "gate-budgets.yaml"
API = "https://api.github.com"
USER_AGENT = "squares-check-pr-wall (+https://github.com/jlevy/squares)"
#: Fields a verdict reads; `--dump` keeps these and drops the rest.
RUN_FIELDS = (
    "id",
    "name",
    "path",
    "event",
    "status",
    "conclusion",
    "created_at",
    "run_started_at",
    "run_attempt",
    "head_branch",
    "head_sha",
)
JOB_FIELDS = ("name", "status", "conclusion", "created_at", "started_at", "completed_at")
STEP_FIELDS = ("name", "conclusion", "started_at", "completed_at")
#: How long an aggregator waits for the API to report a prerequisite it has already been
#: told finished. The jobs endpoint can lag the `needs` graph by a moment.
SETTLE_ATTEMPTS = 3
SETTLE_SECONDS = 3.0


class WallError(Exception):
    """The register or the API cannot supply what a verdict needs."""


@dataclass(frozen=True)
class Sample:
    run: int
    seconds: float


@dataclass(frozen=True)
class KindRecord:
    """The recorded wall of one pull-request kind: its runs, and their median."""

    kind: str
    median_seconds: float
    measured_on: str
    samples: tuple[Sample, ...]


@dataclass(frozen=True)
class WorkflowWall:
    id: str
    file: str
    aggregator: str
    not_gating: tuple[str, ...]
    budget_seconds: float
    kinds: tuple[KindRecord, ...]

    def record(self, kind: str | None) -> KindRecord | None:
        return next((record for record in self.kinds if record.kind == kind), None)


@dataclass(frozen=True)
class WallPolicy:
    regression_ratio: float
    min_samples: int
    main_branch: str
    setup_steps: tuple[re.Pattern[str], ...]

    def is_setup(self, step_name: str) -> bool:
        return any(pattern.search(step_name) for pattern in self.setup_steps)


@dataclass(frozen=True)
class WallRegister:
    policy: WallPolicy
    workflows: tuple[WorkflowWall, ...]

    def workflow(self, workflow_id: str) -> WorkflowWall:
        found = next((entry for entry in self.workflows if entry.id == workflow_id), None)
        if found is None:
            known = ", ".join(entry.id for entry in self.workflows)
            raise WallError(f"no pull-request wall is declared for {workflow_id!r} ({known})")
        return found


@dataclass(frozen=True)
class JobTiming:
    name: str
    conclusion: str | None
    queue_seconds: float | None
    setup_seconds: float
    work_seconds: float
    wall_seconds: float | None


@dataclass(frozen=True)
class Measurement:
    run_id: int
    workflow: str
    kind: str | None
    wall_seconds: float | None
    ends_at: str
    critical_job: str | None
    jobs: tuple[JobTiming, ...]
    unmeasurable: tuple[str, ...] = ()
    #: The aggregator's own wait for a runner, which the pull request waits through too.
    aggregator_queue_seconds: float | None = None


@dataclass(frozen=True)
class WallVerdict:
    status: Literal["passed", "failed", "unmeasurable"]
    failures: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    #: Rules that were not applied, and why. They render as warnings, because a rule that
    #: silently did not run reads exactly like a rule that passed.
    unjudged: tuple[str, ...] = ()


def _mapping(value: object, what: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise WallError(f"{what} must be a mapping, found {type(value).__name__}")
    return value


def _number(value: object, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise WallError(f"{what} must be a positive number, found {value!r}")
    return float(value)


def _text(value: object, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise WallError(f"{what} must be a non-empty string, found {value!r}")
    return value.strip()


def _kind_from(raw: object, where: str) -> KindRecord:
    entry = _mapping(raw, where)
    kind = _text(entry.get("kind"), f"{where}.kind")
    raw_samples = entry.get("samples")
    if not isinstance(raw_samples, list) or not raw_samples:
        raise WallError(f"{where} ({kind}) must list the runs its median was taken from")
    samples = tuple(
        Sample(
            run=int(_number(_mapping(item, f"{where}.samples").get("run"), f"{where} run")),
            seconds=_number(item.get("seconds"), f"{where} seconds"),
        )
        for item in raw_samples
    )
    median = _number(entry.get("median_seconds"), f"{where}.median_seconds")
    computed = statistics.median(sample.seconds for sample in samples)
    if abs(computed - median) > 0.05:
        raise WallError(
            f"{where} ({kind}) declares a median of {median:g}s but its samples' median is "
            f"{computed:g}s; the figure is read from the runs, not typed beside them"
        )
    return KindRecord(
        kind=kind,
        median_seconds=median,
        measured_on=_text(entry.get("measured_on"), f"{where}.measured_on"),
        samples=samples,
    )


def load_walls(path: Path = REGISTER) -> WallRegister:
    """Read `pull_request_walls` from the register, refusing what no rule could apply to."""
    try:
        document = _mapping(yaml.safe_load(path.read_text(encoding="utf-8")), str(path))
    except OSError as error:
        raise WallError(f"the register is unreadable at {path}: {error}") from error
    section = _mapping(document.get("pull_request_walls"), "pull_request_walls")
    raw_policy = _mapping(section.get("policy"), "pull_request_walls.policy")
    ratio = _number(raw_policy.get("regression_ratio"), "policy.regression_ratio")
    if ratio <= 1.0:
        raise WallError(f"policy.regression_ratio is {ratio:g}; at or below 1 every run fails")
    patterns = raw_policy.get("setup_steps")
    if not isinstance(patterns, list) or not patterns:
        raise WallError("policy.setup_steps must list the step-name patterns that are setup")
    policy = WallPolicy(
        regression_ratio=ratio,
        min_samples=int(_number(raw_policy.get("min_samples"), "policy.min_samples")),
        main_branch=_text(raw_policy.get("main_branch"), "policy.main_branch"),
        setup_steps=tuple(
            re.compile(_text(item, "a setup_steps pattern")) for item in patterns
        ),
    )
    raw_workflows = section.get("workflows")
    if not isinstance(raw_workflows, list) or not raw_workflows:
        raise WallError("pull_request_walls.workflows must be a non-empty list")
    workflows: list[WorkflowWall] = []
    for index, raw in enumerate(raw_workflows):
        entry = _mapping(raw, f"workflows[{index}]")
        workflow_id = _text(entry.get("id"), f"workflows[{index}].id")
        where = f"workflow {workflow_id!r}"
        not_gating = entry.get("not_gating") or []
        if not isinstance(not_gating, list):
            raise WallError(f"{where}.not_gating must be a list of job ids")
        _text(entry.get("argument"), f"{where}.argument")
        workflows.append(
            WorkflowWall(
                id=workflow_id,
                file=_text(entry.get("file"), f"{where}.file"),
                aggregator=_text(entry.get("aggregator"), f"{where}.aggregator"),
                not_gating=tuple(_text(name, f"{where}.not_gating") for name in not_gating),
                budget_seconds=_number(entry.get("budget_seconds"), f"{where}.budget_seconds"),
                kinds=tuple(
                    _kind_from(kind, f"{where}.kinds[{position}]")
                    for position, kind in enumerate(entry.get("kinds") or [])
                ),
            )
        )
    return WallRegister(policy=policy, workflows=tuple(workflows))


def kind_of(base_ref: str | None, main_branch: str) -> str | None:
    """`main` for a pull request into the main branch, `stacked` for one into any other."""
    if not base_ref:
        return None
    return "main" if base_ref == main_branch else "stacked"


def _instant(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    return datetime.fromisoformat(value)


def _span(start: object, end: object) -> float | None:
    begun, finished = _instant(start), _instant(end)
    if begun is None or finished is None:
        return None
    return max(0.0, (finished - begun).total_seconds())


def _job_id(name: str) -> str:
    """A matrix job is reported as `id (value)`; `not_gating` names the id."""
    return name.split(" (", 1)[0]


def _gates(job: dict[str, Any], workflow: WorkflowWall, aggregator: str) -> bool:
    """Whether a pull request waits on this job: not the aggregator, not declared aside."""
    return job["name"] != aggregator and _job_id(str(job["name"])) not in workflow.not_gating


def _timing(job: dict[str, Any], policy: WallPolicy) -> JobTiming:
    setup = work = 0.0
    for step in job.get("steps") or []:
        seconds = _span(step.get("started_at"), step.get("completed_at")) or 0.0
        if policy.is_setup(str(step.get("name", ""))):
            setup += seconds
        else:
            work += seconds
    completed = job.get("status") == "completed"
    return JobTiming(
        name=str(job["name"]),
        conclusion=job.get("conclusion"),
        queue_seconds=_span(job.get("created_at"), job.get("started_at")),
        setup_seconds=setup,
        work_seconds=work,
        wall_seconds=_span(job.get("started_at"), job.get("completed_at"))
        if completed
        else None,
    )


def measure(
    run: dict[str, Any],
    jobs: Sequence[dict[str, Any]],
    workflow: WorkflowWall,
    policy: WallPolicy,
    *,
    kind: str | None,
) -> Measurement:
    """The run's wall to its aggregator's start, and every gating job's split."""
    reasons: list[str] = []
    if run.get("conclusion") == "cancelled":
        reasons.append("the run was cancelled, so its wall is not the wall of a finished run")
    gating = [
        job
        for job in jobs
        if _gates(job, workflow, workflow.aggregator) and job.get("conclusion") != "skipped"
    ]
    if not gating:
        reasons.append("no gating job ran")
    for job in gating:
        if job.get("status") != "completed":
            reasons.append(f"`{job['name']}` has not completed ({job.get('status')})")
        elif job.get("conclusion") != "success":
            reasons.append(
                f"`{job['name']}` concluded {job.get('conclusion')}, so the run's wall is "
                "not comparable with a run that did its whole work"
            )
    finished = sorted(
        (instant, str(job["name"]))
        for job in gating
        if (instant := _instant(job.get("completed_at"))) is not None
    )
    start = _instant(run.get("run_started_at") or run.get("created_at"))
    aggregator = next((job for job in jobs if job["name"] == workflow.aggregator), None)
    aggregator_start = _instant(aggregator.get("started_at")) if aggregator else None
    if aggregator_start is not None:
        end, ends_at = aggregator_start, f"the start of `{workflow.aggregator}`"
    elif finished:
        end = finished[-1][0]
        ends_at = f"the last gating job's completion (this run has no `{workflow.aggregator}`)"
    else:
        end, ends_at = None, "nowhere: no gating job completed"
    wall = None if start is None or end is None else max(0.0, (end - start).total_seconds())
    return Measurement(
        run_id=int(run["id"]),
        workflow=workflow.id,
        kind=kind,
        wall_seconds=wall,
        ends_at=ends_at,
        critical_job=finished[-1][1] if finished else None,
        jobs=tuple(_timing(job, policy) for job in gating),
        unmeasurable=tuple(reasons),
        aggregator_queue_seconds=(
            _span(aggregator.get("created_at"), aggregator.get("started_at"))
            if aggregator
            else None
        ),
    )


def critical_split(measurement: Measurement) -> str:
    """The job that set the wall, and where its time went."""
    job = next((job for job in measurement.jobs if job.name == measurement.critical_job), None)
    if job is None:
        return "no gating job completed"
    queued = "" if job.queue_seconds is None else f"queued {job.queue_seconds:.0f}s, "
    split = (
        f"`{job.name}` finished last ({queued}setup {job.setup_seconds:.0f}s, "
        f"work {job.work_seconds:.0f}s)"
    )
    if measurement.aggregator_queue_seconds is None:
        return split
    return f"{split}, then the aggregator queued {measurement.aggregator_queue_seconds:.0f}s"


def judge(measurement: Measurement, workflow: WorkflowWall, policy: WallPolicy) -> WallVerdict:
    """Apply the budget and the regression rule, and name every rule that did not run."""
    if measurement.unmeasurable or measurement.wall_seconds is None:
        return WallVerdict(
            status="unmeasurable",
            unjudged=(
                *measurement.unmeasurable,
                "neither the budget nor the regression rule was applied to this run",
            ),
        )
    wall = measurement.wall_seconds
    failures: list[str] = []
    notes: list[str] = []
    unjudged: list[str] = []
    if wall > workflow.budget_seconds:
        failures.append(
            f"the pull request waited {wall:.0f}s against the {workflow.budget_seconds:g}s "
            f"budget: {critical_split(measurement)}"
        )
    else:
        notes.append(f"{wall:.0f}s is inside the {workflow.budget_seconds:g}s budget")
    record = workflow.record(measurement.kind)
    if measurement.kind is None:
        unjudged.append(
            "the pull request's base branch is unknown, so its kind and its recorded median "
            "are too; the regression rule was not applied"
        )
    elif record is None:
        unjudged.append(
            f"no wall is recorded for {workflow.id} pull requests of kind "
            f"`{measurement.kind}`; the regression rule was not applied. Record one with "
            "--sample"
        )
    elif len(record.samples) < policy.min_samples:
        unjudged.append(
            f"the `{measurement.kind}` record holds {len(record.samples)} run(s) and the "
            f"regression rule needs {policy.min_samples}; it was not applied"
        )
    else:
        ratio = wall / record.median_seconds
        described = (
            f"{wall:.0f}s is {ratio:.2f}x the {record.median_seconds:g}s median of "
            f"{len(record.samples)} `{measurement.kind}` runs recorded {record.measured_on}"
        )
        if ratio >= policy.regression_ratio:
            failures.append(
                f"{described}, where {policy.regression_ratio:g}x fails: "
                f"{critical_split(measurement)}"
            )
        else:
            notes.append(described)
    return WallVerdict(
        status="failed" if failures else "passed",
        failures=tuple(failures),
        notes=tuple(notes),
        unjudged=tuple(unjudged),
    )


def _jobs_by_wall(measurement: Measurement) -> list[JobTiming]:
    return sorted(measurement.jobs, key=lambda job: -(job.wall_seconds or 0.0))


def _seconds(value: float | None, missing: str) -> str:
    return missing if value is None else f"{value:.0f}"


def render(measurement: Measurement, verdict: WallVerdict) -> list[str]:
    """The verdict and the per-job table, as lines."""
    lines = [
        (
            f"== pull-request wall: {measurement.workflow} run {measurement.run_id}, kind "
            f"{measurement.kind or 'unknown'} =="
        ),
        (
            f"  {_seconds(measurement.wall_seconds, 'unmeasured')}s from the run's start to "
            f"{measurement.ends_at}"
        ),
        f"  {'job':<34} {'queue':>6} {'setup':>6} {'work':>6} {'wall':>6}",
    ]
    lines.extend(
        f"  {job.name:<34} {_seconds(job.queue_seconds, '-'):>6} {job.setup_seconds:>6.0f} "
        f"{job.work_seconds:>6.0f} {_seconds(job.wall_seconds, '-'):>6}"
        for job in _jobs_by_wall(measurement)
    )
    lines.extend(f"  FAIL: {failure}" for failure in verdict.failures)
    lines.extend(f"  NOT JUDGED: {note}" for note in verdict.unjudged)
    lines.extend(f"  note: {note}" for note in verdict.notes)
    lines.append(f"  verdict: {verdict.status}")
    return lines


def summary_markdown(measurement: Measurement, verdict: WallVerdict) -> str:
    """The same verdict, for `$GITHUB_STEP_SUMMARY`."""
    rows = [
        f"### Pull-request wall: {verdict.status}",
        "",
        (
            f"{_seconds(measurement.wall_seconds, 'unmeasured')} s from the run's start to "
            f"{measurement.ends_at} (kind `{measurement.kind or 'unknown'}`)."
        ),
        "",
        "| Job | Queue | Setup | Work | Wall |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    rows.extend(
        f"| `{job.name}` | {_seconds(job.queue_seconds, '')} | {job.setup_seconds:.0f} "
        f"| {job.work_seconds:.0f} | {_seconds(job.wall_seconds, '')} |"
        for job in _jobs_by_wall(measurement)
    )
    rows.append("")
    rows.extend(f"- **Fail:** {failure}" for failure in verdict.failures)
    rows.extend(f"- **Not judged:** {note}" for note in verdict.unjudged)
    rows.extend(f"- {note}" for note in verdict.notes)
    return "\n".join(rows) + "\n"


class Client:
    """The few GitHub API reads a verdict needs, retrying a transient failure."""

    def __init__(self, repository: str, token: str | None) -> None:
        self.repository = repository
        self.token = token

    def get(self, path: str) -> Any:
        headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(
            f"{API}/repos/{self.repository}/{path}", headers=headers
        )
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    return json.load(response)
            except urllib.error.HTTPError as error:
                if error.code < 500 or attempt == 2:
                    raise WallError(
                        f"GET {path} answered {error.code}: {error.reason}"
                    ) from error
            except urllib.error.URLError as error:
                if attempt == 2:
                    raise WallError(f"GET {path} failed: {error.reason}") from error
            time.sleep(2.0 * (attempt + 1))
        raise WallError(f"GET {path} failed")  # pragma: no cover - the loop returns or raises

    def run(self, run_id: int) -> dict[str, Any]:
        return self.get(f"actions/runs/{run_id}")

    def jobs(self, run_id: int) -> list[dict[str, Any]]:
        return list(self.get(f"actions/runs/{run_id}/jobs?filter=latest&per_page=100")["jobs"])

    def base_ref(self, run: dict[str, Any]) -> str | None:
        """The pull request's base, from the run or from the pulls its head commit is in."""
        for pull in run.get("pull_requests") or []:
            return str(pull["base"]["ref"])
        pulls = self.get(f"commits/{run['head_sha']}/pulls")
        heads = [pull for pull in pulls if pull["head"]["sha"] == run["head_sha"]] or pulls
        return str(heads[0]["base"]["ref"]) if heads else None

    def recent_runs(self, workflow_file: str, count: int) -> list[dict[str, Any]]:
        name = Path(workflow_file).name
        page = self.get(
            f"actions/workflows/{name}/runs?event=pull_request&status=success&per_page={count}"
        )
        return list(page["workflow_runs"])


def trim(run: dict[str, Any], jobs: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """The API payload a verdict reads, and nothing else, for `--dump` and the fixtures."""
    return {
        "run": {key: run.get(key) for key in RUN_FIELDS},
        "jobs": [
            {
                **{key: job.get(key) for key in JOB_FIELDS},
                "steps": [{key: step.get(key) for key in STEP_FIELDS} for step in job["steps"]],
            }
            for job in jobs
        ],
    }


def github_token() -> str | None:
    for variable in ("GITHUB_TOKEN", "GH_TOKEN"):
        if os.environ.get(variable):
            return os.environ[variable]
    try:
        completed = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, check=False, timeout=10
        )
    except OSError, subprocess.SubprocessError:
        return None
    return completed.stdout.strip() or None


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Hold a pull request's CI wall to its budget.")
    parser.add_argument("--workflow", required=True, help="the workflow's id in the register")
    parser.add_argument("--run-id", type=int, action="append", default=[])
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY", "jlevy/squares"))
    parser.add_argument("--base-ref", help="the pull request's base branch, when known")
    parser.add_argument("--register", type=Path, default=REGISTER)
    parser.add_argument("--sample", action="store_true", help="print a record from many runs")
    parser.add_argument("--recent", type=int, default=0, help="with --sample: the last N runs")
    parser.add_argument("--dump", action="store_true", help="print the trimmed API payload")
    return parser


def _settled_jobs(client: Client, run_id: int, workflow: WorkflowWall) -> list[dict[str, Any]]:
    """The jobs, once every gating job the API lists reports its completion."""
    jobs = client.jobs(run_id)
    for _ in range(SETTLE_ATTEMPTS - 1):
        if all(
            job.get("status") == "completed"
            for job in jobs
            if _gates(job, workflow, workflow.aggregator)
        ):
            break
        time.sleep(SETTLE_SECONDS)
        jobs = client.jobs(run_id)
    return jobs


def _sample(
    client: Client, register: WallRegister, workflow: WorkflowWall, arguments: Any
) -> int:
    runs = [client.run(run_id) for run_id in arguments.run_id]
    if arguments.recent:
        runs.extend(client.recent_runs(workflow.file, arguments.recent))
    by_kind: dict[str, list[Sample]] = {}
    for run in runs:
        kind = kind_of(client.base_ref(run), register.policy.main_branch)
        measurement = measure(
            run, client.jobs(int(run["id"])), workflow, register.policy, kind=kind
        )
        if measurement.unmeasurable or measurement.wall_seconds is None or kind is None:
            reasons = "; ".join(measurement.unmeasurable) or "its kind is unknown"
            print(f"run {run['id']}: not a sample: {reasons}")
            continue
        print(
            f"run {run['id']} ({kind}, {run.get('head_branch')}, {run.get('created_at')}): "
            f"{measurement.wall_seconds:.0f}s, {critical_split(measurement)}"
        )
        by_kind.setdefault(kind, []).append(Sample(int(run["id"]), measurement.wall_seconds))
    for kind, samples in sorted(by_kind.items()):
        median = statistics.median(sample.seconds for sample in samples)
        print(f"\n- kind: {kind}\n  median_seconds: {median:g}\n  samples:")
        print(
            "\n".join(f"  - {{run: {item.run}, seconds: {item.seconds:g}}}" for item in samples)
        )
    return 0


def _annotate(measurement: Measurement, verdict: WallVerdict) -> None:
    """GitHub annotations and a step summary, so a rule that did not run is seen."""
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return
    for failure in verdict.failures:
        print(f"::error title=Pull-request wall::{failure}")
    for note in verdict.unjudged:
        print(f"::warning title=Pull-request wall not judged::{note}")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with Path(summary).open("a", encoding="utf-8") as handle:
            handle.write(summary_markdown(measurement, verdict))


def _running_run(workflow: WorkflowWall) -> int:
    """The run this job belongs to, refusing a job that is not the declared aggregator.

    A wall measured from a job that is not the one every other job feeds would end
    somewhere in the middle of the run, which is worse than not measuring it.
    """
    run_id = os.environ.get("GITHUB_RUN_ID")
    if not run_id:
        raise WallError("no --run-id was given and GITHUB_RUN_ID is not set")
    job = os.environ.get("GITHUB_JOB")
    if job != workflow.aggregator:
        raise WallError(
            f"this job is `{job}` but the register names `{workflow.aggregator}` as "
            f"{workflow.id}'s aggregator, so the wall would end in the wrong place"
        )
    return int(run_id)


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        register = load_walls(arguments.register)
        workflow = register.workflow(arguments.workflow)
        client = Client(arguments.repo, github_token())
        if arguments.sample:
            return _sample(client, register, workflow, arguments)
        in_run = not arguments.run_id
        if in_run:
            arguments.run_id = [_running_run(workflow)]
        status = 0
        for run_id in arguments.run_id:
            run = client.run(run_id)
            jobs = _settled_jobs(client, run_id, workflow) if in_run else client.jobs(run_id)
            if arguments.dump:
                print(json.dumps(trim(run, jobs), indent=1))
                continue
            base = (
                arguments.base_ref or os.environ.get("GITHUB_BASE_REF") or client.base_ref(run)
            )
            kind = kind_of(base, register.policy.main_branch)
            measurement = measure(run, jobs, workflow, register.policy, kind=kind)
            verdict = judge(measurement, workflow, register.policy)
            print("\n".join(render(measurement, verdict)))
            _annotate(measurement, verdict)
            status = max(status, 1 if verdict.status == "failed" else 0)
    except WallError as error:
        print(f"check_pr_wall: {error}", file=sys.stderr)
        return 2
    return status


if __name__ == "__main__":
    raise SystemExit(main())
