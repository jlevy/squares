"""Exact mass of a closed unit square under a mixed cover of the k^2 - 5 board kind (review of #973, L144).

Written here from the definitions: mu(P) = sum_i w_i |{tau in [0,1] : g_i + tau (g'_i - g_i) in P}| + rho |P cap U|.
The pose is centre c and u = tan(theta/2): e1 = ((1-u^2), 2u)/N, e2 = (-2u, 1-u^2)/N, N = 1 + u^2,
P = {z : |(z - c).e_i| <= 1/2}.  Every quantity is a Fraction; a binary64 pre-test only decides segments that are
inside or outside by a margin of 1e-9, far above its rounding error, and everything else is clipped exactly.
The Lebesgue part is the exact area of P clipped to the axis-parallel rectangle U (Sutherland-Hodgman, shoelace).
No code of the source or of evand/square-packing is used.
"""
from bisect import bisect_left, bisect_right
from fractions import Fraction as F

MARGIN = 1e-9


def load_cover(path):
    L = open(path).read().split("\n")
    i = 0
    while not L[i].split() or L[i].startswith("#") or L[i].startswith("mixed"):
        i += 1
    sn, sd = map(int, L[i].split())
    pitch = int(L[i + 1])
    wden = int(L[i + 2])
    if int(L[i + 3]) != 0:
        raise ValueError("points are not supported here")
    n = int(L[i + 4])
    hor, ver = {}, {}
    for j in range(n):
        x0, y0, x1, y1, w = map(int, L[i + 5 + j].split())
        if abs(x1 - x0) + abs(y1 - y0) != 1:
            raise ValueError("the candidate search assumes elementary pieces of length 1/pitch")
        if y0 == y1:
            hor.setdefault(y0, []).append((min(x0, x1), max(x0, x1), w))
        elif x0 == x1:
            ver.setdefault(x0, []).append((min(y0, y1), max(y0, y1), w))
        else:
            raise ValueError("segment not axis-parallel")
    for d in (hor, ver):
        for k in d:
            d[k].sort()
    rest = [ln for ln in L[i + 5 + n:] if ln.strip()]
    rects = []
    for j in range(int(rest[0])):
        v = list(map(int, rest[1 + j].split()))
        xs, ys = v[2::2], v[3::2]
        x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
        if v[0] != 4 or sorted(zip(xs, ys)) != sorted([(x0, y0), (x1, y0), (x1, y1), (x0, y1)]):
            raise ValueError("only axis-parallel rectangles")
        area = F((x1 - x0) * (y1 - y0), pitch * pitch)
        rects.append((F(x0, pitch), F(x1, pitch), F(y0, pitch), F(y1, pitch), F(v[1], wden) / area))
    hkeys, vkeys = sorted(hor), sorted(ver)
    hstart = {k: [s[0] for s in hor[k]] for k in hor}
    vstart = {k: [s[0] for s in ver[k]] for k in ver}
    return dict(side=F(sn, sd), pitch=pitch, wden=wden, hor=hor, ver=ver, hkeys=hkeys, vkeys=vkeys,
                hstart=hstart, vstart=vstart, rects=rects)


def _interval(p0, d, half):
    """{tau in [0,1] : -half <= p0 + tau d <= half} as (lo, hi) or None (exact)"""
    if d == 0:
        return (F(0), F(1)) if -half <= p0 <= half else None
    a, b = (-half - p0) / d, (half - p0) / d
    if a > b:
        a, b = b, a
    lo, hi = max(a, F(0)), min(b, F(1))
    return (lo, hi) if lo <= hi else None


def _seg_len(gx, gy, hx, hy, cx, cy, n1, n2, half):
    """exact length fraction of segment g->h inside P; N e_i = n_i"""
    lo, hi = F(0), F(1)
    for (ax, ay) in (n1, n2):
        p0 = (gx - cx) * ax + (gy - cy) * ay
        d = (hx - gx) * ax + (hy - gy) * ay
        iv = _interval(p0, d, half)
        if iv is None:
            return F(0)
        lo, hi = max(lo, iv[0]), min(hi, iv[1])
        if lo > hi:
            return F(0)
    return hi - lo


def _clip(poly, inside, cross):
    out = []
    for k in range(len(poly)):
        a, b = poly[k - 1], poly[k]
        ia, ib = inside(a), inside(b)
        if ib:
            if not ia:
                out.append(cross(a, b))
            out.append(b)
        elif ia:
            out.append(cross(a, b))
    return out


def rect_area(verts, x0, x1, y0, y1):
    def cx(v):
        return lambda a, b: (v, a[1] + (b[1] - a[1]) * (v - a[0]) / (b[0] - a[0]))

    def cy(v):
        return lambda a, b: (a[0] + (b[0] - a[0]) * (v - a[1]) / (b[1] - a[1]), v)
    poly = verts
    for inside, cross in ((lambda p: p[0] >= x0, cx(x0)), (lambda p: p[0] <= x1, cx(x1)),
                          (lambda p: p[1] >= y0, cy(y0)), (lambda p: p[1] <= y1, cy(y1))):
        poly = _clip(poly, inside, cross)
        if not poly:
            return F(0)
    s = F(0)
    for k in range(len(poly)):
        a, b = poly[k - 1], poly[k]
        s += a[0] * b[1] - b[0] * a[1]
    return abs(s) / 2


def mass(cv, cx, cy, u, detail=False):
    """exact mu(P) for the pose (cx, cy, u); cx, cy, u Fractions"""
    cx, cy, u = F(cx), F(cy), F(u)
    N = 1 + u * u
    n1 = (1 - u * u, 2 * u)           # N e1
    n2 = (-2 * u, 1 - u * u)          # N e2
    half = N / 2
    fx, fy, fn1, fn2, fh = float(cx), float(cy), (float(n1[0]), float(n1[1])), (float(n2[0]), float(n2[1])), float(half)
    pitch = cv["pitch"]
    reach = 0.72
    tot = F(0)
    exact_n = 0
    parts = [] if detail else None
    for orient in ("h", "v"):
        keys = cv["hkeys"] if orient == "h" else cv["vkeys"]
        lines = cv["hor"] if orient == "h" else cv["ver"]
        starts = cv["hstart"] if orient == "h" else cv["vstart"]
        lc, ac = (fy, fx) if orient == "h" else (fx, fy)
        lo_line = bisect_left(keys, int((lc - reach) * pitch) - 1)
        hi_line = bisect_right(keys, int((lc + reach) * pitch) + 1)
        for line in keys[lo_line:hi_line]:
            segs = lines[line]
            st = starts[line]
            j0 = bisect_left(st, int((ac - reach) * pitch) - 2)
            j1 = bisect_right(st, int((ac + reach) * pitch) + 1)
            for s0, s1, w in segs[j0:j1]:
                if orient == "h":
                    g, h = (s0 / pitch, line / pitch), (s1 / pitch, line / pitch)
                else:
                    g, h = (line / pitch, s0 / pitch), (line / pitch, s1 / pitch)
                # binary64 pre-test with a margin
                state = "in"
                for (ax, ay) in (fn1, fn2):
                    pa = (g[0] - fx) * ax + (g[1] - fy) * ay
                    pb = (h[0] - fx) * ax + (h[1] - fy) * ay
                    if (pa > fh + MARGIN and pb > fh + MARGIN) or (pa < -fh - MARGIN and pb < -fh - MARGIN):
                        state = "out"
                        break
                    if not (-fh + MARGIN < pa < fh - MARGIN and -fh + MARGIN < pb < fh - MARGIN):
                        state = "exact"
                if state == "out":
                    continue
                if state == "in":
                    frac = F(1)
                else:
                    exact_n += 1
                    if orient == "h":
                        frac = _seg_len(F(s0, pitch), F(line, pitch), F(s1, pitch), F(line, pitch), cx, cy, n1, n2, half)
                    else:
                        frac = _seg_len(F(line, pitch), F(s0, pitch), F(line, pitch), F(s1, pitch), cx, cy, n1, n2, half)
                if frac:
                    contrib = frac * F(w, cv["wden"])
                    tot += contrib
                    if detail:
                        parts.append((orient, line, s0, s1, w, contrib))
    e1 = (n1[0] / N, n1[1] / N)
    e2 = (n2[0] / N, n2[1] / N)
    verts = [(cx + a * e1[0] / 2 + b * e2[0] / 2, cy + a * e1[1] / 2 + b * e2[1] / 2) for a, b in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
    area_part = F(0)
    for x0, x1, y0, y1, rho in cv["rects"]:
        if float(x0) > fx + reach or float(x1) < fx - reach or float(y0) > fy + reach or float(y1) < fy - reach:
            continue
        area_part += rho * rect_area(verts, x0, x1, y0, y1)
    tot += area_part
    if detail:
        return tot, parts, area_part, exact_n
    return tot


def admissible(side, cx, cy, u):
    """the closed unit square lies in [0, side]^2 (u in [0, 1))"""
    w = (1 + 2 * u - u * u) / (1 + u * u) if u >= 0 else (1 - 2 * u - u * u) / (1 + u * u)
    return w / 2 <= cx <= side - w / 2 and w / 2 <= cy <= side - w / 2
