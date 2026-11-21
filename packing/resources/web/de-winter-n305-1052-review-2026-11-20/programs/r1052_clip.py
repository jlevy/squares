"""Method B of lane r1052: exact convex clipping of corners, in GMP rationals.

Method B is handed the side and the corners, or poses from which it writes the corners
itself as c - u/2 - v/2, c + u/2 - v/2, c + u/2 + v/2, c - u/2 + v/2 with v the quarter
turn of u. Four points are a unit square in cyclic order exactly when the four sides have
squared length 1 and both diagonals squared length 2: four equal sides close into a
rhombus, or fold onto a figure whose diagonal vanishes, and a rhombus with equal
diagonals is a square. Twice the signed area, +2 or -2, gives the sense; a clockwise
square is reversed before it is used.

A pair is decided by clipping one square against the four closed half-planes to the left
of the other's counterclockwise edges (Sutherland-Hodgman, keeping points on the line),
which yields their intersection exactly, both ways round; the two results must agree in
class and area. Empty is apart; non-empty with zero area is contact, since the interior
of an intersection of convex sets is the intersection of their interiors; positive area
is overlap, by that area. For a pair apart, the squared Euclidean distance is the least
squared distance from a vertex of one square to an edge of the other, exactly.

Each wall is classed by clipping the square against the closed half-plane outside it, and
containment is decided apart: a unit square lies in the box exactly when its intersection
with the box has area exactly 1. The clearance to each wall is read off the corners.

Method B shares the reader with method A and nothing else.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Any

from gmpy2 import mpq

Point = tuple[Any, Any]

HALF = mpq(1, 2)


def q(value: Fraction) -> Any:
    return mpq(value.numerator, value.denominator)


def fr(value: Any) -> Fraction:
    value = mpq(value)
    return Fraction(int(value.numerator), int(value.denominator))


def corners_from_pose(x: Fraction, y: Fraction, a: Fraction, b: Fraction) -> list[Point]:
    cx, cy, ux, uy = q(x), q(y), q(a) * HALF, q(b) * HALF
    vx, vy = -uy, ux
    return [
        (cx - ux - vx, cy - uy - vy),
        (cx + ux - vx, cy + uy - vy),
        (cx + ux + vx, cy + uy + vy),
        (cx - ux + vx, cy - uy + vy),
    ]


def twice_area(poly: list[Point]) -> Any:
    total = mpq(0)
    m = len(poly)
    for k in range(m):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % m]
        total += x0 * y1 - x1 * y0
    return total


def unit_square(poly: list[Point]) -> tuple[bool, int]:
    """(is a unit square in cyclic order, sense +1 or -1)."""
    for k in range(4):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % 4]
        if (x1 - x0) ** 2 + (y1 - y0) ** 2 != 1:
            return False, 0
    for k in (0, 1):
        x0, y0 = poly[k]
        x2, y2 = poly[k + 2]
        if (x2 - x0) ** 2 + (y2 - y0) ** 2 != 2:
            return False, 0
    s = twice_area(poly)
    if s == 2:
        return True, 1
    if s == -2:
        return True, -1
    return False, 0


def clip_line(poly: list[Point], a: Any, b: Any, c: Any) -> list[Point]:
    """Keep the part of a convex polygon where a x + b y + c >= 0."""
    out: list[Point] = []
    m = len(poly)
    if m == 0:
        return out
    f = [a * x + b * y + c for x, y in poly]
    for k in range(m):
        s, e = poly[k - 1], poly[k]
        fs, fe = f[k - 1], f[k]
        if fe >= 0:
            if fs < 0:
                t = fs / (fs - fe)
                out.append((s[0] + t * (e[0] - s[0]), s[1] + t * (e[1] - s[1])))
            out.append(e)
        elif fs >= 0:
            t = fs / (fs - fe)
            out.append((s[0] + t * (e[0] - s[0]), s[1] + t * (e[1] - s[1])))
    return out


def clip_by(poly: list[Point], ccw: list[Point]) -> list[Point]:
    """The part of a convex polygon inside a counterclockwise convex polygon, closed."""
    out = poly
    m = len(ccw)
    for k in range(m):
        x0, y0 = ccw[k]
        x1, y1 = ccw[(k + 1) % m]
        # left of the edge (x0, y0) -> (x1, y1): (x1 - x0)(y - y0) - (y1 - y0)(x - x0) >= 0
        a = -(y1 - y0)
        b = x1 - x0
        c = (y1 - y0) * x0 - (x1 - x0) * y0
        out = clip_line(out, a, b, c)
        if not out:
            break
    return out


def area_class(poly: list[Point], kind: str) -> tuple[str, Any]:
    if not poly:
        return "apart", mpq(0)
    s = twice_area(poly)
    if s < 0:
        raise AssertionError("a clipped polygon turned clockwise")
    if s == 0:
        return "contact", s
    return kind, s


def seg_dist2(p: Point, a: Point, b: Point) -> Any:
    abx, aby = b[0] - a[0], b[1] - a[1]
    apx, apy = p[0] - a[0], p[1] - a[1]
    t = (apx * abx + apy * aby) / (abx * abx + aby * aby)
    if t < 0:
        t = mpq(0)
    elif t > 1:
        t = mpq(1)
    dx, dy = apx - t * abx, apy - t * aby
    return dx * dx + dy * dy


def gap2(p: list[Point], r: list[Point]) -> Any:
    best = None
    for one, other in ((p, r), (r, p)):
        for v in one:
            for k in range(4):
                d = seg_dist2(v, other[k], other[(k + 1) % 4])
                if best is None or d < best:
                    best = d
    return best


def pair(p: list[Point], r: list[Point], *, distance: bool = True) -> tuple[str, Any, Any]:
    """(class, twice the intersection's area, squared gap if apart) of two ccw unit squares."""
    one = area_class(clip_by(r, p), "overlap")
    two = area_class(clip_by(p, r), "overlap")
    if one != two:
        return "disagree", one[1], None
    g = gap2(p, r) if (one[0] == "apart" and distance) else None
    return one[0], one[1], g


def walls(side: Any, p: list[Point]) -> dict[str, Any]:
    """Each wall's class by clipping, containment by area, and the clearances."""
    z, one = mpq(0), mpq(1)
    outside = {
        "left": (-one, z, z),  # x <= 0
        "bottom": (z, -one, z),  # y <= 0
        "right": (one, z, -side),  # x >= side
        "top": (z, one, -side),  # y >= side
    }
    classes = {}
    for name, (a, b, c) in outside.items():
        cls, _ = area_class(clip_line(p, a, b, c), "crossing")
        classes[name] = cls
    box = [(z, z), (side, z), (side, side), (z, side)]
    inside2 = twice_area(clip_by(p, box)) if p else mpq(0)
    xs = [pt[0] for pt in p]
    ys = [pt[1] for pt in p]
    clear = (min(xs), min(ys), side - max(xs), side - max(ys))
    return {"classes": classes, "inside2": inside2, "clearances": clear}


def run(
    side: Fraction,
    *,
    poses: list[tuple[Fraction, Fraction, Fraction, Fraction]] | None = None,
    corners: list[list[tuple[Fraction, Fraction]]] | None = None,
    distance: bool = True,
) -> dict[str, Any]:
    """Decide every square, wall and pair. No pair is skipped and nothing is rounded."""
    if (poses is None) == (corners is None):
        raise ValueError("give poses or corners")
    s = q(side)
    if corners is not None:
        polys = [[(q(x), q(y)) for x, y in sq] for sq in corners]
    else:
        assert poses is not None
        polys = [corners_from_pose(*pose) for pose in poses]
    unit: list[bool] = []
    sense: list[int] = []
    ccw: list[list[Point] | None] = []
    for poly in polys:
        ok, sg = unit_square(poly)
        unit.append(ok)
        sense.append(sg)
        ccw.append(None if not ok else (poly if sg == 1 else poly[::-1]))
    wall_rows: list[dict[str, Any] | None] = [None if p is None else walls(s, p) for p in ccw]
    n = len(ccw)
    pairs: dict[tuple[int, int], tuple[str, Any, Any]] = {}
    for i in range(n):
        pi = ccw[i]
        if pi is None:
            continue
        for j in range(i + 1, n):
            pj = ccw[j]
            if pj is None:
                continue
            pairs[(i, j)] = pair(pi, pj, distance=distance)
    return {"unit": unit, "sense": sense, "walls": wall_rows, "pairs": pairs, "n": n}
