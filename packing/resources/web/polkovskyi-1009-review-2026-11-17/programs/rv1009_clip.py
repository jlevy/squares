"""Method B: exact convex clipping in GMP rationals, from corners and nothing else.

Lane c-review-1009-1117, stage 4 blind review of issue #1009. Clean-room.

A square is four points. They are a unit square in cyclic order exactly when all four
sides have squared length 1 and both diagonals squared length 2: each triple of
consecutive corners is then a right isosceles triangle with legs 1, and the fourth corner
is forced. The shoelace sum, +2 or -2, gives the sense of the listing; a clockwise
listing is reversed before clipping.

A pair is decided by clipping one square against the four closed half-planes to the left
of the other's counterclockwise edges (Sutherland-Hodgman, keeping points on the line).
For convex polygons this is the intersection of the two closed squares exactly. Empty is
apart; non-empty with zero area is contact, since the interior of an intersection of
convex sets is the intersection of their interiors; positive area is overlap, by that
area. A wall is classed the same way, by clipping the square against the closed
half-plane outside it, and containment is decided apart: a unit square lies in the closed
box exactly when its intersection with the box has area exactly 1.
"""

from __future__ import annotations

from gmpy2 import mpq

Point = tuple[mpq, mpq]
ZERO = mpq(0)
ONE = mpq(1)
TWO = mpq(2)


def points(corners: object) -> list[Point]:
    """Four corners given as pairs of ``(numerator, denominator)`` to GMP rationals."""
    return [(mpq(xn, xd), mpq(yn, yd)) for (xn, xd), (yn, yd) in corners]  # type: ignore[union-attr]


def _dist2(p: Point, q: Point) -> mpq:
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def twice_area(poly: list[Point]) -> mpq:
    """Twice the signed area of a polygon: positive when counterclockwise."""
    total = ZERO
    count = len(poly)
    for k in range(count):
        p = poly[k]
        q = poly[(k + 1) % count]
        total += p[0] * q[1] - q[0] * p[1]
    return total


def unit_sense(quad: list[Point]) -> int:
    """+1 for a unit square listed counterclockwise, -1 clockwise, 0 for anything else."""
    if len(quad) != 4:
        return 0
    for k in range(4):
        if _dist2(quad[k], quad[(k + 1) % 4]) != ONE:
            return 0
    if _dist2(quad[0], quad[2]) != TWO or _dist2(quad[1], quad[3]) != TWO:
        return 0
    area2 = twice_area(quad)
    if area2 == TWO:
        return 1
    if area2 == -TWO:
        return -1
    return 0


def counterclockwise(quad: list[Point]) -> list[Point]:
    """The same unit square listed counterclockwise."""
    sense = unit_sense(quad)
    if sense == 0:
        msg = "not a unit square"
        raise ValueError(msg)
    return list(quad) if sense == 1 else [quad[0], quad[3], quad[2], quad[1]]


def clip_line(poly: list[Point], a: mpq, b: mpq, c: mpq) -> list[Point]:
    """The part of a convex polygon in the closed half-plane ``a*x + b*y + c >= 0``."""
    out: list[Point] = []
    count = len(poly)
    if count == 0:
        return out
    values = [a * p[0] + b * p[1] + c for p in poly]
    for k in range(count):
        cur = poly[k]
        prev = poly[k - 1]
        vc = values[k]
        vp = values[k - 1]
        if vc >= 0:
            if vp < 0:
                s = vp / (vp - vc)
                out.append((prev[0] + s * (cur[0] - prev[0]), prev[1] + s * (cur[1] - prev[1])))
            out.append(cur)
        elif vp >= 0:
            s = vp / (vp - vc)
            out.append((prev[0] + s * (cur[0] - prev[0]), prev[1] + s * (cur[1] - prev[1])))
    return out


def edge_lines(clipper: list[Point]) -> list[tuple[mpq, mpq, mpq]]:
    """For each directed edge p -> q of a counterclockwise polygon, the line
    ``a*x + b*y + c`` that is non-negative exactly on its left: (q - p) x (z - p)."""
    out = []
    count = len(clipper)
    for k in range(count):
        p = clipper[k]
        q = clipper[(k + 1) % count]
        out.append((p[1] - q[1], q[0] - p[0], p[0] * q[1] - q[0] * p[1]))
    return out


def clip_convex(
    subject: list[Point], clipper: list[Point], lines: list[tuple[mpq, mpq, mpq]] | None = None
) -> list[Point]:
    """The intersection of a convex polygon with a counterclockwise convex polygon;
    ``lines`` are the clipper's ``edge_lines`` when the caller has them already."""
    out = list(subject)
    for a, b, c in edge_lines(clipper) if lines is None else lines:
        out = clip_line(out, a, b, c)
        if not out:
            break
    return out


def _class_of(poly: list[Point]) -> tuple[str, mpq]:
    if not poly:
        return "apart", ZERO
    area2 = twice_area(poly)
    if area2 == 0:
        return "touch", ZERO
    if area2 > 0:
        return "overlap", area2 / 2
    msg = "negative area from a counterclockwise subject"
    raise ArithmeticError(msg)


def pair_class(
    qi: list[Point],
    qj: list[Point],
    li: list[tuple[mpq, mpq, mpq]] | None = None,
    lj: list[tuple[mpq, mpq, mpq]] | None = None,
) -> tuple[str, mpq]:
    """Class and overlap area of two counterclockwise unit squares, clipped both ways;
    ``li`` and ``lj`` are their ``edge_lines`` when the caller has them already."""
    one = _class_of(clip_convex(qj, qi, li))
    two = _class_of(clip_convex(qi, qj, lj))
    if one != two:
        msg = f"the two clipping orders disagree: {one} and {two}"
        raise ArithmeticError(msg)
    return one


def wall_classes(quad: list[Point], side: mpq) -> tuple[tuple[str, mpq], ...]:
    """Class at (left, bottom, right, top): what of the square lies in the closed
    half-plane outside each wall of ``[0, side]^2``; ``apart`` is clear, ``touch`` is
    contact, ``overlap`` is crossing, with the area outside."""
    return (
        _class_of(clip_line(quad, -ONE, ZERO, ZERO)),
        _class_of(clip_line(quad, ZERO, -ONE, ZERO)),
        _class_of(clip_line(quad, ONE, ZERO, -side)),
        _class_of(clip_line(quad, ZERO, ONE, -side)),
    )


def area_in_box(quad: list[Point], side: mpq) -> mpq:
    """The area of the square's intersection with the closed box ``[0, side]^2``."""
    poly = clip_line(quad, ONE, ZERO, ZERO)
    poly = clip_line(poly, ZERO, ONE, ZERO)
    poly = clip_line(poly, -ONE, ZERO, side)
    poly = clip_line(poly, ZERO, -ONE, side)
    if not poly:
        return ZERO
    return twice_area(poly) / 2
