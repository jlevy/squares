#!/usr/bin/env python3
"""The first-order growth cone at Trump's n = 11 pose and the capture radius it certifies.

H-237 (X-046 candidate H-d) asks whether the exact first-order growth function

    g_b(d) = min { sigma : A_b d + sigma e >= 0 },   e = indicator of the far-wall rows,

minimised over the 128 derivative-distinct branches of exp-013 and over the whole
sup-norm sphere, combined with the BC-199 per-row remainder bounds
``|R_j(v)| <= (K_j/2) ||v||_inf^2``, certifies side > U on a ball larger than
``rho_row = 808514697/200000000000``.  This module computes ``g`` exactly on all 66 faces
of every branch (floats propose, an exact far-normalised dual certifies a lower bound, an
exact vertex pins the minimum), reproduces the BC-199 weighted modulus on the same faces
as a control, and evaluates face by face the radius the growth route can certify.

What caps the route is a lemma, not a computation, and the tool checks its consequence
on every face rather than assuming it:

    Exhaustion lemma.  Fix a branch b, a direction d with ||d||_inf = 1 and a scale t > 0.
    The system { a_j.(t d) + sigma e_j + r_j >= 0 for all j, |r_j| <= (K_j/2) t^2,
    sigma <= 0 } has a solution iff a_j.d + (K_j/2) t >= 0 for every row j, that is iff
    t >= t_b(d) := max_j -(2/K_j) a_j.d.

    Proof.  If t >= t_b(d), take sigma = 0 and r_j = (K_j/2) t^2.  Conversely
    sigma e_j <= 0 and r_j <= (K_j/2) t^2 give a_j.(t d) + (K_j/2) t^2 >= 0 row by row.

Every certificate that uses only the branch rows with remainders bounded per row is
therefore exhausted at ``min_b min_d t_b(d)``, the BC-199 weighted modulus, which is
where ``rho_row`` comes from.  In LP terms: a multiplier vector ``mu >= 0`` on the rows
certifies side > U (or infeasibility) on a face up to radius ``2 beta(mu) / (mu^T K)``
with ``beta(mu) = -s w_k - sum_{i != k} |w_i|``, ``w = A_b^T mu``; the growth dual is this
family under the normalisation ``sum_far mu = 1``, and maximising the radius over the
whole family is exactly the weighted-modulus LP under the normalisation
``sum_j mu_j K_j / 2 = 1``.  The growth cone is the same LP with a worse normalisation.

Floats propose, exact arithmetic in Q(u) decides.  Nothing retained rests on a float.
"""

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from cases.trump11 import isolation_radius as ir
from cases.trump11 import tangent_cones as tc
from sqpack.exact_lp import LinearRow
from sqpack.field import FieldElement, NumberField
from sqpack.research.exact_jets import SecondOrderJet
from sqpack.verify import edge_axes

VARIABLES = tc.EXPECTED_VARIABLES
FACES = 2 * VARIABLES
ANGLE_COORDINATES = tuple(3 * index + 2 for index in range(tc.EXPECTED_SQUARES))
ANGLE_FACES = tuple((coordinate, sign) for coordinate in ANGLE_COORDINATES for sign in (-1, 1))
ALL_FACES = tuple((coordinate, sign) for coordinate in range(VARIABLES) for sign in (-1, 1))

# BC-240's preferred radius and the BC-199 branch-0 decimals it rests on.  The weighted
# pass below must reproduce the second exactly; the first is the H-237 threshold.
RHO_ROW = Fraction(808514697, 200000000000)
RHO_ROW_DECIMAL = "0.00404257348533135396598905037166"
KAPPA_0_DECIMAL = "0.0114802720615064442376926526944"

CLAIM_BOUNDARY = (
    "Exact lower bounds on the first-order growth g_b over every face of the sup-norm "
    "sphere in the anchored 33-coordinate chart at Trump's labelled pose, for every "
    "derivative-distinct branch of exp-013, and the radius the growth route certifies "
    "under the BC-199 per-row remainder bounds. The growth constants are new; the "
    "radius is bounded above by the BC-199 weighted modulus by the exhaustion lemma, so "
    "no claim here enlarges the BC-240 ball. Nothing global."
)


class CaptureRadiusError(ValueError):
    """A typed refusal: malformed input, an uncertified face, or a failed exact check."""


@dataclass(frozen=True)
class Vertex:
    """An exact face vertex: its bounds, basis multipliers and direction."""

    lower: FieldElement | None
    upper: FieldElement | None
    multipliers: list[FieldElement] | None
    free_count: int
    point: list[FieldElement]


@dataclass
class Face:
    """One face program ``d_k = sign`` of a branch, with its exact certificate."""

    coordinate: int
    sign: int
    status: str
    float_value: float | None
    lower: FieldElement | None
    upper: FieldElement | None
    exact: bool
    dual_curvature: FieldElement | None
    route_radius: FieldElement | None
    free_count: int | None = None
    point: list[FieldElement] | None = None

    def as_record(self, field: NumberField) -> dict:
        return {
            "coordinate": self.coordinate,
            "sign": self.sign,
            "status": self.status,
            "float_value": self.float_value,
            "lower_decimal": ir.decimal(field, self.lower) if self.lower is not None else None,
            "upper_decimal": ir.decimal(field, self.upper) if self.upper is not None else None,
            "exact": self.exact,
            "route_radius_decimal": (
                ir.decimal(field, self.route_radius) if self.route_radius is not None else None
            ),
            "free_count": self.free_count,
        }


# ----------------------------------------------------------------------------------------
# One face program: floats propose, an exact dual certifies


def face_lp(
    matrix: np.ndarray, column: np.ndarray, coordinate: int, sign: int
) -> tuple[np.ndarray, float, np.ndarray] | None:
    """``min s`` subject to ``A d + s column >= 0``, ``d_k = sign``, ``-1 <= d <= 1``.

    Returns ``None`` when the face is infeasible, which happens for the growth column
    whenever no direction on the face keeps every non-far row nonnegative.
    """
    row_count, variable_count = matrix.shape
    objective = np.zeros(variable_count + 1)
    objective[-1] = 1.0
    a_ub = np.hstack([-matrix, -column.reshape(row_count, 1)])
    b_ub = np.zeros(row_count)
    bounds = [(-1.0, 1.0)] * variable_count + [(None, None)]
    bounds[coordinate] = (float(sign), float(sign))
    result = linprog(objective, A_ub=a_ub, b_ub=b_ub, bounds=bounds, method="highs")
    if result.status == 2:
        return None
    if not result.success or result.x is None:
        message = f"face LP failed on coordinate {coordinate} sign {sign}: {result.message}"
        raise CaptureRadiusError(message)
    return result.x[:variable_count], float(result.x[-1]), -np.asarray(result.ineqlin.marginals)


def dual_bound(
    field: NumberField,
    sparse: list[list[tuple[int, FieldElement]]],
    weights: list[Fraction],
    coordinate: int,
    sign: int,
) -> FieldElement:
    """``beta = -s w_k - sum_{i != k} |w_i|`` for ``w = A^T weights``.

    For every ``(d, s)`` on the face with ``A d + s column >= 0`` and ``weights >= 0``,
    ``(column^T weights) s >= beta``: a lower bound on ``s`` when the weights carry unit
    column mass, and a Farkas contradiction when they carry none and ``beta > 0``.
    """
    if any(weight < 0 for weight in weights):
        message = "dual weights must be nonnegative"
        raise CaptureRadiusError(message)
    columns: list[list[tuple[FieldElement, Fraction]]] = [[] for _ in range(VARIABLES)]
    for row_index, entries in enumerate(sparse):
        weight = weights[row_index]
        if weight == 0:
            continue
        for column_index, value in entries:
            columns[column_index].append((value, weight))
    w = [ir.combine(field, terms) for terms in columns]
    bound = -ir.scale(w[coordinate], Fraction(sign))
    for index, value in enumerate(w):
        if index != coordinate:
            bound = bound - ir.absolute(value)
    return bound


def exact_vertex(
    field: NumberField,
    rows: tuple[LinearRow, ...],
    sparse: list[list[tuple[int, FieldElement]]],
    column: list[Fraction],
    *,
    coordinate: int,
    sign: int,
    d_float: np.ndarray,
    value_float: float,
    marginals: np.ndarray | None = None,
    tolerance: float = 1e-6,
) -> Vertex | None:
    """Re-solve the face vertex and its dual exactly from the float active set.

    ``upper`` is the exact face value at the vertex when the vertex is feasible,
    ``lower`` the exact dual bound on the same basis when that dual is nonnegative,
    ``multipliers`` the basis multipliers indexed like ``rows``, and ``point`` the exact
    vertex direction.  ``None`` means the float active set did not identify a vertex;
    the caller keeps the rationalised bounds.

    The vertex is usually primal-degenerate (more active rows than unknowns), so the
    basis is chosen among the active rows in order of decreasing float multiplier: a
    basis that carries the dual's support reproduces the optimal dual exactly, while
    one chosen by row index can land on a basis whose dual has a negative entry.
    """
    free = [
        index
        for index in range(VARIABLES)
        if index != coordinate and abs(abs(float(d_float[index])) - 1.0) > tolerance
    ]
    fixed: dict[int, Fraction] = {coordinate: Fraction(sign)}
    for index in range(VARIABLES):
        if index != coordinate and index not in free:
            fixed[index] = Fraction(1 if d_float[index] > 0 else -1)
    products = [
        sum(float(value) * float(d_float[index]) for index, value in entries)
        for entries in sparse
    ]
    active = [
        index
        for index, product in enumerate(products)
        if abs(product + float(column[index]) * value_float)
        <= tolerance * (1.0 + abs(value_float))
    ]
    if len(active) < len(free) + 1:
        return None
    if marginals is not None:
        active.sort(key=lambda index: -float(marginals[index]))
    system_rows = tuple(
        LinearRow(
            f"active:{index}",
            (
                *(rows[index].coefficients[free_index] for free_index in free),
                field.rational(column[index]),
            ),
        )
        for index in active
    )
    pivots = tc.exact_pivot_rows(system_rows)
    if pivots is None:
        return None
    basis = [active[pivot] for pivot in pivots]
    matrix = [list(system_rows[pivot].coefficients) for pivot in pivots]
    rhs = [
        -ir.combine(
            field,
            [(value, fixed[index]) for index, value in sparse[active[pivot]] if index in fixed],
        )
        for pivot in pivots
    ]
    solution = tc.exact_solve(matrix, rhs, field)
    if solution is None:
        return None
    point: list[FieldElement] = [field.zero for _ in range(VARIABLES)]
    for index, value in fixed.items():
        point[index] = field.rational(value)
    for index, value in zip(free, solution[:-1], strict=True):
        point[index] = value
    if any((ir.absolute(point[index]) - field.one).sign() > 0 for index in free):
        return None
    exact_products = [
        sum((value * point[index] for index, value in entries), field.zero)
        for entries in sparse
    ]
    upper: FieldElement | None = None
    if all(
        product.sign() >= 0
        for product, weight in zip(exact_products, column, strict=True)
        if weight == 0
    ):
        upper = ir.exact_max(
            [
                -product / field.rational(weight)
                for product, weight in zip(exact_products, column, strict=True)
                if weight != 0
            ]
        )
    size = len(free) + 1
    dual_matrix = [
        [
            rows[basis[column_index]].coefficients[free[row_index]]
            for column_index in range(size)
        ]
        for row_index in range(len(free))
    ]
    dual_matrix.append([field.rational(column[basis[index]]) for index in range(size)])
    dual_rhs = [field.zero for _ in range(len(free))] + [field.one]
    dual = tc.exact_solve(dual_matrix, dual_rhs, field)
    if dual is None or any(weight.sign() < 0 for weight in dual):
        return Vertex(None, upper, None, len(free), point)
    multipliers = [field.zero for _ in rows]
    for index, weight in zip(basis, dual, strict=True):
        multipliers[index] = weight
    w = [
        sum(
            (rows[basis[index]].coefficients[variable] * dual[index] for index in range(size)),
            field.zero,
        )
        for variable in range(VARIABLES)
    ]
    lower = -ir.scale(w[coordinate], Fraction(sign))
    for index, value in enumerate(w):
        if index != coordinate:
            lower = lower - ir.absolute(value)
    return Vertex(lower, upper, multipliers, len(free), point)


# ----------------------------------------------------------------------------------------
# All faces of one branch


def _route_radius(beta: FieldElement, weighted_curvature: FieldElement) -> FieldElement | None:
    """``2 beta / (mu^T K)``: the radius the multipliers ``mu`` certify on the face."""
    if weighted_curvature.sign() <= 0:
        return None
    return (beta + beta) / weighted_curvature


def _curvature_of(field: NumberField, weights: list[Fraction], curvature: list[Fraction]):
    return field.rational(
        sum(
            (weight * value for weight, value in zip(weights, curvature, strict=True)),
            Fraction(0),
        )
    )


def branch_faces(
    field: NumberField,
    rows: tuple[LinearRow, ...],
    column: list[Fraction],
    curvature: list[Fraction],
    *,
    row_weights: list[Fraction] | None = None,
    faces: tuple[tuple[int, int], ...] = ALL_FACES,
    refine_limit: int = 4,
) -> list[Face]:
    """Certify every requested face of ``min s : A d + s column >= 0`` on the sphere.

    ``column`` selects the program: the far-wall indicator gives the growth ``g_b``, all
    ones the BC-199 modulus; ``row_weights`` scale the rows first (``2/K_j`` gives the
    BC-199 per-row pass).  ``curvature`` holds ``K_j`` for the route radius of each face's
    certified multipliers, expressed on the unscaled rows.
    """
    if len(column) != len(rows) or len(curvature) != len(rows):
        message = "column and curvature need one entry per row"
        raise CaptureRadiusError(message)
    if any(weight < 0 for weight in column) or all(weight == 0 for weight in column):
        message = "the scalar column must be nonnegative with positive mass"
        raise CaptureRadiusError(message)
    scaled_rows = rows
    scaling = [Fraction(1)] * len(rows)
    if row_weights is not None:
        if len(row_weights) != len(rows) or any(weight <= 0 for weight in row_weights):
            message = "row weights must be positive and one per row"
            raise CaptureRadiusError(message)
        scaling = list(row_weights)
        scaled_rows = tuple(
            LinearRow(row.label, tuple(ir.scale(value, weight) for value in row.coefficients))
            for row, weight in zip(rows, row_weights, strict=True)
        )
    if any(len(row.coefficients) != VARIABLES for row in scaled_rows):
        message = f"every row must have {VARIABLES} coefficients"
        raise CaptureRadiusError(message)
    matrix = tc.as_float_matrix(scaled_rows)
    sparse = ir.sparse_rows(scaled_rows)
    column_float = np.asarray([float(weight) for weight in column])
    zero_rows = [index for index, weight in enumerate(column) if weight == 0]
    phase_matrix = matrix[zero_rows] if zero_rows else None
    modulus_weights = [
        2 / (value * factor) for value, factor in zip(curvature, scaling, strict=True)
    ]
    modulus_matrix = matrix * np.asarray([float(w) for w in modulus_weights])[:, None]

    results: list[Face] = []
    proposals: dict[tuple[int, int], tuple[np.ndarray, float, np.ndarray]] = {}
    for coordinate, sign in faces:
        proposal = face_lp(matrix, column_float, coordinate, sign)
        if proposal is None:
            results.append(
                _infeasible_face(
                    field,
                    sparse,
                    phase_matrix=phase_matrix,
                    zero_rows=zero_rows,
                    modulus_matrix=modulus_matrix,
                    modulus_weights=modulus_weights,
                    scaling=scaling,
                    curvature=curvature,
                    coordinate=coordinate,
                    sign=sign,
                )
            )
            continue
        d_float, value_float, marginals = proposal
        raw = [ir.rationalise(max(value, 0.0)) for value in marginals]
        mass = sum(
            (weight * entry for weight, entry in zip(raw, column, strict=True)), Fraction(0)
        )
        if mass <= 0:
            message = f"float dual carries no column mass on face {(coordinate, sign)}"
            raise CaptureRadiusError(message)
        weights = [weight / mass for weight in raw]
        beta = dual_bound(field, sparse, weights, coordinate, sign)
        unscaled = [weight * factor for weight, factor in zip(weights, scaling, strict=True)]
        weighted_curvature = _curvature_of(field, unscaled, curvature)
        results.append(
            Face(
                coordinate=coordinate,
                sign=sign,
                status="finite",
                float_value=value_float,
                lower=beta,
                upper=None,
                exact=False,
                dual_curvature=weighted_curvature,
                route_radius=_route_radius(beta, weighted_curvature),
            )
        )
        proposals[(coordinate, sign)] = (d_float, value_float, marginals)

    finite = [index for index, face in enumerate(results) if face.status == "finite"]
    order = sorted(finite, key=lambda index: results[index].float_value or 0.0)
    refined = 0
    best_upper: FieldElement | None = None
    for index in order[:refine_limit]:
        face = results[index]
        if (
            best_upper is not None
            and face.lower is not None
            and (face.lower - best_upper).sign() >= 0
        ):
            break
        d_float, value_float, marginals = proposals[(face.coordinate, face.sign)]
        vertex = exact_vertex(
            field,
            scaled_rows,
            sparse,
            column,
            coordinate=face.coordinate,
            sign=face.sign,
            d_float=d_float,
            value_float=value_float,
            marginals=marginals,
        )
        refined += 1
        if vertex is None:
            continue
        lower, upper, multipliers, free_count = (
            vertex.lower,
            vertex.upper,
            vertex.multipliers,
            vertex.free_count,
        )
        face.free_count = free_count
        face.point = vertex.point
        if upper is not None and (face.upper is None or (upper - face.upper).sign() < 0):
            face.upper = upper
        if lower is not None and face.lower is not None and (lower - face.lower).sign() > 0:
            face.lower = lower
            if multipliers is not None:
                exact_curvature = sum(
                    (
                        ir.scale(weight, factor * value)
                        for weight, factor, value in zip(
                            multipliers, scaling, curvature, strict=True
                        )
                    ),
                    field.zero,
                )
                face.dual_curvature = exact_curvature
                face.route_radius = _route_radius(lower, exact_curvature)
        face.exact = (
            face.lower is not None
            and face.upper is not None
            and (face.lower - face.upper).is_zero()
        )
        if face.upper is not None and (
            best_upper is None or (face.upper - best_upper).sign() < 0
        ):
            best_upper = face.upper
    return results


def _infeasible_face(
    field: NumberField,
    sparse: list[list[tuple[int, FieldElement]]],
    *,
    phase_matrix: np.ndarray | None,
    zero_rows: list[int],
    modulus_matrix: np.ndarray,
    modulus_weights: list[Fraction],
    scaling: list[Fraction],
    curvature: list[Fraction],
    coordinate: int,
    sign: int,
) -> Face:
    """Certify an infeasible face and the best radius any multiplier vector gives it.

    Two exact certificates.  The status comes from a Farkas vector on the zero-column
    rows alone (the growth is ``+inf`` on the face: no direction keeps every non-far
    row nonnegative).  The route radius comes from the per-row weighted modulus over
    all rows, ``min t : (2/K_j) a_j d + t >= 0``, because under ``sigma <= 0`` every
    row, far walls included, reads ``a_j v + R_j >= 0`` and the lemma says that
    program's dual is the best certificate the remainder model admits; the growth
    route has no certificate of its own here, so it is given the best one.
    """
    if phase_matrix is None:
        message = f"face {(coordinate, sign)} is infeasible with a positive column"
        raise CaptureRadiusError(message)
    phase = face_lp(phase_matrix, np.ones(len(zero_rows)), coordinate, sign)
    if phase is None:
        message = f"phase-one program is infeasible on face {(coordinate, sign)}"
        raise CaptureRadiusError(message)
    _d_float, slack, marginals = phase
    raw = [ir.rationalise(max(value, 0.0)) for value in marginals]
    mass = sum(raw, Fraction(0))
    if slack <= 0 or mass <= 0:
        message = f"phase-one program did not certify face {(coordinate, sign)}"
        raise CaptureRadiusError(message)
    farkas = [Fraction(0)] * len(sparse)
    for position, index in enumerate(zero_rows):
        farkas[index] = raw[position] / mass
    if dual_bound(field, sparse, farkas, coordinate, sign).sign() <= 0:
        message = f"exact Farkas bound is not positive on face {(coordinate, sign)}"
        raise CaptureRadiusError(message)
    best = face_lp(modulus_matrix, np.ones(len(sparse)), coordinate, sign)
    if best is None:
        message = f"weighted modulus program is infeasible on face {(coordinate, sign)}"
        raise CaptureRadiusError(message)
    _d_float, _value, marginals = best
    raw = [ir.rationalise(max(value, 0.0)) for value in marginals]
    mass = sum(raw, Fraction(0))
    if mass <= 0:
        message = f"weighted modulus dual carries no mass on face {(coordinate, sign)}"
        raise CaptureRadiusError(message)
    weights = [
        entry * factor / mass for entry, factor in zip(raw, modulus_weights, strict=True)
    ]
    beta = dual_bound(field, sparse, weights, coordinate, sign)
    unscaled = [weight * factor for weight, factor in zip(weights, scaling, strict=True)]
    weighted_curvature = _curvature_of(field, unscaled, curvature)
    return Face(
        coordinate=coordinate,
        sign=sign,
        status="infeasible",
        float_value=None,
        lower=None,
        upper=None,
        exact=False,
        dual_curvature=weighted_curvature,
        route_radius=_route_radius(beta, weighted_curvature),
    )


# ----------------------------------------------------------------------------------------
# Branch summaries and the domination check


type Planar = tuple[SecondOrderJet, SecondOrderJet]
_FRAMES: dict[
    int, tuple[dict[tuple[int, int], Planar], dict[tuple[int, int], Planar], SecondOrderJet]
] = {}


def _pose_frame(witness: ir.Witness):
    """Corner and edge-normal jets of every square at the pose, built once per witness."""
    cached = _FRAMES.get(id(witness))
    if cached is not None:
        return cached
    field = witness.field
    dimension = VARIABLES

    def variable(value: FieldElement, index: int) -> SecondOrderJet:
        return SecondOrderJet.variable(value, dimension, index)

    corners: dict[tuple[int, int], Planar] = {}
    axes: dict[tuple[int, int], Planar] = {}
    for index, square in enumerate(witness.squares):
        cx, cy = witness.centres[index]
        x_jet, y_jet = variable(cx, 3 * index), variable(cy, 3 * index + 1)
        spin = variable(field.zero, 3 * index + 2)
        for corner, (px, py) in enumerate(square):
            fx, fy = SecondOrderJet.rotation((px - cx, py - cy), spin)
            corners[(index, corner)] = (x_jet + fx, y_jet + fy)
        for axis_index, axis in enumerate(edge_axes(square)):
            axes[(index, axis_index)] = SecondOrderJet.rotation(axis, spin)
    frame = (corners, axes, SecondOrderJet.constant(witness.side, dimension))
    _FRAMES[id(witness)] = frame
    return frame


def row_jets(witness: ir.Witness, rows: tuple[LinearRow, ...]) -> list[SecondOrderJet]:
    """Every branch row as an exact second-order jet, rebuilt from its label.

    A wall row is the corner coordinate (or the side minus it); a pair row is the owner's
    rotated edge normal dotted with the difference of the two named corners.  Each jet
    must vanish at the pose and have exactly the retained row as its gradient, which ties
    ``exact_jets`` to ``tangent_cones`` row by row; a mismatch is a refusal.
    """
    corners, axes, side = _pose_frame(witness)

    def build(label: str) -> SecondOrderJet:
        parts = label.split(":")
        if parts[0] == "wall":
            square, wall = int(parts[1]), parts[2]
            corner = int(parts[3].split("-")[1])
            px, py = corners[(square, corner)]
            return {"left": px, "right": side - px, "bottom": py, "top": side - py}[wall]
        if parts[0] != "pair":
            message = f"unrecognised row label: {label}"
            raise CaptureRadiusError(message)
        owner = int(parts[2].split("-")[1])
        axis_index = int(parts[3].split("-")[1])
        negative, positive = parts[5].removeprefix("vertices-").split("-")
        negative_square, negative_corner = (int(item) for item in negative.split("."))
        positive_square, positive_corner = (int(item) for item in positive.split("."))
        ax, ay = axes[(owner, axis_index)]
        ppx, ppy = corners[(positive_square, positive_corner)]
        pnx, pny = corners[(negative_square, negative_corner)]
        return ax * (ppx - pnx) + ay * (ppy - pny)

    jets = []
    for row in rows:
        jet = build(row.label)
        if not jet.value.is_zero():
            message = f"row {row.label} does not vanish at the pose"
            raise CaptureRadiusError(message)
        if any(
            not (left - right).is_zero()
            for left, right in zip(jet.gradient, row.coefficients, strict=True)
        ):
            message = f"row {row.label} gradient does not match the retained row"
            raise CaptureRadiusError(message)
        jets.append(jet)
    return jets


def directional_curvature(
    witness: ir.Witness,
    rows: tuple[LinearRow, ...],
    curvature: list[Fraction],
    point: list[FieldElement],
) -> dict:
    """Exact Taylor coefficients of every row along one direction, against ``K_j/2``.

    Along ``z* + t point`` row ``j`` reads ``l_j t + q_j t^2 + O(t^3)`` with ``l_j`` the
    retained first-order change and ``q_j = point^T H_j point / 2`` exact.  The uniform
    model replaces ``q_j`` by ``+K_j/2`` for every row at once.  A row with ``l_j < 0``
    and ``q_j <= 0`` is violated at every scale to second order; one with ``q_j > 0``
    recovers at ``t = -l_j/q_j``.  The direction is excluded until every decreasing row
    has recovered, so the second-order exclusion scale is the largest recovery scale, or
    unbounded when some row never recovers.  This ignores the cubic remainder and the
    other directions: a discriminator for a sharper remainder model, not a theorem.
    """
    field = witness.field
    jets = row_jets(witness, rows)
    zero = [field.zero for _ in range(VARIABLES)]
    table = []
    never = 0
    recovery: list[FieldElement] = []
    largest_ratio: Fraction | None = None
    for row, jet, bound in zip(rows, jets, curvature, strict=True):
        taylor = jet.substitute(point, zero)
        half = Fraction(bound, 2)
        ratio = Fraction(ir.rational_upper(field, taylor.quadratic)) / half
        largest_ratio = (
            ratio if largest_ratio is None or ratio > largest_ratio else largest_ratio
        )
        entry = {
            "row": row.label,
            "linear_decimal": ir.decimal(field, taylor.linear),
            "quadratic_decimal": ir.decimal(field, taylor.quadratic),
            "half_K": str(half),
            "quadratic_over_half_K_float": float(ratio),
        }
        if taylor.linear.sign() < 0:
            if taylor.quadratic.sign() > 0:
                scale_value = -taylor.linear / taylor.quadratic
                recovery.append(scale_value)
                entry["recovery_scale_decimal"] = ir.decimal(field, scale_value)
            else:
                never += 1
                entry["recovery_scale_decimal"] = None
        table.append(entry)
    exclusion = None if never else (ir.exact_max(recovery) if recovery else None)
    return {
        "rows": table,
        "decreasing_rows_never_recovering_to_second_order": never,
        "decreasing_rows_recovering": len(recovery),
        "second_order_exclusion_scale_decimal": (
            ir.decimal(field, exclusion) if exclusion is not None else None
        ),
        "second_order_exclusion_unbounded": never > 0,
        "largest_quadratic_over_half_K_float": (
            float(largest_ratio) if largest_ratio is not None else None
        ),
    }


def _argmin_curvature(
    witness: ir.Witness,
    branch: dict,
    rows: tuple[LinearRow, ...],
    curvature: list[Fraction],
    control: list[Face],
) -> dict:
    """The directional-curvature table along the control pass's exact argmin vertex."""
    field = witness.field
    argmin = min(
        (face for face in control if face.point is not None),
        key=lambda face: face.float_value or 0.0,
        default=None,
    )
    if argmin is None or argmin.point is None:
        message = f"branch {branch['branch']} has no exact argmin vertex"
        raise CaptureRadiusError(message)
    detail = directional_curvature(witness, rows, curvature, argmin.point)
    return {
        "face": {"coordinate": argmin.coordinate, "sign": argmin.sign},
        "uniform_model_scale_decimal": (
            ir.decimal(field, argmin.lower) if argmin.lower is not None else None
        ),
        "angle_components_float": [float(argmin.point[index]) for index in ANGLE_COORDINATES],
        **detail,
    }


def face_minimum(faces: list[Face], subset: tuple[tuple[int, int], ...] | None = None) -> dict:
    """Certified lower and upper bounds on the minimum over the chosen finite faces."""
    chosen = [
        face
        for face in faces
        if face.status == "finite"
        and (subset is None or (face.coordinate, face.sign) in subset)
    ]
    if not chosen:
        return {"finite_faces": 0, "lower": None, "upper": None, "exact": False, "argmin": None}
    lowers = [face.lower for face in chosen if face.lower is not None]
    uppers = [face.upper for face in chosen if face.upper is not None]
    if len(lowers) != len(chosen):
        message = "a finite face lacks a certified lower bound"
        raise CaptureRadiusError(message)
    lower = ir.exact_min(lowers)
    upper = ir.exact_min(uppers) if uppers else None
    argmin = min(chosen, key=lambda face: face.float_value or 0.0)
    return {
        "finite_faces": len(chosen),
        "lower": lower,
        "upper": upper,
        "exact": upper is not None and (lower - upper).is_zero(),
        "argmin": {
            "coordinate": argmin.coordinate,
            "sign": argmin.sign,
            "free_count": argmin.free_count,
        },
    }


def domination(growth: list[Face], modulus: list[Face]) -> dict:
    """Check ``route radius <= weighted modulus`` face by face, as the lemma predicts.

    The sufficient comparison is against the modulus face's certified lower bound; the
    necessary one is against its upper bound where an exact vertex pinned it.
    """
    by_face = {(face.coordinate, face.sign): face for face in modulus}
    sufficient = necessary = comparable = 0
    worst_ratio: FieldElement | None = None
    for face in growth:
        other = by_face.get((face.coordinate, face.sign))
        if other is None or face.route_radius is None or other.lower is None:
            continue
        comparable += 1
        if (face.route_radius - other.lower).sign() <= 0:
            sufficient += 1
        if other.upper is None or (face.route_radius - other.upper).sign() <= 0:
            necessary += 1
        ratio = face.route_radius / other.lower
        if worst_ratio is None or (ratio - worst_ratio).sign() > 0:
            worst_ratio = ratio
    return {
        "comparable_faces": comparable,
        "route_radius_at_most_modulus_lower": sufficient,
        "route_radius_at_most_modulus_upper": necessary,
        "largest_route_over_modulus_ratio": worst_ratio,
    }


def far_column(rows: tuple[LinearRow, ...]) -> list[Fraction]:
    far = set(ir.far_rows(rows))
    return [Fraction(1 if index in far else 0) for index in range(len(rows))]


def build_result(
    *,
    branch_limit: int | None = None,
    faces: tuple[tuple[int, int], ...] = ALL_FACES,
    refine_limit: int = 4,
    modulus: bool = True,
    curvature_at_argmin: bool = False,
    log=None,
) -> dict:
    """Run the growth pass (and the weighted-modulus control) over the branches."""
    started = time.monotonic()
    witness = ir.load_witness()
    field = witness.field
    functions = ir.elementary_functions(witness, ir.DEFAULT_BOX)
    identification = ir.identify_rows(witness, functions)
    row_curvature = identification["row_curvature"]
    branches = witness.branches if branch_limit is None else witness.branches[:branch_limit]

    table = []
    growth_lowers: list[FieldElement] = []
    growth_uppers: list[FieldElement] = []
    angle_lowers: list[FieldElement] = []
    modulus_lowers: list[FieldElement] = []
    route_radii: list[FieldElement] = []
    dominated = {
        "comparable_faces": 0,
        "route_radius_at_most_modulus_lower": 0,
        "route_radius_at_most_modulus_upper": 0,
    }
    worst_ratio: FieldElement | None = None
    for branch in branches:
        stamp = time.monotonic()
        rows = branch["rows"]
        curvature = [row_curvature[tc.row_key(row)] for row in rows]
        column = far_column(rows)
        growth = branch_faces(
            field, rows, column, curvature, faces=faces, refine_limit=refine_limit
        )
        summary = face_minimum(growth)
        angles = face_minimum(growth, ANGLE_FACES)
        entry = {
            "branch": branch["branch"],
            "raw_selection_count": branch["raw_selection_count"],
            "faces": len(growth),
            "finite_faces": summary["finite_faces"],
            "infeasible_faces": sum(face.status == "infeasible" for face in growth),
            "growth_lower_decimal": ir.decimal(field, summary["lower"]),
            "growth_upper_decimal": (
                ir.decimal(field, summary["upper"]) if summary["upper"] is not None else None
            ),
            "growth_exact": summary["exact"],
            "growth_argmin_face": summary["argmin"],
            "angle_faces_finite": angles["finite_faces"],
            "angle_faces_growth_lower_decimal": (
                ir.decimal(field, angles["lower"]) if angles["lower"] is not None else None
            ),
        }
        growth_lowers.append(summary["lower"])
        if summary["upper"] is not None:
            growth_uppers.append(summary["upper"])
        if angles["lower"] is not None:
            angle_lowers.append(angles["lower"])
        radii = [face.route_radius for face in growth if face.route_radius is not None]
        if len(radii) != len(growth):
            message = f"branch {branch['branch']} has a face without a route radius"
            raise CaptureRadiusError(message)
        branch_route = ir.exact_min(radii)
        route_radii.append(branch_route)
        entry["route_radius_min_decimal"] = ir.decimal(field, branch_route)
        if modulus:
            weights = [2 / value for value in curvature]
            control = branch_faces(
                field,
                rows,
                [Fraction(1)] * len(rows),
                curvature,
                row_weights=weights,
                faces=faces,
                refine_limit=refine_limit,
            )
            control_summary = face_minimum(control)
            modulus_lowers.append(control_summary["lower"])
            entry["weighted_modulus_lower_decimal"] = ir.decimal(
                field, control_summary["lower"]
            )
            entry["weighted_modulus_exact"] = control_summary["exact"]
            entry["weighted_modulus_argmin_face"] = control_summary["argmin"]
            check = domination(growth, control)
            for key in dominated:
                dominated[key] += check[key]
            ratio = check["largest_route_over_modulus_ratio"]
            if ratio is not None and (worst_ratio is None or (ratio - worst_ratio).sign() > 0):
                worst_ratio = ratio
            entry["domination"] = {
                key: value
                for key, value in check.items()
                if key != "largest_route_over_modulus_ratio"
            }
            entry["domination"]["largest_ratio_decimal"] = (
                ir.decimal(field, ratio) if ratio is not None else None
            )
            if curvature_at_argmin:
                entry["directional_curvature"] = _argmin_curvature(
                    witness, branch, rows, curvature, control
                )
        entry["seconds"] = round(time.monotonic() - stamp, 3)
        table.append(entry)
        if log is not None:
            route_text = entry["route_radius_min_decimal"][:12]
            log(
                f"branch {branch['branch']:3d} g [{entry['growth_lower_decimal'][:12]}, "
                f"{(entry['growth_upper_decimal'] or '')[:12]}] exact={entry['growth_exact']} "
                f"infeasible={entry['infeasible_faces']} route={route_text} "
                f"modulus={entry.get('weighted_modulus_lower_decimal', '')[:12]} "
                f"{entry['seconds']}s"
            )
    if not table:
        message = "no branch was computed"
        raise CaptureRadiusError(message)
    growth_lower = ir.exact_min(growth_lowers)
    growth_upper = ir.exact_min(growth_uppers) if growth_uppers else None
    route_radius = ir.exact_min(route_radii)
    modulus_lower = ir.exact_min(modulus_lowers) if modulus_lowers else None
    return {
        "schema_version": 1,
        "hypothesis": "H-237",
        "chart": (
            "anchored centre-angle chart of BC-240: container [0, U]^2 with a corner at the "
            "origin, square i = (x_i, y_i, theta_i), sup norm over the 33 coordinates"
        ),
        "claim_boundary": CLAIM_BOUNDARY,
        "inputs": {path: ir.sha256(ir.ROOT / path) for path in ir.FROZEN_INPUTS},
        "branches_computed": len(table),
        "faces_per_branch": len(faces),
        "growth": {
            "definition": "g_b(d) = min { sigma : A_b d + sigma e >= 0 }, e = far-wall rows",
            "sphere_min_lower_decimal": ir.decimal(field, growth_lower),
            "sphere_min_lower_rational": str(ir.rational_lower(field, growth_lower)),
            "sphere_min_upper_decimal": (
                ir.decimal(field, growth_upper) if growth_upper is not None else None
            ),
            "sphere_min_exact": growth_upper is not None
            and (growth_lower - growth_upper).is_zero(),
            "angle_faces_min_lower_decimal": (
                ir.decimal(field, ir.exact_min(angle_lowers)) if angle_lowers else None
            ),
            "all_faces_positive": all(lower.sign() > 0 for lower in growth_lowers),
        },
        "route": {
            "statement": (
                "on a face with certified multipliers mu, side > U (or infeasibility) is "
                "certified for 0 < ||v||_inf < 2 beta(mu) / (mu^T K)"
            ),
            "facewise_radius_decimal": ir.decimal(field, route_radius),
            "facewise_radius_rational_lower": str(ir.rational_lower(field, route_radius)),
            "rho_row": str(RHO_ROW),
            "rho_row_float": float(RHO_ROW),
            "facewise_radius_over_rho_row": float(
                ir.rational_lower(field, route_radius) / RHO_ROW
            ),
            "exceeds_retained_rho_row": (route_radius - field.rational(RHO_ROW)).sign() > 0,
            "excess_over_retained_rho_row_float": float(
                ir.rational_lower(field, route_radius) - RHO_ROW
            ),
            "at_most_weighted_modulus_min": (
                modulus_lower is not None and (route_radius - modulus_lower).sign() <= 0
            ),
            "equals_weighted_modulus_min": (
                modulus_lower is not None and (route_radius - modulus_lower).is_zero()
            ),
            "note": (
                "the retained rho_row is a rational lower bound on the exact BC-199 "
                "weighted modulus; an excess below 1e-12 is that shortening, not a larger "
                "ball"
            ),
        },
        "modulus_control": {
            "weighted_modulus_min_lower_decimal": (
                ir.decimal(field, modulus_lower) if modulus_lower is not None else None
            ),
            "reproduces_bc199_branch_0": (
                table[0].get("weighted_modulus_lower_decimal", "").startswith(RHO_ROW_DECIMAL)
            ),
            **dominated,
            "largest_route_over_modulus_ratio_decimal": (
                ir.decimal(field, worst_ratio) if worst_ratio is not None else None
            ),
            "lemma_consequence_holds": (
                dominated["comparable_faces"] > 0
                and dominated["route_radius_at_most_modulus_upper"]
                == dominated["comparable_faces"]
            ),
        },
        "branches": table,
        "elapsed_seconds": round(time.monotonic() - started, 3),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", type=Path, help="write the JSON record atomically")
    parser.add_argument("--branches", type=int, default=None, help="only the first N branches")
    parser.add_argument(
        "--angle-faces", action="store_true", help="only the 22 angle faces, not all 66"
    )
    parser.add_argument(
        "--no-modulus", action="store_true", help="skip the weighted-modulus control"
    )
    parser.add_argument(
        "--curvature",
        action="store_true",
        help="exact second-order terms of every row along each branch's argmin direction",
    )
    parser.add_argument(
        "--refine-limit",
        type=int,
        default=4,
        help="faces re-solved exactly per branch and pass",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build_result(
        branch_limit=args.branches,
        faces=ANGLE_FACES if args.angle_faces else ALL_FACES,
        refine_limit=args.refine_limit,
        modulus=not args.no_modulus,
        curvature_at_argmin=args.curvature,
        log=lambda line: print(line, flush=True),
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.record.with_suffix(args.record.suffix + ".tmp")
        temporary.write_text(rendered)
        temporary.replace(args.record)
    summary = {
        key: result[key] for key in ("growth", "route", "modulus_control", "elapsed_seconds")
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
