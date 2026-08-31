"""Exact certificate for Bentz 2010, Figure 2: the base configuration of Theorem 9.

What is certified here, entirely by exact rational sign with no tolerance anywhere:

- the 30-cell complex exactly partitions `[0, 4]^2` (areas, incidences, noncrossing,
  boundary walk on the container walls);
- each Lemma 1 pentagon lies inside its corner's unit square, and both of its outs
  are set points on the boundary of the lemma's conclusion triangle (the corner
  images of the triangle spanned by `(1, 1)`, `(0.9, 1)`, `(1, 0.9)`), so a box
  centred in the pentagon -- which, being open inside the container, never meets the
  corner's wall axes -- contains both;
- each Lemma 4 rectangle sits on its wall with `a <= 1`, `b <= 1`, and
  `(a + 2b)^2 <= 8` decided exactly (slack `604/250000`), with both inner corners
  set points, the wall-touch disjunct again vacuous for open boxes;
- each Lemma 2 triangle has all sides of squared length at most one and all
  vertices set points; and
- the charge count: every one of the 16 points is charged by some cell, so any box
  inside `[0, 4]^2` contains at least one Figure 2 point.

What is cited rather than re-proved: Lemma 1 (Nagamochi; Stromquist), Lemma 2
(Friedman; Stromquist), and Lemma 4 (Friedman; Stromquist) themselves -- the same
posture as the Theorem 8 certificate. The premises those lemmas need are what this
module decides. This is the foundation layer of Theorem 9 (`s(13) = 4`), not the
theorem: the pigeonhole here says "every box contains a point", and Section 3's
case analysis (Lemma 10's replacements onward) builds on it.

Usage, from `packing/`:
    uv run --frozen python -m cases.bentz13.verify_cover
"""

from __future__ import annotations

import time
from fractions import Fraction

from cases.bentz13.packing import (
    BOUNDARY,
    EXPECTED_FACES,
    EXPECTED_POINTS,
    SIDE,
    CellPlan,
    Rat,
    build,
)
from sqpack.cover import (
    Point,
    point_in_closed_convex_polygon,
    squared_distance,
    validate_polygon_partition,
)


class CoverCertificateError(ValueError):
    """A premise the printed constants fail exactly; the message names the cell."""


#: Lemma 1's conclusion triangle at the origin corner, mirrored per corner below.
CORNER_TRIANGLE = (
    (Fraction(1), Fraction(1)),
    (Fraction(9, 10), Fraction(1)),
    (Fraction(1), Fraction(9, 10)),
)


def build_certificate() -> dict[str, object]:
    set_points, vertices, plan = build()
    return certify(set_points=set_points, vertices=vertices, plan=plan)


def certify(
    *,
    set_points: dict[str, Point],
    vertices: dict[str, Point],
    plan: dict[str, CellPlan],
) -> dict[str, object]:
    one = Rat.of(1)
    side = Rat.of(SIDE)
    zero = Rat.of(0)

    faces = tuple(entry.face for entry in plan.values())
    partition = validate_polygon_partition(
        vertices, faces, BOUNDARY, expected_faces=EXPECTED_FACES
    )
    for name in BOUNDARY:
        x, y = vertices[name]
        on_wall = x.is_zero() or y.is_zero() or (x - side).is_zero() or (y - side).is_zero()
        if not on_wall:
            raise CoverCertificateError(f"boundary vertex {name} is not on a container wall")

    def point(name: object) -> Point:
        return vertices[str(name)]

    charged: set[str] = set()
    kinds = {"corner1": 0, "lemma4": 0, "lemma2": 0}

    for name, entry in plan.items():
        kind = entry.kind
        face = entry.face
        kinds[kind] += 1
        if kind == "corner1":
            corner = point(entry.corner)
            corner_x, corner_y = corner
            if not (corner_x.is_zero() or (corner_x - side).is_zero()) or not (
                corner_y.is_zero() or (corner_y - side).is_zero()
            ):
                raise CoverCertificateError(f"{name}: corner is not a container corner")
            for vertex in face:
                x, y = point(vertex)
                dx = x - corner_x if (x - corner_x).sign() >= 0 else corner_x - x
                dy = y - corner_y if (y - corner_y).sign() >= 0 else corner_y - y
                if (one - dx).sign() < 0 or (one - dy).sign() < 0:
                    raise CoverCertificateError(
                        f"{name}: a pentagon vertex leaves the corner unit square"
                    )

            # Map Lemma 1's conclusion triangle into this corner's frame.
            def image(
                local: tuple[Fraction, Fraction], *, corner_x: Point = corner, _side: Rat = side
            ) -> Point:
                lx, ly = Rat.of(local[0]), Rat.of(local[1])
                x = lx if corner_x[0].is_zero() else _side - lx
                y = ly if corner_x[1].is_zero() else _side - ly
                return (x, y)

            triangle = tuple(image(local) for local in CORNER_TRIANGLE)
            for out in entry.outs:
                if out not in set_points:
                    raise CoverCertificateError(f"{name}: out {out} is not a set point")
                if not point_in_closed_convex_polygon(point(out), triangle):
                    raise CoverCertificateError(
                        f"{name}: out {out} is outside Lemma 1's conclusion triangle"
                    )
            charged.update(entry.outs)
        elif kind == "lemma4":
            xs = sorted({point(v)[0] for v in face}, key=lambda value: value.value)
            ys = sorted({point(v)[1] for v in face}, key=lambda value: value.value)
            if len(xs) != 2 or len(ys) != 2:
                raise CoverCertificateError(f"{name}: not an axis-aligned rectangle")
            horizontal = entry.wall in ("bottom", "top")
            width = (xs[1] - xs[0]) if horizontal else (ys[1] - ys[0])
            height = (ys[1] - ys[0]) if horizontal else (xs[1] - xs[0])
            if (one - width).sign() < 0 or (one - height).sign() < 0:
                raise CoverCertificateError(f"{name}: Lemma 4 needs a, b at most one")
            reach = width + height + height
            if (Rat.of(8) - reach * reach).sign() < 0:
                raise CoverCertificateError(f"{name}: (a + 2b)^2 exceeds 8")
            wall_value = {
                "bottom": (ys[0], zero),
                "top": (ys[1], side),
                "left": (xs[0], zero),
                "right": (xs[1], side),
            }[str(entry.wall)]
            if not (wall_value[0] - wall_value[1]).is_zero():
                raise CoverCertificateError(f"{name}: rectangle does not sit on its wall")
            inner = ys[0] if entry.wall == "top" else ys[1]
            if not horizontal:
                inner = xs[0] if entry.wall == "right" else xs[1]
            axis = 1 if horizontal else 0
            for out in entry.outs:
                if out not in set_points:
                    raise CoverCertificateError(f"{name}: out {out} is not a set point")
                if not (point(out)[axis] - inner).is_zero():
                    raise CoverCertificateError(f"{name}: out {out} is not an inner corner")
            if len(entry.outs) != 2:
                raise CoverCertificateError(f"{name}: Lemma 4 needs both inner corners")
            charged.update(entry.outs)
        else:  # lemma2
            for left, right in zip(face, face[1:] + face[:1], strict=True):
                gap = one - squared_distance(point(left), point(right))
                if gap.sign() < 0:
                    raise CoverCertificateError(f"{name}: a triangle side exceeds one")
            if any(vertex not in set_points for vertex in face):
                raise CoverCertificateError(f"{name}: a triangle vertex is not a set point")
            charged.update(face)

    if charged != set(set_points):
        missing = sorted(set(set_points) - charged)
        raise CoverCertificateError(f"points never charged by any cell: {missing}")

    return {
        "claim": "Bentz 2010 Figure 2: every box in [0,4]^2 contains one of the 16 points",
        "arithmetic": "exact rational signs only; radical premises squared away",
        "partition": partition,
        "cells": kinds,
        "set_point_count": len(set_points),
        "every_cell_charges_a_set_point": True,
        "cited_not_reproved": [
            "Lemma 1 (Nagamochi; Stromquist)",
            "Lemma 2 (Friedman; Stromquist)",
            "Lemma 4 (Friedman; Stromquist)",
        ],
        "role_in_theorem_9": (
            "base configuration: 13 boxes against 16 points forces at least ten "
            "boxes with exactly one point, hence two corner-restricted boxes; the "
            "Section 3 case analysis continues from there"
        ),
    }


def main() -> int:
    started = time.monotonic()
    certificate = build_certificate()
    elapsed = time.monotonic() - started
    print(f"partition: {EXPECTED_FACES} faces certified over exact rationals")
    print(f"cells: {certificate['cells']}")
    print(f"points charged: {certificate['set_point_count']} of {EXPECTED_POINTS}")
    print(f"claim: {certificate['claim']}")
    print(f"wall: {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
