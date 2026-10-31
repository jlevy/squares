#!/usr/bin/env python3
"""Float stress test of a mixed cover, written from scratch (no shared code with the exact checkers) [measured].
Evaluates mu(Q) for many admissible closed unit squares Q in [0,7]^2: random poses, near-tile poses at small tilts,
and 45-degree poses.  Points count if inside the closed square (tolerance +1e-12); segments contribute
density * (length of the segment inside Q).  Reports the minimum found.  usage: stress.py FILE NRANDOM"""
import sys, math, numpy as np

L = [l.split() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
D = int(L[2][0]); W = int(L[3][0]); i = 4; npt = int(L[i][0]); i += 1
P = np.array([list(map(int, L[i + k])) for k in range(npt)], float); i += npt
nsg = int(L[i][0]); i += 1
G = np.array([list(map(int, L[i + k])) for k in range(nsg)], float)
px, py, pw = P[:, 0] / D, P[:, 1] / D, P[:, 2] / W
S = float(L[1][0]) / float(L[1][1])
# segments: (vertical?, line coord, t0, t1, density)
segs = []
for x0, y0, x1, y1, w in G:
    if x0 == x1: segs.append((1, x0 / D, min(y0, y1) / D, max(y0, y1) / D, (w / W) / (abs(y1 - y0) / D)))
    else: segs.append((0, y0 / D, min(x0, x1) / D, max(x0, x1) / D, (w / W) / (abs(x1 - x0) / D)))
segs = np.array(segs)


def mass(cx, cy, th):
    c, s = math.cos(th), math.sin(th)
    # points
    dx = px - cx; dy = py - cy
    u = dx * c + dy * s; v = -dx * s + dy * c
    m = pw[(np.abs(u) <= 0.5 + 1e-12) & (np.abs(v) <= 0.5 + 1e-12)].sum()
    # segments: parametrize the segment line, intersect with the 4 slab constraints |u|<=1/2, |v|<=1/2
    vert = segs[:, 0] == 1; a = segs[:, 1]; t0 = segs[:, 2]; t1 = segs[:, 3]; rho = segs[:, 4]
    # point on line: vertical x=a, y=t ; horizontal y=a, x=t
    X0 = np.where(vert, a, 0.0); Y0 = np.where(vert, 0.0, a)
    ex = np.where(vert, 0.0, 1.0); ey = np.where(vert, 1.0, 0.0)
    lo = t0.copy(); hi = t1.copy()
    for (k1, k2) in ((c, s), (-s, c)):
        base = (X0 - cx) * k1 + (Y0 - cy) * k2; slope = ex * k1 + ey * k2
        with np.errstate(divide='ignore', invalid='ignore'):
            r1 = (-0.5 - 1e-12 - base) / slope; r2 = (0.5 + 1e-12 - base) / slope
        lo_k = np.where(slope != 0, np.minimum(r1, r2), np.where(np.abs(base) <= 0.5 + 1e-12, -np.inf, np.inf))
        hi_k = np.where(slope != 0, np.maximum(r1, r2), np.where(np.abs(base) <= 0.5 + 1e-12, np.inf, -np.inf))
        lo = np.maximum(lo, lo_k); hi = np.minimum(hi, hi_k)
    m += (rho * np.clip(hi - lo, 0, None)).sum()
    return m


rng = np.random.default_rng(12345)
best = (9, None)
def test(cx, cy, th):
    global best
    w = abs(math.cos(th)) + abs(math.sin(th))
    cx = min(max(cx, w / 2), S - w / 2); cy = min(max(cy, w / 2), S - w / 2)
    v = mass(cx, cy, th)
    if v < best[0]: best = (v, (cx, cy, th))
    return v

N = int(sys.argv[2])
for _ in range(N):
    test(rng.uniform(0, S), rng.uniform(0, S), rng.uniform(0, math.pi / 2))
print(f'random {N}: min {best[0]:.6f} at {best[1]}', flush=True)
r0 = best[0]; best = (9, None)
for _ in range(N):
    i, j = rng.integers(0, 7, 2); th = 10 ** rng.uniform(-6, -1) * rng.choice([-1, 1])
    test(i + 0.5 + th * rng.uniform(-1, 1), j + 0.5 + th * rng.uniform(-1, 1), th)
print(f'near-tile {N}: min {best[0]:.6f} at {best[1]}', flush=True)
best = (9, None)
for _ in range(N // 4):
    test(rng.uniform(0, S), rng.uniform(0, S), math.pi / 4 + rng.choice([-1, 1]) * 10 ** rng.uniform(-7, -1))
print(f'near-45 {N // 4}: min {best[0]:.6f} at {best[1]}', flush=True)
