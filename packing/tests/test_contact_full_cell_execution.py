from __future__ import annotations

import inspect
import json
from dataclasses import asdict, replace
from unittest.mock import patch

import pytest

import sqpack.contact_full_cell_execution as execution_module
from devtools.generate_contact_full_cell_control import literal_control_cell
from sqpack.contact_full_cell import (
    CanonicalFullCell,
    FullCellLimits,
    OrientedPairAxis,
    canonicalize_full_cell,
)
from sqpack.contact_full_cell_execution import (
    FullCellExecutionError,
    FullCellExecutionPlan,
    compile_full_cell_execution_plan,
    replay_full_cell_execution_plan,
)

EXPECTED_BASELINE_ROWS = (
    ("wall/0/left", "open-wall-inequality"),
    ("wall/0/right", "seated-wall-equality"),
    ("wall/0/bottom", "open-wall-inequality"),
    ("wall/0/top", "seated-wall-equality"),
    ("wall/1/left", "open-wall-inequality"),
    ("wall/1/right", "open-wall-inequality"),
    ("wall/1/bottom", "open-wall-inequality"),
    ("wall/1/top", "seated-wall-equality"),
    ("wall/2/left", "open-wall-inequality"),
    ("wall/2/right", "seated-wall-equality"),
    ("wall/2/bottom", "open-wall-inequality"),
    ("wall/2/top", "open-wall-inequality"),
    ("pair/0/1/0/u/0", "contact-equality"),
    ("pair/0/2/0/v/0", "contact-equality"),
    ("pair/1/2/1/u/2", "nonedge-inequality"),
)


def _canonical(cell) -> CanonicalFullCell:
    result = canonicalize_full_cell(cell, limits=FullCellLimits(maximum_orbit_images=48))
    assert result.status == "canonical"
    return result


def _row_tuples(plan: FullCellExecutionPlan) -> tuple[tuple[str, str], ...]:
    return tuple((row.row_id, row.mode) for row in plan.rows)


def test_target_free_plan_derives_exact_rows_and_work() -> None:
    cell = literal_control_cell()
    canonical = _canonical(cell)
    with patch("builtins.open", side_effect=AssertionError("unexpected source read")):
        plan = compile_full_cell_execution_plan(cell, canonical)

    assert plan.contract == "packing.squares:FullCellExecutionPlan/v1"
    assert plan.promotion_boundary == (
        "passing advances only BC-017 instrumentation readiness; actual LP execution, "
        "BC-017 completion, BC-018, think-u97a, BC-021, and target-sized execution "
        "remain closed"
    )
    assert _row_tuples(plan) == EXPECTED_BASELINE_ROWS
    modes = [row.mode for row in plan.rows]
    assert modes.count("seated-wall-equality") == 4
    assert modes.count("open-wall-inequality") == 8
    assert modes.count("contact-equality") == 2
    assert modes.count("nonedge-inequality") == 1
    assert len({row.row_id for row in plan.rows}) == len(plan.rows) == 15
    assert plan.work.raw_cell_domain_size == 8
    assert plan.work.raw_cells_built == 1
    assert plan.work.axis_order_branches_examined == 1
    assert plan.work.orbit_images_examined == 48
    assert plan.work.unique_orbit_images == 48
    assert plan.work.duplicate_orbit_images == 0
    assert plan.work.canonical_cells_admitted == 1
    assert plan.work.wall_rows_compiled == 12
    assert plan.work.contact_equalities == 2
    assert plan.work.nonedge_inequalities == 1
    assert plan.work.pair_constraints_compiled == 3
    assert plan.work.pair_tests == 0
    assert plan.work.lp_solver_attempts == 0
    assert replay_full_cell_execution_plan(cell, canonical, plan) == plan


def test_aggregate_preserving_role_swap_does_not_forge_pair_plan_change() -> None:
    cell = literal_control_cell()
    canonical = _canonical(cell)
    baseline = compile_full_cell_execution_plan(cell, canonical)
    swapped = replace(
        cell,
        contacts=(
            OrientedPairAxis(0, 2, 0, "v", 2),
            OrientedPairAxis(1, 2, 1, "u", 1),
        ),
        nonedges=(OrientedPairAxis(0, 1, 0, "u", 1),),
    )
    changed = compile_full_cell_execution_plan(swapped, _canonical(swapped))

    baseline_pairs = _row_tuples(baseline)[12:]
    changed_pairs = _row_tuples(changed)[12:]
    assert baseline_pairs == changed_pairs == EXPECTED_BASELINE_ROWS[12:]
    assert baseline.work == changed.work
    assert baseline.work.pair_constraints_compiled == 3
    assert changed.work.pair_constraints_compiled == 3
    assert baseline.work.raw_cell_domain_size == changed.work.raw_cell_domain_size == 8


def test_non_equivalent_pair_axes_change_the_exact_pair_plan() -> None:
    cell = literal_control_cell()
    baseline = compile_full_cell_execution_plan(cell, _canonical(cell))
    changed_cell = replace(
        cell,
        contacts=(
            OrientedPairAxis(0, 2, 0, "u", 0),
            OrientedPairAxis(1, 2, 1, "u", 1),
        ),
        nonedges=(OrientedPairAxis(0, 1, 0, "u", 0),),
    )
    changed = compile_full_cell_execution_plan(changed_cell, _canonical(changed_cell))

    assert _row_tuples(changed)[12:] == (
        ("pair/0/1/0/u/0", "contact-equality"),
        ("pair/0/2/0/u/0", "contact-equality"),
        ("pair/1/2/1/u/1", "nonedge-inequality"),
    )
    assert _row_tuples(changed)[12:] != EXPECTED_BASELINE_ROWS[12:]
    assert baseline.work == changed.work


def test_wall_flip_changes_one_mode_class_without_changing_domain_size() -> None:
    cell = literal_control_cell()
    baseline = compile_full_cell_execution_plan(cell, _canonical(cell))
    walls = list(cell.walls)
    wall_index = next(
        index for index, row in enumerate(walls) if (row.square, row.wall) == (0, "left")
    )
    walls[wall_index] = replace(walls[wall_index], seated=False)
    flipped = replace(cell, walls=tuple(walls))
    changed = compile_full_cell_execution_plan(flipped, _canonical(flipped))

    differences = tuple(
        (before, after)
        for before, after in zip(_row_tuples(baseline), _row_tuples(changed), strict=True)
        if before != after
    )
    assert differences == (
        (
            ("wall/0/right", "seated-wall-equality"),
            ("wall/0/right", "open-wall-inequality"),
        ),
    )
    assert sum(row.mode == "seated-wall-equality" for row in changed.rows) == 3
    assert sum(row.mode == "open-wall-inequality" for row in changed.rows) == 9
    assert baseline.work.raw_cell_domain_size == changed.work.raw_cell_domain_size


def test_exact_replay_rejects_omitted_rows_and_forged_counts() -> None:
    cell = literal_control_cell()
    canonical = _canonical(cell)
    plan = compile_full_cell_execution_plan(cell, canonical)

    with pytest.raises(FullCellExecutionError) as row_error:
        replay_full_cell_execution_plan(cell, canonical, replace(plan, rows=plan.rows[:-1]))
    assert row_error.value.kind == "full-cell-row-plan"

    with pytest.raises(FullCellExecutionError) as boundary_error:
        replay_full_cell_execution_plan(
            cell,
            canonical,
            replace(
                plan,
                promotion_boundary="passing also advances BC-016 readiness",
            ),
        )
    assert boundary_error.value.kind == "full-cell-row-plan"

    forged = replace(plan, work=replace(plan.work, pair_tests=3))
    with pytest.raises(FullCellExecutionError) as work_error:
        replay_full_cell_execution_plan(cell, canonical, forged)
    assert work_error.value.kind == "full-cell-work-count"


def test_replay_rejects_aggregate_preserving_contact_nonedge_mode_swap() -> None:
    cell = literal_control_cell()
    canonical = _canonical(cell)
    plan = compile_full_cell_execution_plan(cell, canonical)
    rows = list(plan.rows)
    contact_index = next(
        index for index, row in enumerate(rows) if row.mode == "contact-equality"
    )
    nonedge_index = next(
        index for index, row in enumerate(rows) if row.mode == "nonedge-inequality"
    )
    rows[contact_index] = replace(rows[contact_index], mode="nonedge-inequality")
    rows[nonedge_index] = replace(rows[nonedge_index], mode="contact-equality")
    mutation = replace(plan, rows=tuple(rows))
    assert sum(row.mode == "contact-equality" for row in mutation.rows) == 2
    assert sum(row.mode == "nonedge-inequality" for row in mutation.rows) == 1
    assert mutation.work == plan.work

    with pytest.raises(FullCellExecutionError) as error:
        replay_full_cell_execution_plan(cell, canonical, mutation)
    assert error.value.kind == "full-cell-row-plan"


def test_plan_contains_no_numerical_or_target_claim_surface() -> None:
    cell = literal_control_cell()
    plan = compile_full_cell_execution_plan(cell, _canonical(cell))
    document = json.dumps(asdict(plan), sort_keys=True).lower()
    forbidden = (
        '"side":',
        '"coordinates":',
        '"centres":',
        '"outcome":',
        '"feasible":',
        '"optimal":',
        '"container_fit":',
        '"target":',
        '"n11":',
        '"solver_status":',
        '"coefficients":',
        '"rhs":',
        '"digest":',
        '"hash":',
    )
    assert all(term not in document for term in forbidden)

    source = inspect.getsource(execution_module)
    for forbidden_source in ("solve_cell", "linprog", "known-best", "frontier/"):
        assert forbidden_source not in source
