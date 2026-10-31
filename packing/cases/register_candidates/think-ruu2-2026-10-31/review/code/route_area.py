"""Route B: exact clipped areas, over Q with Fractions.

Shares only the reader (qio) with route A. Each square becomes its four corners in
counter-clockwise order, c + (-e1 - e2)/2, c + (e1 - e2)/2, c + (e1 + e2)/2,
c + (-e1 + e2)/2, with e1 = (a, b) and e2 = (-b, a).

- unit: every edge has squared length 1, consecutive edges are orthogonal, and the
  shoelace area is 1;
- walls: the square clipped to [0, side]^2 (Sutherland-Hodgman against four half-planes)
  keeps area exactly 1. A closed square with interior whose part in the closed box has
  its full area lies in the box: an interior point outside would leave an open set
  outside;
- pairs: every pair i < j is decided. Where the axis-aligned bounding boxes of the
  corners have disjoint interiors (max of one <= min of the other on x or on y) the
  interiors of the squares are disjoint; otherwise square i is clipped against square j's
  four edge half-planes and the clipped polygon's area must be exactly 0. Convex bodies
  with nonempty interiors have disjoint interiors iff their intersection has zero area.
"""

from __future__ import annotations

from fractions import Fraction

from qio import Square

type Pt = tuple[Fraction, Fraction]


def corners(sq: Square) -> list[Pt]:
    cx, cy, a, b = sq
    h = Fraction(1, 2)
    e1 = (a * h, b * h)
    e2 = (-b * h, a * h)
    return [
        (cx - e1[0] - e2[0], cy - e1[1] - e2[1]),
        (cx + e1[0] - e2[0], cy + e1[1] - e2[1]),
        (cx + e1[0] + e2[0], cy + e1[1] + e2[1]),
        (cx - e1[0] + e2[0], cy - e1[1] + e2[1]),
    ]


def area2(poly: list[Pt]) -> Fraction:
    s = Fraction(0)
    m = len(poly)
    for k in range(m):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % m]
        s += x1 * y2 - x2 * y1
    return s


def clip(subject: list[Pt], p: Pt, q: Pt) -> list[Pt]:
    """Keep the part of subject left of (or on) the directed line p -> q."""
    ex, ey = q[0] - p[0], q[1] - p[1]

    def f(v: Pt) -> Fraction:
        return ex * (v[1] - p[1]) - ey * (v[0] - p[0])

    out: list[Pt] = []
    m = len(subject)
    for k in range(m):
        s_pt = subject[k - 1]
        e_pt = subject[k]
        fs, fe = f(s_pt), f(e_pt)
        if fe >= 0:
            if fs < 0:
                r = fs / (fs - fe)
                out.append((s_pt[0] + (e_pt[0] - s_pt[0]) * r, s_pt[1] + (e_pt[1] - s_pt[1]) * r))
            out.append(e_pt)
        elif fs >= 0:
            r = fs / (fs - fe)
            out.append((s_pt[0] + (e_pt[0] - s_pt[0]) * r, s_pt[1] + (e_pt[1] - s_pt[1]) * r))
    return out


def clip_convex(subject: list[Pt], clipper: list[Pt]) -> list[Pt]:
    poly = subject
    m = len(clipper)
    for k in range(m):
        if not poly:
            break
        poly = clip(poly, clipper[k], clipper[(k + 1) % m])
    return poly


def unit_shape(c: list[Pt]) -> bool:
    edges = [(c[(k + 1) % 4][0] - c[k][0], c[(k + 1) % 4][1] - c[k][1]) for k in range(4)]
    if any(ex * ex + ey * ey != 1 for ex, ey in edges):
        return False
    if any(edges[k][0] * edges[(k + 1) % 4][0] + edges[k][1] * edges[(k + 1) % 4][1] != 0 for k in range(4)):
        return False
    return area2(c) == 2


def check(side: Fraction, squares: list[Square]) -> dict[str, object]:
    n = len(squares)
    polys = [corners(s) for s in squares]
    zero = Fraction(0)
    box = [(zero, zero), (side, zero), (side, side), (zero, side)]
    non_unit = [i for i, c in enumerate(polys) if not unit_shape(c)]
    outside = [i for i, c in enumerate(polys) if area2(clip_convex(c, box)) != 2]
    bbox = [
        (min(x for x, _ in c), max(x for x, _ in c), min(y for _, y in c), max(y for _, y in c)) for c in polys
    ]
    clipped = 0
    positive: list[tuple[int, int, Fraction]] = []
    pairs = 0
    for i in range(n):
        bi = bbox[i]
        for j in range(i + 1, n):
            pairs += 1
            bj = bbox[j]
            if bi[1] <= bj[0] or bj[1] <= bi[0] or bi[3] <= bj[2] or bj[3] <= bi[2]:
                continue
            clipped += 1
            a2 = area2(clip_convex(polys[i], polys[j]))
            if a2 != 0:
                positive.append((i, j, a2 / 2))
    ok = not non_unit and not outside and not positive
    return {
        "route": "B: exact clipped area of every pair within reach, container by clipped area",
        "n": n,
        "side": side,
        "accepted": ok,
        "pairs_decided": pairs,
        "pairs_clipped": clipped,
        "non_unit": non_unit,
        "outside": outside[:10],
        "outside_count": len(outside),
        "positive_area_count": len(positive),
        "positive_area": positive[:5],
    }
