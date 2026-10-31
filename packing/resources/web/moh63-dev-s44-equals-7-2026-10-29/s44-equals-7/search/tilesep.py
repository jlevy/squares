#!/usr/bin/env python3
"""tilesep.py -- near-tile separation for a mixed cover of [0,S]^2  [measured tool; not a proof].

Poses near an axis-parallel unit tile centered at (i+1/2, j+1/2) with small tilt th have narrow valleys of low captured
mass along (dx, dy) ~ th * (t, u).  The lattice separator (pitch 0.01, 0.5 deg) misses them.  Here: for every tile in
the D4 octant (i <= j <= (n-1)/2), both tilt signs, th on a geometric grid, scan (t, u) = (dx/th, dy/th) on a grid,
keep admissible poses, then polish the worst ones by random local search.  Output: violated poses (cx cy th).
usage: tilesep.py COVER OUT [thr]
"""
import sys, os, math, time, numpy as np
sys.path.insert(0, '/home/claude/sq/work/s44/tools')
import line_cover as LC
import closed4 as C

S = float(os.environ.get('SIDE', '7'))
cov = LC.cover_from_file(sys.argv[1])[0]
OUT = sys.argv[2]
THR = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
n = int(round(S))
rng = np.random.default_rng(1)


def local(cx, cy):
    sel = (np.abs(cov.P[:, 0] - cx) < 1.0) & (np.abs(cov.P[:, 1] - cy) < 1.0)
    c = LC.Cover.__new__(LC.Cover); c.s = cov.s; c.P = cov.P[sel]; c.w = cov.w[sel]; c.lines = cov.lines
    c.segs = cov.segs; c.sw = cov.sw
    return c


def admissible(Q):
    w = np.abs(np.cos(Q[:, 2])) + np.abs(np.sin(Q[:, 2]))
    lo = w / 2; hi = S - w / 2
    return (Q[:, 0] >= lo) & (Q[:, 0] <= hi) & (Q[:, 1] >= lo) & (Q[:, 1] <= hi)


def clip(Q):
    w = np.abs(np.cos(Q[:, 2])) + np.abs(np.sin(Q[:, 2])); lo = w / 2 + 1e-12; hi = S - w / 2 - 1e-12
    Q[:, 0] = np.clip(Q[:, 0], lo, hi); Q[:, 1] = np.clip(Q[:, 1], lo, hi)
    return Q


ths = np.geomspace(1e-5, 0.05, 36)
G = np.arange(-0.8, 0.8 + 1e-9, 0.02)
T, U = np.meshgrid(G, G, indexing='ij'); T = T.ravel(); U = U.ravel()
found = []
t0 = time.time()
for i in range(n):
    for j in range(i, n):
        if j > (n - 1) / 2 + 1e-9: continue
        cx0, cy0 = i + 0.5, j + 0.5
        lc = local(cx0, cy0)
        seeds = []
        for sg in (1, -1):
            for th in ths:
                Q = np.c_[cx0 + th * T, cy0 + th * U, np.full(len(T), sg * th)]
                Q = clip(Q)          # wall tiles: push onto the admissible boundary (where the valleys are)
                v = lc.mass(Q)
                o = np.argsort(v)[:6]
                for k in o: seeds.append((v[k], *Q[k]))
        seeds.sort()
        seeds = np.array(seeds[:60])
        cur = seeds[:, 1:].copy(); curv = seeds[:, 0].copy()
        for r in range(10):
            rad = 0.3 ** r
            m = len(cur); Q = np.repeat(cur, 48, axis=0)
            th = np.abs(Q[:, 2]) + 1e-9
            d = rng.normal(size=Q.shape)
            Q[:, 0] += d[:, 0] * th * 0.2 * rad; Q[:, 1] += d[:, 1] * th * 0.2 * rad
            Q[:, 2] *= np.exp(d[:, 2] * 0.3 * rad)
            Q = clip(Q); v = lc.mass(Q)
            V = v.reshape(m, 48); a = V.argmin(1); b = V[np.arange(m), a] < curv
            cur[b] = Q.reshape(m, 48, 3)[np.arange(m), a][b]; curv[b] = V[np.arange(m), a][b]
            bad = v < THR
            for q, vv in zip(Q[bad], v[bad]): found.append((vv, *q))
        for q, vv in zip(cur, curv):
            if vv < THR: found.append((vv, *q))
        print(f'tile ({i},{j}) min {curv.min():.6f}  ({time.time() - t0:.0f}s)', flush=True)

F = np.array(found).reshape(-1, 4)
if len(F):
    # verify with the full cover, dedupe
    F = F[admissible(F[:, 1:])]
    v = cov.mass(F[:, 1:]); F[:, 0] = v; F = F[v < THR]
    key = np.c_[np.round(F[:, 1] / 1e-5), np.round(F[:, 2] / 1e-5), np.round(F[:, 3] / 1e-6)]
    _, idx = np.unique(key, axis=0, return_index=True); F = F[np.sort(idx)]
    F = F[np.argsort(F[:, 0])][:3000]
np.savetxt(OUT, F[:, 1:] if len(F) else np.zeros((0, 3)), fmt='%.12f')
print(f'violations {len(F)}  min {F[:, 0].min() if len(F) else 1:.6f}', flush=True)
