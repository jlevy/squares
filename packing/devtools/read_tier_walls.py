#!/usr/bin/env python3
"""Read the gate's own tier verdicts out of hosted job logs, to record or attribute a cost.

`gate-budgets.yaml` records a tier's cost from CI readings at the tier's reference shape,
and until 2026-09-15 those readings were copied out of logs by hand. That is how the
`checks` and `sweeps` entries stayed empty for eight days while the gate printed the line
to write on every run (`think-gsz0`), and how a record came to rest on one reading.

For each named run this lists every job that ran `packing-validate` on a whole tier. The
tier is read from the command the job ran, with the CLI's own parser; the wall comes from
the gate's `== the tier against its ceiling ==` block, which is the figure
`gate_budgets.judge` compared rather than a job wall with setup around it. A reading whose
block says the band was reported and not enforced ran off the tier's reference shape, and
is listed but left out of the mean. Readings are grouped by the gate's own "k of M steps"
count as well as by tier, since a tier that selects different steps is a different tier.
Per group it prints the geometric mean the register's convention asks for and the
`measured_where` text naming every run behind it.

With `--baseline-run-id` it also attributes the change, which is what a raised record
must carry (`check_gate_budgets`' ratchet rule). The log names the eight slowest steps of
each run, so the growth table compares those: a step outside the eight in every run of a
group is shown as 0 there, which bounds it rather than measuring it. The printed
`attribution:` block leaves the cause for a person to name.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.read_tier_walls \
        --run-id 34924677097 --run-id 35013703659 [--tier checks] \
        [--baseline-run-id 34023002068 ...]

It reads logs over the network, so it is not a gate step; `tests/test_read_tier_walls.py`
covers the parsing on a recorded log excerpt. `think-mvyk` is the wider re-record tool
this is the first piece of.
"""

# `_parser` and `_tier_id` are the CLI's own, so the tier is read the way the gate reads
# it rather than by a second parser that could drift. `check_declared_commands` takes the
# same exemption.
# pyright: reportPrivateUsage=false
from __future__ import annotations

import argparse
import math
import re
import shlex
import sys
import time
import urllib.error
import urllib.request
from collections.abc import Sequence
from dataclasses import dataclass, field

from devtools.check_pr_wall import API, USER_AGENT, Client, WallError, github_token
from sqpack.cli.validate import _parser as _validate_parser
from sqpack.cli.validate import _tier_id

COMMAND = re.compile(r"##\[group\]Run .*?(packing-validate(?: .*)?)$")
WALL = re.compile(r"^\s*(?P<wall>[0-9.]+)s  wall of a (?P<ceiling>[0-9.]+)s ceiling")
STEP = re.compile(r"^\s*(?P<seconds>[0-9.]+)s  (?P<name>.+)$")
COUNT = re.compile(r"^(?P<selected>\d+) of (?P<total>\d+) STEPS ")
TIMESTAMP = re.compile(r"^\d{4}-\d\d-\d\dT[0-9:.]+Z ")
UNENFORCED = "reported and not enforced"
TIMINGS = "== where the time went =="
TOTAL = "TOTAL (wall)"
#: Growth rows the attribution block names; the rest are summarised in the table.
ATTRIBUTED_ROWS = 6


@dataclass(frozen=True)
class Reading:
    tier: str
    wall_seconds: float
    enforced: bool
    steps: str
    step_seconds: dict[str, float] = field(default_factory=dict)
    run: int = 0
    job: str = ""


def _tier_of(command: str) -> str | None:
    tokens = shlex.split(command)
    try:
        namespace = _validate_parser().parse_args(tokens[1:])
    except SystemExit:
        return None
    return None if namespace.only or namespace.skip else _tier_id(namespace)


def parse_log(text: str) -> list[Reading]:
    """Every whole-tier verdict the gate printed in one job's log, in order."""
    lines = [TIMESTAMP.sub("", line) for line in text.splitlines()]
    readings: list[Reading] = []
    tier: str | None = None
    timings: dict[str, float] = {}
    in_timings = False
    for index, line in enumerate(lines):
        command = COMMAND.search(line)
        if command:
            tier, timings = _tier_of(command.group(1)), {}
            continue
        if line.strip() == TIMINGS:
            in_timings, timings = True, {}
            continue
        step = STEP.match(line) if in_timings else None
        if step:
            if step.group("name") == TOTAL:
                in_timings = False
            else:
                timings[step.group("name")] = float(step.group("seconds"))
            continue
        wall = WALL.match(line)
        if not wall or tier is None:
            continue
        notes: list[str] = []
        steps = "unknown"
        for following in lines[index + 1 :]:
            counted = COUNT.match(following)
            if counted:
                steps = f"{counted.group('selected')} of {counted.group('total')}"
                break
            notes.append(following)
        readings.append(
            Reading(
                tier=tier,
                wall_seconds=float(wall.group("wall")),
                enforced=not any(UNENFORCED in note for note in notes),
                steps=steps,
                step_seconds=dict(timings),
            )
        )
    return readings


def geometric_mean(values: Sequence[float]) -> float:
    return math.exp(sum(math.log(value) for value in values) / len(values))


def step_means(readings: Sequence[Reading]) -> dict[str, float]:
    """Each listed step's geometric mean over the readings that list it."""
    names = {name for reading in readings for name in reading.step_seconds}
    return {
        name: geometric_mean(
            [reading.step_seconds[name] for reading in readings if name in reading.step_seconds]
        )
        for name in names
    }


def growth(
    before: Sequence[Reading], after: Sequence[Reading]
) -> list[tuple[str, float, float]]:
    """(step, before, after) for every listed step, largest growth first."""
    old, new = step_means(before), step_means(after)
    rows = [(name, old.get(name, 0.0), new.get(name, 0.0)) for name in {*old, *new}]
    return sorted(rows, key=lambda row: row[2] - row[1], reverse=True)


def _log(client: Client, job_id: int) -> str:
    """A job's log. The API redirects to storage, which must not receive the API token."""
    request = urllib.request.Request(
        f"{API}/repos/{client.repository}/actions/jobs/{job_id}/logs",
        headers={"User-Agent": USER_AGENT},
    )
    if client.token:
        request.add_unredirected_header("Authorization", f"Bearer {client.token}")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read().decode("utf-8", errors="replace")
        except (urllib.error.URLError, ConnectionError) as error:
            if attempt == 2:
                raise WallError(f"the log of job {job_id} is unreadable: {error}") from error
            time.sleep(2.0 * (attempt + 1))
    raise WallError(f"the log of job {job_id} is unreadable")  # pragma: no cover


def _collect(client: Client, run_ids: Sequence[int], tiers: Sequence[str]) -> list[Reading]:
    readings: list[Reading] = []
    for run_id in run_ids:
        for job in client.jobs(run_id):
            if job.get("conclusion") != "success":
                continue
            for parsed in parse_log(_log(client, int(job["id"]))):
                if tiers and parsed.tier not in tiers:
                    continue
                reading = Reading(**{**parsed.__dict__, "run": run_id, "job": str(job["name"])})
                readings.append(reading)
                shape = "" if reading.enforced else "  (off the reference shape; not averaged)"
                print(
                    f"run {run_id} job {reading.job}: {reading.tier} "
                    f"{reading.wall_seconds:.2f}s, {reading.steps} steps{shape}"
                )
    return readings


def _groups(readings: Sequence[Reading]) -> dict[tuple[str, str], list[Reading]]:
    grouped: dict[tuple[str, str], list[Reading]] = {}
    for reading in readings:
        if reading.enforced:
            grouped.setdefault((reading.tier, reading.steps), []).append(reading)
    return grouped


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read tier walls out of hosted job logs.")
    parser.add_argument("--run-id", type=int, action="append", required=True)
    parser.add_argument("--baseline-run-id", type=int, action="append", default=[])
    parser.add_argument("--tier", action="append", default=[], help="only these tiers")
    parser.add_argument("--repo", default="jlevy/squares")
    arguments = parser.parse_args(argv)
    client = Client(arguments.repo, github_token())
    try:
        readings = _collect(client, arguments.run_id, arguments.tier)
        baseline = _collect(client, arguments.baseline_run_id, arguments.tier)
    except WallError as error:
        print(f"read_tier_walls: {error}", file=sys.stderr)
        return 2
    for (tier, steps), counted in sorted(_groups(readings).items()):
        walls = [item.wall_seconds for item in counted]
        listed = ", ".join(f"{wall:.2f}" for wall in walls)
        runs = ", ".join(str(item.run) for item in counted)
        print(
            f"\n{tier} ({steps} steps): measured_seconds {geometric_mean(walls):.2f}, the "
            f"geometric mean of {len(walls)} readings at the reference shape -- {listed} -- "
            f"across runs {runs}. Observed spread {max(walls) / min(walls):.2f}x."
        )
        before = [item for item in baseline if item.tier == tier and item.enforced]
        if not before:
            continue
        old = geometric_mean([item.wall_seconds for item in before])
        print(
            f"  against {len(before)} baseline readings, geometric mean {old:.2f}s: "
            f"{geometric_mean(walls) / old:.2f}x. Listed steps, largest growth first:"
        )
        rows = growth(before, counted)
        for name, was, now in rows:
            print(f"    {now - was:+8.2f}s  {was:7.2f}s -> {now:7.2f}s  {name}")
        print("  attribution:\n    cause: >-\n      NAME THE CAUSE\n    unit: step-seconds")
        print(
            "    source: read_tier_walls --baseline-run-id "
            + " ".join(str(item.run) for item in before)
            + " --run-id "
            + " ".join(str(item.run) for item in counted)
        )
        print("    grew:")
        for name, was, now in [row for row in rows if row[2] > row[1]][:ATTRIBUTED_ROWS]:
            print(f"    - {{name: {name!r}, before: {was:.2f}, after: {now:.2f}}}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
