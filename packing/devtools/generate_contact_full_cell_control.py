#!/usr/bin/env python3
"""Generate the literal target-free structural full-cell control."""

from __future__ import annotations

import argparse
import json
from collections.abc import Callable
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any
from unittest.mock import patch

from jsonschema import Draft202012Validator
from strif import atomic_output_file

from sqpack.contact_assembly import D4_BY_NAME, Axis
from sqpack.contact_full_cell import (
    AssemblyPart,
    CanonicalFullCell,
    FullCellError,
    FullCellLimits,
    FullCellPrice,
    FullFixedAngleCell,
    OrientedPairAxis,
    WallDecision,
    canonicalize_full_cell,
    price_full_cell,
    replay_full_cell_witness,
    transform_full_cell,
)
from sqpack.contact_full_cell_execution import (
    FullCellExecutionError,
    FullCellExecutionPlan,
    compile_full_cell_execution_plan,
    replay_full_cell_execution_plan,
)
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "atlas/known-best/contact-full-cell-control.json"
SCHEMA = ROOT / "atlas/known-best/contact-full-cell-control.schema.yaml"
GENERATOR = "python -m devtools.generate_contact_full_cell_control"
EVIDENCE_ROLE = (
    "target-free structural full-cell label and work price; no geometry, container fit, "
    "packing feasibility, or optimality claim"
)
PROMOTION_BOUNDARY = (
    "passing authorizes only a BC-016 or BC-017 readiness decision; BC-021 and "
    "target-sized execution remain closed"
)
D4_AXIS_TABLE: dict[str, dict[Axis, tuple[Axis, int]]] = {
    "identity": {"u": ("u", 1), "v": ("v", 1)},
    "rotate-90": {"u": ("v", 1), "v": ("u", -1)},
    "rotate-180": {"u": ("u", -1), "v": ("v", -1)},
    "rotate-270": {"u": ("v", -1), "v": ("u", 1)},
    "reflect-x": {"u": ("u", 1), "v": ("v", -1)},
    "reflect-y": {"u": ("u", -1), "v": ("v", 1)},
    "reflect-diagonal": {"u": ("v", 1), "v": ("u", 1)},
    "reflect-antidiagonal": {"u": ("v", -1), "v": ("u", -1)},
}


def _axis(left: int, right: int, axis: Axis, positive: int) -> OrientedPairAxis:
    return OrientedPairAxis(left, right, left, axis, positive)


def literal_control_cell() -> FullFixedAngleCell:
    """Return the source-free three-square L label used by CG-010."""
    seated = {
        (0, "left"),
        (0, "bottom"),
        (1, "bottom"),
        (2, "left"),
    }
    return FullFixedAngleCell(
        angle_frame="axis-aligned/v1",
        angles=("0", "0", "0"),
        parts=tuple(AssemblyPart("free", (square,)) for square in range(3)),
        walls=tuple(
            WallDecision(square, wall, (square, wall) in seated)
            for square in range(3)
            for wall in ("left", "right", "bottom", "top")
        ),
        contacts=(_axis(0, 1, "u", 1), _axis(0, 2, "v", 2)),
        nonedges=(_axis(1, 2, "u", 1),),
    )


def _refusal(kind: str, operation: Callable[[], object]) -> dict[str, str]:
    try:
        operation()
    except FullCellError as error:
        if error.kind != kind:
            raise AssertionError(f"expected {kind}, got {error.kind}") from error
        return {"status": "passing", "observed_kind": error.kind}
    raise AssertionError(f"mutation did not trigger {kind}")


def _execution_refusal(kind: str, operation: Callable[[], object]) -> dict[str, str]:
    try:
        operation()
    except FullCellExecutionError as error:
        if error.kind != kind:
            raise AssertionError(f"expected {kind}, got {error.kind}") from error
        return {"status": "passing", "observed_kind": error.kind}
    raise AssertionError(f"mutation did not trigger {kind}")


def _fixture_document(cell: FullFixedAngleCell) -> dict[str, Any]:
    return {
        "angle_frame": cell.angle_frame,
        "angles": list(cell.angles),
        "parts": [{"kind": part.kind, "members": list(part.members)} for part in cell.parts],
        "walls": [asdict(row) for row in cell.walls],
        "contacts": [asdict(row) for row in cell.contacts],
        "nonedges": [asdict(row) for row in cell.nonedges],
    }


def _execution_plan_document(plan: FullCellExecutionPlan) -> dict[str, Any]:
    return {
        "contract": plan.contract,
        "evidence_role": plan.evidence_role,
        "promotion_boundary": plan.promotion_boundary,
        "canonical_label": plan.canonical_label,
        "rows": [asdict(row) for row in plan.rows],
        "work": asdict(plan.work),
    }


def _positive_under_read_trap() -> tuple[
    FullFixedAngleCell,
    CanonicalFullCell,
    FullCellPrice,
    FullCellExecutionPlan,
]:
    with patch("builtins.open", side_effect=AssertionError("unexpected source read")):
        cell = literal_control_cell()
        canonical = canonicalize_full_cell(cell, limits=FullCellLimits(maximum_orbit_images=48))
        if canonical.status != "canonical":
            raise AssertionError("the 48-image positive control did not complete")
        if replay_full_cell_witness(cell, canonical.witness) != canonical.cell:
            raise AssertionError("the retained full-cell witness did not replay")
        price = price_full_cell(cell, canonical)
        execution_plan = compile_full_cell_execution_plan(cell, canonical)
        if replay_full_cell_execution_plan(cell, canonical, execution_plan) != execution_plan:
            raise AssertionError("the retained full-cell execution plan did not replay")
    return cell, canonical, price, execution_plan


def expected_document() -> dict[str, Any]:
    """Build and independently exercise the byte-stable target-free control."""
    cell, canonical, price, execution_plan = _positive_under_read_trap()

    limited = canonicalize_full_cell(cell, limits=FullCellLimits(maximum_orbit_images=47))
    if limited.status != "limit":
        raise AssertionError("the 47-image orbit mutation did not stop")

    d4_cases = 0
    negative_d4_cases = 0
    for symmetry_name, axis_rows in D4_AXIS_TABLE.items():
        for source_axis, (expected_axis, polarity) in axis_rows.items():
            source = replace(cell, nonedges=(_axis(1, 2, source_axis, 1),))
            image = transform_full_cell(
                source,
                symmetry=D4_BY_NAME[symmetry_name],
                old_to_new=(0, 1, 2),
            )
            expected_positive = 1 if polarity > 0 else 2
            if (image.nonedges[0].axis, image.nonedges[0].positive) != (
                expected_axis,
                expected_positive,
            ):
                raise AssertionError(f"D4 pair-axis mismatch at {symmetry_name}/{source_axis}")
            d4_cases += 1
            negative_d4_cases += polarity < 0
    reversed_image = transform_full_cell(
        cell,
        symmetry=D4_BY_NAME["rotate-90"],
        old_to_new=(0, 2, 1),
    )
    if reversed_image.nonedges[0] != OrientedPairAxis(1, 2, 1, "v", 2):
        raise AssertionError("pair ids were not mapped before sorted endpoint storage")

    other_walls = (replace(cell.walls[0], seated=False), *cell.walls[1:])
    other = replace(cell, walls=other_walls)
    other_canonical = canonicalize_full_cell(other)
    if other_canonical.status != "canonical":
        raise AssertionError("the mismatched-receipt mutation did not canonicalize")

    contact_index = next(
        index for index, row in enumerate(execution_plan.rows) if row.mode == "contact-equality"
    )
    nonedge_index = next(
        index
        for index, row in enumerate(execution_plan.rows)
        if row.mode == "nonedge-inequality"
    )
    role_swapped_rows = list(execution_plan.rows)
    role_swapped_rows[contact_index] = replace(
        role_swapped_rows[contact_index], mode="nonedge-inequality"
    )
    role_swapped_rows[nonedge_index] = replace(
        role_swapped_rows[nonedge_index], mode="contact-equality"
    )
    role_swapped_plan = replace(execution_plan, rows=tuple(role_swapped_rows))
    if (
        sum(row.mode == "contact-equality" for row in role_swapped_plan.rows)
        != execution_plan.work.contact_equalities
        or sum(row.mode == "nonedge-inequality" for row in role_swapped_plan.rows)
        != execution_plan.work.nonedge_inequalities
        or role_swapped_plan.work != execution_plan.work
    ):
        raise AssertionError("the execution-plan role swap changed aggregate work")

    controls = {
        "positive-completeness": {"status": "passing"},
        "omitted-wall": _refusal(
            "full-cell-wall-inventory",
            lambda: replace(cell, walls=cell.walls[:-1]),
        ),
        "omitted-pair-axis": _refusal(
            "full-cell-pair-inventory", lambda: replace(cell, nonedges=())
        ),
        "duplicate-pair-axis": _refusal(
            "full-cell-pair-inventory",
            lambda: replace(cell, nonedges=(cell.nonedges[0], cell.nonedges[0])),
        ),
        "d4-negative-polarity": {
            "status": "passing",
            "cases_checked": d4_cases,
            "negative_cases_checked": negative_d4_cases,
            "reversed_relabel_checked": True,
        },
        "orbit-image-cap": {
            "status": "passing",
            "observed_kind": limited.kind,
            "limit": limited.limit,
            "required_images": limited.required_images,
            "examined_images": limited.examined_images,
            "canonical_cells_emitted": 0,
            "lp_solves": 0,
        },
        "mismatched-price-receipt": _refusal(
            "full-cell-price-prerequisite",
            lambda: price_full_cell(cell, other_canonical),
        ),
        "execution-plan-replay": {"status": "passing"},
        "execution-plan-omitted-row": _execution_refusal(
            "full-cell-row-plan",
            lambda: replay_full_cell_execution_plan(
                cell,
                canonical,
                replace(execution_plan, rows=execution_plan.rows[:-1]),
            ),
        ),
        "execution-plan-role-swap": _execution_refusal(
            "full-cell-row-plan",
            lambda: replay_full_cell_execution_plan(cell, canonical, role_swapped_plan),
        ),
        "execution-plan-forged-count": _execution_refusal(
            "full-cell-work-count",
            lambda: replay_full_cell_execution_plan(
                cell,
                canonical,
                replace(
                    execution_plan,
                    work=replace(execution_plan.work, pair_tests=1),
                ),
            ),
        ),
        "source-isolation": {
            "status": "passing",
            "source": "literal-source-free-n3-axis-aligned-L/v1",
            "attempted_reads": 0,
        },
    }
    return {
        "softschema": {
            "contract": "packing.squares:ContactFullCellControl/v1",
            "schema": SCHEMA.name,
            "envelope": "control",
            "status": "enforced",
        },
        "control": {
            "generated_by": GENERATOR,
            "scope": "one literal axis-aligned three-square structural cell",
            "evidence_role": EVIDENCE_ROLE,
            "fixture": _fixture_document(cell),
            "canonical": {
                "contract": "packing.squares:FullFixedAngleCellLabel/v1",
                "label": canonical.canonical_label,
                "witness": {
                    "symmetry": canonical.witness.symmetry,
                    "old_to_new": list(canonical.witness.old_to_new),
                },
                "raw_image_count": canonical.raw_image_count,
                "unique_image_count": canonical.unique_image_count,
                "duplicate_image_count": canonical.raw_image_count
                - canonical.unique_image_count,
            },
            "price": asdict(price),
            "execution_plan": _execution_plan_document(execution_plan),
            "caps": {"maximum_orbit_images": 48},
            "controls": controls,
            "promotion_boundary": PROMOTION_BOUNDARY,
        },
    }


def _text(document: dict[str, Any]) -> str:
    return json.dumps(document, indent=2, sort_keys=True) + "\n"


def validate_document(document: dict[str, Any]) -> None:
    """Validate the control payload against its enforced soft schema."""
    schema = safe_load(SCHEMA.read_text(encoding="utf-8"))
    problems = sorted(
        Draft202012Validator(schema).iter_errors(document["control"]),
        key=lambda problem: list(problem.path),
    )
    if problems:
        raise ValueError(f"full-cell control schema failure: {problems[0].message}")


def update() -> None:
    document = expected_document()
    validate_document(document)
    with atomic_output_file(OUTPUT) as temporary:
        temporary.write_text(_text(document), encoding="utf-8")
    print("contact full-cell control updated")


def check() -> None:
    document = expected_document()
    validate_document(document)
    if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != _text(document):
        raise ValueError(f"{OUTPUT.relative_to(ROOT)} is stale")
    print("contact full-cell control check passed")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true")
    mode.add_argument("--check", action="store_true")
    return command


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.update:
        update()
    else:
        check()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
