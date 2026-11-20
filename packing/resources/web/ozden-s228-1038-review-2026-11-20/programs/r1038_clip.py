"""Method B: exact convex clipping of corners, in GMP rationals (`gmpy2.mpq`).

It is handed each square's centre and basis as rationals and nothing else, and builds the
four corners c - u/2 - v/2, c + u/2 - v/2, c + u/2 + v/2, c - u/2 + v/2 with v = (-b, a).

- Unit square: the four sides have squared length 1 and both diagonals squared length 2.
  The shoelace sum, +2 or -2, is the listing's sense; a clockwise listing is reversed.
- Pair: one square is clipped against the four closed half-planes to the left of the
  other's counterclockwise edges (Sutherland-Hodgman, keeping points on the line), which
  gives their intersection exactly; it is done both ways round, and the two results must
  agree in class and in area. Empty is apart; non-empty with zero area is contact, since
  the interior of an intersection of convex sets is the intersection of their interiors;
  positive area is overlap, by that area.
- Wall: the square is clipped against the closed half-plane outside the wall: empty is
  clear, zero area touching, positive area crossing. Containment is decided apart: a unit
  square lies in the box exactly when its intersection with the box has area exactly 1.

It imports nothing but `gmpy2`, and shares nothing with method A but the reader's output.
"""

from __future__ import annotations

from fractions import Fraction

from gmpy2 import mpq

Point = tuple[mpq, mpq]
HALF = mpq(1, 2)
ZERO = mpq(0)
ONE = mpq(1)
TWO = mpq(2)


def to_mpq(value: Fraction) -> mpq:
    """A reader's Fraction as a GMP rational."""
    return mpq(value.numerator, value.denominator)


def corners(cx: mpq, cy: mpq, a: mpq, b: mpq) -> list[Point]:
    """The four corners of the square with centre (cx, cy) and basis (a, b)."""
    ux, uy = a * HALF, b * HALF
    vx, vy = -b * HALF, a * HALF
    return [
        (cx - ux - vx, cy - uy - vy),
        (cx + ux - vx, cy + uy - vy),
        (cx + ux + vx, cy + uy + vy),
        (cx - ux + vx, cy - uy + vy),
    ]


def _squared(p: Point, q: Point) -> mpq:
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    return dx * dx + dy * dy


def area2(polygon: list[Point]) -> mpq:
    """Twice the signed area (the shoelace sum)."""
    total = ZERO
    count = len(polygon)
    for index in range(count):
        x0, y0 = polygon[index]
        x1, y1 = polygon[(index + 1) % count]
        total += x0 * y1 - x1 * y0
    return total


def unit_square(points: list[Point]) -> bool:
    """Whether four points, in cyclic order, are a unit square."""
    sides = all(_squared(points[k], points[(k + 1) % 4]) == ONE for k in range(4))
    diagonals = _squared(points[0], points[2]) == TWO and _squared(points[1], points[3]) == TWO
    return sides and diagonals


def counterclockwise(points: list[Point]) -> tuple[list[Point], int]:
    """The points listed counterclockwise, and the sense they were listed in (+1 or -1)."""
    twice = area2(points)
    if twice == TWO:
        return points, 1
    if twice == -TWO:
        return list(reversed(points)), -1
    raise ValueError(f"shoelace sum {twice} is not +2 or -2")


def _side(p: Point, q: Point, r: Point) -> mpq:
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def clip(polygon: list[Point], p: Point, q: Point) -> list[Point]:
    """The polygon cut to the closed half-plane left of the directed line p -> q."""
    result: list[Point] = []
    count = len(polygon)
    for index in range(count):
        start = polygon[index]
        end = polygon[(index + 1) % count]
        s_start = _side(p, q, start)
        s_end = _side(p, q, end)
        if s_end >= 0:
            if s_start < 0:
                t = s_start / (s_start - s_end)
                result.append((start[0] + (end[0] - start[0]) * t, start[1] + (end[1] - start[1]) * t))
            result.append(end)
        elif s_start >= 0:
            t = s_start / (s_start - s_end)
            result.append((start[0] + (end[0] - start[0]) * t, start[1] + (end[1] - start[1]) * t))
    return result


def intersection(subject: list[Point], clipper_ccw: list[Point]) -> list[Point]:
    """The subject cut to the counterclockwise convex clipper."""
    current = subject
    for index in range(len(clipper_ccw)):
        if not current:
            return current
        current = clip(current, clipper_ccw[index], clipper_ccw[(index + 1) % len(clipper_ccw)])
    return current


def classify(polygon: list[Point]) -> tuple[str, mpq]:
    """apart, contact or overlap, and the area."""
    if not polygon:
        return "apart", ZERO
    twice = area2(polygon)
    if twice < 0:
        raise ValueError("a clipped polygon with negative area")
    if twice == 0:
        return "contact", ZERO
    return "overlap", twice / 2


def pair(square_i: list[Point], square_j: list[Point]) -> tuple[str, mpq, bool]:
    """A pair's class and area, both ways round, and whether the two ways agree."""
    class_a, area_a = classify(intersection(square_j, square_i))
    class_b, area_b = classify(intersection(square_i, square_j))
    return class_a, area_a, class_a == class_b and area_a == area_b


def walls(square: list[Point], side: mpq) -> tuple[list[str], mpq]:
    """The square's class at the left, bottom, right and top walls, and its area inside."""
    outside = [
        ((ZERO, ZERO), (ZERO, ONE)),  # x <= 0
        ((ONE, ZERO), (ZERO, ZERO)),  # y <= 0
        ((side, ONE), (side, ZERO)),  # x >= side
        ((ZERO, side), (ONE, side)),  # y >= side
    ]
    classes: list[str] = []
    for p, q in outside:
        name, _ = classify(clip(square, p, q))
        classes.append({"apart": "clear", "contact": "touching", "overlap": "crossing"}[name])
    box = [(ZERO, ZERO), (side, ZERO), (side, side), (ZERO, side)]
    inside = intersection(square, box)
    area = area2(inside) / 2 if inside else ZERO
    return classes, area
