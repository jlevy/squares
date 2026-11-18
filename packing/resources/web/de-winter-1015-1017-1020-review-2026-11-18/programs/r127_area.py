"""Method B: the exact intersection of two convex polygons by vertex enumeration, in GMP
rationals (gmpy2.mpq).

Lane r127-1118.  Written for this review; imports nothing from the repository and
nothing from method A.

Four points are a unit square in cyclic order when all four sides have squared length 1
and both diagonals squared length 2.  The shoelace sum, +-2, gives the sense, and a
clockwise listing is reversed before use.

The intersection of two closed convex polygons P and Q is the convex hull of: the
vertices of P lying in closed Q, the vertices of Q lying in closed P, and the points
where an edge of P meets a non-parallel edge of Q (both closed segments).  An extreme
point of the intersection that is a vertex of neither polygon lies on an edge of each,
and those edges cannot be parallel (two parallel edges meet in a segment whose
endpoints are vertices of one polygon or the other), so the hull is the whole
intersection.  No point: apart.  A hull of zero area: contact (the interior of an
intersection of convex sets is the intersection of their interiors).  Positive area:
overlap, by exactly that area.

A wall is classed by intersecting the square with the closed half-plane outside it, by
the same enumeration against a large box beyond the wall; containment is decided
apart: a unit square lies in the box exactly when its intersection with the box has
area exactly 1.
"""

from __future__ import annotations

from gmpy2 import mpq

ZERO = mpq(0)


def to_mpq(pts):
    return [(mpq(x.numerator, x.denominator), mpq(y.numerator, y.denominator)) for x, y in pts]


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def shoelace2(pts):
    s = ZERO
    k = len(pts)
    for i in range(k):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % k]
        s += x1 * y2 - x2 * y1
    return s


def unit_square(pts) -> tuple[bool, int]:
    """(is a unit square in cyclic order, sense +1 ccw / -1 cw / 0)."""
    def d2(p, q):
        return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2
    ok = all(d2(pts[k], pts[(k + 1) % 4]) == 1 for k in range(4))
    ok = ok and d2(pts[0], pts[2]) == 2 and d2(pts[1], pts[3]) == 2
    s = shoelace2(pts)
    sense = 1 if s > 0 else (-1 if s < 0 else 0)
    ok = ok and (s == 2 or s == -2)
    return ok, sense


def ccw(pts):
    return pts if shoelace2(pts) > 0 else list(reversed(pts))


def inside_closed(p, poly) -> bool:
    k = len(poly)
    return all(cross(poly[i], poly[(i + 1) % k], p) >= 0 for i in range(k))


def seg_intersections(P, Q):
    out = []
    kp, kq = len(P), len(Q)
    for i in range(kp):
        a, b = P[i], P[(i + 1) % kp]
        rx, ry = b[0] - a[0], b[1] - a[1]
        for j in range(kq):
            c, d = Q[j], Q[(j + 1) % kq]
            sx, sy = d[0] - c[0], d[1] - c[1]
            den = rx * sy - ry * sx
            if den == 0:
                continue
            qpx, qpy = c[0] - a[0], c[1] - a[1]
            t = (qpx * sy - qpy * sx) / den
            u = (qpx * ry - qpy * rx) / den
            if 0 <= t <= 1 and 0 <= u <= 1:
                out.append((a[0] + t * rx, a[1] + t * ry))
    return out


def hull(points):
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower: list = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def intersection(P, Q):
    """Return (number of candidate points, exact area of P cap Q); P, Q ccw convex."""
    cand = [p for p in P if inside_closed(p, Q)]
    cand += [q for q in Q if inside_closed(q, P)]
    cand += seg_intersections(P, Q)
    if not cand:
        return 0, ZERO
    h = hull(cand)
    area = shoelace2(h) / 2 if len(h) >= 3 else ZERO
    return len(cand), area


def pair_class(P, Q) -> tuple[str, object]:
    npts, area = intersection(P, Q)
    if npts == 0:
        return "apart", ZERO
    if area == 0:
        return "contact", ZERO
    return "overlap", area


def box(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def wall_classes(P, side):
    """Per wall (left, bottom, right, top): 'clear', 'touch' or 'cross', and the area
    of P inside [0, side]^2."""
    big = side + 4
    halves = [
        box(-big, -big, ZERO, big + side),  # x <= 0
        box(-big, -big, big + side, ZERO),  # y <= 0
        box(side, -big, side + big, big + side),  # x >= side
        box(-big, side, big + side, side + big),  # y >= side
    ]
    out = []
    for h in halves:
        npts, area = intersection(P, h)
        out.append("clear" if npts == 0 else ("touch" if area == 0 else "cross"))
    _, inside = intersection(P, box(ZERO, ZERO, side, side))
    return out, inside


def decide(corners_list, side_fraction, pairs=None):
    """Return (units, senses, wall classes, areas inside, {pair: (class, area)})."""
    side = mpq(side_fraction.numerator, side_fraction.denominator)
    raw = [to_mpq(c) for c in corners_list]
    units, senses, polys = [], [], []
    for pts in raw:
        ok, sense = unit_square(pts)
        units.append(ok)
        senses.append(sense)
        polys.append(ccw(pts))
    wl, ins = [], []
    for P in polys:
        w, a = wall_classes(P, side)
        wl.append(w)
        ins.append(a)
    n = len(polys)
    if pairs is None:
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
    pc = {(i, j): pair_class(polys[i], polys[j]) for i, j in pairs}
    return units, senses, wl, ins, pc
