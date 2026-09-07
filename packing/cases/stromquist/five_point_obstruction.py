"""Construct an exact square escaping at most five rational sites in [0,3]^2.

The continuum proof and compactness argument are in the dated obstruction review.
This control checks supplied point sets, exact square geometry, and strict separation;
it does not turn finite input tests into a proof for all real point sets.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from itertools import pairwise, product
from pathlib import Path

from sqpack.cover import write_text_atomic

type Point = tuple[Fraction, Fraction]
type Polygon = tuple[Point, ...]

SVG_ARTIFACT = Path(__file__).with_name("five-point-obstruction.svg")

BOTTOM_DIAMOND: Polygon = (
    (Fraction(3, 2), Fraction(0)),
    (Fraction(9, 4), Fraction(3, 4)),
    (Fraction(3, 2), Fraction(3, 2)),
    (Fraction(3, 4), Fraction(3, 4)),
)
AXIS_SIDE = Fraction(101, 100)
DIAMOND_RADIUS = Fraction(143, 200)
INNER_CORNERS: tuple[Point, ...] = tuple(
    (Fraction(x), Fraction(y)) for x, y in product((1, 2), repeat=2)
)


def _subtract(left: Point, right: Point) -> Point:
    return left[0] - right[0], left[1] - right[1]


def _dot(left: Point, right: Point) -> Fraction:
    return left[0] * right[0] + left[1] * right[1]


def _cross(left: Point, right: Point) -> Fraction:
    return left[0] * right[1] - left[1] * right[0]


def _validate_points(points: tuple[Point, ...]) -> None:
    if any(
        not isinstance(point, tuple)
        or len(point) != 2
        or any(not isinstance(value, Fraction) for value in point)
        for point in points
    ):
        raise ValueError("each point must be a pair of Fraction coordinates")


def verify_escape(vertices: Polygon, points: tuple[Point, ...]) -> tuple[Fraction, ...]:
    """Reject invalid geometry or a point on/in the closed square; return margins.

    A margin is the largest outward edge determinant for that point. Strict
    positivity certifies separation from a closed convex polygon, without a tolerance.
    """
    _validate_points(vertices)
    _validate_points(points)
    if len(vertices) != 4:
        raise ValueError("a square requires four vertices")
    edges = tuple(
        _subtract(b, a) for a, b in zip(vertices, (*vertices[1:], vertices[0]), strict=True)
    )
    side_squared = _dot(edges[0], edges[0])
    if side_squared < AXIS_SIDE**2 or any(_dot(edge, edge) != side_squared for edge in edges):
        raise ValueError("the four sides must be equal and at least 101/100 long")
    for left, right in zip(edges, (*edges[1:], edges[0]), strict=True):
        if _dot(left, right) != 0 or _cross(left, right) <= 0:
            raise ValueError("vertices must describe a counterclockwise square")
    if any(not 0 <= coordinate <= 3 for vertex in vertices for coordinate in vertex):
        raise ValueError("the closed square is not contained in [0,3]^2")
    margins = tuple(
        max(
            -_cross(edge, _subtract(point, vertex))
            for vertex, edge in zip(vertices, edges, strict=True)
        )
        for point in points
    )
    if any(margin <= 0 for margin in margins):
        raise ValueError("a supplied point lies on or inside the closed square")
    return margins


@dataclass(frozen=True)
class Escape:
    branch: str
    vertices: Polygon

    def record(self, points: tuple[Point, ...]) -> dict[str, object]:
        """Recheck the returned witness before serializing its rational values."""
        margins = verify_escape(self.vertices, points)
        edge = _subtract(self.vertices[1], self.vertices[0])
        return {
            "branch": self.branch,
            "points": [[str(x), str(y)] for x, y in points],
            "closed_square_vertices": [[str(x), str(y)] for x, y in self.vertices],
            "side_squared": str(_dot(edge, edge)),
            "outward_determinant_margins": [str(margin) for margin in margins],
        }


def _event_representatives(coordinates: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    """One representative of every face of the exact side-a translation partition."""
    high = 3 - AXIS_SIDE
    cuts = sorted(
        {Fraction(0), high}
        | {
            event
            for value in coordinates
            for event in (value - AXIS_SIDE, value)
            if 0 <= event <= high
        }
    )
    return tuple(sorted((*cuts, *((left + right) / 2 for left, right in pairwise(cuts)))))


def _empty_axis_square(points: tuple[Point, ...]) -> Point | None:
    axes = tuple(
        _event_representatives(tuple(point[axis] for point in points)) for axis in (0, 1)
    )
    for x, y in product(*axes):
        if all(
            not (x <= px <= x + AXIS_SIDE and y <= py <= y + AXIS_SIDE) for px, py in points
        ):
            return x, y
    return None


def axis_square(lower: Point) -> Polygon:
    """A closed side-a square, with container-wall contact allowed."""
    _validate_points((lower,))
    if any(not 0 <= value <= 3 - AXIS_SIDE for value in lower):
        raise ValueError("the square's lower corner must lie in [0,3-a]^2")
    x, y = lower
    return (
        (x, y),
        (x + AXIS_SIDE, y),
        (x + AXIS_SIDE, y + AXIS_SIDE),
        (x, y + AXIS_SIDE),
    )


def diamond_witnesses() -> tuple[Polygon, ...]:
    """Four fixed closed diamonds of L1 radius 143/200 and side greater than a."""
    polygon = BOTTOM_DIAMOND
    scale = DIAMOND_RADIUS / Fraction(3, 4)
    diamonds: list[Polygon] = []
    for _ in range(4):
        center = tuple(
            sum((vertex[axis] for vertex in polygon), Fraction(0)) / 4 for axis in (0, 1)
        )
        diamonds.append(
            tuple(
                (center[0] + scale * (x - center[0]), center[1] + scale * (y - center[1]))
                for x, y in polygon
            )
        )
        polygon = tuple((3 - y, x) for x, y in polygon)
    return tuple(diamonds)


def escape_square(points: tuple[Point, ...]) -> Escape:
    """Find and verify a strict closed-square escape for a finite rational input.

    Site membership is constant on each product of translation-event strata, so
    the axis branch is exhaustive over that continuum, including boundaries.
    If every side-a axis square is hit, the proof supplies one of four diamond escapes.
    """
    _validate_points(points)
    points = tuple(dict.fromkeys(points))
    if len(points) > 5 or any(not 0 <= value <= 3 for point in points for value in point):
        raise ValueError("supply at most five distinct points in [0,3]^2")
    lower = _empty_axis_square(points)
    if lower is not None:
        witness = Escape("axis-side-101/100", axis_square(lower))
        verify_escape(witness.vertices, points)
        return witness
    for index, vertices in enumerate(diamond_witnesses()):
        try:
            verify_escape(vertices, points)
        except ValueError:
            continue
        return Escape(f"diamond-{index}", vertices)
    raise ValueError("the constructive five-point obstruction failed")


def control_record() -> dict[str, object]:
    """Retain exact controls for the arbitrary-site and symmetric arguments."""
    controls = {
        "empty": (),
        "container_corners_and_center": (
            *((Fraction(x), Fraction(y)) for x, y in product((0, 3), repeat=2)),
            (Fraction(3, 2), Fraction(3, 2)),
        ),
        "inner_corners_and_center": (*INNER_CORNERS, (Fraction(3, 2), Fraction(3, 2))),
        "inner_corners_and_edge": (*INNER_CORNERS, (Fraction(3, 2), Fraction(1, 2))),
        "asymmetric_edge_allocation": (
            (Fraction(99, 100), Fraction(1)),
            (Fraction(201, 100), Fraction(1)),
            (Fraction(1), Fraction(2)),
            (Fraction(2), Fraction(2)),
            (Fraction(7, 5), Fraction(1)),
        ),
    }
    # Affine functions nonnegative at all vertices are positive in the interior
    # unless identically zero. These separate the whole diagonal/midline families.
    diagonal_ranges = (
        tuple(x - y for x, y in BOTTOM_DIAMOND),
        tuple(3 - x - y for x, y in BOTTOM_DIAMOND),
    )
    if any(min(values) != 0 or max(values) <= 0 for values in diagonal_ranges):
        raise ValueError("the open diamond does not strictly avoid both diagonals")
    midline_square = (
        (Fraction(0), Fraction(0)),
        (Fraction(3, 2), Fraction(0)),
        (Fraction(3, 2), Fraction(3, 2)),
        (Fraction(0), Fraction(3, 2)),
    )
    midline_ranges = (
        tuple(Fraction(3, 2) - x for x, _ in midline_square),
        tuple(Fraction(3, 2) - y for _, y in midline_square),
    )
    if any(min(values) != 0 or max(values) <= 0 for values in midline_ranges):
        raise ValueError("the open axis square does not strictly avoid both midlines")
    verify_escape(BOTTOM_DIAMOND, ())
    verify_escape(midline_square, ())
    diamond_edge = _subtract(BOTTOM_DIAMOND[1], BOTTOM_DIAMOND[0])
    midline_edge = _subtract(midline_square[1], midline_square[0])
    if _dot(diamond_edge, diamond_edge) != Fraction(9, 8):
        raise ValueError("the diagonal witness has an unexpected side length")
    if _dot(midline_edge, midline_edge) != Fraction(9, 4):
        raise ValueError("the midline witness has an unexpected side length")
    wall_points = ((Fraction(3, 2), Fraction(3, 2)),)
    upper_wall = Escape(
        "axis-square-at-upper-walls",
        axis_square((3 - AXIS_SIDE, 3 - AXIS_SIDE)),
    )
    return {
        "schema_version": 1,
        "scope": "exact-witness-controls-for-five-unweighted-sites",
        "continuum_proof": "docs/project/reviews/review-2026-09-07-n6-pure-dots-obstruction.md",
        "new_packing_bound": False,
        "minimum_escape_side": str(AXIS_SIDE),
        "diamond_side_squared": str(2 * DIAMOND_RADIUS**2),
        "diamond_squared_gap_over_minimum": str(2 * DIAMOND_RADIUS**2 - AXIS_SIDE**2),
        "controls": {
            **{name: escape_square(points).record(points) for name, points in controls.items()},
            "upper_wall_axis_square": upper_wall.record(wall_points),
        },
        "symmetric_open_witnesses": {
            "diagonal_side_squared": "9/8",
            "midline_side_squared": "9/4",
            "diagonal_separating_forms_at_vertices": [
                [str(value) for value in values] for values in diagonal_ranges
            ],
            "midline_separating_forms_at_vertices": [
                [str(value) for value in values] for values in midline_ranges
            ],
        },
    }


def _parse_point(value: str) -> Point:
    try:
        x, y = value.split(",")
        return Fraction(x), Fraction(y)
    except ValueError, ZeroDivisionError:
        raise argparse.ArgumentTypeError(
            "use two exact rational coordinates: --point 1/2,2"
        ) from None


def escape_svg(points: tuple[Point, ...], escape: Escape) -> str:
    """Render already verified geometry; floating conversion is presentation only."""
    verify_escape(escape.vertices, points)

    def display(point: Point) -> tuple[float, float]:
        return 45 + 170 * float(point[0]), 565 - 170 * float(point[1])

    polygon = " ".join(f"{x:.6f},{y:.6f}" for x, y in map(display, escape.vertices))
    marks = "\n".join(
        f'<circle cx="{x:.6f}" cy="{y:.6f}" r="3.5" fill="#b72d4b" stroke="white"/>'
        for x, y in map(display, points)
    )
    edge = _subtract(escape.vertices[1], escape.vertices[0])
    side_squared = _dot(edge, edge)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 650">
  <title>A closed square escaping the supplied dots in a side-three container</title>
  <rect width="600" height="650" fill="white"/>
  <g font-family="system-ui, sans-serif" fill="#263139">
    <text x="45" y="30" font-size="20">What {len(points)} dots miss</text>
    <rect x="45" y="55" width="510" height="510" fill="#f7f8fa" stroke="#52616c"/>
    <path d="M45 55L555 565M45 565L555 55" stroke="#d4d9de" stroke-dasharray="5 5"/>
    <polygon points="{polygon}" fill="#d1eee2" stroke="#1b7252" stroke-width="2"/>
    {marks}
    <text x="45" y="600" font-size="16">Closed escaping square: side² = {side_squared}</text>
    <text x="45" y="627" font-size="14">
      Container side 3. Every dot lies strictly outside the green square.
    </text>
  </g>
</svg>
'''


def control_svg() -> str:
    """Rebuild the retained central five-site drawing from the exact constructor."""
    points = (*INNER_CORNERS, (Fraction(3, 2), Fraction(3, 2)))
    return escape_svg(points, escape_square(points))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--point", action="append", type=_parse_point, default=None)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--svg", type=Path, help="render the supplied sites, or the central control"
    )
    args = parser.parse_args()
    points: tuple[Point, ...] | None = None if args.point is None else tuple(args.point)
    record = control_record() if points is None else escape_square(points).record(points)
    rendered = json.dumps(record, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        write_text_atomic(args.output, rendered)
    if args.svg is not None:
        drawing = control_svg() if points is None else escape_svg(points, escape_square(points))
        write_text_atomic(args.svg, drawing)
    print(rendered, end="")


if __name__ == "__main__":
    main()
