"""Lane L174 method B: exact convex clipping in Q(sqrt 2) over GMP rationals.

Each square's four corners are computed from its centre, angle and side.  The closed
intersection of two squares is computed by clipping one square's corner polygon against
the four closed half-planes of the other (Sutherland-Hodgman, exact), and its area by
the shoelace formula.  A pair is

* apart       when the intersection is empty,
* touching    when it is non-empty with area exactly 0,
* overlapping when its area is positive (the interiors of convex sets meet exactly when
  their intersection has positive area).

Each pair is clipped both ways round, and the two areas must be equal.
A square's wall class is decided by clipping it against the closed outer half-plane of
each wall (x <= 0, y <= 0, x >= W, y >= W) the same way; containment is also decided by
area: the square clipped to [0, W]^2 keeps its whole area.  A unit square has four sides
of squared length exactly 1, two diagonals of squared length exactly 2 and area 1.

Signs of ``a + b sqrt 2`` (a, b rational) are decided by bracketing sqrt 2 between
consecutive convergents p/q of its continued fraction (Pell numbers), refined until the
two rational evaluations agree in sign; ``a = b = 0`` is the only zero, since sqrt 2 is
irrational.  No squaring comparison is used.

No pair is skipped: every one of the n(n-1)/2 pairs is decided.
"""

from __future__ import annotations

import hashlib

import gmpy2
from gmpy2 import mpq

from l174_reader import Construction

Q = tuple[mpq, mpq]  # a + b sqrt 2
Point = tuple[Q, Q]

ZERO = mpq(0)
ONE = mpq(1)
HALF = mpq(1, 2)


def _convergents(count: int) -> list[mpq]:
    # sqrt 2 = [1; 2, 2, 2, ...]: p/q with p' = 2p + p_prev, q' = 2q + q_prev
    out = [mpq(1, 1), mpq(3, 2)]
    p0, q0, p1, q1 = 1, 1, 3, 2
    for _ in range(count):
        p0, q0, p1, q1 = p1, q1, 2 * p1 + p0, 2 * q1 + q0
        out.append(mpq(p1, q1))
    return out


_CONV = _convergents(4000)
# Consecutive convergents straddle sqrt 2; start at a pair accurate to about 1e-25.
_START = 32


def qsign(x: Q) -> int:
    a, b = x
    if b == 0:
        return (a > 0) - (a < 0)
    if a == 0:
        return (b > 0) - (b < 0)
    if (a > 0) == (b > 0):
        return 1 if a > 0 else -1
    k = _START
    while k + 1 < len(_CONV):
        lo_val = a + b * _CONV[k]
        hi_val = a + b * _CONV[k + 1]
        if lo_val > 0 and hi_val > 0:
            return 1
        if lo_val < 0 and hi_val < 0:
            return -1
        k += 16
    msg = "sign undecided after 4000 convergents"
    raise ArithmeticError(msg)


def qadd(x: Q, y: Q) -> Q:
    return (x[0] + y[0], x[1] + y[1])


def qsub(x: Q, y: Q) -> Q:
    return (x[0] - y[0], x[1] - y[1])


def qmul(x: Q, y: Q) -> Q:
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def qdiv(x: Q, y: Q) -> Q:
    # x / y = x * conj(y) / (y conj(y)), y conj(y) = c^2 - 2 d^2 (rational, non-zero)
    c, d = y
    norm = c * c - 2 * d * d
    if norm == 0:
        msg = "division by zero in Q(sqrt 2)"
        raise ZeroDivisionError(msg)
    num = qmul(x, (c, -d))
    return (num[0] / norm, num[1] / norm)


def qeq(x: Q, y: Q) -> bool:
    return x[0] == y[0] and x[1] == y[1]


def corners(cx: Q, cy: Q, angle: int, size: mpq) -> list[Point]:
    """Counterclockwise corners."""
    if angle == 0:
        h: Q = (size * HALF, ZERO)
        return [
            (qsub(cx, h), qsub(cy, h)),
            (qadd(cx, h), qsub(cy, h)),
            (qadd(cx, h), qadd(cy, h)),
            (qsub(cx, h), qadd(cy, h)),
        ]
    # 45 degrees: half-diagonal size/sqrt 2 = (size/2) sqrt 2 along the axes
    d: Q = (ZERO, size * HALF)
    return [
        (qadd(cx, d), cy),
        (cx, qadd(cy, d)),
        (qsub(cx, d), cy),
        (cx, qsub(cy, d)),
    ]


def _side_value(a: Point, b: Point, p: Point) -> Q:
    # cross(b - a, p - a): >= 0 on the closed left side of the directed edge a -> b
    ex, ey = qsub(b[0], a[0]), qsub(b[1], a[1])
    px, py = qsub(p[0], a[0]), qsub(p[1], a[1])
    return qsub(qmul(ex, py), qmul(ey, px))


def _clip_halfplane(poly: list[Point], value: list[Q]) -> list[Point]:
    """Keep the closed part of poly where value >= 0 (value given per vertex)."""
    m = len(poly)
    signs = [qsign(v) for v in value]
    out: list[Point] = []
    for idx in range(m):
        cur, nxt = poly[idx], poly[(idx + 1) % m]
        sc, sn = signs[idx], signs[(idx + 1) % m]
        vc, vn = value[idx], value[(idx + 1) % m]
        if sc >= 0:
            out.append(cur)
        if (sc > 0 and sn < 0) or (sc < 0 and sn > 0):
            t = qdiv(vc, qsub(vc, vn))
            out.append(
                (
                    qadd(cur[0], qmul(t, qsub(nxt[0], cur[0]))),
                    qadd(cur[1], qmul(t, qsub(nxt[1], cur[1]))),
                )
            )
    return out


def clip_convex(subject: list[Point], clip: list[Point]) -> list[Point]:
    poly = subject
    m = len(clip)
    for idx in range(m):
        if not poly:
            return poly
        a, b = clip[idx], clip[(idx + 1) % m]
        poly = _clip_halfplane(poly, [_side_value(a, b, p) for p in poly])
    return poly


def area2(poly: list[Point]) -> Q:
    """Twice the signed area (shoelace)."""
    total: Q = (ZERO, ZERO)
    m = len(poly)
    for idx in range(m):
        x0, y0 = poly[idx]
        x1, y1 = poly[(idx + 1) % m]
        total = qadd(total, qsub(qmul(x0, y1), qmul(x1, y0)))
    return total


def _halfplane_clip(poly: list[Point], fn: object) -> list[Point]:
    return _clip_halfplane(poly, [fn(p) for p in poly])  # pyright: ignore[reportCallIssue]


class Prepared:
    def __init__(self, con: Construction) -> None:
        def q(p: tuple[object, object]) -> Q:
            return (mpq(p[0]), mpq(p[1]))  # pyright: ignore[reportCallIssue, reportArgumentType]

        self.width: Q = q(con.container)
        self.polys: list[list[Point]] = [
            corners(q(s.cx), q(s.cy), s.angle, mpq(s.size)) for s in con.squares  # pyright: ignore[reportCallIssue, reportArgumentType]
        ]


def pair_class(prep: Prepared, i: int, j: int) -> tuple[int, Q]:
    pi, pj = prep.polys[i], prep.polys[j]
    one = clip_convex(pi, pj)
    two = clip_convex(pj, pi)
    if bool(one) != bool(two):
        msg = f"clipping disagrees on emptiness for pair ({i}, {j})"
        raise AssertionError(msg)
    if not one:
        return 1, (ZERO, ZERO)
    a1, a2 = area2(one), area2(two)
    if not qeq(a1, a2):
        msg = f"clipping areas differ for pair ({i}, {j}): {a1} vs {a2}"
        raise AssertionError(msg)
    s = qsign(a1)
    if s < 0:
        msg = f"negative area for pair ({i}, {j})"
        raise AssertionError(msg)
    return (0 if s == 0 else -1), a1


def wall_classes(prep: Prepared, i: int) -> tuple[tuple[int, int, int, int], bool]:
    """Classes against left, bottom, right, top (+1 clear, 0 touching, -1 crossing),
    and whether the square clipped to the container keeps its whole area."""
    w = prep.width
    poly = prep.polys[i]
    outer = (
        lambda p: qsub((ZERO, ZERO), p[0]),  # x <= 0
        lambda p: qsub((ZERO, ZERO), p[1]),  # y <= 0
        lambda p: qsub(p[0], w),  # x >= W
        lambda p: qsub(p[1], w),  # y >= W
    )
    classes: list[int] = []
    for fn in outer:
        part = _halfplane_clip(poly, fn)
        if not part:
            classes.append(1)
        else:
            classes.append(0 if qsign(area2(part)) == 0 else -1)
    inner = (
        lambda p: p[0],
        lambda p: p[1],
        lambda p: qsub(w, p[0]),
        lambda p: qsub(w, p[1]),
    )
    inside = poly
    for fn in inner:
        if not inside:
            break
        inside = _halfplane_clip(inside, fn)
    kept = bool(inside) and qeq(area2(inside), area2(poly))
    return (classes[0], classes[1], classes[2], classes[3]), kept


def unit_square(poly: list[Point]) -> bool:
    def d2(p: Point, r: Point) -> Q:
        dx, dy = qsub(r[0], p[0]), qsub(r[1], p[1])
        return qadd(qmul(dx, dx), qmul(dy, dy))

    one: Q = (ONE, ZERO)
    two: Q = (mpq(2), ZERO)
    sides = all(qeq(d2(poly[k], poly[(k + 1) % 4]), one) for k in range(4))
    diagonals = qeq(d2(poly[0], poly[2]), two) and qeq(d2(poly[1], poly[3]), two)
    area = qeq(area2(poly), two)  # twice the area
    return sides and diagonals and area


def decide(con: Construction) -> dict[str, object]:
    prep = Prepared(con)
    n = len(con.squares)
    digest = hashlib.sha256()
    counts = {1: 0, 0: 0, -1: 0}
    touching: list[tuple[int, int]] = []
    overlapping: list[tuple[int, int]] = []
    overlap_areas: list[list[str]] = []
    for i in range(n):
        row = bytearray()
        for j in range(i + 1, n):
            c, a2 = pair_class(prep, i, j)
            counts[c] += 1
            row.append(c + 1)
            if c == 0:
                touching.append((i, j))
            elif c < 0:
                overlapping.append((i, j))
                overlap_areas.append([str(a2[0] / 2), str(a2[1] / 2)])
        digest.update(bytes(row))
    walls: list[tuple[int, int, int, int]] = []
    inside: list[bool] = []
    for i in range(n):
        cls, kept = wall_classes(prep, i)
        walls.append(cls)
        inside.append(kept)
    wall_digest = hashlib.sha256(bytes(c + 1 for w in walls for c in w)).hexdigest()
    return {
        "method": "B: exact convex clipping in Q(sqrt 2) over gmpy2.mpq, signs by Pell brackets",
        "gmpy2": gmpy2.version(),
        "n": n,
        "pairs": n * (n - 1) // 2,
        "apart": counts[1],
        "touching": counts[0],
        "overlapping": counts[-1],
        "touching_pairs": touching,
        "overlapping_pairs": overlapping,
        "overlap_areas": overlap_areas,
        "pair_class_sha256": digest.hexdigest(),
        "walls": walls,
        "wall_class_sha256": wall_digest,
        "inside_by_area": inside,
        "unit": [unit_square(p) for p in prep.polys],
    }
