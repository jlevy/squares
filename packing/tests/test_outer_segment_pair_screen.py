"""Known-answer controls for the exact outer-segment owner-pair screen."""

from __future__ import annotations

from fractions import Fraction
from itertools import product

import pytest

from devtools import outer_segment_pair_screen as screen_module
from devtools.outer_segment_pair_screen import LEFT_M, LOWER, RHO, UPPER, Q, screen

Point = tuple[Fraction, Fraction]
Vector = tuple[Fraction, Fraction]


def _dot(left: Vector, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _axes(tangent: Fraction) -> tuple[Vector, Vector]:
    denominator = 1 + tangent * tangent
    u = ((1 - tangent * tangent) / denominator, 2 * tangent / denominator)
    return u, (-u[1], u[0])


def _centre(u: Vector, w: Vector, w_sign: int) -> Point:
    return (
        LEFT_M[0] + (u[0] + w_sign * w[0]) / 2,
        LEFT_M[1] + (u[1] + w_sign * w[1]) / 2,
    )


def _corners(centre: Point, u: Vector, w: Vector) -> list[Point]:
    half = Fraction(1, 2)
    return [
        (centre[0] + a * u[0] + b * w[0], centre[1] + a * u[1] + b * w[1])
        for a, b in product((-half, half), repeat=2)
    ]


def _anchor_clearance(centre: Point, anchor: Point, axes: tuple[Vector, Vector]) -> Fraction:
    relative = anchor[0] - centre[0], anchor[1] - centre[1]
    return min(Fraction(1, 2) - abs(_dot(axis, relative)) for axis in axes)


def test_touching_axis_pair_survives_as_unresolved() -> None:
    result = screen(Fraction(0), Fraction(0))
    surviving = [
        branch
        for branch in result["branches"]
        if branch["status"] == "survives_necessary_relaxation"
    ]
    assert result["verdict"] == "unresolved"
    assert surviving
    for branch in surviving:
        assert Fraction(branch["extrema"]["alpha_min"]) <= Fraction(
            branch["extrema"]["beta_max"]
        )
    assert not result["packing_certificate"]


def test_plain_integer_angles_are_normalized_exactly() -> None:
    integer = screen(0, 0)
    rational = screen(Fraction(0), Fraction(0))
    assert integer["inputs"] == rational["inputs"]
    assert integer["branches"] == rational["branches"]
    assert integer["method"]["arithmetic"] == "exact_rational"


@pytest.mark.parametrize("value", [0.0, 0.4, True])
def test_inexact_or_boolean_angle_arguments_are_rejected_before_screening(
    value: object,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def forbidden(*_args: object) -> None:
        raise AssertionError("polygon construction must not receive an inexact angle")

    monkeypatch.setattr(screen_module, "_domain", forbidden)
    with pytest.raises(TypeError, match="Fraction or plain integer"):
        screen(value, Fraction(0))  # type: ignore[arg-type]


@pytest.mark.parametrize("t2", [Fraction(2, 5), Fraction(-2, 5)])
def test_steep_pairs_are_excluded(t2: Fraction) -> None:
    result = screen(Fraction(2, 5), t2)
    assert result["verdict"] == "excluded"
    assert all(branch["status"] == "impossible" for branch in result["branches"])


@pytest.mark.parametrize("tangent", [Fraction(1, 4), Fraction(-1, 4)])
def test_same_sign_quarter_turn_witnesses_survive(tangent: Fraction) -> None:
    axes = _axes(tangent)
    lower_centre = _centre(*axes, -1)
    upper_centre = _centre(*axes, 1)
    lower_corners = _corners(lower_centre, *axes)
    upper_corners = _corners(upper_centre, *axes)
    corners = lower_corners + upper_corners

    assert screen(tangent, tangent)["verdict"] == "unresolved"
    assert _dot(axes[1], lower_centre) + Fraction(1, 2) == _dot(
        axes[1], upper_centre
    ) - Fraction(1, 2)
    assert LEFT_M in lower_corners
    assert LEFT_M in upper_corners
    assert all(0 <= coordinate <= Q for corner in corners for coordinate in corner)
    assert min(
        _anchor_clearance(lower_centre, LOWER, axes),
        _anchor_clearance(upper_centre, UPPER, axes),
    ) >= Fraction(33, 425)
    assert Fraction(33, 425) > RHO


def test_mixed_quarter_turn_witness_touches_at_segment_midpoint() -> None:
    lower_axes, upper_axes = _axes(Fraction(-1, 4)), _axes(Fraction(1, 4))
    lower_centre = _centre(*lower_axes, -1)
    upper_centre = _centre(*upper_axes, 1)
    lower_corners = _corners(lower_centre, *lower_axes)
    upper_corners = _corners(upper_centre, *upper_axes)

    assert screen(Fraction(-1, 4), Fraction(1, 4))["verdict"] == "unresolved"
    assert max(point[1] for point in lower_corners) == LEFT_M[1]
    assert min(point[1] for point in upper_corners) == LEFT_M[1]
    assert LEFT_M in lower_corners
    assert LEFT_M in upper_corners
    assert min(
        _anchor_clearance(lower_centre, LOWER, lower_axes),
        _anchor_clearance(upper_centre, UPPER, upper_axes),
    ) >= Fraction(33, 425)


@pytest.mark.parametrize("tangent", [Fraction(1, 3), Fraction(-1, 3)])
def test_third_turn_pairs_are_excluded_by_exact_clipping(tangent: Fraction) -> None:
    assert screen(tangent, tangent)["verdict"] == "excluded"


def test_positive_third_turn_has_the_exact_upper_domain_contradiction() -> None:
    result = screen(Fraction(1, 3), Fraction(1, 3))
    branch = next(item for item in result["branches"] if item["normal"] == ["-3/5", "4/5"])
    inequalities = {item["reason"]: item for item in branch["owner2"]["inequalities"]}

    assert branch["owner2"]["vertices"] == []
    assert inequalities["container_left"]["upper"] == "-7/10"
    assert inequalities["owner_tube_edge_u_upper"]["upper"] == "213/100"
    assert inequalities["branch_beta_lower"]["upper"] == "-419/250"
    bound = Fraction(27, 50) + Fraction(4, 5) * Fraction(23, 500)
    bound += Fraction(3, 5) * Fraction(9, 250)
    assert bound == Fraction(374, 625)
    assert Fraction(3, 5) - bound == Fraction(1, 625)


def test_right_segment_is_the_exact_reflection_of_left() -> None:
    left = screen(Fraction(1, 5), Fraction(-1, 4), "left")
    right = screen(Fraction(-1, 5), Fraction(1, 4), "right")
    right_status = {
        tuple(Fraction(value) for value in branch["normal"]): branch["status"]
        for branch in right["branches"]
    }
    assert right["verdict"] == left["verdict"]
    for branch in left["branches"]:
        x, y = (Fraction(value) for value in branch["normal"])
        assert right_status[-x, y] == branch["status"]


def test_record_declares_exact_complete_nonsampling_relaxation() -> None:
    result = screen(Fraction(0), Fraction(0))
    method = result["method"]
    assert method == {
        "arithmetic": "exact_rational",
        "branch_enumeration": "complete_signed_edge_normals",
        "sampling": False,
        "floating_point": False,
        "relaxation": "necessary_only",
    }
    assert result["inputs"]["t1"]["owner"] == "lower_anchor"
    assert result["inputs"]["t2"]["owner"] == "upper_anchor"


@pytest.mark.parametrize("tangent", [Fraction(1, 2), Fraction(-1, 2)])
def test_folded_angle_guard_refuses_invalid_half_tangent(tangent: Fraction) -> None:
    with pytest.raises(ValueError, match="folded-angle guard"):
        screen(tangent, Fraction(0))
