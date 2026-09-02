"""Target-blind controls for the external n = 17 resumability boundary."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from cases.n17_weighted_certificate.model import Atom, Direction, canonical_hash
from cases.n17_weighted_certificate.source_faithful import accumulate_source_faithful
from cases.n17_weighted_certificate.target_independent import (
    accumulate_target_independent,
)
from cases.n17_weighted_certificate_resume.run import (
    FROZEN_PACKAGE_SHA256,
    FROZEN_SOURCE_SHA256,
    SCHEMA_VERSION,
    CheckpointError,
    CheckpointStore,
    DirectionSlicedDriver,
    RunBinding,
    driver_sha256,
    fixture_binding_hash,
    frozen_package_manifest_sha256,
    run_selftest,
    verify_frozen_inputs,
)


def _fixture() -> tuple[tuple[Atom, ...], tuple[Direction, ...], Fraction, Fraction]:
    atoms = (
        Atom("a", Fraction(1, 2), Fraction(1, 2), Fraction(1)),
        Atom("b", Fraction(1), Fraction(1), Fraction(2)),
        Atom("c", Fraction(3, 2), Fraction(3, 2), Fraction(3)),
    )
    directions = (
        Direction("axis", Fraction(1), Fraction(0), Fraction(0), Fraction(1)),
        Direction(
            "three-four",
            Fraction(3, 5),
            Fraction(4, 5),
            Fraction(-4, 5),
            Fraction(3, 5),
        ),
    )
    return atoms, directions, Fraction(2), Fraction(1)


def _store(tmp_path: Path) -> tuple[CheckpointStore, tuple[Atom, ...], Fraction, Fraction]:
    atoms, directions, outer_side, square_side = _fixture()
    checkpoint = tmp_path / "round.checkpoint.json"
    progress = tmp_path / "round.progress.json"
    binding = RunBinding(
        schema_version=SCHEMA_VERSION,
        experiment_id="exp-052",
        hypothesis_id="H-052",
        session_id="session-068",
        package_manifest_sha256=FROZEN_PACKAGE_SHA256,
        source_sha256=FROZEN_SOURCE_SHA256,
        fixture_hash=fixture_binding_hash(
            atoms=atoms,
            directions=directions,
            outer_side=outer_side,
            square_side=square_side,
        ),
        direction_count=len(directions),
        direction_hash=canonical_hash(directions),
        driver_sha256=driver_sha256(),
        result_path=str(tmp_path / "round.json"),
        checkpoint_path=str(checkpoint),
        progress_path=str(progress),
    )
    return (
        CheckpointStore(
            binding=binding,
            directions=directions,
            result_path=tmp_path / "round.json",
            checkpoint_path=checkpoint,
            progress_path=progress,
        ),
        atoms,
        outer_side,
        square_side,
    )


def test_frozen_source_and_package_hashes_match() -> None:
    verify_frozen_inputs()
    assert frozen_package_manifest_sha256() == FROZEN_PACKAGE_SHA256


def test_driver_atomically_round_trips_complete_pairs(tmp_path: Path) -> None:
    store, atoms, outer_side, square_side = _store(tmp_path)
    checkpoint = DirectionSlicedDriver(store).run(
        atoms=atoms, outer_side=outer_side, square_side=square_side
    )

    assert checkpoint == store.load()
    assert len(checkpoint.rows) == 2
    assert all(row.agreement for row in checkpoint.rows)
    assert not store.progress_path.exists()
    assert not list(tmp_path.glob(".*.tmp"))


def test_source_only_stage_is_not_a_completed_row_and_resumes(tmp_path: Path) -> None:
    store, atoms, outer_side, square_side = _store(tmp_path)
    calls = 0

    def interrupted(*args: object) -> object:
        nonlocal calls
        calls += 1
        raise RuntimeError("synthetic interruption")

    with pytest.raises(RuntimeError, match="synthetic interruption"):
        DirectionSlicedDriver(
            store,
            independent_accumulator=interrupted,  # type: ignore[arg-type]
        ).run(atoms=atoms, outer_side=outer_side, square_side=square_side)

    assert store.load().rows == ()
    marker = json.loads(store.progress_path.read_text(encoding="utf-8"))
    assert marker["ordinal"] == 0
    assert marker["stage"] == "independent_started"

    resumed = DirectionSlicedDriver(store).run(
        atoms=atoms, outer_side=outer_side, square_side=square_side
    )
    assert calls == 1
    assert len(resumed.rows) == 2


def test_changed_row_hash_is_rejected(tmp_path: Path) -> None:
    store, atoms, outer_side, square_side = _store(tmp_path)
    DirectionSlicedDriver(store).run(
        atoms=atoms, outer_side=outer_side, square_side=square_side
    )
    raw = json.loads(store.checkpoint_path.read_text(encoding="utf-8"))
    raw["rows"][0]["row_hash"] = "f" * 64
    store.checkpoint_path.write_text(json.dumps(raw), encoding="utf-8")

    with pytest.raises(CheckpointError, match="row hash changed"):
        store.load()


def test_real_accumulators_agree_on_each_synthetic_direction() -> None:
    atoms, directions, outer_side, square_side = _fixture()
    for direction in directions:
        assert accumulate_source_faithful(
            atoms, direction, outer_side, square_side
        ) == accumulate_target_independent(atoms, direction, outer_side, square_side)


def test_production_selftest_runs_every_target_blind_guard_without_asserts() -> None:
    receipt = run_selftest()
    if receipt.get("passed") is not True:
        raise AssertionError("production selftest did not report an unqualified pass")
    guards = receipt.get("receipts")
    if not isinstance(guards, dict) or len(guards) != 27 or not all(guards.values()):
        raise AssertionError("production selftest guard inventory is incomplete")
