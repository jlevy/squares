"""Method B of lane r1012: exact convex clipping of the corners, in GMP rationals.

Clean room, written for the stage 4 review of issue 1012. It is handed the side
and each square's four corners in the order written, converts them to gmpy2.mpq,
and shares no code with method A.

A square is accepted as a unit square in cyclic order when its four sides have
squared length 1 and both diagonals squared length 2: four equal sides make a
rhombus (or a degenerate figure, whose diagonal would vanish), and a rhombus of
side 1 whose diagonals are equal is a square. The shoelace sum, which is then
+2 or -2, gives the sense; a clockwise square is reversed before it is used as a
clipping polygon.

A pair is decided by Sutherland-Hodgman clipping of one square against the four
closed half-planes to the left of the other's counterclockwise edges, keeping
points on the line, which yields their intersection exactly. Empty is apart;
non-empty with zero area is contact (the interior of an intersection of convex
sets is the intersection of their interiors); positive area is overlap, by that
area. Every pair is clipped both ways round, and the two must agree in class and
area.

A wall is classed by clipping the square against the closed half-plane outside
it, in the same three classes (clear, touch, cross). Containment is decided
apart: a unit square lies in the box exactly when its intersection with the box,
clipped against the box's four closed half-planes, has area exactly 1.
"""

from gmpy2 import mpq


def to_mpq(quad):
    return [(mpq(x.numerator, x.denominator), mpq(y.numerator, y.denominator)) for x, y in quad]


def _d2(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


def shoelace2(poly):
    s = mpq(0)
    k = len(poly)
    for idx in range(k):
        x0, y0 = poly[idx]
        x1, y1 = poly[(idx + 1) % k]
        s += x0 * y1 - x1 * y0
    return s


def unit_square(pts):
    """(accepted, sense, reasons) for four points in the order given."""
    why = []
    for k in range(4):
        if _d2(pts[k], pts[(k + 1) % 4]) != 1:
            why.append(f"side {k} squared length != 1")
    if _d2(pts[0], pts[2]) != 2:
        why.append("diagonal 0-2 squared length != 2")
    if _d2(pts[1], pts[3]) != 2:
        why.append("diagonal 1-3 squared length != 2")
    s = shoelace2(pts)
    sense = 1 if s > 0 else (-1 if s < 0 else 0)
    if not why and s not in (2, -2):
        why.append("shoelace sum not +-2")
    return (not why), sense, why


def ccw(pts, sense):
    return list(pts) if sense > 0 else list(reversed(pts))


def _side(a, b, p):
    """Twice the signed area of (a, b, p): positive when p is left of a->b."""
    return (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])


def clip_halfplane(poly, inside, cut):
    """Sutherland-Hodgman against one closed half-plane.

    inside(p) -> mpq value v(p), with the half-plane v >= 0 (v affine in p).
    cut(s, e, vs, ve) -> the point on segment s-e where v = 0.
    """
    out = []
    k = len(poly)
    if k == 0:
        return out
    for idx in range(k):
        s = poly[idx - 1]
        e = poly[idx]
        vs = inside(s)
        ve = inside(e)
        if ve >= 0:
            if vs < 0:
                out.append(cut(s, e, vs, ve))
            out.append(e)
        elif vs >= 0:
            out.append(cut(s, e, vs, ve))
    return out


def _cut(s, e, vs, ve):
    t = vs / (vs - ve)
    return (s[0] + t * (e[0] - s[0]), s[1] + t * (e[1] - s[1]))


def clip_by_convex(subject, clip_ccw):
    poly = list(subject)
    k = len(clip_ccw)
    for idx in range(k):
        a = clip_ccw[idx]
        b = clip_ccw[(idx + 1) % k]
        poly = clip_halfplane(poly, lambda p, a=a, b=b: _side(a, b, p), _cut)
        if not poly:
            break
    return poly


def area(poly):
    if len(poly) < 3:
        return mpq(0)
    return abs(shoelace2(poly)) / 2


def classify_intersection(poly):
    if not poly:
        return "apart", mpq(0)
    a = area(poly)
    return ("touch" if a == 0 else "overlap"), a


def wall_classes(pts, side):
    """Classes for (left, bottom, right, top) by clipping against the outside of each wall."""
    zero = mpq(0)
    outside = (
        lambda p: zero - p[0],          # left:   x <= 0
        lambda p: zero - p[1],          # bottom: y <= 0
        lambda p: p[0] - side,          # right:  x >= S
        lambda p: p[1] - side,          # top:    y >= S
    )
    classes = []
    for v in outside:
        poly = clip_halfplane(list(pts), v, _cut)
        if not poly:
            classes.append("clear")
        else:
            classes.append("touch" if area(poly) == 0 else "cross")
    return tuple(classes)


def area_inside_box(pts, side):
    box = [(mpq(0), mpq(0)), (side, mpq(0)), (side, side), (mpq(0), side)]
    return area(clip_by_convex(list(pts), box))


def decide(side_fraction, quads):
    """Method B over a packing: every square, every wall, every pair (both orders)."""
    side = mpq(side_fraction.numerator, side_fraction.denominator)
    pts = [to_mpq(q) for q in quads]
    n = len(pts)
    unit, sense, why, ccws = [], [], [], []
    for p in pts:
        ok, sg, reasons = unit_square(p)
        unit.append(ok)
        sense.append(sg)
        why.append(reasons)
        ccws.append(ccw(p, sg) if ok else None)
    walls, inside = [], []
    for k in range(n):
        if unit[k]:
            walls.append(wall_classes(ccws[k], side))
            inside.append(area_inside_box(ccws[k], side))
        else:
            walls.append(None)
            inside.append(None)
    pair_class, pair_area, order_disagree = {}, {}, []
    for i in range(n):
        for j in range(i + 1, n):
            if not (unit[i] and unit[j]):
                pair_class[(i, j)] = None
                pair_area[(i, j)] = None
                continue
            c1, a1 = classify_intersection(clip_by_convex(ccws[j], ccws[i]))
            c2, a2 = classify_intersection(clip_by_convex(ccws[i], ccws[j]))
            if c1 != c2 or a1 != a2:
                order_disagree.append((i, j))
            pair_class[(i, j)] = c1
            pair_area[(i, j)] = a1
    return {
        "unit": unit,
        "sense": sense,
        "why": why,
        "wall_class": walls,
        "inside_area": inside,
        "pair_class": pair_class,
        "pair_area": pair_area,
        "order_disagree": order_disagree,
    }
