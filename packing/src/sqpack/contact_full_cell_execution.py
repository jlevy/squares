"""Target-free tagged row plans and derived work for one structural full cell."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from sqpack.contact_full_cell import (
    CanonicalFullCell,
    FullCellCanonicalization,
    FullCellError,
    FullFixedAngleCell,
    price_full_cell,
)

EXECUTION_PLAN_EVIDENCE_ROLE = (
    "target-free structural row plan and derived work only; no numerical matrix, solver, "
    "geometry, feasibility, or optimality claim"
)
EXECUTION_PLAN_CONTRACT = "packing.squares:FullCellExecutionPlan/v1"
EXECUTION_PLAN_PROMOTION_BOUNDARY = (
    "passing advances only BC-017 instrumentation readiness; actual LP execution, "
    "BC-017 completion, BC-018, think-u97a, BC-021, and target-sized execution remain "
    "closed"
)

type FullCellExecutionRowMode = Literal[
    "seated-wall-equality",
    "open-wall-inequality",
    "contact-equality",
    "nonedge-inequality",
]


class FullCellExecutionError(ValueError):
    """A typed refusal to compile or replay a structural execution plan."""

    def __init__(self, kind: str, detail: str):
        super().__init__(detail)
        self.kind = kind


@dataclass(frozen=True, order=True)
class FullCellExecutionRow:
    """One stable structural row identity and its exact declared mode."""

    row_id: str
    mode: FullCellExecutionRowMode


@dataclass(frozen=True)
class FullCellStructuralWork:
    """Counts derived while compiling one canonical structural cell."""

    raw_cell_domain_size: int
    raw_cells_built: int
    axis_order_branches_examined: int
    orbit_images_examined: int
    unique_orbit_images: int
    duplicate_orbit_images: int
    canonical_cells_admitted: int
    wall_rows_compiled: int
    contact_equalities: int
    nonedge_inequalities: int
    pair_constraints_compiled: int
    pair_tests: int
    lp_solver_attempts: int


@dataclass(frozen=True)
class FullCellExecutionPlan:
    """The exact tagged row plan and its replayable structural work receipt."""

    contract: Literal["packing.squares:FullCellExecutionPlan/v1"]
    evidence_role: str
    promotion_boundary: str
    canonical_label: str
    rows: tuple[FullCellExecutionRow, ...]
    work: FullCellStructuralWork


def _canonical_or_refuse(
    canonical: FullCellCanonicalization,
) -> CanonicalFullCell:
    if canonical.status != "canonical":
        raise FullCellExecutionError(
            "full-cell-execution-prerequisite",
            "execution-plan compilation requires a completed canonical cell",
        )
    return canonical


def _compile_rows(canonical: CanonicalFullCell) -> tuple[FullCellExecutionRow, ...]:
    cell = canonical.cell
    wall_rows = tuple(
        FullCellExecutionRow(
            f"wall/{row.square}/{row.wall}",
            "seated-wall-equality" if row.seated else "open-wall-inequality",
        )
        for row in cell.walls
    )
    contact_rows = tuple(
        FullCellExecutionRow(
            f"pair/{row.left}/{row.right}/{row.owner}/{row.axis}/{row.positive}",
            "contact-equality",
        )
        for row in cell.contacts
    )
    nonedge_rows = tuple(
        FullCellExecutionRow(
            f"pair/{row.left}/{row.right}/{row.owner}/{row.axis}/{row.positive}",
            "nonedge-inequality",
        )
        for row in cell.nonedges
    )
    pair_rows = tuple(
        sorted(
            contact_rows + nonedge_rows,
            key=lambda row: row.row_id,
        )
    )
    return wall_rows + pair_rows


def compile_full_cell_execution_plan(
    cell: FullFixedAngleCell,
    canonical: FullCellCanonicalization,
) -> FullCellExecutionPlan:
    """Compile exact tagged rows and derive all work counts from verified inputs."""
    completed = _canonical_or_refuse(canonical)
    try:
        price = price_full_cell(cell, completed)
    except FullCellError as error:
        raise FullCellExecutionError(
            "full-cell-execution-prerequisite",
            "the canonical receipt does not replay against the source full cell",
        ) from error

    rows = _compile_rows(completed)
    wall_rows_compiled = sum(row.row_id.startswith("wall/") for row in rows)
    contact_equalities = sum(row.mode == "contact-equality" for row in rows)
    nonedge_inequalities = sum(row.mode == "nonedge-inequality" for row in rows)
    pair_constraints_compiled = contact_equalities + nonedge_inequalities
    work = FullCellStructuralWork(
        raw_cell_domain_size=price.candidate_domains["raw_cells"],
        raw_cells_built=price.executed_work["raw_cells_built"],
        axis_order_branches_examined=price.executed_work["axis_order_branches_examined"],
        orbit_images_examined=price.executed_work["orbit_images_examined"],
        unique_orbit_images=price.executed_work["unique_orbit_images"],
        duplicate_orbit_images=price.executed_work["duplicate_orbit_images"],
        canonical_cells_admitted=price.executed_work["canonical_cells_emitted"],
        wall_rows_compiled=wall_rows_compiled,
        contact_equalities=contact_equalities,
        nonedge_inequalities=nonedge_inequalities,
        pair_constraints_compiled=pair_constraints_compiled,
        pair_tests=0,
        lp_solver_attempts=0,
    )
    return FullCellExecutionPlan(
        contract=EXECUTION_PLAN_CONTRACT,
        evidence_role=EXECUTION_PLAN_EVIDENCE_ROLE,
        promotion_boundary=EXECUTION_PLAN_PROMOTION_BOUNDARY,
        canonical_label=completed.canonical_label,
        rows=rows,
        work=work,
    )


def replay_full_cell_execution_plan(
    cell: FullFixedAngleCell,
    canonical: FullCellCanonicalization,
    plan: FullCellExecutionPlan,
) -> FullCellExecutionPlan:
    """Recompile a plan and reject any changed row identity, mode, or work count."""
    expected = compile_full_cell_execution_plan(cell, canonical)
    if (
        plan.contract != expected.contract
        or plan.evidence_role != expected.evidence_role
        or plan.promotion_boundary != expected.promotion_boundary
        or plan.canonical_label != expected.canonical_label
        or plan.rows != expected.rows
    ):
        raise FullCellExecutionError(
            "full-cell-row-plan",
            "the retained execution row plan does not replay exactly",
        )
    if plan.work != expected.work:
        raise FullCellExecutionError(
            "full-cell-work-count",
            "the retained structural work counts are not derived from the replayed plan",
        )
    return expected
