"""Exact audit of Friedman's DS7 Theorem 2: four unavoidable points give `s(5) >= 2 + 1/sqrt 2`.

Source: `resources/papers/friedman-ds7-packing-unit-squares-in-squares.md`, section 4
(Lemmas 1 to 3) and section 5 (the shrinking argument and Theorem 2). Figure 24 is not
extractable, but the proof's sentence fixes the partition: with `a = 1/sqrt 2` and the
container `[0, 2 + a]^2`, the set

    P = {(1, 1), (1, 1 + a), (1 + a, 1), (1 + a, 1 + a)}

is unavoidable "from Lemma 1 if the center of the square is in a corner, from Lemma 2 if
it is near a side, and from Lemma 3 if it is in a triangle". The ten cells are the four
corner unit squares, the four wall rectangles of width `a` along their wall and depth 1,
and the central `a x a` square cut by its diagonal into two triangles of legs `a` and
hypotenuse 1.

What is decided here, by exact sign in `Q(sqrt 2)` with no tolerance:

- the field's contract: `x^2 - 2` irreducible and squarefree, `(1, 2)` isolating its
  positive root;
- the ten cells exactly tile the container (areas, incidences, noncrossing, Euler
  characteristic, every boundary edge on a container wall);
- each corner cell is the unit square at its container corner, and its out is the inner
  corner, a point of `P` (Lemma 1, in the corner's frame);
- each wall cell is a rectangle on its wall of width `x` and depth `y` with
  `0 < x <= 1`, `0 < y <= 1` and `x + 2y < 2 sqrt 2`, and both its outs, the inner
  corners, are points of `P` (Lemma 2, in the wall's frame). The lowest-corner function
  of Lemma 2's proof, `f = t - x (t^2 - 1)/2` over `t = sin + cos` in `[1, sqrt 2]`, is
  evaluated at both ends of that interval, where its minimum lies since it is concave
  in `t`; the record keeps both values and the margin over `y`;
- each triangle has its three vertices in `P` and every side of squared length at most
  one (Lemma 3);
- every point of `P` is charged by some cell, and the pigeonhole count: four points,
  five squares.

What is cited rather than proved: the statements of Lemmas 1 to 3, the reduction steps
of their proofs, and section 5's shrinking argument, which turns "every unit square in
the container contains a point of `P`, possibly on its boundary" into "five unit
squares do not pack in any smaller square". The frames are the container's own
isometries taking the cell's corner to the origin or its wall to the axis, so a unit
square inside the container lies inside the quadrant or half-plane each lemma assumes.

Usage, from `packing/`:
    uv run --frozen python -m cases.friedman5.verify_cover
    uv run --frozen python -m cases.friedman5.verify_cover \
        --check cases/friedman5/certificate.json

`--out PATH` writes the record instead, which is how `certificate.json` was made.
"""

from __future__ import annotations

import argparse
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from sqpack import retained_json
from sqpack.cover import (
    Face,
    Point,
    checked_number_field,
    polygon_area2,
    triangle_edge_certificate,
    validate_square_tiling,
)
from sqpack.field import FieldElement, NumberField

#: sqrt 2 generates the field: `x^2 - 2`, its positive root isolated by `(1, 2)`.
MIN_POLY = (1, 0, -2)
ISOLATING = (1, 2)
EXPECTED_POINTS = 4
EXPECTED_FACES = 4 + 4 + 2
SQUARES = 5
SOURCE = "resources/papers/friedman-ds7-packing-unit-squares-in-squares.md"
RECORD = Path(__file__).with_name("certificate.json")

type Frame = Callable[[Point], Point]


class CoverCertificateError(ValueError):
    """A premise the construction fails exactly; the message names the cell."""


@dataclass(frozen=True)
class Cell:
    """One cell of the cover: its counterclockwise face, its lemma and that lemma's frame."""

    face: Face
    kind: str
    frame: str
    outs: tuple[str, ...]


@dataclass(frozen=True)
class Cover:
    """The construction: its field, side, the points of `P`, every vertex and the cells."""

    field: NumberField
    sqrt2: FieldElement
    offset: FieldElement
    gap: FieldElement
    side: FieldElement
    set_points: dict[str, Point]
    vertices: dict[str, Point]
    cells: dict[str, Cell]


def build(*, offset_shift: Fraction = Fraction(0), gap_shift: Fraction = Fraction(0)) -> Cover:
    """Friedman's construction, or a mutant of it.

    The points of `P` stand `offset` from the walls and `gap` apart, in a container of
    side `2 offset + gap`. Friedman's is `offset = 1`, `gap = 1/sqrt 2`; the shifts move
    either away from it, for the negative controls.
    """
    field, _checks = checked_number_field(MIN_POLY, ISOLATING)
    rational = field.rational
    sqrt2 = field.alpha
    if not (sqrt2 * sqrt2 - rational(2)).is_zero() or sqrt2.sign() <= 0:
        raise CoverCertificateError("the generator is not the positive square root of 2")
    offset = rational(1) + rational(offset_shift)
    gap = sqrt2 / 2 + rational(gap_shift)
    side = 2 * offset + gap
    zero = rational(0)
    near, far = offset, offset + gap

    set_points: dict[str, Point] = {
        "p11": (near, near),
        "p12": (near, far),
        "p21": (far, near),
        "p22": (far, far),
    }
    vertices: dict[str, Point] = dict(set_points)
    vertices |= {
        "c_bl": (zero, zero),
        "c_br": (side, zero),
        "c_tl": (zero, side),
        "c_tr": (side, side),
        "b1": (near, zero),
        "b2": (far, zero),
        "t1": (near, side),
        "t2": (far, side),
        "l1": (zero, near),
        "l2": (zero, far),
        "r1": (side, near),
        "r2": (side, far),
    }

    def oriented(face: Face) -> Face:
        area2 = polygon_area2(tuple(vertices[name] for name in face))
        if area2.sign() == 0:
            raise CoverCertificateError(f"degenerate face: {face}")
        return face if area2.sign() > 0 else tuple(reversed(face))

    plan = {
        "corner_bl": (("c_bl", "b1", "p11", "l1"), "lemma1", "bottom-left", ("p11",)),
        "corner_br": (("b2", "c_br", "r1", "p21"), "lemma1", "bottom-right", ("p21",)),
        "corner_tl": (("l2", "p12", "t1", "c_tl"), "lemma1", "top-left", ("p12",)),
        "corner_tr": (("p22", "r2", "c_tr", "t2"), "lemma1", "top-right", ("p22",)),
        "wall_bottom": (("b1", "b2", "p21", "p11"), "lemma2", "bottom", ("p11", "p21")),
        "wall_top": (("p12", "p22", "t2", "t1"), "lemma2", "top", ("p12", "p22")),
        "wall_left": (("l1", "p11", "p12", "l2"), "lemma2", "left", ("p11", "p12")),
        "wall_right": (("p21", "r1", "r2", "p22"), "lemma2", "right", ("p21", "p22")),
        "triangle_low": (("p11", "p21", "p22"), "lemma3", "none", ("p11", "p21", "p22")),
        "triangle_high": (("p11", "p22", "p12"), "lemma3", "none", ("p11", "p22", "p12")),
    }
    cells = {
        name: Cell(face=oriented(face), kind=kind, frame=frame, outs=outs)
        for name, (face, kind, frame, outs) in plan.items()
    }
    return Cover(field, sqrt2, offset, gap, side, set_points, vertices, cells)


def corner_frames(side: FieldElement) -> dict[str, Frame]:
    """Isometries of the container taking each corner to the origin, its walls to the axes."""
    return {
        "bottom-left": lambda p: (p[0], p[1]),
        "bottom-right": lambda p: (side - p[0], p[1]),
        "top-left": lambda p: (p[0], side - p[1]),
        "top-right": lambda p: (side - p[0], side - p[1]),
    }


def wall_frames(side: FieldElement) -> dict[str, Frame]:
    """Isometries of the container taking each wall to the axis `v = 0`, the box to `v >= 0`."""
    return {
        "bottom": lambda p: (p[0], p[1]),
        "top": lambda p: (p[0], side - p[1]),
        "left": lambda p: (p[1], p[0]),
        "right": lambda p: (p[1], side - p[0]),
    }


def certify_corner(cover: Cover, name: str, cell: Cell) -> dict[str, object]:
    """Lemma 1: the cell is `[0, 1]^2` in its corner's frame, and its out is `(1, 1)`."""
    frame = corner_frames(cover.side)[cell.frame]
    local = {vertex: frame(cover.vertices[vertex]) for vertex in cell.face}
    one, zero = cover.field.one, cover.field.zero
    unit = {(zero, zero), (one, zero), (one, one), (zero, one)}
    found = {(u.text(), v.text()) for u, v in local.values()}
    if len(local) != 4 or found != {(u.text(), v.text()) for u, v in unit}:
        raise CoverCertificateError(f"{name}: not the unit square at its container corner")
    (out,) = cell.outs
    u, v = local[out]
    if not ((u - one).is_zero() and (v - one).is_zero()):
        raise CoverCertificateError(f"{name}: the out is not the corner cell's inner corner")
    if out not in cover.set_points:
        raise CoverCertificateError(f"{name}: the out {out} is not a point of P")
    return {"lemma": 1, "corner": cell.frame, "out": out}


def lemma2_angle_minimum(
    sqrt2: FieldElement, width: FieldElement, depth: FieldElement
) -> dict[str, object]:
    """The lowest corner of Lemma 2's proof against the wall, at every angle.

    With both reference points on the square's boundary at angle `theta`, the lowest
    corner sits `f - y` below the wall, `f = cos + sin - x sin cos`. In `t = sin + cos`,
    which runs over `[1, sqrt 2]` for `theta` in `[0, pi/2]`, `f = t - x (t^2 - 1)/2`,
    concave since `x > 0`, so its minimum over the interval is at an end: `f(1) = 1` at
    `theta = 0` and `pi/2`, `f(sqrt 2) = sqrt 2 - x/2` at `pi/4`. The corner reaches the
    wall at every angle when the smaller end is at least `y`.
    """
    at_axis = width.field.one
    at_diagonal = sqrt2 - width / 2
    least = at_axis if (at_axis - at_diagonal).sign() <= 0 else at_diagonal
    margin = least - depth
    if margin.sign() < 0:
        raise CoverCertificateError("Lemma 2's lowest corner stays above the wall")
    return {
        "f_at_t_1": at_axis.text(),
        "f_at_t_sqrt2": at_diagonal.text(),
        "minimum_at": "t = 1 (theta = 0, pi/2)"
        if least is at_axis
        else "t = sqrt 2 (theta = pi/4)",
        "minimum_minus_depth": margin.text(),
        "minimum_equals_depth": margin.is_zero(),
    }


def certify_wall(cover: Cover, name: str, cell: Cell) -> dict[str, object]:
    """Lemma 2: a rectangle on its wall, width `x <= 1`, depth `y <= 1`, `x + 2y < 2 sqrt 2`."""
    frame = wall_frames(cover.side)[cell.frame]
    local = {vertex: frame(cover.vertices[vertex]) for vertex in cell.face}
    us = sorted({u.text(): u for u, _v in local.values()}.values())
    vs = sorted({v.text(): v for _u, v in local.values()}.values())
    if len(local) != 4 or len(us) != 2 or len(vs) != 2:
        raise CoverCertificateError(
            f"{name}: not an axis-aligned rectangle in its wall's frame"
        )
    if not vs[0].is_zero():
        raise CoverCertificateError(f"{name}: the rectangle does not sit on its wall")
    width, depth = us[1] - us[0], vs[1]
    one = cover.field.one
    if width.sign() <= 0 or (one - width).sign() < 0:
        raise CoverCertificateError(f"{name}: Lemma 2 needs 0 < x <= 1")
    if depth.sign() <= 0 or (one - depth).sign() < 0:
        raise CoverCertificateError(f"{name}: Lemma 2 needs 0 < y <= 1")
    slack = 2 * cover.sqrt2 - (width + 2 * depth)
    if slack.sign() <= 0:
        raise CoverCertificateError(f"{name}: x + 2y is not below 2 sqrt 2")
    inner = {vertex for vertex, (_u, v) in local.items() if (v - depth).is_zero()}
    if set(cell.outs) != inner:
        raise CoverCertificateError(f"{name}: the outs are not the rectangle's inner corners")
    missing = [out for out in cell.outs if out not in cover.set_points]
    if missing:
        raise CoverCertificateError(f"{name}: an out is not a point of P: {missing}")
    return {
        "lemma": 2,
        "wall": cell.frame,
        "x": width.text(),
        "y": depth.text(),
        "two_sqrt2_minus_x_minus_2y": slack.text(),
        "outs": list(cell.outs),
        "lowest_corner": lemma2_angle_minimum(cover.sqrt2, width, depth),
    }


def certify_triangle(cover: Cover, name: str, cell: Cell) -> dict[str, object]:
    """Lemma 3: three points of `P`, every side of length at most one."""
    if any(vertex not in cover.set_points for vertex in cell.face):
        raise CoverCertificateError(f"{name}: a triangle vertex is not a point of P")
    try:
        sides = triangle_edge_certificate(cover.vertices, cell.face)
    except ValueError as error:
        raise CoverCertificateError(f"{name}: {error}") from error
    return {"lemma": 3, **sides}


def certify(cover: Cover) -> dict[str, object]:
    """Decide every premise of Theorem 2's proof for `cover`, or refuse with the cell."""
    if len(cover.set_points) != EXPECTED_POINTS:
        raise CoverCertificateError(f"expected {EXPECTED_POINTS} points of P")
    faces = tuple(cell.face for cell in cover.cells.values())
    try:
        tiling = validate_square_tiling(
            cover.vertices, faces, side=cover.side, expected_faces=EXPECTED_FACES
        )
    except ValueError as error:
        raise CoverCertificateError(f"tiling: {error}") from error
    deciders = {"lemma1": certify_corner, "lemma2": certify_wall, "lemma3": certify_triangle}
    cells = {name: deciders[cell.kind](cover, name, cell) for name, cell in cover.cells.items()}
    charged = {out for cell in cover.cells.values() for out in cell.outs}
    if charged != set(cover.set_points):
        raise CoverCertificateError(
            f"points never charged by any cell: {sorted(set(cover.set_points) - charged)}"
        )
    kinds = {kind: sum(cell.kind == kind for cell in cover.cells.values()) for kind in deciders}
    return {
        "kind": "friedman-ds7-theorem2-audit/v1",
        "theorem": "Friedman DS7 Theorem 2: s(5) = 2 + 1/sqrt(2), its lower half",
        "source": SOURCE,
        "field": {
            "generator": "alpha = sqrt(2)",
            "minimal_polynomial_high_to_low": list(MIN_POLY),
            "isolating_interval": [str(bound) for bound in ISOLATING],
            "serialization": "poly[c0,c1] = c0 + c1 sqrt(2)",
            "all_decisions": "exact signs in Q(sqrt 2)",
        },
        "container_side": cover.side.text(),
        "container_side_decimal_for_display_only": cover.field.decimal(cover.side, 20),
        "points": {
            name: [coordinate.text() for coordinate in point]
            for name, point in sorted(cover.set_points.items())
        },
        "tiling": tiling,
        "cells": cells,
        "cell_kinds": kinds,
        "every_point_charged": True,
        "pigeonhole": {
            "points": EXPECTED_POINTS,
            "squares": SQUARES,
            "claim": (
                "every unit square in the container contains a point of P, possibly on its "
                "boundary; by section 5's shrinking argument five unit squares with "
                "disjoint interiors fit in no square of side below 2 + 1/sqrt(2)"
            ),
        },
        "cited_not_reproved": [
            "Lemma 1 (Friedman DS7, section 4)",
            "Lemma 2 (Friedman DS7, section 4): its reduction to both points on the boundary",
            "Lemma 3 (Friedman DS7, section 4)",
            "Section 5's shrinking argument, after Stromquist",
        ],
    }


def record_text() -> str:
    """The retained record of Friedman's construction, as `--out` writes it."""
    return retained_json.dumps(certify(build()), sort_keys=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    parser.add_argument("--out", type=Path, help="write the record here")
    parser.add_argument("--check", type=Path, help="exit 1 unless the record here is replayed")
    args = parser.parse_args(argv)
    started = time.monotonic()
    record = certify(build())
    text = retained_json.dumps(record, sort_keys=True)
    elapsed = time.monotonic() - started
    print(f"container side {record['container_side_decimal_for_display_only']} = 2 + 1/sqrt 2")
    print(f"tiling: {EXPECTED_FACES} cells certified exactly over Q(sqrt 2)")
    print(f"cells: {record['cell_kinds']}")
    print(f"points charged: {EXPECTED_POINTS} of {EXPECTED_POINTS}")
    print(f"conclusion: {SQUARES} unit squares do not pack below side 2 + 1/sqrt 2")
    print(f"wall: {elapsed:.2f}s")
    if args.out is not None:
        args.out.write_text(text, encoding="utf-8")
        print(f"wrote {args.out}")
    if args.check is not None:
        if args.check.read_text(encoding="utf-8") != text:
            print(f"REPLAY MISMATCH: {args.check} is not this record", file=sys.stderr)
            return 1
        print(f"replayed {args.check} byte for byte")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
