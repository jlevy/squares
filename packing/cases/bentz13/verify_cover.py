"""Exact certificates for Bentz 2010, Section 3 configurations over `[0, 4]^2`.

Every decision is an exact rational sign or an exact rational interval bound; there
is no tolerance anywhere. A cell may be any subset of its declared lemma region --
a box centred in the cell is centred in the region, so the lemma's conclusion
applies unchanged -- and the cell kinds are:

- ``corner1``: subset of a container-corner unit square. Lemma 1's conclusion
  triangle at that corner (the images of `(1, 1)`, `(0.9, 1)`, `(1, 0.9)`) is
  contained by any box centred there, the wall-axes disjunct being vacuous for open
  boxes inside the container; each out is a set point inside that triangle.
- ``lemma4``: subset of a declared wall rectangle with `a <= 1`, `b <= 1`, and
  `(a + 2b)^2 <= 8` exactly; the outs are the rectangle's two inner corners, both
  set points; the wall disjunct is vacuous as above.
- ``lemma5``: subset of a declared bottom-wall quadrilateral `(o, 0)`,
  `(o + a, 0)`, `(o + a, b)`, `(o, 1)` in Stromquist's regime (`(a + 2)^2 > 8`,
  `a < 1`, `b < 1`, `a^2 + (b - 1)^2 <= 1`) with the threshold `b < f(a)` certified
  by a rigorous rational subdivision lower bound on the defining infimum; the outs
  are the two off-wall corners, both set points.
- ``lemma2``: an exact triangle with all squared sides at most one and every vertex
  a set point.
- ``margin``: subset of the band within `1/2` of one container wall. No box centre
  can lie there -- a box has side strictly above one and sits inside the container,
  so its centre keeps distance above `1/2` from every wall -- and the cell declares
  no outs at all.
- ``near``: every cell vertex within squared distance `1/4` of the declared out. An
  open box of side above one contains the closed `1/2`-ball around its centre (its
  inscribed ball has radius `side/2 > 1/2`), so it contains the out point.

What is cited rather than re-proved: Lemmas 1, 2, 4, and 5 themselves (Nagamochi;
Friedman; Stromquist -- with Bentz's own footnote correcting Lemma 5's original
root-selection claim), the same posture as the Theorem 8 certificate. The premises
those lemmas need are what this module decides.

Usage, from `packing/`:
    uv run --frozen python -m cases.bentz13.verify_cover
"""

from __future__ import annotations

import time
from fractions import Fraction
from math import isqrt

from cases.bentz13.packing import (
    BOUNDARY,
    EXPECTED_FACES,
    EXPECTED_POINTS,
    SIDE,
    CellPlan,
    Face,
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

#: Grid for the Lemma 5 threshold bound: c = cos(theta) over (0, pi/4].
C_START = Fraction(7_071, 10**4)
C_END = Fraction(99, 100)
GRID_STEPS = 800
SQRT_SCALE = 10**8


def sqrt_upper(value: Fraction) -> Fraction:
    """A rational upper bound on sqrt(value), verified by squaring."""
    if value < 0:
        raise CoverCertificateError("sqrt_upper of a negative value")
    scaled = (value.numerator * SQRT_SCALE * SQRT_SCALE) // value.denominator
    root = Fraction(isqrt(scaled) + 1, SQRT_SCALE)
    if root * root < value:
        raise CoverCertificateError("sqrt upper bound failed its own square check")
    return root


def lemma5_threshold_certificate(a: Fraction, b: Fraction) -> dict[str, object]:
    """Certify `b < f(a)` for rational `a` by a rigorous lower bound on the infimum.

    `f(a)` is the infimum over `theta` in `(0, pi/4]` of
    `cos t/(1+cos t) + (1 - a cos t)/sin t`; substituting `c = cos t` the range is
    `c` in `[sqrt(2)/2, 1)`. Every rounding is downward for the bound: the first
    term uses the interval's left end (it is increasing in `c`), the second uses
    the right end in its numerator (`a > 0`) and an upper bound for `sin t` in its
    denominator. A `b` at or above the bound is a typed refusal, never a silent
    pass.
    """
    if a <= 0 or a >= 1:
        raise CoverCertificateError("Lemma 5 threshold needs 0 < a < 1")
    if C_START * C_START - Fraction(1, 2) >= 0:
        raise CoverCertificateError("C_START is not at or below cos(pi/4)")

    lows: list[Fraction] = []
    step = (C_END - C_START) / GRID_STEPS
    for index in range(GRID_STEPS):
        c0 = C_START + step * index
        c1 = c0 + step
        numerator_low = 1 - a * c1
        if numerator_low <= 0:
            raise CoverCertificateError("second-term numerator lost positivity on the grid")
        sin_upper = sqrt_upper(1 - c0 * c0)
        lows.append(c0 / (1 + c0) + numerator_low / sin_upper)
    tail_low = C_END / (1 + C_END) + (1 - a) / sqrt_upper(1 - C_END * C_END)
    lows.append(tail_low)
    bound = min(lows)
    if bound <= b:
        raise CoverCertificateError(
            f"threshold refused: certified lower bound {float(bound):.6f} does not exceed b={b}"
        )
    return {
        "a": str(a),
        "b": str(b),
        "grid": [str(C_START), str(C_END), GRID_STEPS],
        "certified_infimum_lower_bound": str(bound),
        "decimal_for_display_only": f"{float(bound):.6f}",
        "strictly_exceeds_b": True,
    }


def build_certificate() -> dict[str, object]:
    set_points, vertices, plan = build()
    return certify(set_points=set_points, vertices=vertices, plan=plan)


def certify(
    *,
    set_points: dict[str, Point],
    vertices: dict[str, Point],
    plan: dict[str, CellPlan],
    expected_faces: int = EXPECTED_FACES,
    boundary: Face = BOUNDARY,
) -> dict[str, object]:
    one = Rat.of(1)
    half = Rat.of(Fraction(1, 2))
    side = Rat.of(SIDE)
    zero = Rat.of(0)

    faces = tuple(entry.face for entry in plan.values())
    partition = validate_polygon_partition(
        vertices, faces, boundary, expected_faces=expected_faces
    )
    for name in boundary:
        x, y = vertices[name]
        on_wall = x.is_zero() or y.is_zero() or (x - side).is_zero() or (y - side).is_zero()
        if not on_wall:
            raise CoverCertificateError(f"boundary vertex {name} is not on a container wall")

    def point(name: object) -> Point:
        return vertices[str(name)]

    def require_set(cell: str, out: str) -> None:
        if out not in set_points:
            raise CoverCertificateError(f"{cell}: out {out} is not a set point")

    charged: set[str] = set()
    kinds: dict[str, int] = {}
    thresholds: list[dict[str, object]] = []

    for name, entry in plan.items():
        kind = entry.kind
        face = entry.face
        kinds[kind] = kinds.get(kind, 0) + 1
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
                        f"{name}: a cell vertex leaves the corner unit square"
                    )

            def image(local: tuple[Fraction, Fraction], *, corner_at: Point = corner) -> Point:
                lx, ly = Rat.of(local[0]), Rat.of(local[1])
                x = lx if corner_at[0].is_zero() else side - lx
                y = ly if corner_at[1].is_zero() else side - ly
                return (x, y)

            triangle = tuple(image(local) for local in CORNER_TRIANGLE)
            for out in entry.outs:
                require_set(name, out)
                if not point_in_closed_convex_polygon(point(out), triangle):
                    raise CoverCertificateError(
                        f"{name}: out {out} is outside Lemma 1's conclusion triangle"
                    )
            charged.update(entry.outs)
        elif kind == "lemma4":
            if entry.rect is None:
                raise CoverCertificateError(f"{name}: Lemma 4 cell declares no rectangle")
            x0, x1, y0, y1 = (Rat.of(value) for value in entry.rect)
            horizontal = entry.wall in ("bottom", "top")
            width = (x1 - x0) if horizontal else (y1 - y0)
            height = (y1 - y0) if horizontal else (x1 - x0)
            if width.sign() <= 0 or height.sign() <= 0:
                raise CoverCertificateError(f"{name}: declared rectangle is degenerate")
            if (one - width).sign() < 0 or (one - height).sign() < 0:
                raise CoverCertificateError(f"{name}: Lemma 4 needs a, b at most one")
            reach = width + height + height
            if (Rat.of(8) - reach * reach).sign() < 0:
                raise CoverCertificateError(f"{name}: (a + 2b)^2 exceeds 8")
            wall_ok = {
                "bottom": y0.is_zero(),
                "top": (y1 - side).is_zero(),
                "left": x0.is_zero(),
                "right": (x1 - side).is_zero(),
            }[str(entry.wall)]
            if not wall_ok:
                raise CoverCertificateError(f"{name}: rectangle does not sit on its wall")
            for vertex in face:
                x, y = point(vertex)
                inside = (
                    (x - x0).sign() >= 0
                    and (x1 - x).sign() >= 0
                    and (y - y0).sign() >= 0
                    and (y1 - y).sign() >= 0
                )
                if not inside:
                    raise CoverCertificateError(
                        f"{name}: a cell vertex leaves the declared rectangle"
                    )
            inner_corners = {
                "bottom": ((x0, y1), (x1, y1)),
                "top": ((x0, y0), (x1, y0)),
                "left": ((x1, y0), (x1, y1)),
                "right": ((x0, y0), (x0, y1)),
            }[str(entry.wall)]
            if len(entry.outs) != 2:
                raise CoverCertificateError(f"{name}: Lemma 4 needs both inner corners")
            matched = []
            for out in entry.outs:
                require_set(name, out)
                ox, oy = point(out)
                matched.append(
                    next(
                        (
                            index
                            for index, (cx, cy) in enumerate(inner_corners)
                            if (ox - cx).is_zero() and (oy - cy).is_zero()
                        ),
                        None,
                    )
                )
            if set(matched) != {0, 1}:
                raise CoverCertificateError(
                    f"{name}: outs do not match the rectangle's inner corners"
                )
            charged.update(entry.outs)
        elif kind == "lemma5":
            if entry.quad is None or entry.wall != "bottom":
                raise CoverCertificateError(f"{name}: Lemma 5 cell declares no bottom quad")
            origin, a, b = entry.quad
            if not (Fraction(0) < a < 1 and Fraction(0) < b < 1):
                raise CoverCertificateError(f"{name}: a, b outside Lemma 5's open box")
            if (a + 2) * (a + 2) <= 8:
                raise CoverCertificateError(f"{name}: a not above 2 sqrt 2 - 2")
            if a * a + (b - 1) * (b - 1) > 1:
                raise CoverCertificateError(f"{name}: (a, b) further than one from (0, 1)")
            thresholds.append(lemma5_threshold_certificate(a, b))
            corners = (
                (Rat.of(origin), zero),
                (Rat.of(origin + a), zero),
                (Rat.of(origin + a), Rat.of(b)),
                (Rat.of(origin), one),
            )
            for vertex in face:
                if not point_in_closed_convex_polygon(point(vertex), corners):
                    raise CoverCertificateError(
                        f"{name}: a cell vertex leaves the declared quadrilateral"
                    )
            if len(entry.outs) != 2:
                raise CoverCertificateError(f"{name}: Lemma 5 needs both off-wall corners")
            targets = (corners[3], corners[2])
            for out, target in zip(entry.outs, targets, strict=True):
                require_set(name, out)
                ox, oy = point(out)
                if not (ox - target[0]).is_zero() or not (oy - target[1]).is_zero():
                    raise CoverCertificateError(
                        f"{name}: out {out} is not the declared quad corner"
                    )
            charged.update(entry.outs)
        elif kind == "margin":
            if entry.outs:
                raise CoverCertificateError(f"{name}: a margin cell charges nothing")
            for vertex in face:
                x, y = point(vertex)
                within = {
                    "bottom": (half - y).sign() >= 0,
                    "top": (y - (side - half)).sign() >= 0,
                    "left": (half - x).sign() >= 0,
                    "right": (x - (side - half)).sign() >= 0,
                }[str(entry.wall)]
                if not within:
                    raise CoverCertificateError(
                        f"{name}: a cell vertex leaves the half-unit wall band"
                    )
        elif kind == "near":
            if len(entry.outs) != 1:
                raise CoverCertificateError(f"{name}: a near cell names exactly one out")
            out = entry.outs[0]
            require_set(name, out)
            anchor = point(out)
            quarter = Rat.of(Fraction(1, 4))
            for vertex in face:
                gap = quarter - squared_distance(point(vertex), anchor)
                if gap.sign() < 0:
                    raise CoverCertificateError(
                        f"{name}: a cell vertex is further than 1/2 from {out}"
                    )
            charged.add(out)
        elif kind == "lemma2":
            for left, right in zip(face, face[1:] + face[:1], strict=True):
                gap = one - squared_distance(point(left), point(right))
                if gap.sign() < 0:
                    raise CoverCertificateError(f"{name}: a triangle side exceeds one")
            if any(vertex not in set_points for vertex in face):
                raise CoverCertificateError(f"{name}: a triangle vertex is not a set point")
            charged.update(face)
        else:
            raise CoverCertificateError(f"{name}: unknown cell kind {kind}")

    if charged != set(set_points):
        missing = sorted(set(set_points) - charged)
        raise CoverCertificateError(f"points never charged by any cell: {missing}")

    return {
        "claim": (
            f"every box in [0,4]^2 contains one of the configuration's {len(set_points)} points"
        ),
        "arithmetic": "exact rational signs only; radical premises squared away",
        "partition": partition,
        "cells": kinds,
        "lemma5_thresholds": thresholds,
        "set_point_count": len(set_points),
        "every_cell_charges_a_set_point": True,
        "cited_not_reproved": [
            "Lemma 1 (Nagamochi; Stromquist)",
            "Lemma 2 (Friedman; Stromquist)",
            "Lemma 4 (Friedman; Stromquist)",
            "Lemma 5 (Stromquist; Bentz's footnote corrects its root selection)",
        ],
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
