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

A tier whose hosted walls are a distribution rather than a point may also record its
`measured_band`: the lowest and highest readings seen at its reference shape. The
policy's ratios stay the policy's; the band only moves what they are measured against,
so the stale rule reads the band's low edge and the drift rule its high edge. That is
`think-be1s`'s answer to D-472. On 2026-09-29 the `geometry` tier read 110 to 116 s on
eleven hosted runs and 58.75 to 70.50 s on the next three, on unchanged steps, and no
single record can hold both regimes inside 0.6x and 1.5x.

Hosted pull-request cost findings may be declared advisory under tracked policy:
record-relative findings under `pull_request_relative_rules`, and completed-run ceiling
findings under `pull_request_ceiling`. Both stay computed, printed and annotated; the
tracker owns replacing uncontrolled runner walls with attributable measurements. On
2026-09-30 unchanged code varied 2.0 to 2.3x across hosted draws. By 2026-10-10 a completed
399s frontend run with all 408 tests and four HTTP budgets passing was being called a
hang solely because it exceeded twice a 165s cost ceiling. A finished run's wall cannot
establish that it hung. Actual subprocess deadlines and the retained per-test guard
bound hangs; main, scheduled and explicit `--enforce-budget` runs keep cost enforcement.

A tier that has never been read at its reference shape may say so instead of leaving its
record empty without comment. `pending_measurement` names the bead that owns the first
reading and `pending_until` the last day the tier may go without one; the two come
together, and neither may sit beside `measured_seconds`, `measured_on`, `measured_where`
or `measured_band`, so a forecast cannot pass for a reading. Nothing in `judge` reads
either: the ceiling applies from the first run, and the drift and stale rules have no
record to be relative to. `devtools.check_gate_budgets` is what holds the date and the
bead, and only for a tier a pull request runs, where an empty record otherwise fails.

Nothing here prints or exits; `sqpack.cli.validate` renders the verdict and
`devtools.check_gate_budgets` is the static check's command surface.
"""

from __future__ import annotations

import itertools
import math
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Any, Literal

import yaml

from sqpack.project import configured_project_root
from sqpack.yamlio import load_yaml

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
    #: The lowest and highest readings at the reference shape, for a tier whose walls are
    #: a distribution: the stale rule reads the low edge and the drift rule the high one.
    measured_band: tuple[float, float] | None = None
    #: The bead that owns the first reading of a tier with no record yet. A forecast is
    #: not data, so this never sits beside a current record; the ceiling applies meanwhile.
    pending_measurement: str | None = None
    #: The last day the tier may go unrecorded under `pending_measurement`. Required with
    #: it, so the allowance ends on a date and not when somebody remembers.
    pending_until: date | None = None

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


#: What the two record-relative rules do on a hosted pull-request run. Absent means
#: `enforcing`, the way an absent `enforcement` on a pull-request wall does.
RELATIVE_ENFORCEMENT = ("enforcing", "advisory")
#: A bead alias, the only thing a relaxed rule may name as its tracker: the shape
#: `check_pr_wall` requires of an advisory wall, for the same reason a reporting-only CI
#: gate requires it below. A relaxation with no bead behind it is a permanent one.
TRACKING_BEAD = r"think-[a-z0-9]{4}"


@dataclass(frozen=True)
class Advisory:
    """A relaxation that names the work that ends it.

    Carried on the verdict as well as the policy so every rendering of an advisory finding
    can say which bead it is advisory under and why.
    """

    tracking_bead: str
    reason: str
    #: What is relaxed, and what still fails a pull-request run under the relaxation, as
    #: the sentence `advisory_note` renders. The defaults are the drift and stale rules'.
    rules: str = "the drift and stale rules"
    still_fails: str = "Functional failures and subprocess timeouts remain enforced."


@dataclass(frozen=True)
class CeilingAdvisory:
    """Completed-run cost advisory on pull requests, retaining the per-test guard.

    Subprocess deadlines detect commands that fail to finish. A finished tier's wall
    remains cost evidence regardless of its ratio to the recorded ceiling.
    """

    advisory: Advisory
    per_test_hang_seconds: float


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
    #: Set when the register declares the drift and stale rules advisory on hosted
    #: pull-request runs; None is enforcing. The ceiling is outside this.
    pull_request_relative_rules: Advisory | None = None
    #: Set when the register declares the ceiling, and the per-test call-wall rule,
    #: advisory on hosted pull-request runs, retaining command/per-test guards; None
    #: is enforcing.
    pull_request_ceiling: CeilingAdvisory | None = None


@dataclass(frozen=True)
class Register:
    """The whole declaration: one policy, and one entry per selectable tier."""

    policy: Policy
    tiers: tuple[TierBudget, ...]
    path: Path | None = None
    #: The CI gates whose hosted jobs are clocked by the same rules (`OR-17`). Empty in a
    #: register that predates them, which is why it has a default.
    ci_gates: tuple[CiGate, ...] = ()

    def tier(self, tier_id: str) -> TierBudget | None:
        return next((tier for tier in self.tiers if tier.id == tier_id), None)

    def ci_gate(self, gate_id: str) -> CiGate | None:
        return next((gate for gate in self.ci_gates if gate.id == gate_id), None)

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(tier.id for tier in self.tiers)


@dataclass(frozen=True)
class Verdict:
    """What one run's wall says about the tier it ran.

    `status` is the only field callers need to branch on. `failures` carries the reasons,
    each already naming the step that spent the time; `notes` carries what was measured
    but deliberately not enforced. `advisory_failures` are findings of a rule the register
    has declared advisory for this run: real, printed word for word, and not what the run
    is failed for. `advisory` says under which bead, and why.
    """

    tier: str | None
    wall_seconds: float
    status: Literal["passed", "failed", "advisory", "reported", "unknown"]
    enforced: bool = False
    ceiling_seconds: float | None = None
    measured_seconds: float | None = None
    failures: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    top_steps: tuple[tuple[str, float], ...] = field(default=())
    advisory_failures: tuple[str, ...] = ()
    advisory: Advisory | None = None

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


def _positive_integer(value: object, what: str) -> int:
    number = _positive(value, what)
    if not number.is_integer():
        raise BudgetError(f"{what} must be a positive integer, found {value!r}")
    return int(number)


def _optional_positive(value: object, what: str) -> float | None:
    return None if value is None else _positive(value, what)


def _nonnegative(value: object, what: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise BudgetError(f"{what} must be a number, found {value!r}")
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise BudgetError(f"{what} must be non-negative and finite, found {number!r}")
    return number


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
        grew.append(
            Growth(
                name=_text(row.get("name"), f"{where}.grew[{position}].name"),
                before=_nonnegative(row.get("before"), f"{where}.grew[{position}].before"),
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
    pending, pending_until = _pending_from(entry, where)
    if (measured is None) != (measured_on is None):
        raise BudgetError(
            f"{where} records a cost without a date or a date without a cost; a "
            "measurement nobody can place is not a measurement"
        )
    band = _band_from(entry.get("measured_band"), where)
    if band is not None and measured is None:
        raise BudgetError(
            f"{where} records a measured_band without a measured_seconds; a band is the "
            "spread of the readings a record was taken from"
        )
    return TierBudget(
        id=tier_id,
        command=_text(entry.get("command"), f"{where}.command"),
        ceiling_seconds=_positive(entry.get("ceiling_seconds"), f"{where}.ceiling_seconds"),
        reference=Reference(
            jobs=_positive_integer(reference.get("jobs"), f"{where}.reference.jobs"),
            inner_jobs=_positive_integer(
                reference.get("inner_jobs"), f"{where}.reference.inner_jobs"
            ),
            cpus=_positive_integer(reference.get("cpus"), f"{where}.reference.cpus"),
        ),
        argument=_text(entry.get("argument"), f"{where}.argument"),
        measured_seconds=measured,
        measured_on=measured_on,
        measured_where=_optional_text(entry.get("measured_where"), f"{where}.measured_where"),
        history=_history_from(entry.get("history"), where),
        attribution=_attribution_from(entry.get("attribution"), f"{where}.attribution"),
        measured_band=band,
        pending_measurement=pending,
        pending_until=pending_until,
    )


#: The fields of a current record. A pending tier may carry none of them: its superseded
#: records stay in `history` and its forecast in `argument`.
OBSERVATION_FIELDS = ("measured_seconds", "measured_on", "measured_where", "measured_band")


def _pending_from(entry: dict[str, Any], where: str) -> tuple[str | None, date | None]:
    """A tier's `pending_measurement` and `pending_until`: both, or neither.

    The contract `_ci_job_from` holds a pending hosted job to, plus the date. A tier is
    something a pull request waits on, so its allowance names the day it ends as well as
    the bead that ends it. Whether that day has passed and that bead is live is
    `devtools.check_gate_budgets`' question: this module reads no clock and no bead store.
    """
    pending = _optional_text(entry.get("pending_measurement"), f"{where}.pending_measurement")
    raw_until = entry.get("pending_until")
    if pending is None:
        if raw_until is not None:
            raise BudgetError(
                f"{where}.pending_until requires pending_measurement; a date with no bead "
                "behind it is an allowance nothing tracks"
            )
        return None, None
    if re.fullmatch(TRACKING_BEAD, pending) is None:
        raise BudgetError(
            f"{where}.pending_measurement must name a `think-xxxx` bead, found {pending!r}"
        )
    if raw_until is None:
        raise BudgetError(
            f"{where}.pending_measurement requires pending_until; a pending measurement "
            "with no date is a permanent one"
        )
    observed = [name for name in OBSERVATION_FIELDS if entry.get(name) is not None]
    if observed:
        raise BudgetError(
            f"{where} cannot be pending and measured at once: it names pending_measurement "
            f"beside {', '.join(observed)}. Retain superseded records in history and "
            "estimates in argument"
        )
    return pending, _iso_date(raw_until, f"{where}.pending_until")


def _iso_date(value: object, what: str) -> date:
    """A calendar date, quoted as the register's other dates are or written as YAML's own."""
    refusal = f"{what} must be an ISO date, 'YYYY-MM-DD', found {value!r}"
    if isinstance(value, date) and not isinstance(value, datetime):
        return value
    if not isinstance(value, str):
        raise BudgetError(refusal)
    try:
        return date.fromisoformat(value.strip())
    except ValueError as error:
        raise BudgetError(refusal) from error


def _band_from(raw: object, where: str) -> tuple[float, float] | None:
    if raw is None:
        return None
    entry = _require_mapping(raw, f"{where}.measured_band")
    low = _positive(entry.get("low"), f"{where}.measured_band.low")
    high = _positive(entry.get("high"), f"{where}.measured_band.high")
    if low > high:
        raise BudgetError(f"{where}.measured_band has low {low:g} above high {high:g}")
    return low, high


def _relative_rules_from(raw: object) -> Advisory | None:
    """The drift and stale rules' enforcement on pull requests: None when enforcing.

    The same contract `check_pr_wall` holds an advisory wall to. An advisory declaration
    must name its tracking bead and its reason; an enforcing one may name neither, so a
    relaxation cannot linger half-removed, with the rule back on and a bead still cited.
    """
    where = "policy.pull_request_relative_rules"
    if raw is None:
        return None
    entry = _require_mapping(raw, where)
    enforcement = entry.get("enforcement", "enforcing")
    if enforcement not in RELATIVE_ENFORCEMENT:
        raise BudgetError(
            f"{where}.enforcement must be one of {', '.join(RELATIVE_ENFORCEMENT)}, found "
            f"{enforcement!r}"
        )
    bead, reason = entry.get("tracking_bead"), entry.get("advisory_reason")
    if enforcement == "enforcing":
        stray = [
            name
            for name, value in (("tracking_bead", bead), ("advisory_reason", reason))
            if value is not None
        ]
        if stray:
            raise BudgetError(
                f"{where} is enforcing and still names {', '.join(stray)}; an enforcing "
                "rule names no tracker, so remove them when enforcement returns"
            )
        return None
    if not isinstance(bead, str) or re.fullmatch(TRACKING_BEAD, bead.strip()) is None:
        raise BudgetError(
            f"{where} is advisory and must name the bead tracking its return to "
            f"enforcement as `tracking_bead: think-xxxx`, found {bead!r}"
        )
    if not isinstance(reason, str) or not reason.strip():
        raise BudgetError(
            f"{where} is advisory and must say why in a non-empty advisory_reason, "
            f"found {reason!r}"
        )
    return Advisory(tracking_bead=bead.strip(), reason=" ".join(reason.split()))


def _ceiling_rule_from(raw: object) -> CeilingAdvisory | None:
    """The ceiling's enforcement on pull requests: None when enforcing.

    Advisory cost needs an owner and reason. The retained per-test guard is independent
    of tier cost; an obsolete completed-wall ratio must not silently reinstate it.
    """
    where = "policy.pull_request_ceiling"
    if raw is None:
        return None
    entry = _require_mapping(raw, where)
    if "hang_ratio" in entry:
        raise BudgetError(
            f"{where}.hang_ratio is no longer supported: a completed-run wall cannot "
            "establish a hang; use subprocess deadlines and the per-test guard"
        )
    relaxed = _relative_rules_from(
        {key: entry.get(key) for key in ("enforcement", "tracking_bead", "advisory_reason")}
        | {"enforcement": entry.get("enforcement", "enforcing")}
    )
    per_test = entry.get("per_test_hang_seconds")
    if relaxed is None:
        if per_test is not None:
            raise BudgetError(
                f"{where} is enforcing and still declares a hang detector; remove "
                "per_test_hang_seconds when enforcement returns"
            )
        return None
    per_test_seconds = _positive(per_test, f"{where}.per_test_hang_seconds")
    return CeilingAdvisory(
        advisory=Advisory(
            tracking_bead=relaxed.tracking_bead,
            reason=relaxed.reason,
            rules="the tier ceilings and the per-test call-wall rule",
            still_fails=(
                "Functional failures, subprocess timeouts, explicit timeout caps, and "
                f"test calls of {per_test_seconds:g}s or more still fail a pull-request run."
            ),
        ),
        per_test_hang_seconds=per_test_seconds,
    )


def load(path: Path | None = None) -> Register:
    """Read the tier register, refusing anything a rule could not be applied to."""
    source = BUDGETS if path is None else path
    try:
        text = source.read_text(encoding="utf-8")
    except OSError as error:
        raise BudgetError(f"the tier register is unreadable at {source}: {error}") from error
    try:
        document = _require_mapping(load_yaml(text), str(source))
    except yaml.YAMLError as error:
        raise BudgetError(f"the tier register is invalid YAML at {source}: {error}") from error
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
        pull_request_relative_rules=_relative_rules_from(
            policy_entry.get("pull_request_relative_rules")
        ),
        pull_request_ceiling=_ceiling_rule_from(policy_entry.get("pull_request_ceiling")),
    )
    raw_tiers = document.get("tiers")
    if not isinstance(raw_tiers, list) or not raw_tiers:
        raise BudgetError("tiers must be a non-empty list")
    tiers = tuple(_tier_from(raw, index) for index, raw in enumerate(raw_tiers))
    duplicates = sorted({tier.id for tier in tiers if [t.id for t in tiers].count(tier.id) > 1})
    if duplicates:
        raise BudgetError(f"tiers declared more than once: {', '.join(duplicates)}")
    raw_gates = document.get("ci_gates")
    if raw_gates is not None and not isinstance(raw_gates, list):
        raise BudgetError("ci_gates must be a list of gates, or absent")
    gates = tuple(_ci_gate_from(raw, index) for index, raw in enumerate(raw_gates or []))
    gate_ids = [gate.id for gate in gates]
    repeated = sorted({gate.id for gate in gates if gate_ids.count(gate.id) > 1})
    if repeated:
        raise BudgetError(f"ci gates declared more than once: {', '.join(repeated)}")
    return Register(policy=policy, tiers=tiers, path=source, ci_gates=gates)


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
        problems.extend(band_problems(tier, policy))
    return problems


def band_problems(tier: TierBudget, policy: Policy) -> list[str]:
    """What is wrong with a tier's `measured_band`, read against its record and policy.

    A band moves the edges the policy's ratios are applied to, so it must not become a
    way to switch them off. It must bracket the record it was taken with, and it may be
    no wider than the window the policy already tolerates around a point record
    (`drift_ratio / stale_ratio`). A ceiling under the band's drift edge is not refused:
    the ceiling then binds first, as it may for a point record (`checks`' 140 s ceiling,
    under its band's 205.65 s drift edge, does).

    What a band gives up is sensitivity in its fast regime: a run from the low end can
    grow to the drift edge, `drift_ratio` times the high edge, or to the ceiling if that
    is lower, before any rule fires. That is the price of not failing on which runner a
    job drew, and each banded tier's `measured_where` states its own figure.
    """
    if tier.measured_band is None or tier.measured_seconds is None:
        return []
    low, high = tier.measured_band
    measured = tier.measured_seconds
    label = f"tier {tier.id!r}"
    problems: list[str] = []
    if not low <= measured <= high:
        problems.append(
            f"{label}: measured_band [{low:g}, {high:g}] does not contain the recorded "
            f"{measured:g}s it was taken with"
        )
    window = policy.drift_ratio / policy.stale_ratio
    if high / low > window:
        problems.append(
            f"{label}: measured_band [{low:g}, {high:g}] is {high / low:.2f}x wide, wider "
            f"than the {window:.2f}x window the policy tolerates around a point record "
            "(drift_ratio / stale_ratio), so it would switch the rules off rather than "
            "place them"
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


# ---------------------------------------------------------------------------
# CI gates. The same register, the same four rules, a hosted job's wall instead
# of a local tier's. `OR-17` is why this exists: a tier that leaves the fast
# surface stops being clocked by anything, and the deep gate reached 2674s
# against its own declared 1943.05s with no rule reading either number.
# ---------------------------------------------------------------------------

#: What a CI gate's size verdict does to the run. Absent means `enforcing`.
CI_ENFORCEMENT = ("enforcing", "reporting")
#: A bead alias, the only thing a reporting-only gate may name as its tracker.
CI_TRACKING_BEAD = TRACKING_BEAD


@dataclass(frozen=True)
class CiReference:
    """The runner a CI job's recorded wall was measured on.

    `Reference` pins a local tier to `--jobs`, `--inner-jobs` and a core count. A hosted
    job has none of those to vary: the workflow fixes its flags, so what is left to
    disagree about is the runner label the job asked for. `cpus` is recorded for the
    argument rather than matched, because the jobs API reports the label and not the
    machine behind it.
    """

    runner: str
    cpus: int

    def matches(self, *, runner: str) -> bool:
        return self.runner == runner

    def describe(self) -> str:
        return f"{self.runner}, {self.cpus} cpus"


@dataclass(frozen=True)
class CiJobBudget:
    """One hosted job's declared ceiling and the wall that justifies it.

    Deliberately the same five fields a `pages:` job entry carries, plus the history and
    attribution a `tiers:` entry carries, so the ratchet rule reaches these too.
    """

    id: str
    ceiling_seconds: float
    argument: str
    measured_seconds: float | None = None
    measured_on: str | None = None
    measured_where: str | None = None
    #: Sample max/min across the readings behind `measured_seconds`. The sampler emits
    #: 1.0 for one reading; that arithmetic ratio does not estimate runner variance.
    #: `None` means no sample spread is recorded, as for a pending measurement.
    spread: float | None = None
    history: tuple[Record, ...] = ()
    attribution: Attribution | None = None
    pending_measurement: str | None = None
    """Bead owning the first observation of a new job shape; forecasts are not data."""

    @property
    def records(self) -> tuple[Record, ...]:
        """Every record this job has held, oldest first, ending with the current one."""
        if self.measured_seconds is None or self.measured_on is None:
            return self.history
        current = Record(
            self.measured_seconds, self.measured_on, self.measured_where, self.attribution
        )
        return (*self.history, current)

    @property
    def headroom(self) -> float | None:
        if self.measured_seconds is None:
            return None
        return self.ceiling_seconds / self.measured_seconds


@dataclass(frozen=True)
class CiGate:
    """One workflow's jobs and its whole wall, under one declared band."""

    id: str
    file: str
    aggregate: str
    selected_by: str
    reference: CiReference
    #: The band this gate's walls are held to, in place of `policy.drift_ratio`. A hosted
    #: runner is noisier than the box a local tier is measured on, and the entry says in
    #: the register what spread it was chosen against.
    drift_ratio: float
    enforcement: str
    argument: str
    #: The gate's complete wall, same shape as a job so the same rules apply to it.
    wall: CiJobBudget
    jobs: tuple[CiJobBudget, ...]
    tracking_bead: str | None = None
    reporting_reason: str | None = None

    def job(self, job_id: str) -> CiJobBudget | None:
        return next((job for job in self.jobs if job.id == job_id), None)

    @property
    def ids(self) -> tuple[str, ...]:
        return tuple(job.id for job in self.jobs)

    @property
    def reports_only(self) -> bool:
        return self.enforcement == "reporting"


def _ci_job_from(raw: object, where: str) -> CiJobBudget:
    entry = _require_mapping(raw, where)
    job_id = _text(entry.get("id"), f"{where}.id")
    at = f"{where}[{job_id!r}]"
    measured = _optional_positive(entry.get("measured_seconds"), f"{at}.measured_seconds")
    measured_on = _optional_text(entry.get("measured_on"), f"{at}.measured_on")
    pending = _optional_text(entry.get("pending_measurement"), f"{at}.pending_measurement")
    if pending is not None:
        if re.fullmatch(CI_TRACKING_BEAD, pending) is None:
            raise BudgetError(f"{at}.pending_measurement must name a `think-xxxx` bead")
        if any(
            entry.get(field) is not None
            for field in ("measured_seconds", "measured_on", "measured_where", "spread")
        ):
            raise BudgetError(
                f"{at} has both a pending measurement and current observation fields; "
                "retain predecessor observations in history and estimates in argument"
            )
    if (measured is None) != (measured_on is None):
        raise BudgetError(
            f"{at} records a wall without a date or a date without a wall; a measurement "
            "nobody can place is not a measurement"
        )
    return CiJobBudget(
        id=job_id,
        ceiling_seconds=_positive(entry.get("ceiling_seconds"), f"{at}.ceiling_seconds"),
        argument=_text(entry.get("argument"), f"{at}.argument"),
        measured_seconds=measured,
        measured_on=measured_on,
        measured_where=_optional_text(entry.get("measured_where"), f"{at}.measured_where"),
        spread=_optional_positive(entry.get("spread"), f"{at}.spread"),
        history=_history_from(entry.get("history"), at),
        attribution=_attribution_from(entry.get("attribution"), f"{at}.attribution"),
        pending_measurement=pending,
    )


def _ci_gate_from(raw: object, index: int) -> CiGate:
    entry = _require_mapping(raw, f"ci_gates[{index}]")
    gate_id = _text(entry.get("id"), f"ci_gates[{index}].id")
    where = f"ci gate {gate_id!r}"
    reference = _require_mapping(entry.get("reference"), f"{where}.reference")
    enforcement = _text(entry.get("enforcement"), f"{where}.enforcement")
    if enforcement not in CI_ENFORCEMENT:
        raise BudgetError(f"{where}.enforcement is {enforcement!r}; expected {CI_ENFORCEMENT}")
    bead = _optional_text(entry.get("tracking_bead"), f"{where}.tracking_bead")
    reason = _optional_text(entry.get("reporting_reason"), f"{where}.reporting_reason")
    if enforcement == "reporting" and (bead is None or reason is None):
        raise BudgetError(
            f"{where} reports rather than enforces without naming both a `tracking_bead` "
            "and a `reporting_reason`; a relaxation with no bead behind it is permanent"
        )
    if enforcement == "enforcing" and (bead is not None or reason is not None):
        raise BudgetError(
            f"{where} enforces and still names a reporting tracker; remove it with the "
            "relaxation it tracked"
        )
    if bead is not None and re.fullmatch(CI_TRACKING_BEAD, bead) is None:
        raise BudgetError(f"{where}.tracking_bead is {bead!r}; expected a `think-xxxx` alias")
    raw_jobs = entry.get("jobs")
    if not isinstance(raw_jobs, list) or not raw_jobs:
        raise BudgetError(f"{where}.jobs must be a non-empty list")
    jobs = tuple(_ci_job_from(item, f"{where}.jobs") for item in raw_jobs)
    seen = [job.id for job in jobs]
    duplicates = sorted({job.id for job in jobs if seen.count(job.id) > 1})
    if duplicates:
        raise BudgetError(f"{where} declares jobs more than once: {', '.join(duplicates)}")
    wall = _require_mapping(entry.get("wall"), f"{where}.wall")
    return CiGate(
        id=gate_id,
        file=_text(entry.get("file"), f"{where}.file"),
        aggregate=_text(entry.get("aggregate"), f"{where}.aggregate"),
        selected_by=_text(entry.get("selected_by"), f"{where}.selected_by"),
        reference=CiReference(
            runner=_text(reference.get("runner"), f"{where}.reference.runner"),
            cpus=_positive_integer(reference.get("cpus"), f"{where}.reference.cpus"),
        ),
        drift_ratio=_positive(entry.get("drift_ratio"), f"{where}.drift_ratio"),
        enforcement=enforcement,
        argument=_text(entry.get("argument"), f"{where}.argument"),
        wall=_ci_job_from({**wall, "id": "wall"}, f"{where}.wall"),
        jobs=jobs,
        tracking_bead=bead,
        reporting_reason=reason,
    )


def ci_declaration_problems(register: Register) -> list[str]:
    """Rule 2 and the ratchet over the CI gates, with no clock involved.

    The static half of `OR-17`'s third obligation. A hosted job with no recorded wall, or
    a ceiling with more headroom than `policy.max_headroom`, is a job that can double
    without anything objecting -- which is exactly what `exhaustive-tier` did.
    """
    policy = register.policy
    problems: list[str] = []
    for gate in register.ci_gates:
        label = f"ci gate {gate.id!r}"
        if gate.drift_ratio <= 1.0:
            problems.append(
                f"{label}: drift_ratio is {gate.drift_ratio:g}; a band at or below the "
                "recorded wall fails every honest run"
            )
        if gate.drift_ratio > policy.max_headroom:
            problems.append(
                f"{label}: drift_ratio is {gate.drift_ratio:g}, above "
                f"policy.max_headroom ({policy.max_headroom:g}); a band looser than the "
                "ceiling's own slack cannot be the thing that speaks first"
            )
        for job in (*gate.jobs, gate.wall):
            at = f"{label} job {job.id!r}"
            measured = job.measured_seconds
            if measured is None:
                if job.pending_measurement is None:
                    problems.append(
                        f"{at}: no wall is recorded, so its drift, stale and headroom rules "
                        "are all switched off. Run `devtools.check_ci_gate_walls --sample`, "
                        "or name pending_measurement for the first run of a new job shape."
                    )
                continue
            if job.ceiling_seconds < measured:
                problems.append(
                    f"{at}: the ceiling is {job.ceiling_seconds:g}s and the recorded wall "
                    f"is {measured:g}s, so the job is declared to fail every time it runs"
                )
            headroom = job.headroom
            if headroom is not None and headroom > policy.max_headroom:
                problems.append(
                    f"{at}: the ceiling is {job.ceiling_seconds:g}s against a recorded "
                    f"{measured:g}s, which is {headroom:.2f}x of headroom where "
                    f"policy.max_headroom allows {policy.max_headroom:g}x"
                )
            if headroom is not None and headroom < gate.drift_ratio:
                problems.append(
                    f"{at}: the ceiling is {headroom:.2f}x of the record, inside the "
                    f"gate's own {gate.drift_ratio:g}x drift band, so the ceiling would "
                    "fail before the drift rule could name what moved"
                )
            found, _ = rise_findings(at, job.records, policy)
            problems.extend(found)
        walls = [job.measured_seconds for job in gate.jobs if job.measured_seconds is not None]
        recorded_wall = gate.wall.measured_seconds
        if walls and recorded_wall is not None and recorded_wall < max(walls):
            problems.append(
                f"{label}: the gate's wall is recorded at {recorded_wall:g}s, under its "
                f"longest job at {max(walls):g}s; the wall is at least the longest job"
            )
    return problems


def judge_ci_job(
    register: Register,
    gate_id: str,
    job_id: str,
    *,
    wall_seconds: float,
    steps: tuple[tuple[str, float], ...] = (),
    runner: str,
    force: bool = False,
    enforce: bool = False,
) -> Verdict:
    """Compare one finished hosted job against the register.

    `Verdict.tier` carries the job id here. The four rules are `band_findings`, the same
    function `judge` uses, so a CI job cannot end up under a second set of bands that
    drifts from the tiers'.

    `force` overrides the runner match and `enforce` overrides a gate's declared
    `enforcement: reporting`. Both are for a caller asking the question deliberately; the
    register is the authority on what CI itself does with the answer.
    """
    top = _named_steps(steps, wall_seconds)
    gate = register.ci_gate(gate_id)
    if gate is None:
        return Verdict(
            tier=job_id,
            wall_seconds=wall_seconds,
            status="unknown",
            notes=(f"no ci gate {gate_id!r} is declared in {register.path}",),
            top_steps=top,
        )
    job = gate.wall if job_id == "wall" else gate.job(job_id)
    if job is None:
        return Verdict(
            tier=job_id,
            wall_seconds=wall_seconds,
            status="unknown",
            notes=(
                (
                    f"the {gate.id} gate declares no ceiling for its {job_id!r} job in "
                    f"{register.path}; every job a gate runs needs one"
                ),
            ),
            top_steps=top,
        )
    enforced = force or gate.reference.matches(runner=runner)
    found = band_findings(
        subject=f"the {gate.id} gate's {job.id!r} job",
        wall_seconds=wall_seconds,
        ceiling_seconds=job.ceiling_seconds,
        measured_seconds=job.measured_seconds,
        shape=gate.reference.describe(),
        policy=register.policy,
        attribution=_attribution(steps, wall_seconds),
        register_path=register.path,
        drift_ratio=gate.drift_ratio,
    )
    failures, notes = list(found.failures), list(found.notes)
    if failures and not enforced:
        notes.extend(failures)
        notes.append(
            f"this job ran on {runner!r}; the {gate.id} gate's band is declared for "
            f"{gate.reference.describe()}, so the run above is reported and not failed"
        )
        failures = []
    if failures and gate.reports_only and not enforce:
        notes.extend(failures)
        notes.append(
            f"the {gate.id} gate reports rather than enforces under {gate.tracking_bead}: "
            f"{gate.reporting_reason}"
        )
        failures = []
    return Verdict(
        tier=job.id,
        wall_seconds=wall_seconds,
        status="failed" if failures else ("passed" if enforced else "reported"),
        enforced=enforced and (enforce or not gate.reports_only),
        ceiling_seconds=job.ceiling_seconds,
        measured_seconds=job.measured_seconds,
        failures=tuple(failures),
        notes=tuple(notes),
        top_steps=top,
    )


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


@dataclass(frozen=True)
class Findings:
    """Rules 1, 3 and 4 over one wall, kept apart by what they are relative to.

    `ceiling` is rule 1, absolute and never relaxed. `relative` is rules 3 and 4, measured
    against the record, which a register may declare advisory on a pull request. A caller
    with no such distinction to draw reads `failures`, the two together in rule order.
    """

    ceiling: tuple[str, ...] = ()
    relative: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def failures(self) -> tuple[str, ...]:
        return (*self.ceiling, *self.relative)


def band_findings(
    *,
    subject: str,
    wall_seconds: float,
    ceiling_seconds: float,
    measured_seconds: float | None,
    shape: str,
    policy: Policy,
    attribution: str,
    register_path: Path | None,
    drift_ratio: float | None = None,
    band: tuple[float, float] | None = None,
) -> Findings:
    """Rules 1, 3 and 4 over one wall.

    The one place the four rules are written, so a surface that clocks something other
    than a local tier -- `judge_ci_job` clocks a hosted job -- is held to the same bands
    rather than to a second copy of them that drifts from this one. `drift_ratio`
    overrides `policy.drift_ratio` for a surface whose noise the policy figure was not
    measured on; nothing else is overridable, because a per-entry stale ratio or headroom
    is a tier declaring its own policy, which is what `policy` exists to prevent.
    `band`, a recorded `(low, high)` of readings, changes what the ratios are applied to,
    never the ratios: the stale rule reads its low edge and the drift rule its high edge.
    """
    ceiling: list[str] = []
    failures: list[str] = []
    notes: list[str] = []
    drift = policy.drift_ratio if drift_ratio is None else drift_ratio
    if wall_seconds > ceiling_seconds:
        ceiling.append(
            f"{subject} ran {wall_seconds:.1f}s against a "
            f"{ceiling_seconds:g}s ceiling: {attribution}"
        )
    if measured_seconds is None:
        notes.append(
            f"no cost is recorded for {subject} at {shape}; "
            f"write `measured_seconds: {wall_seconds:.1f}` into {register_path} to arm the "
            "drift rule"
        )
    elif wall_seconds < policy.min_wall_seconds:
        notes.append(
            f"{wall_seconds:.1f}s is under the {policy.min_wall_seconds:g}s noise floor, so "
            "the drift and stale rules were not applied"
        )
    else:
        low, high = band if band is not None else (measured_seconds, measured_seconds)
        against = (
            f"the recorded band [{low:g}, {high:g}]s"
            if band is not None
            else f"a recorded {measured_seconds:g}s"
        )
        if wall_seconds > drift * high:
            failures.append(
                f"{subject} ran {wall_seconds:.1f}s against {against} "
                f"({wall_seconds / high:.2f}x, where {drift:g}x fails): {attribution}"
            )
        if wall_seconds < policy.stale_ratio * low:
            tightened = min(ceiling_seconds, wall_seconds * policy.max_headroom)
            advice = (
                f"Widen measured_band's low to {wall_seconds:.1f} if the readings still "
                f"span the band, or re-record the tier, in {register_path}."
                if band is not None
                else f"Write `measured_seconds: {wall_seconds:.1f}` and "
                f"`ceiling_seconds: {tightened:.0f}` into {register_path}."
            )
            failures.append(
                f"{subject} ran {wall_seconds:.1f}s against {against}, which is "
                f"{wall_seconds / low:.2f}x. The record is "
                f"stale in the flattering direction, which is how a ceiling stops "
                f"detecting anything. {advice}"
            )
    return Findings(ceiling=tuple(ceiling), relative=tuple(failures), notes=tuple(notes))


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
    pull_request: bool = False,
) -> Verdict:
    """Compare one finished run against the register.

    `tier_id` is `None` for a scoped run -- `--only`, or `--since` narrowing a tier --
    because a subset of a tier has no declared cost and pretending otherwise is how a
    ceiling gets waived by accident.

    `pull_request` says the run is a hosted pull-request job. When the register declares
    `policy.pull_request_relative_rules` advisory, the drift and stale findings of such a
    run are reported under that bead and do not fail it. `pull_request_ceiling` makes
    completed-run ceiling findings advisory independently of their ratio. `force` is an
    operator asking deliberately and overrides both relaxations and reference matching.
    A full checkpoint stays enforcing even if invoked inside a pull-request job.
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
    attribution = _attribution(steps, wall_seconds)
    measured = tier.measured_seconds
    found = band_findings(
        subject=f"the {tier.id} tier",
        wall_seconds=wall_seconds,
        ceiling_seconds=tier.ceiling_seconds,
        measured_seconds=measured,
        shape=tier.reference.describe(),
        policy=policy,
        attribution=attribution,
        register_path=register.path,
        band=tier.measured_band,
    )
    failures = list(found.failures)
    notes = list(found.notes)
    advisory_failures: tuple[str, ...] = ()
    # Full checkpoints keep cost enforcement even when invoked inside a PR job.
    advisory_run = pull_request and not force and tier.id != "full"
    advisory = policy.pull_request_relative_rules if advisory_run else None
    if advisory is not None and found.relative:
        failures = list(found.ceiling)
        advisory_failures = found.relative
    ceiling_rule = policy.pull_request_ceiling if advisory_run else None
    if ceiling_rule is not None and found.ceiling:
        failures = [failure for failure in failures if failure not in found.ceiling]
        advisory_failures = (*found.ceiling, *advisory_failures)
        advisory = ceiling_rule.advisory

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
    if failures:
        status: Literal["passed", "failed", "advisory", "reported"] = "failed"
    elif not enforced:
        status = "reported"
    elif advisory_failures:
        status = "advisory"
    else:
        status = "passed"
    return Verdict(
        tier=tier.id,
        wall_seconds=wall_seconds,
        status=status,
        enforced=enforced,
        ceiling_seconds=tier.ceiling_seconds,
        measured_seconds=measured,
        failures=tuple(failures),
        notes=tuple(notes),
        top_steps=top,
        advisory_failures=advisory_failures if enforced else (),
        advisory=advisory if enforced and advisory_failures else None,
    )


def advisory_note(advisory: Advisory) -> str:
    """The sentence every rendering of an advisory finding carries."""
    reason = advisory.reason if advisory.reason.endswith(".") else f"{advisory.reason}."
    return (
        f"{advisory.rules} are advisory on pull requests under "
        f"{advisory.tracking_bead}: {reason} {advisory.still_fails}"
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
    lines.extend(
        f"  FAIL (advisory, not enforced): {reason}" for reason in verdict.advisory_failures
    )
    if verdict.advisory is not None:
        lines.append(f"  enforcement: {advisory_note(verdict.advisory)}")
    lines.extend(f"  note: {note}" for note in verdict.notes)
    return lines
