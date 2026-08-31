"""Exact certificate for Bentz 2010, Theorem 8: `s(46) = 7`.

What is certified here, by exact sign in `Q(sqrt 2, sqrt 3)` or exact rational
interval arithmetic, with no tolerance anywhere:

- the 92-cell complex exactly tiles `[0, 7]^2` (areas, incidences, noncrossing,
  Euler characteristic, boundary edges on the container walls);
- every Lemma 2 triangle has all sides of squared length exactly one;
- every Lemma 4 rectangle sits on its wall with `a <= 1`, `b <= 1`, and
  `a + 2b <= 2 sqrt(2)` decided by exact sign (the bottom row meets it with exact
  equality, `1 + 2(sqrt 2 - 1/2) = 2 sqrt 2` -- the margin is zero, not small);
- every Lemma 5 quadrilateral matches the lemma's frame exactly (wall span
  `a = sqrt(3)/2`, off-wall corners at perpendicular distances `1` and `1/2`, the
  regime `2 sqrt 2 - 2 < a < 1`, and `a^2 + (b-1)^2 <= 1` holding with exact
  equality), and the threshold `b < f(a)` is certified by a rigorous rational
  interval subdivision lower bound on the infimum defining `f`;
- every cell offers at least one containable out that is a set point, walls and
  wall vertices being uncontainable for a box inside the container; and
- the pigeonhole arithmetic: 45 points, each in at most one open box, so at most
  45 disjoint boxes, so 46 cannot pack.

What is cited rather than re-proved: the non-avoidance lemma statements themselves
(Lemma 2 -- Friedman, Stromquist; Lemma 4 -- Friedman, Stromquist; Lemma 5 --
Stromquist, with Bentz's own footnote correcting its original root-selection claim),
exactly as the retained Stromquist certificates cite theirs. The premises those
lemmas need are what this module decides.

Usage, from `packing/`:
    uv run --frozen python -m cases.bentz46.verify_cover
"""

from __future__ import annotations

import time
from fractions import Fraction
from math import isqrt

from cases.bentz46.packing import EXPECTED_FACES, EXPECTED_POINTS, CellPlan, build
from sqpack.cover import Point, squared_distance, validate_square_tiling
from sqpack.field import FieldElement, NumberField

#: Rational upper bound on sqrt(3)/2, verified by squaring below.
A_UPPER = Fraction(8_660_255, 10**7)
#: Grid start at or below cos(pi/4) and the tail split point.
C_START = Fraction(7_071, 10**4)
C_END = Fraction(99, 100)
GRID_STEPS = 400
SQRT_SCALE = 10**8


class CoverCertificateError(ValueError):
    """A premise the printed constants fail exactly; the message names the cell."""


def sqrt_upper(value: Fraction) -> Fraction:
    """A rational upper bound on sqrt(value), verified by squaring."""
    if value < 0:
        raise CoverCertificateError("sqrt_upper of a negative value")
    scaled = (value.numerator * SQRT_SCALE * SQRT_SCALE) // value.denominator
    root = Fraction(isqrt(scaled) + 1, SQRT_SCALE)
    if root * root < value:
        raise CoverCertificateError("sqrt upper bound failed its own square check")
    return root


def lemma5_threshold_certificate(b: Fraction) -> dict[str, object]:
    """Certify `b < f(sqrt(3)/2)` by a rigorous lower bound on the infimum.

    `f(a)` is the infimum over `theta` in `(0, pi/4]` of
    `cos t/(1+cos t) + (1 - a cos t)/sin t`; substituting `c = cos t` the range is
    `c` in `[sqrt(2)/2, 1)`. Every rounding below is downward for the bound: the
    first term uses the interval's left end (it is increasing in `c`), the second
    uses an upper bound for `a` and `c` in its numerator and an upper bound for
    `sin t` in its denominator. A `b` at or above the bound is a typed refusal,
    never a silent pass.
    """
    if A_UPPER * A_UPPER - Fraction(3, 4) <= 0:
        raise CoverCertificateError("A_UPPER is not an upper bound for sqrt(3)/2")
    if C_START * C_START - Fraction(1, 2) >= 0:
        raise CoverCertificateError("C_START is not at or below cos(pi/4)")

    lows: list[Fraction] = []
    step = (C_END - C_START) / GRID_STEPS
    for index in range(GRID_STEPS):
        c0 = C_START + step * index
        c1 = c0 + step
        numerator_low = 1 - A_UPPER * c1
        if numerator_low <= 0:
            raise CoverCertificateError("second-term numerator lost positivity on the grid")
        sin_upper = sqrt_upper(1 - c0 * c0)
        lows.append(c0 / (1 + c0) + numerator_low / sin_upper)
    tail_low = C_END / (1 + C_END) + (1 - A_UPPER) / sqrt_upper(1 - C_END * C_END)
    lows.append(tail_low)
    bound = min(lows)
    if bound <= b:
        raise CoverCertificateError(
            f"threshold refused: certified lower bound {float(bound):.6f} does not exceed b={b}"
        )
    return {
        "a": "sqrt(3)/2, bounded above by " + str(A_UPPER),
        "b": str(b),
        "grid": [str(C_START), str(C_END), GRID_STEPS],
        "tail": "c in [99/100, 1): numerator bounded by 1 - A_UPPER",
        "certified_infimum_lower_bound": str(bound),
        "decimal_for_display_only": f"{float(bound):.6f}",
        "strictly_exceeds_b": True,
    }


def build_certificate() -> dict[str, object]:
    field, sqrt2, sqrt3, set_points, vertices, plan = build()
    return certify(field, sqrt2, sqrt3, set_points=set_points, vertices=vertices, plan=plan)


def certify(
    field: NumberField,
    sqrt2: FieldElement,
    sqrt3: FieldElement,
    *,
    set_points: dict[str, Point],
    vertices: dict[str, Point],
    plan: dict[str, CellPlan],
) -> dict[str, object]:
    rational = field.rational
    side = rational(7)
    one = rational(1)
    two_sqrt2 = 2 * sqrt2
    dy = sqrt3 / 2
    half = rational(Fraction(1, 2))

    faces = tuple(entry.face for entry in plan.values())
    tiling = validate_square_tiling(vertices, faces, side=side, expected_faces=EXPECTED_FACES)

    def point(name: object) -> Point:
        return vertices[str(name)]

    charged: set[str] = set()
    kinds = {"lemma2": 0, "lemma4": 0, "lemma5": 0}
    threshold = lemma5_threshold_certificate(Fraction(1, 2))

    for name, entry in plan.items():
        kind = entry.kind
        face = entry.face
        kinds[kind] += 1
        if kind == "lemma2":
            for left, right in zip(face, face[1:] + face[:1], strict=True):
                gap = squared_distance(point(left), point(right)) - one
                if not gap.is_zero():
                    raise CoverCertificateError(f"{name}: a triangle side is not exactly one")
            if any(vertex not in set_points for vertex in face):
                raise CoverCertificateError(f"{name}: a triangle vertex is not a set point")
            charged.update(face)
        elif kind == "lemma4":
            width, height = entry.width, entry.height
            if width is None or height is None:
                raise CoverCertificateError(f"{name}: Lemma 4 plan lacks width or height")
            if (one - width).sign() < 0 or (one - height).sign() < 0:
                raise CoverCertificateError(f"{name}: Lemma 4 needs a, b at most one")
            slack = two_sqrt2 - (width + 2 * height)
            if slack.sign() < 0:
                raise CoverCertificateError(f"{name}: a + 2b exceeds 2 sqrt 2")
            xs = sorted({point(v)[0] for v in face}, key=float)
            ys = sorted({point(v)[1] for v in face}, key=float)
            if len(xs) != 2 or len(ys) != 2:
                raise CoverCertificateError(f"{name}: not an axis-aligned rectangle")
            if not (xs[1] - xs[0] - width).is_zero() or not (ys[1] - ys[0] - height).is_zero():
                raise CoverCertificateError(f"{name}: rectangle sides disagree with the plan")
            wall_y = ys[1] if entry.wall == "top" else ys[0]
            expected_wall = side if entry.wall == "top" else rational(0)
            if not (wall_y - expected_wall).is_zero():
                raise CoverCertificateError(f"{name}: rectangle does not sit on its wall")
            outs = entry.outs
            inner_y = ys[0] if entry.wall == "top" else ys[1]
            for out in outs:
                if not (point(out)[1] - inner_y).is_zero():
                    raise CoverCertificateError(f"{name}: an out is not an inner corner")
            set_outs = [out for out in outs if out in set_points]
            if not set_outs:
                raise CoverCertificateError(f"{name}: no containable set-point out")
            charged.update(set_outs)
        else:  # lemma5
            wall = str(entry.wall)
            wall_x = rational(0) if wall == "left" else side
            wall_names = [v for v in face if (point(v)[0] - wall_x).is_zero()]
            if len(wall_names) != 2:
                raise CoverCertificateError(f"{name}: quad does not span its wall")
            span = point(wall_names[0])[1] - point(wall_names[1])[1]
            span = span if span.sign() > 0 else -span
            if not (span - dy).is_zero():
                raise CoverCertificateError(f"{name}: wall span is not sqrt(3)/2")
            if (span - (two_sqrt2 - 2)).sign() <= 0 or (one - span).sign() <= 0:
                raise CoverCertificateError(f"{name}: a outside Lemma 5's regime")
            reach = span * span + (half - one) ** 2 - one
            if reach.sign() > 0:
                raise CoverCertificateError(f"{name}: (a, b) further than one from (0, 1)")
            far, near = str(entry.far), str(entry.near)
            inward = one if wall == "left" else -one
            far_distance = inward * (point(far)[0] - wall_x)
            near_distance = inward * (point(near)[0] - wall_x)
            if not (far_distance - one).is_zero() or not (near_distance - half).is_zero():
                raise CoverCertificateError(f"{name}: off-wall corners at wrong distances")
            matched = {
                (point(far)[1] - point(wall_names[0])[1]).is_zero(),
                (point(near)[1] - point(wall_names[1])[1]).is_zero(),
            } | {
                (point(far)[1] - point(wall_names[1])[1]).is_zero(),
                (point(near)[1] - point(wall_names[0])[1]).is_zero(),
            }
            if True not in matched:
                raise CoverCertificateError(f"{name}: corners do not align with the wall span")
            if far not in set_points or near not in set_points:
                raise CoverCertificateError(f"{name}: a Lemma 5 out is not a set point")
            charged.update((far, near))

    if charged != set(set_points):
        missing = sorted(set(set_points) - charged)
        raise CoverCertificateError(f"points never charged by any cell: {missing}")

    return {
        "theorem": "Bentz 2010 Theorem 8: 46 boxes cannot pack in [0,7]^2",
        "field": {
            "generator": "alpha=sqrt(2)+sqrt(3)",
            "minimal_polynomial_high_to_low": [1, 0, -10, 0, 1],
            "all_decisions": "exact signs in Q(alpha) plus exact rational intervals",
        },
        "tiling": tiling,
        "cells": kinds,
        "lemma5_threshold": threshold,
        "set_point_count": len(set_points),
        "every_cell_charges_a_set_point": True,
        "pigeonhole": {
            "boxes_forced_to_contain_a_point": True,
            "points": EXPECTED_POINTS,
            "box_bound": EXPECTED_POINTS,
            "claim": "46 pairwise-disjoint open boxes of side > 1 cannot fit",
        },
        "cited_not_reproved": [
            "Lemma 2 (Friedman; Stromquist)",
            "Lemma 4 (Friedman; Stromquist)",
            "Lemma 5 (Stromquist; Bentz's footnote corrects its root selection)",
        ],
    }


def main() -> int:
    started = time.monotonic()
    certificate = build_certificate()
    elapsed = time.monotonic() - started
    cells = certificate["cells"]
    threshold = certificate["lemma5_threshold"]
    print(f"tiling: {EXPECTED_FACES} faces certified over Q(sqrt2, sqrt3)")
    print(f"cells: {cells}")
    print(
        "lemma 5 threshold at (sqrt(3)/2, 1/2): certified infimum lower bound "
        f"{threshold['decimal_for_display_only']}"  # type: ignore[index]
    )
    print(f"points charged: {certificate['set_point_count']} of {EXPECTED_POINTS}")
    print(f"conclusion: {certificate['pigeonhole']['claim']}")  # type: ignore[index]
    print(f"wall: {elapsed:.2f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
