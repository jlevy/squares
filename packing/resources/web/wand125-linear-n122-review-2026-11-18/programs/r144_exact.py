"""Exact capture of a closed core by the certificate's measure, by two methods.

capture_a: in the core's own frame (u, v); a point is tested by two slabs, a segment is
clipped by Liang-Barsky on its parameter, a rectangle's four rotated corners are clipped
by the four slabs (Sutherland-Hodgman) and its area taken by the shoelace formula.

capture_b: in the container's frame; the core is the convex polygon with corners
c +- b u +- b v. A point is tested by edge cross products; an axis-parallel segment by
the core's cross-section along its line (edge crossings), an oblique one by Cyrus-Beck
on the polygon's edge normals; a rectangle by clipping the core polygon to the
rectangle's four axis-parallel half-planes.

Both are exact rational arithmetic (fractions.Fraction). An image is skipped only when
its binary64 bounding box misses the core's bounding box by more than 1e-6, which no
rounding of numbers below 16 can produce. Written for this review; imports nothing
from jlevy/squares or the source.
"""

from __future__ import annotations

from fractions import Fraction as F

import numpy as np

from r144_common import angle_data, expand_images


class Measure:
    def __init__(self, prims, L: F, factor: F = F(1)):
        self.L = L
        self.images = expand_images(prims, L, factor)
        lo = []
        hi = []
        for kind, g, m, _i, _g in self.images:
            if kind == "point":
                lo.append((float(g[0]), float(g[1])))
                hi.append((float(g[0]), float(g[1])))
            else:
                lo.append((float(min(g[0], g[2])), float(min(g[1], g[3]))))
                hi.append((float(max(g[0], g[2])), float(max(g[1], g[3]))))
        self.lo = np.array(lo)
        self.hi = np.array(hi)

    def near(self, cx: float, cy: float, R: float, pad: float = 1e-6):
        m = (
            (self.hi[:, 0] >= cx - R - pad)
            & (self.lo[:, 0] <= cx + R + pad)
            & (self.hi[:, 1] >= cy - R - pad)
            & (self.lo[:, 1] <= cy + R + pad)
        )
        return np.nonzero(m)[0]


def _shoelace(poly) -> F:
    a = F(0)
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2


def _clip_halfplane(poly, a: F, b: F, c: F):
    """Keep the part of a convex polygon with a*x + b*y <= c."""
    out = []
    n = len(poly)
    for i in range(n):
        p = poly[i]
        q = poly[(i + 1) % n]
        fp = a * p[0] + b * p[1] - c
        fq = a * q[0] + b * q[1] - c
        if fp <= 0:
            out.append(p)
        if (fp < 0 < fq) or (fq < 0 < fp):
            s = fp / (fp - fq)
            out.append((p[0] + s * (q[0] - p[0]), p[1] + s * (q[1] - p[1])))
    return out


def capture_a(meas: Measure, ang: dict, cx: F, cy: F, idx=None) -> F:
    c, s, b = ang["cos"], ang["sin"], ang["b"]
    Uc = c * cx + s * cy
    Vc = -s * cx + c * cy
    u0, u1, v0, v1 = Uc - b, Uc + b, Vc - b, Vc + b
    if idx is None:
        R = float(b * (abs(c) + abs(s)))
        idx = meas.near(float(cx), float(cy), R)
    total = F(0)
    for k in idx:
        kind, g, m, _i, _g = meas.images[k]
        if kind == "point":
            U = c * g[0] + s * g[1]
            V = -s * g[0] + c * g[1]
            if u0 <= U <= u1 and v0 <= V <= v1:
                total += m
        elif kind == "segment":
            Ua = c * g[0] + s * g[1]
            Va = -s * g[0] + c * g[1]
            Ub = c * g[2] + s * g[3]
            Vb = -s * g[2] + c * g[3]
            lo, hi = F(0), F(1)
            ok = True
            for a0, d, w0, w1 in ((Ua, Ub - Ua, u0, u1), (Va, Vb - Va, v0, v1)):
                if d == 0:
                    if not (w0 <= a0 <= w1):
                        ok = False
                        break
                    continue
                t0 = (w0 - a0) / d
                t1 = (w1 - a0) / d
                if t0 > t1:
                    t0, t1 = t1, t0
                lo = max(lo, t0)
                hi = min(hi, t1)
            if ok and hi > lo:
                total += m * (hi - lo)
        else:
            x0, y0, x1, y1 = g
            area = (x1 - x0) * (y1 - y0)
            poly = [
                (c * x + s * y, -s * x + c * y) for (x, y) in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))
            ]
            for a, bb, cc in ((1, 0, u1), (-1, 0, -u0), (0, 1, v1), (0, -1, -v0)):
                poly = _clip_halfplane(poly, F(a), F(bb), cc)
                if not poly:
                    break
            if len(poly) >= 3:
                total += m * _shoelace(poly) / area
    return total


def _core_polygon(ang: dict, cx: F, cy: F):
    c, s, b = ang["cos"], ang["sin"], ang["b"]
    ux, uy = c, s
    vx, vy = -s, c
    # counter-clockwise: (+u+v)? order: -u-v, +u-v, +u+v, -u+v
    return [
        (cx - b * ux - b * vx, cy - b * uy - b * vy),
        (cx + b * ux - b * vx, cy + b * uy - b * vy),
        (cx + b * ux + b * vx, cy + b * uy + b * vy),
        (cx - b * ux + b * vx, cy - b * uy + b * vy),
    ]


def _inside_poly(poly, x: F, y: F) -> bool:
    n = len(poly)
    for i in range(n):
        ax, ay = poly[i]
        bx, by = poly[(i + 1) % n]
        if (bx - ax) * (y - ay) - (by - ay) * (x - ax) < 0:
            return False
    return True


def _section(poly, horizontal: bool, level: F):
    """The interval cut from a convex polygon by the line y = level (or x = level)."""
    vals = []
    n = len(poly)
    for i in range(n):
        p = poly[i]
        q = poly[(i + 1) % n]
        if horizontal:
            pa, pb, qa, qb = p[1], p[0], q[1], q[0]
        else:
            pa, pb, qa, qb = p[0], p[1], q[0], q[1]
        if pa == level:
            vals.append(pb)
        if (pa - level) * (qa - level) < 0:
            vals.append(pb + (level - pa) * (qb - pb) / (qa - pa))
    if not vals:
        return None
    return min(vals), max(vals)


def capture_b(meas: Measure, ang: dict, cx: F, cy: F, idx=None) -> F:
    c, s, b = ang["cos"], ang["sin"], ang["b"]
    poly = _core_polygon(ang, cx, cy)
    if idx is None:
        R = float(b * (abs(c) + abs(s)))
        idx = meas.near(float(cx), float(cy), R)
    total = F(0)
    for k in idx:
        kind, g, m, _i, _g = meas.images[k]
        if kind == "point":
            if _inside_poly(poly, g[0], g[1]):
                total += m
        elif kind == "segment":
            x0, y0, x1, y1 = g
            if y0 == y1:
                sec = _section(poly, True, y0)
                if sec is not None:
                    lo, hi = max(sec[0], min(x0, x1)), min(sec[1], max(x0, x1))
                    if hi > lo:
                        total += m * (hi - lo) / abs(x1 - x0)
            elif x0 == x1:
                sec = _section(poly, False, x0)
                if sec is not None:
                    lo, hi = max(sec[0], min(y0, y1)), min(sec[1], max(y0, y1))
                    if hi > lo:
                        total += m * (hi - lo) / abs(y1 - y0)
            else:
                # Cyrus-Beck against each edge's inward normal
                lo, hi = F(0), F(1)
                dx, dy = x1 - x0, y1 - y0
                ok = True
                n = len(poly)
                for i in range(n):
                    ax, ay = poly[i]
                    bx, by = poly[(i + 1) % n]
                    nx, ny = -(by - ay), bx - ax  # inward for counter-clockwise
                    num = nx * (x0 - ax) + ny * (y0 - ay)
                    den = nx * dx + ny * dy
                    if den == 0:
                        if num < 0:
                            ok = False
                            break
                        continue
                    tt = -num / den
                    if den > 0:
                        lo = max(lo, tt)
                    else:
                        hi = min(hi, tt)
                if ok and hi > lo:
                    total += m * (hi - lo)
        else:
            x0, y0, x1, y1 = g
            area = (x1 - x0) * (y1 - y0)
            q = list(poly)
            for a, bb, cc in ((1, 0, x1), (-1, 0, -x0), (0, 1, y1), (0, -1, -y0)):
                q = _clip_halfplane(q, F(a), F(bb), cc)
                if not q:
                    break
            if len(q) >= 3:
                total += m * _shoelace(q) / area
    return total


def angle(j: int, cand: dict) -> dict:
    return angle_data(j, cand["step"], cand["L"], cand["B"])
