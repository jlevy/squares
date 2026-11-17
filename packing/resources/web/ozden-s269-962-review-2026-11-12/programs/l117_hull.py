"""Lane L117, method B: the intersection as a convex hull, in gmpy2 rationals.

Clean-room code for the stage 4 review of jlevy/squares#962.

Unit squares. A quadrilateral p_0..p_3 is a unit square exactly when each of its four
edges e_k = p_{k+1} - p_k has e_k.e_k = 1 and each corner is a right angle,
e_k.e_{k+1} = 0. (Unit sides and right angles force e_2 = -e_0 and e_3 = -e_1.)
Its listing sense is the sign of its shoelace sum, which is then +2 or -2.

Pairs. For closed convex polygons P and Q, every extreme point of P n Q is a vertex of
P lying in Q, a vertex of Q lying in P, or a crossing point of a non-parallel edge of P
with an edge of Q (a boundary point in the relative interior of two collinear edges is
never extreme). So P n Q is the convex hull of that finite set V, and each point of V
lies in both. Then: V empty is apart (the closed squares are disjoint); V non-empty
and collinear is contact (the closed squares meet, the interiors do not, because the
interior of P n Q is the intersection of the interiors); V spanning the plane is
overlap, and the hull's area is the overlap area.

Walls. A square lies in [0, S]^2 exactly when its centre does and its interior meets
none of four slabs of width 4 outside the box (a corner outside lies within sqrt(2)/2
of a centre inside, hence inside a slab). Each wall is classed by the pair test
against its slab.
"""

from __future__ import annotations

from gmpy2 import mpq

Rat = tuple[int, int]
Corner = tuple[Rat, Rat]
Pt = tuple[mpq, mpq]


def to_points(corners: list[Corner]) -> list[Pt]:
    return [(mpq(x[0], x[1]), mpq(y[0], y[1])) for x, y in corners]


def _sub(a: Pt, b: Pt) -> Pt:
    return (a[0] - b[0], a[1] - b[1])


def _cross(a: Pt, b: Pt) -> mpq:
    return a[0] * b[1] - a[1] * b[0]


def _dot(a: Pt, b: Pt) -> mpq:
    return a[0] * b[0] + a[1] * b[1]


def unit_sense(pts: list[Pt]) -> int:
    """+1 counterclockwise unit square, -1 clockwise unit square, 0 not a unit square."""
    edges = [_sub(pts[(k + 1) % 4], pts[k]) for k in range(4)]
    for k in range(4):
        if _dot(edges[k], edges[k]) != 1:
            return 0
        if _dot(edges[k], edges[(k + 1) % 4]) != 0:
            return 0
    twice_area = sum((_cross(pts[k], pts[(k + 1) % 4]) for k in range(4)), mpq(0))
    if twice_area == 2:
        return 1
    if twice_area == -2:
        return -1
    return 0


def ccw(pts: list[Pt]) -> list[Pt]:
    """The polygon listed counterclockwise (by its shoelace sign)."""
    twice_area = sum((_cross(pts[k], pts[(k + 1) % 4]) for k in range(4)), mpq(0))
    return list(pts) if twice_area > 0 else list(reversed(pts))


def _in_closed(p: Pt, poly: list[Pt]) -> bool:
    m = len(poly)
    for k in range(m):
        a, b = poly[k], poly[(k + 1) % m]
        if _cross(_sub(b, a), _sub(p, a)) < 0:
            return False
    return True


def _crossings(P: list[Pt], Q: list[Pt]) -> list[Pt]:
    out: list[Pt] = []
    for i in range(len(P)):
        a, b = P[i], P[(i + 1) % len(P)]
        r = _sub(b, a)
        for j in range(len(Q)):
            c, d = Q[j], Q[(j + 1) % len(Q)]
            s = _sub(d, c)
            den = _cross(r, s)
            if den == 0:
                continue  # parallel: any shared point is a vertex of one lying in the other
            ca = _sub(c, a)
            tn = _cross(ca, s)
            un = _cross(ca, r)
            if den > 0:
                ok = 0 <= tn <= den and 0 <= un <= den
            else:
                ok = den <= tn <= 0 and den <= un <= 0
            if ok:
                t = tn / den
                out.append((a[0] + t * r[0], a[1] + t * r[1]))
    return out


def _hull_area(V: list[Pt]) -> mpq:
    """Area of the convex hull (monotone chain, exact)."""
    pts = sorted(set(V))
    if len(pts) < 3:
        return mpq(0)

    def half(seq: list[Pt]) -> list[Pt]:
        h: list[Pt] = []
        for p in seq:
            while len(h) >= 2 and _cross(_sub(h[-1], h[-2]), _sub(p, h[-2])) <= 0:
                h.pop()
            h.append(p)
        return h

    lower = half(pts)
    upper = half(list(reversed(pts)))
    hull = lower[:-1] + upper[:-1]
    s = mpq(0)
    for k in range(len(hull)):
        s += _cross(hull[k], hull[(k + 1) % len(hull)])
    return abs(s) / 2


def intersection_set(P: list[Pt], Q: list[Pt]) -> list[Pt]:
    """V for two counterclockwise convex polygons."""
    V = [p for p in P if _in_closed(p, Q)]
    V += [q for q in Q if _in_closed(q, P)]
    V += _crossings(P, Q)
    return V


def classify(P: list[Pt], Q: list[Pt]) -> tuple[str, mpq]:
    """('apart' | 'contact' | 'overlap', overlap area) for counterclockwise P and Q."""
    V = intersection_set(P, Q)
    if not V:
        return "apart", mpq(0)
    a = V[0]
    b = next((p for p in V if p != a), None)
    if b is None:
        return "contact", mpq(0)
    ab = _sub(b, a)
    if all(_cross(ab, _sub(p, a)) == 0 for p in V):
        return "contact", mpq(0)
    return "overlap", _hull_area(V)


def slabs(side: mpq) -> dict[str, list[Pt]]:
    """Four closed slabs of width 4 outside [0, side]^2, counterclockwise."""
    z, s, m = mpq(0), side, mpq(4)

    def box(x0: mpq, y0: mpq, x1: mpq, y1: mpq) -> list[Pt]:
        return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]

    return {
        "left": box(z - m, z - m, z, s + m),
        "right": box(s, z - m, s + m, s + m),
        "bottom": box(z - m, z - m, s + m, z),
        "top": box(z - m, s, s + m, s + m),
    }


def walls(P: list[Pt], side: mpq, slab: dict[str, list[Pt]]) -> tuple[dict[str, str], bool]:
    """Each wall's class ('apart' | 'contact' | 'outside') and whether the centre is in the box."""
    out: dict[str, str] = {}
    for name, poly in slab.items():
        cls, _ = classify(P, poly)
        out[name] = "outside" if cls == "overlap" else cls
    cx = sum((p[0] for p in P), mpq(0)) / 4
    cy = sum((p[1] for p in P), mpq(0)) / 4
    centre_in = 0 <= cx <= side and 0 <= cy <= side
    return out, centre_in
