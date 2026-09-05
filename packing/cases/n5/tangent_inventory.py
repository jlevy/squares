#!/usr/bin/env python3
"""Exact, first-order inventory for the six n=5 fixed-side active cones.

This deliberately stops at the linearized cone.  In particular neither ``-W`` nor a
nonlinear continuation of a transverse ray is a conclusion of this module.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
import time
from collections.abc import Callable, Iterable
from pathlib import Path

from strif import atomic_output_file

from cases.n5 import angle_sheet, second_order_obstruction
from cases.n5 import equal_side_face as face
from cases.n5 import tangent_cones as source
from sqpack.field import FieldElement, NumberField

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = 1
RESULTS = ROOT / "campaign/series/series-000-smoke-and-calibration/results"
EXP034 = RESULTS / "exp-034-h-023-n5-angle-sheet.json"
EXP035 = RESULTS / "exp-035-h-023-n5-tangent-cones.json"
EXP036 = RESULTS / "exp-036-h-023-n5-second-order-obstruction.json"
STRATA = ("A", "interior", "B")
OWNERS = ("owner3:a+", "owner4:a+")
SLACK_RELATION = "X- + Y+ = X+ + Y-"
RAY_SUPPORTS = {
    "R1": {"contact:1-4:owner4:a-"},
    "R2": {"contact:0-4:owner4:a-"},
    "R3": {"wall:1:y-lower:-", "wall:1:y-lower:+"},
    "R4": {"wall:1:x-upper:-", "wall:1:y-lower:-"},
    "R5": {"wall:1:x-upper:+", "wall:1:y-lower:+"},
    "R6": {"wall:1:x-upper:-", "wall:1:x-upper:+"},
}
VARIABLES = (
    [f"dx{i}" for i in range(5)]
    + [f"dy{i}" for i in range(5)]
    + [f"dtheta{i}" for i in range(5)]
)


def rank(rows: Iterable[source.LinearRow]) -> int:
    return source.exact_rank(tuple(rows))


def coefficient_rank(vectors: list[list[FieldElement]]) -> int:
    """Return the exact row rank for vectors of any common finite length."""
    if not vectors:
        return 0
    work = [list(vector) for vector in vectors]
    width = len(work[0])
    if any(len(vector) != width for vector in work):
        raise ValueError("rank vectors have unequal lengths")
    result = 0
    for column in range(width):
        pivot = next(
            (row for row in range(result, len(work)) if not work[row][column].is_zero()),
            None,
        )
        if pivot is None:
            continue
        work[result], work[pivot] = work[pivot], work[result]
        inverse = work[result][column].inverse()
        work[result] = [value * inverse for value in work[result]]
        for row_index in range(len(work)):
            if row_index == result:
                continue
            factor = work[row_index][column]
            if factor.is_zero():
                continue
            work[row_index] = [
                left - factor * right
                for left, right in zip(work[row_index], work[result], strict=True)
            ]
        result += 1
    return result


def exact_vector(field: NumberField, values: dict[int, FieldElement]) -> list[FieldElement]:
    vector = source.zero_row(field)
    for index, value in values.items():
        vector[index] = value
    return vector


def add_vectors(
    field: NumberField,
    *vectors: list[FieldElement],
    scales: tuple[FieldElement, ...] | None = None,
) -> list[FieldElement]:
    factors = scales or tuple(field.one for _ in vectors)
    if len(factors) != len(vectors):
        raise ValueError("vector and scale counts differ")
    return [
        sum(
            (factor * vector[index] for factor, vector in zip(factors, vectors, strict=True)),
            field.zero,
        )
        for index in range(source.VARIABLE_COUNT)
    ]


def encode_vector(vector: list[FieldElement]) -> dict[str, object]:
    return {
        "variables": VARIABLES,
        "coordinates_low_degree_first": [source.encode(value) for value in vector],
    }


def matrix(field: NumberField, stratum: str, owner: str) -> tuple[source.LinearRow, ...]:
    fixed, branches = source.contact_rows(field, source.centres_for_stratum(field, stratum))
    return (*source.wall_rows(field, stratum), *fixed, *branches[owner])


def rref_nullity(rows: tuple[source.LinearRow, ...]) -> int:
    """Exact equality lineality dimension (the kernel of the active matrix)."""
    return source.VARIABLE_COUNT - rank(rows)


def left_kernel(
    rows: tuple[source.LinearRow, ...], field: NumberField
) -> list[list[FieldElement]]:
    """Return an exact basis of {c : c A = 0}, by RREF of A transpose."""
    work = [[item.coefficients[i] for item in rows] for i in range(source.VARIABLE_COUNT)]
    pivots: list[int] = []
    pivot_row = 0
    for column in range(len(rows)):
        pivot = next(
            (i for i in range(pivot_row, len(work)) if not work[i][column].is_zero()), None
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        inverse = work[pivot_row][column].inverse()
        work[pivot_row] = [value * inverse for value in work[pivot_row]]
        for candidate in range(len(work)):
            if candidate != pivot_row and not work[candidate][column].is_zero():
                factor = work[candidate][column]
                work[candidate] = [
                    left - factor * right
                    for left, right in zip(work[candidate], work[pivot_row], strict=True)
                ]
        pivots.append(column)
        pivot_row += 1
    free = [column for column in range(len(rows)) if column not in pivots]
    basis: list[list[FieldElement]] = []
    for column in free:
        vector = [field.zero for _ in rows]
        vector[column] = field.one
        for row_index, pivot_column in enumerate(pivots):
            vector[pivot_column] = -work[row_index][column]
        basis.append(vector)
    return basis


def check_relation(
    rows: tuple[source.LinearRow, ...], weights: list[FieldElement], field: NumberField
) -> None:
    if any(
        not value.is_zero()
        for value in (
            sum(
                (
                    weight * row.coefficients[i]
                    for weight, row in zip(weights, rows, strict=True)
                ),
                field.zero,
            )
            for i in range(source.VARIABLE_COUNT)
        )
    ):
        raise ValueError("advertised left-kernel relation is not exact")


def certificate(rows: tuple[source.LinearRow, ...], field: NumberField) -> dict[str, object]:
    basis = left_kernel(rows, field)
    if len(basis) != len(rows) - rank(rows) or len(basis) != 3:
        raise ValueError("left-kernel dimension is not exactly three")
    square1 = [i for i, row in enumerate(rows) if row.label.startswith("wall:1:")]
    square2 = [i for i, row in enumerate(rows) if row.label.startswith("wall:2:")]
    survivor = next(
        (v for v in basis if {i for i, x in enumerate(v) if not x.is_zero()} == set(square1)),
        None,
    )
    balance = next(
        (v for v in basis if {i for i, x in enumerate(v) if not x.is_zero()} == set(square2)),
        None,
    )
    core = next(
        (
            v
            for v in basis
            if any(
                rows[i].label.startswith("contact:3-4:") and not x.is_zero()
                for i, x in enumerate(v)
            )
        ),
        None,
    )
    if survivor is None or balance is None or core is None:
        raise ValueError("could not identify exact slack and positive certificates")
    if survivor[square1[0]].sign() < 0:
        survivor = [-value for value in survivor]
    if balance[square2[0]].sign() < 0:
        balance = [-value for value in balance]
    # The core relation is positive except that the two missing square-2 slacks are
    # supplied by adding/subtracting half of the surviving relation.
    if any(value.sign() < 0 for value in core if not value.is_zero()):
        core = [-value for value in core]
    # Two distinct positive identities are enough to force the entire nine-slack
    # support; both are exact combinations of the core identity and the survivor.
    positive = [
        [a + field.rational(1) / 4 * b for a, b in zip(core, balance, strict=True)],
        [a + field.rational(1) / 2 * b for a, b in zip(core, balance, strict=True)],
    ]
    for weights in (*positive, balance, survivor):
        check_relation(rows, weights, field)
    if any(
        value.sign() <= 0 for weights in positive for value in weights if not value.is_zero()
    ):
        raise ValueError("positive left-kernel certificate lost positivity")
    forced = {
        rows[i].label
        for weights in positive
        for i, value in enumerate(weights)
        if not value.is_zero()
    }
    expected_forced = {
        "wall:2:x-lower:+",
        "wall:2:x-lower:-",
        "wall:2:y-lower:+",
        "wall:2:y-lower:-",
        "wall:3:x-upper",
        "wall:3:y-upper",
        "contact:2-4:owner4:a+",
        *(row.label for row in rows if row.label.startswith("contact:3-4:")),
    }
    if forced != expected_forced or len(forced) != 9:
        raise ValueError("positive certificate does not force exactly nine slacks")
    if coefficient_rank([*positive, survivor]) != 3:
        raise ValueError("the advertised relations do not exhaust the left kernel")
    survivor_by_label = {rows[i].label: value for i, value in enumerate(survivor)}
    expected_survivor = {
        "wall:1:x-upper:+": field.one,
        "wall:1:x-upper:-": -field.one,
        "wall:1:y-lower:+": -field.one,
        "wall:1:y-lower:-": field.one,
    }
    if {
        label: value for label, value in survivor_by_label.items() if not value.is_zero()
    } != expected_survivor:
        raise ValueError("the named square-1 slack balance drifted")

    def encode(weights: list[FieldElement]) -> dict[str, list[str]]:
        return {
            rows[i].label: source.encode(value)
            for i, value in enumerate(weights)
            if not value.is_zero()
        }

    return {
        "left_kernel_dimension": 3,
        "certificate_rank": 3,
        "left_kernel_exhausted": True,
        "positive_identities": [encode(x) for x in positive],
        "surviving_relation": encode(survivor),
        "forced_zero_slacks": sorted(forced),
    }


def cone_face_vectors() -> dict[str, object]:
    # R_+^2 times the cone over a quadrilateral.  Its f-vector is the convolution
    # of (1,2,1) with the quadrilateral-cone f-vector (1,4,4,1).
    orthant = (1, 2, 1)
    quad = (1, 4, 4, 1)
    transverse = tuple(
        sum(orthant[i] * quad[k - i] for i in range(len(orthant)) if 0 <= k - i < len(quad))
        for k in range(6)
    )
    endpoint = tuple(
        sum(
            transverse[i] * orthant[k - i]
            for i in range(len(transverse))
            if 0 <= k - i < len(orthant)
        )
        for k in range(8)
    )
    if transverse != (1, 6, 13, 13, 6, 1):
        raise ValueError("derived transverse face vector drifted")
    if endpoint != (1, 8, 26, 45, 45, 26, 8, 1):
        raise ValueError("derived endpoint face vector drifted")
    return {
        "convention": (
            "entry k counts k-dimensional faces of the pointed quotient by lineality, "
            "including its apex and whole quotient and excluding the empty face"
        ),
        "transverse_dimensions_0_through_5": list(transverse),
        "endpoint_dimensions_0_through_7": list(endpoint),
    }


def geometry_vectors(
    field: NumberField, stratum: str
) -> tuple[
    dict[str, list[FieldElement]],
    dict[str, list[FieldElement]],
    dict[str, list[FieldElement]],
    str,
]:
    """Return exact lineality, sheet, and transverse vectors for one stratum."""
    q = field.rational
    r = field.alpha
    delta = 3 * r / 2 - 2
    slide = exact_vector(field, {source.x(0): q(1), source.y(0): q(1)})
    angle = exact_vector(field, {source.theta(0): q(1)})
    common = exact_vector(
        field,
        {
            source.x(4): delta / 2,
            source.theta(3): q(1),
            source.theta(4): q(1),
        },
    )
    if stratum == "A":
        common[source.y(0)] = -delta
    elif stratum == "B":
        common[source.x(0)] = -delta
    elif stratum != "interior":
        raise ValueError(f"unknown stratum {stratum}")
    if common != source.witness(field, stratum):
        raise ValueError("the W normalization no longer matches exp-035")

    base = {
        "R1": exact_vector(
            field,
            {
                source.x(0): -r,
                source.x(4): -r / 2,
                source.y(4): r / 2,
            },
        ),
        "R2": exact_vector(field, {source.x(0): -r}),
        "R3": exact_vector(
            field,
            {
                source.x(0): -q(1),
                source.x(4): -q(1) / 2,
                source.y(1): q(1),
                source.y(4): q(1) / 2,
            },
        ),
        "R4": exact_vector(
            field,
            {
                source.x(0): -q(1),
                source.x(1): -q(1) / 2,
                source.x(4): -q(1) / 2,
                source.y(1): q(1) / 2,
                source.y(4): q(1) / 2,
                source.theta(1): -q(1),
            },
        ),
        "R5": exact_vector(
            field,
            {
                source.x(0): -q(1),
                source.x(1): -q(1) / 2,
                source.x(4): -q(1) / 2,
                source.y(1): q(1) / 2,
                source.y(4): q(1) / 2,
                source.theta(1): q(1),
            },
        ),
        "R6": exact_vector(
            field,
            {
                source.x(0): -q(1),
                source.x(1): -q(1),
                source.x(4): -q(1) / 2,
                source.y(4): q(1) / 2,
            },
        ),
    }
    if stratum == "A":
        base["R1"] = add_vectors(field, base["R1"], slide, scales=(q(1), r))
        base["R2"] = add_vectors(field, base["R2"], slide, scales=(q(1), r))
        for name in ("R3", "R4", "R5", "R6"):
            base[name] = add_vectors(field, base[name], slide)

    if stratum == "interior":
        lineality = {"sheet_slide": slide, "sheet_angle": angle, "W": common}
        sheet = {"sheet_slide": slide, "sheet_angle": angle}
        sheet_kind = "lineality_space"
    else:
        sign = q(1) if stratum == "A" else -q(1)
        sheet = {
            "sheet_angle_negative": exact_vector(
                field,
                {
                    source.x(0): sign / 2,
                    source.y(0): sign / 2,
                    source.theta(0): -q(1),
                },
            ),
            "sheet_angle_positive": exact_vector(
                field,
                {
                    source.x(0): sign / 2,
                    source.y(0): sign / 2,
                    source.theta(0): q(1),
                },
            ),
        }
        lineality = {"W": common}
        sheet_kind = "pointed_cone"
    return lineality, sheet, base, sheet_kind


def ray_record(
    rows: tuple[source.LinearRow, ...],
    vector: list[FieldElement],
    field: NumberField,
    *,
    expected_support: set[str],
) -> dict[str, object]:
    residuals = [source.exact_dot(item, vector, field) for item in rows]
    if any(value.sign() < 0 for value in residuals):
        raise ValueError("an advertised generator violates an exact active row")
    positive = {
        item.label for item, value in zip(rows, residuals, strict=True) if value.sign() > 0
    }
    if positive != expected_support:
        raise ValueError(f"generator support drifted: {sorted(positive)}")
    tight = tuple(item for item, value in zip(rows, residuals, strict=True) if value.is_zero())
    active_rank = rank(tight)
    if active_rank != rank(rows) - 1:
        raise ValueError("an advertised pointed ray lacks codimension-one active rank")
    return {
        **encode_vector(vector),
        "positive_slacks": {
            item.label: source.encode(value)
            for item, value in zip(rows, residuals, strict=True)
            if value.sign() > 0
        },
        "tight_active_rank": active_rank,
    }


def validate_sources() -> dict[str, str]:
    """Regenerate and compare every exact predecessor used by this result."""
    retained_034 = angle_sheet.require_dict(
        json.loads(EXP034.read_text(encoding="utf-8")), "exp-034"
    )
    angle_sheet.require_same_result(retained_034, angle_sheet.build_result())
    retained_035 = source.require_dict(
        json.loads(EXP035.read_text(encoding="utf-8")), "exp-035"
    )
    source.require_same_result(retained_035, source.build_result())
    retained_036 = second_order_obstruction.require_dict(
        json.loads(EXP036.read_text(encoding="utf-8")), "exp-036"
    )
    second_order_obstruction.require_same_result(
        retained_036, second_order_obstruction.build_result()
    )
    return {
        "exp_034": str(EXP034.relative_to(ROOT)),
        "exp_035": str(EXP035.relative_to(ROOT)),
        "exp_036": str(EXP036.relative_to(ROOT)),
    }


def build_result() -> dict[str, object]:
    field = face.make_field()
    source.geometry_inventory(field)  # exact geometry drift check before matrix assembly
    records: list[dict[str, object]] = []
    owner_v_representations: list[dict[str, object]] = []
    for stratum in STRATA:
        lineality, sheet_vectors, transverse_vectors, sheet_kind = geometry_vectors(
            field, stratum
        )
        expected_nullity = 3 if stratum == "interior" else 1
        if coefficient_rank(list(lineality.values())) != expected_nullity:
            raise ValueError("the declared lineality basis is dependent or incomplete")
        relation = add_vectors(
            field,
            transverse_vectors["R3"],
            transverse_vectors["R6"],
            transverse_vectors["R4"],
            transverse_vectors["R5"],
            scales=(field.one, field.one, -field.one, -field.one),
        )
        if any(not value.is_zero() for value in relation):
            raise ValueError("the sole transverse generator relation drifted")
        if coefficient_rank(list(transverse_vectors.values())) != 5:
            raise ValueError("the transverse generators have another linear relation")
        if (
            stratum != "interior"
            and coefficient_rank([*transverse_vectors.values(), *sheet_vectors.values()]) != 7
        ):
            raise ValueError("the endpoint pointed quotient does not have dimension seven")
        stratum_records: list[dict[str, object]] = []
        for owner in OWNERS:
            rows = matrix(field, stratum, owner)
            row_labels = [item.label for item in rows]
            # The tied 3--4 rows have owner-specific names; their common forced role is
            # retained separately so that the certificate does not confuse a conjunction
            # with a branch alternative.
            if sum(label.startswith("contact:3-4:") for label in row_labels) != 2:
                raise ValueError("owner branch lost a tied support row")
            matrix_rank = rank(rows)
            if matrix_rank != (12 if stratum == "interior" else 14):
                raise ValueError("source branch rank drifted")
            if rref_nullity(rows) != expected_nullity:
                raise ValueError("source branch lineality drifted")
            for vector in lineality.values():
                if any(not source.exact_dot(item, vector, field).is_zero() for item in rows):
                    raise ValueError("a declared lineality vector left an active row")

            transverse_records = {
                name: ray_record(
                    rows,
                    vector,
                    field,
                    expected_support=RAY_SUPPORTS[name],
                )
                for name, vector in transverse_vectors.items()
            }
            if stratum == "interior":
                for vector in sheet_vectors.values():
                    if any(
                        not source.exact_dot(item, vector, field).is_zero() for item in rows
                    ):
                        raise ValueError("the interior sheet is not active-row lineality")
                sheet_record: dict[str, object] = {
                    "kind": sheet_kind,
                    "basis": {
                        name: encode_vector(vector) for name, vector in sheet_vectors.items()
                    },
                }
                sheet_supports: set[str] = set()
            else:
                wall = "x-lower" if stratum == "A" else "y-upper"
                sheet_record = {
                    "kind": sheet_kind,
                    "rays": {
                        name: ray_record(
                            rows,
                            vector,
                            field,
                            expected_support={
                                f"wall:0:{wall}:{'-' if name.endswith('negative') else '+'}"
                            },
                        )
                        for name, vector in sheet_vectors.items()
                    },
                }
                sheet_supports = {f"wall:0:{wall}:-", f"wall:0:{wall}:+"}
            certificate_record = certificate(rows, field)
            forced_value = certificate_record["forced_zero_slacks"]
            if not isinstance(forced_value, list):
                raise TypeError("forced-zero slack inventory is malformed")
            forced_labels = set(forced_value)
            surviving_labels = set().union(*RAY_SUPPORTS.values(), sheet_supports)
            if set(row_labels) - forced_labels != surviving_labels:
                raise ValueError("the physical generators do not exhaust surviving slacks")
            record = {
                "stratum": stratum,
                "owner": owner,
                "row_count": len(rows),
                "rank": matrix_rank,
                "lineality_dimension": expected_nullity,
                "rows": row_labels,
                "positive_left_kernel_certificate": certificate_record,
                "lineality_basis": {
                    name: encode_vector(vector) for name, vector in lineality.items()
                },
                "sheet": sheet_record,
                "transverse_rays": transverse_records,
                "pointed_quotient_ray_count": 6 + (2 if stratum != "interior" else 0),
            }
            records.append(record)
            stratum_records.append(record)
        first_signature = {
            "lineality_basis": stratum_records[0]["lineality_basis"],
            "sheet": stratum_records[0]["sheet"],
            "transverse_rays": stratum_records[0]["transverse_rays"],
        }
        second_signature = {
            "lineality_basis": stratum_records[1]["lineality_basis"],
            "sheet": stratum_records[1]["sheet"],
            "transverse_rays": stratum_records[1]["transverse_rays"],
        }
        if first_signature != second_signature:
            raise ValueError("owner branches do not have one exact V-representation")
        owner_v_representations.append(
            {
                "stratum": stratum,
                "owner3_equals_owner4": True,
                "proof": (
                    "both exact matrices have the displayed complete left-kernel "
                    "factorization, lineality basis, sheet data, and physical generators"
                ),
                "pointed_quotient_ray_count": 6 + (2 if stratum != "interior" else 0),
            }
        )
    # The six matrices are source-derived and exact.  The quotient inventory is invariant
    # under the owner choice; endpoint sheet rays are not quotient symmetries.
    result: dict[str, object] = {
        "schema_version": SCHEMA_VERSION,
        "contract": "packing.squares:N5TangentInventory/v1",
        "source": {
            "builders": "cases/n5/tangent_cones.py",
            "field": "Q(sqrt(2))",
            **validate_sources(),
        },
        "six_matrices": records,
        "transverse_cone": {
            "slack_relation": SLACK_RELATION,
            "ray_names": list(RAY_SUPPORTS),
            "sole_relation": "R3 + R6 = R4 + R5",
            "structure": "R_+^2 times the cone over a quadrilateral",
        },
        "face_vectors": cone_face_vectors(),
        "owner_branch_v_representations": owner_v_representations,
        "scope_refusals": {
            "plus_W_excluded_by_exp_036": True,
            "minus_W_covered": False,
            "nonlinear_transverse_lift_continued": False,
            "statement": (
                "-W and every transverse or mixed-direction nonlinear lift remain "
                "unresolved; exp-034 supplies the declared sheet lifts"
            ),
        },
        "determination": {
            "outcome": "criterion_met",
            "claim": (
                "the six exact branchwise linearization cones have the retained complete "
                "V-representations and both owner branches coincide at first order"
            ),
            "scope": (
                "first-order branchwise linearizations only; transverse and mixed "
                "Bouligand status, terminal membership, component identity, basin mass, "
                "and unequal-side clearance remain unresolved; exp-034 separately "
                "supplies its declared sheet lifts"
            ),
        },
    }
    validate_result(result)
    controls = controls_for(result)
    result["controls"] = controls
    if len(controls) != 10 or not all(controls.values()):
        raise ValueError("a preregistered control failed")
    return result


def validate_result(result: dict[str, object]) -> None:
    matrices = result.get("six_matrices")
    if not isinstance(matrices, list) or len(matrices) != 6:
        raise ValueError("missing or duplicated owner matrix record")
    owners = {
        (item.get("stratum"), item.get("owner")) for item in matrices if isinstance(item, dict)
    }
    if owners != {(stratum, owner) for stratum in STRATA for owner in OWNERS}:
        raise ValueError("owner matrix identities drifted")
    for item in matrices:
        if not isinstance(item, dict):
            raise TypeError("a matrix record is malformed")
        stratum = item.get("stratum")
        expected_lineality = (
            {"sheet_slide", "sheet_angle", "W"} if stratum == "interior" else {"W"}
        )
        lineality = item.get("lineality_basis")
        if not isinstance(lineality, dict) or set(lineality) != expected_lineality:
            raise ValueError("a lineality basis is incomplete")
        rays = item.get("transverse_rays")
        if not isinstance(rays, dict) or set(rays) != set(RAY_SUPPORTS):
            raise ValueError("a transverse generator is missing or mislabeled")
        for name, ray in rays.items():
            if (
                not isinstance(ray, dict)
                or set(ray.get("positive_slacks", {})) != RAY_SUPPORTS[name]
            ):
                raise ValueError("a transverse generator support is mislabeled")
        sheet = item.get("sheet")
        if not isinstance(sheet, dict):
            raise TypeError("sheet data is missing")
        if stratum == "interior":
            if sheet.get("kind") != "lineality_space" or set(sheet.get("basis", {})) != {
                "sheet_slide",
                "sheet_angle",
            }:
                raise ValueError("interior sheet classification drifted")
            expected_ray_count = 6
        else:
            sheet_rays = sheet.get("rays", {})
            if sheet.get("kind") != "pointed_cone" or set(sheet_rays) != {
                "sheet_angle_negative",
                "sheet_angle_positive",
            }:
                raise ValueError("endpoint sheet classification drifted")
            wall = "x-lower" if stratum == "A" else "y-upper"
            for name, ray in sheet_rays.items():
                if not isinstance(ray, dict) or set(ray.get("positive_slacks", {})) != {
                    f"wall:0:{wall}:{'-' if name.endswith('negative') else '+'}"
                }:
                    raise ValueError("endpoint sheet ray support drifted")
            expected_ray_count = 8
        if item.get("pointed_quotient_ray_count") != expected_ray_count:
            raise ValueError("pointed quotient ray count drifted")
        certificate_value = item.get("positive_left_kernel_certificate")
        if not isinstance(certificate_value, dict):
            raise TypeError("left-kernel certificate is missing")
        if (
            certificate_value.get("left_kernel_dimension") != 3
            or certificate_value.get("certificate_rank") != 3
            or certificate_value.get("left_kernel_exhausted") is not True
            or len(certificate_value.get("forced_zero_slacks", [])) != 9
        ):
            raise ValueError("left-kernel certificate is incomplete")
    cone = result.get("transverse_cone")
    if not isinstance(cone, dict) or cone.get("ray_names") != list(RAY_SUPPORTS):
        raise ValueError("a transverse ray was dropped or changed")
    if cone.get("sole_relation") != "R3 + R6 = R4 + R5":
        raise ValueError("transverse sole relation drifted")
    if result.get("face_vectors") != cone_face_vectors():
        raise ValueError("pointed quotient face vectors drifted")
    branch_records = result.get("owner_branch_v_representations")
    if (
        not isinstance(branch_records, list)
        or len(branch_records) != 3
        or any(
            not isinstance(item, dict) or item.get("owner3_equals_owner4") is not True
            for item in branch_records
        )
    ):
        raise ValueError("owner-branch equality record drifted")
    scope = result.get("scope_refusals")
    if (
        not isinstance(scope, dict)
        or scope.get("plus_W_excluded_by_exp_036") is not True
        or scope.get("minus_W_covered")
        or scope.get("nonlinear_transverse_lift_continued")
    ):
        raise ValueError("first-order inventory overclaims scope")
    determination = result.get("determination")
    if not isinstance(determination, dict) or determination.get("outcome") != "criterion_met":
        raise ValueError("the exact first-order criterion was not met")


def controls_for(result: dict[str, object]) -> dict[str, bool]:
    field = face.make_field()

    def rejected(mutator: Callable[[dict[str, object]], None]) -> bool:
        trial = copy.deepcopy(result)
        mutator(trial)
        try:
            validate_result(trial)
        except ValueError:
            return True
        return False

    def claim_minus_w(trial: dict[str, object]) -> None:
        scope = trial["scope_refusals"]
        assert isinstance(scope, dict)
        scope["minus_W_covered"] = True

    def claim_lift(trial: dict[str, object]) -> None:
        scope = trial["scope_refusals"]
        assert isinstance(scope, dict)
        scope["nonlinear_transverse_lift_continued"] = True

    rigid_axis = exact_vector(field, {source.x(0): field.one})
    rigid_rows = (
        source.LinearRow("positive", tuple(rigid_axis)),
        source.LinearRow("negative", tuple(-value for value in rigid_axis)),
    )
    rigid_weights = [field.one, field.one]
    check_relation(rigid_rows, rigid_weights, field)
    negative_rigid_axis = [-value for value in rigid_axis]
    rigid_ok = (
        rank(rigid_rows) == 1
        and source.exact_dot(rigid_rows[1], rigid_axis, field).sign() < 0
        and source.exact_dot(rigid_rows[0], negative_rigid_axis, field).sign() < 0
    )

    orthant_rows = (
        source.LinearRow("x", tuple(rigid_axis)),
        source.LinearRow("y", tuple(exact_vector(field, {source.y(0): field.one}))),
    )
    orthant_ok = all(
        ray_record(orthant_rows, vector, field, expected_support={label})
        for label, vector in (
            ("x", rigid_axis),
            ("y", exact_vector(field, {source.y(0): field.one})),
        )
    )
    lineality_vector = exact_vector(field, {source.y(0): field.one})
    lineality_rows = (source.LinearRow("x", tuple(rigid_axis)),)
    lineality_ok = (
        source.exact_dot(lineality_rows[0], lineality_vector, field).is_zero()
        and not source.exact_dot(lineality_rows[0], rigid_axis, field).is_zero()
        and coefficient_rank([rigid_axis, lineality_vector]) == 2
        and bool(
            ray_record(
                lineality_rows,
                rigid_axis,
                field,
                expected_support={"x"},
            )
        )
    )

    def first_matrix(trial: dict[str, object]) -> dict[str, object]:
        matrices = trial["six_matrices"]
        assert isinstance(matrices, list)
        assert isinstance(matrices[0], dict)
        return matrices[0]

    def sheet_as_transverse(trial: dict[str, object]) -> None:
        first = first_matrix(trial)
        transverse = first["transverse_rays"]
        sheet = first["sheet"]
        assert isinstance(transverse, dict)
        assert isinstance(sheet, dict)
        sheet_rays = sheet["rays"]
        assert isinstance(sheet_rays, dict)
        transverse["R1"] = sheet_rays["sheet_angle_negative"]

    def transverse_as_sheet(trial: dict[str, object]) -> None:
        first = first_matrix(trial)
        transverse = first["transverse_rays"]
        sheet = first["sheet"]
        assert isinstance(transverse, dict)
        assert isinstance(sheet, dict)
        sheet_rays = sheet["rays"]
        assert isinstance(sheet_rays, dict)
        sheet_rays["sheet_angle_negative"] = transverse["R1"]

    def missing_owner(trial: dict[str, object]) -> None:
        matrices = trial["six_matrices"]
        assert isinstance(matrices, list)
        matrices.pop()

    def duplicate_owner(trial: dict[str, object]) -> None:
        matrices = trial["six_matrices"]
        assert isinstance(matrices, list)
        matrices.append(matrices[0])

    def drop_ray(trial: dict[str, object]) -> None:
        cone = trial["transverse_cone"]
        assert isinstance(cone, dict)
        ray_names = cone["ray_names"]
        assert isinstance(ray_names, list)
        ray_names.pop()

    return {
        "rigid_cone_has_no_pointed_ray": rigid_ok,
        "orthant_has_declared_rays": orthant_ok,
        "lineality_separates_from_pointed_generator": lineality_ok,
        "missing_owner_record_rejected": rejected(missing_owner),
        "duplicated_owner_record_rejected": rejected(duplicate_owner),
        "dropped_transverse_generator_rejected": rejected(drop_ray),
        "sheet_as_transverse_rejected": rejected(sheet_as_transverse),
        "transverse_as_sheet_rejected": rejected(transverse_as_sheet),
        "minus_W_claim_rejected": rejected(claim_minus_w),
        "nonlinear_lift_claim_rejected": rejected(claim_lift),
    }


def write_json_atomic(path: Path, result: dict[str, object]) -> None:
    with atomic_output_file(path, make_parents=True) as temporary:
        temporary.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )


def require_same(retained: object, regenerated: dict[str, object]) -> None:
    if retained != regenerated:
        raise ValueError("retained record differs from exact regeneration")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--record", type=Path)
    mode.add_argument("--replay", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    try:
        result = build_result()
        if args.record:
            write_json_atomic(args.record, result)
        else:
            retained = json.loads(args.replay.read_text(encoding="utf-8"))
            require_same(retained, result)
        print(
            json.dumps(
                {
                    "record_written": bool(args.record),
                    "record_replayed": bool(args.replay),
                    "matrix_count": 6,
                    "controls": result["controls"],
                    "elapsed_seconds": round(time.monotonic() - started, 6),
                },
                sort_keys=True,
            )
        )
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
