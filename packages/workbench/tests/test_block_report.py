"""Independent seed slots, unsuccessful blocks, and explicit report denominators."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import pytest
from workbench_tools import block_report
from workbench_tools.cohort_manifest import (
    SCHEMA,
    Attempt,
    AttemptStatus,
    Cohort,
    Manifest,
    Partition,
    read_manifest,
    strict_json,
)
from workbench_tools.trial_records import (
    EffectiveConfiguration,
    RepairReceipt,
    SourceReceipt,
    Trial,
    admission_reason,
    canonical_reference,
)

from devtools.known_structure import record


def _trial(seed: int, *, reached: bool = True) -> Trial:
    matrix, side = record(5)
    poses = tuple((float(row[0]), float(row[1]), float(row[2])) for row in matrix)
    grid = ((0.5, 0.5, 0.0), (1.5, 0.5, 0.0), (2.5, 0.5, 0.0), (0.5, 1.5, 0.0), (1.5, 1.5, 0.0))
    result_side = side if reached else 3.0
    return Trial(
        n=5,
        seed=seed,
        style="bodies",
        excess=(result_side / side - 1) * 100,
        side=result_side,
        record=side,
        closed=1.0 if reached else 0.0,
        overlap=0.0,
        resolved_side=result_side,
        resolved_closed=1.0 if reached else 0.0,
        resolved_overlap=0.0,
        steps=20,
        ms=1.0,
        centre=0.0,
        angle=0.0,
        poses=poses if reached else grid,
        resolved_poses=poses if reached else grid,
    )


@pytest.fixture
def admit_test_geometry(monkeypatch: pytest.MonkeyPatch) -> None:
    # Admission has its own geometry/provenance controls. Isolate arithmetic here so an
    # independently changing record format cannot conceal a denominator regression.
    monkeypatch.setattr(
        block_report,
        "admission_reason",
        lambda trial: "missing-geometry" if trial.resolved_poses is None else None,
    )


def _cohort(attempts: tuple[Attempt, ...], block_size: int = 2) -> Cohort:
    return Cohort(
        "control", 5, "bodies", {}, Partition.EXPLORATORY, block_size, 100, 400, attempts
    )


@pytest.mark.usefixtures("admit_test_geometry")
def test_disjoint_blocks_keep_failures_cancellation_and_trailing_slots() -> None:
    cohort = _cohort(
        (
            Attempt(0, AttemptStatus.COMPLETED),
            Attempt(1, AttemptStatus.COMPLETED),
            Attempt(2, AttemptStatus.FAILED, steps=5),
            Attempt(3, AttemptStatus.COMPLETED),
            Attempt(4, AttemptStatus.NOT_STARTED),
            Attempt(5, AttemptStatus.CANCELLED, 3, 0.3),
            Attempt(6, AttemptStatus.COMPLETED),
        )
    )
    result = block_report.summarize_cohort(
        cohort,
        [
            _trial(0),
            replace(_trial(1), resolved_poses=None),
            _trial(3, reached=False),
            _trial(6),
        ],
        tolerance_pct=0.0001,
    )
    assert result["counts"] == {
        "planned": 7,
        "attempted": 6,
        "completed": 4,
        "failed": 1,
        "cancelled": 1,
        "not-started": 1,
        "accepted": 3,
        "rejected": 1,
    }
    _assert_rate(result["trial_success_per_attempt"], 2, 6, 1 / 3)
    _assert_rate(result["trial_success_conditional_on_validity"], 2, 3, 2 / 3)
    _assert_rate(result["block_success_per_planned_block"], 1, 3, 1 / 3)
    _assert_rate(result["block_success_per_completed_block"], 1, 2, 0.5)
    assert result["trailing_partial_block_seeds"] == [6]
    assert result["blocks_without_valid_result"] == 1
    assert result["work"] == {
        "max_steps_per_attempt": 100,
        "repair_budget": 400,
        "measured_steps": 88,
        "attempts_with_unknown_steps": 0,
        "measured_milliseconds": 4.3,
        "attempts_with_unknown_time": 1,
        "measured_repair_sweeps": 0,
        "measured_physics_milliseconds": 0.0,
        "measured_repair_milliseconds": 0.0,
        "attempts_with_unknown_repair": 6,
    }
    blocks = result["blocks"]
    assert isinstance(blocks, list)
    assert [block["seeds"] for block in blocks] == [[0, 1], [2, 3], [4, 5]]
    assert [block["best_seed"] for block in blocks] == [0, 3, None]
    json.dumps(result, allow_nan=False)


@pytest.mark.usefixtures("admit_test_geometry")
def test_empty_and_all_rejected_populations_have_no_invented_score() -> None:
    empty = block_report.summarize_cohort(_cohort(()), [], tolerance_pct=0.0)
    assert empty["block_success_per_planned_block"] == {
        "hits": 0,
        "denominator": 0,
        "rate": None,
        "wilson_95": None,
    }
    rejected = block_report.summarize_cohort(
        _cohort((Attempt(0, AttemptStatus.COMPLETED),), 1),
        [replace(_trial(0), resolved_poses=None)],
        tolerance_pct=0.0,
    )
    assert rejected["blocks_without_valid_result"] == 1
    assert rejected["best_relative_excess_pct_conditional_on_validity"] == {
        "count": 0,
        "min": None,
        "median": None,
        "max": None,
    }
    _assert_rate(rejected["trial_success_per_attempt"], 0, 1, 0.0)


@pytest.mark.usefixtures("admit_test_geometry")
def test_zero_gap_is_undefined_normalization_not_an_infinite_score() -> None:
    cohort = replace(_cohort((Attempt(0, AttemptStatus.COMPLETED),), 1), n=4)
    trial = replace(_trial(0), n=4, record=2.0, side=2.0, resolved_side=2.0)
    result = block_report.summarize_cohort(cohort, [trial], tolerance_pct=0.0)
    assert result["best_grid_gap_closed_conditional_on_defined_score"] == {
        "count": 0,
        "min": None,
        "median": None,
        "max": None,
    }
    _assert_rate(result["block_success_per_planned_block"], 1, 1, 1.0)
    json.dumps(result, allow_nan=False)


def test_duplicate_missing_and_mismatched_rows_cannot_change_block_membership() -> None:
    cohort = _cohort((Attempt(0, AttemptStatus.COMPLETED),), 1)
    for rows in (
        [],
        [_trial(0), _trial(0)],
        [_trial(1)],
        [replace(_trial(0), params={"anneal": 99})],
    ):
        with pytest.raises(ValueError, match=r"duplicate|configuration|manifest"):
            block_report.summarize_cohort(cohort, rows, tolerance_pct=0.0)


def _manifest_value() -> dict[str, object]:
    return {
        "schema": SCHEMA,
        "source_commit": "a" * 40,
        "reference_source": "known-best/control",
        "instrument": "packages/workbench/probes/bench-annealing.ts",
        "purpose": "software-validation",
        "cohorts": [
            {
                "id": "control",
                "n": 5,
                "style": "bodies",
                "params": {},
                "partition": "tuning",
                "block_size": 1,
                "max_steps": 100,
                "repair_budget": 400,
                "attempts": [{"seed": 0, "status": "completed"}],
            }
        ],
    }


def test_manifest_roundtrip_and_explicit_work_partition() -> None:
    value = read_manifest(json.loads(json.dumps(_manifest_value())))
    assert isinstance(value, Manifest)
    assert value.cohorts[0].attempts == (Attempt(0, AttemptStatus.COMPLETED),)
    assert value.cohorts[0].partition is Partition.TUNING


@pytest.mark.parametrize(
    ("field", "value"),
    [("source_commit", "HEAD"), ("schema", "unknown"), ("unrecognized", True)],
)
def test_manifest_rejects_unversioned_or_ambiguous_metadata(field: str, value: object) -> None:
    with pytest.raises(ValueError, match=r"revision|schema|fields"):
        read_manifest(_manifest_value() | {field: value})


def test_manifest_refuses_seed_leakage_and_duplicate_seed_slots() -> None:
    value = _manifest_value()
    cohorts = value["cohorts"]
    assert isinstance(cohorts, list)
    original = cohorts[0]
    assert isinstance(original, dict)
    with pytest.raises(ValueError, match="disjoint"):
        read_manifest(
            value
            | {"cohorts": [original, original | {"id": "holdout", "partition": "held-out"}]}
        )
    with pytest.raises(ValueError, match="unique"):
        read_manifest(
            value
            | {"cohorts": [original | {"attempts": [{"seed": 0, "status": "completed"}] * 2}]}
        )


def test_wilson_interval_matches_known_all_failure_control() -> None:
    low, high = block_report.wilson_interval(0, 10) or (-1.0, -1.0)
    assert low == 0.0
    assert high == pytest.approx(0.2775327999)


def _assert_rate(value: object, hits: int, denominator: int, expected: float) -> None:
    assert isinstance(value, dict)
    assert value["hits"] == hits
    assert value["denominator"] == denominator
    assert value["rate"] == pytest.approx(expected)


def _verified_trial(seed: int = 0) -> Trial:
    return replace(
        _trial(seed),
        record_source=canonical_reference(5).source,
        configuration=EffectiveConfiguration("bodies", "blind", seed, 1.12, 3),
        source=SourceReceipt(
            commit="a" * 40,
            dirty=False,
            page="packing/site/workbench/index.html",
            page_sha256="b" * 64,
            benchmark="packages/workbench/probes/bench-annealing.ts",
            browser="chromium",
            browser_version="fixture",
            browser_executable="/fixture/chromium",
            playwright_version="fixture",
            python_version="3.14.7",
            platform="fixture",
            viewport_width=1920,
            viewport_height=1080,
        ),
        repair=RepairReceipt(
            sweeps=1, sweep_limit=400, converged=True, physics_ms=0.4, repair_ms=0.1
        ),
    )


def test_manifest_cli_replays_canonical_geometry_and_retains_work(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    manifest = _manifest_value() | {"reference_source": "packing/witnesses/known-best"}
    trial = _verified_trial()
    assert admission_reason(trial) is None
    manifest_path, rows_path, output_path = (
        tmp_path / "manifest.json",
        tmp_path / "trials.jsonl",
        tmp_path / "report.json",
    )
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    rows_path.write_text(
        json.dumps({"cohort": "control", "trial": trial.row()}, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(
        "sys.argv",
        ["block-report", str(manifest_path), str(rows_path), "--out", str(output_path)],
    )
    assert block_report.main() == 0
    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["cohorts"][0]["counts"]["accepted"] == 1
    assert result["cohorts"][0]["work"]["measured_repair_sweeps"] == 1
    assert result["cohorts"][0]["work"]["measured_physics_milliseconds"] == 0.4
    assert result["cohorts"][0]["work"]["measured_repair_milliseconds"] == 0.1
    assert result["cohorts"][0]["blocks"][0]["best_seed"] == 0
    assert trial.source is not None
    assert result["cohorts"][0]["source"] == trial.source.row()
    assert result["cohorts"][0]["effective_configuration"]["inflate"] == 1.12
    assert result["cohorts"][0]["effective_configuration"]["anneal"] == 3


def test_manifest_prevents_source_reference_and_research_provenance_substitution() -> None:
    manifest = read_manifest(
        _manifest_value() | {"reference_source": "packing/witnesses/known-best"}
    )
    good = _verified_trial()
    source = good.source
    assert source is not None
    for trial in (
        replace(good, source=replace(source, commit="f" * 40)),
        replace(good, source=replace(source, benchmark="different")),
        replace(good, record_source="other/n-005.yaml"),
    ):
        with pytest.raises(ValueError, match="manifest"):
            block_report.report(manifest, {"control": [trial]})
    research = read_manifest(
        _manifest_value()
        | {"purpose": "research", "reference_source": "packing/witnesses/known-best"}
    )
    with pytest.raises(ValueError, match="committed instrument"):
        block_report.report(
            research, {"control": [replace(good, source=replace(source, dirty=True))]}
        )


def test_a_trial_that_exceeds_declared_work_cannot_win_a_block() -> None:
    trial = _verified_trial()
    assert trial.repair is not None
    too_many_steps = replace(trial, steps=101)
    wrong_repair_budget = replace(trial, repair=replace(trial.repair, sweep_limit=500))
    for candidate in (too_many_steps, wrong_repair_budget):
        result = block_report.summarize_cohort(
            _cohort((Attempt(0, AttemptStatus.COMPLETED),), 1), [candidate], tolerance_pct=0.001
        )
        assert result["blocks_without_valid_result"] == 1


def test_identical_overrides_cannot_hide_different_effective_defaults() -> None:
    first, second = _verified_trial(0), _verified_trial(1)
    assert second.configuration is not None
    changed = replace(
        second, configuration=replace(second.configuration, inflate=1.5, anneal=9)
    )
    assert admission_reason(changed) is None
    cohort = _cohort((Attempt(0, AttemptStatus.COMPLETED), Attempt(1, AttemptStatus.COMPLETED)))
    with pytest.raises(ValueError, match="one effective configuration"):
        block_report.summarize_cohort(cohort, [first, changed], tolerance_pct=0.001)


@pytest.mark.parametrize("token", ["NaN", "Infinity", "-Infinity"])
def test_nonstandard_numeric_tokens_are_refused_before_manifest_or_trial_admission(
    token: str,
) -> None:
    with pytest.raises(ValueError, match="nonfinite JSON token"):
        strict_json('{"trial":{"ms":' + token + "}}")
