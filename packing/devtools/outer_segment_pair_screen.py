"""Exact necessary screen with t1 owning the lower and t2 the upper E4 anchor."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path
from typing import Any, Literal

from sqpack.cover import write_text_atomic

Point = tuple[Fraction, Fraction]
Vector = tuple[Fraction, Fraction]
Inequality = tuple[Fraction, Fraction, Fraction, str]
Segment = Literal["left", "right"]

ZERO = Fraction(0)
ONE = Fraction(1)
Q = Fraction(96, 25)
ELL = Fraction(1, 10)
DELTA = Fraction(3, 500)
RHO = Fraction(1, 1000)
LEFT_M = (Fraction(27, 50), Fraction(48, 25))
LOWER = (Fraction(9, 10), Fraction(41, 25))
UPPER = (Fraction(9, 10), Fraction(11, 5))


def _dot(left: Vector, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _axes(tangent: Fraction) -> tuple[Vector, Vector]:
    denominator = 1 + tangent * tangent
    u = ((1 - tangent * tangent) / denominator, 2 * tangent / denominator)
    return u, (-u[1], u[0])


def _support(axes: tuple[Vector, Vector], normal: Vector) -> Fraction:
    return (abs(_dot(normal, axes[0])) + abs(_dot(normal, axes[1]))) / 2


def _slab(
    inequalities: list[Inequality],
    normal: Vector,
    centre: Point,
    radius: Fraction,
    label: str,
) -> None:
    middle = _dot(normal, centre)
    x, y = normal
    inequalities.extend(
        (
            (x, y, middle + radius, label + "_upper"),
            (-x, -y, -middle + radius, label + "_lower"),
        )
    )


def _clip(polygon: list[Point], inequality: Inequality) -> list[Point]:
    a, b, bound, _label = inequality
    if not polygon:
        return []
    output: list[Point] = []
    previous = polygon[-1]
    previous_value = a * previous[0] + b * previous[1]
    previous_inside = previous_value <= bound
    for current in polygon:
        current_value = a * current[0] + b * current[1]
        current_inside = current_value <= bound
        if current_inside != previous_inside:
            ratio = (bound - previous_value) / (current_value - previous_value)
            output.append(
                (
                    previous[0] + ratio * (current[0] - previous[0]),
                    previous[1] + ratio * (current[1] - previous[1]),
                )
            )
        if current_inside:
            output.append(current)
        previous, previous_value, previous_inside = current, current_value, current_inside
    return output


def _polygon(inequalities: list[Inequality]) -> list[Point]:
    polygon = [(ZERO, ZERO), (Q, ZERO), (Q, Q), (ZERO, Q)]
    for inequality in inequalities:
        polygon = _clip(polygon, inequality)
    return polygon


def _domain(
    tangent: Fraction, anchor: Point, middle: Point
) -> tuple[tuple[Vector, Vector], list[Inequality]]:
    axes = _axes(tangent)
    h = (abs(axes[0][0]) + abs(axes[0][1])) / 2
    inequalities: list[Inequality] = [
        (-ONE, ZERO, -h, "container_left"),
        (ONE, ZERO, Q - h, "container_right"),
        (ZERO, -ONE, -h, "container_bottom"),
        (ZERO, ONE, Q - h, "container_top"),
    ]
    for label, normal in (
        ("axis_x", (ONE, ZERO)),
        ("axis_y", (ZERO, ONE)),
        ("edge_u", axes[0]),
        ("edge_w", axes[1]),
    ):
        radius = _support(axes, normal) + ELL * abs(normal[0]) / 2 + DELTA
        _slab(inequalities, normal, middle, radius, "owner_tube_" + label)
    for label, normal in (("u", axes[0]), ("w", axes[1])):
        _slab(inequalities, normal, anchor, Fraction(1, 2) - RHO, "anchor_" + label)
    return axes, inequalities


def _records(inequalities: list[Inequality], polygon: list[Point]) -> dict[str, Any]:
    return {
        "inequalities": [
            {"a": str(a), "b": str(b), "upper": str(bound), "reason": reason}
            for a, b, bound, reason in inequalities
        ],
        "vertices": [[str(x), str(y)] for x, y in polygon],
    }


def _reflected(point: Point) -> Point:
    return Q - point[0], point[1]


def _fraction(value: Fraction | int, name: str) -> Fraction:
    if isinstance(value, bool):
        raise TypeError(f"{name} must be a Fraction or plain integer")
    if isinstance(value, Fraction):
        return value
    if isinstance(value, int):
        return Fraction(value)
    raise TypeError(f"{name} must be a Fraction or plain integer")


def screen(t1: Fraction | int, t2: Fraction | int, segment: Segment = "left") -> dict[str, Any]:
    """Screen the ordered lower-t1/upper-t2 owners; unordered callers run both orders."""
    t1, t2 = _fraction(t1, "t1"), _fraction(t2, "t2")
    for tangent in (t1, t2):
        if tangent * tangent + 2 * abs(tangent) - 1 > 0:
            raise ValueError("half-tangent violates the folded-angle guard")
    if segment not in ("left", "right"):
        raise ValueError("segment must be 'left' or 'right'")
    middle, lower, upper = LEFT_M, LOWER, UPPER
    if segment == "right":
        middle, lower, upper = map(_reflected, (middle, lower, upper))
    axes1, base1 = _domain(t1, lower, middle)
    axes2, base2 = _domain(t2, upper, middle)
    normals: list[Vector] = []
    for axis in (*axes1, *axes2):
        for normal in (axis, (-axis[0], -axis[1])):
            if normal not in normals:
                normals.append(normal)

    branches: list[dict[str, Any]] = []
    for normal in normals:
        h1, h2 = _support(axes1, normal), _support(axes2, normal)
        middle_value = _dot(normal, middle)
        radius = ELL * abs(normal[0]) / 2 + DELTA
        lower1, upper1 = middle_value - radius - h1, middle_value + radius - h1
        lower2, upper2 = middle_value - radius + h2, middle_value + radius + h2
        extra1 = [
            (normal[0], normal[1], upper1, "branch_alpha_upper"),
            (-normal[0], -normal[1], -lower1, "branch_alpha_lower"),
        ]
        extra2 = [
            (normal[0], normal[1], upper2, "branch_beta_upper"),
            (-normal[0], -normal[1], -lower2, "branch_beta_lower"),
        ]
        polygon1, polygon2 = _polygon(base1 + extra1), _polygon(base2 + extra2)
        alpha_min = min((_dot(normal, point) + h1 for point in polygon1), default=None)
        beta_max = max((_dot(normal, point) - h2 for point in polygon2), default=None)
        reasons = []
        if not polygon1:
            reasons.append("lower_anchor_owner_domain_empty")
        if not polygon2:
            reasons.append("upper_anchor_owner_domain_empty")
        if alpha_min is not None and beta_max is not None and alpha_min > beta_max:
            reasons.append("strict_support_order_gap")
        survives = not reasons
        branches.append(
            {
                "normal": [str(value) for value in normal],
                "support_half_widths": [str(h1), str(h2)],
                "segment_projection": {"middle": str(middle_value), "radius": str(radius)},
                "owner1": _records(base1 + extra1, polygon1),
                "owner2": _records(base2 + extra2, polygon2),
                "extrema": {
                    "alpha_min": None if alpha_min is None else str(alpha_min),
                    "beta_max": None if beta_max is None else str(beta_max),
                },
                "status": "survives_necessary_relaxation" if survives else "impossible",
                "reasons": reasons,
            }
        )
    unresolved = any(branch["status"] == "survives_necessary_relaxation" for branch in branches)
    return {
        "schema": "outer-segment-pair-screen-v1",
        "target": {
            "q": str(Q),
            "square_side": "1",
            "segment": segment,
            "middle": [str(value) for value in middle],
            "length": str(ELL),
            "tube_delta": str(DELTA),
            "anchor_radius": str(RHO),
            "anchors": [[str(value) for value in point] for point in (lower, upper)],
        },
        "inputs": {
            "t1": {"half_tangent": str(t1), "owner": "lower_anchor"},
            "t2": {"half_tangent": str(t2), "owner": "upper_anchor"},
            "ordering": "ordered; unordered callers must evaluate both assignments",
        },
        "method": {
            "arithmetic": "exact_rational",
            "branch_enumeration": "complete_signed_edge_normals",
            "sampling": False,
            "floating_point": False,
            "relaxation": "necessary_only",
        },
        "owners": [
            {"role": "lower_anchor_owner1", **_records(base1, _polygon(base1))},
            {"role": "upper_anchor_owner2", **_records(base2, _polygon(base2))},
        ],
        "branches": branches,
        "verdict": "unresolved" if unresolved else "excluded",
        "packing_certificate": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("t1", type=Fraction, help="half-tangent of the lower-anchor owner")
    parser.add_argument("t2", type=Fraction, help="half-tangent of the upper-anchor owner")
    parser.add_argument("--segment", choices=("left", "right"), default="left")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    record = screen(args.t1, args.t2, args.segment)
    text = json.dumps(record, indent=1) + "\n"
    if args.out is None:
        print(text, end="")
    else:
        write_text_atomic(args.out, text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
