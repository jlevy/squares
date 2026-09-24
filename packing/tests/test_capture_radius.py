"""Behaviour checks for the Trump n = 11 growth-cone capture-radius tool (H-237)."""

from __future__ import annotations

import functools
from fractions import Fraction

import pytest

from cases.trump11 import capture_radius as tool
from cases.trump11 import isolation_radius as ir
from cases.trump11 import tangent_cones as tc
from sqpack.exact_lp import LinearRow
from sqpack.field import NumberField

# Branch 0's growth minimum over the whole sphere, pinned by an exact vertex on the face
# theta_10 = -1.  The prefix is the tool's own decimal; a change here is a change in the
# rows, the far-wall set, or the field.
PINNED_G_0_DECIMAL = "0.05177145320566823254"
COORDINATE_FACES = ((0, 1), (0, -1))


@functools.cache
def witness() -> ir.Witness:
    return ir.load_witness()


@functools.cache
def branch_zero() -> tuple:
    w = witness()
    functions = ir.elementary_functions(w, ir.DEFAULT_BOX)
    identification = ir.identify_rows(w, functions)
    rows = w.branches[0]["rows"]
    curvature = [identification["row_curvature"][tc.row_key(row)] for row in rows]
    return w.field, rows, curvature


def toy_field() -> NumberField:
    return NumberField([1, 0, -2], (1, 2))


def toy_row(field: NumberField, label: str, entries: dict[int, Fraction]) -> LinearRow:
    coefficients = [field.zero for _ in range(tool.VARIABLES)]
    for index, value in entries.items():
        coefficients[index] = field.rational(value)
    return LinearRow(label, tuple(coefficients))


def test_toy_growth_exceeds_modulus_and_route_radius_equals_weighted_modulus() -> None:
    # One coordinate: a far row d_0 >= 0 with K = 1 and a non-far row -d_0/2 >= 0 with
    # K = 4.  The cone is zero.  The face d_0 = +1 is infeasible at first order and the
    # Farkas multiplier certifies radius 2 (1/2) / 4 = 1/4; the face d_0 = -1 has growth
    # 1 and radius 2.  The plain modulus is 1/2 < 1, and the per-row weighted modulus
    # reproduces both radii, which is the lemma's equality case.
    field = toy_field()
    rows = (
        toy_row(field, "wall:0:right:corner-0", {0: Fraction(1)}),
        toy_row(field, "pair:0-1", {0: Fraction(-1, 2)}),
    )
    column = [Fraction(1), Fraction(0)]
    curvature = [Fraction(1), Fraction(4)]
    growth = tool.branch_faces(field, rows, column, curvature, faces=COORDINATE_FACES)
    by_face = {(face.coordinate, face.sign): face for face in growth}
    plus, minus = by_face[(0, 1)], by_face[(0, -1)]
    assert plus.status == "infeasible"
    assert plus.route_radius is not None
    assert (plus.route_radius - field.rational(Fraction(1, 4))).is_zero()
    assert minus.status == "finite"
    assert minus.exact is True
    assert minus.lower is not None
    assert (minus.lower - field.one).is_zero()
    assert minus.route_radius is not None
    assert (minus.route_radius - field.rational(2)).is_zero()
    summary = tool.face_minimum(growth)
    assert summary["exact"] is True
    assert (summary["lower"] - field.one).is_zero()

    plain = tool.branch_faces(
        field, rows, [Fraction(1), Fraction(1)], curvature, faces=COORDINATE_FACES
    )
    assert (tool.face_minimum(plain)["lower"] - field.rational(Fraction(1, 2))).is_zero()

    weighted = tool.branch_faces(
        field,
        rows,
        [Fraction(1), Fraction(1)],
        curvature,
        row_weights=[2 / value for value in curvature],
        faces=COORDINATE_FACES,
    )
    check = tool.domination(growth, weighted)
    assert check["comparable_faces"] == 2
    assert check["route_radius_at_most_modulus_lower"] == 2
    assert check["route_radius_at_most_modulus_upper"] == 2
    assert (check["largest_route_over_modulus_ratio"] - field.one).is_zero()


def test_toy_two_dimensional_zero_cone_is_certified_on_both_faces() -> None:
    # Far rows d_0 >= 0 and d_1 >= 0, a non-far row -d_0 - d_1 >= 0 with K = 10: the cone
    # is zero and the growth is 1 on both faces of coordinate 0.  On d_0 = +1 the growth
    # dual must lean on the non-far row, so the route radius there is 2/(1 + 10) = 2/11,
    # and the weighted modulus on that face is the same 2/11.
    field = toy_field()
    rows = (
        toy_row(field, "wall:0:right:corner-0", {0: Fraction(1)}),
        toy_row(field, "wall:0:top:corner-0", {1: Fraction(1)}),
        toy_row(field, "pair:0-1", {0: Fraction(-1), 1: Fraction(-1)}),
    )
    column = [Fraction(1), Fraction(1), Fraction(0)]
    curvature = [Fraction(1), Fraction(1), Fraction(10)]
    growth = tool.branch_faces(field, rows, column, curvature, faces=COORDINATE_FACES)
    assert all(face.status == "finite" for face in growth)
    assert all(face.lower is not None and (face.lower - field.one).is_zero() for face in growth)
    plus = next(face for face in growth if face.sign == 1)
    assert plus.route_radius is not None
    assert (plus.route_radius - field.rational(Fraction(2, 11))).is_zero()
    weighted = tool.branch_faces(
        field,
        rows,
        [Fraction(1)] * 3,
        curvature,
        row_weights=[2 / value for value in curvature],
        faces=COORDINATE_FACES,
    )
    check = tool.domination(growth, weighted)
    assert check["route_radius_at_most_modulus_upper"] == 2


def test_refusals_name_the_malformed_input() -> None:
    field = toy_field()
    rows = (toy_row(field, "wall:0:right:corner-0", {0: Fraction(1)}),)
    with pytest.raises(tool.CaptureRadiusError, match="one entry per row"):
        tool.branch_faces(field, rows, [Fraction(1), Fraction(1)], [Fraction(1)])
    with pytest.raises(tool.CaptureRadiusError, match="positive mass"):
        tool.branch_faces(field, rows, [Fraction(0)], [Fraction(1)])
    with pytest.raises(tool.CaptureRadiusError, match="nonnegative"):
        tool.branch_faces(field, rows, [Fraction(-1)], [Fraction(1)])
    with pytest.raises(tool.CaptureRadiusError, match="row weights"):
        tool.branch_faces(field, rows, [Fraction(1)], [Fraction(1)], row_weights=[Fraction(0)])
    with pytest.raises(tool.CaptureRadiusError, match="nonnegative"):
        tool.dual_bound(field, ir.sparse_rows(rows), [Fraction(-1)], 0, 1)
    assert tool.far_column(branch_zero()[1]).count(Fraction(1)) == 9


def test_branch_zero_angle_faces_are_all_positive_and_pinned() -> None:
    field, rows, curvature = branch_zero()
    growth = tool.branch_faces(
        field, rows, tool.far_column(rows), curvature, faces=tool.ANGLE_FACES, refine_limit=2
    )
    assert len(growth) == 22
    finite = [face for face in growth if face.status == "finite"]
    assert all(face.lower is not None and face.lower.sign() > 0 for face in finite)
    assert all(
        face.route_radius is not None and face.route_radius.sign() > 0 for face in growth
    )
    summary = tool.face_minimum(growth)
    assert summary["exact"] is True
    assert ir.decimal(field, summary["lower"]).startswith(PINNED_G_0_DECIMAL)
    assert summary["argmin"]["coordinate"] == 32


@pytest.mark.slow
def test_branch_zero_reproduces_bc199_and_the_lemma_caps_the_route() -> None:
    field, rows, curvature = branch_zero()
    growth = tool.branch_faces(field, rows, tool.far_column(rows), curvature)
    control = tool.branch_faces(
        field,
        rows,
        [Fraction(1)] * len(rows),
        curvature,
        row_weights=[2 / value for value in curvature],
    )
    assert len(growth) == len(control) == 66
    modulus = tool.face_minimum(control)
    assert modulus["exact"] is True
    assert ir.decimal(field, modulus["lower"]).startswith(tool.RHO_ROW_DECIMAL)
    assert tool.face_minimum(growth)["exact"] is True
    assert ir.decimal(field, tool.face_minimum(growth)["lower"]).startswith(PINNED_G_0_DECIMAL)
    check = tool.domination(growth, control)
    assert check["comparable_faces"] == 66
    assert check["route_radius_at_most_modulus_upper"] == 66
    route = ir.exact_min(
        [face.route_radius for face in growth if face.route_radius is not None]
    )
    # The route's best certified radius is the BC-199 weighted modulus itself, reached on
    # the same face theta_10 = -1; it exceeds the retained rational only by its shortening.
    assert (route - modulus["lower"]).is_zero()
    assert 0 < float(ir.rational_lower(field, route) - tool.RHO_ROW) < 1e-12

    # Along that exact argmin direction, every row's jet reproduces the retained row and
    # 36 of the 42 rows decrease with a nonpositive exact second-order term: the uniform
    # remainder model, which lets each of them recover at t*, is what binds.
    argmin = next(face for face in control if face.coordinate == 32 and face.sign == -1)
    assert argmin.point is not None
    detail = tool.directional_curvature(witness(), rows, curvature, argmin.point)
    assert len(detail["rows"]) == tc.EXPECTED_BRANCH_ROWS
    assert detail["decreasing_rows_never_recovering_to_second_order"] == 36
    assert detail["second_order_exclusion_unbounded"] is True
    assert detail["largest_quadratic_over_half_K_float"] < 1.0

    # The jet refusals reuse the same exact branch-0 system rather than paying for it in a
    # test of their own, which would sit below the slow floor in the lane that already
    # built it.
    jets = tool.row_jets(witness(), rows[:3])
    assert all(jet.dimension == tool.VARIABLES for jet in jets)
    scaled = LinearRow(rows[0].label, tuple(value + value for value in rows[0].coefficients))
    with pytest.raises(tool.CaptureRadiusError, match="gradient"):
        tool.row_jets(witness(), (scaled,))
    with pytest.raises(tool.CaptureRadiusError, match="unrecognised"):
        tool.row_jets(witness(), (LinearRow("bound:0", rows[0].coefficients),))
    assert field.degree == 8
