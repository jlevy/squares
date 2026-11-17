"""Two exact decision methods for closed unit squares in a closed box, written for this review.

Each square is given by its centre (x, y), the half-angle tangent t = tan(theta/2) and a
half side h (1/2 for a unit square). Its axes are u = (c, s) and v = (-s, c) with
c = (1 - t^2)/(1 + t^2) and s = 2t/(1 + t^2), so c^2 + s^2 = 1 exactly and the square
is exact: corners centre + h(+-u +- v). sense = -1 reads the rotation the other way
(s -> -s), which is the reversed-sense control.

Method A, separating axes in fractions.Fraction. Two convex polygons have disjoint
interiors if and only if, along one of their edge normals, the projection of one lies
at or below the projection of the other (the Minkowski difference argument; for two
squares the edge normals are u_i, v_i, u_j, v_j). The pair gap is the largest
projection gap over those four unit axes: it is >= 0 exactly when the interiors are
disjoint, and it is a lower bound on the Euclidean distance between the squares. A
square lies in the box [0, S]^2 if and only if its four corners do; the wall clearance
is the least corner coordinate distance to the four walls.

Method B, exact clipped areas in gmpy2.mpq, with its own corner construction from
t = p/q (c = (q^2 - p^2)/(q^2 + p^2), s = 2pq/(q^2 + p^2)). Square i is clipped by the
four closed half-planes of square j (Sutherland-Hodgman, inclusive), and the shoelace
area of the result is the area of the intersection: it is 0 exactly when the interiors
are disjoint (a convex set has zero area if and only if its interior is empty, and
int(A n B) = int A n int B). For the walls, the square is clipped by the box and its
area must be the square's own area (a closed convex body is inside a closed convex set
if and only if their intersection has the body's full area).

No distance filter is used anywhere: callers decide every pair.
"""

from __future__ import annotations

from fractions import Fraction

import gmpy2
from gmpy2 import mpq

HALF = Fraction(1, 2)

# ---------------------------------------------------------------- method A (Fraction)


def frame_a(t: Fraction, sense: int = 1) -> tuple[Fraction, Fraction]:
    d = 1 + t * t
    c = (1 - t * t) / d
    s = (2 * t) / d
    if sense == -1:
        s = -s
    return c, s


def square_a(x: Fraction, y: Fraction, t: Fraction, h: Fraction = HALF, sense: int = 1):
    """Corners (counter-clockwise) and the two unit axes of one square, in Fraction."""
    c, s = frame_a(t, sense)
    ux, uy = c * h, s * h
    vx, vy = -s * h, c * h
    corners = (
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
    )
    axes = ((c, s), (-s, c))
    return corners, axes


def pair_gap_a(sq_i, sq_j) -> tuple[Fraction, int]:
    """Largest projection gap over the four edge normals, and which axis gives it.

    >= 0 iff the interiors are disjoint. Axis index 0, 1 are square i's u, v; 2, 3 are j's.
    """
    ci, ai = sq_i
    cj, aj = sq_j
    best = None
    best_k = -1
    for k, (ax, ay) in enumerate(ai + aj):
        pi = [px * ax + py * ay for (px, py) in ci]
        pj = [px * ax + py * ay for (px, py) in cj]
        g1 = min(pj) - max(pi)
        g2 = min(pi) - max(pj)
        g = g1 if g1 >= g2 else g2
        if best is None or g > best:
            best = g
            best_k = k
    return best, best_k


def wall_clearance_a(sq, side: Fraction) -> Fraction:
    """Least distance of a corner coordinate to the four walls; >= 0 iff inside."""
    corners, _ = sq
    return min(min(px, side - px, py, side - py) for (px, py) in corners)


# ---------------------------------------------------------------- method B (gmpy2.mpq)


def _q(v: Fraction) -> mpq:
    return mpq(v.numerator, v.denominator)


def square_b(x: Fraction, y: Fraction, t: Fraction, h: Fraction = HALF, sense: int = 1):
    """Corners (counter-clockwise) of one square, in mpq, from t = p/q directly."""
    p, q = t.numerator, t.denominator
    d = q * q + p * p
    c = mpq(q * q - p * p, d)
    s = mpq(2 * p * q, d)
    if sense == -1:
        s = -s
    hx = _q(h)
    X, Y = _q(x), _q(y)
    out = []
    for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        out.append((X + hx * (a * c - b * s), Y + hx * (a * s + b * c)))
    return tuple(out)


def _clip(poly, ax, ay, bx, by):
    """Keep the part of poly on the closed left side of the directed line A -> B."""
    if not poly:
        return poly
    ex, ey = bx - ax, by - ay
    vals = [ex * (py - ay) - ey * (px - ax) for (px, py) in poly]
    out = []
    m = len(poly)
    for k in range(m):
        px, py = poly[k - 1]
        fp = vals[k - 1]
        qx, qy = poly[k]
        fq = vals[k]
        if fq >= 0:
            if fp < 0:
                r = fp / (fp - fq)
                out.append((px + r * (qx - px), py + r * (qy - py)))
            out.append((qx, qy))
        elif fp >= 0:
            r = fp / (fp - fq)
            out.append((px + r * (qx - px), py + r * (qy - py)))
    return out


def area_b(poly) -> mpq:
    """Shoelace area (counter-clockwise positive)."""
    if len(poly) < 3:
        return mpq(0)
    s = mpq(0)
    m = len(poly)
    for k in range(m):
        x1, y1 = poly[k - 1]
        x2, y2 = poly[k]
        s += x1 * y2 - x2 * y1
    return s / 2


def pair_area_b(poly_i, poly_j) -> mpq:
    """Area of the intersection of two counter-clockwise convex polygons."""
    out = list(poly_i)
    m = len(poly_j)
    for k in range(m):
        ax, ay = poly_j[k]
        bx, by = poly_j[(k + 1) % m]
        out = _clip(out, ax, ay, bx, by)
        if not out:
            return mpq(0)
    a = area_b(out)
    if a < 0:
        raise AssertionError("negative clipped area: orientation error")
    return a


def wall_deficit_b(poly, side: Fraction) -> mpq:
    """Area of the square outside the closed box [0, S]^2 (0 iff inside)."""
    sd = _q(side)
    z = mpq(0)
    box = ((z, z), (sd, z), (sd, sd), (z, sd))
    out = list(poly)
    for k in range(4):
        ax, ay = box[k]
        bx, by = box[(k + 1) % 4]
        out = _clip(out, ax, ay, bx, by)
    return area_b(poly) - area_b(out)


GMPY2_VERSION = gmpy2.version()
