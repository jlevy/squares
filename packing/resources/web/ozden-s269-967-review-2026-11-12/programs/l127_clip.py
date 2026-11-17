"""Method B: unit squares, walls and pairs by exact convex clipping in GMP rationals.

Lane L127, clean room. Shares only the reader's integers with method A.

Unit square. Four points P0..P3 with all four sides of squared length 1 and both
diagonals of squared length 2 are a unit square listed in cyclic order: |P0P1| =
|P1P2| = 1 and |P0P2|^2 = 2 put a right angle at P1 (converse of Pythagoras), likewise
at P3; P1 and P3 are then the two points at distance 1 from both P0 and P2, which are
distinct because |P1P3|^2 = 2, so they lie on opposite sides of P0P2. The listing sense
is the sign of the shoelace sum, which is then exactly +2 or -2.

Pairs. The intersection of two closed convex polygons is computed by clipping one
against the closed half-planes of the other's edges (Sutherland-Hodgman, keeping points
on the boundary). The result is the intersection exactly. Empty: apart. Non-empty with
zero area: touching, since the interior of an intersection of convex sets is the
intersection of their interiors. Positive area: overlapping, by that area. Clipping stops
when the polygon becomes empty, since the intersection is then empty.

Walls. Each wall is the closed half-plane outside it (x <= 0, y <= 0, x >= S, y >= S);
the square is clipped against it and classed the same way: empty is clear of that wall,
zero area touches it, positive area crosses it. Containment is decided separately: a
unit square lies in [0, S]^2 exactly when its intersection with the box, clipped against
the box's four closed inner half-planes, has area exactly 1 (a point of the square
outside the closed box has a neighbourhood outside it, which meets the square's
interior in positive area).
"""

from __future__ import annotations

from dataclasses import dataclass

from gmpy2 import mpq

Pt = tuple[mpq, mpq]


@dataclass(frozen=True)
class SquareB:
    ccw: tuple[Pt, ...]  # the corners in counterclockwise order
    sense: int  # +1 if listed counterclockwise, -1 if clockwise


class NotUnit(Exception):
    """The four corners are not a unit square in cyclic order."""


def _d2(p: Pt, q: Pt) -> mpq:
    dx = q[0] - p[0]
    dy = q[1] - p[1]
    return dx * dx + dy * dy


def shoelace2(poly: list[Pt] | tuple[Pt, ...]) -> mpq:
    """Twice the signed area."""
    s = mpq(0)
    n = len(poly)
    for k in range(n):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % n]
        s += x0 * y1 - x1 * y0
    return s


def make_square(corners: list[tuple[tuple[int, int], tuple[int, int]]]) -> SquareB:
    pts = tuple((mpq(xp, xq), mpq(yp, yq)) for (xp, xq), (yp, yq) in corners)
    one, two = mpq(1), mpq(2)
    for k in range(4):
        if _d2(pts[k], pts[(k + 1) % 4]) != one:
            msg = f"side {k} is not of length 1"
            raise NotUnit(msg)
    if _d2(pts[0], pts[2]) != two or _d2(pts[1], pts[3]) != two:
        msg = "a diagonal is not of squared length 2"
        raise NotUnit(msg)
    a2 = shoelace2(pts)
    if a2 == two:
        return SquareB(ccw=pts, sense=1)
    if a2 == -two:
        return SquareB(ccw=tuple(reversed(pts)), sense=-1)
    msg = "shoelace sum is not +-2"
    raise NotUnit(msg)


def _side(a: Pt, b: Pt, p: Pt) -> mpq:
    """Cross product (b - a) x (p - a): >= 0 is the closed left half-plane of a->b."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def clip_halfplane(poly: list[Pt], a: Pt, b: Pt, *, keep_boundary: bool = True) -> list[Pt]:
    """Clip a convex polygon (possibly degenerate) to the closed left half-plane of a->b.

    `keep_boundary=False` is the deliberately broken open variant the self-test uses.
    """
    out: list[Pt] = []
    n = len(poly)
    for k in range(n):
        p = poly[k]
        q = poly[(k + 1) % n]
        sp = _side(a, b, p)
        sq = _side(a, b, q)
        inside = sp >= 0 if keep_boundary else sp > 0
        if inside:
            out.append(p)
        if (sp > 0 and sq < 0) or (sp < 0 and sq > 0):
            t = sp / (sp - sq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def clip_convex(poly: list[Pt], clipper_ccw: tuple[Pt, ...], *, keep_boundary: bool = True) -> list[Pt]:
    cur = list(poly)
    m = len(clipper_ccw)
    for k in range(m):
        if not cur:
            return cur
        cur = clip_halfplane(cur, clipper_ccw[k], clipper_ccw[(k + 1) % m], keep_boundary=keep_boundary)
    return cur


def classify(poly: list[Pt]) -> tuple[str, mpq]:
    if not poly:
        return "apart", mpq(0)
    area = abs(shoelace2(poly)) / 2
    if area == 0:
        return "touch", area
    return "overlap", area


def pair(a: SquareB, b: SquareB, *, keep_boundary: bool = True) -> tuple[str, mpq]:
    """Class and overlap area of two squares."""
    return classify(clip_convex(list(b.ccw), a.ccw, keep_boundary=keep_boundary))


def _outer_halfplane(wall: str, s: mpq) -> tuple[Pt, Pt]:
    """Two points a, b whose closed left half-plane is the outside of the wall."""
    z = mpq(0)
    o = mpq(1)
    if wall == "left":  # x <= 0: direction (0, 1) from (0, 0); left side is x <= 0
        return (z, z), (z, o)
    if wall == "bottom":  # y <= 0: direction (-1, 0) from (0, 0)
        return (z, z), (-o, z)
    if wall == "right":  # x >= s: direction (0, -1) from (s, 0)
        return (s, z), (s, -o)
    if wall == "top":  # y >= s: direction (1, 0) from (0, s)
        return (z, s), (o, s)
    msg = f"unknown wall {wall}"
    raise ValueError(msg)


WALLS = ("left", "bottom", "right", "top")


def wall_classes(sq: SquareB, side: tuple[int, int], *, keep_boundary: bool = True) -> dict[str, str]:
    s = mpq(*side)
    out: dict[str, str] = {}
    for wall in WALLS:
        a, b = _outer_halfplane(wall, s)
        poly = clip_halfplane(list(sq.ccw), a, b, keep_boundary=keep_boundary)
        if not poly:
            out[wall] = "clear"
        elif shoelace2(poly) == 0:
            out[wall] = "touch"
        else:
            out[wall] = "outside"
    return out


def inside_box(sq: SquareB, side: tuple[int, int], *, keep_boundary: bool = True) -> bool:
    s = mpq(*side)
    z = mpq(0)
    box = ((z, z), (s, z), (s, s), (z, s))
    poly = clip_convex(list(sq.ccw), box, keep_boundary=keep_boundary)
    return bool(poly) and abs(shoelace2(poly)) == 2
