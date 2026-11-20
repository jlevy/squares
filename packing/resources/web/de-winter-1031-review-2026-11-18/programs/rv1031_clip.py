"""Method B of the review of jlevy/squares#1031: exact convex clipping on corners.

Written for this review; imports nothing from this repository or the source.

The method is handed four corners per square, as ``gmpy2.mpq``, and nothing else.

* Four points are a unit square in cyclic order when all four sides have squared
  length 1 and both diagonals squared length 2.  The shoelace sum (twice the signed
  area, so +2 or -2) gives the sense; a clockwise listing is reversed before clipping.
* A pair is decided by clipping one square against the four closed half-planes to the
  left of the other's counterclockwise edges (Sutherland-Hodgman, keeping points on the
  line), which gives the intersection of the two closed squares exactly.  Empty is
  apart; non-empty with zero area is contact (the interior of an intersection of convex
  sets is the intersection of their interiors); positive area is overlap, by that area.
  Each pair is clipped both ways round and the two results must agree.
* A wall is classed by the corners' signed distances to it, and containment is decided
  apart: a unit square lies in the box exactly when its intersection with the box, by
  clipping against the box's four closed half-planes, has area exactly 1.
"""

from __future__ import annotations

from fractions import Fraction

import gmpy2
from gmpy2 import mpq

Pt = tuple[object, object]

OPEN_HALF_PLANES = False  # a switch the self-test flips to make a broken copy


def to_mpq(corners: list[tuple[Fraction, Fraction]]) -> list[Pt]:
    return [(mpq(x.numerator, x.denominator), mpq(y.numerator, y.denominator)) for x, y in corners]


def unit_square_sense(c: list[Pt]) -> str | None:
    """``ccw`` or ``cw`` for a unit square listed in cyclic order, else None."""
    if len(c) != 4:
        return None
    one, two = mpq(1), mpq(2)
    for k in range(4):
        ax, ay = c[k]
        bx, by = c[(k + 1) % 4]
        if (bx - ax) ** 2 + (by - ay) ** 2 != one:  # type: ignore[operator]
            return None
    (x0, y0), (x1, y1), (x2, y2), (x3, y3) = c
    if (x2 - x0) ** 2 + (y2 - y0) ** 2 != two or (x3 - x1) ** 2 + (y3 - y1) ** 2 != two:  # type: ignore[operator]
        return None
    s = shoelace2(c)
    if s == two:
        return "ccw"
    if s == -two:
        return "cw"
    return None


def shoelace2(poly: list[Pt]):
    """Twice the signed area."""
    s = mpq(0)
    m = len(poly)
    for k in range(m):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % m]
        s += x1 * y2 - x2 * y1  # type: ignore[operator]
    return s


def ccw(c: list[Pt]) -> list[Pt]:
    sense = unit_square_sense(c)
    if sense is None:
        raise ValueError("not a unit square")
    return list(c) if sense == "ccw" else list(reversed(c))


def _inside(f) -> bool:
    return f > 0 if OPEN_HALF_PLANES else f >= 0


def clip_halfplane(poly: list[Pt], a: Pt, b: Pt) -> list[Pt]:
    """Keep the part of ``poly`` in the closed half-plane to the left of the line a->b."""
    if not poly:
        return []
    ax, ay = a
    ex, ey = b[0] - ax, b[1] - ay  # type: ignore[operator]
    out: list[Pt] = []
    m = len(poly)
    vals = [ex * (py - ay) - ey * (px - ax) for px, py in poly]  # type: ignore[operator]
    for k in range(m):
        s, e = poly[k - 1], poly[k]
        fs, fe = vals[k - 1], vals[k]
        if _inside(fe):
            if not _inside(fs):
                t = fs / (fs - fe)
                out.append((s[0] + (e[0] - s[0]) * t, s[1] + (e[1] - s[1]) * t))  # type: ignore[operator]
            out.append(e)
        elif _inside(fs):
            t = fs / (fs - fe)
            out.append((s[0] + (e[0] - s[0]) * t, s[1] + (e[1] - s[1]) * t))  # type: ignore[operator]
    return out


def clip_convex(subject: list[Pt], clip: list[Pt]) -> list[Pt]:
    """Intersection of a convex polygon with a convex counterclockwise polygon."""
    poly = list(subject)
    m = len(clip)
    for k in range(m):
        poly = clip_halfplane(poly, clip[k], clip[(k + 1) % m])
        if not poly:
            return []
    return poly


def pair_class(ci: list[Pt], cj: list[Pt]) -> tuple[str, object]:
    """Class and area of the intersection of two counterclockwise unit squares, clipped
    both ways; raises if the two ways disagree."""
    r1 = clip_convex(cj, ci)
    r2 = clip_convex(ci, cj)
    k1, a1 = _klass(r1)
    k2, a2 = _klass(r2)
    if k1 != k2 or a1 != a2:
        raise AssertionError(f"clipping disagrees: {k1} {a1} / {k2} {a2}")
    return k1, a1


def _klass(poly: list[Pt]) -> tuple[str, object]:
    if not poly:
        return "apart", mpq(0)
    area = abs(shoelace2(poly)) / 2
    if area == 0:
        return "contact", area
    return "overlap", area


def wall_terms(c: list[Pt], side) -> tuple[object, object, object, object]:
    """(left, bottom, right, top): the least signed distance of a corner to each wall."""
    xs = [p[0] for p in c]
    ys = [p[1] for p in c]
    return min(xs), min(ys), side - max(xs), side - max(ys)  # type: ignore[operator]


def area_inside(c: list[Pt], side) -> object:
    box = [(mpq(0), mpq(0)), (side, mpq(0)), (side, side), (mpq(0), side)]
    inter = clip_convex(c, box)
    return abs(shoelace2(inter)) / 2 if inter else mpq(0)


def mpq_to_fraction(v) -> Fraction:
    v = mpq(v)
    return Fraction(int(v.numerator), int(v.denominator))


def version() -> str:
    return f"gmpy2 {gmpy2.version()} GMP {gmpy2.mp_version()}"
