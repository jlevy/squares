"""Clean-room exact checker for Evan Daniel-format centre/half-angle certificates.

Written for the stage 4 review of Polkovskyi's 23 October and #846 certificates
(think-ikku). Reads a certificate as data: a header ``n S`` then ``n`` lines ``x y t``,
each a rational; square k is the unit square centred at (x, y) with axes
u = (c, s), v = (-s, c), c = (1 - t^2)/(1 + t^2), s = 2t/(1 + t^2).

Two routes, sharing only the reader:

- Route A (separating axes): containment by each square's exact axis extents;
  disjointness by the separating-axis theorem over the four edge normals, on every
  pair whose centres are within 3/2 (others are disjoint since a unit square lies in
  the open disc of radius sqrt(2)/2 about its centre). Reports the least wall
  clearance per wall and the least pair margin.
- Route B (clipping area): containment by every corner in [0, S]^2; disjointness of
  interiors by the exact area of the intersection polygon (Sutherland-Hodgman) on
  every pair whose closed bounding boxes overlap with positive area, which must be 0.

Usage: python -I rv_check.py check CERT [CERT...]   (prints one JSON line per cert)
       python -I rv_check.py selftest
"""

from __future__ import annotations

import json
import sys
from fractions import Fraction as F
from pathlib import Path

HALF = F(1, 2)


def read_cert(path: str):
    lines = [ln.strip() for ln in Path(path).read_text().splitlines()]
    body = [ln for ln in lines if ln and not ln.startswith("#")]
    head = body[0].split()
    if len(head) != 2:
        raise ValueError("header is not 'n S'")
    n, side = int(head[0]), F(head[1])
    rows = body[1:]
    if len(rows) != n:
        raise ValueError(f"{len(rows)} rows for n = {n}")
    sq = []
    for r in rows:
        p = r.split()
        if len(p) != 3:
            raise ValueError(f"row {r[:40]!r} has {len(p)} fields")
        x, y, t = (F(v) for v in p)
        d = 1 + t * t
        sq.append((x, y, (1 - t * t) / d, 2 * t / d))
    return n, side, sq


# ---------------------------------------------------------------- route A
def extent(c, s):
    return (abs(c) + abs(s)) / 2


def walls_a(side, sq):
    best = {"left": None, "right": None, "bottom": None, "top": None}
    for x, y, c, s in sq:
        h = extent(c, s)
        for k, v in (("left", x - h), ("right", side - x - h), ("bottom", y - h), ("top", side - y - h)):
            if best[k] is None or v < best[k]:
                best[k] = v
    return best


def pair_margin(a, b):
    """Max over the four edge normals of the projection gap (>= 0 iff separated)."""
    xa, ya, ca, sa = a
    xb, yb, cb, sb = b
    dx, dy = xb - xa, yb - ya
    best = None
    for (ax, ay) in ((ca, sa), (-sa, ca), (cb, sb), (-sb, cb)):
        d = abs(dx * ax + dy * ay)
        ra = (abs(ca * ax + sa * ay) + abs(-sa * ax + ca * ay)) / 2
        rb = (abs(cb * ax + sb * ay) + abs(-sb * ax + cb * ay)) / 2
        g = d - ra - rb
        if best is None or g > best:
            best = g
    return best


def route_a(side, sq):
    w = walls_a(side, sq)
    least = None
    where = None
    close = 0
    lim = F(9, 4)
    n = len(sq)
    order = sorted(range(n), key=lambda k: sq[k][0])
    for ii in range(n):
        i = order[ii]
        xi, yi = sq[i][0], sq[i][1]
        for jj in range(ii + 1, n):
            j = order[jj]
            dx = sq[j][0] - xi
            if dx > F(3, 2):
                break
            dy = sq[j][1] - yi
            if dx * dx + dy * dy > lim:
                continue
            close += 1
            m = pair_margin(sq[i], sq[j])
            if least is None or m < least:
                least, where = m, (min(i, j), max(i, j))
    ok = min(w.values()) >= 0 and (least is None or least >= 0)
    return ok, w, least, where, close


# ---------------------------------------------------------------- route B
def corners(x, y, c, s):
    ux, uy, vx, vy = c / 2, s / 2, -s / 2, c / 2
    return [(x + ux + vx, y + uy + vy), (x - ux + vx, y - uy + vy),
            (x - ux - vx, y - uy - vy), (x + ux - vx, y + uy - vy)]


def area2(poly):
    t = F(0)
    for k in range(len(poly)):
        x1, y1 = poly[k]
        x2, y2 = poly[(k + 1) % len(poly)]
        t += x1 * y2 - x2 * y1
    return t


def clip(subject, clipper):
    """Sutherland-Hodgman: subject polygon clipped by convex CCW clipper (closed)."""
    out = subject
    m = len(clipper)
    for k in range(m):
        (ax, ay), (bx, by) = clipper[k], clipper[(k + 1) % m]
        ex, ey = bx - ax, by - ay
        inp, out = out, []
        if not inp:
            break

        def side_of(p):
            return ex * (p[1] - ay) - ey * (p[0] - ax)

        prev = inp[-1]
        fp = side_of(prev)
        for cur in inp:
            fc = side_of(cur)
            if fc >= 0:
                if fp < 0:
                    tt = fp / (fp - fc)
                    out.append((prev[0] + tt * (cur[0] - prev[0]), prev[1] + tt * (cur[1] - prev[1])))
                out.append(cur)
            elif fp >= 0:
                tt = fp / (fp - fc)
                out.append((prev[0] + tt * (cur[0] - prev[0]), prev[1] + tt * (cur[1] - prev[1])))
            prev, fp = cur, fc
    return out


def ccw(poly):
    return poly if area2(poly) > 0 else poly[::-1]


def route_b(side, sq):
    polys = [ccw(corners(*q)) for q in sq]
    inside = all(0 <= px <= side and 0 <= py <= side for p in polys for (px, py) in p)
    boxes = [(min(p[0] for p in P), max(p[0] for p in P), min(p[1] for p in P), max(p[1] for p in P)) for P in polys]
    n = len(sq)
    order = sorted(range(n), key=lambda k: boxes[k][0])
    tested = 0
    worst = F(0)
    for ii in range(n):
        i = order[ii]
        bi = boxes[i]
        for jj in range(ii + 1, n):
            j = order[jj]
            bj = boxes[j]
            if bj[0] >= bi[1]:
                break
            if bj[2] >= bi[3] or bi[2] >= bj[3]:
                continue
            tested += 1
            inter = clip(polys[j], polys[i])
            a = area2(inter) if len(inter) >= 3 else F(0)
            if a > worst:
                worst = a
    return inside and worst == 0, inside, worst / 2, tested


def check(path):
    n, side, sq = read_cert(path)
    ok_a, w, least, where, close = route_a(side, sq)
    ok_b, inside_b, overlap_b, tested_b = route_b(side, sq)
    return {
        "cert": path, "n": n, "side": f"{side.numerator}/{side.denominator}",
        "route_a": ok_a, "route_b": ok_b,
        "walls": {k: float(v) for k, v in w.items()},
        "walls_exact": {k: str(v) for k, v in w.items()},
        "least_pair_margin": float(least), "least_pair_margin_exact": str(least), "least_pair": where,
        "pairs_a": close, "pairs_b": tested_b, "b_inside": inside_b, "b_max_overlap_area": float(overlap_b),
    }


# ---------------------------------------------------------------- selftest
def selftest():
    ok = []
    e = F(1, 10**30)
    base = [(F(1, 2), F(1, 2), F(1), F(0)), (F(3, 2), F(1, 2), F(1), F(0))]
    S = F(2)
    def both(side, sq):
        return route_a(side, sq)[0], route_b(side, sq)[0]
    ok.append(("two touching squares accepted", both(S, base) == (True, True)))
    ok.append(("box below extent refused", both(S - e, base) == (False, False)))
    sh = [(F(1, 2), F(1, 2), F(1), F(0)), (F(3, 2) - e, F(1, 2), F(1), F(0))]
    ok.append(("pair past contact refused", both(S, sh) == (False, False)))
    dup = [base[0], base[0]]
    ok.append(("duplicate refused", both(S, dup) == (False, False)))
    # a 3-4-5 rotation: t = 1/3 -> c = 4/5, s = 3/5; extent 7/10
    rot = [(F(7, 10), F(7, 10), F(4, 5), F(3, 5))]
    ok.append(("rotated at contact accepted", both(F(7, 5), rot) == (True, True)))
    ok.append(("rotated past contact refused", both(F(7, 5) - e, rot) == (False, False)))
    # corner-to-corner diagonal touch of two axis squares
    cc = [(F(1, 2), F(1, 2), F(1), F(0)), (F(3, 2), F(3, 2), F(1), F(0))]
    ok.append(("corner touch accepted", both(F(2), cc) == (True, True)))
    cc2 = [(F(1, 2), F(1, 2), F(1), F(0)), (F(3, 2) - e, F(3, 2) - e, F(1), F(0))]
    ok.append(("corner past contact refused", both(F(2), cc2) == (False, False)))
    # rotated square's vertex against an axis square's face
    v = [(F(1, 2), F(1, 2), F(1), F(0)), (F(1) + F(7, 10), F(4, 5), F(4, 5), F(3, 5))]
    ok.append(("vertex on face accepted", both(F(3), v) == (True, True)))
    v2 = [(F(1, 2), F(1, 2), F(1), F(0)), (F(1) + F(7, 10) - e, F(4, 5), F(4, 5), F(3, 5))]
    ok.append(("vertex past face refused", both(F(3), v2) == (False, False)))
    for name, good in ok:
        print(("PASS " if good else "FAIL ") + name)
    return all(g for _, g in ok)


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(0 if selftest() else 1)
    for p in sys.argv[2:]:
        print(json.dumps(check(p)), flush=True)
