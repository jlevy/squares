"""The gate's declared cost, as data the gate reads rather than prose beside a constant.

`validate.py` carried its own baseline in a docstring -- "Measured on 2026-08-30:
`--fast` is 499s" -- next to a 1800s cap. Six days later the same tier cost 1369.60s on
CI and nothing objected, because 1370 is inside 1800 and because 499 is prose.

The failure is not that the cap was missing. It is that the cap had 3.61x of headroom
over the only measurement anyone had, and a ceiling with 3.61x of headroom cannot detect
a 2.65x regression. So this module enforces the *relationship* between the declared
ceiling and the recorded cost, not just the ceiling:

* `declaration_problems` is static. It reads `devtools/gate-budgets.yaml` and nothing
  else, needs no clock, and fails a ceiling that has drifted more than `max_headroom`
  above the tier's own recorded cost. Run on 2026-08-30's numbers it fails immediately,
  which is the whole claim of this file.
* `judge` is dynamic. It compares one finished run's wall against the same register and
  fails a run over the ceiling, a run that has drifted above the record, or a run far
  enough under the record that the record is the thing that is now wrong.
* `ratchet_problems` is static too, and it exists because the drift rule was defeated
  without being broken. Between 2026-09-06 and 2026-09-09 `suite` tripped 1.5x three
  times and each time its record was re-based to the new reading -- 102.83, 162.62,
  118.72, 183.44 s -- with the ceiling following at 205, 260, 237 and 275 s. Every step
  cited a real hosted reading and 2.4x of growth went through. So a record keeps its
  history in the register, and a record that rises past `max_unattributed_rise` of the
  lowest record since the last attributed one must carry an attribution: the per-step
  or per-file costs that grew, and a named cause.

Bounding the record from both sides is what stops a person having to remember it. The
figure to write is printed by the run that discovers it.

Nothing here prints or exits; `sqpack.cli.validate` renders the verdict and
`devtools.check_gate_budgets` is the static check's command surface.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from sqpack.project import configured_project_root
from sqpack.yamlio import safe_load

BUDGETS = configured_project_root() / "devtools/gate-budgets.yaml"
#: How many of the slowest steps a verdict names. One is usually the whole story -- the
#: 2026-09-05 regression was 96.7 per cent one step -- but a tier that grew in two places
#: should say so rather than blame the larger half.
NAMED_STEP_COUNT = 3
#: Below this share of the tier, a step is not what made the tier slow and naming it
#: would point the reader at the wrong file.
NAMED_STEP_MIN_SHARE = 0.05


class BudgetError(ValueError):
    """The tier register is missing, malformed, or internally inconsistent."""


@dataclass(frozen=True)
class Reference:
    """The run shape a tier's recorded cost was measured at.

    Wall time is not comparable across machines, so the ratio rules enforce only on a run
    that matches this. Every other run is measured and reported and never failed, because
    a check that fails on a slow runner is a check people turn off.
    """

    jobs: int
    inner_jobs: int
    cpus: int
    """How many CPUs the machine that set the record had.

    Matching `--jobs` alone is not enough: a one-core box asked for two jobs runs the same
    flags two to three times slower, and enforcing a ceiling there would fail a run for
    the machine rather than for the change. This is the field that keeps the ratio rules
    on the runner they were measured for."""

    def matches(self, *, jobs: int, inner_jobs: int, cpus: int) -> bool:
        return self.jobs == jobs and self.inner_jobs == inner_jobs and self.cpus == cpus

    def describe(self) -> str:
        return f"{self.cpus} cpus, --jobs {self.jobs} --inner-jobs {self.inner_jobs}"


@dataclass(frozen=True)
class Growth:
    """One step's or one test file's cost before and after a record moved."""

    name: str
    before: float
    after: float


@dataclass(frozen=True)
class Attribution:
    """Why a record rose: what grew, by how much, measured where, and the named cause."""

    cause: str
    unit: str
    source: str
    grew: tuple[Growth, ...]


@dataclass(frozen=True)
class Record:
    """One recorded cost in a tier's history, oldest first, the current record last."""

    seconds: float
    on: str
    where: str | None = None
    attribution: Attribution | None = None


@dataclass(frozen=True)
class TierBudget:
    """One tier's declared ceiling and the cost that justifies it."""

    id: str
    command: str
    ceiling_seconds: float
    reference: Reference
    argument: str
    measured_seconds: float | None = None
    measured_on: str | None = None
    measured_where: str | None = None
    #: Superseded records, oldest first. A cleared record leaves its history in place.
    history: tuple[Record, ...] = ()
    #: Why the current record is higher than the records before it, when it is.
    attribution: Attribution | None = None

    @property
    def records(self) -> tuple[Record, ...]:
        """Every record this tier has held, oldest first, ending with the current one."""
        if self.measured_seconds is None or self.measured_on is None:
            return self.history
        current = Record(
            self.measured_seconds, self.measured_on, self.measured_where, self.attribution
        )
        return (*self.history, current)

    @property
    def headroom(self) -> float | None:
        """How many times its own recorded cost this tier's ceiling sits at."""
        if self.measured_seconds is None:
            return None
        return self.ceiling_seconds / self.measured_seconds


@dataclass(frozen=True)
class Policy:
    """The bands every tier is held to, so no tier can quietly declare its own."""

    max_headroom: float
    drift_ratio: float
    stale_ratio: float
    min_wall_seconds: float
    #: How far a record may rise above the lowest record since its last attributed one
    #: before it must say what grew. `None` only in a register that predates the rule.
    max_unattributed_rise: float | None = None
    #: Records dated before this are history the rule did not exist for: shown, not failed.
    attribution_required_from: str | None = None


@dataclass(frozen=True)
class Register:
    """The whole declaration: one policy, and one entry per selectable tier."""

    policy: Policy
    tiers: tuple[TierBudget, ...]
    path: Path | None = None

    def tier(self, tier_id: str) -> TierBudget | None:
        return next((tier for tier in self.tiers if tier.id == tier_id), None)

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(tier.id for tier in self.tiers)


@dataclass(frozen=True)
class Verdict:
    """What one run's wall says about the tier it ran.

    `status` is the only field callers need to branch on. `failures` carries the reasons,
    each already naming the step that spent the time; `notes` carries what was measured
    but deliberately not enforced.
    """

    tier: str | None
    wall_seconds: float
    status: Literal["passed", "failed", "reported", "unknown"]
    enforced: bool = False
    ceiling_seconds: float | None = None
    measured_seconds: float | None = None
    failures: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    top_steps: tuple[tuple[str, float], ...] = field(default=())

    @property
    def failed(self) -> bool:
        return self.status == "failed"


def _require_mapping(value: object, what: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise BudgetError(f"{what} must be a mapping, found {type(value).__name__}")
    return value


def _positive(value: object, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise BudgetError(f"{what} must be a number, found {value!r}")
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise BudgetError(f"{what} must be positive and finite, found {number!r}")
    return number


def _optional_positive(value: object, what: str) -> float | None:
    return None if value is None else _positive(value, what)


def _text(value: object, what: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BudgetError(f"{what} must be a non-empty string, found {value!r}")
    return value.strip()


def _optional_text(value: object, what: str) -> str | None:
    return None if value is None else _text(value, what)


ATTRIBUTION_UNITS = ("step-seconds", "test-seconds", "job-seconds")


def _attribution_from(raw: object, where: str) -> Attribution | None:
    if raw is None:
        return None
    entry = _require_mapping(raw, where)
    unit = _text(entry.get("unit"), f"{where}.unit")
    if unit not in ATTRIBUTION_UNITS:
        raise BudgetError(f"{where}.unit is {unit!r}; expected one of {ATTRIBUTION_UNITS}")
    raw_grew = entry.get("grew")
    if not isinstance(raw_grew, list) or not raw_grew:
        raise BudgetError(
            f"{where}.grew must name the steps or files that grew; a cause with no costs is "
            "a story, not an attribution"
        )
    grew: list[Growth] = []
    for position, item in enumerate(raw_grew):
        row = _require_mapping(item, f"{where}.grew[{position}]")
        before = row.get("before")
        if isinstance(before, bool) or not isinstance(before, (int, float)) or before < 0:
            raise BudgetError(
                f"{where}.grew[{position}].before must be a cost, found {before!r}"
            )
        grew.append(
            Growth(
                name=_text(row.get("name"), f"{where}.grew[{position}].name"),
                before=float(before),
                after=_positive(row.get("after"), f"{where}.grew[{position}].after"),
            )
        )
    if sum(item.after - item.before for item in grew) <= 0:
        raise BudgetError(f"{where}.grew names no growth, so it attributes no rise")
    return Attribution(
        cause=_text(entry.get("cause"), f"{where}.cause"),
        unit=unit,
        source=_text(entry.get("source"), f"{where}.source"),
        grew=tuple(grew),
    )


def _history_from(raw: object, where: str) -> tuple[Record, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise BudgetError(f"{where}.history must be a list of superseded records")
    records: list[Record] = []
    for position, item in enumerate(raw):
        entry = _require_mapping(item, f"{where}.history[{position}]")
        records.append(
            # The same three keys the current record uses, so a record moves into history
            # by being cut and pasted rather than retyped.
            Record(
                seconds=_positive(
                    entry.get("measured_seconds"),
                    f"{where}.history[{position}].measured_seconds",
                ),
                on=_text(entry.get("measured_on"), f"{where}.history[{position}].measured_on"),
                where=_optional_text(
                    entry.get("measured_where"), f"{where}.history[{position}].measured_where"
                ),
                attribution=_attribution_from(
                    entry.get("attribution"), f"{where}.history[{position}].attribution"
                ),
            )
        )
    return tuple(records)


def _tier_from(raw: object, index: int) -> TierBudget:
    entry = _require_mapping(raw, f"tiers[{index}]")
    tier_id = _text(entry.get("id"), f"tiers[{index}].id")
    where = f"tier {tier_id!r}"
    reference = _require_mapping(entry.get("reference"), f"{where}.reference")
    measured = _optional_positive(entry.get("measured_seconds"), f"{where}.measured_seconds")
    measured_on = _optional_text(entry.get("measured_on"), f"{where}.measured_on")
    if (measured is None) != (measured_on is None):
        raise BudgetError(
            f"{where} records a cost without a date or a date without a cost; a "
            "measurement nobody can place is not a measurement"
        )
    return TierBudget(
        id=tier_id,
        command=_text(entry.get("command"), f"{where}.command"),
        ceiling_seconds=_positive(entry.get("ceiling_seconds"), f"{where}.ceiling_seconds"),
        reference=Reference(
            jobs=int(_positive(reference.get("jobs"), f"{where}.reference.jobs")),
            inner_jobs=int(
                _positive(reference.get("inner_jobs"), f"{where}.reference.inner_jobs")
            ),
            cpus=int(_positive(reference.get("cpus"), f"{where}.reference.cpus")),
        ),
        argument=_text(entry.get("argument"), f"{where}.argument"),
        measured_seconds=measured,
        measured_on=measured_on,
        measured_where=_optional_text(entry.get("measured_where"), f"{where}.measured_where"),
        history=_history_from(entry.get("history"), where),
        attribution=_attribution_from(entry.get("attribution"), f"{where}.attribution"),
    )


def load(path: Path | None = None) -> Register:
    """Read the tier register, refusing anything a rule could not be applied to."""
    source = BUDGETS if path is None else path
    try:
        text = source.read_text(encoding="utf-8")
    except OSError as error:
        raise BudgetError(f"the tier register is unreadable at {source}: {error}") from error
    document = _require_mapping(safe_load(text), str(source))
    policy_entry = _require_mapping(document.get("policy"), "policy")
    policy = Policy(
        max_headroom=_positive(policy_entry.get("max_headroom"), "policy.max_headroom"),
        drift_ratio=_positive(policy_entry.get("drift_ratio"), "policy.drift_ratio"),
        stale_ratio=_positive(policy_entry.get("stale_ratio"), "policy.stale_ratio"),
        min_wall_seconds=_positive(
            policy_entry.get("min_wall_seconds"), "policy.min_wall_seconds"
        ),
        max_unattributed_rise=_optional_positive(
            policy_entry.get("max_unattributed_rise"), "policy.max_unattributed_rise"
        ),
        attribution_required_from=_optional_text(
            policy_entry.get("attribution_required_from"), "policy.attribution_required_from"
        ),
    )
    raw_tiers = document.get("tiers")
    if not isinstance(raw_tiers, list) or not raw_tiers:
        raise BudgetError("tiers must be a non-empty list")
    tiers = tuple(_tier_from(raw, index) for index, raw in enumerate(raw_tiers))
    duplicates = sorted({tier.id for tier in tiers if [t.id for t in tiers].count(tier.id) > 1})
    if duplicates:
        raise BudgetError(f"tiers declared more than once: {', '.join(duplicates)}")
    return Register(policy=policy, tiers=tiers, path=source)


def declaration_problems(register: Register) -> list[str]:
    """Everything wrong with the declaration itself, with no clock involved.

    This is the check that would have fired on 2026-08-30. It needs no run, so it cannot
    be noisy and cannot be blamed on a busy runner, and it is the reason a ceiling here
    cannot quietly grow slack the way `FAST_SUITE_BUDGET_SECONDS` did.
    """
    policy = register.policy
    problems: list[str] = []
    if policy.stale_ratio >= 1.0:
        problems.append(
            f"policy.stale_ratio is {policy.stale_ratio:g}; a floor at or above the "
            "recorded cost fails every honest run"
        )
    if policy.drift_ratio <= 1.0:
        problems.append(
            f"policy.drift_ratio is {policy.drift_ratio:g}; a ceiling at or below the "
            "recorded cost fails every honest run"
        )
    if policy.max_headroom < policy.drift_ratio:
        problems.append(
            f"policy.max_headroom ({policy.max_headroom:g}) is below policy.drift_ratio "
            f"({policy.drift_ratio:g}); the ceiling would fail before the drift rule "
            "could name what moved"
        )
    for tier in register.tiers:
        measured = tier.measured_seconds
        headroom = tier.headroom
        if measured is None or headroom is None:
            continue
        if headroom > policy.max_headroom:
            allowed = measured * policy.max_headroom
            problems.append(
                f"tier {tier.id!r}: the ceiling is {tier.ceiling_seconds:g}s against a "
                f"recorded {measured:g}s, which is {headroom:.2f}x of headroom where "
                f"policy.max_headroom allows {policy.max_headroom:g}x. A ceiling this "
                f"slack cannot see a regression smaller than {headroom:.2f}x. Tighten "
                f"ceiling_seconds to {allowed:.0f} or record why the tier needs it."
            )
        if tier.ceiling_seconds < measured:
            problems.append(
                f"tier {tier.id!r}: the ceiling is {tier.ceiling_seconds:g}s and the "
                f"recorded cost is {measured:g}s, so the tier is declared to fail every "
                "time it runs"
            )
    return problems


def rise_findings(
    label: str, records: tuple[Record, ...], policy: Policy
) -> tuple[list[str], list[str]]:
    """(problems, grandfathered) for one record history: the ratchet rule.

    Each record is compared with the lowest record since the last attributed one, not only
    with its predecessor, so a ratchet of small steps adds up the way the large one did. A
    fall needs no attribution; a rise past `max_unattributed_rise` does. An attributed
    record starts the comparison afresh from itself.

    A rise dated before `attribution_required_from` is returned in the second list rather
    than the first: the register shows it, the rule did not exist for it, and it stays a
    baseline for what comes after.
    """
    problems: list[str] = []
    grandfathered: list[str] = []
    ratio = policy.max_unattributed_rise
    if ratio is None:
        return [
            f"{label}: policy.max_unattributed_rise is not declared, so no rise is checked"
        ], []
    for earlier, later in itertools.pairwise(records):
        if later.on < earlier.on:
            problems.append(
                f"{label}: the record of {later.on} follows one of {earlier.on}; history is "
                "oldest first, or no rise in it can be read"
            )
    base = 0
    for index in range(1, len(records)):
        record = records[index]
        if records[index - 1].attribution is not None:
            base = index - 1
        floor = min(earlier.seconds for earlier in records[base:index])
        rise = record.seconds / floor
        if rise <= ratio or record.attribution is not None:
            continue
        finding = (
            f"{label}: {record.seconds:g}s on {record.on} is {rise:.2f}x the lowest record "
            f"since the last attributed one ({floor:g}s), where {ratio:g}x is the most a "
            "record may rise without naming the per-step or per-file costs that grew and why"
        )
        required = policy.attribution_required_from
        if required is not None and record.on < required:
            grandfathered.append(f"{finding} -- dated before {required}, so shown, not failed")
        else:
            problems.append(
                f"{finding}. Add an `attribution:` block (devtools.read_tier_walls)"
            )
    return problems, grandfathered


def ratchet_problems(register: Register) -> tuple[list[str], list[str]]:
    """The ratchet rule over every tier's record history."""
    if register.policy.max_unattributed_rise is None:
        return [
            "policy.max_unattributed_rise is not declared, so no record's rise is checked"
        ], []
    problems: list[str] = []
    grandfathered: list[str] = []
    for tier in register.tiers:
        found, old = rise_findings(f"tier {tier.id!r}", tier.records, register.policy)
        problems.extend(found)
        grandfathered.extend(old)
    return problems, grandfathered


def _named_steps(
    steps: tuple[tuple[str, float], ...], wall: float
) -> tuple[tuple[str, float], ...]:
    ranked = sorted(steps, key=lambda item: item[1], reverse=True)[:NAMED_STEP_COUNT]
    if wall <= 0:
        return tuple(ranked)
    return tuple(item for item in ranked if item[1] / wall >= NAMED_STEP_MIN_SHARE) or tuple(
        ranked[:1]
    )


def _attribution(steps: tuple[tuple[str, float], ...], wall: float) -> str:
    """The sentence that makes a slow tier actionable: which step, and how much of it."""
    named = _named_steps(steps, wall)
    if not named:
        return "no step timings were captured, so the tier cannot be attributed"
    parts = [
        f"{name!r} is {seconds:.1f}s of it ({seconds / wall:.1%})"
        if wall > 0
        else f"{name!r} is {seconds:.1f}s"
        for name, seconds in named
    ]
    return "; ".join(parts)


def judge(
    register: Register,
    tier_id: str | None,
    *,
    wall_seconds: float,
    steps: tuple[tuple[str, float], ...] = (),
    jobs: int,
    inner_jobs: int,
    cpus: int,
    force: bool = False,
) -> Verdict:
    """Compare one finished run against the register.

    `tier_id` is `None` for a scoped run -- `--only`, or `--since` narrowing a tier --
    because a subset of a tier has no declared cost and pretending otherwise is how a
    ceiling gets waived by accident.
    """
    top = _named_steps(steps, wall_seconds)
    if tier_id is None:
        return Verdict(
            tier=None,
            wall_seconds=wall_seconds,
            status="unknown",
            notes=(
                (
                    "this run is a subset of a tier, so no declared ceiling applies; "
                    f"{_attribution(steps, wall_seconds)}"
                ),
            ),
            top_steps=top,
        )
    tier = register.tier(tier_id)
    if tier is None:
        return Verdict(
            tier=tier_id,
            wall_seconds=wall_seconds,
            status="unknown",
            notes=(f"no ceiling is declared for tier {tier_id!r} in {register.path}",),
            top_steps=top,
        )

    enforced = force or tier.reference.matches(jobs=jobs, inner_jobs=inner_jobs, cpus=cpus)
    policy = register.policy
    failures: list[str] = []
    notes: list[str] = []
    attribution = _attribution(steps, wall_seconds)

    if wall_seconds > tier.ceiling_seconds:
        failures.append(
            f"the {tier.id} tier ran {wall_seconds:.1f}s against a "
            f"{tier.ceiling_seconds:g}s ceiling: {attribution}"
        )
    measured = tier.measured_seconds
    if measured is None:
        notes.append(
            f"no cost is recorded for the {tier.id} tier at {tier.reference.describe()}; "
            f"write `measured_seconds: {wall_seconds:.1f}` into {register.path} to arm the "
            "drift rule"
        )
    elif wall_seconds < policy.min_wall_seconds:
        notes.append(
            f"{wall_seconds:.1f}s is under the {policy.min_wall_seconds:g}s noise floor, so "
            "the drift and stale rules were not applied"
        )
    else:
        if wall_seconds > policy.drift_ratio * measured:
            failures.append(
                f"the {tier.id} tier ran {wall_seconds:.1f}s against a recorded "
                f"{measured:g}s ({wall_seconds / measured:.2f}x, where "
                f"{policy.drift_ratio:g}x fails): {attribution}"
            )
        if wall_seconds < policy.stale_ratio * measured:
            tightened = min(tier.ceiling_seconds, wall_seconds * policy.max_headroom)
            failures.append(
                f"the {tier.id} tier ran {wall_seconds:.1f}s against a recorded "
                f"{measured:g}s, which is {wall_seconds / measured:.2f}x. The record is "
                f"stale in the flattering direction, which is how a ceiling stops "
                f"detecting anything. Write `measured_seconds: {wall_seconds:.1f}` and "
                f"`ceiling_seconds: {tightened:.0f}` into {register.path}."
            )

    if failures and not enforced:
        notes.extend(failures)
        notes.append(
            f"this run was {cpus} cpus, {jobs} jobs, {inner_jobs} inner jobs; the "
            f"{tier.id} tier's band is declared for {tier.reference.describe()}, so the "
            "run above is reported and not failed. Re-run with --enforce-budget to fail "
            "on it."
        )
        return Verdict(
            tier=tier.id,
            wall_seconds=wall_seconds,
            status="reported",
            enforced=False,
            ceiling_seconds=tier.ceiling_seconds,
            measured_seconds=measured,
            notes=tuple(notes),
            top_steps=top,
        )
    if not enforced:
        notes.append(
            f"within the declared band, but this run's shape ({cpus} cpus, {jobs} jobs, "
            f"{inner_jobs} inner) is not the {tier.id} tier's reference "
            f"({tier.reference.describe()}), so the band was reported and not enforced"
        )
    return Verdict(
        tier=tier.id,
        wall_seconds=wall_seconds,
        status="failed" if failures else ("passed" if enforced else "reported"),
        enforced=enforced,
        ceiling_seconds=tier.ceiling_seconds,
        measured_seconds=measured,
        failures=tuple(failures),
        notes=tuple(notes),
        top_steps=top,
    )


def render(verdict: Verdict) -> list[str]:
    """The `== the tier against its ceiling ==` block, as lines."""
    lines: list[str] = []
    if verdict.ceiling_seconds is None:
        headline = f"  {verdict.wall_seconds:7.2f}s  wall, against no declared ceiling"
    else:
        share = verdict.wall_seconds / verdict.ceiling_seconds
        recorded = (
            f", recorded {verdict.measured_seconds:g}s"
            if verdict.measured_seconds is not None
            else ", never recorded at this shape"
        )
        headline = (
            f"  {verdict.wall_seconds:7.2f}s  wall of a {verdict.ceiling_seconds:g}s "
            f"ceiling ({share:.0%}){recorded}"
        )
    lines.append(headline)
    lines.extend(f"  FAIL: {reason}" for reason in verdict.failures)
    lines.extend(f"  note: {note}" for note in verdict.notes)
    return lines
