"""A213b differential test 2 -- FUZZ the rectangle-obstacle clip: random convex rational obstacles (1e-9 grid like a
certified K', and core-like vertices over 2^28 * q), random tilt sub-bins (on the t-grid and after several halvings),
random rects, and points chosen ON the decision boundaries; assert
    multibox.dead_poly            == pinclip_int.dead_poly            (the exact test)
    multibox._dead_poly_f         == pinclip_int.dead_poly_f          (bit-identical float twin)
    multibox._clip_rect_obstacle  == pinclip_int.clip_rect_obstacle   (rect, stats and trace)
   python tests/fuzz_clip213.py [ncases] [seed]
"""
import math
import os
import random
import sys
import time
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
CODE = os.path.abspath(os.path.join(HERE, "..", "code"))
sys.path.insert(0, CODE)
import pinclip_int as PI                                       # noqa: E402
import multibox as MB                                          # noqa: E402

VDEN = 10 ** 9
E = 1 << 24


def hull(pts):
    """ccw convex hull of exact rational points (monotone chain)."""
    P = sorted(set(pts))
    if len(P) < 3:
        return P

    def cr(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo = []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(P):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def rand_obstacle(rng, kind):
    cx = Fr(rng.randrange(12 * VDEN // 10, 28 * VDEN // 10), VDEN)
    cy = Fr(rng.randrange(12 * VDEN // 10, 28 * VDEN // 10), VDEN)
    den = VDEN if kind == "poly" else (1 << 28) * rng.choice([1, 3, 7, 1000003])
    n = rng.randrange(4, 13)
    R = rng.uniform(0.05, 0.45)
    pts = []
    for _ in range(n):
        a = rng.uniform(0, 6.283185307179586)
        r = R * rng.uniform(0.3, 1.0)
        pts.append((cx + Fr(int(r * math.cos(a) * den), den), cy + Fr(int(r * math.sin(a) * den), den)))
    h = hull(pts)
    if len(h) < 3:
        return None
    return MB.Obstacle(h, name="f", kind=kind), cx, cy


def rand_bin(rng):
    k = rng.randrange(0, 12)
    t0 = Fr(rng.randrange(0, E - 4096), E)
    w = Fr(rng.randrange(1, 4096), E)
    t1 = t0 + w
    for _ in range(k):                                          # the coarse tree halves t at every t-split
        m = (t0 + t1) / 2
        if rng.random() < 0.5:
            t1 = m
        else:
            t0 = m
    return MB.Bin(t0, t1)


def rand_rect(rng, cx, cy, sc):
    x0 = cx + Fr(rng.randrange(-int(sc * VDEN), int(sc * VDEN)), VDEN)
    y0 = cy + Fr(rng.randrange(-int(sc * VDEN), int(sc * VDEN)), VDEN)
    w = Fr(rng.randrange(1, int(sc * VDEN)), VDEN)
    h = Fr(rng.randrange(1, int(sc * VDEN)), VDEN)
    return (x0, x0 + w, y0, y0 + h)


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 213
    rng = random.Random(seed)
    bad = pts = clips = 0
    tq = tqi = tf = tfi = tc = tci = 0.0
    npts = nclip = 0
    kinds = {"poly": 0, "core": 0}
    for case in range(n):
        kind = "poly" if rng.random() < 0.6 else "core"
        ob = rand_obstacle(rng, kind)
        if ob is None:
            continue
        obs, cx, cy = ob
        kinds[kind] += 1
        bn = rand_bin(rng)
        # ---- the point tests (random + boundary-seeking: the corners of random rects)
        P = []
        for _ in range(14):
            P.append((cx + Fr(rng.randrange(-700000000, 700000000), VDEN),
                      cy + Fr(rng.randrange(-700000000, 700000000), VDEN)))
        for (px, py) in obs.verts[:4]:                          # exactly ON the obstacle's vertices
            P.append((px, py))
            P.append((px + Fr(1, VDEN), py - Fr(1, VDEN)))
        for (px, py) in P:
            t = time.perf_counter()
            a = MB.dead_poly(px, py, obs, bn)
            tq += time.perf_counter() - t
            t = time.perf_counter()
            b = PI.dead_poly(px, py, obs, bn)
            tqi += time.perf_counter() - t
            fx, fy = float(px), float(py)
            t = time.perf_counter()
            c = MB._dead_poly_f(fx, fy, obs, bn)
            tf += time.perf_counter() - t
            t = time.perf_counter()
            d = PI.dead_poly_f(fx, fy, obs, bn)
            tfi += time.perf_counter() - t
            npts += 1
            if a != b or c != d:
                bad += 1
                pts += 1
                print("MISMATCH point %r: exact lib %r int %r | float lib %r int %r" % ((px, py), a, b, c, d))
        # ---- the clip itself
        for _ in range(3):
            rect = rand_rect(rng, cx, cy, 0.6)
            s1, s2 = {"exact_calls": 0, "backoffs": 0}, {"exact_calls": 0, "backoffs": 0}
            tr1, tr2 = [], []
            t = time.perf_counter()
            r1 = MB._clip_rect_obstacle(rect, obs, bn, s1, trace=tr1, tag="f")
            tc += time.perf_counter() - t
            t = time.perf_counter()
            r2 = PI.clip_rect_obstacle(rect, obs, bn, s2, trace=tr2, tag="f")
            tci += time.perf_counter() - t
            nclip += 1
            PI.FILTER = True
            s3, tr3 = {"exact_calls": 0, "backoffs": 0}, []
            r3 = PI.clip_rect_obstacle(rect, obs, bn, s3, trace=tr3, tag="f")
            PI.FILTER = False
            if r3 != r1 or s3 != s1 or tr3 != tr1:
                bad += 1
                clips += 1
                print("MISMATCH clip (float filter) %r: lib %r %r vs filtered %r %r" % (rect, r1, s1, r3, s3))
            if r1 != r2 or s1 != s2 or tr1 != tr2:
                bad += 1
                clips += 1
                print("MISMATCH clip %r:\n  lib  %r %r\n  int  %r %r\n  tr1 %r\n  tr2 %r"
                      % (rect, r1, s1, r2, s2, tr1, tr2))
    print("A213b fuzz: %d cases (%d poly, %d core), %d point tests, %d clips -- %d mismatches (%d point, %d clip)"
          % (n, kinds["poly"], kinds["core"], npts, nclip, bad, pts, clips))
    print("  dead_poly    library %.1f us  integer %.1f us  x%.1f" % (1e6 * tq / max(npts, 1), 1e6 * tqi / max(npts, 1), tq / max(tqi, 1e-12)))
    print("  _dead_poly_f library %.1f us  hoisted %.1f us  x%.1f" % (1e6 * tf / max(npts, 1), 1e6 * tfi / max(npts, 1), tf / max(tfi, 1e-12)))
    print("  clip         library %.2f ms  integer %.2f ms  x%.1f" % (1e3 * tc / max(nclip, 1), 1e3 * tci / max(nclip, 1), tc / max(tci, 1e-12)))
    print("  pinclip_int.rep() %r" % (PI.rep(),))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
