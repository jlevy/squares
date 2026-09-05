from __future__ import annotations

import inspect
import json
import math
from dataclasses import replace
from itertools import permutations
from typing import cast
from unittest.mock import patch

import pytest

import sqpack.contact_full_cell as full_cell_module
from sqpack.contact_assembly import D4_BY_NAME, D4_TRANSFORMS, Axis
from sqpack.contact_full_cell import (
    AssemblyPart,
    FullCellError,
    FullCellLimits,
    FullFixedAngleCell,
    OrientedPairAxis,
    WallDecision,
    canonicalize_full_cell,
    full_cell_label,
    price_full_cell,
    replay_full_cell_witness,
    transform_full_cell,
)


def _axis(left: int, right: int, axis: Axis, positive: int) -> OrientedPairAxis:
    return OrientedPairAxis(left, right, left, axis, positive)


def _l_cell() -> FullFixedAngleCell:
    seated = {
        (0, "left"),
        (0, "bottom"),
        (1, "bottom"),
        (2, "left"),
    }
    walls = tuple(
        WallDecision(square, wall, (square, wall) in seated)
        for square in range(3)
        for wall in ("left", "right", "bottom", "top")
    )
    return FullFixedAngleCell(
        angle_frame="axis-aligned/v1",
        angles=("0", "0", "0"),
        parts=(
            AssemblyPart("free", (0,)),
            AssemblyPart("free", (1,)),
            AssemblyPart("free", (2,)),
        ),
        walls=walls,
        contacts=(_axis(0, 1, "u", 1), _axis(0, 2, "v", 2)),
        nonedges=(_axis(1, 2, "u", 1),),
    )


def _expected_label_document(cell: FullFixedAngleCell) -> dict[str, object]:
    """Decode the label against an independently enumerated channel contract."""
    return {
        "contract": "packing.squares:FullFixedAngleCellLabel/v1",
        "angle_frame": cell.angle_frame,
        "angles": list(cell.angles),
        "parts": [{"kind": part.kind, "members": list(part.members)} for part in cell.parts],
        "walls": [[row.square, row.wall, row.seated] for row in cell.walls],
        "contacts": [
            [row.left, row.right, row.owner, row.axis, row.positive] for row in cell.contacts
        ],
        "nonedges": [
            [row.left, row.right, row.owner, row.axis, row.positive] for row in cell.nonedges
        ],
    }


def _assert_label_document_matches(
    document: dict[str, object], cell: FullFixedAngleCell
) -> None:
    assert set(document) == {
        "contract",
        "angle_frame",
        "angles",
        "parts",
        "walls",
        "contacts",
        "nonedges",
    }
    assert document == _expected_label_document(cell)


def test_complete_literal_cell_has_joint_canonical_label_and_exact_price() -> None:
    cell = _l_cell()
    canonical = canonicalize_full_cell(cell)
    assert canonical.status == "canonical"
    assert canonical.raw_image_count == 8 * math.factorial(3) == 48
    assert canonical.unique_image_count == 48
    assert replay_full_cell_witness(cell, canonical.witness) == canonical.cell
    assert full_cell_label(canonical.cell) == canonical.canonical_label

    price = price_full_cell(cell, canonical)
    assert price.candidate_domains == {
        "partitions": 1,
        "angle_assignments": 1,
        "wall_seatings": 1,
        "nonedge_axis_assignments": 8,
        "raw_cells": 8,
    }
    assert price.executed_work == {
        "raw_cells_built": 1,
        "axis_order_branches_examined": 1,
        "orbit_images_examined": 48,
        "unique_orbit_images": canonical.unique_image_count,
        "duplicate_orbit_images": 48 - canonical.unique_image_count,
        "canonical_cells_emitted": 1,
        "lp_solves": 0,
    }
    assert price.inventory == {
        "squares": 3,
        "angle_values": 3,
        "wall_decisions": 12,
        "seated_walls": 4,
        "contact_pairs": 2,
        "nonedge_pairs": 1,
    }
    document = json.loads(canonical.canonical_label)
    _assert_label_document_matches(document, canonical.cell)
    assert price.evidence_role == (
        "target-free structural full-cell label and work price; no geometry, container fit, "
        "packing feasibility, or optimality claim"
    )
    forbidden = {"centres", "coordinates", "side", "container_fit", "feasible", "optimal"}
    assert forbidden.isdisjoint(json.dumps(document).lower().replace("-", "_").split('"'))


def test_full_cell_label_contract_refuses_an_omitted_channel() -> None:
    canonical = canonicalize_full_cell(_l_cell())
    assert canonical.status == "canonical"
    mutation = json.loads(canonical.canonical_label)
    del mutation["walls"]
    with pytest.raises(AssertionError):
        _assert_label_document_matches(mutation, canonical.cell)


def test_total_wall_and_pair_axis_inventories_refuse_omissions() -> None:
    cell = _l_cell()
    with pytest.raises(FullCellError, match="wall decision") as wall_error:
        replace(cell, walls=cell.walls[:-1])
    assert wall_error.value.kind == "full-cell-wall-inventory"

    with pytest.raises(FullCellError, match="pair partition") as axis_error:
        replace(cell, nonedges=())
    assert axis_error.value.kind == "full-cell-pair-inventory"

    with pytest.raises(FullCellError, match="pair partition") as duplicate_error:
        replace(cell, nonedges=(cell.nonedges[0], cell.nonedges[0]))
    assert duplicate_error.value.kind == "full-cell-pair-inventory"

    with pytest.raises(FullCellError, match="pair partition") as overlap_error:
        replace(cell, nonedges=(cell.contacts[0], cell.nonedges[0]))
    assert overlap_error.value.kind == "full-cell-pair-inventory"

    all_false_walls = tuple(replace(row, seated=False) for row in cell.walls)
    assert len(replace(cell, walls=all_false_walls).walls) == 12


@pytest.mark.parametrize("bad_id", [False, 0.0])
def test_square_identifiers_are_exact_non_boolean_integers(bad_id: object) -> None:
    invalid = cast(int, bad_id)
    with pytest.raises(FullCellError) as part_error:
        AssemblyPart("free", (invalid,))
    assert part_error.value.kind == "full-cell-partition"

    with pytest.raises(FullCellError) as wall_error:
        WallDecision(invalid, "left", seated=True)
    assert wall_error.value.kind == "full-cell-wall-inventory"

    with pytest.raises(FullCellError) as axis_error:
        OrientedPairAxis(invalid, 1, invalid, "u", 1)
    assert axis_error.value.kind == "full-cell-nonedge-axis-inventory"

    with pytest.raises(FullCellError) as positive_error:
        OrientedPairAxis(0, 1, 0, "u", invalid)
    assert positive_error.value.kind == "full-cell-nonedge-axis-inventory"


def test_part_kind_requires_a_nonempty_string() -> None:
    with pytest.raises(FullCellError) as error:
        AssemblyPart(cast(str, 7), (0,))
    assert error.value.kind == "full-cell-partition"


def test_axis_owner_tie_endpoint_order_and_d4_relabel_are_canonical() -> None:
    cell = _l_cell()
    # At equal angles, the two endpoint-owned copies name the same physical line.
    owner_tie = replace(
        cell,
        nonedges=(OrientedPairAxis(1, 2, 2, "u", 1),),
    )
    assert owner_tie == cell

    transformed = transform_full_cell(
        cell,
        symmetry=D4_BY_NAME["reflect-diagonal"],
        old_to_new=(0, 2, 1),
    )
    transformed_canonical = canonicalize_full_cell(transformed)
    source_canonical = canonicalize_full_cell(cell)
    assert transformed_canonical.status == "canonical"
    assert source_canonical.status == "canonical"
    assert transformed_canonical.canonical_label == source_canonical.canonical_label


@pytest.mark.parametrize(
    ("symmetry", "axis", "expected_axis", "expected_positive"),
    [
        ("identity", "u", "u", 1),
        ("identity", "v", "v", 1),
        ("rotate-90", "u", "v", 1),
        ("rotate-90", "v", "u", 2),
        ("rotate-180", "u", "u", 2),
        ("rotate-180", "v", "v", 2),
        ("rotate-270", "u", "v", 2),
        ("rotate-270", "v", "u", 1),
        ("reflect-x", "u", "u", 1),
        ("reflect-x", "v", "v", 2),
        ("reflect-y", "u", "u", 2),
        ("reflect-y", "v", "v", 1),
        ("reflect-diagonal", "u", "v", 1),
        ("reflect-diagonal", "v", "u", 1),
        ("reflect-antidiagonal", "u", "v", 2),
        ("reflect-antidiagonal", "v", "u", 2),
    ],
)
def test_exact_d4_axis_action_toggles_the_positive_endpoint(
    symmetry: str,
    axis: Axis,
    expected_axis: str,
    expected_positive: int,
) -> None:
    cell = replace(_l_cell(), nonedges=(_axis(1, 2, axis, 1),))
    transformed = transform_full_cell(
        cell,
        symmetry=D4_BY_NAME[symmetry],
        old_to_new=(0, 1, 2),
    )
    assert (transformed.nonedges[0].axis, transformed.nonedges[0].positive) == (
        expected_axis,
        expected_positive,
    )


def test_axis_action_maps_ids_before_reversing_sorted_endpoint_storage() -> None:
    cell = _l_cell()
    transformed = transform_full_cell(
        cell,
        symmetry=D4_BY_NAME["rotate-90"],
        old_to_new=(0, 2, 1),
    )
    # u has positive polarity under rotate-90; old positive 1 maps to new endpoint 2.
    assert transformed.nonedges[0] == OrientedPairAxis(1, 2, 1, "v", 2)


def test_every_full_orbit_image_canonicalizes_and_replays_jointly() -> None:
    cell = _l_cell()
    source = canonicalize_full_cell(cell)
    assert source.status == "canonical"
    for symmetry in D4_TRANSFORMS:
        for old_to_new in permutations(range(3)):
            image = transform_full_cell(
                cell,
                symmetry=symmetry,
                old_to_new=old_to_new,
            )
            result = canonicalize_full_cell(image)
            assert result.status == "canonical"
            assert result.canonical_label == source.canonical_label
            assert replay_full_cell_witness(image, result.witness) == result.cell
            assert len(result.cell.walls) == 12
            assert len(result.cell.contacts) + len(result.cell.nonedges) == 3


def test_orbit_cap_returns_typed_partial_receipt_without_completed_price() -> None:
    cell = _l_cell()
    limited = canonicalize_full_cell(cell, limits=FullCellLimits(maximum_orbit_images=47))
    assert limited.status == "limit"
    assert limited.kind == "orbit-image-cap"
    assert limited.limit == 47
    assert limited.required_images == 48
    assert limited.examined_images == 47
    with pytest.raises(FullCellError, match="completed canonical cell") as error:
        price_full_cell(cell, limited)
    assert error.value.kind == "full-cell-price-prerequisite"
    completed = canonicalize_full_cell(cell, limits=FullCellLimits(maximum_orbit_images=48))
    assert completed.status == "canonical"


def test_price_refuses_a_canonical_receipt_from_another_cell() -> None:
    cell = _l_cell()
    other_walls = (replace(cell.walls[0], seated=False), *cell.walls[1:])
    other = replace(cell, walls=other_walls)
    other_canonical = canonicalize_full_cell(other)
    assert other_canonical.status == "canonical"
    with pytest.raises(FullCellError, match="does not replay") as error:
        price_full_cell(cell, other_canonical)
    assert error.value.kind == "full-cell-price-prerequisite"

    source_canonical = canonicalize_full_cell(cell)
    assert source_canonical.status == "canonical"
    forged = replace(
        source_canonical,
        unique_image_count=source_canonical.unique_image_count - 1,
    )
    with pytest.raises(FullCellError, match="does not replay"):
        price_full_cell(cell, forged)


def test_full_cell_module_has_no_calibration_or_geometry_reader() -> None:
    source = inspect.getsource(full_cell_module)
    for forbidden in ("known_best", "atlas/", "Path(", "contact_realization", "solve_cell"):
        assert forbidden not in source
    with patch("builtins.open", side_effect=AssertionError("unexpected file read")):
        cell = _l_cell()
        canonical = canonicalize_full_cell(cell)
        assert canonical.status == "canonical"
        price_full_cell(cell, canonical)
