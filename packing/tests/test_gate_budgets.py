"""The gate's cost check, held to the standard the gate holds everything else to.

A detector nobody has watched fire is not a detector. `run_negative_controls` makes that
argument for the record checks; these make it for the timing check, and they make it
twice -- once for the declaration, which needs no clock, and once for a finished run.

**No test here writes a number it wants the live check to agree with.** Every figure is
read back out of `devtools/gate-budgets.yaml` and scaled by the policy's own ratios,
because a test that pinned `1369.60` would rot on the day the tier changed -- which is
exactly how the docstring this mechanism replaces came to be wrong. Where a test needs a
declaration the live register does not have, it fabricates a whole one in `tmp_path`, the
way `test_control_anchors` fabricates a control spec.

The one place literal seconds appear is the 2026-08-30 replay, whose numbers are the
incident itself: 499 seconds recorded beside an 1800 second cap.
Those are history and cannot drift.
"""

# Reaching for `_parser`, `_tier_id` and `_render_text` is the point: a test that
# reimplemented any of them would drift from the CLI it checks, which is the failure this
# file exists to prevent. `devtools/check_declared_commands.py` takes the same exemption.
# pyright: reportPrivateUsage=false
from __future__ import annotations

import json
import math
import os
from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path

import pytest

from devtools import bead_state
from devtools.check_gate_budgets import (
    OR_14_OUTER_EDGE_SECONDS,
    attribute_files,
    coverage_problems,
    pull_request_tiers,
    relative_rule_problems,
    unrecorded_problems,
    wall_problems,
)
from devtools.check_pr_wall import load_walls
from sqpack import gate_budgets
from sqpack.cli import validate
from sqpack.gate_budgets import BudgetError, Register, TierBudget
from sqpack.yamlio import safe_load

LIVE = gate_budgets.BUDGETS
SLOW_STEP = "a step that got slower"
CHEAP_STEP = "a step that did not"
#: One day of hosted readings of two tiers, with the verdict each gets under three rules.
HOSTED_DAY = (
    Path(__file__).resolve().parent
    / "fixtures"
    / "tier-walls"
    / "hosted-readings-2026-09-30.yaml"
)


def live() -> Register:
    return gate_budgets.load(LIVE)


def fabricated(
    tmp_path: Path, *, ceiling: float, measured: str, date: str = "'2026-08-30'"
) -> Path:
    """A whole register in `tmp_path`, so a test can declare what it needs to refuse."""
    spec = tmp_path / "gate-budgets.yaml"
    spec.write_text(
        "policy:\n"
        "  max_headroom: 2.0\n"
        "  drift_ratio: 1.5\n"
        "  stale_ratio: 0.6\n"
        "  min_wall_seconds: 20.0\n"
        "tiers:\n"
        "- id: fast\n"
        "  command: packing-validate --fast\n"
        f"  ceiling_seconds: {ceiling}\n"
        f"  measured_seconds: {measured}\n"
        f"  measured_on: {date}\n"
        "  measured_where: a fabricated register\n"
        "  reference: {jobs: 2, inner_jobs: 1, cpus: 2}\n"
        "  argument: a fabricated register\n",
        encoding="utf-8",
    )
    return spec


def pending_ci_register(tmp_path: Path, job_fields: str) -> Path:
    """A new hosted shape with a real ceiling and no fabricated measurement."""
    spec = fabricated(tmp_path, ceiling=200.0, measured="100.0")
    with spec.open("a", encoding="utf-8") as stream:
        stream.write(
            "ci_gates:\n"
            "- id: new-gate\n"
            "  file: .github/workflows/new.yml\n"
            "  aggregate: required\n"
            "  selected_by: dispatch\n"
            "  reference: {runner: ubuntu-latest, cpus: 4}\n"
            "  drift_ratio: 1.5\n"
            "  enforcement: reporting\n"
            "  tracking_bead: think-test\n"
            "  reporting_reason: first hosted observation is pending\n"
            "  argument: a new parallel partition\n"
            "  wall:\n"
            "    ceiling_seconds: 200\n"
            "    argument: ceiling retained until the first observation\n"
            "    pending_measurement: think-test\n"
            "  jobs:\n"
            "  - id: worker\n"
            "    ceiling_seconds: 200\n"
            "    argument: bounded bootstrap with explicitly unmeasured wall\n"
            f"{job_fields}"
        )
    return spec


def test_pending_ci_measurement_keeps_the_absolute_ceiling(tmp_path: Path) -> None:
    register = gate_budgets.load(
        pending_ci_register(tmp_path, "    pending_measurement: think-test\n")
    )
    assert gate_budgets.ci_declaration_problems(register) == []
    verdict = gate_budgets.judge_ci_job(
        register,
        "new-gate",
        "worker",
        wall_seconds=201,
        runner="ubuntu-latest",
        enforce=True,
    )
    assert verdict.failed
    assert verdict.measured_seconds is None


def test_unmeasured_ci_job_without_an_owner_still_fails(tmp_path: Path) -> None:
    register = gate_budgets.load(pending_ci_register(tmp_path, ""))
    assert any(
        "no wall is recorded" in problem
        for problem in gate_budgets.ci_declaration_problems(register)
    )


@pytest.mark.parametrize(
    "extra",
    [
        "    measured_seconds: 100\n    measured_on: '2026-09-29'\n",
        "    measured_where: estimated from predecessor\n",
        "    spread: 1.5\n",
    ],
)
def test_pending_ci_measurement_cannot_masquerade_as_observed(
    tmp_path: Path, extra: str
) -> None:
    path = pending_ci_register(tmp_path, "    pending_measurement: think-test\n" + extra)
    with pytest.raises(BudgetError, match="both a pending measurement"):
        gate_budgets.load(path)


def test_pending_ci_measurement_requires_a_bead_alias(tmp_path: Path) -> None:
    path = pending_ci_register(tmp_path, "    pending_measurement: later\n")
    with pytest.raises(BudgetError, match="think-xxxx"):
        gate_budgets.load(path)


def recorded_tier(register: Register) -> TierBudget:
    """A tier with a cost on record, for the rules that need something to compare to.

    The register can legitimately carry none: a tier whose composition just changed has no
    valid record until the next run at its reference shape takes one. When that is the
    case the tier's own ceiling stands in, divided by the loosest headroom the policy
    allows -- still the register's arithmetic, still no figure typed here. A tier with a
    `measured_band` is skipped: its rules sit at the band's edges, which the band tests
    below exercise, and these tests are about a point record.
    """
    for tier in register.tiers:
        if tier.measured_seconds is not None and tier.measured_band is None:
            return tier
    tier = register.tiers[0]
    return replace(
        tier,
        measured_seconds=tier.ceiling_seconds / register.policy.max_headroom,
        measured_on="(no tier carries a record; synthesised from this tier's ceiling)",
    )


def judge_at_reference(
    register: Register,
    tier: TierBudget,
    steps: tuple[tuple[str, float], ...],
) -> gate_budgets.Verdict:
    """Judge a synthetic run on the tier's own reference shape, so the band is enforced."""
    return gate_budgets.judge(
        with_tier(register, tier),
        tier.id,
        wall_seconds=sum(seconds for _, seconds in steps),
        steps=steps,
        jobs=tier.reference.jobs,
        inner_jobs=tier.reference.inner_jobs,
        cpus=tier.reference.cpus,
    )


def with_tier(register: Register, tier: TierBudget) -> Register:
    """The live register with one tier replaced, so a stand-in record is the one judged."""
    return replace(
        register,
        tiers=tuple(tier if other.id == tier.id else other for other in register.tiers),
    )


def test_the_live_declaration_is_internally_consistent() -> None:
    """Rule 2, against the register as checked in. This is the records-tier step."""
    assert gate_budgets.declaration_problems(live()) == []


def test_every_selectable_tier_declares_a_ceiling() -> None:
    """A tier with no ceiling is a tier that can triple, which is the whole incident."""
    assert set(live().ids) == set(validate.TIER_IDS)


def test_a_tier_without_a_ceiling_is_refused(tmp_path: Path) -> None:
    """The coverage rule has to bite; one that only ever passes proves nothing."""
    head, _, _ = LIVE.read_text(encoding="utf-8").partition("- id: fast")
    spec = tmp_path / "gate-budgets.yaml"
    spec.write_text(head, encoding="utf-8")
    problems = coverage_problems(gate_budgets.load(spec))
    assert any("fast" in problem for problem in problems), problems


def test_the_2026_08_30_declaration_would_have_been_refused(tmp_path: Path) -> None:
    """The incident, replayed.

    On 2026-08-30 `--fast` was measured at 499s and capped at 1800s. Six days later it
    cost 1369.60s and passed, because 1370 is inside 1800. The declaration itself is what
    was wrong: 3.61x of headroom cannot see a 2.65x regression, and no clock is needed to
    notice that.
    """
    register = gate_budgets.load(fabricated(tmp_path, ceiling=1800.0, measured="499.0"))
    problems = gate_budgets.declaration_problems(register)
    assert any("headroom" in problem for problem in problems), problems
    # And the ceiling it prints is one the 1369.60s run of six days later would have failed.
    assert any("998" in problem for problem in problems), problems

    tightened = replace(register.tiers[0], ceiling_seconds=998.0)
    verdict = judge_at_reference(
        replace(register, tiers=(tightened,)),
        tightened,
        (("fast behavioral tests", 1324.0), ("every other fast step", 45.6)),
    )
    assert verdict.failed, verdict
    assert any("fast behavioral tests" in reason for reason in verdict.failures), verdict


def test_a_slowed_step_fails_the_check_and_is_named() -> None:
    """Negative control one: deliberately slow a step, and the run must fail for it.

    The slow step is given the tier's whole ceiling, so the run is over by construction
    whatever the ceiling happens to be, and no seconds figure is written here.
    """
    register = live()
    tier = recorded_tier(register)
    steps = ((SLOW_STEP, tier.ceiling_seconds), (CHEAP_STEP, register.policy.min_wall_seconds))
    verdict = judge_at_reference(register, tier, steps)

    assert verdict.failed, verdict
    assert verdict.enforced
    assert any(SLOW_STEP in reason for reason in verdict.failures), verdict.failures
    assert any("ceiling" in reason for reason in verdict.failures), verdict.failures


def test_a_run_inside_the_band_passes_without_a_figure_in_the_assertion() -> None:
    """Negative control two: the check must not simply always fire.

    The synthetic run costs exactly what the register says the tier costs, split across
    two steps. Every number comes out of the register; none is typed here, so this test
    cannot rot into agreeing with a stale figure.
    """
    register = live()
    tier = recorded_tier(register)
    recorded = tier.measured_seconds
    assert recorded is not None
    steps = ((SLOW_STEP, recorded * 0.9), (CHEAP_STEP, recorded * 0.1))
    verdict = judge_at_reference(register, tier, steps)

    assert verdict.failures == (), verdict.failures
    assert verdict.status == "passed", verdict


def test_the_drift_rule_fires_while_the_run_is_still_inside_the_ceiling() -> None:
    """The rule that catches a regression against a cap the run never reaches.

    A ceiling alone did not catch the incident: 1370s is inside 1800s. Drift against the
    tier's own record is what does. The tier here is given the loosest ceiling the policy
    still allows -- exactly `max_headroom` times its record, the worst declaration that can
    pass the static check -- and the run is then placed between the drift ratio and that
    ceiling, which is where the 2026-09-05 run sat.
    """
    register = live()
    tier = recorded_tier(register)
    recorded = tier.measured_seconds
    assert recorded is not None
    policy = register.policy
    loosest = replace(tier, ceiling_seconds=recorded * policy.max_headroom)
    assert gate_budgets.declaration_problems(with_tier(register, loosest)) == [], (
        "the loosest ceiling the policy allows must still be a legal declaration"
    )

    midpoint = (policy.drift_ratio + policy.max_headroom) / 2
    steps = ((SLOW_STEP, recorded * midpoint),)
    verdict = judge_at_reference(register, loosest, steps)

    assert verdict.wall_seconds < loosest.ceiling_seconds, "the run stayed inside the cap"
    assert verdict.failed, verdict
    assert any("recorded" in reason for reason in verdict.failures), verdict.failures
    assert any(SLOW_STEP in reason for reason in verdict.failures), verdict.failures


def test_a_record_the_tier_has_outgrown_downward_fails_and_prints_the_new_figure() -> None:
    """The other direction, which is how the 499 became prose in the first place.

    A record bounded only from above rots downward: the tier gets faster, nobody updates
    it, and the ratio rules stop meaning anything. So a run far enough under the record
    fails too, and names the value to write.
    """
    register = live()
    tier = recorded_tier(register)
    recorded = tier.measured_seconds
    assert recorded is not None
    wall = recorded * register.policy.stale_ratio / 2
    verdict = judge_at_reference(register, tier, ((SLOW_STEP, wall),))

    assert verdict.failed, verdict
    assert any("stale" in reason for reason in verdict.failures), verdict.failures
    assert any(f"{wall:.1f}" in reason for reason in verdict.failures), verdict.failures


def test_an_unmeasured_tier_prints_the_line_that_would_arm_the_drift_rule() -> None:
    """A tier with no record is the state a composition change leaves behind.

    Nobody has to remember to take the measurement: the first run at the reference shape
    prints the exact line to paste, and until then the absolute ceiling still applies.
    """
    register = live()
    unmeasured = next((tier for tier in register.tiers if tier.measured_seconds is None), None)
    if unmeasured is None:
        pytest.skip("every tier currently carries a record")
    wall = unmeasured.ceiling_seconds / 2
    verdict = judge_at_reference(register, unmeasured, ((CHEAP_STEP, wall),))

    assert not verdict.failed, verdict
    assert any(f"measured_seconds: {wall:.1f}" in note for note in verdict.notes), verdict


def test_a_scoped_run_is_not_judged_against_a_whole_tier() -> None:
    """`--only` is a slice, and a slice finishing fast says nothing about the tier."""
    register = live()
    tier = recorded_tier(register)
    verdict = gate_budgets.judge(
        register,
        None,
        wall_seconds=tier.ceiling_seconds * 2,
        steps=((SLOW_STEP, tier.ceiling_seconds * 2),),
        jobs=tier.reference.jobs,
        inner_jobs=tier.reference.inner_jobs,
        cpus=tier.reference.cpus,
    )
    assert verdict.status == "unknown"
    assert not verdict.failed


def test_a_run_off_the_reference_shape_reports_instead_of_failing() -> None:
    """Wall time is not comparable across machines.

    A check that fails on a slow runner is a check people turn off, so an unmatched shape
    prints the same sentence and does not fail. `--enforce-budget` overrides that for an
    operator who means it.
    """
    register = live()
    tier = recorded_tier(register)
    steps = ((SLOW_STEP, tier.ceiling_seconds * 2),)
    elsewhere = {
        "wall_seconds": steps[0][1],
        "steps": steps,
        "jobs": tier.reference.jobs,
        "inner_jobs": tier.reference.inner_jobs,
        "cpus": tier.reference.cpus + 1,
    }
    reported = gate_budgets.judge(with_tier(register, tier), tier.id, **elsewhere)
    assert reported.status == "reported"
    assert not reported.failed
    assert any(SLOW_STEP in note for note in reported.notes), reported.notes

    forced = gate_budgets.judge(with_tier(register, tier), tier.id, force=True, **elsewhere)
    assert forced.failed, forced


def test_a_register_that_records_a_cost_without_a_date_is_refused(tmp_path: Path) -> None:
    """A measurement nobody can place cannot be re-taken, so it is not a measurement."""
    with pytest.raises(BudgetError, match="date"):
        gate_budgets.load(fabricated(tmp_path, ceiling=1800.0, measured="499.0", date="null"))


def test_every_boolean_flag_is_classified_as_a_tier_or_not() -> None:
    """A new tier flag must not be able to arrive without a ceiling.

    `TIER_IDS` is what `devtools.check_gate_budgets` compares the register against, so a
    tier flag missing from it would run with no declared cost and nothing would say so.
    Every `store_true` option on the parser is therefore either a tier or named here as
    deliberately not one.
    """
    not_a_tier = {"strict", "deep", "list", "budgets", "enforce_budget"}
    # A `store_true` flag is exactly one that defaults to False in the parsed namespace,
    # which reads the real parser without reaching into argparse's internals.
    defaults = vars(validate._parser().parse_args([]))
    booleans = {name for name, value in defaults.items() if value is False}
    unclassified = booleans - set(validate.TIER_FLAGS) - not_a_tier
    assert unclassified == set(), (
        f"{sorted(unclassified)} is neither a tier in TIER_FLAGS nor listed as not one; "
        "a tier with no entry in gate-budgets.yaml runs with no declared ceiling"
    )


def test_the_tier_of_an_invocation_is_always_one_the_register_declares() -> None:
    """Whatever `_tier_id` names, the register must have a ceiling for it."""
    declared = set(live().ids)
    for flags in (
        [],
        ["--records"],
        ["--edit"],
        ["--fast"],
        ["--push"],
        ["--records", "--fast"],
        ["--typecheck"],
        ["--suite-a"],
        ["--suite-b"],
        ["--suite-c"],
        ["--suite-d"],
    ):
        namespace = validate._parser().parse_args(flags)
        tier = validate._tier_id(namespace)
        assert tier in declared, (flags, tier)
    scoped = validate._parser().parse_args(["--only", "lint"])
    assert validate._tier_id(scoped) is None


def test_a_run_over_its_ceiling_fails_the_command_even_with_every_step_green(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """The seam between the verdict and the process exit code.

    Every step passes and the command still returns 1, because the tier cost more than it
    is allowed to. That is the whole behavioural difference from the docstring this
    replaces: a number the run acts on rather than one a reader might notice.
    """
    register = live()
    tier = recorded_tier(register)
    steps = ((SLOW_STEP, tier.ceiling_seconds), (CHEAP_STEP, register.policy.min_wall_seconds))
    summary = validate.RunSummary(
        results=[
            validate.StepResult(name=name, status="passed", seconds=seconds)
            for name, seconds in steps
        ],
        wall_seconds=sum(seconds for _, seconds in steps),
        selected_count=len(steps),
        total_count=len(steps),
        budget=judge_at_reference(register, tier, steps),
    )
    assert validate._render_text(summary, strict=False) == 1
    printed = capsys.readouterr().out
    assert "THE TIER IS OUTSIDE ITS DECLARED COST BAND" in printed
    assert SLOW_STEP in printed


# --- the three rules added on 2026-09-15, each named for how the second spiral got past --


def a_record(seconds: float, on: str, *, attributed: bool = False) -> gate_budgets.Record:
    """One record in a history, with or without the attribution a rise needs."""
    attribution = (
        gate_budgets.Attribution(
            cause="a fabricated cause",
            unit="step-seconds",
            source="a fabricated source",
            grew=(gate_budgets.Growth(name=SLOW_STEP, before=1.0, after=2.0),),
        )
        if attributed
        else None
    )
    return gate_budgets.Record(
        seconds=seconds, on=on, where="fabricated", attribution=attribution
    )


def rises(records: tuple[gate_budgets.Record, ...]) -> tuple[list[str], list[str]]:
    return gate_budgets.rise_findings("a fabricated tier", records, live().policy)


def test_a_tier_a_pull_request_runs_may_not_have_an_empty_record() -> None:
    """Rule 5, and the gap the second spiral used first.

    An empty record switches rules 2, 3 and 4 off together and leaves one absolute
    ceiling. `checks` and `sweeps` sat empty for eight days and `checks` failed its
    ceiling at least nine times in them with every step green.
    """
    register = live()
    tier = recorded_tier(register)
    emptied = with_tier(register, replace(tier, measured_seconds=None, measured_on=None))
    problems = unrecorded_problems(emptied, {tier.id: "a job"})
    assert any("no recorded cost" in problem for problem in problems)
    assert unrecorded_problems(register, {tier.id: "a job"}) == []


def test_a_pull_request_record_must_name_the_run_it_was_read_from() -> None:
    """A reading nobody can re-take is a number, and the register is not for numbers."""
    register = live()
    tier = recorded_tier(register)
    prose = with_tier(register, replace(tier, measured_where="measured on a good day"))
    problems = unrecorded_problems(prose, {tier.id: "a job"})
    assert any("names no hosted run" in problem for problem in problems)


def test_every_tier_the_workflow_runs_on_a_pull_request_is_recorded() -> None:
    """The live statement of rule 5, read from the workflow rather than from a list."""
    tiers = pull_request_tiers()
    assert set(tiers) <= set(live().ids)
    assert tiers, "no pull-request job runs a whole tier"
    assert unrecorded_problems(live(), tiers) == []


# --- a tier pending its first hosted measurement: a bead, a date, and the ceiling --------

#: The record lines `fabricated` writes, which a pending tier carries none of.
FABRICATED_RECORD = (
    "  measured_seconds: 100.0\n"
    "  measured_on: '2026-08-30'\n"
    "  measured_where: a fabricated register\n"
)
PENDING_UNTIL = date(2026, 10, 8)


def pending_tier(
    tmp_path: Path,
    *,
    bead: str | None = "think-aaaa",
    until: str | None = f"'{PENDING_UNTIL.isoformat()}'",
    record: str = "",
) -> Path:
    """The fabricated register with its one tier's record replaced by pending fields.

    Each field is written only when given, so a test can leave one out to see it refused,
    and `record` puts observation fields beside them for the same purpose. `fast` stands in
    for a tier a pull request runs: the caller says so in the mapping it passes.
    """
    spec = fabricated(tmp_path, ceiling=200.0, measured="100.0")
    document = spec.read_text(encoding="utf-8")
    assert FABRICATED_RECORD in document
    lines = "".join(
        f"  {name}: {value}\n"
        for name, value in (("pending_measurement", bead), ("pending_until", until))
        if value is not None
    )
    spec.write_text(document.replace(FABRICATED_RECORD, record + lines, 1), encoding="utf-8")
    return spec


def test_a_pending_pull_request_tier_passes_until_its_date_and_fails_after_it(
    tmp_path: Path,
) -> None:
    """A tier that has never run has no hosted reading to cite, for a while.

    Under a live bead it passes up to and on `pending_until`, and the day after it is an
    empty record like any other, with the date and the command that records it in the
    message. The ceiling is not part of the allowance: a run over it fails throughout.
    """
    register = gate_budgets.load(pending_tier(tmp_path))
    tier = register.tiers[0]
    assert tier.measured_seconds is None
    assert tier.pending_measurement == "think-aaaa"
    assert tier.pending_until == PENDING_UNTIL
    assert gate_budgets.declaration_problems(register) == []
    read = bead_state.fixture_store({"aaaa": "open"})
    run_by = {tier.id: "a job"}

    for day in (PENDING_UNTIL - timedelta(days=7), PENDING_UNTIL):
        assert unrecorded_problems(register, run_by, today=day, read=read) == [], day

    expired = unrecorded_problems(
        register, run_by, today=PENDING_UNTIL + timedelta(days=1), read=read
    )
    assert len(expired) == 1, expired
    assert f"tier {tier.id!r}" in expired[0]
    assert f"pending measurement under think-aaaa expired on {PENDING_UNTIL}" in expired[0]
    assert f"python -m devtools.read_tier_walls --tier {tier.id} --run-id" in expired[0]

    over = judge_at_reference(register, tier, ((SLOW_STEP, tier.ceiling_seconds * 1.01),))
    assert over.failed, over
    assert any("ceiling" in reason for reason in over.failures), over.failures
    inside = judge_at_reference(register, tier, ((SLOW_STEP, tier.ceiling_seconds / 2),))
    assert not inside.failed, inside
    assert any("no cost is recorded" in note for note in inside.notes), inside.notes


def test_an_unowned_empty_record_is_still_refused_whatever_the_date(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The allowance is the bead and the date together, not the absence of a record."""
    register = gate_budgets.load(pending_tier(tmp_path, bead=None, until=None))
    tier = register.tiers[0]
    assert tier.pending_measurement is None

    def unreachable() -> None:
        raise AssertionError("a tier with nothing pending must not need the bead store")

    monkeypatch.setattr(bead_state, "store", unreachable)
    problems = unrecorded_problems(
        register, {tier.id: "a job"}, today=PENDING_UNTIL - timedelta(days=7)
    )
    assert len(problems) == 1, problems
    assert "no recorded cost" in problems[0]


@pytest.mark.parametrize(
    ("record", "named"),
    [
        ("  measured_seconds: 100.0\n  measured_on: '2026-08-30'\n", "measured_seconds"),
        ("  measured_where: estimated from the shard beside it\n", "measured_where"),
        ("  measured_on: '2026-08-30'\n", "measured_on"),
        ("  measured_band: {low: 80, high: 120}\n", "measured_band"),
    ],
)
def test_a_pending_tier_cannot_masquerade_as_measured(
    tmp_path: Path, record: str, named: str
) -> None:
    """A forecast is not a reading, and a reading is not pending."""
    with pytest.raises(BudgetError, match="pending and measured at once") as refusal:
        gate_budgets.load(pending_tier(tmp_path, record=record))
    assert named in str(refusal.value)


@pytest.mark.parametrize(
    ("bead", "until", "message"),
    [
        ("later", "'2026-10-08'", r"pending_measurement must name a `think-xxxx` bead"),
        ("closed-4cwy", "'2026-10-08'", r"pending_measurement must name a `think-xxxx` bead"),
        ("think-aaaa", None, "pending_measurement requires pending_until"),
        (None, "'2026-10-08'", "pending_until requires pending_measurement"),
        ("think-aaaa", "next week", "pending_until must be an ISO date"),
        ("think-aaaa", "'2026-13-08'", "pending_until must be an ISO date"),
        ("think-aaaa", "20", "pending_until must be an ISO date"),
    ],
)
def test_a_malformed_pending_declaration_is_refused(
    tmp_path: Path, bead: str | None, until: str | None, message: str
) -> None:
    """The bead and the date come together, and each has to be what it says it is."""
    with pytest.raises(BudgetError, match=message):
        gate_budgets.load(pending_tier(tmp_path, bead=bead, until=until))


def test_a_pending_date_may_be_written_quoted_or_as_yaml_s_own(tmp_path: Path) -> None:
    """The register quotes its dates; an unquoted one is the same day, not a refusal."""
    for until in ("'2026-10-08'", "2026-10-08"):
        register = gate_budgets.load(pending_tier(tmp_path, until=until))
        assert register.tiers[0].pending_until == PENDING_UNTIL, until


def test_a_pending_tier_must_be_owned_by_an_open_bead(tmp_path: Path) -> None:
    """The ratchet an advisory wall is held to, applied to a pending measurement.

    A closed bead means the measurement is claimed taken while the record is still empty;
    an unknown one never owned anything. Both are refused inside the date, on a fixture
    store so this runs anywhere.
    """
    read = bead_state.fixture_store({"aaaa": "open", "bbbb": "in_progress", "cccc": "closed"})
    run_by = {"fast": "a job"}

    def problems(bead: str) -> list[str]:
        register = gate_budgets.load(pending_tier(tmp_path, bead=bead))
        return unrecorded_problems(register, run_by, today=PENDING_UNTIL, read=read)

    assert problems("think-aaaa") == []
    assert problems("think-bbbb") == []
    closed = problems("think-cccc")
    assert len(closed) == 1, closed
    assert "tier 'fast' is pending its first hosted measurement" in closed[0]
    assert "under think-cccc: closed" in closed[0]
    assert "python -m devtools.read_tier_walls --tier fast --run-id" in closed[0]
    unknown = problems("think-zzzz")
    assert len(unknown) == 1, unknown
    assert "under think-zzzz: no such bead" in unknown[0]


def test_a_pending_tier_with_no_bead_store_fails_under_ci_and_skips_locally(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A bead nothing can resolve is not trusted in CI; a recorded tier never asks."""
    register = gate_budgets.load(pending_tier(tmp_path))
    run_by = {"fast": "a job"}
    monkeypatch.setattr(bead_state, "store", lambda: None)
    monkeypatch.setenv("CI", "true")
    problems = unrecorded_problems(register, run_by, today=PENDING_UNTIL)
    assert len(problems) == 1, problems
    assert "no bead store is reachable" in problems[0]
    assert "fetch full history" in problems[0]

    monkeypatch.delenv("CI")
    capsys.readouterr()
    assert unrecorded_problems(register, run_by, today=PENDING_UNTIL) == []
    printed = capsys.readouterr().out
    assert printed.startswith("SKIP "), printed
    assert "no bead store is reachable" in printed
    assert "think-aaaa" in printed

    # Past the date the bead is beside the point: the tier fails on the calendar alone.
    capsys.readouterr()
    expired = unrecorded_problems(register, run_by, today=PENDING_UNTIL + timedelta(days=1))
    assert len(expired) == 1, expired
    assert "expired on" in expired[0]
    assert capsys.readouterr().out == ""

    def unreachable() -> None:
        raise AssertionError("a recorded tier must not need the bead store")

    monkeypatch.setattr(bead_state, "store", unreachable)
    recorded = gate_budgets.load(fabricated(tmp_path, ceiling=200.0, measured="100.0"))
    problems = unrecorded_problems(recorded, run_by, today=PENDING_UNTIL)
    assert len(problems) == 1, problems
    assert "names no hosted run" in problems[0]


def test_the_live_pending_tiers_pass_until_their_dates_and_are_named_after_them() -> None:
    """The register as checked in, with the dates read from it rather than typed here.

    Each tier pending a first hosted measurement is one a pull-request job runs, since
    that is the only place the date and the bead are held to anything. The whole surface
    passes up to the earliest date, each tier is named the day after its own, and the
    beads are then resolved in the checkout's real store. With nothing pending this
    skips, as the unmeasured-tier test does: the mechanism is for a new tier's first days.
    """
    register = live()
    tiers = pull_request_tiers()
    pending = [tier for tier in register.tiers if tier.pending_measurement is not None]
    if not pending:
        pytest.skip("no tier is currently pending its first measurement")
    dates: dict[str, date] = {}
    for tier in pending:
        assert tier.pending_until is not None
        assert tier.id in tiers, (
            f"{tier.id} is pending a first hosted measurement and no pull-request job runs "
            "it, so nothing holds its date or its bead"
        )
        dates[tier.id] = tier.pending_until
    every_bead_open = bead_state.fixture_store(
        {(tier.pending_measurement or "").removeprefix("think-"): "open" for tier in pending}
    )
    earliest = min(dates.values())
    assert unrecorded_problems(register, tiers, today=earliest, read=every_bead_open) == []
    for tier_id, until in dates.items():
        after = unrecorded_problems(
            register, tiers, today=until + timedelta(days=1), read=every_bead_open
        )
        assert any(
            f"tier {tier_id!r}" in problem and f"expired on {until}" in problem
            for problem in after
        ), (tier_id, after)
    real = _require_bead_store()
    assert unrecorded_problems(register, tiers, today=earliest, read=real) == []


def test_a_record_that_rises_without_attribution_is_refused() -> None:
    """Rule 6, and the gap the second spiral used second.

    `suite`'s record moved 102.83 -> 162.62 -> 118.72 -> 183.44 s in three days, each move
    a real hosted reading, and 2.4x of growth went through a 1.5x drift rule because every
    reading became the next baseline.
    """
    policy = live().policy
    assert policy.max_unattributed_rise is not None
    rise = policy.max_unattributed_rise
    history = (a_record(100.0, "2026-12-01"), a_record(100.0 * rise * 1.1, "2026-12-02"))
    problems, grandfathered = rises(history)
    assert grandfathered == []
    assert any(
        "without naming the per-step or per-file costs" in problem for problem in problems
    )


def test_an_attributed_rise_passes_and_becomes_the_new_baseline() -> None:
    """The rule asks for an argument, not for the tier to stop growing."""
    policy = live().policy
    assert policy.max_unattributed_rise is not None
    rise = policy.max_unattributed_rise
    attributed = a_record(100.0 * rise * 1.1, "2026-12-02", attributed=True)
    problems, _ = rises((a_record(100.0, "2026-12-01"), attributed))
    assert problems == []
    after = a_record(attributed.seconds * 1.05, "2026-12-03")
    problems, _ = rises((a_record(100.0, "2026-12-01"), attributed, after))
    assert problems == [], "an attributed record starts the comparison again from itself"


def test_a_ratchet_of_small_rises_is_measured_from_the_lowest_record() -> None:
    """Each step inside the ratio, and the sum outside it: the failure the rule is for."""
    policy = live().policy
    assert policy.max_unattributed_rise is not None
    step = (policy.max_unattributed_rise - 1.0) / 2 + 1.0
    history = tuple(
        a_record(100.0 * step**index, f"2026-12-0{index + 1}") for index in range(4)
    )
    problems, _ = rises(history)
    assert problems, "four rises of half the allowance each are still a ratchet"


def test_a_record_that_falls_needs_no_attribution() -> None:
    """Rule 4 is what answers a record that falls; this rule is only about rises."""
    problems, grandfathered = rises(
        (a_record(200.0, "2026-12-01"), a_record(100.0, "2026-12-02"))
    )
    assert (problems, grandfathered) == ([], [])


def test_the_live_register_has_no_unresolved_or_grandfathered_rise() -> None:
    """The current measured topology starts each new tier with attributed evidence."""
    register = live()
    problems, grandfathered = gate_budgets.ratchet_problems(register)
    assert problems == []
    assert grandfathered == []


def test_a_wall_budget_past_or14s_outer_edge_is_refused(tmp_path: Path) -> None:
    """`OR-14` sets the edge; a budget past it is a different rule, not a looser one."""
    register = tmp_path / "gate-budgets.yaml"
    register.write_text(
        "pull_request_walls:\n"
        "  policy:\n"
        "    regression_ratio: 1.2\n"
        "    min_samples: 15\n"
        "    main_branch: main\n"
        "    setup_steps: ['^Set up job$']\n"
        "  workflows:\n"
        "  - id: packing-validation\n"
        "    file: .github/workflows/packing-validation.yml\n"
        "    aggregator: packing-required\n"
        "    not_gating: [macos-portability]\n"
        f"    budget_seconds: {OR_14_OUTER_EDGE_SECONDS * 2}\n"
        "    argument: a fabricated register\n",
        encoding="utf-8",
    )
    problems = wall_problems(register)
    assert any("outer edge" in problem for problem in problems)


def test_the_pages_wall_cannot_declare_a_second_budget(tmp_path: Path) -> None:
    """The page register and the live wall checker describe the same metric."""
    register = tmp_path / "gate-budgets.yaml"
    register.write_text(
        "pages:\n"
        "  wall:\n"
        "    ceiling_seconds: 179.0\n"
        "pull_request_walls:\n"
        "  policy:\n"
        "    regression_ratio: 1.2\n"
        "    min_samples: 15\n"
        "    main_branch: main\n"
        "    setup_steps: ['^Set up job$']\n"
        "  workflows:\n"
        "  - id: certificate-page\n"
        "    file: .github/workflows/pages.yml\n"
        "    aggregator: pages-required\n"
        "    not_gating: []\n"
        "    budget_seconds: 180.0\n"
        "    argument: a fabricated register\n",
        encoding="utf-8",
    )
    problems = wall_problems(register)
    assert any("same metric" in problem for problem in problems)


def _require_bead_store() -> bead_state.Reader:
    """The checkout's bead store: skipped without one locally, failed without one under `CI`."""
    try:
        return bead_state.require_store()
    except bead_state.UnavailableError as error:
        if os.environ.get("CI"):
            pytest.fail(f"{error}; the job must fetch full history to check trackers")
        return pytest.skip(str(error))


def test_a_missing_bead_store_fails_under_ci_and_skips_locally(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(bead_state, "store", lambda: None)
    monkeypatch.setenv("CI", "true")
    with pytest.raises(pytest.fail.Exception, match="must fetch full history"):
        _require_bead_store()
    monkeypatch.delenv("CI")
    with pytest.raises(pytest.skip.Exception, match="no bead store is reachable"):
        _require_bead_store()


def advisory_walls(tmp_path: Path, *, bead: str = "think-aaaa", budget: float = 180.0) -> Path:
    """A wall register in `tmp_path` whose one wall is advisory under `bead`."""
    register = tmp_path / "gate-budgets.yaml"
    register.write_text(
        "pull_request_walls:\n"
        "  policy:\n"
        "    regression_ratio: 1.2\n"
        "    min_samples: 15\n"
        "    main_branch: main\n"
        "    setup_steps: ['^Set up job$']\n"
        "  workflows:\n"
        "  - id: packing-validation\n"
        "    file: .github/workflows/packing-validation.yml\n"
        "    aggregator: packing-required\n"
        "    not_gating: [macos-portability]\n"
        f"    budget_seconds: {budget}\n"
        "    enforcement: advisory\n"
        f"    tracking_bead: {bead}\n"
        "    advisory_reason: a fabricated owner decision\n"
        "    argument: a fabricated register\n",
        encoding="utf-8",
    )
    return register


def test_an_advisory_wall_must_be_tracked_by_an_open_bead(tmp_path: Path) -> None:
    """An advisory wall is a relaxation, and a relaxation names the work that ends it.

    A closed bead means that work is claimed done while the wall is still not enforced; an
    unknown one never tracked anything. Both are the lower floor `think-4cwy` became for
    the `tsconfig` flags, and both are refused on a fixture store so this runs anywhere.
    """
    read = bead_state.fixture_store({"aaaa": "open", "bbbb": "in_progress", "cccc": "closed"})
    assert wall_problems(advisory_walls(tmp_path, bead="think-aaaa"), read) == []
    assert wall_problems(advisory_walls(tmp_path, bead="think-bbbb"), read) == []
    closed = wall_problems(advisory_walls(tmp_path, bead="think-cccc"), read)
    assert len(closed) == 1, closed
    assert "advisory under think-cccc: closed" in closed[0]
    unknown = wall_problems(advisory_walls(tmp_path, bead="think-zzzz"), read)
    assert len(unknown) == 1, unknown
    assert "advisory under think-zzzz: no such bead" in unknown[0]


def test_an_advisory_wall_with_no_bead_store_fails_under_ci_and_skips_locally(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """A tracker nothing can resolve is not trusted in CI; an enforcing wall never asks.

    Locally a checkout without the `tbd-sync` branch is a normal state, so the check says
    loudly that it skipped, the way `check_bead_tree` does, rather than failing a laptop.
    """
    monkeypatch.setattr(bead_state, "store", lambda: None)
    monkeypatch.setenv("CI", "true")
    problems = wall_problems(advisory_walls(tmp_path))
    assert len(problems) == 1, problems
    assert "no bead store is reachable" in problems[0]
    assert "fetch full history" in problems[0]

    monkeypatch.delenv("CI")
    capsys.readouterr()
    assert wall_problems(advisory_walls(tmp_path)) == []
    printed = capsys.readouterr().out
    assert printed.startswith("SKIP "), printed
    assert "no bead store is reachable" in printed
    assert "think-aaaa" in printed

    enforcing = advisory_walls(tmp_path)
    document = enforcing.read_text(encoding="utf-8")
    enforcing.write_text(
        document.replace("    enforcement: advisory\n", "")
        .replace("    tracking_bead: think-aaaa\n", "")
        .replace("    advisory_reason: a fabricated owner decision\n", ""),
        encoding="utf-8",
    )

    def unreachable() -> None:
        raise AssertionError("an enforcing wall must not need the bead store")

    monkeypatch.setattr(bead_state, "store", unreachable)
    assert wall_problems(enforcing) == []


def test_an_advisory_wall_keeps_or14s_outer_edge(tmp_path: Path) -> None:
    """Advisory relaxes what a wall over the budget does, never the budget itself."""
    read = bead_state.fixture_store({"aaaa": "open"})
    problems = wall_problems(
        advisory_walls(tmp_path, budget=OR_14_OUTER_EDGE_SECONDS * 2), read
    )
    assert any("outer edge" in problem for problem in problems), problems


@pytest.mark.parametrize(
    ("old", "new", "message"),
    [
        ("    tracking_bead: think-aaaa\n", "", "tracking_bead: think-xxxx"),
        ("    advisory_reason: a fabricated owner decision\n", "", "advisory_reason"),
        ("enforcement: advisory", "enforcement: lenient", "enforcement must be one of"),
    ],
)
def test_the_static_check_reports_a_malformed_enforcement(
    tmp_path: Path, old: str, new: str, message: str
) -> None:
    """The records tier fails on the declaration before any pull request reads it."""
    path = advisory_walls(tmp_path)
    document = path.read_text(encoding="utf-8")
    assert old in document
    path.write_text(document.replace(old, new, 1), encoding="utf-8")
    problems = wall_problems(path, bead_state.fixture_store({"aaaa": "open"}))
    assert len(problems) == 1, problems
    assert problems[0].startswith("pull_request_walls: "), problems
    assert message in problems[0], problems


def test_each_workflow_still_runs_the_wall_check_it_declares() -> None:
    """Rule 7's wiring: a budget nothing runs is a budget nothing enforces.

    Both job graphs are being restructured as this lands, so the check is that each
    workflow's declared aggregator still invokes the tool -- not that the graph has a
    particular shape. The wiring is checked everywhere, against a store in which every
    declared tracker is open. An advisory wall's tracker is then resolved in the
    checkout's real bead store, which is why the jobs that run this file fetch full
    history; without one that half skips locally and fails under `CI`.
    """
    trackers = {
        workflow.advisory.tracking_bead.removeprefix("think-"): "open"
        for workflow in load_walls().workflows
        if workflow.advisory is not None
    }
    assert wall_problems(read=bead_state.fixture_store(trackers)) == []
    assert wall_problems(read=_require_bead_store()) == []


def test_an_attribution_that_names_no_growth_is_refused(tmp_path: Path) -> None:
    """A cause with no costs is a story. The rule asks for what grew, and by how much."""
    spec = fabricated(tmp_path, ceiling=200.0, measured="100.0")
    spec.write_text(
        spec.read_text(encoding="utf-8") + "  attribution:\n"
        "    cause: the tier got slower\n"
        "    unit: step-seconds\n"
        "    source: a fabricated source\n"
        "    grew:\n"
        "    - {name: a step, before: 10.0, after: 10.0}\n",
        encoding="utf-8",
    )
    with pytest.raises(BudgetError, match="no growth"):
        gate_budgets.load(spec)


@pytest.mark.parametrize("field", ["jobs", "inner_jobs", "cpus"])
def test_fractional_reference_resources_are_refused(tmp_path: Path, field: str) -> None:
    spec = fabricated(tmp_path, ceiling=200.0, measured="100.0")
    document = spec.read_text(encoding="utf-8")
    old = f"{field}: 2" if field in {"jobs", "cpus"} else f"{field}: 1"
    assert old in document
    spec.write_text(document.replace(old, f"{field}: 1.5", 1), encoding="utf-8")

    with pytest.raises(BudgetError, match=rf"reference\.{field}.*positive integer"):
        gate_budgets.load(spec)


@pytest.mark.parametrize(
    "declaration",
    ["  max_headroom: 2.0\n", "  ceiling_seconds: 200.0\n"],
)
def test_duplicate_budget_fields_are_refused(tmp_path: Path, declaration: str) -> None:
    spec = fabricated(tmp_path, ceiling=200.0, measured="100.0")
    document = spec.read_text(encoding="utf-8")
    assert declaration in document
    spec.write_text(
        document.replace(declaration, declaration + declaration, 1), encoding="utf-8"
    )

    with pytest.raises(BudgetError, match="duplicate key"):
        gate_budgets.load(spec)


# `-.inf` adds no regression coverage: 5ca38b03 already refused it as a negative cost.
@pytest.mark.parametrize("before", [".nan", ".inf", "-.inf"])
def test_an_attribution_before_cost_must_be_finite(tmp_path: Path, before: str) -> None:
    spec = fabricated(tmp_path, ceiling=200.0, measured="100.0")
    spec.write_text(
        spec.read_text(encoding="utf-8") + "  attribution:\n"
        "    cause: a fabricated rise\n"
        "    unit: step-seconds\n"
        "    source: a fabricated source\n"
        "    grew:\n"
        f"    - {{name: a step, before: {before}, after: 10.0}}\n",
        encoding="utf-8",
    )
    with pytest.raises(BudgetError, match="non-negative and finite"):
        gate_budgets.load(spec)


def test_a_suite_record_can_be_attributed_from_two_per_file_reports(tmp_path: Path) -> None:
    """G5's consumer: `suite` grows by many small files, so its attribution is per file.

    115 new test files added 281 s of junit time between 2026-09-08 and 2026-09-14 and
    nothing priced them. This turns two per-file reports into the block a raised record
    has to carry, and says what the second one added.
    """
    before = tmp_path / "before.json"
    after = tmp_path / "after.json"
    before.write_text(
        json.dumps([{"file": "tests/test_old.py", "tests": 4, "seconds": 2.0}]),
        encoding="utf-8",
    )
    after.write_text(
        json.dumps(
            [
                {"file": "tests/test_old.py", "tests": 4, "seconds": 2.5},
                {"file": "tests/test_new.py", "tests": 9, "seconds": 30.0},
            ]
        ),
        encoding="utf-8",
    )
    lines = attribute_files(before, after)
    assert "added test files: 1, 9 tests, 30.0 test-seconds" in lines[0]
    assert any("test_new.py" in line and "after: 30.00" in line for line in lines)
    assert any("test_old.py" in line and "before: 2.00" in line for line in lines)


def banded_tier(register: Register) -> TierBudget:
    """The live tier that records a `measured_band`; the register must carry one."""
    tier = next((tier for tier in register.tiers if tier.measured_band is not None), None)
    assert tier is not None, "no live tier records a measured_band"
    return tier


def test_a_band_places_the_stale_rule_at_its_low_edge_and_drift_at_its_high() -> None:
    """think-be1s, D-472: the ratios stay the policy's, the band moves their edges.

    A reading at the band's low edge passes; a reading under `stale_ratio` of the low edge
    still fails, and so does one over `drift_ratio` of the high edge, inside a ceiling
    loosened to leave the drift rule room. Every figure comes from the register.
    """
    register = live()
    tier = banded_tier(register)
    policy = register.policy
    assert tier.measured_band is not None
    low, high = tier.measured_band

    at_low = judge_at_reference(register, tier, ((SLOW_STEP, low),))
    assert at_low.failures == (), at_low.failures

    stale = judge_at_reference(register, tier, ((SLOW_STEP, policy.stale_ratio * low * 0.9),))
    assert stale.failed, stale
    assert any("stale" in reason and "band" in reason for reason in stale.failures)

    roomy = replace(tier, ceiling_seconds=high * policy.drift_ratio * 1.2)
    wall = high * (policy.drift_ratio + 0.1)
    drift = judge_at_reference(register, roomy, ((SLOW_STEP, wall),))
    assert wall < roomy.ceiling_seconds
    assert drift.failed, drift
    assert any("band" in reason for reason in drift.failures), drift.failures


def test_every_live_band_passes_the_readings_it_was_taken_from() -> None:
    """Each banded tier passes its band's edges and middle: the runs that failed a point
    record from the other regime (geometry at 58.75 s, typecheck at 92.27 s) now pass."""
    register = live()
    banded = [tier for tier in register.tiers if tier.measured_band is not None]
    assert banded, "no live tier records a measured_band"
    for tier in banded:
        assert tier.measured_band is not None
        low, high = tier.measured_band
        for wall in (low, (low + high) / 2, high):
            verdict = judge_at_reference(register, tier, ((SLOW_STEP, wall),))
            assert verdict.failures == (), (tier.id, wall, verdict.failures)


def test_a_band_that_does_not_bracket_its_record_is_refused() -> None:
    register = live()
    tier = banded_tier(register)
    assert tier.measured_seconds is not None
    measured = tier.measured_seconds
    off = replace(tier, measured_band=(measured * 1.05, measured * 1.2))
    problems = gate_budgets.band_problems(off, register.policy)
    assert any("does not contain" in problem for problem in problems), problems


def test_a_band_wider_than_the_policy_window_is_refused() -> None:
    """A band may not switch the rules off: no wider than drift_ratio / stale_ratio."""
    register = live()
    tier = banded_tier(register)
    policy = register.policy
    assert tier.measured_seconds is not None
    measured = tier.measured_seconds
    window = policy.drift_ratio / policy.stale_ratio
    wide = replace(tier, measured_band=(measured / window, measured * 1.01))
    problems = gate_budgets.band_problems(wide, policy)
    assert any("window" in problem for problem in problems), problems


def test_a_ceiling_under_the_band_s_drift_edge_binds_first_and_is_legal() -> None:
    """The ceiling may bind before the drift rule, as it may for a point record."""
    register = live()
    tier = banded_tier(register)
    policy = register.policy
    assert tier.measured_band is not None
    high = tier.measured_band[1]
    tight = replace(tier, ceiling_seconds=policy.drift_ratio * high * 0.95)
    assert gate_budgets.band_problems(tight, policy) == []
    over = judge_at_reference(register, tight, ((SLOW_STEP, tight.ceiling_seconds * 1.01),))
    assert over.failed, over
    assert any("ceiling" in reason for reason in over.failures), over.failures


def test_a_band_without_a_record_is_refused(tmp_path: Path) -> None:
    spec = tmp_path / "gate-budgets.yaml"
    spec.write_text(
        "policy:\n"
        "  max_headroom: 2.0\n"
        "  drift_ratio: 1.5\n"
        "  stale_ratio: 0.6\n"
        "  min_wall_seconds: 20.0\n"
        "tiers:\n"
        "- id: fast\n"
        "  command: packing-validate --fast\n"
        "  ceiling_seconds: 100\n"
        "  measured_band: {low: 40, high: 60}\n"
        "  reference: {jobs: 2, inner_jobs: 1, cpus: 2}\n"
        "  argument: a fabricated register\n",
        encoding="utf-8",
    )
    with pytest.raises(BudgetError, match="measured_band without a measured_seconds"):
        gate_budgets.load(spec)


# --- the drift and stale rules, advisory on pull requests (think-53a2, 2026-10-01) ------


def relaxed(
    tmp_path: Path,
    *,
    enforcement: str | None = "advisory",
    bead: str | None = "think-aaaa",
    reason: str | None = "a fabricated owner decision",
    ceiling: float = 200.0,
    measured: str = "100.0",
) -> Path:
    """The fabricated register with `policy.pull_request_relative_rules` declared.

    Each field is written only when given, so a test can leave one out to see it refused.
    """
    spec = fabricated(tmp_path, ceiling=ceiling, measured=measured)
    lines = ["  pull_request_relative_rules:"]
    lines.extend(
        f"    {name}: {value}"
        for name, value in (
            ("enforcement", enforcement),
            ("tracking_bead", bead),
            ("advisory_reason", reason),
        )
        if value is not None
    )
    document = spec.read_text(encoding="utf-8")
    spec.write_text(document.replace("tiers:\n", "\n".join(lines) + "\ntiers:\n", 1))
    return spec


def judge_pull_request(
    register: Register, wall: float, *, pull_request: bool = True, force: bool = False
) -> gate_budgets.Verdict:
    """Judge one wall of the fabricated register's one tier at its reference shape."""
    tier = register.tiers[0]
    return gate_budgets.judge(
        register,
        tier.id,
        wall_seconds=wall,
        steps=((SLOW_STEP, wall),),
        jobs=tier.reference.jobs,
        inner_jobs=tier.reference.inner_jobs,
        cpus=tier.reference.cpus,
        force=force,
        pull_request=pull_request,
    )


def test_band_findings_keep_the_ceiling_apart_from_the_relative_rules(tmp_path: Path) -> None:
    """Rule 1 is absolute and rules 3 and 4 are relative to the record, and a caller that
    relaxes the latter must be able to tell them apart without parsing a sentence."""
    register = gate_budgets.load(fabricated(tmp_path, ceiling=200.0, measured="100.0"))
    policy = register.policy
    found = gate_budgets.band_findings(
        subject="the fast tier",
        wall_seconds=210.0,
        ceiling_seconds=200.0,
        measured_seconds=100.0,
        shape="fabricated",
        policy=policy,
        attribution="one step",
        register_path=None,
    )
    assert len(found.ceiling) == 1
    assert "ceiling" in found.ceiling[0]
    assert len(found.relative) == 1
    assert f"{policy.drift_ratio:g}x fails" in found.relative[0]
    assert found.failures == (*found.ceiling, *found.relative)


def test_a_stale_run_on_a_pull_request_is_reported_and_not_failed(tmp_path: Path) -> None:
    """The 2026-09-30 failure, replayed on a fabricated register.

    PR #262's checks tier ran 62.3 s against a recorded 114.34 s, 0.54x, with every step
    green, and the job failed. Under the relaxation the same finding is computed, printed
    as advisory under its bead, and the run passes; off a pull request, or with the
    operator's `--enforce-budget`, it still fails.
    """
    register = gate_budgets.load(relaxed(tmp_path))
    policy = register.policy
    wall = 100.0 * policy.stale_ratio * 0.9

    advisory = judge_pull_request(register, wall)
    assert advisory.status == "advisory", advisory
    assert not advisory.failed
    assert advisory.failures == ()
    assert len(advisory.advisory_failures) == 1
    assert "stale in the flattering direction" in advisory.advisory_failures[0]
    assert advisory.advisory is not None
    assert advisory.advisory.tracking_bead == "think-aaaa"
    rendered = gate_budgets.render(advisory)
    assert any(line.startswith("  FAIL (advisory, not enforced): ") for line in rendered)
    assert any("advisory on pull requests under think-aaaa" in line for line in rendered)
    assert not any(line.startswith("  FAIL: ") for line in rendered)
    assert (
        validate._summary_status(
            validate.RunSummary(
                results=[], wall_seconds=wall, selected_count=1, total_count=1, budget=advisory
            ),
            strict=False,
        )
        == 0
    )

    locally = judge_pull_request(register, wall, pull_request=False)
    assert locally.failed, locally
    assert locally.advisory is None
    assert locally.advisory_failures == ()

    forced = judge_pull_request(register, wall, force=True)
    assert forced.failed, forced


def test_a_drifted_run_on_a_pull_request_is_advisory_but_the_ceiling_still_fails_it(
    tmp_path: Path,
) -> None:
    """PR #255's shard C: 140.2 s against 88.59 s, 1.58x, inside the 154 s ceiling, is
    advisory; 172.5 s is over the ceiling and fails whatever the relaxation says."""
    register = gate_budgets.load(relaxed(tmp_path))
    policy = register.policy
    inside = judge_pull_request(register, 100.0 * (policy.drift_ratio + 0.1))
    assert inside.status == "advisory", inside
    assert any(f"{policy.drift_ratio:g}x fails" in r for r in inside.advisory_failures)

    over = judge_pull_request(register, 200.0 * 1.05)
    assert over.failed, over
    assert len(over.failures) == 1
    assert "ceiling" in over.failures[0]
    assert any("fails" in r for r in over.advisory_failures), (
        "the drift finding is still reported beside the ceiling failure"
    )


def test_a_pull_request_run_off_the_reference_shape_is_reported_not_advisory(
    tmp_path: Path,
) -> None:
    register = gate_budgets.load(relaxed(tmp_path))
    tier = register.tiers[0]
    verdict = gate_budgets.judge(
        register,
        tier.id,
        wall_seconds=10.0 * register.policy.stale_ratio,
        steps=((SLOW_STEP, 10.0),),
        jobs=tier.reference.jobs,
        inner_jobs=tier.reference.inner_jobs,
        cpus=tier.reference.cpus + 1,
        pull_request=True,
    )
    assert verdict.status == "reported"
    assert verdict.advisory is None
    assert verdict.advisory_failures == ()


def test_an_enforcing_declaration_leaves_every_rule_as_it_was(tmp_path: Path) -> None:
    """`enforcement: enforcing`, and an absent block, are the same thing: no relaxation."""
    spec = relaxed(tmp_path, enforcement="enforcing", bead=None, reason=None)
    register = gate_budgets.load(spec)
    assert register.policy.pull_request_relative_rules is None
    wall = 100.0 * register.policy.stale_ratio * 0.9
    assert judge_pull_request(register, wall).failed
    assert (
        gate_budgets.load(
            fabricated(tmp_path, ceiling=200.0, measured="100.0")
        ).policy.pull_request_relative_rules
        is None
    )


@pytest.mark.parametrize(
    ("enforcement", "bead", "reason", "message"),
    [
        (
            "enforcing",
            "think-aaaa",
            "a reason",
            "enforcing and still names tracking_bead, advisory_reason",
        ),
        ("advisory", None, "a reason", "tracking_bead: think-xxxx"),
        ("advisory", "closed-4cwy", "a reason", "tracking_bead: think-xxxx"),
        ("advisory", "think-aaaa", None, "advisory_reason"),
        ("lenient", "think-aaaa", "a reason", "enforcement must be one of"),
    ],
)
def test_a_malformed_relative_rule_declaration_is_refused(
    tmp_path: Path, enforcement: str, bead: str | None, reason: str | None, message: str
) -> None:
    """The records tier fails on the declaration before any pull request reads it."""
    with pytest.raises(BudgetError, match=message):
        gate_budgets.load(relaxed(tmp_path, enforcement=enforcement, bead=bead, reason=reason))


def test_an_advisory_relative_rule_must_be_tracked_by_an_open_bead(tmp_path: Path) -> None:
    """The ratchet an advisory wall is held to, applied to the relaxed rules.

    A closed bead means the work that ends the relaxation is claimed done while the rules
    are still not enforced; an unknown one never tracked anything. Both are refused on a
    fixture store so this runs anywhere.
    """
    read = bead_state.fixture_store({"aaaa": "open", "bbbb": "in_progress", "cccc": "closed"})
    assert (
        relative_rule_problems(gate_budgets.load(relaxed(tmp_path, bead="think-aaaa")), read)
        == []
    )
    assert (
        relative_rule_problems(gate_budgets.load(relaxed(tmp_path, bead="think-bbbb")), read)
        == []
    )
    closed = relative_rule_problems(
        gate_budgets.load(relaxed(tmp_path, bead="think-cccc")), read
    )
    assert len(closed) == 1, closed
    assert "under think-cccc: closed" in closed[0]
    unknown = relative_rule_problems(
        gate_budgets.load(relaxed(tmp_path, bead="think-zzzz")), read
    )
    assert len(unknown) == 1, unknown
    assert "under think-zzzz: no such bead" in unknown[0]
    enforcing = gate_budgets.load(
        relaxed(tmp_path, enforcement="enforcing", bead=None, reason=None)
    )
    assert relative_rule_problems(enforcing, read) == []


def test_an_advisory_relative_rule_with_no_bead_store_fails_under_ci_and_skips_locally(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    register = gate_budgets.load(relaxed(tmp_path))
    monkeypatch.setattr(bead_state, "store", lambda: None)
    monkeypatch.setenv("CI", "true")
    problems = relative_rule_problems(register)
    assert len(problems) == 1, problems
    assert "fetch full history" in problems[0]

    monkeypatch.delenv("CI")
    capsys.readouterr()
    assert relative_rule_problems(register) == []
    printed = capsys.readouterr().out
    assert printed.startswith("SKIP "), printed
    assert "think-aaaa" in printed


def test_the_live_relaxation_names_a_live_bead_and_keeps_the_hang_detector() -> None:
    """The register as checked in: both relaxations advisory under beads the store
    confirms are open. Since 2026-10-05 (think-6erz) a pull-request run just over a ceiling
    is advisory; one over the hang ratio still fails."""
    register = live()
    declared = register.policy.pull_request_relative_rules
    assert declared is not None, "the live register no longer declares the relaxation"
    ceiling = register.policy.pull_request_ceiling
    assert ceiling is not None, "the live register no longer relaxes the ceiling"
    assert relative_rule_problems(register, _require_bead_store()) == []
    tier = recorded_tier(register)

    def on_a_pull_request(wall: float) -> gate_budgets.Verdict:
        return gate_budgets.judge(
            register,
            tier.id,
            wall_seconds=wall,
            steps=((SLOW_STEP, wall),),
            jobs=tier.reference.jobs,
            inner_jobs=tier.reference.inner_jobs,
            cpus=tier.reference.cpus,
            pull_request=True,
        )

    over = on_a_pull_request(tier.ceiling_seconds * 1.01)
    assert not over.failed, over
    assert any("ceiling" in finding for finding in over.advisory_failures), over
    hung = on_a_pull_request(tier.ceiling_seconds * ceiling.hang_ratio * 1.01)
    assert hung.failed, hung


def test_the_day_of_2026_09_30_is_judged_on_code_not_on_the_runner() -> None:
    """Every hosted reading of the two tiers that failed that day, replayed three ways.

    The fixture carries the readings with their run ids and the verdict intended under
    each rule; this computes all three from the register and holds them to it, so the
    table in the fixture is what the code does and not a story about it. The `intended`
    column is judged against the live register with the two tiers' records as they were
    re-taken from these readings on 2026-10-01, and the ceilings they had that day, which
    the fixture's `retaken` block carries, so a later re-take of either record, or a later
    raise of either ceiling, does not rewrite what this day's readings were held to. Under
    it every clean reading passes, and the only walls still failed are the two over the
    154 s ceiling, which `OR-17` keeps absolute.

    Two things keep `retaken` honest. It is the counted readings' own geometric mean and
    range, computed here; and each of its records is still in the live register, as the
    current record or in its history.
    """
    document = safe_load(HOSTED_DAY.read_text(encoding="utf-8"))
    # That day is judged under that day's policy: the ceiling's own pull-request
    # relaxation (think-6erz, 2026-10-05) came later and is held by its own tests.
    current = live()
    register = replace(current, policy=replace(current.policy, pull_request_ceiling=None))
    superseded = document["superseded"]
    retaken = document["retaken"]
    intended = replace(
        register,
        tiers=tuple(
            replace(
                tier,
                measured_seconds=float(retaken[tier.id]["measured_seconds"]),
                measured_band=(
                    float(retaken[tier.id]["measured_band"]["low"]),
                    float(retaken[tier.id]["measured_band"]["high"]),
                ),
                ceiling_seconds=float(retaken[tier.id]["ceiling_seconds"]),
            )
            if tier.id in retaken
            else tier
            for tier in register.tiers
        ),
    )
    old_register = replace(
        register,
        policy=replace(register.policy, pull_request_relative_rules=None),
        tiers=tuple(
            replace(
                tier,
                measured_seconds=float(superseded[tier.id]["measured_seconds"]),
                ceiling_seconds=float(superseded[tier.id]["ceiling_seconds"]),
                measured_band=None,
                history=(),
                attribution=None,
            )
            if tier.id in superseded
            else tier
            for tier in register.tiers
        ),
    )
    relaxed_old = replace(old_register, policy=register.policy)
    assert register.policy.pull_request_relative_rules is not None

    def verdict(which: Register, tier_id: str, wall: float) -> str:
        tier = which.tier(tier_id)
        assert tier is not None
        judged = gate_budgets.judge(
            which,
            tier_id,
            wall_seconds=wall,
            steps=((f"fast behavioral tests, {tier_id}", wall),),
            jobs=tier.reference.jobs,
            inner_jobs=tier.reference.inner_jobs,
            cpus=tier.reference.cpus,
            pull_request=True,
        )
        return judged.status

    readings = document["readings"]
    assert len(readings) >= 60
    for reading in readings:
        tier_id, wall = str(reading["tier"]), float(reading["wall"])
        where = f"{tier_id} {wall} in run {reading['run']}"
        assert verdict(old_register, tier_id, wall) == reading["old_rule"], where
        assert verdict(relaxed_old, tier_id, wall) == reading["relaxation_alone"], where
        assert verdict(intended, tier_id, wall) == reading["intended"], where

    counted = [r for r in readings if not r.get("step_failed")]
    assert all(r["intended"] == "passed" for r in counted)
    refused = [r for r in readings if r.get("step_failed")]
    assert refused
    assert all(r["intended"] == "failed" for r in refused)
    assert set(retaken) == {str(r["tier"]) for r in readings} == set(superseded)
    for tier_id, record in retaken.items():
        walls = [float(r["wall"]) for r in counted if r["tier"] == tier_id]
        band = (float(record["measured_band"]["low"]), float(record["measured_band"]["high"]))
        assert band == (min(walls), max(walls)), tier_id
        geometric = math.exp(sum(math.log(w) for w in walls) / len(walls))
        seconds = float(record["measured_seconds"])
        assert seconds == pytest.approx(geometric, abs=0.01), tier_id
        tier = register.tier(tier_id)
        assert tier is not None
        assert any(held.seconds == pytest.approx(seconds, abs=0.01) for held in tier.records), (
            f"the {tier_id} record re-taken from this day's readings, {seconds:g}s, is no "
            "longer in the live register as the current record or in its history"
        )


# --- the ceiling, advisory on pull requests up to a hang detector (think-6erz, 2026-10-05)


def ceiling_relaxed(
    tmp_path: Path,
    *,
    enforcement: str | None = "advisory",
    bead: str | None = "think-aaaa",
    reason: str | None = "a fabricated owner decision",
    hang: str | None = "2.0",
    per_test: str | None = "45.0",
) -> Path:
    """The fabricated register (ceiling 200 s, record 150 s) with
    `policy.pull_request_ceiling` declared; a field left as None is not written."""
    spec = fabricated(tmp_path, ceiling=200.0, measured="150.0")
    lines = ["  pull_request_ceiling:"]
    lines.extend(
        f"    {name}: {value}"
        for name, value in (
            ("enforcement", enforcement),
            ("tracking_bead", bead),
            ("advisory_reason", reason),
            ("hang_ratio", hang),
            ("per_test_hang_seconds", per_test),
        )
        if value is not None
    )
    document = spec.read_text(encoding="utf-8")
    spec.write_text(document.replace("tiers:\n", "\n".join(lines) + "\ntiers:\n", 1))
    return spec


def test_a_ceiling_breach_on_a_pull_request_is_advisory_below_the_hang_ratio(
    tmp_path: Path,
) -> None:
    """#356's shard C, 171.2 s against 168 s with every test green, is the case: over the
    ceiling but far under twice it, so it is reported under the bead and does not fail."""
    register = gate_budgets.load(ceiling_relaxed(tmp_path))
    verdict = judge_pull_request(register, 200.0 * 1.02)
    assert verdict.status == "advisory", verdict
    assert not verdict.failures
    assert any("ceiling" in finding for finding in verdict.advisory_failures)
    assert verdict.advisory is not None
    assert verdict.advisory.tracking_bead == "think-aaaa"
    note = gate_budgets.advisory_note(verdict.advisory)
    assert "the tier ceilings and the per-test call-wall rule are advisory" in note
    assert "above 2x its ceiling" in note


def test_a_pull_request_wall_above_the_hang_ratio_still_fails(tmp_path: Path) -> None:
    """The relaxation gives up the verdict on runner speed, not on a run that has stopped
    making progress: above twice the ceiling the ceiling failure stands."""
    register = gate_budgets.load(ceiling_relaxed(tmp_path))
    verdict = judge_pull_request(register, 200.0 * 2.0 + 1.0)
    assert verdict.failed, verdict
    assert any("ceiling" in failure for failure in verdict.failures)


def test_the_ceiling_relaxation_applies_only_to_a_pull_request_run_and_yields_to_force(
    tmp_path: Path,
) -> None:
    """Main, scheduled and deep runs keep the ceiling, and an operator asking on purpose
    with --enforce-budget gets the enforced verdict."""
    register = gate_budgets.load(ceiling_relaxed(tmp_path))
    assert judge_pull_request(register, 210.0, pull_request=False).failed
    assert judge_pull_request(register, 210.0, force=True).failed


def test_the_ceiling_relaxation_is_held_to_the_tracked_advisory_contract(
    tmp_path: Path,
) -> None:
    """No bead, no reason or no hang detector is refused; an enforcing declaration that
    still names a tracker or a hang detector is refused; enforcing with neither is None."""
    for missing in ("bead", "reason", "hang", "per_test"):
        with pytest.raises(BudgetError):
            gate_budgets.load(ceiling_relaxed(tmp_path, **{missing: None}))
    with pytest.raises(BudgetError, match="must exceed 1"):
        gate_budgets.load(ceiling_relaxed(tmp_path, hang="1.0"))
    with pytest.raises(BudgetError, match="still declares a hang detector"):
        gate_budgets.load(
            ceiling_relaxed(tmp_path, enforcement="enforcing", bead=None, reason=None)
        )
    enforcing = gate_budgets.load(
        ceiling_relaxed(
            tmp_path, enforcement="enforcing", bead=None, reason=None, hang=None, per_test=None
        )
    )
    assert enforcing.policy.pull_request_ceiling is None


def test_an_advisory_ceiling_must_be_tracked_by_an_open_bead(tmp_path: Path) -> None:
    """The same liveness ratchet the relaxed drift and stale rules are held to."""
    read = bead_state.fixture_store({"aaaa": "open", "cccc": "closed"})
    assert relative_rule_problems(gate_budgets.load(ceiling_relaxed(tmp_path)), read) == []
    closed = relative_rule_problems(
        gate_budgets.load(ceiling_relaxed(tmp_path, bead="think-cccc")), read
    )
    assert len(closed) == 1, closed
    assert "policy.pull_request_ceiling.enforcement" in closed[0]
    assert "under think-cccc: closed" in closed[0]
