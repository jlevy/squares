"""Method B: exact polygon clipping in GMP rationals (`gmpy2.mpq`).

L96 review program. Imports nothing from this repository, the source, or Method A.

A square (x, y, t) is built as four corners, counterclockwise: centre -u/2 -v/2,
+u/2 -v/2, +u/2 +v/2, -u/2 +v/2, with u = (cos, sin), v = (-sin, cos), cos = (1 - t^2)/(1 +
t^2), sin = 2t/(1 + t^2). It is accepted as a unit square when its four edges have squared
length 1, every turn has cross product +1, and its shoelace area is 1.

Containment: a convex polygon lies in [0, L]^2 iff its corners do; each wall's clearance
is the least corner distance to it.

Pairs: square i is clipped by the four closed half-planes of square j (Sutherland-Hodgman,
points on a line kept). An empty result is `clear`, a non-empty result of area 0 is
`contact`, positive area is `overlap`. A pair is decided `clear` without clipping when its
centres are more than sqrt(2) apart (d^2 > 2): each square lies in the closed disc of
radius sqrt(2)/2 about its centre. Pairs are enumerated by integer cells floor(x),
floor(y); a pair whose cells differ by 3 or more in x or y has centres more than 2 apart
and is decided the same way without being enumerated.
"""

from gmpy2 import mpq

ZERO = mpq(0)
ONE = mpq(1)


def floor_q(q):
    """Exact floor of an mpq, by integer floor division (never through mpfr)."""
    return int(q.numerator // q.denominator)


def corners(x, y, t):
    d = 1 + t * t
    c = (1 - t * t) / d
    s = 2 * t / d
    ux, uy = c / 2, s / 2
    vx, vy = -s / 2, c / 2
    return [
        (x - ux - vx, y - uy - vy),
        (x + ux - vx, y + uy - vy),
        (x + ux + vx, y + uy + vy),
        (x - ux + vx, y - uy + vy),
    ]


def area2(poly):
    """Twice the signed shoelace area."""
    acc = ZERO
    m = len(poly)
    for k in range(m):
        x0, y0 = poly[k]
        x1, y1 = poly[(k + 1) % m]
        acc += x0 * y1 - x1 * y0
    return acc


def unit_ok(poly):
    for k in range(4):
        ax, ay = poly[k]
        bx, by = poly[(k + 1) % 4]
        cx, cy = poly[(k + 2) % 4]
        ex, ey = bx - ax, by - ay
        fx, fy = cx - bx, cy - by
        if ex * ex + ey * ey != ONE:
            return False
        if ex * fy - ey * fx != ONE:
            return False
    return area2(poly) == 2


def clip(subject, clipper):
    out = list(subject)
    m = len(clipper)
    for k in range(m):
        if not out:
            break
        ax, ay = clipper[k]
        bx, by = clipper[(k + 1) % m]
        ex, ey = bx - ax, by - ay
        src = out
        out = []
        L = len(src)
        for q in range(L):
            sx, sy = src[q - 1]
            px, py = src[q]
            ss = ex * (sy - ay) - ey * (sx - ax)
            sp = ex * (py - ay) - ey * (px - ax)
            if sp >= 0:
                if ss < 0:
                    r = ss / (ss - sp)
                    out.append((sx + (px - sx) * r, sy + (py - sy) * r))
                out.append((px, py))
            elif ss >= 0:
                r = ss / (ss - sp)
                out.append((sx + (px - sx) * r, sy + (py - sy) * r))
    return out


def pair_class(pi, pj):
    inter = clip(pi, pj)
    if not inter:
        return "clear", ZERO
    a2 = area2(inter)
    if a2 < 0:
        raise AssertionError("negative clipped area")
    return ("contact" if a2 == 0 else "overlap"), a2 / 2


def walls(poly, side):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    return {"left": min(xs), "bottom": min(ys), "right": side - max(xs), "top": side - max(ys)}


def decide(side_pair, triples):
    side = mpq(side_pair[0], side_pair[1])
    polys = []
    cells = {}
    centres = []
    for k, (a, b, c) in enumerate(triples):
        x, y, t = mpq(*a), mpq(*b), mpq(*c)
        polys.append(corners(x, y, t))
        centres.append((x, y))
        key = (floor_q(x), floor_q(y))
        cells.setdefault(key, []).append(k)
    n = len(polys)
    bad_unit = [k + 1 for k, p in enumerate(polys) if not unit_ok(p)]
    clear = {k + 1: walls(p, side) for k, p in enumerate(polys)}
    classes = {}
    areas = {}
    enumerated = 0
    by_disc = 0
    for i in range(n):
        xi, yi = centres[i]
        cx, cy = floor_q(xi), floor_q(yi)
        for ddx in range(-2, 3):
            for ddy in range(-2, 3):
                for j in cells.get((cx + ddx, cy + ddy), ()):
                    if j <= i:
                        continue
                    enumerated += 1
                    dx, dy = centres[j][0] - xi, centres[j][1] - yi
                    if dx * dx + dy * dy > 2:
                        by_disc += 1
                        continue
                    cls, area = pair_class(polys[i], polys[j])
                    classes[(i + 1, j + 1)] = cls
                    if cls != "clear":
                        areas[(i + 1, j + 1)] = area
    total = n * (n - 1) // 2
    return {
        "n": n,
        "side": side,
        "polys": polys,
        "bad_unit": bad_unit,
        "clearances": clear,
        "classes": classes,
        "areas": areas,
        "pairs_total": total,
        "pairs_not_enumerated": total - enumerated,
        "pairs_decided_by_disc": by_disc,
        "pairs_clipped": len(classes),
    }
