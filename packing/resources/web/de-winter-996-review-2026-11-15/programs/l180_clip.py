"""Lane L180 method B: exact convex clipping of corners, in GMP rationals.

Written for the blind stage 4 review of issue #996 as a clean-room implementation.
It imports nothing from this repository or the source, and reuses no code of any
earlier review. It is handed four corners per square and uses nothing else: no
centre, no direction, no angle.

- **A unit square.** Four points in cyclic order are a unit square exactly when the
  four sides have squared length 1 and both diagonals squared length 2 (the converse
  of Pythagoras puts right angles at the second and fourth points, which are then the
  two distinct points at distance 1 from both the first and the third). The listing's
  sense is the sign of the shoelace sum, which is then +2 or -2; a clockwise listing is
  reversed before clipping.
- **A pair.** One square is clipped against the four closed half-planes to the left of
  the other's counterclockwise edges (Sutherland-Hodgman, keeping boundary points), so
  the result is the intersection exactly. Empty is apart; non-empty with zero area is
  contact (the interior of an intersection of convex sets is the intersection of their
  interiors); positive area is overlap, by that area. Every pair is clipped both ways
  round, and the two results must agree in class and area.
- **A wall.** The square is clipped against the closed half-plane outside the wall:
  empty is inside, zero area is contact, positive area is crossing.
- **Containment.** The square lies in [0, S]^2 exactly when its intersection with the
  box has area exactly 1.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from fractions import Fraction

from gmpy2 import mpq

APART, TOUCH, OVERLAP = "apart", "touch", "overlap"
INSIDE, CROSS = "inside", "cross"

Pt = tuple[mpq, mpq]
Lin = Callable[[Pt], mpq]

ZERO = mpq(0)


def to_mpq(corners: Sequence[tuple[Fraction, Fraction]]) -> list[Pt]:
    return [(mpq(x.numerator, x.denominator), mpq(y.numerator, y.denominator)) for x, y in corners]


def _d2(p: Pt, q: Pt) -> mpq:
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def shoelace2(poly: Sequence[Pt]) -> mpq:
    """Twice the signed area of a polygon listed in order."""
    total = ZERO
    n = len(poly)
    for k in range(n):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % n]
        total += x0 * y1 - x1 * y0
    return total


def unit_square(c: Sequence[Pt]) -> tuple[bool, int]:
    """(is a unit square in cyclic order, listing sense +1 counterclockwise or -1)."""
    if len(c) != 4:
        return False, 0
    sides = all(_d2(c[k], c[(k + 1) % 4]) == 1 for k in range(4))
    diagonals = _d2(c[0], c[2]) == 2 and _d2(c[1], c[3]) == 2
    if not (sides and diagonals):
        return False, 0
    a2 = shoelace2(c)
    if a2 == 2:
        return True, 1
    if a2 == -2:
        return True, -1
    return False, 0


def ccw(c: Sequence[Pt]) -> list[Pt]:
    """The listing counterclockwise (the caller has checked it is a unit square)."""
    return list(c) if shoelace2(c) > 0 else list(reversed(c))


def clip_by(poly: list[Pt], f: Lin) -> list[Pt]:
    """Keep the part of a convex polygon where the affine function f is >= 0."""
    out: list[Pt] = []
    n = len(poly)
    for k in range(n):
        cur = poly[k]
        prev = poly[k - 1]
        fc = f(cur)
        fp = f(prev)
        if fc >= 0:
            if fp < 0:
                t = fp / (fp - fc)
                out.append((prev[0] + t * (cur[0] - prev[0]), prev[1] + t * (cur[1] - prev[1])))
            out.append(cur)
        elif fp >= 0:
            t = fp / (fp - fc)
            out.append((prev[0] + t * (cur[0] - prev[0]), prev[1] + t * (cur[1] - prev[1])))
    return out


def _left_of(a: Pt, b: Pt) -> Lin:
    ex = b[0] - a[0]
    ey = b[1] - a[1]

    def f(p: Pt) -> mpq:
        return ex * (p[1] - a[1]) - ey * (p[0] - a[0])

    return f


def intersect(p: list[Pt], q_ccw: list[Pt]) -> list[Pt]:
    """The intersection of convex polygon p with the convex polygon q (counterclockwise)."""
    out = p
    for k in range(len(q_ccw)):
        out = clip_by(out, _left_of(q_ccw[k], q_ccw[(k + 1) % len(q_ccw)]))
        if not out:
            return out
    return out


def area(poly: list[Pt]) -> mpq:
    return abs(shoelace2(poly)) / 2 if len(poly) >= 3 else ZERO


def _classify(inter: list[Pt]) -> tuple[str, mpq]:
    if not inter:
        return APART, ZERO
    a = area(inter)
    return (TOUCH, a) if a == 0 else (OVERLAP, a)


def pair(p_ccw: list[Pt], q_ccw: list[Pt]) -> tuple[str, mpq, bool]:
    """(class, overlap area, the two clipping orders agree)."""
    c1, a1 = _classify(intersect(p_ccw, q_ccw))
    c2, a2 = _classify(intersect(q_ccw, p_ccw))
    return c1, a1, (c1 == c2 and a1 == a2)


def wall_functions(side: mpq) -> dict[str, Lin]:
    """For each wall, the affine function that is >= 0 on the closed outside of it."""
    return {
        "left": lambda p: -p[0],
        "bottom": lambda p: -p[1],
        "right": lambda p: p[0] - side,
        "top": lambda p: p[1] - side,
    }


def walls(sq_ccw: list[Pt], side: mpq) -> dict[str, tuple[str, mpq]]:
    out: dict[str, tuple[str, mpq]] = {}
    for name, f in wall_functions(side).items():
        part = clip_by(list(sq_ccw), f)
        if not part:
            out[name] = (INSIDE, ZERO)
        else:
            a = area(part)
            out[name] = (TOUCH, a) if a == 0 else (CROSS, a)
    return out


def area_inside(sq_ccw: list[Pt], side: mpq) -> mpq:
    box: list[Pt] = [(ZERO, ZERO), (side, ZERO), (side, side), (ZERO, side)]
    return area(intersect(list(sq_ccw), box))
