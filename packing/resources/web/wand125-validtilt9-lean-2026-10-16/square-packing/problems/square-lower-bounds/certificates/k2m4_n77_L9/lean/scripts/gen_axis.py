#!/usr/bin/env python3
"""AXIS leaves (Lemma Z, `LemmaZ.lean`) for a mixed cover: an exact mirror of `axOk`.

For a box of centres [x0, x1] x [y0, y1] (over Q = D*S) at theta = 0 it claims every point, axis-parallel
segment and rectangle that `axOk` can use, and evaluates `axVal` at the four corners.

    gen_axis.py COVER S x0 x1 y0 y1        # report one box
"""
import sys
from math import lcm


def read_cover(path):
    toks = []
    for line in open(path):
        line = line.split('#')[0].strip()
        if line:
            toks.append(line.split())
    it = iter(toks)
    assert next(it)[0] == 'mixed'
    side = next(it)
    D = int(next(it)[0]); W = int(next(it)[0])
    pts = [tuple(map(int, next(it))) for _ in range(int(next(it)[0]))]
    segs = []
    for _ in range(int(next(it)[0])):
        a, b, c, d, w = map(int, next(it))
        if (a, b) > (c, d):
            a, b, c, d = c, d, a, b
        segs.append((a, b, c, d, w))
    rects = []
    for _ in range(int(next(it)[0])):
        t = list(map(int, next(it)))
        k, w, vs = t[0], t[1], t[2:]
        xs, ys = vs[0::2], vs[1::2]
        X0, X1, Y0, Y1 = min(xs), max(xs), min(ys), max(ys)
        assert k == 4 and sorted(zip(xs, ys)) == sorted([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)])
        area = (X1 - X0) * (Y1 - Y0)
        assert (w * D * D) % area == 0, "density must be an integer over W"
        rects.append((X0, Y0, X1, Y1, w * D * D // area))
    return side, D, W, pts, segs, rects


def clampZ(h, A, B, t):
    return max(0, min(B, t + h) - max(A, t - h))


def capX(D, S, x0, x1, X):
    return 2 * X * S <= 2 * x0 + D * S and 2 * x1 <= 2 * X * S + D * S


def bpOk(D, S, x0, x1, A, B):
    return all(b <= 2 * x0 or 2 * x1 <= b
               for b in (2*A*S - D*S, 2*A*S + D*S, 2*B*S - D*S, 2*B*S + D*S))


def axVal(D, S, Lc, cps, chs, cvs, crs, x, y):
    v = sum(p[2] * 4 * D * D * S * S * Lc for p in cps)
    v += sum(e[4] * clampZ(D*S, 2*e[0]*S, 2*e[2]*S, 2*x) * 2*D*D*S*(Lc // (e[2]-e[0])) for e in chs)
    v += sum(e[4] * clampZ(D*S, 2*e[1]*S, 2*e[3]*S, 2*y) * 2*D*D*S*(Lc // (e[3]-e[1])) for e in cvs)
    v += sum(r[4] * clampZ(D*S, 2*r[0]*S, 2*r[2]*S, 2*x) * clampZ(D*S, 2*r[1]*S, 2*r[3]*S, 2*y) * Lc
             for r in crs)
    return v


def claim(D, S, W, x0, x1, y0, y1, pts, segs, rects):
    corners = [(x0, y0), (x0, y1), (x1, y0), (x1, y1)]
    cps = [p for p in pts if capX(D, S, x0, x1, p[0]) and capX(D, S, y0, y1, p[1])]
    chs, cvs = [], []
    for e in segs:
        if e[1] == e[3] and e[0] < e[2] and capX(D, S, y0, y1, e[1]) and bpOk(D, S, x0, x1, e[0], e[2]):
            if any(clampZ(D*S, 2*e[0]*S, 2*e[2]*S, 2*x) > 0 for x, _ in corners):
                chs.append(e)
        elif e[0] == e[2] and e[1] < e[3] and capX(D, S, x0, x1, e[0]) and bpOk(D, S, y0, y1, e[1], e[3]):
            if any(clampZ(D*S, 2*e[1]*S, 2*e[3]*S, 2*y) > 0 for _, y in corners):
                cvs.append(e)
    crs = [r for r in rects if bpOk(D, S, x0, x1, r[0], r[2]) and bpOk(D, S, y0, y1, r[1], r[3])]
    Lc = 1
    for e in chs:
        Lc = lcm(Lc, e[2] - e[0])
    for e in cvs:
        Lc = lcm(Lc, e[3] - e[1])
    K = 4 * D * D * S * S * Lc
    vals = [axVal(D, S, Lc, cps, chs, cvs, crs, x, y) for x, y in corners]
    return Lc, cps, chs, cvs, crs, vals, [W * K <= v for v in vals], K


if __name__ == '__main__':
    path, S, x0, x1, y0, y1 = sys.argv[1], *map(int, sys.argv[2:])
    side, D, W, pts, segs, rects = read_cover(path)
    Lc, cps, chs, cvs, crs, vals, ok, K = claim(D, S, W, x0, x1, y0, y1, pts, segs, rects)
    print(f"D={D} W={W} S={S} box=[{x0},{x1}]x[{y0},{y1}]/{D*S}: {len(cps)} pts, {len(chs)}+{len(cvs)} segs, "
          f"{len(crs)} rects, Lc={Lc}")
    for v, o in zip(vals, ok):
        print(f"  corner mass {v / K / W:.15f}  ok={o}")
