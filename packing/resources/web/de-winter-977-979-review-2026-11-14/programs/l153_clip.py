"""Lane L153 method B: exact convex clipping in GMP rationals (gmpy2.mpq).

Clean-room: written for this review, importing nothing from this repository or the
source, and reusing no code of any earlier review.

A square is turned into its four corners, C - u/2 - v/2, C + u/2 - v/2, C + u/2 + v/2,
C - u/2 + v/2 with u = (c, s) and v = (-s, c), and from then on only the corners are
used: no unit normal and no half-width.

- **Unit square.** The four corners are a unit square in cyclic order when all four
  sides have squared length 1 and both diagonals squared length 2: the converse of
  Pythagoras gives right angles at the second and fourth corners, which are then the two
  points at distance 1 from both the first and the third.
- **Pairs.** One square is clipped (Sutherland-Hodgman) against the four closed
  half-planes to the left of the other's directed edges, keeping boundary points; for
  convex polygons the result is exactly their intersection. Empty is apart; non-empty
  with zero area is contact, since the interior of an intersection of convex sets is the
  intersection of their interiors; positive area is overlap, by that area.
- **Walls.** Each square is clipped against the closed half-plane outside each wall of
  [0, S]^2, and classed the same way (apart, contact, crossing).
- **Containment.** A unit square lies in the closed box exactly when its intersection
  with the box has area exactly 1: a point of the square outside the box has a
  neighbourhood outside it, which meets the square's interior in positive area.
"""

from __future__ import annotations

from collections.abc import Callable

from gmpy2 import mpq

Pair = tuple[int, int]
Square = tuple[Pair, Pair, Pair, Pair]
Point = tuple[mpq, mpq]
Poly = list[Point]

HALF = mpq(1, 2)
ZERO = mpq(0)
ONE = mpq(1)
TWO = mpq(2)


def corners(square: Square) -> Poly:
    (px, qx), (py, qy), (pc, qc), (ps, qs) = square
    cx, cy = mpq(px, qx), mpq(py, qy)
    ux, uy = mpq(pc, qc) * HALF, mpq(ps, qs) * HALF
    vx, vy = -uy, ux
    return [
        (cx - ux - vx, cy - uy - vy),
        (cx + ux - vx, cy + uy - vy),
        (cx + ux + vx, cy + uy + vy),
        (cx - ux + vx, cy - uy + vy),
    ]


def _d2(p: Point, q: Point) -> mpq:
    dx, dy = q[0] - p[0], q[1] - p[1]
    return dx * dx + dy * dy


def is_unit(poly: Poly) -> bool:
    sides = all(_d2(poly[k], poly[(k + 1) % 4]) == ONE for k in range(4))
    return sides and _d2(poly[0], poly[2]) == TWO and _d2(poly[1], poly[3]) == TWO


def signed_area2(poly: Poly) -> mpq:
    """Twice the signed shoelace area."""
    total = ZERO
    count = len(poly)
    for k in range(count):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % count]
        total += x0 * y1 - x1 * y0
    return total


def clip(poly: Poly, f: Callable[[Point], mpq], closed: bool = True) -> Poly:
    """Sutherland-Hodgman step: keep the part of poly where the affine f is >= 0.

    `closed=False` keeps only f > 0; it exists for the self-test's broken copy.
    """
    if not poly:
        return poly
    values = [f(p) for p in poly]
    inside = [v >= 0 if closed else v > 0 for v in values]
    out: Poly = []
    count = len(poly)
    for k in range(count):
        s, e = poly[k - 1], poly[k]
        fs, fe = values[k - 1], values[k]
        if inside[k]:
            if not inside[k - 1]:
                out.append(_cross_point(s, e, fs, fe))
            out.append(e)
        elif inside[k - 1]:
            out.append(_cross_point(s, e, fs, fe))
    return out


def _cross_point(s: Point, e: Point, fs: mpq, fe: mpq) -> Point:
    t = fs / (fs - fe)
    return (s[0] + t * (e[0] - s[0]), s[1] + t * (e[1] - s[1]))


def _edge_function(a: Point, b: Point) -> Callable[[Point], mpq]:
    ex, ey = b[0] - a[0], b[1] - a[1]
    ax, ay = a

    def f(p: Point) -> mpq:
        return ex * (p[1] - ay) - ey * (p[0] - ax)

    return f


def intersect(subject: Poly, clipper: Poly, closed: bool = True) -> Poly:
    """subject clipped against the closed left half-planes of clipper's directed edges.

    The clipper must be listed counterclockwise; `corners` lists every square so.
    """
    poly = subject
    for k in range(4):
        poly = clip(poly, _edge_function(clipper[k], clipper[(k + 1) % 4]), closed)
        if not poly:
            break
    return poly


def classify_polygon(poly: Poly) -> tuple[str, mpq]:
    if not poly:
        return "apart", ZERO
    area = abs(signed_area2(poly)) / 2
    if area == 0:
        return "contact", ZERO
    return "overlap", area


def pair(pi: Poly, pj: Poly, closed: bool = True) -> tuple[str, mpq]:
    return classify_polygon(intersect(pj, pi, closed))


def _outside(wall: str, side: mpq) -> Callable[[Point], mpq]:
    if wall == "left":
        return lambda p: -p[0]
    if wall == "right":
        return lambda p: p[0] - side
    if wall == "bottom":
        return lambda p: -p[1]
    return lambda p: p[1] - side


def wall(poly: Poly, name: str, side: mpq, closed: bool = True) -> tuple[str, mpq]:
    """apart, contact or crossing (with the area outside) for one wall."""
    cls, area = classify_polygon(clip(poly, _outside(name, side), closed))
    return ("crossing" if cls == "overlap" else cls), area


def inside_area(poly: Poly, side: mpq) -> mpq:
    """Area of the square's intersection with the closed box [0, side]^2."""
    fs: list[Callable[[Point], mpq]] = [
        lambda p: p[0],
        lambda p: side - p[0],
        lambda p: p[1],
        lambda p: side - p[1],
    ]
    out = poly
    for f in fs:
        out = clip(out, f)
    return abs(signed_area2(out)) / 2 if out else ZERO
