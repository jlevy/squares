"""All benchmark views admit the same canonical, finite packing snapshot."""

from __future__ import annotations

import argparse
import math
from dataclasses import replace
from pathlib import Path
from typing import cast

import pytest
from workbench_tools.trial_records import (
    EffectiveConfiguration,
    RepairReceipt,
    SourceReceipt,
    Trial,
    admission_reason,
    canonical_reference,
    gap_closed,
    trial_from_json,
    trial_from_probe,
    trial_from_row,
    trial_to_json,
)

from devtools import bench_annealing as bench
from devtools.known_structure import record


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
        configuration=EffectiveConfiguration(
            style="bodies", mode="blind", seed=seed, inflate=1.12, anneal=3
        ),
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
    assert "undefined for every zero reference-gap control" in capsys.readouterr().out


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
    bad = replace(good, seed=1, resolved_closed=999.0, resolved_poses=None)
    monkeypatch.setattr(bench, "RESULTS", tmp_path)
    monkeypatch.setattr(bench, "run_trials", lambda _run: [good, bad])
    args = argparse.Namespace(
        sweep=["anneal=6"], n=[5], style="bodies", inflate=None, anneal=6, budget=1.0
    )
    assert bench.sweep(args, [0, 1], "fixture") == 0
    output = capsys.readouterr().out
    assert "999.000" not in output
    assert "REFUSED 1 of 2" in output


@pytest.mark.parametrize(
    "spec",
    [
        ["unknown=1"],
        ["anneal=11"],
        ["inflate=0.9"],
        ["anneal=3", "anneal=4"],
    ],
)
def test_sweep_rejects_options_the_probe_cannot_honor(spec: list[str]) -> None:
    with pytest.raises((ValueError, argparse.ArgumentTypeError)):
        bench.parse_grid(spec)
