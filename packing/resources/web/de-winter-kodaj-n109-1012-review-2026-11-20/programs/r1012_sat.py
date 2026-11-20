"""Method A of lane r1012: separating axes on the corners, in Python integers.

Clean room, written for the stage 4 review of issue 1012. It receives the side
and the corners as exact rationals from the reader and immediately writes each
square's eight coordinates over one positive integer denominator D, so that the
corners are P_k / D with integer vectors P_k. From there every test is integer
arithmetic; a quantity it reports is an exact pair (numerator, denominator), with
the denominator positive.

A square is accepted as a unit square in cyclic order when, with E = P1 - P0 and
F = P2 - P1, the remaining sides are P3 - P2 = -E and P0 - P3 = -F, and
E.E = F.F = D^2 and E.F = 0. Its edge directions e = E/D and f = F/D are then exact
unit vectors, and they are the normals of its edges.

A pair is decided on the four axes e_i, f_i, e_j, f_j. On a unit axis w the
projections of the two squares are the intervals spanned by their corners'
projections, and the separation max(lo_j - hi_i, lo_i - hi_j) is an exact
distance; on an axis of square i all eight projections are integers over the
common denominator D_i^2 D_j. The margin is the greatest separation over the four
axes. Two convex polygons have disjoint interiors exactly when some line parallel
to an edge of one of them weakly separates them, so a positive margin is apart, a
zero margin is contact with disjoint interiors, and a negative margin is overlap.

A wall clearance is the signed distance from the square's extreme corner to the
wall: left min x, bottom min y, right S - max x, top S - max y.
"""

from math import gcd, lcm


def _over_one_denominator(quad):
    """quad: four (x, y) with x, y having .numerator and .denominator (exact)."""
    den = 1
    for x, y in quad:
        den = lcm(den, x.denominator, y.denominator)
    pts = []
    for x, y in quad:
        pts.append((x.numerator * (den // x.denominator), y.numerator * (den // y.denominator)))
    return den, pts


def _sign(num):
    return (num > 0) - (num < 0)


def _cmp(a, b):
    """Compare exact pairs (num, den) with den > 0: -1, 0 or 1."""
    return _sign(a[0] * b[1] - b[0] * a[1])


def _reduce(num, den):
    # gcd is positive and den > 0, so the denominator stays positive.
    g = gcd(num, den)
    return (num // g, den // g)


class Square:
    __slots__ = ("den", "pts", "unit", "sense", "E", "F", "why")

    def __init__(self, quad):
        self.den, self.pts = _over_one_denominator(quad)
        d = self.den
        (x0, y0), (x1, y1), (x2, y2), (x3, y3) = self.pts
        E = (x1 - x0, y1 - y0)
        F = (x2 - x1, y2 - y1)
        G = (x3 - x2, y3 - y2)
        H = (x0 - x3, y0 - y3)
        self.E, self.F = E, F
        why = []
        if G != (-E[0], -E[1]):
            why.append("P3 - P2 != -(P1 - P0)")
        if H != (-F[0], -F[1]):
            why.append("P0 - P3 != -(P2 - P1)")
        if E[0] * E[0] + E[1] * E[1] != d * d:
            why.append("|P1 - P0| != 1")
        if F[0] * F[0] + F[1] * F[1] != d * d:
            why.append("|P2 - P1| != 1")
        if E[0] * F[0] + E[1] * F[1] != 0:
            why.append("(P1 - P0).(P2 - P1) != 0")
        self.unit = not why
        self.why = why
        cross = E[0] * F[1] - E[1] * F[0]
        self.sense = _sign(cross)

    def axes(self):
        return (self.E, self.F)


def wall_clearances(sq, side):
    """Exact (num, den) clearances (left, bottom, right, top) of one square."""
    d = sq.den
    sn, sd = side.numerator, side.denominator
    xs = [p[0] for p in sq.pts]
    ys = [p[1] for p in sq.pts]
    left = _reduce(min(xs), d)
    bottom = _reduce(min(ys), d)
    right = _reduce(sn * d - sd * max(xs), sd * d)
    top = _reduce(sn * d - sd * max(ys), sd * d)
    return (left, bottom, right, top)


def _separation_on_axis_of(a, b, axis):
    """Separation of squares a, b on the unit axis = axis / a.den (axis of square a).

    Projections of a's corners: (P.axis) / a.den^2; of b's: (P.axis) / (a.den * b.den).
    Common denominator a.den^2 * b.den.
    """
    da, db = a.den, b.den
    ax, ay = axis
    pa = [(x * ax + y * ay) * db for x, y in a.pts]
    pb = [(x * ax + y * ay) * da for x, y in b.pts]
    num = max(min(pb) - max(pa), min(pa) - max(pb))
    return (num, da * da * db)


def pair_margin(a, b):
    """The exact margin of a pair of unit squares, (num, den) reduced, and its axis."""
    best = None
    where = None
    for owner, sq, other in (("i", a, b), ("j", b, a)):
        for k, axis in enumerate(sq.axes()):
            sep = _separation_on_axis_of(sq, other, axis)
            if best is None or _cmp(sep, best) > 0:
                best = sep
                where = f"{owner}{'ef'[k]}"
    return _reduce(*best), where


def classify_margin(m):
    s = _sign(m[0])
    return "apart" if s > 0 else ("touch" if s == 0 else "overlap")


def classify_clearance(c):
    s = _sign(c[0])
    return "clear" if s > 0 else ("touch" if s == 0 else "cross")


def decide(side, quads):
    """Method A over a packing: every square, every wall, every pair."""
    squares = [Square(q) for q in quads]
    n = len(squares)
    out = {
        "unit": [s.unit for s in squares],
        "why": [s.why for s in squares],
        "sense": [s.sense for s in squares],
        "den": [s.den for s in squares],
        "walls": [],
        "wall_class": [],
        "pairs": {},
        "pair_class": {},
        "pair_axis": {},
    }
    for s in squares:
        if s.unit:
            c = wall_clearances(s, side)
            out["walls"].append(c)
            out["wall_class"].append(tuple(classify_clearance(v) for v in c))
        else:
            out["walls"].append(None)
            out["wall_class"].append(None)
    for i in range(n):
        for j in range(i + 1, n):
            if squares[i].unit and squares[j].unit:
                m, axis = pair_margin(squares[i], squares[j])
                out["pairs"][(i, j)] = m
                out["pair_class"][(i, j)] = classify_margin(m)
                out["pair_axis"][(i, j)] = axis
            else:
                out["pairs"][(i, j)] = None
                out["pair_class"][(i, j)] = None
                out["pair_axis"][(i, j)] = None
    return out
