"""Method B: exact clipped areas in gmpy2.mpq (review L83, clean room).

A polygon is a unit square when its four edges have squared length 1, its turns all
have one sign, and its shoelace area is 1: an equilateral convex quadrilateral is a
rhombus, and a rhombus of side 1 and area 1 is a unit square.

Pairs: the intersection of two convex polygons is the subject clipped by each closed
half-plane of the other (Sutherland-Hodgman). Empty is clear, nonempty with area 0 is
contact, positive area is overlap. Walls: the square clipped by the closed outer
half-plane of each wall, read the same three ways, and the square clipped to the box,
whose area must stay 1.
"""

from __future__ import annotations

from gmpy2 import mpq

Pt = tuple[mpq, mpq]


def points(corners) -> list[Pt]:
    return [(mpq(x[0], x[1]), mpq(y[0], y[1])) for x, y in corners]


def area2(poly: list[Pt]) -> mpq:
    s = mpq(0)
    k = len(poly)
    for i in range(k):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % k]
        s += x0 * y1 - x1 * y0
    return s


def unit_square_sense(poly: list[Pt]) -> int:
    """+1 counterclockwise, -1 clockwise; raises ValueError if not a unit square."""
    if len(poly) != 4:
        raise ValueError("not four corners")
    edges = []
    for i in range(4):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % 4]
        ex, ey = x1 - x0, y1 - y0
        if ex * ex + ey * ey != 1:
            raise ValueError("edge not of length 1")
        edges.append((ex, ey))
    turns = [edges[i][0] * edges[(i + 1) % 4][1] - edges[i][1] * edges[(i + 1) % 4][0] for i in range(4)]
    if all(t > 0 for t in turns):
        sense = 1
    elif all(t < 0 for t in turns):
        sense = -1
    else:
        raise ValueError("turns not of one sign")
    if abs(area2(poly)) != 2:
        raise ValueError("area not 1")
    return sense


def clip(poly: list[Pt], a: mpq, b: mpq, c: mpq) -> list[Pt]:
    """Keep the part of poly where a*x + b*y + c >= 0."""
    k = len(poly)
    if k == 0:
        return []
    out: list[Pt] = []
    vals = [a * x + b * y + c for x, y in poly]
    for i in range(k):
        px, py = poly[i - 1]
        qx, qy = poly[i]
        dp, dq = vals[i - 1], vals[i]
        if dq >= 0:
            if dp < 0:
                t = dp / (dp - dq)
                out.append((px + t * (qx - px), py + t * (qy - py)))
            out.append((qx, qy))
        elif dp > 0:
            t = dp / (dp - dq)
            out.append((px + t * (qx - px), py + t * (qy - py)))
    dedup: list[Pt] = []
    for p in out:
        if not dedup or dedup[-1] != p:
            dedup.append(p)
    while len(dedup) > 1 and dedup[0] == dedup[-1]:
        dedup.pop()
    return dedup


def halfplanes(poly: list[Pt], sense: int) -> list[tuple[mpq, mpq, mpq]]:
    """Each edge p->q as a*x + b*y + c >= 0 on the polygon's side."""
    out = []
    k = len(poly)
    for i in range(k):
        px, py = poly[i]
        qx, qy = poly[(i + 1) % k]
        ex, ey = qx - px, qy - py
        # sense * cross(e, r - p) >= 0, with cross(e, d) = ex*dy - ey*dx
        a, b = -ey * sense, ex * sense
        out.append((a, b, -(a * px + b * py)))
    return out


def intersect(subject: list[Pt], hps: list[tuple[mpq, mpq, mpq]]) -> list[Pt]:
    poly = subject
    for a, b, c in hps:
        poly = clip(poly, a, b, c)
        if not poly:
            return []
    return poly


def pair_class(p: list[Pt], q_hps) -> tuple[str, mpq]:
    inter = intersect(p, q_hps)
    if not inter:
        return "clear", mpq(0)
    ar = abs(area2(inter)) / 2
    return ("contact" if ar == 0 else "overlap"), ar


def wall_classes(poly: list[Pt], side: mpq) -> dict[str, str]:
    outer = {
        "left": (mpq(-1), mpq(0), mpq(0)),
        "bottom": (mpq(0), mpq(-1), mpq(0)),
        "right": (mpq(1), mpq(0), -side),
        "top": (mpq(0), mpq(1), -side),
    }
    out = {}
    for wall, (a, b, c) in outer.items():
        part = clip(poly, a, b, c)
        if not part:
            out[wall] = "clear"
        else:
            out[wall] = "contact" if area2(part) == 0 else "overlap"
    return out


def box_area(poly: list[Pt], side: mpq) -> mpq:
    box = [(mpq(0), mpq(0)), (side, mpq(0)), (side, side), (mpq(0), side)]
    inter = intersect(poly, halfplanes(box, 1))
    return abs(area2(inter)) / 2 if inter else mpq(0)
