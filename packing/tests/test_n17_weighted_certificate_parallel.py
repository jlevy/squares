"""Focused controls for the exp-053 parent-bound parallel profiler."""

from __future__ import annotations

import multiprocessing
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

from cases.n17_weighted_certificate.model import Atom, Direction
from cases.n17_weighted_certificate_parallel import runner as parallel_runner
from cases.n17_weighted_certificate_parallel.runner import (
    DIRECTION_HASH,
    FIXTURE_HASH,
    PARENT_CHECKPOINT,
    PARENT_CHECKPOINT_SHA256,
    PARENT_PROGRESS,
    PARENT_PROGRESS_SHA256,
    RAW_ROOT,
    SOURCE_KERNEL_SHA256,
    ProfileBinding,
    ProfileContext,
    ProfileError,
    cleanup_partial_arms,
    load_parent_context,
    merge_fragments,
    profile_binding_hash,
    run_arm,
    run_selftest,
    validate_pair_parameters,
)

_DIGEST = "0" * 64


def _context() -> ProfileContext:
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
        Direction(
            "five-twelve",
            Fraction(5, 13),
            Fraction(12, 13),
            Fraction(-12, 13),
            Fraction(5, 13),
        ),
    )
    binding = ProfileBinding(
        schema_version=1,
        experiment_id="exp-053",
        hypothesis_id="H-057",
        session_id="session-073",
        launch_revision="synthetic",
        parent_checkpoint_sha256=_DIGEST,
        parent_progress_sha256=_DIGEST,
        parent_binding_hash=_DIGEST,
        parent_previous_row_hash=_DIGEST,
        frozen_package_sha256=_DIGEST,
        fixture_hash=_DIGEST,
        direction_hash=_DIGEST,
        source_kernel_sha256=_DIGEST,
        independent_kernel_sha256=_DIGEST,
        runner_sha256=_DIGEST,
        benchmark_sha256=_DIGEST,
        ordinals=(0, 1, 2),
    )
    return ProfileContext(
        binding=binding,
        atoms=atoms,
        directions=directions,
        outer_side=Fraction(2),
        square_side=Fraction(1),
    )


def test_parent_boundary_replays_without_evaluating_a_direction() -> None:
    context = load_parent_context()

    assert context.binding.parent_checkpoint_sha256 == PARENT_CHECKPOINT_SHA256
    assert context.binding.parent_progress_sha256 == PARENT_PROGRESS_SHA256
    assert context.binding.fixture_hash == FIXTURE_HASH
    assert context.binding.direction_hash == DIRECTION_HASH
    assert context.binding.source_kernel_sha256 == SOURCE_KERNEL_SHA256
    assert context.binding.ordinals == (33, 107, 180)


def test_serial_arm_writes_a_complete_canonical_fragment_set(tmp_path: Path) -> None:
    context = _context()
    receipt = run_arm(tmp_path, "A", context)

    arm = tmp_path / "arm-A"
    assert receipt["mode"] == "serial"
    assert receipt["worker_count"] == 1
    assert len(list((arm / "fragments").glob("fragment-*.json"))) == 3
    assert (arm / "merged.json").read_bytes() == merge_fragments(arm / "fragments", context)
    assert len(profile_binding_hash(context.binding)) == 64
    assert not list(tmp_path.glob(".arm-A.partial-*"))


def test_spawned_workers_match_serial_bytes_and_completed_arms_resume(
    tmp_path: Path,
) -> None:
    context = _context()
    serial = run_arm(tmp_path, "A", context)
    parallel = run_arm(tmp_path, "B", context)

    assert serial["fragment_sha256"] == parallel["fragment_sha256"]
    assert serial["merged_sha256"] == parallel["merged_sha256"]
    serial_receipt = (tmp_path / "arm-A/receipt.json").read_bytes()
    parallel_receipt = (tmp_path / "arm-B/receipt.json").read_bytes()

    assert run_arm(tmp_path, "A", context) == serial
    assert run_arm(tmp_path, "B", context) == parallel
    assert (tmp_path / "arm-A/receipt.json").read_bytes() == serial_receipt
    assert (tmp_path / "arm-B/receipt.json").read_bytes() == parallel_receipt


def test_parallel_failure_stops_children_cleans_partial_and_preserves_complete_arm(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    context = _context()
    serial = run_arm(tmp_path, "A", context)
    serial_receipt = (tmp_path / "arm-A/receipt.json").read_bytes()
    before = {process.pid for process in multiprocessing.active_children()}
    original_jobs = parallel_runner._jobs  # pyright: ignore[reportPrivateUsage]  # noqa: SLF001
    escaped_path: Path | None = None

    def invalid_jobs(
        fragment_dir: Path, profile: ProfileContext
    ) -> list[parallel_runner.WorkItem]:
        nonlocal escaped_path
        jobs = original_jobs(fragment_dir, profile)
        outside = fragment_dir.parent.parent / "outside-assigned-fragment-root"
        outside.mkdir()
        escaped_path = outside / jobs[0].output_path.name
        jobs[0] = replace(jobs[0], output_path=escaped_path)
        return jobs

    monkeypatch.setattr(parallel_runner, "_jobs", invalid_jobs)
    with pytest.raises(ProfileError, match="preassigned"):
        run_arm(tmp_path, "B", context)

    assert (tmp_path / "arm-A/receipt.json").read_bytes() == serial_receipt
    assert run_arm(tmp_path, "A", context) == serial
    assert not (tmp_path / "arm-B").exists()
    assert not list(tmp_path.glob(".arm-B.partial-*"))
    assert escaped_path is not None and not escaped_path.exists()
    assert {process.pid for process in multiprocessing.active_children()} == before


def test_stale_partial_cleanup_is_confined_to_one_pair_root(tmp_path: Path) -> None:
    stale = tmp_path / ".arm-B.partial-interrupted"
    stale.mkdir()
    (stale / "partial.json").write_text("{", encoding="utf-8")
    neighbor = tmp_path.with_name(f"{tmp_path.name}-must-survive")
    neighbor.mkdir()

    assert cleanup_partial_arms(tmp_path, "B") == 1
    assert not stale.exists()
    assert neighbor.is_dir()


def test_pair_contract_refuses_ordinal_or_output_substitution() -> None:
    with pytest.raises(ProfileError, match="fixed ordinal"):
        validate_pair_parameters(
            experiment="exp-053",
            session="session-073",
            parent_checkpoint=PARENT_CHECKPOINT,
            parent_progress=PARENT_PROGRESS,
            ordinals=(33, 107, 179),
            workers=3,
            start_method="spawn",
            pair_index=1,
            order="AB",
            output_root=RAW_ROOT / "pair-01-ab",
        )

    with pytest.raises(ProfileError, match="output root"):
        validate_pair_parameters(
            experiment="exp-053",
            session="session-073",
            parent_checkpoint=PARENT_CHECKPOINT,
            parent_progress=PARENT_PROGRESS,
            ordinals=(33, 107, 180),
            workers=3,
            start_method="spawn",
            pair_index=1,
            order="AB",
            output_root=RAW_ROOT / "pair-02-ba",
        )


def test_production_selftest_fires_every_guard_without_skips() -> None:
    receipt = run_selftest()

    assert receipt["passed"] is True
    assert receipt["guard_count"] == 30
    assert receipt["skips"] == 0
    guards = receipt["guards"]
    assert isinstance(guards, dict)
    assert len(guards) == 30
    assert guards["same_basename_outside_root_rejected"] is True
    assert guards["symlink_fragment_root_rejected"] is True
    assert guards["assembler_requires_fixed_three_pairs"] is True
    assert guards["assembler_recomputes_median"] is True
    assert guards["assembler_recomputes_minimum"] is True
    assert guards["assembler_refuses_missing_pair"] is True
    assert guards["assembler_refuses_corrupt_pair"] is True
    assert guards["assembler_refuses_result_overwrite"] is True
    assert guards["assembler_preserves_claim_boundary"] is True
    assert all(guards.values())
