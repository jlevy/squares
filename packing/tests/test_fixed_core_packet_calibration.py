"""Known-answer and lifecycle controls for the fixed-core packet calibration."""

# The calibration deliberately reuses private generic row/readback primitives while
# keeping a closed outer state machine. These tests exercise that integration seam.
# pyright: reportPrivateUsage=false
# ruff: noqa: SLF001

from __future__ import annotations

import ast
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
from collections.abc import Callable
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from pathlib import Path
from typing import cast
from unittest.mock import patch

import pytest

from devtools import calibrate_fixed_core_packet as calibration
from devtools.dilation_corollary import (
    build_limit_record,
)
from devtools.fixed_core_packet import (
    RUNTIME_ATTESTATION_SCOPE,
    PacketError,
    RawMinimum,
    WorkerTaskObservation,
    _direction_digest,
    _reconstruct_dilation_directions,
    _reconstruct_raw_directions,
    run_exact_route,
    run_interval_route,
    run_raw_sweep,
)
from devtools.fixed_core_packet import load_result as load_scientific_result
from sqpack.fractional.threshold import (
    ThresholdCertificate,
    exact_charge,
    expansion_terms,
)

REPOSITORY = Path(__file__).resolve().parents[2]
FIXTURE = REPOSITORY / calibration.FIXTURE_PATH
REVISION = "a" * 40


def _fixture() -> tuple[ThresholdCertificate, dict[str, object]]:
    return calibration.load_fixture(FIXTURE.read_bytes())


def _normalized(certificate: ThresholdCertificate) -> ThresholdCertificate:
    return replace(
        certificate,
        atoms=tuple(
            replace(atom, weight=atom.weight * calibration.NORMALIZATION_ALPHA)
            for atom in certificate.atoms
        ),
        threshold_atoms=tuple(
            replace(atom, weight=atom.weight * calibration.NORMALIZATION_ALPHA)
            for atom in certificate.threshold_atoms
        ),
    )


def _small(
    certificate: ThresholdCertificate, *, normalized: bool = False
) -> ThresholdCertificate:
    reduced = replace(
        certificate,
        half_tangents=(Fraction(0), calibration.FIXTURE_HALF_GAP),
    )
    return _normalized(reduced) if normalized else reduced


def _seed(output: Path, *, invocation_started: float | None = None) -> dict[str, object]:
    started = time.perf_counter() if invocation_started is None else invocation_started
    document = calibration.initial_document(
        REVISION,
        workers=1,
        calibration_seconds=1.0,
        external_seconds=2.0,
        grace_seconds=0.05,
        invocation_started=started,
        run_order=1,
        cache_observation="test process; cache state unmeasured",
        background_load="test host; background load unmeasured",
    )
    calibration.write_result(output, document)
    return document


def _terminal_candidate_summary(
    output: Path | None = None,
    *,
    coordinator_pid: int = 101,
) -> dict[str, object]:
    document = calibration.initial_document(
        REVISION,
        workers=1,
        calibration_seconds=4.0,
        external_seconds=5.0,
        grace_seconds=0.05,
        invocation_started=0.0,
        run_order=1,
        cache_observation="no-kernel publication control",
        background_load="unmeasured",
    )
    document.update(
        phase="awaiting-worker-exit",
        error="parent has not observed worker exit",
    )
    cast(dict[str, object], document["raw"]).update(
        directions_completed=calibration.RAW_DIRECTIONS,
        completed_directions=list(range(calibration.RAW_DIRECTIONS)),
        observed_minimum_upper_bound="2",
        observed_argmin=0,
        observed_witness=["3/8", "3/8"],
        raw_minimum="2",
        comparison="passed",
        witness_replay_charge="2",
        witness_admissible=True,
        directions_sha256="a" * 64,
    )
    document["normalized"] = {
        "path": "candidate.json",
        "sha256": "b" * 64,
        "source_fixture_sha256": calibration.FIXTURE_SHA256,
        "id": calibration.NORMALIZED_ID,
        "alpha": "1/2",
        "point_mass": "1/4",
        "threshold_budget": "3/4",
        "total_budget": "1",
        "least_cell_charge": "1",
        "integer_scale": 8,
        "closed_form_conditions": [],
    }
    common: dict[str, object] = {
        "status": "complete",
        "source_sha256": "b" * 64,
        "directions_expected": calibration.RAW_DIRECTIONS,
        "directions_completed": calibration.RAW_DIRECTIONS,
        "completed_directions": list(range(calibration.RAW_DIRECTIONS)),
        "directions_sha256": "a" * 64,
    }
    routes = cast(dict[str, object], document["routes"])
    routes["normalized_exact"] = common | {
        "minimum": "1",
        "argmin": 0,
        "witness": ["3/8", "3/8"],
        "dense_slab_disagreements": 0,
    }
    routes["reflected_interval"] = common | {
        "directions_expected": calibration.INTERVAL_DIRECTIONS,
        "directions_completed": calibration.INTERVAL_DIRECTIONS,
        "completed_directions": list(calibration._interval_labels()),
        "integer_scale": 8,
        "integer_enclosure": [8, 8],
        "enclosure": ["1", "1"],
        "stalled": 0,
        "budget_exhausted": 0,
        "accepted": True,
        "boxes_observed": calibration.INTERVAL_DIRECTIONS,
    }
    routes["dilation"] = common | {
        "completed_directions": [str(index) for index in range(calibration.RAW_DIRECTIONS)],
        "record_sha256": "c" * 64,
        "generic_record_schema": calibration.THRESHOLD_LIMIT_RECORD_SCHEMA,
        "generic_record_scope": (
            "valid normalized n=2 calibration fixture; no campaign or fixed-packet evidence"
        ),
        "factor_supremum": "2*sqrt(33177601)/5761",
        "factor_supremum_squared": "132710404/33189121",
        "bounded_side": "3*sqrt(33177601)/11522",
        "bounded_side_squared": "298598409/132756484",
        "relation": ">=",
        "endpoint_certificate": False,
        "requires_compactness": False,
    }
    cast(dict[str, object], document["resources"]).update(
        cpu_observations={
            "coordinator_start_seconds": 0.0,
            "coordinator_end_seconds": 0.1,
            "direct_children_user_start_seconds": 0.0,
            "direct_children_user_end_seconds": 0.0,
            "direct_children_system_start_seconds": 0.0,
            "direct_children_system_end_seconds": 0.0,
        },
        coordinator_process_seconds=0.1,
        reaped_direct_children_user_seconds=0.0,
        reaped_direct_children_system_seconds=0.0,
    )
    for key in cast(dict[str, object], document["clocks"]):
        if key != "phase_duration_scope":
            cast(dict[str, object], document["clocks"])[key] = 0.01
    cast(dict[str, object], document["clocks"])["worker_elapsed_seconds"] = 0.2
    if output is not None:
        with (
            patch.object(calibration.os, "getpid", return_value=coordinator_pid),
            patch.object(calibration.os, "getppid", return_value=max(1, coordinator_pid - 1)),
            patch.object(calibration.os, "getpgid", return_value=coordinator_pid),
        ):
            cast(dict[str, object], document["resources"])["worker_topology"] = (
                calibration._write_worker_topology(
                    output,
                    invocation_started=0.0,
                    configured_workers=cast(
                        dict[str, int],
                        cast(dict[str, object], document["settings"])["effective_workers"],
                    ),
                    raw_observations=[],
                    exact_observations=[],
                )
            )
    return document


def _write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, allow_nan=False) + "\n", encoding="utf-8")


def _run_small_raw(
    tmp_path: Path, certificate: ThresholdCertificate
) -> tuple[Path, RawMinimum]:
    directory = tmp_path / "raw"
    result = run_raw_sweep(
        certificate,
        workers=1,
        deadline=10.0,
        clock=lambda: 0.0,
        progress=lambda *_args: None,
        log=directory,
    )
    return directory, result


def _dilation_oracle() -> dict[str, object]:
    certificate, _source = _fixture()
    return calibration._expected_dilation_record(_normalized(certificate), "b" * 64)


def test_frozen_cross_fixture_and_normalization_have_the_reviewed_answers() -> None:
    certificate, source = _fixture()
    normalized, record = calibration.load_normalized(calibration.normalized_bytes(source))

    assert hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == calibration.FIXTURE_SHA256
    assert len(FIXTURE.read_bytes()) == calibration.FIXTURE_BYTES
    assert certificate.total_budget == calibration.RAW_BUDGET == 2
    assert len(certificate.directions) == calibration.RAW_DIRECTIONS == 2_881
    assert calibration._interval_labels()[0::2_880] == ("0", "2880", "2880'")
    assert calibration.TOTAL_DIRECTION_ROWS == 14_404
    assert normalized.total_budget == calibration.NORMALIZED_BUDGET == 1
    assert record["point_mass"] == "1/4"
    assert record["threshold_budget"] == "3/4"
    assert record["least_cell_charge"] == "1"


def test_real_generic_raw_exact_and_reflected_interval_kernels_run_on_reduced_net(
    tmp_path: Path,
) -> None:
    certificate, _source = _fixture()
    raw_directory, raw = _run_small_raw(tmp_path, _small(certificate))
    normalized = _small(certificate, normalized=True)
    exact_directory = tmp_path / "exact"
    interval_directory = tmp_path / "interval"

    exact = run_exact_route(
        normalized,
        workers=1,
        deadline=10.0,
        clock=lambda: 0.0,
        progress=lambda *_args: None,
        log=exact_directory,
    )
    interval = run_interval_route(
        normalized,
        workers=1,
        deadline=10.0,
        clock=lambda: 0.0,
        progress=lambda *_args: None,
        log=interval_directory,
    )

    assert raw.minimum == 2
    assert raw.direction == 0
    assert raw.completed == 2
    assert {path.name for path in raw_directory.iterdir()} == {"0.json", "1.json"}
    assert exact.minimum == 1
    assert exact.direction == 0
    assert exact.completed == 2
    assert exact.disagreements == 0
    assert (interval.lower, interval.upper) == (Fraction(1), Fraction(1))
    assert interval.completed == 3
    assert interval.stalled == interval.budget_exhausted == 0
    assert {path.name for path in interval_directory.iterdir()} == {
        "0.json",
        "1.json",
        "1'.json",
    }


def test_parallel_raw_and_exact_kernels_report_route_task_identity(tmp_path: Path) -> None:
    certificate, _source = _fixture()
    raw_observations: list[WorkerTaskObservation] = []
    exact_observations: list[WorkerTaskObservation] = []
    run_raw_sweep(
        _small(certificate),
        workers=2,
        deadline=time.perf_counter() + 10.0,
        clock=time.perf_counter,
        progress=lambda *_args: None,
        log=tmp_path / "observed-raw",
        task_observer=raw_observations.append,
    )
    run_exact_route(
        _small(certificate, normalized=True),
        workers=2,
        deadline=time.perf_counter() + 10.0,
        clock=time.perf_counter,
        progress=lambda *_args: None,
        log=tmp_path / "observed-exact",
        task_observer=exact_observations.append,
    )

    for observations in (raw_observations, exact_observations):
        assert sorted(row.direction for row in observations) == [0, 1]
        assert all(row.ppid == os.getpid() for row in observations)
        assert all(row.pgid == os.getpgid(0) for row in observations)
        assert all(row.started < row.finished for row in observations)


def test_strict_raw_comparison_refuses_the_n1_equality_control() -> None:
    assert calibration.raw_decision(Fraction(2), n=1) == "refused"
    assert calibration.raw_decision(Fraction(2), n=2) == "passed"


def test_underweight_control_fails_exact_interval_and_dilation(
    tmp_path: Path,
) -> None:
    certificate, source = _fixture()
    underweight = replace(
        _small(certificate, normalized=True),
        atoms=(replace(certificate.atoms[0], weight=Fraction(1, 8)),),
    )
    exact = run_exact_route(
        underweight,
        workers=1,
        deadline=10.0,
        clock=lambda: 0.0,
        progress=lambda *_args: None,
        log=tmp_path / "underweight-exact",
    )
    interval = run_interval_route(
        underweight,
        workers=1,
        deadline=10.0,
        clock=lambda: 0.0,
        progress=lambda *_args: None,
        log=tmp_path / "underweight-interval",
    )
    assert exact.minimum == Fraction(7, 8)
    assert (interval.lower, interval.upper) == (Fraction(7, 8), Fraction(7, 8))
    assert not interval.accepted

    record = calibration._normalized_record(source)
    cast(list[list[str]], record["atoms"])[0][2] = "1/8"
    record.update(
        {
            "point_mass": "1/8",
            "total_budget": "7/8",
            "least_cell_charge": "7/8",
        }
    )
    path = tmp_path / "underweight.json"
    _write_json(path, record)
    with pytest.raises(ValueError, match="not accepted on all five conditions"):
        build_limit_record(path, source_name="underweight.json", workers=1)


def test_threshold_semantics_and_inclusion_exclusion_anchors() -> None:
    certificate, _source = _fixture()
    witness = (Fraction(9, 32), Fraction(9, 32))
    contains = calibration._placement_membership(certificate, 0, witness)
    counts = tuple(atom.trace_count(contains) for atom in certificate.threshold_atoms)
    all_three_charge = sum(
        (
            atom.weight
            for atom, count in zip(certificate.threshold_atoms, counts, strict=True)
            if count > 2
        ),
        start=certificate.atoms[0].weight,
    )

    assert counts == (2, 2)
    assert (
        exact_charge(certificate.atoms, certificate.threshold_atoms, contains)
        == calibration.RAW_MINIMUM
    )
    assert all_three_charge == Fraction(1, 2)
    assert expansion_terms(3, 2) == ((2, 1), (3, -2))
    assert 3 * 1 != 1


def test_larger_domain_control_reaches_zero_at_an_admissible_witness() -> None:
    assert calibration.larger_domain_zero_control() == (Fraction(0), True)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda row: row.update({"id": "other"}),
        lambda row: cast(list[list[str]], row["atoms"])[0].__setitem__(0, "1/4"),
        lambda row: cast(list[list[str]], row["atoms"])[0].__setitem__(2, "1/4"),
        lambda row: cast(list[dict[str, object]], row["threshold_atoms"])[0].update(
            {"threshold": 3}
        ),
        lambda row: cast(list[dict[str, object]], row["threshold_atoms"]).reverse(),
        lambda row: row.update({"provenance": {"kind": "substituted"}}),
    ],
)
def test_fixture_freeze_refuses_identity_geometry_weight_threshold_order_and_source(
    mutation: Callable[[dict[str, object]], object],
) -> None:
    record = cast(dict[str, object], json.loads(FIXTURE.read_bytes()))
    mutation(record)
    raw = (json.dumps(record, indent=1, allow_nan=False) + "\n").encode()
    with pytest.raises(calibration.CalibrationError, match="fixture bytes"):
        calibration.load_fixture(raw)


def test_normalization_refuses_a_substituted_source_identity() -> None:
    _certificate, source = _fixture()
    source["id"] = "substituted"
    with pytest.raises(calibration.CalibrationError, match="frozen calibration fixture"):
        calibration.normalized_bytes(source)


def test_nonargmin_charge_mutation_is_refused_even_when_the_minimum_survives(
    tmp_path: Path,
) -> None:
    certificate, _source = _fixture()
    directory, _result = _run_small_raw(tmp_path, _small(certificate))
    row = cast(dict[str, object], json.loads((directory / "1.json").read_bytes()))
    row["charge"] = "3"
    _write_json(directory / "1.json", row)

    with pytest.raises(calibration.CalibrationError, match="known-answer"):
        calibration._check_raw_rows(directory, _small(certificate), expected=2)


@pytest.mark.parametrize("mutation", ["delete", "add", "mislabel", "numeric-alias"])
def test_row_set_and_label_mutations_are_refused(tmp_path: Path, mutation: str) -> None:
    certificate, _source = _fixture()
    small = _small(certificate)
    directory, _result = _run_small_raw(tmp_path, small)
    if mutation == "delete":
        (directory / "1.json").unlink()
    elif mutation == "add":
        _write_json(directory / "2.json", json.loads((directory / "1.json").read_bytes()))
    elif mutation == "mislabel":
        row = cast(dict[str, object], json.loads((directory / "1.json").read_bytes()))
        row["direction"] = 0
        _write_json(directory / "1.json", row)
    else:
        _write_json(directory / "01.json", json.loads((directory / "1.json").read_bytes()))

    with pytest.raises((calibration.CalibrationError, PacketError)):
        calibration._check_raw_rows(directory, small, expected=2)


def test_witness_byte_binding_and_coherently_inadmissible_witness_are_refused(
    tmp_path: Path,
) -> None:
    certificate, _source = _fixture()
    small = _small(certificate)
    directory, result = _run_small_raw(tmp_path, small)
    paths = tuple(directory / f"{index}.json" for index in range(2))
    receipt: dict[str, object] = {
        "directions_expected": 2,
        "directions_completed": 2,
        "completed_directions": [0, 1],
        "observed_minimum_upper_bound": str(result.minimum),
        "observed_argmin": result.direction,
        "observed_witness": [str(result.witness[0]), str(result.witness[1])],
        "raw_minimum": str(result.minimum),
        "directions_sha256": _direction_digest(paths),
    }
    row = cast(dict[str, object], json.loads(paths[1].read_bytes()))
    row["witness"] = ["0", "0"]
    _write_json(paths[1], row)
    with pytest.raises(PacketError, match="digest"):
        _reconstruct_raw_directions(directory, receipt, expected=2, complete=True)

    receipt["directions_sha256"] = _direction_digest(paths)
    _reconstruct_raw_directions(directory, receipt, expected=2, complete=True)
    with pytest.raises(calibration.CalibrationError, match="known-answer"):
        calibration._check_raw_rows(directory, small, expected=2)


def test_interval_scale_is_semantic_while_box_count_is_observational(
    tmp_path: Path,
) -> None:
    certificate, _source = _fixture()
    normalized = _small(certificate, normalized=True)
    directory = tmp_path / "interval"
    run_interval_route(
        normalized,
        workers=1,
        deadline=10.0,
        clock=lambda: 0.0,
        progress=lambda *_args: None,
        log=directory,
    )
    labels = ("0", "1", "1'")
    row = cast(dict[str, object], json.loads((directory / "1.json").read_bytes()))
    row["boxes"] = cast(int, row["boxes"]) + 17
    _write_json(directory / "1.json", row)
    readback, boxes = calibration._check_interval_rows(directory, normalized, labels=labels)
    assert readback.enclosure == (Fraction(1), Fraction(1))
    assert boxes > 17

    row["lower"] = row["upper"] = 1
    _write_json(directory / "1.json", row)
    with pytest.raises(calibration.CalibrationError, match="known-answer"):
        calibration._check_interval_rows(directory, normalized, labels=labels)


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("source", "outer_side"), "999"),
        (("strict_dilation_family", "factor_supremum"), "2*sqrt(33177601)/5761+0"),
        (("strict_dilation_family", "factor_supremum_squared"), "4"),
        (("strict_dilation_family", "factor_supremum_defining_polynomial"), "x^2-1"),
        (("conclusion", "bounded_side_squared"), "3"),
        (("conclusion", "endpoint_certificate"), True),
        (("proof", "requires_compactness"), True),
    ],
)
def test_dilation_surd_endpoint_and_compactness_mutations_are_refused(
    path: tuple[str, str], value: object
) -> None:
    certificate, _source = _fixture()
    normalized = _normalized(certificate)
    record = _dilation_oracle()
    calibration._check_dilation_record(record, normalized, "b" * 64)
    cast(dict[str, object], record[path[0]])[path[1]] = value
    with pytest.raises(calibration.CalibrationError, match="dilation record"):
        calibration._check_dilation_record(record, normalized, "b" * 64)


def test_dilation_record_refuses_a_missing_generic_field() -> None:
    certificate, _source = _fixture()
    normalized = _normalized(certificate)
    record = _dilation_oracle()
    cast(dict[str, object], record["source"]).pop("variant")
    with pytest.raises(calibration.CalibrationError, match="dilation record"):
        calibration._check_dilation_record(record, normalized, "b" * 64)


def test_real_generic_dilation_record_matches_oracle_on_small_complete_net(
    tmp_path: Path,
) -> None:
    _certificate, source = _fixture()
    candidate = calibration._normalized_record(source)
    candidate["direction_steps"] = 2
    path = tmp_path / "candidate.json"
    _write_json(path, candidate)

    record = build_limit_record(path, source_name="candidate.json", workers=1)
    certificate, _declared = calibration.load(path.read_bytes())

    assert len(certificate.directions) == 3
    assert cast(dict[str, object], record["source"])["accepted_conditions"] == [
        condition.name
        for condition in calibration.closed_form_threshold_conditions(certificate)
    ] + ["Condition 5' every reachable cell is charged at least 1"]
    calibration._check_dilation_record(
        record,
        certificate,
        hashlib.sha256(path.read_bytes()).hexdigest(),
    )


def test_calibration_wrapper_is_closed_and_cross_schema_readers_refuse(
    tmp_path: Path,
) -> None:
    output = tmp_path / "receipt"
    output.mkdir()
    document = _seed(output)
    calibration.validate_document(document)

    scientific = deepcopy(document)
    scientific["schema"] = "fixed-core-packet-result/v1"
    with pytest.raises(calibration.CalibrationError, match="calibration/v1"):
        calibration.validate_document(scientific)

    extra = deepcopy(document)
    extra["scientific_decision"] = "accepted"
    with pytest.raises(calibration.CalibrationError, match="calibration/v1"):
        calibration.validate_document(extra)

    forbidden = deepcopy(document)
    cast(dict[str, object], forbidden["sources"])["packet"] = "packet-accepted"
    with pytest.raises(calibration.CalibrationError, match="forbidden"):
        calibration.validate_document(forbidden)

    with pytest.raises(PacketError, match="schema"):
        load_scientific_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
        )


def test_terminal_status_cannot_substitute_declared_row_counts_for_routes(
    tmp_path: Path,
) -> None:
    output = tmp_path / "fabricated-terminal"
    output.mkdir()
    document = _seed(output)
    document.update(
        {
            "status": "complete",
            "disposition": "calibration-passed",
            "phase": "complete",
            "error": None,
        }
    )
    document["artifacts"] = [
        {
            "role": "declared-direction-counts",
            "path": "absent",
            "count": calibration.TOTAL_DIRECTION_ROWS,
            "bytes": 0,
        }
    ]
    resources = cast(dict[str, object], document["resources"])
    resources.update(
        {
            "cpu_observations": {
                "coordinator_start_seconds": 0.0,
                "coordinator_end_seconds": 0.1,
                "direct_children_user_start_seconds": 0.0,
                "direct_children_user_end_seconds": 0.0,
                "direct_children_system_start_seconds": 0.0,
                "direct_children_system_end_seconds": 0.0,
            },
            "coordinator_process_seconds": 0.1,
            "reaped_direct_children_user_seconds": 0.0,
            "reaped_direct_children_system_seconds": 0.0,
            "rss": {"sample_count": 2, "positive_sample_count": 2},
        }
    )
    cast(dict[str, object], document["supervision"]).update(
        {
            "status": "observed-exit",
            "worker_exit_status": 0,
            "process_group_reaped": True,
        }
    )
    _write_json(output / "result.json", document)

    with pytest.raises(calibration.CalibrationError, match="complete known-answer routes"):
        calibration.load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            expected_invocation=cast(
                dict[str, object],
                cast(dict[str, object], document["invocation"])["identity"],
            ),
        )


def test_partial_route_receipts_bind_the_exact_published_direction_set() -> None:
    receipt: dict[str, object] = {
        "status": "partial",
        "source_sha256": "b" * 64,
        "directions_expected": calibration.RAW_DIRECTIONS,
        "directions_completed": 2,
        "completed_directions": [0, 2],
        "observed_minimum_upper_bound": "1",
        "argmin": 0,
        "witness": ["0", "0"],
    }
    calibration._validate_route_receipt("normalized_exact", receipt)
    receipt["completed_directions"] = [0]
    with pytest.raises(calibration.CalibrationError, match="progress"):
        calibration._validate_route_receipt("normalized_exact", receipt)


def test_partial_dilation_receipt_round_trips_through_common_reader(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "dilation-directions"
    directory.mkdir()
    rows = (
        {"direction": 0, "label": "0", "minimum": "1"},
        {"direction": 1, "label": "1", "minimum": "1"},
    )
    for row in rows:
        _write_json(directory / f"{row['direction']}.json", row)
    labels = tuple(str(index) for index in range(calibration.RAW_DIRECTIONS))
    receipt: dict[str, object] = {
        "status": "partial",
        "source_sha256": "b" * 64,
        "directions_expected": calibration.RAW_DIRECTIONS,
        "directions_completed": 2,
        "completed_directions": ["0", "1"],
        "last": rows[1],
    }

    calibration._validate_route_receipt("dilation", receipt)
    _reconstruct_dilation_directions(
        directory,
        receipt,
        labels=labels,
        complete=False,
    )

    substituted = deepcopy(receipt)
    substituted["completed_directions"] = ["0", "2"]
    with pytest.raises(PacketError):
        _reconstruct_dilation_directions(
            directory,
            substituted,
            labels=labels,
            complete=False,
        )

    (directory / "1.json").unlink()
    with pytest.raises(PacketError, match="not retained"):
        _reconstruct_dilation_directions(
            directory,
            receipt,
            labels=labels,
            complete=False,
        )
    _write_json(directory / "1.json", rows[1])

    bad_last = deepcopy(receipt)
    bad_last["last"] = {"direction": 2, "label": "2", "minimum": "1"}
    with pytest.raises(PacketError, match="retained direction"):
        _reconstruct_dilation_directions(
            directory,
            bad_last,
            labels=labels,
            complete=False,
        )

    _write_json(directory / "2.json", {"direction": 2, "label": "wrong", "minimum": "1"})
    with pytest.raises(PacketError, match="wrong identity"):
        _reconstruct_dilation_directions(
            directory,
            receipt,
            labels=labels,
            complete=False,
        )


def test_receipt_parser_refuses_duplicate_keys(tmp_path: Path) -> None:
    output = tmp_path / "duplicate"
    output.mkdir()
    (output / "result.json").write_text(
        '{"schema":"fixed-core-packet-calibration/v1","schema":"forged"}\n',
        encoding="utf-8",
    )
    with pytest.raises(PacketError, match="duplicate"):
        calibration.load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
        )


def test_readback_takes_the_recorded_runtime_as_history(tmp_path: Path) -> None:
    """A dependency or interpreter change never invalidates a retained receipt.

    The readback never consults the current runtime, so a receipt whose recorded
    runtime differs from today's reads back unchanged; a malformed runtime record is
    still refused.
    """
    output = tmp_path / "another-runtime"
    output.mkdir()
    document = _seed(output)
    manifest = [
        {
            "path": calibration.FIXTURE_PATH,
            "git_blob": "b" * 40,
            "sha256": calibration.FIXTURE_SHA256,
        }
    ]
    recorded: dict[str, object] = {
        "python": {
            "implementation": "cpython",
            "version": "3.14.6",
            "abi": "cpython-314-recorded",
            "gil_enabled": True,
            "environment": "/elsewhere/packing/.venv",
            "executable": "/elsewhere/packing/.venv/bin/python",
            "resolved_executable": "/elsewhere/python3.14",
            "build": "3.14.6 recorded build",
        },
        "packages": {"numpy": "2.4.0", "strif": "3.0.0"},
        "attestation_scope": RUNTIME_ATTESTATION_SCOPE,
    }
    sources = cast(dict[str, object], document["sources"])
    sources.update(manifest=manifest, runtime=recorded)
    calibration.write_result(output, document)
    not_consulted = AssertionError("readback consulted the current runtime")
    with (
        patch.object(calibration, "source_manifest", return_value=manifest),
        patch.object(calibration, "runtime_binding", side_effect=not_consulted),
    ):
        readback = calibration.load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
        )
    assert cast(dict[str, object], readback["sources"])["runtime"] == recorded

    sources["runtime"] = {**recorded, "packages": {"numpy": "2.4.0"}}
    calibration.write_result(output, document)
    with (
        patch.object(calibration, "source_manifest", return_value=manifest),
        pytest.raises(PacketError, match="runtime package identities are malformed"),
    ):
        calibration.load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
        )


def test_source_closure_calls_real_generic_kernels_without_target_entry_points() -> None:
    source = (REPOSITORY / "packing/devtools/calibrate_fixed_core_packet.py").read_text(
        encoding="utf-8"
    )
    tree = ast.parse(source)
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    defaults = calibration.RouteKernels()
    paths = calibration.discover_implementation_paths(REPOSITORY)

    assert defaults.raw is run_raw_sweep
    assert defaults.exact is run_exact_route
    assert defaults.interval is run_interval_route
    assert defaults.dilation is calibration.run_dilation_replay
    assert (
        not {
            "execute_packet",
            "normalized_record",
            "load_packet_source",
        }
        & calls
    )
    assert calibration.FIXTURE_PATH in paths
    assert "packing/devtools/calibrate_fixed_core_packet.py" in paths


def test_output_must_be_fresh_and_outside_the_repository(tmp_path: Path) -> None:
    with pytest.raises(calibration.CalibrationError, match="outside"):
        calibration.prepare_output_dir(REPOSITORY / "packing/calibration-result", REPOSITORY)
    existing = tmp_path / "existing"
    existing.mkdir()
    with pytest.raises(calibration.CalibrationError, match="fresh"):
        calibration.prepare_output_dir(existing, REPOSITORY)


def test_rss_summary_is_byte_bound_but_not_a_semantic_answer(tmp_path: Path) -> None:
    samples: list[dict[str, object]] = [
        {
            "elapsed_seconds": 0.1,
            "phase": "raw-sweep",
            "pids": [101, 102],
            "rss_bytes": 4_096,
            "error": None,
        },
        {
            "elapsed_seconds": 0.25,
            "phase": "normalized-exact",
            "pids": [101],
            "rss_bytes": 2_048,
            "error": None,
        },
    ]
    summary = calibration._write_rss_samples(tmp_path, samples, observation_lifetime=0.3)
    resources: dict[str, object] = {
        "cpu_scope": calibration.CPU_SCOPE,
        "cpu_observations": None,
        "coordinator_process_seconds": None,
        "reaped_direct_children_user_seconds": None,
        "reaped_direct_children_system_seconds": None,
        "rss": summary,
    }
    calibration._validate_rss_observations(tmp_path, resources, required=True)
    record = cast(
        dict[str, object],
        json.loads((tmp_path / "rss-samples.json").read_bytes()),
    )
    cast(list[dict[str, object]], record["samples"])[0]["rss_bytes"] = 1
    _write_json(tmp_path / "rss-samples.json", record)
    with pytest.raises(calibration.CalibrationError, match="byte binding"):
        calibration._validate_rss_observations(tmp_path, resources, required=True)


def test_parallel_worker_topology_distinguishes_configuration_from_execution() -> None:
    observations = (
        WorkerTaskObservation(0, 201, 100, 100, 1.0, 3.0),
        WorkerTaskObservation(1, 202, 100, 100, 1.5, 2.5),
        WorkerTaskObservation(2, 201, 100, 100, 3.0, 4.0),
        WorkerTaskObservation(3, 202, 100, 100, 4.0, 5.0),
    )
    route = calibration._build_route_worker_topology(
        "raw-sweep",
        configured_workers=4,
        directions_expected=4,
        coordinator_pid=100,
        coordinator_group=100,
        invocation_started=0.0,
        observations=observations,
    )

    summary = calibration._validate_worker_topology_route(
        "raw",
        route,
        phase="raw-sweep",
        configured_workers=4,
        directions_expected=4,
        coordinator_pid=100,
        coordinator_group=100,
        required=True,
    )

    assert summary == {
        "configured_workers": 4,
        "execution_model": "process-pool",
        "observed_child_count": 2,
        "maximum_simultaneous_children": 2,
    }


def test_worker_topology_refuses_coherently_shifted_tasks_past_worker_elapsed() -> None:
    route = calibration._build_route_worker_topology(
        "raw-sweep",
        configured_workers=2,
        directions_expected=2,
        coordinator_pid=100,
        coordinator_group=100,
        invocation_started=0.0,
        observations=(
            WorkerTaskObservation(0, 201, 100, 100, 0.1, 0.3),
            WorkerTaskObservation(1, 202, 100, 100, 0.2, 0.4),
        ),
    )
    calibration._validate_worker_topology_route(
        "raw",
        route,
        phase="raw-sweep",
        configured_workers=2,
        directions_expected=2,
        coordinator_pid=100,
        coordinator_group=100,
        required=True,
        worker_elapsed_seconds=1.0,
    )

    for task in cast(list[dict[str, object]], route["tasks"]):
        task["started_seconds"] = cast(float, task["started_seconds"]) + 100.0
        task["finished_seconds"] = cast(float, task["finished_seconds"]) + 100.0
    for child in cast(list[dict[str, object]], route["children"]):
        child["first_task_started_seconds"] = (
            cast(float, child["first_task_started_seconds"]) + 100.0
        )
        child["last_task_finished_seconds"] = (
            cast(float, child["last_task_finished_seconds"]) + 100.0
        )

    with pytest.raises(calibration.CalibrationError, match="child task is malformed"):
        calibration._validate_worker_topology_route(
            "raw",
            route,
            phase="raw-sweep",
            configured_workers=2,
            directions_expected=2,
            coordinator_pid=100,
            coordinator_group=100,
            required=True,
            worker_elapsed_seconds=1.0,
        )


def test_worker_topology_refuses_digest_consistent_reversed_route_chronology(
    tmp_path: Path,
) -> None:
    document = calibration.initial_document(
        REVISION,
        workers=2,
        calibration_seconds=4.0,
        external_seconds=5.0,
        grace_seconds=0.05,
        invocation_started=0.0,
        run_order=1,
        cache_observation="synthetic chronology control",
        background_load="unmeasured",
    )
    coordinator = {"role": "coordinator", "pid": 100, "ppid": 99, "pgid": 100}
    settings = cast(dict[str, object], document["settings"])
    resources = cast(dict[str, object], document["resources"])
    supervision = cast(dict[str, object], document["supervision"])
    summaries: dict[str, object] = {}
    sidecars: dict[str, dict[str, object]] = {}
    for name, phase, first_pid, starts in (
        ("raw", "raw-sweep", 201, (0.1, 0.2)),
        ("normalized_exact", "normalized-exact", 301, (0.6, 0.7)),
    ):
        route = calibration._build_route_worker_topology(
            phase,
            configured_workers=2,
            directions_expected=2,
            coordinator_pid=100,
            coordinator_group=100,
            invocation_started=0.0,
            observations=tuple(
                WorkerTaskObservation(index, first_pid + index, 100, 100, start, start + 0.3)
                for index, start in enumerate(starts)
            ),
        )
        sidecars[name] = {
            "schema": calibration.WORKER_TOPOLOGY_ROUTE_SCHEMA,
            "scope": calibration.WORKER_TOPOLOGY_SCOPE,
            "coordinator": coordinator,
            "route": route,
        }
        filename = f"{name.replace('_', '-')}-worker-topology.json"
        _write_json(tmp_path / filename, sidecars[name])
        summaries[name] = {
            "configured_workers": route["configured_workers"],
            "execution_model": route["execution_model"],
            "observed_child_count": route["observed_child_count"],
            "maximum_simultaneous_children": route["maximum_simultaneous_children"],
            "record_path": filename,
            "record_sha256": hashlib.sha256((tmp_path / filename).read_bytes()).hexdigest(),
        }
    resources["worker_topology"] = {
        "schema": calibration.WORKER_TOPOLOGY_SCHEMA,
        "scope": calibration.WORKER_TOPOLOGY_SCOPE,
        "coordinator": coordinator,
        "routes": summaries,
    }

    def validate() -> None:
        calibration._validate_worker_topology(
            tmp_path,
            resources,
            settings,
            supervision,
            required_routes={"raw", "normalized_exact"},
            require_supervisor_binding=False,
            expected_directions={"raw": 2, "normalized_exact": 2},
            worker_elapsed_seconds=1.0,
        )

    validate()
    raw_route = cast(dict[str, object], sidecars["raw"]["route"])
    exact_route = cast(dict[str, object], sidecars["normalized_exact"]["route"])
    for key, fields in (
        ("tasks", ("started_seconds", "finished_seconds")),
        ("children", ("first_task_started_seconds", "last_task_finished_seconds")),
    ):
        raw_rows = cast(list[dict[str, object]], raw_route[key])
        exact_rows = cast(list[dict[str, object]], exact_route[key])
        for raw_row, exact_row in zip(raw_rows, exact_rows, strict=True):
            for field in fields:
                raw_row[field], exact_row[field] = exact_row[field], raw_row[field]
    for name in ("raw", "normalized_exact"):
        filename = f"{name.replace('_', '-')}-worker-topology.json"
        _write_json(tmp_path / filename, sidecars[name])
        cast(dict[str, object], summaries[name])["record_sha256"] = hashlib.sha256(
            (tmp_path / filename).read_bytes()
        ).hexdigest()

    with pytest.raises(calibration.CalibrationError, match="raw tasks finish after"):
        validate()


@pytest.mark.parametrize("mutation", ["single", "combined", "finite-sum-overflow"])
def test_terminal_document_refuses_worker_phase_durations_beyond_elapsed(
    tmp_path: Path,
    mutation: str,
) -> None:
    document = _terminal_candidate_summary(tmp_path)
    document.update(
        status="complete", disposition="calibration-passed", phase="complete", error=None
    )
    supervision = cast(dict[str, object], document["supervision"])
    supervision.update(
        status="observed-exit",
        worker_exit_status=0,
        process_group_reaped=True,
        coordinator_pid=101,
        coordinator_process_group_id=101,
    )
    cast(dict[str, object], document["resources"])["rss"] = {
        "sample_count": 2,
        "positive_sample_count": 2,
    }
    clocks = cast(dict[str, object], document["clocks"])
    calibration.validate_document(document)
    if mutation == "single":
        clocks["raw_seconds"] = 100.0
    elif mutation == "combined":
        clocks["worker_elapsed_seconds"] = 0.1
        for phase in (
            "preflight_seconds",
            "raw_seconds",
            "normalization_publication_seconds",
            "exact_seconds",
            "interval_seconds",
            "dilation_seconds",
            "full_readback_seconds",
        ):
            clocks[phase] = 0.02
    else:
        clocks["raw_seconds"] = clocks["exact_seconds"] = 1e308
        clocks["worker_elapsed_seconds"] = 1e308
    with pytest.raises(calibration.CalibrationError, match="phase durations"):
        calibration.validate_document(document)


def test_producer_phase_rounding_tolerance_has_a_small_boundary() -> None:
    clocks: dict[str, object] = dict.fromkeys(calibration.WORKER_DISJOINT_PHASES, 0.01)
    clocks["worker_elapsed_seconds"] = 0.07 - 5e-10
    calibration._validate_worker_phase_durations(clocks)
    clocks["worker_elapsed_seconds"] = 0.07 - 5e-7
    with pytest.raises(calibration.CalibrationError, match="phase durations"):
        calibration._validate_worker_phase_durations(clocks)


def test_producer_accepts_finite_phase_total_near_float_limit() -> None:
    clocks: dict[str, object] = dict.fromkeys(calibration.WORKER_DISJOINT_PHASES, 0.0)
    clocks.update(raw_seconds=1e308, exact_seconds=7e307, worker_elapsed_seconds=1.7e308)
    calibration._validate_worker_phase_durations(clocks)


def test_producer_refuses_nonfinite_derived_deadlines() -> None:
    document = calibration.initial_document(
        REVISION,
        workers=1,
        calibration_seconds=1e307,
        external_seconds=2e307,
        grace_seconds=1.0,
        invocation_started=1e308,
        run_order=1,
        cache_observation="test cache",
        background_load="test load",
    )
    calibration.validate_document(document)
    settings = cast(dict[str, object], document["settings"])
    settings.update(calibration_seconds=1e308, external_seconds=1.1e308)
    identity = cast(
        dict[str, object], cast(dict[str, object], document["invocation"])["identity"]
    )
    identity.update(
        calibration_seconds=1e308,
        external_seconds=1.1e308,
        calibration_deadline_monotonic=1e307,
        external_deadline_monotonic=1e307,
    )
    encoded = json.dumps(document, allow_nan=False)
    for field in ("calibration_deadline_monotonic", "external_deadline_monotonic"):
        placeholder = f'"{field}": 1e+307'
        assert placeholder in encoded
        encoded = encoded.replace(placeholder, f'"{field}": 1e999', 1)
    parsed = calibration._strict_json_bytes(encoded.encode(), "calibration receipt")
    with pytest.raises(calibration.CalibrationError, match="deadline"):
        calibration.validate_document(parsed)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda route: cast(list[object], route["tasks"]).pop(),
        lambda route: route.update(observed_child_count=1),
        lambda route: route.update(maximum_simultaneous_children=1),
        lambda route: cast(list[dict[str, object]], route["children"])[0].update(ppid=99),
    ],
)
def test_worker_topology_refuses_incomplete_or_coherently_false_execution(
    mutation: Callable[[dict[str, object]], object],
) -> None:
    route = calibration._build_route_worker_topology(
        "raw-sweep",
        configured_workers=2,
        directions_expected=2,
        coordinator_pid=100,
        coordinator_group=100,
        invocation_started=0.0,
        observations=(
            WorkerTaskObservation(0, 201, 100, 100, 1.0, 3.0),
            WorkerTaskObservation(1, 202, 100, 100, 1.5, 2.5),
        ),
    )
    mutation(route)

    with pytest.raises(calibration.CalibrationError):
        calibration._validate_worker_topology_route(
            "raw",
            route,
            phase="raw-sweep",
            configured_workers=2,
            directions_expected=2,
            coordinator_pid=100,
            coordinator_group=100,
            required=True,
        )


def test_unpublished_topology_tail_is_validated_without_entering_inventory(
    tmp_path: Path,
) -> None:
    output = tmp_path / "topology-tail"
    output.mkdir()
    document = _seed(output, invocation_started=0.0)
    settings = cast(dict[str, object], document["settings"])
    with (
        patch.object(calibration.os, "getpid", return_value=101),
        patch.object(calibration.os, "getppid", return_value=100),
        patch.object(calibration.os, "getpgid", return_value=101),
    ):
        calibration._write_worker_topology(
            output,
            invocation_started=0.0,
            configured_workers=cast(dict[str, int], settings["effective_workers"]),
            raw_observations=[],
            exact_observations=None,
        )

    calibration._validate_worker_topology(
        output,
        cast(dict[str, object], document["resources"]),
        settings,
        cast(dict[str, object], document["supervision"]),
        required_routes=set(),
        require_supervisor_binding=False,
    )
    roles = {
        cast(str, row["role"])
        for row in calibration._artifact_inventory(
            output,
            (output / "result.json").stat().st_size,
            None,
        )
    }
    assert "raw-worker-topology" not in roles

    (output / "raw-worker-topology.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(calibration.CalibrationError, match="unknown schema or scope"):
        calibration._validate_worker_topology(
            output,
            cast(dict[str, object], document["resources"]),
            settings,
            cast(dict[str, object], document["supervision"]),
            required_routes=set(),
            require_supervisor_binding=False,
        )


def test_worker_topology_refuses_a_missing_receipt_bound_sidecar(tmp_path: Path) -> None:
    output = tmp_path / "missing-topology-sidecar"
    output.mkdir()
    document = _terminal_candidate_summary(output)
    (output / "raw-worker-topology.json").unlink()

    with pytest.raises(calibration.CalibrationError, match="lacks retained raw"):
        calibration._validate_worker_topology(
            output,
            cast(dict[str, object], document["resources"]),
            cast(dict[str, object], document["settings"]),
            cast(dict[str, object], document["supervision"]),
            required_routes={"raw", "normalized_exact"},
            require_supervisor_binding=False,
        )


def test_launch_oserror_is_an_operational_unresolved_receipt(
    tmp_path: Path,
) -> None:
    output = tmp_path / "launch"
    output.mkdir()
    _seed(output)
    with patch(
        "devtools.calibrate_fixed_core_packet.subprocess.Popen",
        side_effect=OSError("temporary launch failure"),
    ):
        status = calibration.supervise_worker(
            (sys.executable, "-c", "raise SystemExit"),
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            external_seconds=2.0,
            grace_seconds=0.05,
            invocation_started=time.perf_counter(),
            external_deadline=time.perf_counter() + 1.0,
        )
    receipt = json.loads((output / "result.json").read_bytes())
    assert status == 1
    assert receipt["status"] == "partial"
    assert receipt["phase"] == "operational-failure"
    assert receipt["supervision"]["status"] == "launch-failed"


def test_supervisor_recomputes_deadline_after_process_launch(tmp_path: Path) -> None:
    output = tmp_path / "launch-boundary"
    output.mkdir()
    _seed(output)

    class Process:
        pid = 123

        @staticmethod
        def poll() -> None:
            return None

    times = iter((0.0, 0.1, 0.9, 0.91, 1.01, 1.02, 1.025, 1.03))
    with (
        patch(
            "devtools.calibrate_fixed_core_packet.time.perf_counter",
            side_effect=lambda: next(times),
        ),
        patch(
            "devtools.calibrate_fixed_core_packet.subprocess.Popen",
            return_value=Process(),
        ),
        patch(
            "devtools.calibrate_fixed_core_packet._sample_process_group",
            return_value={
                "elapsed_seconds": 0.91,
                "phase": "preflight",
                "pids": [123],
                "rss_bytes": 1,
                "error": None,
            },
        ),
        patch(
            "devtools.calibrate_fixed_core_packet._reap_process_group",
            return_value=(-9, 0.01),
        ),
        patch(
            "devtools.calibrate_fixed_core_packet._record_supervision",
            return_value={},
        ) as record,
    ):
        status = calibration.supervise_worker(
            ("worker",),
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            external_seconds=1.0,
            grace_seconds=0.05,
            invocation_started=0.0,
            external_deadline=1.0,
        )

    assert status == 1
    assert record.call_args.kwargs["status"] == "deadline-terminated"
    assert record.call_args.kwargs["launch_seconds"] == pytest.approx(0.8)


@pytest.mark.parametrize(
    "phase",
    [
        "raw-sweep",
        "normalized-exact",
        "reflected-interval",
        "dilation-replay",
        "readback",
    ],
)
def test_each_execution_checkpoint_remains_partial_when_terminated(
    tmp_path: Path, phase: str
) -> None:
    # The supervisor samples only after the worker launches, so a launch slower than
    # the external window terminates the worker before any checkpoint is observed.
    # Every attempt must still be a deadline-terminated partial receipt; the window
    # widens only while no sample was taken, and the bound matters only on failure.
    window = 0.08
    give_up = time.monotonic() + 10.0
    attempt = 0
    while True:
        output = tmp_path / f"{phase}-{attempt}"
        output.mkdir()
        document = _seed(output)
        document["phase"] = phase
        document["error"] = f"{phase} is incomplete"
        calibration.write_result(output, document)
        started = time.perf_counter()
        status = calibration.supervise_worker(
            (sys.executable, "-c", "import time; time.sleep(60)"),
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            external_seconds=window,
            grace_seconds=0.03,
            invocation_started=started,
            external_deadline=started + window,
        )
        receipt = json.loads((output / "result.json").read_bytes())
        rss = cast(dict[str, object], cast(dict[str, object], receipt["resources"])["rss"])
        assert status == 1
        assert receipt["status"] == "partial"
        assert receipt["phase"] == "timeout"
        if cast(int, rss["sample_count"]) or time.monotonic() >= give_up:
            break
        window *= 2
        attempt += 1
    assert phase in cast(dict[str, object], rss["pids_by_phase"])


def test_timeout_kills_and_reaps_a_termination_resistant_process_group(
    tmp_path: Path,
) -> None:
    output = tmp_path / "timeout"
    output.mkdir()
    _seed(output)
    grandchild = (
        "import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(60)"
    )
    leader = (
        "import signal,subprocess,sys,time;"
        "signal.signal(signal.SIGTERM,signal.SIG_IGN);"
        f"subprocess.Popen([sys.executable,'-c',{grandchild!r}]);"
        "time.sleep(60)"
    )
    started = time.perf_counter()
    status = calibration.supervise_worker(
        (sys.executable, "-c", leader),
        output,
        repository=REPOSITORY,
        expected_revision=REVISION,
        external_seconds=0.2,
        grace_seconds=0.05,
        invocation_started=started,
        external_deadline=started + 0.2,
    )
    receipt = json.loads((output / "result.json").read_bytes())
    assert status == 1
    assert receipt["status"] == "partial"
    assert receipt["phase"] == "timeout"
    supervision = cast(dict[str, object], receipt["supervision"])
    coordinator_pid = supervision.pop("coordinator_pid")
    coordinator_group = supervision.pop("coordinator_process_group_id")
    assert type(coordinator_pid) is int
    assert coordinator_pid > 0
    assert coordinator_group == coordinator_pid
    assert supervision == {
        "status": "deadline-terminated",
        "worker_exit_status": -9,
        "process_group_reaped": True,
        "supervisor_signal": None,
    }


class _ExitedLeader:
    pid = 4321

    @staticmethod
    def wait(timeout: float | None = None) -> int:
        del timeout
        return -signal.SIGKILL


def test_reaper_polls_through_eperm_until_the_group_is_gone() -> None:
    # macOS reports EPERM for signal 0 while the group's last member is exiting but not
    # yet reaped, and for a signal sent in that window. Neither may escape the reaper,
    # and only the later ESRCH may count as the group being gone.
    probes = [PermissionError, PermissionError, PermissionError]

    def killpg(_pid: int, signal_number: int) -> None:
        if signal_number == 0:
            raise probes.pop(0) if probes else ProcessLookupError
        raise PermissionError

    with patch("devtools.calibrate_fixed_core_packet.os.killpg", side_effect=killpg) as sent:
        status, _cleanup = calibration._reap_process_group(
            cast(subprocess.Popen[bytes], _ExitedLeader()), grace_seconds=1.0
        )

    assert status == -signal.SIGKILL
    assert [call.args for call in sent.call_args_list] == [
        (4321, 0),
        (4321, signal.SIGTERM),
        (4321, 0),
        (4321, signal.SIGKILL),
        (4321, 0),
        (4321, 0),
        (4321, 0),
    ]


def test_reaper_refuses_to_prove_reaping_while_the_group_reports_eperm() -> None:
    with (
        patch(
            "devtools.calibrate_fixed_core_packet.os.killpg", side_effect=PermissionError
        ) as sent,
        pytest.raises(
            calibration.CalibrationOperationalError,
            match="worker process group remained alive after SIGKILL",
        ),
    ):
        calibration._reap_process_group(
            cast(subprocess.Popen[bytes], _ExitedLeader()), grace_seconds=0.02
        )

    calls = [call.args for call in sent.call_args_list]
    assert calls[:4] == [
        (4321, 0),
        (4321, signal.SIGTERM),
        (4321, 0),
        (4321, signal.SIGKILL),
    ]
    assert len(calls) > 4
    assert set(calls[4:]) == {(4321, 0)}


def test_nonzero_exit_revokes_a_stale_complete_candidate_phase(
    tmp_path: Path,
) -> None:
    output = tmp_path / "nonzero"
    output.mkdir()
    document = _seed(output)
    document["phase"] = "awaiting-worker-exit"
    document["error"] = "parent has not observed worker exit"
    calibration.write_result(output, document)
    started = time.perf_counter()
    status = calibration.supervise_worker(
        (sys.executable, "-c", "raise SystemExit(7)"),
        output,
        repository=REPOSITORY,
        expected_revision=REVISION,
        external_seconds=2.0,
        grace_seconds=0.05,
        invocation_started=started,
        external_deadline=started + 2.0,
    )
    receipt = json.loads((output / "result.json").read_bytes())
    assert status == 1
    assert receipt["status"] == "partial"
    assert receipt["phase"] == "operational-failure"
    assert receipt["supervision"]["worker_exit_status"] == 7


def test_interrupt_during_parent_readback_never_publishes_success(tmp_path: Path) -> None:
    output = tmp_path / "interrupted-readback"
    output.mkdir()
    document = _seed(output)
    document["phase"] = "awaiting-worker-exit"
    document["error"] = "parent has not observed worker exit"
    calibration.write_result(output, document)

    class Worker:
        pid = 101

        @staticmethod
        def poll() -> int:
            return 0

    class Readback:
        pid = 102

        @staticmethod
        def wait(*, timeout: float) -> int:
            del timeout
            raise KeyboardInterrupt

    started = time.perf_counter()
    with (
        patch(
            "devtools.calibrate_fixed_core_packet.subprocess.Popen",
            side_effect=[Worker(), Readback()],
        ),
        patch(
            "devtools.calibrate_fixed_core_packet._reap_process_group",
            side_effect=[(0, 0.0), (-signal.SIGTERM, 0.01)],
        ),
        pytest.raises(KeyboardInterrupt),
    ):
        calibration.supervise_worker(
            ("worker", "--worker"),
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            external_seconds=2.0,
            grace_seconds=0.05,
            invocation_started=started,
            external_deadline=started + 2.0,
        )

    receipt = cast(dict[str, object], json.loads((output / "result.json").read_bytes()))
    assert receipt["status"] == "partial"
    assert receipt["phase"] == "operational-failure"
    assert cast(dict[str, object], receipt["supervision"])["status"] == (
        "supervisor-interrupted"
    )


def test_parent_readback_that_finishes_after_deadline_revokes_admission(
    tmp_path: Path,
) -> None:
    output = tmp_path / "late-readback"
    output.mkdir()
    document = _seed(output)
    document["phase"] = "awaiting-worker-exit"
    document["error"] = "parent has not observed worker exit"
    calibration.write_result(output, document)
    started = time.perf_counter()

    program = "import sys,time;time.sleep(0.3 if '--readback-only' in sys.argv else 0.02)"
    status = calibration.supervise_worker(
        (sys.executable, "-c", program, "--worker"),
        output,
        repository=REPOSITORY,
        expected_revision=REVISION,
        external_seconds=0.18,
        grace_seconds=0.05,
        invocation_started=started,
        external_deadline=started + 0.18,
    )
    receipt = json.loads((output / "result.json").read_bytes())
    assert status == 1
    assert receipt["status"] == "partial"
    assert receipt["phase"] == "timeout"
    assert "parent final readback" in receipt["error"]


@pytest.mark.parametrize(
    "late_at",
    [
        "success",
        "phase-overflow",
        "finite-sum-overflow",
        "validation",
        "serialization",
        "publication",
    ],
)
def test_terminal_admission_outcomes(
    tmp_path: Path,
    late_at: str,
) -> None:
    output = tmp_path / f"late-{late_at}"
    output.mkdir()
    document = _terminal_candidate_summary(output)
    if late_at == "phase-overflow":
        cast(dict[str, object], document["clocks"])["raw_seconds"] = 100.0
    elif late_at == "finite-sum-overflow":
        clocks = cast(dict[str, object], document["clocks"])
        clocks["raw_seconds"] = clocks["exact_seconds"] = 1e308
        clocks["worker_elapsed_seconds"] = 1e308
    calibration.write_result(output, document)
    now = [0.0]

    class Worker:
        pid = 101
        states = iter((None, None, 0))

        def poll(self) -> int | None:
            return next(self.states)

    class Readback:
        pid = 102

        @staticmethod
        def wait(*, timeout: float) -> int:
            del timeout
            return 0

    real_validate_cpu = calibration._validate_cpu_observations
    real_serialize = calibration._serialized_document
    real_promote = calibration._promote_staged_result

    def validate_cpu(*args: object, **kwargs: object) -> None:
        real_validate_cpu(*args, **kwargs)  # type: ignore[arg-type]
        if late_at == "validation":
            now[0] = 6.0

    def serialize(output_dir: Path, candidate: dict[str, object]) -> str:
        if late_at == "serialization" and candidate["status"] == "complete":
            now[0] = 6.0
        return real_serialize(output_dir, candidate)

    def promote_file(source: Path, target: Path) -> None:
        real_promote(source, target)
        if late_at == "publication":
            now[0] = 6.0

    def sample(process_group: int, **kwargs: object) -> dict[str, object]:
        return {
            "elapsed_seconds": kwargs["elapsed"],
            "phase": kwargs["phase"],
            "pids": [process_group],
            "rss_bytes": 4_096,
            "error": None,
        }

    with (
        patch.object(calibration.subprocess, "Popen", side_effect=[Worker(), Readback()]),
        patch.object(calibration, "_reap_process_group", return_value=(0, 0.0)),
        patch.object(calibration.time, "perf_counter", side_effect=lambda: now[0]),
        patch.object(
            calibration.time,
            "sleep",
            side_effect=lambda delay: now.__setitem__(0, now[0] + delay),
        ),
        patch.object(calibration, "_sample_process_group", side_effect=sample),
        patch.object(calibration, "_validate_cpu_observations", side_effect=validate_cpu),
        patch.object(calibration, "_serialized_document", side_effect=serialize),
        patch.object(calibration, "_promote_staged_result", side_effect=promote_file),
    ):
        status = calibration.supervise_worker(
            ("control", "--worker"),
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            external_seconds=5.0,
            grace_seconds=0.05,
            invocation_started=0.0,
            external_deadline=5.0,
            expected_invocation=cast(
                dict[str, object],
                cast(dict[str, object], document["invocation"])["identity"],
            ),
        )

    receipt = cast(dict[str, object], json.loads((output / "result.json").read_bytes()))
    if late_at == "success":
        assert status == 0
        assert receipt["status"] == "complete"
        assert receipt["disposition"] == "calibration-passed"
        assert receipt["phase"] == "complete"
    elif late_at in {"phase-overflow", "finite-sum-overflow"}:
        assert status == 2
        assert receipt["status"] == "invalid"
        assert receipt["disposition"] == "calibration-refused"
        assert receipt["phase"] == "metrics-refused"
        assert "phase durations" in cast(str, receipt["error"])
    else:
        assert status == 1
        assert receipt["status"] == "partial"
        assert receipt["disposition"] == "incomplete"
        assert receipt["phase"] == "timeout"
    assert not any(path.name.startswith(".result-admission-") for path in output.iterdir())


def test_metrics_admission_refuses_absent_worker_topology(tmp_path: Path) -> None:
    output = tmp_path / "missing-worker-topology"
    output.mkdir()
    document = _terminal_candidate_summary()
    calibration.write_result(output, document)

    class Worker:
        pid = 101
        states = iter((None, None, 0))

        def poll(self) -> int | None:
            return next(self.states)

    class Readback:
        pid = 102

        @staticmethod
        def wait(*, timeout: float) -> int:
            del timeout
            return 0

    with (
        patch.object(calibration.subprocess, "Popen", side_effect=[Worker(), Readback()]),
        patch.object(calibration, "_reap_process_group", return_value=(0, 0.0)),
        patch.object(calibration.time, "perf_counter", return_value=0.2),
        patch.object(calibration.time, "sleep", return_value=None),
        patch.object(
            calibration,
            "_sample_process_group",
            side_effect=lambda process_group, **kwargs: {
                "elapsed_seconds": kwargs["elapsed"],
                "phase": kwargs["phase"],
                "pids": [process_group],
                "rss_bytes": 4_096,
                "error": None,
            },
        ),
    ):
        status = calibration.supervise_worker(
            ("control", "--worker"),
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            external_seconds=5.0,
            grace_seconds=0.05,
            invocation_started=0.0,
            external_deadline=5.0,
            expected_invocation=cast(
                dict[str, object],
                cast(dict[str, object], document["invocation"])["identity"],
            ),
        )

    receipt = cast(dict[str, object], json.loads((output / "result.json").read_bytes()))
    assert status == 2
    assert receipt["status"] == "invalid"
    assert receipt["disposition"] == "calibration-refused"
    assert receipt["phase"] == "metrics-refused"
    assert "worker topology" in cast(str, receipt["error"])


def test_interrupt_during_terminal_serialization_preserves_partial_receipt(
    tmp_path: Path,
) -> None:
    output = tmp_path / "interrupt-terminal-serialization"
    output.mkdir()
    document = _terminal_candidate_summary(output)
    calibration.write_result(output, document)
    now = [0.0]

    class Worker:
        pid = 101
        states = iter((None, None, 0))

        def poll(self) -> int | None:
            return next(self.states)

    class Readback:
        pid = 102

        @staticmethod
        def wait(*, timeout: float) -> int:
            del timeout
            return 0

    real_serialize = calibration._serialized_document

    def serialize(output_dir: Path, candidate: dict[str, object]) -> str:
        if candidate["status"] == "complete":
            raise KeyboardInterrupt
        return real_serialize(output_dir, candidate)

    with (
        patch.object(calibration.subprocess, "Popen", side_effect=[Worker(), Readback()]),
        patch.object(calibration, "_reap_process_group", return_value=(0, 0.0)),
        patch.object(calibration.time, "perf_counter", side_effect=lambda: now[0]),
        patch.object(
            calibration.time,
            "sleep",
            side_effect=lambda delay: now.__setitem__(0, now[0] + delay),
        ),
        patch.object(
            calibration,
            "_sample_process_group",
            side_effect=lambda process_group, **kwargs: {
                "elapsed_seconds": kwargs["elapsed"],
                "phase": kwargs["phase"],
                "pids": [process_group],
                "rss_bytes": 4_096,
                "error": None,
            },
        ),
        patch.object(calibration, "_serialized_document", side_effect=serialize),
        pytest.raises(KeyboardInterrupt),
    ):
        calibration.supervise_worker(
            ("control", "--worker"),
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            external_seconds=5.0,
            grace_seconds=0.05,
            invocation_started=0.0,
            external_deadline=5.0,
            expected_invocation=cast(
                dict[str, object],
                cast(dict[str, object], document["invocation"])["identity"],
            ),
        )

    receipt = cast(dict[str, object], json.loads((output / "result.json").read_bytes()))
    assert receipt["status"] == "partial"
    assert receipt["disposition"] == "incomplete"
    assert receipt["phase"] == "operational-failure"
    assert not any(path.name.startswith(".result-admission-") for path in output.iterdir())


def _run_staging_resource_control(
    tmp_path: Path,
    *,
    mode: str,
    signal_number: signal.Signals,
    stage_number: int,
) -> dict[str, object]:
    output = tmp_path / f"{mode}-{signal_number.name}-stage-{stage_number}"
    output.mkdir()
    calibration.write_result(output, _terminal_candidate_summary(output))
    observation_path = tmp_path / f"{output.name}.json"
    supervisor_program = f"""
import json
import os
import signal
import threading
from pathlib import Path
from unittest.mock import patch
from devtools import calibrate_fixed_core_packet as calibration

output = Path({str(output)!r})
observation_path = Path({str(observation_path)!r})
document = json.loads((output / "result.json").read_bytes())
mode = {mode!r}
signal_number = signal.Signals({int(signal_number)!r})
deliveries = []
created = []
stage_calls = [0]
fdopen_calls = [0]
system_handlers = {{item: signal.getsignal(item) for item in (
    signal.SIGINT, signal.SIGTERM, signal.SIGHUP
)}}

def prior_handler(signum, _frame):
    deliveries.append(signum)

signal.signal(signal_number, prior_handler)
expected_handlers = {{item: signal.getsignal(item) for item in system_handlers}}
expected_mask = signal.pthread_sigmask(signal.SIG_BLOCK, set())
ready = threading.Event()
stop = threading.Event()
helper = None
if mode == "other-thread":
    def background():
        signal.pthread_sigmask(
            signal.SIG_UNBLOCK, (signal.SIGINT, signal.SIGTERM, signal.SIGHUP)
        )
        ready.set()
        stop.wait(2.0)

    helper = threading.Thread(target=background)
    helper.start()
    if not ready.wait(1.0):
        raise RuntimeError("signal helper did not become eligible")

real_mkstemp = calibration.tempfile.mkstemp
real_fdopen = calibration.os.fdopen

def create(*args, **kwargs):
    descriptor, temporary = real_mkstemp(*args, **kwargs)
    stage_calls[0] += 1
    if stage_calls[0] == {stage_number!r}:
        created.append((descriptor, temporary))
        if mode in {{"main-thread", "other-thread"}}:
            os.kill(os.getpid(), signal_number)
            if helper is not None:
                threading.Event().wait(0.05)
    return descriptor, temporary

def adopt(*args, **kwargs):
    fdopen_calls[0] += 1
    if mode == "fdopen-error" and fdopen_calls[0] == {stage_number!r}:
        raise OSError("retained descriptor-adoption fault")
    return real_fdopen(*args, **kwargs)

class Worker:
    pid = 101
    states = iter((None, None, 0))

    def poll(self):
        return next(self.states)

class Readback:
    pid = 102

    @staticmethod
    def wait(*, timeout):
        del timeout
        return 0

def sample(process_group, **kwargs):
    return {{
        "elapsed_seconds": kwargs["elapsed"],
        "phase": kwargs["phase"],
        "pids": [process_group],
        "rss_bytes": 4096,
        "error": None,
    }}

try:
    with (
        patch.object(calibration.subprocess, "Popen", side_effect=[Worker(), Readback()]),
        patch.object(calibration, "_reap_process_group", return_value=(0, 0.0)),
        patch.object(calibration.time, "perf_counter", return_value=0.2),
        patch.object(calibration.time, "sleep", return_value=None),
        patch.object(calibration, "_sample_process_group", side_effect=sample),
        patch.object(calibration.tempfile, "mkstemp", side_effect=create),
        patch.object(calibration.os, "fdopen", side_effect=adopt),
    ):
        status = None
        raised = None
        try:
            status = calibration.supervise_worker(
                ("control", "--worker"),
                output,
                repository=Path({str(REPOSITORY)!r}),
                expected_revision={REVISION!r},
                external_seconds=5.0,
                grace_seconds=0.05,
                invocation_started=0.0,
                external_deadline=5.0,
                expected_invocation=document["invocation"]["identity"],
            )
        except BaseException as error:
            raised = f"{{type(error).__name__}}: {{error}}"
    receipt = json.loads((output / "result.json").read_bytes())
    descriptor, temporary = created[0]
    try:
        os.fstat(descriptor)
    except OSError:
        descriptor_open = False
    else:
        descriptor_open = True
    readback_error = None
    try:
        calibration.validate_document(receipt)
        calibration._validate_retained_artifact_set(output)
    except calibration.CalibrationError as error:
        readback_error = str(error)
    observation_path.write_text(
        json.dumps(
            {{
                "status": status,
                "raised": raised,
                "receipt_status": receipt["status"],
                "receipt_phase": receipt["phase"],
                "supervisor_signal": receipt["supervision"]["supervisor_signal"],
                "descriptor_open": descriptor_open,
                "staged_path_exists": Path(temporary).exists(),
                "staged_files": sorted(
                    path.name for path in output.glob(".result-admission-*")
                ),
                "readback_error": readback_error,
                "handlers_restored": all(
                    signal.getsignal(item) is expected
                    for item, expected in expected_handlers.items()
                ),
                "mask_restored": (
                    signal.pthread_sigmask(signal.SIG_BLOCK, set()) == expected_mask
                ),
                "deliveries": deliveries,
            }}
        ),
        encoding="utf-8",
    )
finally:
    stop.set()
    if helper is not None:
        helper.join(1.0)
    for item, handler in system_handlers.items():
        signal.signal(item, handler)
"""
    supervisor = subprocess.run(
        (sys.executable, "-c", supervisor_program),
        check=False,
        timeout=5.0,
    )
    assert supervisor.returncode == 0
    return cast(dict[str, object], json.loads(observation_path.read_text(encoding="utf-8")))


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX signals are required")
@pytest.mark.parametrize("stage_number", [1, 2])
@pytest.mark.parametrize("signal_number", [signal.SIGINT, signal.SIGTERM, signal.SIGHUP])
@pytest.mark.parametrize("mode", ["main-thread", "other-thread"])
def test_real_signal_during_staging_acquisition_defers_until_resource_is_owned(
    tmp_path: Path,
    stage_number: int,
    signal_number: signal.Signals,
    mode: str,
) -> None:
    observation = _run_staging_resource_control(
        tmp_path,
        mode=mode,
        signal_number=signal_number,
        stage_number=stage_number,
    )
    assert observation == {
        "status": 128 + signal_number,
        "raised": None,
        "receipt_status": "partial",
        "receipt_phase": "operational-failure",
        "supervisor_signal": signal_number,
        "descriptor_open": False,
        "staged_path_exists": False,
        "staged_files": [],
        "readback_error": None,
        "handlers_restored": True,
        "mask_restored": True,
        "deliveries": [signal_number],
    }


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX signal masks are required")
@pytest.mark.parametrize("stage_number", [1, 2])
def test_fdopen_failure_closes_unadopted_staging_descriptor(
    tmp_path: Path,
    stage_number: int,
) -> None:
    observation = _run_staging_resource_control(
        tmp_path,
        mode="fdopen-error",
        signal_number=signal.SIGINT,
        stage_number=stage_number,
    )
    assert observation == {
        "status": None,
        "raised": "OSError: retained descriptor-adoption fault",
        "receipt_status": "partial",
        "receipt_phase": "operational-failure",
        "supervisor_signal": None,
        "descriptor_open": False,
        "staged_path_exists": False,
        "staged_files": [],
        "readback_error": None,
        "handlers_restored": True,
        "mask_restored": True,
        "deliveries": [],
    }


def test_worker_git_oserror_remains_operationally_unresolved(
    tmp_path: Path,
) -> None:
    output = tmp_path / "worker-oserror"
    output.mkdir()
    started = time.perf_counter()
    _seed(output, invocation_started=started)
    with patch(
        "devtools.calibrate_fixed_core_packet.source_manifest",
        side_effect=OSError("transient Git failure"),
    ):
        status = calibration.run_worker(
            REPOSITORY,
            REVISION,
            output,
            workers=1,
            calibration_seconds=1.0,
            external_seconds=2.0,
            grace_seconds=0.05,
            invocation_started=started,
            calibration_deadline=started + 1.0,
            external_deadline=started + 2.0,
            run_order=1,
            cache_observation="test process; cache state unmeasured",
            background_load="test host; background load unmeasured",
        )
    receipt = json.loads((output / "result.json").read_bytes())
    assert status == 1
    assert receipt["status"] == "partial"
    assert receipt["phase"] == "operational-failure"
    assert "transient Git failure" in receipt["error"]


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX signals are required")
@pytest.mark.parametrize(
    ("signal_number", "delivery", "handler_mode"),
    [
        (signal.SIGTERM, "running", "default"),
        (signal.SIGHUP, "launch", "default"),
        (signal.SIGINT, "launch", "custom"),
    ],
)
def test_real_supervisor_signal_reaps_worker_including_launch_window(
    tmp_path: Path,
    signal_number: signal.Signals,
    delivery: str,
    handler_mode: str,
) -> None:
    during_launch = delivery == "launch"
    output = tmp_path / f"signal-{signal_number.name}"
    output.mkdir()
    _seed(output)
    worker_pid_path = tmp_path / f"worker-{signal_number.name}.pid"
    prior_handler_path = tmp_path / f"prior-handler-{signal_number.name}.txt"
    custom_handler = handler_mode == "custom"
    supervisor_program = f"""
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from devtools import calibrate_fixed_core_packet as calibration

real_popen = subprocess.Popen
pid_path = Path({str(worker_pid_path)!r})
prior_handler_path = Path({str(prior_handler_path)!r})
during_launch = {during_launch!r}
signal_number = signal.Signals({int(signal_number)!r})

if {custom_handler!r}:
    def prior_handler(signum, _frame):
        prior_handler_path.write_text(str(signum), encoding="utf-8")
    signal.signal(signal_number, prior_handler)

def launch(*args, **kwargs):
    process = real_popen(*args, **kwargs)
    # Publish by rename: the test polls for the file and must never see it empty.
    staged_pid_path = pid_path.with_name(pid_path.name + ".tmp")
    staged_pid_path.write_text(str(process.pid), encoding="utf-8")
    os.replace(staged_pid_path, pid_path)
    if during_launch:
        os.kill(os.getpid(), signal_number)
    return process

calibration.subprocess.Popen = launch
started = time.perf_counter()
status = calibration.supervise_worker(
    (sys.executable, "-c", "import time; time.sleep(60)"),
    Path({str(output)!r}),
    repository=Path({str(REPOSITORY)!r}),
    expected_revision={REVISION!r},
    external_seconds=60.0,
    grace_seconds=0.05,
    invocation_started=started,
    external_deadline=started + 60.0,
)
raise SystemExit(status)
"""
    supervisor = subprocess.Popen((sys.executable, "-c", supervisor_program))
    deadline = time.monotonic() + 3.0
    while not worker_pid_path.exists() and time.monotonic() < deadline:
        time.sleep(0.01)
    assert worker_pid_path.exists()
    worker_pid = int(worker_pid_path.read_text())
    if not during_launch:
        os.kill(supervisor.pid, signal_number)
    expected_status = 128 + signal_number if custom_handler else -signal_number
    assert supervisor.wait(timeout=3.0) == expected_status

    receipt = cast(dict[str, object], json.loads((output / "result.json").read_bytes()))
    assert receipt["status"] == "partial"
    assert receipt["phase"] == "operational-failure"
    assert cast(dict[str, object], receipt["supervision"])["status"] == (
        "supervisor-interrupted"
    )
    assert cast(dict[str, object], receipt["supervision"])["supervisor_signal"] == (
        signal_number
    )
    assert prior_handler_path.exists() is custom_handler
    if custom_handler:
        assert prior_handler_path.read_text(encoding="utf-8") == str(signal_number)
    with pytest.raises(ProcessLookupError):
        os.kill(worker_pid, 0)


def test_cpu_observations_reconstruct_elapsed_measurements() -> None:
    resources: dict[str, object] = {
        "cpu_observations": {
            "coordinator_start_seconds": 2.0,
            "coordinator_end_seconds": 3.5,
            "direct_children_user_start_seconds": 4.0,
            "direct_children_user_end_seconds": 4.25,
            "direct_children_system_start_seconds": 5.0,
            "direct_children_system_end_seconds": 5.125,
        },
        "coordinator_process_seconds": 1.5,
        "reaped_direct_children_user_seconds": 0.25,
        "reaped_direct_children_system_seconds": 0.125,
    }
    calibration._validate_cpu_observations(resources, required=True)
    resources["coordinator_process_seconds"] = 1.25
    with pytest.raises(calibration.CalibrationError, match="retained observations"):
        calibration._validate_cpu_observations(resources, required=True)


def test_terminal_rss_requires_ordered_repeated_samples(tmp_path: Path) -> None:
    one_sample = [
        {
            "elapsed_seconds": 0.1,
            "phase": "preflight",
            "pids": [101],
            "rss_bytes": 1024,
            "error": None,
        }
    ]
    resources: dict[str, object] = {
        "rss": calibration._write_rss_samples(tmp_path, one_sample, observation_lifetime=0.2)
    }
    with pytest.raises(calibration.CalibrationError, match="requires observed"):
        calibration._validate_rss_observations(tmp_path, resources, required=True)

    reversed_samples = [
        {**one_sample[0], "elapsed_seconds": 0.2},
        {**one_sample[0], "elapsed_seconds": 0.1},
    ]
    resources["rss"] = calibration._write_rss_samples(
        tmp_path, reversed_samples, observation_lifetime=0.3
    )
    with pytest.raises(calibration.CalibrationError, match="times are not monotonic"):
        calibration._validate_rss_observations(tmp_path, resources, required=True)

    one_positive = [
        one_sample[0],
        {
            "elapsed_seconds": 0.2,
            "phase": "preflight",
            "pids": [],
            "rss_bytes": 0,
            "error": None,
        },
    ]
    resources["rss"] = calibration._write_rss_samples(
        tmp_path,
        one_positive,
        observation_lifetime=0.3,
    )
    with pytest.raises(calibration.CalibrationError, match="requires observed"):
        calibration._validate_rss_observations(tmp_path, resources, required=True)

    two_positive = [
        one_sample[0],
        {**one_sample[0], "elapsed_seconds": 0.2},
    ]
    resources["rss"] = calibration._write_rss_samples(
        tmp_path,
        two_positive,
        observation_lifetime=0.3,
    )
    calibration._validate_rss_observations(tmp_path, resources, required=True)
    cast(dict[str, object], resources["rss"])["positive_sample_count"] = 1
    with pytest.raises(calibration.CalibrationError, match="reconstruct"):
        calibration._validate_rss_observations(tmp_path, resources, required=True)


def test_worker_refuses_arguments_that_differ_from_seeded_invocation(
    tmp_path: Path,
) -> None:
    output = tmp_path / "invocation-mismatch"
    output.mkdir()
    started = time.perf_counter()
    _seed(output, invocation_started=started)
    with (
        patch("devtools.calibrate_fixed_core_packet.source_manifest") as manifest,
        patch("devtools.calibrate_fixed_core_packet.execute_calibration") as execute,
    ):
        status = calibration.run_worker(
            REPOSITORY,
            REVISION,
            output,
            workers=2,
            calibration_seconds=1.0,
            external_seconds=2.0,
            grace_seconds=0.05,
            invocation_started=started,
            calibration_deadline=started + 1.0,
            external_deadline=started + 2.0,
            run_order=1,
            cache_observation="test process; cache state unmeasured",
            background_load="test host; background load unmeasured",
        )
    assert status == 2
    manifest.assert_not_called()
    execute.assert_not_called()
    receipt = cast(dict[str, object], json.loads((output / "result.json").read_bytes()))
    assert receipt["status"] == "invalid"
    assert "worker arguments differ" in cast(str, receipt["error"])


def test_reader_refuses_a_different_invocation_identity(tmp_path: Path) -> None:
    output = tmp_path / "reader-identity"
    output.mkdir()
    document = _seed(output)
    expected = deepcopy(
        cast(dict[str, object], cast(dict[str, object], document["invocation"])["identity"])
    )
    expected["requested_workers"] = 2
    with pytest.raises(calibration.CalibrationError, match="invocation differs"):
        calibration.load_result(
            output,
            repository=REPOSITORY,
            expected_revision=REVISION,
            require_supervision=False,
            expected_invocation=expected,
        )
