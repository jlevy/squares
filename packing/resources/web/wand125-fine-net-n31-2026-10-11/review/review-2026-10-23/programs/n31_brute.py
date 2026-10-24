"""A second exact method for one core's capture, used to cross-check capture.py.

Sutherland-Hodgman clipping of the core's four vertices against each rectangle, in
Fractions, then the shoelace formula; the capture is the sum of density times area over
the merged D4 expansion. Shares no code with n31_geometry. Written for review-2026-10-23.
"""

from __future__ import annotations

from fractions import Fraction


def _clip(poly, inside, cross):
    out = []
    for k in range(len(poly)):
        p, q = poly[k], poly[(k + 1) % len(poly)]
        ip, iq = inside(p), inside(q)
        if ip:
            out.append(p)
        if ip != iq:
            out.append(cross(p, q))
    return out


def polygon_rect_area(poly, rect) -> Fraction:
    x0, y0, x1, y1 = rect

    def cut(axis, bound, keep_ge):
        def inside(p):
            return p[axis] >= bound if keep_ge else p[axis] <= bound

        def cross(p, q):
            t = (bound - p[axis]) / (q[axis] - p[axis])
            pt = [p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])]
            pt[axis] = bound
            return (pt[0], pt[1])
        return inside, cross

    for inside, cross in (cut(0, x0, True), cut(0, x1, False), cut(1, y0, True),
                          cut(1, y1, False)):
        if not poly:
            return Fraction(0)
        poly = _clip(poly, inside, cross)
    if len(poly) < 3:
        return Fraction(0)
    twice = sum(poly[k][0] * poly[(k + 1) % len(poly)][1]
                - poly[(k + 1) % len(poly)][0] * poly[k][1] for k in range(len(poly)))
    return abs(twice) / 2


def core_vertices(cx, cy, half, cos, sin):
    return [(cx + a * half * cos - b * half * sin, cy + a * half * sin + b * half * cos)
            for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]


def capture(merged, cx, cy, side_b, cos, sin) -> Fraction:
    """Exact mu(core) for the core of side side_b, centre (cx, cy), angle (cos, sin)."""
    half = side_b / 2
    verts = core_vertices(cx, cy, half, cos, sin)
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    total = Fraction(0)
    for (x0, y0, x1, y1), dens in merged.items():
        if x1 <= bx0 or x0 >= bx1 or y1 <= by0 or y0 >= by1:
            continue
        total += dens * polygon_rect_area(list(verts), (x0, y0, x1, y1))
    return total
