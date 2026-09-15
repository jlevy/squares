#!/usr/bin/env python3
"""Refuse a tier ceiling that has drifted slack, a tier with no ceiling, and a ratchet.

This is the static half of the gate's own cost check, and it is the half that would have
caught the 2026-08-30 state on the day. `validate.py` recorded `--fast` at 499s in a
docstring beside an 1800s cap: 3.61x of headroom, which cannot see a regression smaller
than 3.61x. The tier then tripled inside the cap and nothing objected.

It was not enough to stop the second spiral, from 2026-09-06 to 2026-09-15, and the three
rules added on 2026-09-15 are each named for how that one got through:

* **A pull-request tier with no recorded cost fails.** Seven of nine tiers had none, and
  an empty record switches off the drift, stale and headroom rules together, leaving one
  absolute ceiling. `checks` and `sweeps` sat empty for eight days while the gate printed
  the line to write on every run. Which tiers a pull request runs is read from
  `packing-validation.yml`, so a new PR job cannot arrive with an empty record either; the
  record must cite the hosted runs it came from.
* **A record that rises without attribution fails.** `suite`'s record went 102.83 →
  162.62 → 118.72 → 183.44 s in three days, each move a real reading, and 2.4x of growth
  went through a 1.5x drift rule. `gate_budgets.rise_findings` is the rule; the history it
  reads is kept in the register.
* **The pull-request wall is declared and wired.** `OR-14` targets PR wall, and no tier
  sees it. `devtools.check_pr_wall` enforces it on every run; this checks its budgets
  stay inside `OR-14`'s outer edge and that each workflow's aggregator still runs it.

Nothing here runs a tier or looks at a clock, so it cannot be dismissed as a busy runner.
It asserts, about `devtools/gate-budgets.yaml`:

* every tier `packing-validate` can select as a whole has a declared ceiling, so a new
  tier cannot arrive without one;
* every declared tier is a tier that exists, so a ceiling cannot outlive its tier;
* every ceiling is within `policy.max_headroom` of the cost recorded for that tier;
* every tier a pull-request job runs has a recorded cost that cites a hosted run;
* no record rose past `policy.max_unattributed_rise` without an attribution;
* every pull-request wall budget is inside `OR-14`'s three minutes, and runs; and
* `development.md` names every tier.

Usage:
    uv run --frozen --all-extras --group dev python -m devtools.check_gate_budgets

With `--attribute-files BEFORE.json AFTER.json` it prints the `attribution:` block for a
suite record from two per-file test-cost reports (a list of `{file, tests, seconds}`),
and names the files the second adds: the consumer end of lane 2's per-file report.
"""

# `_parser` and `_tier_id` are the CLI's own, so a pull-request job's tier is read the way
# the gate reads it. `check_declared_commands` and `test_validation_cli` take the same
# exemption for the same reason.
# pyright: reportPrivateUsage=false
from __future__ import annotations

import argparse
import json
import re
import shlex
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Any

from devtools.check_pr_wall import WallError, load_walls
from sqpack.cli.validate import TIER_IDS, _tier_id
from sqpack.cli.validate import _parser as _validate_parser
from sqpack.gate_budgets import (
    BudgetError,
    Register,
    declaration_problems,
    load,
    ratchet_problems,
)
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
#: Resolved from this file rather than from the installed package, so a negative control
#: that corrupts a snapshot's register is checking the snapshot's register. `sqpack` is
#: installed and resolves to the real checkout wherever it runs; `devtools` resolves to
#: whatever tree it was launched from, which is the tree the control mutated.
REGISTER = ROOT / "devtools" / "gate-budgets.yaml"
#: The contributor-facing statement of which tier runs where and at what cost. A tier
#: this document does not name is a tier nobody knows to run.
GUIDE = REPO / "development.md"
#: The workflow whose jobs are the pull-request surface of `packing-validate`.
PULL_REQUEST_WORKFLOW = REPO / ".github" / "workflows" / "packing-validation.yml"
NOT_ON_PULL_REQUESTS = "github.event_name != 'pull_request'"
#: A GitHub Actions run id. A record that names none cannot be re-taken or checked.
RUN_ID = re.compile(r"\b\d{10,}\b")
#: `OR-14`: "three is the outer edge of acceptable". A wall budget above it is not a
#: budget but a different rule, and the place to change that is `operating-rules.md`.
OR_14_OUTER_EDGE_SECONDS = 180.0
WALL_TOOL = "check_pr_wall.py"
#: Rows the `--attribute-files` block names.
ATTRIBUTED_FILES = 8


def coverage_problems(register: Register) -> list[str]:
    """Tiers with no ceiling, and ceilings with no tier."""
    declared = set(register.ids)
    selectable = set(TIER_IDS)
    problems = [
        f"tier {tier!r} can be selected but declares no ceiling in {register.path}"
        for tier in sorted(selectable - declared)
    ]
    problems.extend(
        f"tier {tier!r} declares a ceiling but packing-validate cannot select it"
        for tier in sorted(declared - selectable)
    )
    return problems


def documentation_problems(register: Register) -> list[str]:
    """Tiers `development.md` stops describing.

    The register is the machine's copy and the guide is the reader's, and the two drift in
    one direction: a tier gets added or renamed and the prose keeps describing the old
    shape. Naming is all that is checked -- the costs in the guide are explicitly a
    snapshot, and `packing-validate --budgets` is what it tells the reader to run -- but a
    tier the guide never mentions is one a contributor cannot know to choose.
    """
    try:
        text = GUIDE.read_text(encoding="utf-8")
    except OSError as error:
        return [f"{GUIDE.name} is unreadable: {error}"]
    problems = [
        f"{GUIDE.name} never names `{tier.command}`, so a reader cannot tell the "
        f"{tier.id} tier exists or who runs it"
        for tier in register.tiers
        if tier.command not in text
    ]
    if REGISTER.name not in text:
        problems.append(
            f"{GUIDE.name} does not cite {REGISTER.name}, which is where the ceilings it "
            "describes actually live"
        )
    return problems


def pull_request_tiers(workflow: Path = PULL_REQUEST_WORKFLOW) -> dict[str, str]:
    """Each whole tier a pull-request job runs, mapped to the job that runs it.

    Read from the workflow and resolved with the CLI's own parser, as
    `test_the_pull_request_jobs_partition_the_surface` does, so a tier added to the
    pull-request surface is found here without anyone listing it.
    """
    document = safe_load(workflow.read_text(encoding="utf-8"))
    found: dict[str, str] = {}
    for job_name, job in document["jobs"].items():
        if NOT_ON_PULL_REQUESTS in str(job.get("if", "")):
            continue
        for step in job.get("steps", []):
            command = str(step.get("run", ""))
            if "packing-validate" not in command or NOT_ON_PULL_REQUESTS in str(
                step.get("if", "")
            ):
                continue
            tokens = shlex.split(command)
            namespace = _validate_parser().parse_args(
                tokens[tokens.index("packing-validate") + 1 :]
            )
            tier = _tier_id(namespace)
            if tier is not None and not namespace.skip:
                found[tier] = str(job_name)
    return found


def unrecorded_problems(register: Register, tiers: dict[str, str]) -> list[str]:
    """Pull-request tiers whose record is empty, or cites no hosted run."""
    problems: list[str] = []
    for tier_id, job in sorted(tiers.items()):
        tier = register.tier(tier_id)
        if tier is None:
            continue
        if tier.measured_seconds is None:
            problems.append(
                f"tier {tier_id!r} runs on every pull request, in the `{job}` job, and has "
                "no recorded cost, so its drift, stale and headroom rules are all off. Record "
                "it from hosted runs: python -m devtools.read_tier_walls --tier "
                f"{tier_id} --run-id ..."
            )
        elif not RUN_ID.search(tier.measured_where or ""):
            problems.append(
                f"tier {tier_id!r} runs on every pull request and its record names no hosted "
                "run in measured_where, so nobody can re-take the reading it rests on"
            )
    return problems


def wall_problems(register_path: Path = REGISTER) -> list[str]:
    """The pull-request wall budgets: readable, inside `OR-14`, and actually run."""
    try:
        walls = load_walls(register_path)
    except WallError as error:
        return [f"pull_request_walls: {error}"]
    problems: list[str] = []
    for workflow in walls.workflows:
        label = f"pull-request wall {workflow.id!r}"
        if workflow.budget_seconds > OR_14_OUTER_EDGE_SECONDS:
            problems.append(
                f"{label}: a {workflow.budget_seconds:g}s budget is past OR-14's "
                f"{OR_14_OUTER_EDGE_SECONDS:g}s outer edge; change the rule, not the budget"
            )
        path = REPO / workflow.file
        try:
            jobs = safe_load(path.read_text(encoding="utf-8"))["jobs"]
        except (OSError, KeyError, TypeError) as error:
            problems.append(f"{label}: {workflow.file} has no readable jobs: {error}")
            continue
        problems.extend(
            f"{label}: `{name}` is declared not to gate a pull request but {path.name} has "
            "no such job"
            for name in workflow.not_gating
            if name not in jobs
        )
        aggregator = jobs.get(workflow.aggregator)
        if not isinstance(aggregator, dict):
            problems.append(f"{label}: {path.name} has no `{workflow.aggregator}` job")
            continue
        invocation = f"{WALL_TOOL} --workflow {workflow.id}"
        if not any(invocation in str(step.get("run", "")) for step in aggregator["steps"]):
            problems.append(
                f"{label}: `{workflow.aggregator}` never runs `{invocation}`, so the budget "
                "is declared and enforced by nothing"
            )
    return problems


def _report_rows(path: Path) -> dict[str, tuple[int, float]]:
    """A per-file test-cost report as {file: (tests, seconds)}."""
    document: Any = json.loads(path.read_text(encoding="utf-8"))
    rows = document.get("files") if isinstance(document, dict) else document
    if not isinstance(rows, list):
        raise BudgetError(f"{path} is not a list of {{file, tests, seconds}} rows")
    return {str(row["file"]): (int(row["tests"]), float(row["seconds"])) for row in rows}


def attribute_files(before: Path, after: Path) -> list[str]:
    """The `attribution:` block, and the added test cost, from two per-file reports."""
    old, new = _report_rows(before), _report_rows(after)
    rows = sorted(
        ((name, old.get(name, (0, 0.0))[1], new.get(name, (0, 0.0))[1]) for name in new),
        key=lambda row: row[2] - row[1],
        reverse=True,
    )
    added = [name for name in new if name not in old]
    lines = [
        f"added test files: {len(added)}, {sum(new[name][0] for name in added)} tests, "
        f"{sum(new[name][1] for name in added):.1f} test-seconds",
        f"all files: {sum(t for t, _ in old.values())} -> {sum(t for t, _ in new.values())} "
        f"tests, {sum(s for _, s in old.values()):.1f} -> {sum(s for _, s in new.values()):.1f} "
        "test-seconds",
        "attribution:",
        "  cause: >-",
        "    NAME THE CAUSE",
        "  unit: test-seconds",
        f"  source: per-file reports {before.name} and {after.name}",
        "  grew:",
    ]
    lines.extend(
        f"  - {{name: {name!r}, before: {was:.2f}, after: {now:.2f}}}"
        for name, was, now in rows[:ATTRIBUTED_FILES]
        if now > was
    )
    return lines


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check the gate's cost register.")
    parser.add_argument("--attribute-files", nargs=2, type=Path, metavar=("BEFORE", "AFTER"))
    arguments = parser.parse_args(argv)
    try:
        if arguments.attribute_files:
            print("\n".join(attribute_files(*arguments.attribute_files)))
            return 0
        register = load(REGISTER)
    except (BudgetError, OSError, KeyError, ValueError) as error:
        print(f"gate budgets: {error}", file=sys.stderr)
        return 1
    tiers = pull_request_tiers()
    ratchets, grandfathered = ratchet_problems(register)
    problems = (
        coverage_problems(register)
        + declaration_problems(register)
        + documentation_problems(register)
        + unrecorded_problems(register, tiers)
        + ratchets
        + wall_problems()
    )
    if problems:
        for problem in problems:
            print(f"gate budgets: {problem}", file=sys.stderr)
        return 1
    for note in grandfathered:
        print(f"note: {note}")
    recorded = sum(1 for tier in register.tiers if tier.measured_seconds is not None)
    print(
        f"gate budget declaration passed: {len(register.tiers)} tiers, {recorded} with a "
        f"recorded cost, all ceilings within {register.policy.max_headroom:g}x of it, every "
        f"pull-request tier ({', '.join(sorted(tiers))}) recorded from hosted runs, no "
        "unattributed rise, the pull-request walls inside OR-14 and wired, all named in "
        f"{GUIDE.name}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
