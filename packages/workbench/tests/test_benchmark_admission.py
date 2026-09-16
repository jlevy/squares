"""All benchmark views admit the same canonical, finite packing snapshot."""

from __future__ import annotations

import argparse
import math
from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest

from devtools.known_structure import record
from workbench_tools import benchmark as bench
from workbench_tools.trial_records import (
    VALIDITY_TOLERANCE,
    BeatTiming,
    EffectiveConfiguration,
    PackingReference,
    PhysicsLaw,
    RepairReceipt,
    SourceReceipt,
    Trial,
    admission_reason,
    canonical_reference,
    check_success_band,
    gap_closed,
    partition_trials,
    trial_from_json,
    trial_from_probe,
    trial_from_row,
    trial_to_json,
)


def configuration(
    seed: int, *, anneal: int = 3, rigidity: float = 0.15
) -> EffectiveConfiguration:
    """A browser configuration with the law and beat a trial must record."""
    return EffectiveConfiguration(
        style="bodies",
        mode="blind",
        seed=seed,
        inflate=1.12,
        anneal=anneal,
        pair_law=PhysicsLaw(rigidity=rigidity, repulsion=2500, attraction=0, range=0),
        wall_law=PhysicsLaw(rigidity=0.25, repulsion=2500, attraction=0, range=0),
        timing=BeatTiming(dwell=0.6, move=0.8, correct=0.25, settle=0.4),
        anneal_span=0.95,
    )


def _source() -> SourceReceipt:
    return SourceReceipt(
        commit="0" * 40,
        dirty=False,
        page="packing/site/workbench/index.html",
        page_sha256="1" * 64,
        benchmark="packages/workbench/probes/bench-annealing.ts",
        browser="chromium",
        browser_version="test",
        browser_executable="/test/chromium",
        playwright_version="test",
        python_version="3.14.0",
        platform="test",
        viewport_width=1920,
        viewport_height=1080,
    )


def _trial(n: int = 5, *, seed: int = 0) -> Trial:
    array, side = record(n)
    poses = tuple((float(row[0]), float(row[1]), float(row[2])) for row in array)
    reference = canonical_reference(n)
    excess = (side / reference.side - 1) * 100
    return Trial(
        n=n,
        seed=seed,
        style="bodies",
        excess=excess,
        side=side,
        record=reference.side,
        closed=gap_closed(n, reference.side, excess),
        overlap=0.0,
        resolved_side=side,
        resolved_closed=gap_closed(n, reference.side, excess),
        resolved_overlap=0.0,
        steps=20,
        ms=1.0,
        centre=0.0,
        angle=0.0,
        params={},
        poses=poses,
        resolved_poses=poses,
        record_source=reference.source,
        configuration=configuration(seed),
        source=_source(),
        repair=RepairReceipt(
            sweeps=0,
            sweep_limit=400,
            converged=True,
            physics_ms=0.4,
            repair_ms=0.1,
        ),
    )


@pytest.mark.parametrize(
    "field",
    [
        "side",
        "record",
        "excess",
        "closed",
        "overlap",
        "resolved_side",
        "resolved_closed",
        "resolved_overlap",
        "ms",
    ],
)
@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_ranked_values_are_refused(field: str, value: float) -> None:
    assert not bench.valid([replace(_trial(), **{field: value})])


def test_scalar_pass_does_not_admit_missing_or_wrong_repaired_geometry() -> None:
    good = _trial()
    assert good.resolved_poses is not None
    overlapping = tuple((1.0, 1.0, 0.0) for _ in range(good.n))
    outside = ((-0.1, 1.0, 0.0), *good.resolved_poses[1:])
    for poses in (None, (), good.resolved_poses[:1], overlapping, outside):
        assert not bench.valid([replace(good, resolved_poses=poses)])
    assert bench.valid([good]) == [good]


def test_canonical_reference_cannot_be_replaced_by_a_self_consistent_claim() -> None:
    good = _trial()
    forged_record = 2.75
    forged_excess = (good.side / forged_record - 1) * 100
    forged = replace(
        good,
        record=forged_record,
        excess=forged_excess,
        closed=gap_closed(good.n, forged_record, forged_excess),
        resolved_closed=gap_closed(good.n, forged_record, forged_excess),
    )
    assert admission_reason(forged) == "reference-mismatch"


def test_raw_geometry_must_agree_with_overlap_side_and_origin_receipts() -> None:
    good = _trial()
    assert good.poses is not None
    coincident = (good.poses[0], good.poses[0], *good.poses[2:])
    assert admission_reason(replace(good, poses=coincident, overlap=0.0)) == (
        "inconsistent-raw-overlap"
    )
    translated = tuple((x + 0.1, y + 0.1, angle) for x, y, angle in good.poses)
    assert admission_reason(replace(good, poses=translated)) == "raw-geometry"
    larger_side = good.side + 0.1
    assert (
        admission_reason(
            replace(
                good,
                side=larger_side,
                excess=(larger_side / good.record - 1) * 100,
            )
        )
        == "inconsistent-raw-side"
    )
    assert admission_reason(replace(good, excess=1.0)) == "inconsistent-excess"


def test_effective_configuration_source_and_repair_receipts_are_enforced() -> None:
    good = _trial()
    assert good.configuration is not None
    assert good.source is not None
    assert good.repair is not None
    mismatch = replace(
        good,
        params={"anneal": 6},
        configuration=replace(good.configuration, anneal=5),
    )
    assert admission_reason(mismatch) == "configuration-mismatch"
    assert admission_reason(replace(good, source=replace(good.source, dirty=True))) == (
        "unreproducible-source"
    )
    assert (
        admission_reason(replace(good, repair=replace(good.repair, sweeps=401)))
        == "invalid-repair-receipt"
    )
    assert (
        admission_reason(replace(good, repair=replace(good.repair, converged=False)))
        == "inconsistent-repair-receipt"
    )


def test_zero_reference_gap_grid_control_is_valid_without_a_normalized_score(
    capsys: pytest.CaptureFixture[str],
) -> None:
    grid = _trial(4)
    assert grid.closed is None
    assert grid.resolved_closed is None
    assert admission_reason(grid) is None
    assert bench.report([grid]) == 0
    output = capsys.readouterr().out
    assert "undefined for every zero reference-gap control" in output
    assert "absolute container side" in output
    assert "only column that compares across n" not in output


def test_malformed_runtime_values_fail_closed_without_raising() -> None:
    good = _trial()
    fractional_n = replace(good, n=cast(int, 1.5))
    assert admission_reason(fractional_n) == "invalid-configuration"

    row = good.row()
    row["poses"] = [[10**1000, 0.5, 0.0]]
    assert admission_reason(trial_from_row(row)) == "missing-geometry"

    row = good.row()
    row["params"] = {"inflate": 10**1000}
    assert admission_reason(trial_from_row(row)) == "invalid-requested-configuration"


def test_versioned_json_adapter_is_strict_and_round_trips() -> None:
    good = _trial()
    assert trial_from_json(trial_to_json(good)) == good
    with pytest.raises(ValueError, match="non-standard JSON"):
        trial_from_json('{"resolved_side":NaN}')
    with pytest.raises(ValueError, match="Out of range float"):
        trial_to_json(replace(good, resolved_side=math.nan))


def test_browser_probe_adapter_requires_exact_fields_and_preserves_receipts() -> None:
    good = _trial()
    assert good.poses is not None
    result: dict[str, object] = {
        "configuration": {
            "style": "bodies",
            "mode": "blind",
            "seed": 0,
            "inflate": 1.12,
            "anneal": 3,
            "pairLaw": {"rigidity": 0.15, "repulsion": 2500, "attraction": 0, "range": 0},
            "wallLaw": {"rigidity": 0.25, "repulsion": 2500, "attraction": 0, "range": 0},
            "timing": {"dwell": 0.6, "move": 0.8, "correct": 0.25, "settle": 0.4},
            "annealSpan": 0.95,
        },
        "excess": good.excess,
        "side": good.side,
        "record": good.record,
        "centre": 0.0,
        "angle": 0.0,
        "overlap": 0.0,
        "poses": good.poses,
        "resolvedPoses": good.poses,
        "resolvedSide": good.side,
        "resolvedOverlap": 0.0,
        "repairSweeps": 0,
        "repairSweepLimit": 400,
        "repairConverged": True,
        "steps": 20,
        "physicsMs": 0.4,
        "repairMs": 0.1,
        "ms": 1.0,
    }
    adapted = trial_from_probe(
        result,
        n=5,
        seed=0,
        style="bodies",
        params={},
        source=_source(),
    )
    assert admission_reason(adapted) is None
    assert adapted.configuration is not None
    assert adapted.configuration.inflate == 1.12
    assert adapted.repair is not None
    assert adapted.repair.sweep_limit == 400
    with pytest.raises(ValueError, match="unexpected or missing"):
        trial_from_probe(
            {**result, "ignored": True},
            n=5,
            seed=0,
            style="bodies",
            params={},
            source=_source(),
        )


def test_missing_legacy_metrics_stay_readable_but_cannot_rank() -> None:
    row = _trial().row()
    del row["resolved_overlap"]
    del row["resolved_poses"]
    assert not bench.valid([bench.trial_from_row(row)])


def test_report_counts_bad_rows_without_crashing(capsys: pytest.CaptureFixture[str]) -> None:
    bad = replace(_trial(), resolved_overlap=float("nan"))
    assert bench.report([bad]) == 1
    assert "REFUSED 1 of 1" in capsys.readouterr().out


def test_sweep_cannot_rank_an_invalid_high_score(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    good = _trial()
    assert good.configuration is not None
    bad = replace(
        good,
        seed=1,
        configuration=replace(good.configuration, seed=1),
        resolved_closed=999.0,
        resolved_poses=None,
    )
    monkeypatch.setattr(bench, "RESULTS", tmp_path)
    monkeypatch.setattr(
        bench,
        "run_trials",
        lambda _run: bench.RunResult(
            planned=[(5, 0), (5, 1)], trials=[good, bad], failures=[], stopped_early=False
        ),
    )
    args = argparse.Namespace(
        sweep=["anneal=6"], n=[5], style="bodies", inflate=None, anneal=6, budget=1.0
    )
    assert bench.sweep(args, [0, 1], "fixture") == 0
    output = capsys.readouterr().out
    assert "999.000" not in output
    assert "REFUSED 1 of 2 trials: missing-geometry=1" in output


@pytest.mark.parametrize(
    "spec",
    [
        ["unknown=1"],
        ["anneal=21"],
        ["inflate=0.9"],
        ["anneal=3", "anneal=4"],
    ],
)
def test_sweep_rejects_options_the_probe_cannot_honor(spec: list[str]) -> None:
    with pytest.raises((ValueError, argparse.ArgumentTypeError)):
        bench.parse_grid(spec)


def _pressed(p: float, *, reported: float = 0.0, converged: bool = True) -> Trial:
    """The n = 5 record with its top-left corner square pressed `p` into the central square.

    The record's side is unchanged, so only the repaired arrangement's overlap differs from an
    admitted trial; `reported` is the overlap the forged receipt claims.
    """
    good = _trial()
    assert good.resolved_poses is not None
    assert good.repair is not None
    shift = p / math.sqrt(2)
    (x, y, angle), *rest = good.resolved_poses
    return replace(
        good,
        resolved_poses=((x + shift, y - shift, angle), *rest),
        resolved_overlap=reported,
        repair=replace(good.repair, converged=converged),
    )


@pytest.mark.parametrize(
    ("penetration", "reason"),
    [
        (5e-10, None),
        (2e-9, "invalid-packing"),
        (5e-6, "invalid-packing"),
        (2e-5, "invalid-packing"),
    ],
)
def test_repaired_geometry_is_admitted_only_under_the_validity_contract(
    penetration: float, reason: str | None
) -> None:
    assert admission_reason(_pressed(penetration)) == reason


def test_a_non_converged_repair_is_refused_even_when_its_residual_is_small() -> None:
    residual = 5e-6
    assert admission_reason(_pressed(residual, reported=residual, converged=False)) == (
        "repair-not-converged"
    )


def test_a_reported_side_below_the_fitted_box_puts_squares_through_its_walls() -> None:
    good = _trial()
    slack = 5e-6
    shrunk = good.resolved_side - slack
    excess = (shrunk / good.record - 1) * 100
    below = replace(
        good, resolved_side=shrunk, resolved_closed=gap_closed(good.n, good.record, excess)
    )
    assert admission_reason(below) == "invalid-packing"


def test_a_valid_arrangement_below_the_record_is_refused_as_needing_exact_verification() -> (
    None
):
    good = _trial()
    canonical = canonical_reference(good.n)
    larger = PackingReference(n=good.n, side=good.side + 0.01, source=canonical.source)
    excess = (good.side / larger.side - 1) * 100
    beats = replace(
        good,
        record=larger.side,
        excess=excess,
        closed=gap_closed(good.n, larger.side, excess),
        resolved_closed=gap_closed(good.n, larger.side, excess),
    )
    assert admission_reason(beats, reference_for=lambda _n: larger) == "below-record"
    at_record = replace(good)
    assert admission_reason(at_record) is None
    kept, refused = partition_trials([beats], reference_for=lambda _n: larger)
    assert kept == []
    assert refused == {"below-record": 1}


def test_report_names_below_record_trials_separately_from_other_refusals(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    good = _trial()
    canonical = canonical_reference(good.n)
    larger = PackingReference(n=good.n, side=good.side + 0.01, source=canonical.source)
    excess = (good.side / larger.side - 1) * 100
    beats = replace(
        good,
        seed=1,
        configuration=replace(cast(EffectiveConfiguration, good.configuration), seed=1),
        record=larger.side,
        excess=excess,
        closed=gap_closed(good.n, larger.side, excess),
        resolved_closed=gap_closed(good.n, larger.side, excess),
    )
    real = bench.partition_trials
    monkeypatch.setattr(
        bench,
        "partition_trials",
        lambda trials: real(
            trials, reference_for=lambda n: larger if n == good.n else canonical
        ),
    )
    assert bench.report([beats]) == 1
    output = capsys.readouterr().out
    assert "BELOW RECORD 1" in output
    assert "exact verification" in output


def test_a_success_band_finer_than_the_validity_tolerance_is_refused() -> None:
    record_side = canonical_reference(5).side
    with pytest.raises(ValueError, match="finer than the validity tolerance"):
        check_success_band(1e-8, record_side)
    check_success_band(bench.TOLERANCES["exact"], 1.0)
    for name, band in bench.TOLERANCES.items():
        assert band / 100 >= VALIDITY_TOLERANCE, name


def test_a_written_row_says_whether_each_side_belongs_to_a_packing() -> None:
    good = _trial()
    assert good.poses is not None
    row = good.row()
    assert (row["raw_valid"], row["resolved_valid"]) == (True, True)
    coincident = replace(good, poses=(good.poses[0], good.poses[0], *good.poses[2:]))
    assert coincident.row()["raw_valid"] is False
    overlapping = _pressed(2e-9)
    assert overlapping.row()["resolved_valid"] is False
    assert replace(good, resolved_poses=None).row()["resolved_valid"] is False
    assert trial_from_json(trial_to_json(overlapping)) == overlapping


def test_a_configuration_without_its_pair_law_and_timing_is_refused() -> None:
    good = _trial()
    row = good.row()
    legacy = cast(dict[str, object], row["configuration"])
    for recorded in ("pair_law", "wall_law", "timing", "anneal_span"):
        del legacy[recorded]
    legacy["contract"] = "packing.squares:AnnealingConfiguration/v1"
    assert admission_reason(trial_from_row(row)) == "unsupported-configuration-contract"
    assert good.configuration is not None
    for broken in (
        replace(
            good.configuration, pair_law=replace(good.configuration.pair_law, rigidity=0.0)
        ),
        replace(good.configuration, timing=replace(good.configuration.timing, move=math.nan)),
        replace(good.configuration, anneal_span=-1.0),
    ):
        assert admission_reason(replace(good, configuration=broken)) == (
            "invalid-effective-configuration"
        )


def test_trials_under_different_pair_laws_stay_apart() -> None:
    before = _trial(seed=0)
    after = replace(_trial(seed=1), configuration=configuration(1, rigidity=0.35))
    assert admission_reason(before) is None
    assert admission_reason(after) is None
    assert before.row()["configuration"] != {
        **cast(dict[str, object], after.row()["configuration"]),
        "seed": 0,
    }
    assert trial_from_json(trial_to_json(after)) == after
    with pytest.raises(ValueError, match="mixes effective configurations"):
        bench.replay_groups([before, after])
