"""Method B of lane r1021-1118: exact convex clipping in GMP rationals, from corners only.

A pair is decided by clipping one square against the four closed half-planes of the
other (Sutherland-Hodgman, keeping the points on each line), both ways round, and
the two results must agree in class and in area: an empty result is apart, a
non-empty result of zero area is contact, positive area is overlap.  A square's
orientation is read from the sign of its signed area, so a clockwise listing is
clipped with its half-planes reversed.  A wall is classed by clipping the square
against the closed half-plane outside it, and containment is the area of the square
inside the box, which must be exactly 1.

Method B never sees a pose.  It shares the Fractions-to-mpq conversion with nothing
but this file.
"""

from __future__ import annotations

from gmpy2 import mpq

ZERO = mpq(0)


def to_mpq(q):
    return [(mpq(x.numerator, x.denominator), mpq(y.numerator, y.denominator)) for x, y in q]


def area2(poly) -> mpq:
    """Twice the signed area (shoelace)."""
    n = len(poly)
    a = mpq(0)
    for k in range(n):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % n]
        a += x0 * y1 - x1 * y0
    return a


def clip_linear(poly, a, b, c):
    """Keep the points p of the convex polygon with a*p.x + b*p.y + c >= 0 (closed half-plane)."""
    n = len(poly)
    if n == 0:
        return []
    vals = [a * x + b * y + c for x, y in poly]
    if all(v < 0 for v in vals):
        return []
    if all(v >= 0 for v in vals):
        return list(poly)
    out = []
    for k in range(n):
        fp, fc = vals[k - 1], vals[k]
        pp, pc = poly[k - 1], poly[k]
        if fc >= 0:
            if fp < 0:
                t = fp / (fp - fc)
                out.append((pp[0] + t * (pc[0] - pp[0]), pp[1] + t * (pc[1] - pp[1])))
            out.append(pc)
        elif fp > 0:
            t = fp / (fp - fc)
            out.append((pp[0] + t * (pc[0] - pp[0]), pp[1] + t * (pc[1] - pp[1])))
    return out


def edge_halfplanes(q):
    """The closed inner half-planes (a, b, c) of a convex polygon, whatever its listing sense."""
    sgn = 1 if area2(q) > 0 else -1
    out = []
    n = len(q)
    for k in range(n):
        (px, py), (qx, qy) = q[k], q[(k + 1) % n]
        # inside of a counterclockwise edge P->Q: cross(Q - P, X - P) >= 0
        a = -(qy - py) * sgn
        b = (qx - px) * sgn
        c = -(a * px + b * py)
        out.append((a, b, c))
    return out


def clip(subject, halfplanes):
    out = list(subject)
    for a, b, c in halfplanes:
        out = clip_linear(out, a, b, c)
        if not out:
            return out
    return out


def classify(poly):
    """('apart', 0), ('contact', 0) or ('overlap', area)."""
    if not poly:
        return "apart", ZERO
    ar = abs(area2(poly)) / 2
    return ("contact", ZERO) if ar == 0 else ("overlap", ar)


def is_unit_square(q) -> bool:
    def dd(p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    sides = [dd(q[k], q[(k + 1) % 4]) for k in range(4)]
    return all(v == 1 for v in sides) and dd(q[0], q[2]) == 2 and dd(q[1], q[3]) == 2


def decide_corners(squares, side):
    """Method B on a list of corner lists (Fractions) in [0, side]^2.

    Returns not_unit, wall classes per square (left, bottom, right, top), the area of each
    square inside the box, and per pair (lexicographic) the class and area both ways round.
    """
    s = mpq(side.numerator, side.denominator)
    polys = [to_mpq(q) for q in squares]
    hps = [edge_halfplanes(q) for q in polys]
    not_unit = [k for k, q in enumerate(polys) if not is_unit_square(q)]
    box = [(1, 0, ZERO), (0, 1, ZERO), (-1, 0, s), (0, -1, s)]
    outside = [(-1, 0, ZERO), (0, -1, ZERO), (1, 0, -s), (0, 1, -s)]
    walls = []
    inside_area = []
    for q in polys:
        walls.append(tuple(classify(clip_linear(q, a, b, c))[0] for a, b, c in outside))
        inside_area.append(abs(area2(clip(q, box))) / 2)
    n = len(polys)
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            c1, a1 = classify(clip(polys[i], hps[j]))
            c2, a2 = classify(clip(polys[j], hps[i]))
            pairs.append((c1, a1, c2, a2))
    return {"not_unit": not_unit, "walls": walls, "inside_area": inside_area, "pairs": pairs}


def decide_pair(qi, qj):
    """One pair of corner lists (Fractions): (class i in j, area, class j in i, area)."""
    pi, pj = to_mpq(qi), to_mpq(qj)
    c1, a1 = classify(clip(pi, edge_halfplanes(pj)))
    c2, a2 = classify(clip(pj, edge_halfplanes(pi)))
    return c1, a1, c2, a2


def margin_from_corners(qi, qj):
    """A third reading of a pair's margin: on each edge direction of either square (unit
    vectors read from the corners), the gap between the two squares' corner projections;
    the margin is the largest gap.  Equal to method A's margin when both are unit squares."""
    pi, pj = to_mpq(qi), to_mpq(qj)
    axes = []
    for q in (pi, pj):
        for k in (0, 1):
            axes.append((q[k + 1][0] - q[k][0], q[k + 1][1] - q[k][1]))
    best = None
    for wx, wy in axes:
        ri = [x * wx + y * wy for x, y in pi]
        rj = [x * wx + y * wy for x, y in pj]
        gap = max(min(rj) - max(ri), min(ri) - max(rj))
        best = gap if best is None or gap > best else best
    return best


def wall_class_from_clearance(v) -> str:
    return "clear" if v > 0 else ("touching" if v == 0 else "crossing")


WALL_FROM_CLIP = {"apart": "clear", "contact": "touching", "overlap": "crossing"}
