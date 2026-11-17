#!/usr/bin/env python3
"""Float stress test of a family box cover (segments + one Lebesgue rectangle), written from scratch.
mu(Q) = sum over segments of density * length(segment inside Q) + area(Q inside the Lebesgue rectangle).
Samples random poses, poses near grid tiles at small tilts, and near-45-degree poses; reports the minimum.
usage: stress_family.py FILE N"""
import math, sys
import numpy as np

L = [l.split() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
S = int(L[1][0]) / int(L[1][1]); D = int(L[2][0]); W = int(L[3][0])
i = 4; assert int(L[i][0]) == 0; i += 1
nsg = int(L[i][0]); i += 1
G = np.array([list(map(int, L[i + t])) for t in range(nsg)], float); i += nsg
assert int(L[i][0]) == 1; p = list(map(int, L[i + 1]))
xs, ys = p[2::2], p[3::2]; RX0, RX1, RY0, RY1 = min(xs) / D, max(xs) / D, min(ys) / D, max(ys) / D
vert = G[:, 0] == G[:, 2]
A = np.where(vert, G[:, 0], G[:, 1]) / D
T0 = np.where(vert, np.minimum(G[:, 1], G[:, 3]), np.minimum(G[:, 0], G[:, 2])) / D
T1 = np.where(vert, np.maximum(G[:, 1], G[:, 3]), np.maximum(G[:, 0], G[:, 2])) / D
RHO = (G[:, 4] / W) / (T1 - T0)
X0 = np.where(vert, A, 0.0); Y0 = np.where(vert, 0.0, A)
EX = np.where(vert, 0.0, 1.0); EY = np.where(vert, 1.0, 0.0)


def clip_area(cx, cy, th):
    c, s = math.cos(th), math.sin(th)
    poly = [(cx + c * u - s * v, cy + s * u + c * v) for u, v in ((-.5, -.5), (.5, -.5), (.5, .5), (-.5, .5))]
    for (ax, ay, keep) in ((RX0, None, 'ge'), (RX1, None, 'le'), (None, RY0, 'ge'), (None, RY1, 'le')):
        out = []
        for k in range(len(poly)):
            P, Q = poly[k], poly[(k + 1) % len(poly)]
            fp = (P[0] - ax if ax is not None else P[1] - ay); fq = (Q[0] - ax if ax is not None else Q[1] - ay)
            if keep == 'le': fp, fq = -fp, -fq
            if fp >= 0: out.append(P)
            if (fp >= 0) != (fq >= 0):
                t = fp / (fp - fq); out.append((P[0] + t * (Q[0] - P[0]), P[1] + t * (Q[1] - P[1])))
        poly = out
        if not poly: return 0.0
    return 0.5 * abs(sum(poly[k][0] * poly[(k + 1) % len(poly)][1] - poly[(k + 1) % len(poly)][0] * poly[k][1]
                         for k in range(len(poly))))


def mass(cx, cy, th):
    c, s = math.cos(th), math.sin(th)
    lo, hi = T0.copy(), T1.copy()
    for k1, k2 in ((c, s), (-s, c)):
        base = (X0 - cx) * k1 + (Y0 - cy) * k2; slope = EX * k1 + EY * k2
        with np.errstate(divide='ignore', invalid='ignore'):
            r1 = (-0.5 - base) / slope; r2 = (0.5 - base) / slope
        lo = np.maximum(lo, np.where(slope != 0, np.minimum(r1, r2), np.where(np.abs(base) <= 0.5, -np.inf, np.inf)))
        hi = np.minimum(hi, np.where(slope != 0, np.maximum(r1, r2), np.where(np.abs(base) <= 0.5, np.inf, -np.inf)))
    return float((RHO * np.clip(hi - lo, 0, None)).sum()) + clip_area(cx, cy, th)


rng = np.random.default_rng(2026); N = int(sys.argv[2])
def run(name, gen):
    best = (9, None)
    for _ in range(N):
        cx, cy, th = gen(); w = abs(math.cos(th)) + abs(math.sin(th))
        cx = min(max(cx, w / 2), S - w / 2); cy = min(max(cy, w / 2), S - w / 2)
        v = mass(cx, cy, th)
        if v < best[0]: best = (v, (round(cx, 5), round(cy, 5), round(math.degrees(th), 4)))
    print(f'{name}: {N} poses, min mass {best[0]:.10f} (min - 1 = {best[0] - 1:.2e}) at {best[1]}', flush=True)
run('random', lambda: (rng.uniform(0, S), rng.uniform(0, S), rng.uniform(0, math.pi / 2)))
def near_tile():
    i, j = rng.integers(0, int(S), 2); t = 10 ** rng.uniform(-6, -1) * rng.choice([-1, 1])
    return i + .5 + t * rng.uniform(-1, 1), j + .5 + t * rng.uniform(-1, 1), t
run('near-tile', near_tile)
run('near-45', lambda: (rng.uniform(0, S), rng.uniform(0, S), math.pi / 4 + rng.choice([-1, 1]) * 10 ** rng.uniform(-7, -1)))
