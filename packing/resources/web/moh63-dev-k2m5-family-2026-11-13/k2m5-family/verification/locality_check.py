#!/usr/bin/env python3
"""Exact check of the locality premise of the family reduction, written from scratch (no shared code with the
generator or the checkers).

Every closed unit square has a bounding box of width <= sqrt(2), so it lies in a window of side 1.6 whose corner
is on the 1/10 grid (corner at floor(10 x_min)/10, floor(10 y_min)/10, moved inward if needed to stay in [0, k]).
If every such window of mu_k equals, after a translation by an integer vector, a window of mu_11 (same segment mass
piece by piece on the 1/10 grid, same Lebesgue region), then every unit square in [0, k]^2 has the mass of a unit
square in [0, 11]^2.  Integer translations are the symmetry of the period-1 wall pattern.

usage: locality_check.py BOX11 BOXK [BOXK ...]
"""
import sys
from fractions import Fraction as F


def load(path):
    L = [l.split() for l in open(path) if l.strip() and not l.startswith('#')]
    assert L[0] == ['mixed', '1']
    k = F(int(L[1][0]), int(L[1][1])); D = int(L[2][0]); W = int(L[3][0])
    i = 4; npt = int(L[i][0]); i += 1
    assert npt == 0, 'family covers have no points'
    nsg = int(L[i][0]); i += 1
    segs = {}
    for t in range(nsg):
        x0, y0, x1, y1, w = map(int, L[i + t])
        assert x0 == x1 or y0 == y1, 'axis-parallel segments only'
        # split into pieces of length 1/D on the D-grid, mass spread evenly
        if x0 == x1:
            a, b = sorted((y0, y1)); n = b - a
            for s in range(a, b): segs[('v', x0, s)] = segs.get(('v', x0, s), 0) + F(w, W * n)
        else:
            a, b = sorted((x0, x1)); n = b - a
            for s in range(a, b): segs[('h', y0, s)] = segs.get(('h', y0, s), 0) + F(w, W * n)
    i += nsg
    npg = int(L[i][0]); i += 1
    assert npg == 1
    p = L[i]; nv = int(p[0]); w = F(int(p[1]), W)
    xs = [int(v) for v in p[2::2]]; ys = [int(v) for v in p[3::2]]
    assert nv == 4 and len(set(xs)) == 2 and len(set(ys)) == 2, 'one axis-parallel rectangle'
    rect = (min(xs), max(xs), min(ys), max(ys))
    area = F(rect[1] - rect[0], D) * F(rect[3] - rect[2], D)
    assert w == area, f'polygon mass {w} is not its area {area}: density must be 1'
    return k, D, {key: m for key, m in segs.items() if m != 0}, rect


L = 16          # window side in grid units (1/D): any unit square's bounding box (width <= sqrt 2) starting in
                # [i/D, (i+1)/D) ends before (i + 1)/D + 1.4143 < (i + 16)/D, so it lies in [i/D, (i+16)/D]


def index(cov):
    k, D, segs, rect = cov
    assert D == 10
    cells = {}
    for (o, c, s), m in segs.items():
        cells.setdefault((o, c, s), m)
    return cells


def window(cov, cells, i, j):
    k, D, segs, rect = cov
    x0, y0, x1, y1 = i, j, i + L, j + L
    out = []
    for c in range(x0, x1 + 1):
        for s in range(y0, y1):
            m = cells.get(('v', c, s))
            if m: out.append(('v', c - x0, s - y0, m))
    for c in range(y0, y1 + 1):
        for s in range(x0, x1):
            m = cells.get(('h', c, s))
            if m: out.append(('h', c - y0, s - x0, m))
    rx0, rx1, ry0, ry1 = rect
    lx0, lx1, ly0, ly1 = max(rx0, x0), min(rx1, x1), max(ry0, y0), min(ry1, y1)
    leb = (lx0 - x0, lx1 - x0, ly0 - y0, ly1 - y0) if lx0 < lx1 and ly0 < ly1 else None
    return (tuple(out), leb)


def windows(cov):
    k = int(cov[0]); cells = index(cov); n = 10 * k - L   # i in 0..n keeps the window inside [0, k]
    for i in range(n + 1):
        for j in range(n + 1):
            yield i, j, window(cov, cells, i, j)


base = load(sys.argv[1]); assert base[0] == 11 and base[1] == 10
ref = {(i % 10, j % 10, w) for i, j, w in windows(base)}
print(f'mu_11: {len(base[2])} segment pieces, Lebesgue {base[3]}; {len(ref)} distinct windows (side {L}/10, up to integer shifts)')
ok_all = True
for p in sys.argv[2:]:
    cov = load(p); k = int(cov[0])
    tot = 0; miss = []
    for i, j, w in windows(cov):
        tot += 1
        if (i % 10, j % 10, w) not in ref: miss.append((i, j))
    print(f'mu_{k}: {tot} windows, without an integer-translate in mu_11: {len(miss)}' + (f' e.g. {miss[:5]}' if miss else ''))
    ok_all &= not miss
print('LOCALITY OK' if ok_all else 'LOCALITY FAILED')
